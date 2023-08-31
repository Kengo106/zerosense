import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
    title = 'zerosense';
    date: any;
    gameName: string | null = null;
    constructor(private route: ActivatedRoute, private router: Router) {}
    ngOnInit(): void {
        this.route.queryParams.subscribe((param) => {
            this.gameName = param['gamename'];
        });
    }

    moveGameMain(game: string | null) {
        this.router.navigate(['/gamemain'], { queryParams: { gamename: game } });
    }
}
