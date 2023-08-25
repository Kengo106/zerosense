import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Race } from '../race.interface';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
    public uid: string = '';
    public games: string[] = [];
    public isVotableRace: Race[] = [];
    constructor(private raceService: RaceService, private sessionService: SessionService) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.raceService.getCurrentGames(this.uid).subscribe((response) => {
                response.map((game: string) => this.games.push(game));
            });
        });
        this.raceService.getVotableRaces().subscribe((response: Race[]) => {
            response.map((race) => this.isVotableRace.push(race));
            console.log(this.isVotableRace);
        });
    }
}
