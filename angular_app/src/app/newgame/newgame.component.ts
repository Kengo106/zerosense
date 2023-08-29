import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-newgame',
    templateUrl: './newgame.component.html',
    styleUrls: ['./newgame.component.scss'],
})
export class NewgameComponent implements OnInit {
    public gameName: string = '';
    public strOpen: string = '';
    public open: boolean = false;
    public uid: string = '';
    public span: string = '';

    constructor(
        private raceServce: RaceService,
        private sessionService: SessionService,
        private router: Router,
    ) {}

    ngOnInit(): void {
        this.sessionService.uid$.subscribe((UID) => (this.uid = UID));
    }
    onSubmit() {
        if (this.uid && this.uid !== '') {
            if (this.strOpen == 'true') {
                this.open = true;
            } else {
                this.open = false;
            }
            this.raceServce.createNewGame(this.gameName, this.open, this.uid, this.span).subscribe({
                next: (response) => {
                    alert(`大会を作成しました\n${this.gameName}`);
                    this.router.navigate(['/home']);
                },
                error: (error) => {
                    alert(`error\n${error.message}`);
                },
            });
        } else {
            alert('ログインしてください');
            this.router.navigate(['/account/login']);
        }
    }
}
