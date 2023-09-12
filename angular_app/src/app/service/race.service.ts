import { Injectable } from '@angular/core';
import { Observable, timeInterval } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Race, VoteForm } from '../race.interface';

@Injectable({
    providedIn: 'root',
})
export class RaceService {
    constructor(private http: HttpClient) {}

    postUID(uid: string, username: string) {
        return this.http.post<any>(this.UIDUrl, { uid: uid, username: username });
    }

    createNewGame(gameName: string, open: boolean, uid: string, span: string) {
        return this.http.post(this.newGameUrl, {
            gamename: gameName,
            open: open,
            uid: uid,
            span: span,
        });
    }

    joinGame(gameName: string, uid: string) {
        return this.http.post<any>(this.gameUrl, { gamename: gameName, uid: uid });
    }

    getCurrentGames(uid: string) {
        let params = new HttpParams().set('uid', uid);
        return this.http.get<any>(this.gameUrl, { params: params });
    }

    getVotableRaces(uid: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 1).set('uid', uid);
        return this.http.get<Race[]>(this.raceUrl, { params });
    }

    getAllRaces(uid: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 2).set('uid', uid);
        return this.http.get<Race[]>(this.raceUrl, { params });
    }

    getVote(race: Race, uid: string, gameName: string) {
        let params = new HttpParams()
            .set('grade', race.grade)
            .set('date', race.date)
            .set('name', race.name)
            .set('uid', uid)
            .set('gamename', gameName);
        return this.http.get(this.voteUrl, { params });
    }

    submitVote(voteForm: VoteForm, uid: string, race: Race, game: string) {
        // console.log({ voteForm: voteForm, uid: uid, racename: race });
        return this.http.post(this.voteUrl, {
            voteForm: voteForm,
            uid: uid,
            racename: race,
            game: game,
        });
    }

    getScore(game: string) {
        let params = new HttpParams().set('game', game);
        return this.http.get(this.scoreUrl, { params });
    }

    private raceUrl: string = 'http://127.0.0.1:8000/api/race/';

    private gameUrl: string = 'http://127.0.0.1:8000/api/joingame/';

    private newGameUrl: string = 'http://127.0.0.1:8000/api/newgame/';

    private racenameUrl: string = 'http://127.0.0.1:8000/api/racename/';

    private raceresultUrl: string = 'http://127.0.0.1:8000/api/join/';

    private UIDUrl: string = 'http://127.0.0.1:8000/api/UID/';

    private voteUrl: string = 'http://127.0.0.1:8000/api/vote/';

    private scoreUrl: string = 'http://127.0.0.1:8000/api/score/';
}
