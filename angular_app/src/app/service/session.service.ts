import { Injectable } from '@angular/core';
import { Password, Session } from '../class/user';
import { Subject } from 'rxjs';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { auth } from 'firebaseui';

@Injectable({
    providedIn: 'root',
})
export class SessionService {
    public session = new Session();
    public sessionSubject = new Subject<Session>();
    public sessionState = this.sessionSubject.asObservable();

    constructor(private router: Router, private afAuth: AngularFireAuth) {}

    async login(account: Password): Promise<void> {
        try {
            const auth = await this.afAuth.signInWithEmailAndPassword(
                account.email,
                account.password,
            );
            if (!auth.user?.emailVerified) {
                await this.afAuth.signOut();
                console.log(account.email);
                throw new Error('メールアドレスが登録できません');
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
                console.log(account.username + 'です');
                await userCredential.user.updateProfile({
                    displayName: account.username,
                });
                await userCredential.user.sendEmailVerification();
                alert('メールアドレス確認メールを送信しました。');
            } else {
                alert('userCredential.userが空');
            }
        } catch (error) {
            alert('エラー');
        }
    }
}
