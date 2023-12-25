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

    // 修正済み↓
    postUID(uid: string, username: string) {
        const url = `${this.userUrl}regist/`;
        return this.http.post<any>(url, { uid: uid, username: username });
    }
    // 修正済み↓
    updateUserName(name: string, uid: string) {
        const url = `${this.userUrl}edit/${uid}/`;
        return this.http.put(url, { name: name });
    }
    // 修正済み↓
    deleteAccount(uid: string) {
        const url = `${this.userUrl}edit/${uid}/`;
        return this.http.delete(url);
    }

    // 修正済み↓
    createNewGame(gameName: string, open: boolean, uid: string, span: any) {
        const url = `${this.gamesUrl}create/`;
        return this.http.post(url, {
            gamename: gameName,
            open: open,
            uid: uid,
            span: span,
        });
    }
    // 修正済み↓
    getCurrentGames(uid: string) {
        const url = `${this.gamesUrl}list/${uid}/`;
        return this.http.get<any>(url);
    }
    // 修正済み↓
    joinGame(gameId: string, uid: string) {
        const url = `${this.gamesPlayerUrl}regist/${gameId}/`;
        return this.http.post<any>(url, { uid: uid });
    }
    // 修正済み↓
    exitGame(gameId: string, uid: string) {
        const url = `${this.gamesPlayerUrl}delete/${gameId}/${uid}/`;
        return this.http.delete(url);
    }
    // 修正済み↓
    gameSerch(gameSerchId: string) {
        let params = new HttpParams().set('gameserchid', gameSerchId);
        const url = `${this.gamesUrl}serch/`;
        return this.http.get(url, { params });
    }
    // 修正済み↓
    getThisWeekRaces(uid: string, gameId: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 1).set('uid', uid).set('gameid', gameId);
        console.log(gameId);
        return this.http.get<Race[]>(this.racesUrl, { params });
    }
    // 修正済み↓
    getAllRaces(uid: string, gameId: string): Observable<Race[]> {
        let params = new HttpParams().set('flag', 0).set('uid', uid).set('gameid', gameId);
        return this.http.get<Race[]>(this.racesUrl, { params });
    }
    // 修正済み↓
    getVote(race: Race, uid: string, gameId: string) {
        let params = new HttpParams()
            .set('grade', race.grade)
            .set('date', race.date)
            .set('racename', race.name)
            .set('uid', uid)
            .set('gameid', gameId);
        return this.http.get(this.votesUrl, { params });
    }
    // 修正済み↓
    submitVote(voteForm: VoteForm, uid: string, race: Race, gameId: string) {
        return this.http.post(this.votesUrl, {
            voteForm: voteForm,
            uid: uid,
            racename: race,
            gameid: gameId,
        });
    }
    // 修正済み↓
    getRaceResult(race: string, gameId: string) {
        const url = `${this.racesUrl}${race}/games/${gameId}/`;
        return this.http.get(url);
    }
    // 修正済み↓
    getScore(gameId: string) {
        // let params = new HttpParams().set('gameid', gameId);
        const url = `${this.gamesUrl}scores/${gameId}/`;
        return this.http.get(url);
    }

    private racesUrl: string = `${apiUrl}/races/`;

    private gamesUrl: string = `${apiUrl}/games/`;

    private gamesPlayerUrl: string = `${apiUrl}/player/`;

    // private gamesDetailUrl: string = `${apiUrl}/games/detail/`;

    private votesUrl: string = `${apiUrl}/votes/`;

    private userUrl: string = `${apiUrl}/user/`;

    // private userRegistUrl: string = `${apiUrl}/user-regist/`;
}
