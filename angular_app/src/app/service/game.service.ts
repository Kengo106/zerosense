import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class GameService {
    gameNameSubject = new BehaviorSubject<string | null>(null);
    gameName: string | null = null;

    putGameName(game: string | null) {
        this.gameNameSubject.next(game);
    }

    catchGameName(game: string | null) {
        this.gameNameSubject.subscribe((nowGame) => (game = nowGame));
    }
}
