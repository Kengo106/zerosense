import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { SessionService } from '../service/session.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  email: string = "";
  password: string = "";

  constructor(
    private auth: AngularFireAuth,
    private sessionservise : SessionService
  ) { }


  ngOnInit(): void {
    
  }

  submitLogin(){
    this.sessionservise.login()
  }

  login() {
    this.auth.signInWithEmailAndPassword(this.email, this.password)
      .then(() => {
        // ログイン成功時の処理
      })
      .catch((error: any) => {
        // ログイン失敗時の処理
        console.error(error);
      });
  }
}
