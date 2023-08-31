import { Component, OnInit } from '@angular/core';
import { GameService } from './service/game.service';
import { BehaviorSubject } from 'rxjs';
import { ActivatedRoute, Route } from '@angular/router';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
    title = 'zerosense';
    date: any;
    gameName: string | null = null;
    ngOnInit(): void {}
}
