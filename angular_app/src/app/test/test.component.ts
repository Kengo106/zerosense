import { Component } from '@angular/core';
import { Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    selector: 'app-test',
    templateUrl: './test.component.html',
    styleUrls: ['./test.component.scss'],
})
export class TestComponent {
    public uid: string = '';
    game: string = '';
    AllRace: Race[] = [];
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            console.log(this.uid);

            // this.raceService.getAllRaces(this.uid,).subscribe((response) => {
            //     this.AllRace = [];
            //     response.map((responce) => {
            //         this.AllRace.push(responce);
            //     });
            //     console.log(this.AllRace);
            // });
        });
        this.route.queryParams.subscribe((params) => {
            this.game = params['gamename'];
        });
    }

    moveVote(race: Race, game: string) {
        this.router.navigate(['/vote'], { queryParams: { ...race, gamename: game } });
    }
}
