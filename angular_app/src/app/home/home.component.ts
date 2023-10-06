import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Game, Race } from '../race.interface';
import { Router } from '@angular/router';
import { GameService } from '../service/game.service';

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
        private gameService: GameService,
    ) {}
    gameNumber: number = 0;
    currentGame: Game = {
        id: '',
        gamename: '',
        start: '',
        end: '',
    };

    ngOnInit() {
        this.sessionService.loginState$.subscribe((login) => {
            this.isLogin = login;
        });
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.raceService.getCurrentGames(this.uid).subscribe((response) => {
                this.games = [];
                response.map((game: Game) => this.games.push(game));
                console.log(this.games);
                this.gameNumber = this.games.length;
            });
            this.gameService.gameSubject.next(this.currentGame);
        });
    }

    moveGameMain(game: Game) {
        this.router.navigate(['/gamemain'], { queryParams: game });
        console.log(game);
    }

    copyID(gameId: string) {
        alert(`大会IDをクリップボードにコピーしました。\n${gameId}`);
    }
}
