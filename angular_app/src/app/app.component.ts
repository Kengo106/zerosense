import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Game } from './race.interface';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
    title = 'zerosense';
    date: any;
    game: Game = {
        id: '',
        gamename: '',
    };

    constructor(private route: ActivatedRoute, private router: Router) {}
    ngOnInit(): void {
        this.route.queryParams.subscribe((param) => {
            this.game = {
                id: param['id'],
                gamename: param['gamename'],
            };
        });
    }
    moveGameMain(game: Game) {
        this.router.navigate(['/gamemain'], { queryParams: game });
    }
}
