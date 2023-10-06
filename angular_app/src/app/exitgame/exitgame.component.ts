import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'app-exitgame',
    templateUrl: './exitgame.component.html',
    styleUrls: ['./exitgame.component.scss'],
})
export class ExitgameComponent implements OnInit {
    password: string = '';

    constructor() {}
    ngOnInit(): void {}

    exitGame() {}
}
