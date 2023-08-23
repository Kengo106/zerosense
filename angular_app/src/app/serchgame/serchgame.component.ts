import { Component } from '@angular/core';
import { SessionService } from '../service/session.service';
import { RaceService } from '../service/race.service';

@Component({
    selector: 'app-serchgame',
    templateUrl: './serchgame.component.html',
    styleUrls: ['./serchgame.component.scss'],
})
export class SerchgameComponent {
    public gameName: string = '';
    public uid: string = '';
    constructor(private sessionService: SessionService, private raceService: RaceService) {
        this.sessionService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }

    onSubmit() {
        this.raceService
            .joinGame(this.gameName, this.uid)
            .subscribe((response) => alert(`${response.message}`));
    }
}
