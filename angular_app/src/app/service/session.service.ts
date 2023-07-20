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

  login(): void {
    this.session.login =true;
    this.sessionSubject.next(this.session);
    this.router.navigate(['/'])
  }

  logout(): void{
    this.sessionSubject.next(this.session.reset());
    this.router.navigate(['/account/login']);
  }

//   signup(account: Password){
//     this.afAuth.createUserWithEmailAndPassword(account.email, account.pasword)
//     .then( Credential = Credential.user.sendEmailVerification())
//   }
}
