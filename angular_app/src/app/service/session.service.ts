import { Injectable } from '@angular/core';
import { Password, Session } from '../class/user';
import { Subject } from 'rxjs';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { auth } from 'firebaseui';

@Injectable({
  providedIn: 'root'
})
export class SessionService {

  public session = new Session();
  public sessionSubject = new Subject<Session>()
  public sessionState = this.sessionSubject.asObservable();

  constructor(
    private router: Router,
    private afAuth: AngularFireAuth
    ) { }

  login(account : Password): void {
    this.afAuth.signInWithEmailAndPassword(account.email, account.password).then(
      auth => {
            if(!auth.user?.emailVerified){
              this.afAuth.signOut();
              console.log(account.email)
              return Promise.reject('メールアドレスが登録できません')
            }else{
              this.session.login = true;
              this.sessionSubject.next(this.session);
              return this.router.navigate(['/'])
            }}
            ).then(()=>alert('ログインしました'))
            .catch( err => {
              console.log(err);
              alert('ログインに失敗しました。\n' + err);
            })
  }

  logout(): void{
    this.afAuth.signOut()
    .then(() => {
      this.sessionSubject.next(this.session.reset());
      return this.router.navigate(['/account/login']);
    }).then(()=>alert("ログアウトしました"))
    .catch(err => {
      console.log(err);
      alert('ログアウトに失敗しました /n' + err);

    });
  }

  signup(account: Password): Promise<void> {
    return this.afAuth.createUserWithEmailAndPassword(account.email, account.password)
    .then( (userCredential) => {
      if(userCredential.user) {
        console.log(account.username + "です")
        return Promise.all([
          userCredential.user.sendEmailVerification(),
          userCredential.user.updateProfile({
            displayName: account.username
          })
        ])
      }else{throw new Error("Username is not provided.") }
    } )  //ユーザーが自分のメールアドレスを所有していることを確認するためのリンクをメールで送信する
    .then(() => {
      alert('メールアドレス確認メールを送信しました。');
    } )
    .catch(err=>{
      console.log(err),
      alert('アカウントの作成に失敗しました。')
      return Promise.reject(err)
    })
  }
}
