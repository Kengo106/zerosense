import { Component, OnDestroy, OnInit } from '@angular/core';
import { Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription, reduce } from 'rxjs';

interface CompetitorData {
    name: string;
    place: any;
    nowscore: any;
    recovery_rate: any;
}

@Component({
    selector: 'app-gamemain',
    templateUrl: './gamemain.component.html',
    styleUrls: ['./gamemain.component.scss'],
})
export class GamemainComponent implements OnInit {
    public uid: string = '';
    game: string = '';
    isVotableRace: Race[] = [];
    competitorDatas: CompetitorData[] = [];
    competitors: string[] = [];

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

            this.raceService.getVotableRaces(this.uid).subscribe((response) => {
                this.isVotableRace = [];
                response.map((responce) => {
                    this.isVotableRace.push(responce);
                });
                console.log(this.isVotableRace);
            });
        });
        this.route.queryParams.subscribe((params) => {
            this.game = params['gamename'];
            this.raceService.getScore(this.game).subscribe((response: any) => {
                console.log(response);
                this.competitorDatas = [];
                response.forEach((elem: any) => this.competitorDatas.push(elem));
                this.competitorDatas.sort((a, b) => a.place - b.place);
                console.log(this.competitorDatas);
            });
        });
    }

    moveVote(race: Race, game: string) {
        this.router.navigate(['/vote'], { queryParams: { ...race, gamename: game } });
    }
}
