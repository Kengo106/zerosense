import { Component, OnInit } from '@angular/core';
import { Game, Race, VoteForm } from '../race.interface';
import { ActivatedRoute, Router } from '@angular/router';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Location } from '@angular/common';

@Component({
    selector: 'app-vote',
    templateUrl: './vote.component.html',
    styleUrls: ['./vote.component.scss'],
})
export class VoteComponent implements OnInit {
    public race: Race = {
        grade: '',
        name: '',
        date: '',
        voted: null,
    };
    userName: string = '';
    voteList: any[] = [];
    public myVote: VoteForm = {
        first: null,
        second: null,
        third: null,
        comment: '',
    };
    game: Game = {
        id: '',
        gamename: '',
    };
    public uid: string = '';
    public horseList: {
        id: number;
        name: string;
    }[] = [];

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private raceService: RaceService,
        private sessionService: SessionService,
        private location: Location,
    ) {}

    ngOnInit() {
        this.route.queryParams.subscribe(
            (params) =>
                (this.game = {
                    id: params['id'],
                    gamename: params['gamename'],
                }),
        );
        console.log(this.game);
        this.sessionService.username$.subscribe((myName) => (this.userName = myName));
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.route.queryParams.subscribe((params) => {
                this.race = {
                    grade: params['grade'] as string,
                    name: params['racename'] as string,
                    date: params['date'] as string,
                    voted: null,
                };
            });
            this.raceService
                .getVote(this.race, this.uid, this.game.id)
                .subscribe((response: any) => {
                    this.myVote = {
                        first: response.vote.first as number | null,
                        second: response.vote.second as number | null,
                        third: response.vote.third as number | null,
                        comment: response.vote.comment as string | null,
                    };

                    this.horseList = [];
                    response.horses.map((horse: any) => this.horseList.push(horse));
                    this.voteList = [];
                    response.votelist.map((vote: any) => {
                        console.log(vote);
                        this.voteList.push(vote);
                    });
                    console.log(this.voteList);
                });
        });
    }

    onSubmit() {
        if (this.myVote.comment === '' || this.myVote.comment === undefined) {
            this.myVote.comment = null;
        }
        console.log(this.myVote);
        if (
            this.myVote.first != this.myVote.second &&
            this.myVote.first !== this.myVote.third &&
            this.myVote.second !== this.myVote.third
        ) {
            this.raceService.submitVote(this.myVote, this.uid, this.race, this.game.id).subscribe({
                next: (responce: any) => {
                    alert(responce.sucsess);
                    this.router.navigate(['/gamemain'], {
                        queryParams: { gamename: this.game.gamename, id: this.game.id },
                    });
                },
                error: (error: any) => {
                    alert('error');
                },
            });
        } else {
            alert('異なる馬を投票してください');
        }
    }
    goBack() {
        this.location.back();
    }
}
