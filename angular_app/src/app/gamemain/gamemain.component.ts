import { Component, OnDestroy, OnInit } from '@angular/core';
import { Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription, reduce } from 'rxjs';

interface CompetitorData {
    name: string;
    place: any;
    gamescore: any;
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
                this.competitors = Object.keys(response);
                let tempScore = this.competitors.map((competitor) => ({
                    name: competitor,
                    gamescore: Object.values(response[competitor]).reduce(
                        (sumScore: any, score: any) => sumScore + score,
                        0,
                    ),
                }));
                tempScore.sort((a, b) => {
                    let scoreA = a.gamescore as number;
                    let scoreB = b.gamescore as number;
                    return scoreB - scoreA;
                });
                tempScore.forEach((data, index) =>
                    this.competitorDatas.push({
                        name: data.name,
                        place: index + 1,
                        gamescore: data.gamescore,
                    }),
                );

                console.log(this.competitorDatas);
            });
        });
    }

    moveVote(race: Race, game: string) {
        this.router.navigate(['/vote'], { queryParams: { ...race, gamename: game } });
    }
}
