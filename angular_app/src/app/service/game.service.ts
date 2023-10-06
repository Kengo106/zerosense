import { Injectable, OnInit } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { Game } from '../race.interface';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { RaceService } from './race.service';

@Injectable({
    providedIn: 'root',
})
export class GameService implements OnInit {
    gameSubject = new BehaviorSubject<Game>({
        id: '',
        gamename: '大会未選択',
        start: '',
        end: '',
    });

    currentGame: Game = {
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
