import { Component, OnInit } from '@angular/core';
import { RaceService } from '../service/race.service';
import { GameService } from '../service/game.service';
import { Router } from '@angular/router';
import { Game } from '../race.interface';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { EmailAuthCredential, EmailAuthProvider } from 'firebase/auth';
import { SessionService } from '../service/session.service';

@Component({
    selector: 'app-exitgame',
    templateUrl: './exitgame.component.html',
    styleUrls: ['./exitgame.component.scss'],
})
export class ExitgameComponent implements OnInit {
    password: string = '';
    game: Game = {
        gamename: '',
        id: '',
        start: '',
        end: '',
    };
    uid: string = '';

    constructor(
        private raceService: RaceService,
        private gameService: GameService,
        private router: Router,
        private Afauth: AngularFireAuth,
        private sessionService: SessionService,
    ) {}
    ngOnInit(): void {
        this.gameService.gameSubject.subscribe((currentGame) => {
            this.game = currentGame;
        });
        this.sessionService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }

    async exitGame() {
        const user = await this.Afauth.currentUser;
        const credential = EmailAuthProvider.credential(user!.email!, this.password);
        try {
            await user!.reauthenticateWithCredential(credential);
            console.log(this.game);
            const yesNoFlag = window.confirm('大会から退出しますか');
            if (yesNoFlag) {
                this.raceService.exitGame(this.game.id, this.uid).subscribe((message) => {
                    console.log(message);
                    alert(`大会から退出しました\n${this.game.gamename}`);
                    this.router.navigate(['/home/']);
                });
            }
        } catch (error) {
            alert('パスワードを確認できませんでした');
        }
    }
}
