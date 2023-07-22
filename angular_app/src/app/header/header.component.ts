import { Component, OnInit } from '@angular/core';
import { SessionService } from '../service/session.service';
import { Session } from '../class/user';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit{
  
  public login = false;
  public username = ""

  constructor(
    public sessionService: SessionService,
    private afAuth: AngularFireAuth
    ){}

  ngOnInit(): void {
    
    this.sessionService.sessionState.subscribe((session: Session)=>{
      if (session){
        this.login = session.login;
      }
    });

    this.afAuth.authState.subscribe(user => {
      if (user) {
        this.username = user.displayName || "";
        console.log(user.displayName, new Date());

      }
    });
    

  }

  logout():void{
    this.sessionService.logout();
  }
}
