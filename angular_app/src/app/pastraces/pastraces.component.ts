import { Component } from '@angular/core';
import { Game, Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
    selector: 'app-pastraces',
    templateUrl: './pastraces.component.html',
    styleUrls: ['./pastraces.component.scss'],
})
export class PastracesComponent {
    public uid: string = '';
    game: Game = {
        gamename: '',
        id: '',
    };
    AllRace: Race[] = [];
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private route: ActivatedRoute,
        private location: Location,
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            console.log(this.uid);

            this.raceService.getAllRaces(this.uid).subscribe((response) => {
                this.AllRace = [];
                response.map((responce) => {
                    this.AllRace.push(responce);
                });
                console.log(this.AllRace);
            });
        });
        this.route.queryParams.subscribe((params) => {
            this.game = {
                gamename: params['gamename'],
                id: params['id'],
            };
        });
    }

    moveResult(race: Race) {
        this.router.navigate(['/raceresult'], {
            queryParams: {
                date: race.date,
                racename: race.name,
                grade: race.grade,
                gamename: this.game.gamename,
                id: this.game.id,
            },
        });
    }

    goBack() {
        this.location.back();
    }
}
