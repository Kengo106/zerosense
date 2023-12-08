import { Component, OnInit } from '@angular/core';
import { SessionService } from '../service/session.service';
import { RaceService } from '../service/race.service';
import { Router } from '@angular/router';
import { Game } from '../race.interface';
import { GameService } from '../service/game.service';

@Component({
    selector: 'app-serchgame',
    templateUrl: './serchgame.component.html',
    styleUrls: ['./serchgame.component.scss'],
})
export class SerchgameComponent implements OnInit {
    public gameName: string[] = [];
    public uid: string = '';
    gameId: string = '';
    gameNumber: number = 0;
    gameClear: Game = {
        id: '',
        gamename: '',
        start: '',
        end: '',
    };

    constructor(
        private sessionService: SessionService,
        private raceService: RaceService,
        private router: Router,
        private gameService: GameService,
    ) {}

    ngOnInit(): void {
        this.gameService.gameSubject.next(this.gameClear);
        this.sessionService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }

    Serch() {
        this.raceService.gameSerch(this.gameId).subscribe((responce: any) => {
            this.gameName = [];
            if (responce.message == '大会が存在しません') {
                alert(responce.message);
            } else {
                console.log(responce.message.gamename);
                this.gameName.push(responce.message.gamename);

                this.gameNumber = this.gameName.length;
            }
        });
        console.log(this.gameName);
    }

    join() {
        const yesNoFlag = window.confirm(`この大会に参加しますか ${this.gameName}`);
        if (yesNoFlag) {
            this.raceService.joinGame(this.gameId, this.uid).subscribe((response) => {
                alert(`${response.message}`);
                if (response.message !== '大会が存在しません') {
                    this.router.navigate(['home/']);
                } else {
                    alert(response.message);
                }
            });
        }
    }
}
