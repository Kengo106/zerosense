import { Component, OnInit } from '@angular/core';
import { Race, VoteForm } from '../race.interface';
import { ActivatedRoute, Router } from '@angular/router';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';

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
    };
    public voteForm: VoteForm = {
        first: null,
        second: null,
        third: null,
        comment: '',
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
    ) {}

    ngOnInit() {
        this.sessionService.uid$.subscribe((currentUid) => {
            this.uid = currentUid;
            this.route.queryParams.subscribe((params) => {
                this.race = {
                    grade: params['grade'] as string,
                    name: params['name'] as string,
                    date: params['date'] as string,
                };
            });
            this.raceService.getVote(this.race, this.uid).subscribe((response: any) => {
                this.voteForm = {
                    first: response.vote.first as number | null,
                    second: response.vote.second as number | null,
                    third: response.vote.third as number | null,
                    comment: response.vote.comment as string | null,
                };
                this.horseList = [];
                response.horses.map((horse: any) => this.horseList.push(horse));
            });
        });
    }

    onSubmit() {
        if (this.voteForm.comment === '' || this.voteForm.comment === undefined) {
            this.voteForm.comment = null;
        }
        console.log(this.voteForm);
        if (
            this.voteForm.first != this.voteForm.second &&
            this.voteForm.first !== this.voteForm.third &&
            this.voteForm.second !== this.voteForm.third
        ) {
            this.raceService.submitVote(this.voteForm, this.uid, this.race).subscribe({
                next: (responce: any) => {
                    alert(responce.sucsess);
                    this.router.navigate(['/home']);
                },
                error: (error: any) => {
                    alert('error');
                },
            });
        } else {
            alert('異なる馬を投票してください');
        }
    }
}
