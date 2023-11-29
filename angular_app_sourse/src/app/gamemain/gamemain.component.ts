import { Component, OnDestroy, OnInit } from '@angular/core';
import { Game, Race } from '../race.interface';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../service/game.service';

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
        start: '',
        end: '',
    };
    isLogin: boolean = false;
    thisWeekRaces: Race[] = [];
    competitorDatas: CompetitorData[] = [];
    competitors: string[] = [];
    showTime: boolean = false;
    constructor(
        private raceService: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private route: ActivatedRoute,
        private gameService: GameService,
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.sessionService.loginState$.subscribe((login) => {
                this.isLogin = login;
            });
            if (this.isLogin) {
                this.route.queryParams.subscribe((params) => {
                    this.gameService.gameSubject.next({
                        id: params['id'],
                        gamename: params['gamename'],
                        start: params['start'],
                        end: params['end'],
                    });
                    this.game = {
                        id: params['id'],
                        gamename: params['gamename'],
                        start: params['start'],
                        end: params['end'],
                    };
                    if (this.uid.trim().length * this.game.id.trim().length) {
                        this.raceService
                            .getThisWeekRaces(this.uid, this.game.id)
                            .subscribe((response) => {
                                this.thisWeekRaces = [];
                                response.map((responce) => {
                                    console.log(responce);
                                    this.thisWeekRaces.push(responce);
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
            }
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
                start: this.game.start,
                end: this.game.end,
            },
        });
        console.log(this.game);
    }

    moveResult() {
        this.router.navigate(['/pastraces/'], {
            queryParams: { gamename: this.game.gamename, id: this.game.id },
        });
    }

    moveExitGame() {
        this.router.navigate(['/exitgame/'], {
            queryParams: { gamename: this.game.gamename, id: this.game.id },
        });
    }

    toggleTime() {
        this.showTime = !this.showTime;
    }
}
