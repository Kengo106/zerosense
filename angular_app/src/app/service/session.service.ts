import { Injectable } from '@angular/core';
import { Password, Session } from '../class/user';
import { Subject } from 'rxjs';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import { RaceService } from './race.service';

@Injectable({
    providedIn: 'root',
})
export class SessionService {
    public session = new Session();
    public sessionSubject = new Subject<Session>();
    public sessionState = this.sessionSubject.asObservable();

    constructor(
        private router: Router,
        private afAuth: AngularFireAuth,
        private raceService: RaceService,
    ) {
        this.afAuth.authState.subscribe((user) => {
            if (user) {
                this.session.login = true;
            } else {
                this.session.login = false;
            }
        });
    }

    async login(account: Password): Promise<void> {
        try {
            await this.afAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL);
            const auth = await this.afAuth.signInWithEmailAndPassword(
                account.email,
                account.password,
            );
            if (!auth.user?.emailVerified) {
                await this.afAuth.signOut();
                console.log(account.email);
                throw new Error('emailVerifiedが空');
            } else {
                this.session.login = true;
                this.sessionSubject.next(this.session);
                await alert('ログインしました');
                await this.router.navigate(['/']);
            }
        } catch (error) {
            console.log(error);
            alert('ログインに失敗しました。\n' + error);
        }
    }

    logout(): void {
        this.afAuth
            .signOut()
            .then(() => {
                this.sessionSubject.next(this.session.reset());
                return this.router.navigate(['/account/login']);
            })
            .then(() => alert('ログアウトしました'))
            .catch((err) => {
                console.log(err);
                alert('ログアウトに失敗しました /n' + err);
            });
    }

    async signup(account: Password): Promise<void> {
        const userCredential = await this.afAuth.createUserWithEmailAndPassword(
            account.email,
            account.password,
        );
        try {
            if (userCredential.user) {
                await userCredential.user.updateProfile({
                    displayName: account.username,
                });
                const uid = userCredential.user.uid;
                const username = account.username;
                this.raceService.postUID(uid, username).subscribe(async (response) => {
                    await userCredential.user!.sendEmailVerification();
                    alert('メールアドレス確認メールを送信しました。');
                });
            } else {
                alert('userCredential.userが空');
            }
        } catch (error) {
            alert('エラー');
        }
    }
}
