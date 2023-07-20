import { Component, OnInit } from '@angular/core';
import { SessionService } from '../service/session.service';
import { Session } from '../class/user';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit{
  
  public login = false;

  constructor(public sessionService: SessionService){}

  ngOnInit(): void {
    
    this.sessionService.sessionState.subscribe((session: Session)=>{
      if (session){
        this.login = session.login;
      }
    });
  }

  logout():void{
    this.sessionService.logout();
  }
}
