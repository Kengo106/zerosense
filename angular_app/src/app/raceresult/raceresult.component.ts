import { Component } from '@angular/core';
import { Race } from '../race.interface';
import { ActivatedRoute, Router } from '@angular/router';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Location } from '@angular/common';

interface Horse {
    id: number;
    place: number;
    name: string;
}

interface VoteForm {
    name: string;
    UID: string;
    first: { place: number; name: string };
    second: { place: number; name: string };
    third: { place: number; name: string };
    comment: string;
    score: number;
}

interface Odds {
    tan: number | null;
    fuku1: number | null;
    fuku2: number | null;
    fuku3: number | null;
    umaren: number | null;
    umatan: number | null;
    wide12: number | null;
    wide13: number | null;
    wide23: number | null;
    trio: number | null;
    tierce: number | null;
}
@Component({
    selector: 'app-raceresult',
    templateUrl: './raceresult.component.html',
    styleUrls: ['./raceresult.component.scss'],
})
export class RaceresultComponent {
    race: Race = {
        grade: '',
        name: '',
        date: '',
        voted: null,
    };
    userName: string = '';
    gameName: string = '';
    uid: string = '';
    voteList: VoteForm[] = [];
    horseList: Horse[] = [];
    odds: Odds = {
        tan: null,
        fuku1: null,
        fuku2: null,
        fuku3: null,
        umaren: null,
        umatan: null,
        wide12: null,
        wide13: null,
        wide23: null,
        trio: null,
        tierce: null,
    };

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private raceService: RaceService,
        private sessionService: SessionService,
        private location: Location,
    ) {}

    ngOnInit() {
        this.route.queryParams.subscribe((params) => (this.gameName = params['gamename']));
        console.log(this.gameName);
        this.sessionService.username$.subscribe((myName) => (this.userName = myName));
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.route.queryParams.subscribe((params) => {
                this.race = {
                    grade: params['grade'] as string,
                    name: params['name'] as string,
                    date: params['date'] as string,
                    voted: null,
                };
            });
            this.raceService
                .getRaceResult(this.race.name, this.gameName)

                .subscribe((response: any) => {
                    this.voteList = response.body.votes;
                    this.horseList = response.body.horses;
                    this.odds = response.body.odds;
                    this.voteList.sort((a, b) => {
                        if (a.UID === this.uid) {
                            return -1;
                        } else if (b.UID === this.uid) {
                            return 1;
                        }
                        return 0;
                    });

                    console.log(this.voteList, this.horseList, this.odds);
                });
        });
    }

    goBack() {
        this.location.back();
    }
}
