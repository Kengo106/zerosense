import { Injectable } from '@angular/core';
import { Password } from '../class/user';
import { BehaviorSubject, Subject } from 'rxjs';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import { RaceService } from './race.service';

@Injectable({
    providedIn: 'root',
})
export class SessionService {
    private loginSubject = new BehaviorSubject<boolean>(false);
    loginState$ = this.loginSubject.asObservable();
    private usernameSubject = new BehaviorSubject<string>('');
    username$ = this.usernameSubject.asObservable();
    private uidSubject = new BehaviorSubject<string>('');
    uid$ = this.uidSubject.asObservable();

    constructor(
        private router: Router,
        private afAuth: AngularFireAuth,
        private raceService: RaceService,
    ) {
        this.afAuth.authState.subscribe((user) => {
            // console.log(user);
            if (user) {
                this.usernameSubject.next(user.displayName || '');
                this.loginSubject.next(true);
                this.uidSubject.next(user.uid);
            } else {
                this.usernameSubject.next('');
                this.loginSubject.next(false);
                this.uidSubject.next('');
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
                alert('ログインしました');
                this.router.navigate(['/']);
            }
        } catch (error) {
            console.log(error);
            alert('ログインに失敗しました。\n' + error);
        }
    }

    async logout(): Promise<any> {
        try {
            await this.afAuth.signOut();
            alert('ログアウトしました');
            await this.router.navigate(['account/login']);
        } catch (err) {
            console.log(err);
            alert('ログアウトに失敗しました /n' + err);
        }
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
