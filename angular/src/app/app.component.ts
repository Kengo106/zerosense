import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Game } from './race.interface';
import { GameService } from './service/game.service';
import { SessionService } from './service/session.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
    title = 'zerosense';
    date: any;
    currentGame: Game = {
        id: '',
        gamename: '',
        start: '',
        end: '',
    };

    // existGame: number = 0;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private gameService: GameService,
        private sessionService: SessionService,
    ) {}
    ngOnInit(): void {
        console.log(this.currentGame);
        this.gameService.gameSubject.subscribe((game) => {
            this.currentGame = game;
            console.log(this.currentGame);
        });
    }
    moveGameMain(game: Game) {
        this.router.navigate(['/gamemain'], { queryParams: game });
    }

    switchRoute() {
        this.sessionService.loginState$.subscribe((islogin) => {
            if (islogin) {
                this.router.navigate(['']);
            } else {
                this.router.navigate(['/account/login/']);
            }
        });
    }
}
