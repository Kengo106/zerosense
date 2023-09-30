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
    AllRaces: Race[] = [];
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
            // console.log(this.uid);
            this.route.queryParams.subscribe((params) => {
                this.game = {
                    gamename: params['gamename'],
                    id: params['id'],
                };
                if (this.game.id != '') {
                    console.log(this.game.id);
                    this.raceService.getAllRaces(this.uid, this.game.id).subscribe((response) => {
                        this.AllRaces = [];
                        response.map((responce) => {
                            this.AllRaces.push(responce);
                        });
                        console.log(this.AllRaces);
                    });
                }
            });
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
