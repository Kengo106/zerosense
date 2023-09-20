import { Component, OnInit } from '@angular/core';
import { Race, VoteForm } from '../race.interface';
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
    gameName: string = '';
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
                .getVote(this.race, this.uid, this.gameName)
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
            this.raceService.submitVote(this.myVote, this.uid, this.race, this.gameName).subscribe({
                next: (responce: any) => {
                    alert(responce.sucsess);
                    this.router.navigate(['/gamemain'], {
                        queryParams: { gamename: this.gameName },
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
