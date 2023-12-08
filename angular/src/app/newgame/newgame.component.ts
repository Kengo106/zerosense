import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';
import { Router } from '@angular/router';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Game } from '../race.interface';
import { GameService } from '../service/game.service';

@Component({
    selector: 'app-newgame',
    templateUrl: './newgame.component.html',
    styleUrls: ['./newgame.component.scss'],
})
export class NewgameComponent implements OnInit {
    gameName: string = '';
    strOpen: string = 'false';
    open: boolean = false;
    uid: string = '';
    span: {} = {
        start: '',
        end: '',
    };
    gameClear: Game = {
        id: '',
        gamename: '',
        start: '',
        end: '',
    };
    range: FormGroup = this.fb.group({
        start: [null], // 初期値を空文字列に
        end: [null], // 初期値を空文字列に
    });
    constructor(
        private raceServce: RaceService,
        private sessionService: SessionService,
        private router: Router,
        private fb: FormBuilder,
        private gameService: GameService,
    ) {}

    ngOnInit(): void {
        this.gameService.gameSubject.next(this.gameClear);
        this.sessionService.uid$.subscribe((UID) => (this.uid = UID));
    }

    dateSubmit() {
        console.log(this.range.get('start')?.value);
        const startObj = this.range.get('start')?.value;
        const startYear = startObj.getFullYear();
        const startMonth = ('0' + (startObj.getMonth() + 1)).slice(-2);
        const startDate = ('0' + startObj.getDate()).slice(-2);
        console.log(`${startYear}-${startMonth}-${startDate}`);
    }
    onSubmit() {
        if (this.uid && this.uid !== '') {
            if (this.gameName.trim().length != 0) {
                if (this.strOpen == 'true') {
                    this.open = true;
                } else {
                    this.open = false;
                }
                if (this.range.get('start')?.value && this.range.get('end')?.value) {
                    const startObj = this.range.get('start')?.value;
                    const startYear = startObj.getFullYear();
                    const startMonth = ('0' + (startObj.getMonth() + 1)).slice(-2);
                    const startDate = ('0' + startObj.getDate()).slice(-2);
                    const start = `${startYear}-${startMonth}-${startDate}`;
                    const endObj = this.range.get('end')?.value;
                    const endYear = endObj.getFullYear();
                    const endMonth = ('0' + (endObj.getMonth() + 1)).slice(-2);
                    const endDate = ('0' + endObj.getDate()).slice(-2);
                    const end = `${endYear}-${endMonth}-${endDate}`;
                    this.span = {
                        start: start,
                        end: end,
                    };
                    console.log();
                    this.raceServce
                        .createNewGame(this.gameName, this.open, this.uid, this.span)
                        .subscribe({
                            next: (response) => {
                                alert(`大会を作成しました\n${this.gameName}`);
                                this.router.navigate(['/home']);
                            },
                            error: (error) => {
                                alert(`error\n${error.message}`);
                            },
                        });
                } else {
                    alert('開催期間を入力してください');
                }
            } else {
                alert('大会名を入力してください');
            }
        } else {
            alert('ログインしてください');
            this.router.navigate(['/account/login']);
        }
    }
}
