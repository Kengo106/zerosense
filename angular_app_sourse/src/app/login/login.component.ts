import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { SessionService } from '../service/session.service';
import { Password } from '../class/user';
import { GameService } from '../service/game.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
    public account = new Password();

    constructor(
        private sessionServise: SessionService,
        private gameService: GameService,
        private router: Router,
    ) {}

    ngOnInit(): void {
        this.gameService.gameSubject.next({
            id: '',
            gamename: '',
            start: '',
            end: '',
        });
        this.sessionServise.loginState$.subscribe((login) => {
            if (login) {
                this.router.navigate(['home']);
            }
        });
    }

    submitLogin(e: Event) {
        e.preventDefault();
        this.sessionServise.login(this.account);
    }
}
