import { Component, OnInit } from '@angular/core';
import { Password } from '../class/user';
import { SessionService } from '../service/session.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {

  public account = new Password();

  constructor( private session : SessionService){}

  ngOnInit(): void {
    
  }

  submitSignUp(e: Event): void{
    //デフォルトのイベントを発生させるのではなく、カスタムする
    e.preventDefault()
    console.log(this.account.username)
    if (this.account.password !== this.account.passwordConfirmation){
      alert('パスワードが異なります');
      return
    }
    this.session.signup(this.account)
    .then(()=>{this.account.reset();})

  }

}
