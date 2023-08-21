import { Component } from '@angular/core';
import { RaceService } from '../service/race.service';

@Component({
    selector: 'app-newgame',
    templateUrl: './newgame.component.html',
    styleUrls: ['./newgame.component.scss'],
})
export class NewgameComponent {
    public groupName: string = '';
    public open: boolean = false;

    constructor(private raceServce: RaceService) {}
    onSubmit() {
        this.raceServce.createNewGame(this.groupName, this.open);
    }
}
