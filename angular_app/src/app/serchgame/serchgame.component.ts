import { Component } from '@angular/core';
import { SessionService } from '../service/session.service';
import { RaceService } from '../service/race.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-serchgame',
    templateUrl: './serchgame.component.html',
    styleUrls: ['./serchgame.component.scss'],
})
export class SerchgameComponent {
    public gameName: string[] = [];
    public uid: string = '';
    gameId: string = '';
    gameNumber: number = 0;

    constructor(
        private sessionService: SessionService,
        private raceService: RaceService,
        private router: Router,
    ) {
        this.sessionService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }
    Serch() {
        this.gameName = [];
        this.raceService.gameSerch(this.gameId).subscribe((responce: any) => {
            this.gameName.push(responce.message.gamename);
            this.gameNumber = this.gameName.length;
        });
    }

    join() {
        const yesNoFlag = window.confirm(`この大会に参加しますか ${this.gameName}`);
        if (yesNoFlag) {
            this.raceService.joinGame(this.gameId, this.uid).subscribe((response) => {
                alert(`${response.message}`);
                if (response.message !== '大会が存在しません') {
                    this.router.navigate(['home/']);
                }
            });
        }
    }
}
