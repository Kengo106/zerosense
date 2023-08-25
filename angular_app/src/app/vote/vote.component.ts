import { Component } from '@angular/core';
import { Race } from '../race.interface';
import { ActivatedRoute, Router } from '@angular/router';
import { RaceService } from '../service/race.service';

@Component({
    selector: 'app-vote',
    templateUrl: './vote.component.html',
    styleUrls: ['./vote.component.scss'],
})
export class VoteComponent {
    public race: Race = {
        grade: '',
        name: '',
        date: '',
    };
    constructor(private route: ActivatedRoute, private raceServise: RaceService) {
        this.route.queryParams.subscribe((params) => {
            this.race = {
                grade: params['grade'] as string,
                name: params['name'] as string,
                date: params['date'] as string,
            };
        });
        raceServise.getVote(this.race).subscribe();
    }
}
