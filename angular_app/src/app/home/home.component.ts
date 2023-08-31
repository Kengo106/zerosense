import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Race } from '../race.interface';
import { Router } from '@angular/router';
import { GameService } from '../service/game.service';
import { async } from 'rxjs';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
    public uid: string = '';
    public games: string[] = [];
    public isVotableRace: Race[] = [];
    isLogin: boolean = false;
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private gameService: GameService,
    ) {}

    ngOnInit() {
        this.sessionService.loginState$.subscribe((login) => {
            this.isLogin = login;
            console.log(this.isLogin);
        });
        this.gameService.putGameName(null);
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.raceService.getCurrentGames(this.uid).subscribe((response) => {
                this.games = [];
                response.map((game: string) => this.games.push(game));
            });
        });
    }

    moveGameMain(game: string) {
        this.gameService.putGameName(game);

        this.router.navigate(['/gamemain'], { queryParams: { game: game } });
    }
}
