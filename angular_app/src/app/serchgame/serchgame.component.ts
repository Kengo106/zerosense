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
    public gameName: string = '';
    public uid: string = '';
    constructor(
        private sessionService: SessionService,
        private raceService: RaceService,
        private router: Router,
    ) {
        this.sessionService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }

    onSubmit() {
        this.raceService.joinGame(this.gameName, this.uid).subscribe((response) => {
            alert(`${response.message}`);
            if (response.message !== '大会が存在しません') {
                this.router.navigate(['home/']);
            }
        });
    }
}
