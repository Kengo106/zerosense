import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { SessionService } from '../service/session.service';
import { Password } from '../class/user';
import { GameService } from '../service/game.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
    public account = new Password();

    constructor(private sessionservise: SessionService, private gameService: GameService) {}

    ngOnInit(): void {
        this.gameService.gameSubject.next({
            id: '',
            gamename: '',
            start: '',
            end: '',
        });
    }

    submitLogin(e: Event) {
        e.preventDefault();
        this.sessionservise.login(this.account);
    }
}
