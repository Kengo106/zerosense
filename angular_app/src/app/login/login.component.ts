import { Component, Inject } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email: string = "";
  password: string = "";

  constructor(@Inject(AngularFireAuth) private auth: AngularFireAuth) { }

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
