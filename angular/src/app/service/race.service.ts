import { Injectable } from '@angular/core';
import { Observable, timeInterval } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Game, Race, VoteForm } from '../race.interface';
import { environment } from 'src/environments/environment';

const apiUrl = environment.apiUrl;

@Injectable({
    providedIn: 'root',
})
export class RaceService {
    constructor(private http: HttpClient) {}

    postUID(uid: string, username: string) {
        return this.http.post<any>(this.UIDUrl, { uid: uid, username: username });
    }

    createNewGame(gameName: string, open: boolean, uid: string, span: any) {
        return this.http.post(this.newGameUrl, {
            gamename: gameName,
            open: open,
            uid: uid,
            span: span,
        });
    }

    gameSerch(gameSerchId: string) {
        let params = new HttpParams().set('gameserchid', gameSerchId);
        return this.http.get(this.serchGameUrl, { params });
    }

    joinGame(gameId: string, uid: string) {
        return this.http.post<any>(this.gameUrl, { gameid: gameId, uid: uid });
    }

    getCurrentGames(uid: string) {
        let params = new HttpParams().set('uid', uid);
        return this.http.get<any>(this.gameUrl, { params: params });
    }

    getThisWeekRaces(uid: string, gameId: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 1).set('uid', uid).set('gameid', gameId);
        console.log(gameId);
        return this.http.get<Race[]>(this.raceUrl, { params });
    }

    getAllRaces(uid: string, gameId: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 0).set('uid', uid).set('gameid', gameId);
        return this.http.get<Race[]>(this.raceUrl, { params });
    }

    getVote(race: Race, uid: string, gameId: string) {
        let params = new HttpParams()
            .set('grade', race.grade)
            .set('date', race.date)
            .set('racename', race.name)
            .set('uid', uid)
            .set('gameid', gameId);
        return this.http.get(this.voteUrl, { params });
    }

    submitVote(voteForm: VoteForm, uid: string, race: Race, gameId: string) {
        // console.log({ voteForm: voteForm, uid: uid, racename: race });
        return this.http.post(this.voteUrl, {
            voteForm: voteForm,
            uid: uid,
            racename: race,
            gameid: gameId,
        });
    }

    getScore(gameId: string) {
        let params = new HttpParams().set('gameid', gameId);
        return this.http.get(this.scoreUrl, { params });
    }

    updateUserName(name: string, uid: string) {
        return this.http.put(this.userNameUrl, { name: name, uid: uid });
    }

    getRaceResult(race: string, gameId: string) {
        let params = new HttpParams().set('racename', race).set('gameid', gameId);
        return this.http.get(this.raceResult, { params });
    }

    deleteAccount(uid: string) {
        let params = new HttpParams().set('uid', uid);
        return this.http.delete(this.accountUrl, { params });
    }

    exitGame(gameId: string, uid: string) {
        let params = new HttpParams().set('gameid', gameId).set('uid', uid);
        return this.http.delete(this.gameUrl, { params });
    }

    private raceUrl: string = `${apiUrl}/race/`;

    private gameUrl: string = `${apiUrl}/game/`;

    private newGameUrl: string = `${apiUrl}/newgame/`;

    private UIDUrl: string = `${apiUrl}/UID/`;

    private voteUrl: string = `${apiUrl}/vote/`;

    private scoreUrl: string = `${apiUrl}/score/`;

    private userNameUrl: string = `${apiUrl}/username/`;

    private raceResult: string = `${apiUrl}/raceresult/`;

    private accountUrl: string = `${apiUrl}/account/`;

    private serchGameUrl: string = `${apiUrl}/serchgame/`;
}
