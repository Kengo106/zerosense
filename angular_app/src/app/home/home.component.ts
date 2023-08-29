import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Race } from '../race.interface';
import { Router } from '@angular/router';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
    public uid: string = '';
    public games: string[] = [];
    public isVotableRace: Race[] = [];
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            console.log(this.uid);
            this.raceService.getCurrentGames(this.uid).subscribe((response) => {
                this.games = [];
                response.map((game: string) => this.games.push(game));
                // console.log(this.games);
            });
        });
        this.raceService.getVotableRaces().subscribe((response: Race[]) => {
            this.isVotableRace = [];
            response.map((race) => this.isVotableRace.push(race));
            // console.log(this.isVotableRace);
        });
    }

    moveVote(race: Race) {
        this.router.navigate(['/vote'], { queryParams: race });
    }
}
