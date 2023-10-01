import { Injectable, OnInit } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { Game } from '../race.interface';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { RaceService } from './race.service';

interface GameMain extends Game {
    start: string;
    end: string;
}

@Injectable({
    providedIn: 'root',
})
export class GameService implements OnInit {
    gameSubject = new BehaviorSubject<GameMain>({
        id: '',
        gamename: '大会未選択',
        start: '',
        end: '',
    });

    currentGame: GameMain = {
        id: '',
        gamename: '大会未選択',
        start: '',
        end: '',
    };

    constructor(
        private router: Router,
        private afAuth: AngularFireAuth,
        private raceService: RaceService,
    ) {}

    ngOnInit(): void {
        this.gameSubject.subscribe((gameMain) => {
            this.currentGame = gameMain;
        });
    }
}
