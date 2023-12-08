import { Component, OnInit } from '@angular/core';
import { SessionService } from '../service/session.service';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
    public login = false;
    public userName = '';

    constructor(public sessionService: SessionService, private afAuth: AngularFireAuth) {}

    ngOnInit(): void {
        this.sessionService.loginState$.subscribe((isLogin) => (this.login = isLogin));
        this.sessionService.username$.subscribe((name) => (this.userName = name));
    }

    logout(): void {
        const yesNoFlag = window.confirm('ログアウトしますか');
        if (yesNoFlag) {
            this.sessionService.logout();
        }
    }
}
