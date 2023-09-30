import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Game, Race } from '../race.interface';
import { Router } from '@angular/router';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
    public uid: string = '';
    public games: Game[] = [];
    public isVotableRace: Race[] = [];
    isLogin: boolean = false;
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
    ) {}
    gameNumber: number = 0;

    ngOnInit() {
        this.sessionService.loginState$.subscribe((login) => {
            this.isLogin = login;
            console.log(this.isLogin);
        });
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.raceService.getCurrentGames(this.uid).subscribe((response) => {
                this.games = [];
                response.map((game: Game) => this.games.push(game));
                console.log(this.games);
                this.gameNumber = this.games.length;
            });
        });
    }

    moveGameMain(game: Game) {
        this.router.navigate(['/gamemain'], { queryParams: game });
    }

    copyID(gameId: string) {
        alert(`大会IDをクリップボードにコピーしました。\n${gameId}`);
    }
}
