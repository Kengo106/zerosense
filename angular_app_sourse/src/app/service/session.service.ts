import { Injectable } from '@angular/core';
import { Password } from '../class/user';
import { BehaviorSubject, Subject } from 'rxjs';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import { RaceService } from './race.service';
import { GameService } from './game.service';

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
        private gameService: GameService,
    ) {
        this.afAuth.authState.subscribe((user) => {
            // console.log(user);
            if (user) {
                this.usernameSubject.next(user.displayName || '');
                this.loginSubject.next(true);
                this.uidSubject.next(user.uid);
                console.log('T');
            } else {
                this.usernameSubject.next('');
                this.loginSubject.next(false);
                this.uidSubject.next('');
                console.log('F');
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
                throw new Error('メールアドレスの確認を実行してください');
            } else {
                alert('ログインしました');
                this.router.navigate(['/home']);
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
            this.gameService.gameSubject.next({
                id: '',
                gamename: '',
                start: '',
                end: '',
            });
        } catch (err) {
            console.log(err);
            alert('ログアウトに失敗しました /n' + err);
        }
    }

    async signup(account: Password): Promise<void> {
        try {
            const userCredential = await this.afAuth.createUserWithEmailAndPassword(
                account.email,
                account.password,
            );
            if (userCredential.user) {
                await userCredential.user.updateProfile({
                    displayName: account.username,
                });
                const uid = userCredential.user.uid;
                const username = account.username;
                this.raceService.postUID(uid, username).subscribe(async (response) => {
                    await this.afAuth.signOut();
                    await userCredential.user!.sendEmailVerification();

                    alert('メールアドレス確認メールを送信しました。');
                    this.router.navigate(['account/login']);
                });
            } else {
                alert('userCredential.userが空');
            }
        } catch (error: any) {
            console.log(error.code);
            console.log(error.message);
            if (error.code == 'auth/email-already-in-use') {
                alert('そのメールアドレスは既に使用されています。');
            } else if (error.code == 'auth/weak-password') {
                alert('パスワードは6文字以上で設定してください。');
            } else {
                alert('エラーが発生しました。');
            }
        }
    }
}
