import { Component, OnDestroy, OnInit } from '@angular/core';
import { Game, Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';

interface CompetitorData {
    name: string;
    place: any;
    nowscore: any;
    recovery_rate: any;
    latest_week_race_score: any;
    vote_time: any;
    tan_time: any;
    fuku_time: any;
    umaren_time: any;
    umatan_time: any;
    wide_time: any;
    trio_time: any;
    tierce_time: any;
    million_time: any;
    get_top_in_month: any;
}

@Component({
    selector: 'app-gamemain',
    templateUrl: './gamemain.component.html',
    styleUrls: ['./gamemain.component.scss'],
})
export class GamemainComponent implements OnInit {
    public uid: string = '';
    game: Game = {
        id: '',
        gamename: '',
    };
    isVotableRace: Race[] = [];
    competitorDatas: CompetitorData[] = [];
    competitors: string[] = [];
    showTime: boolean = false;
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.route.queryParams.subscribe((params) => {
                this.game = {
                    id: params['id'],
                    gamename: params['gamename'],
                };
                if (this.uid.trim().length * this.game.id.trim().length) {
                    this.raceService
                        .getVotableRaces(this.uid, this.game.id)
                        .subscribe((response) => {
                            this.isVotableRace = [];
                            response.map((responce) => {
                                console.log(responce);
                                this.isVotableRace.push(responce);
                            });
                        });
                    this.raceService.getScore(this.game.id).subscribe((response: any) => {
                        console.log(response);
                        this.competitorDatas = [];
                        response.forEach((elem: any) => this.competitorDatas.push(elem));
                        this.competitorDatas.sort((a, b) => a.place - b.place);
                        console.log(this.competitorDatas);
                    });
                }
            });
        });
    }

    moveVote(race: Race) {
        this.router.navigate(['/vote'], {
            queryParams: {
                date: race.date,
                racename: race.name,
                grade: race.grade,
                gamename: this.game.gamename,
                id: this.game.id,
            },
        });
        console.log(this.game);
    }

    moveResult() {
        this.router.navigate(['/pastraces/'], {
            queryParams: { gamename: this.game.gamename, id: this.game.id },
        });
    }

    toggleTime() {
        this.showTime = !this.showTime;
    }
}
