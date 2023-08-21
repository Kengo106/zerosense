import { Injectable } from '@angular/core';
import { Observable, timeInterval } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
    providedIn: 'root',
})
export class RaceService {
    constructor(private http: HttpClient) {}

    getRaceNames(): Observable<any> {
        const racenames = this.http.get<any>(this.racenameUrl);
        return racenames;
    }

    getResult(raceName: string): Observable<any> {
        const url = `${this.raceresultUrl}?race_name=${encodeURIComponent(raceName).replace(
            /%C2%A0/g,
            '%20',
        )}`;
        console.log(url);
        const raceresult = this.http.get<any>(url);
        return raceresult;
    }

    postUID(uid: string, username: string) {
        return this.http.post<any>(this.postUIDUrl, { uid: uid, username: username });
    }

    createNewGame(groupName: string, open: boolean) {
        return this.http.post(this.createNewGameUrl, { gamename: groupName, open: open });
    }

    private createNewGameUrl: string = 'http://127.0.0.1:8000/api/NewGame/';

    private racenameUrl: string = 'http://127.0.0.1:8000/api/racename/';

    private raceresultUrl: string = 'http://127.0.0.1:8000/api/join/';

    private postUIDUrl: string = 'http://127.0.0.1:8000/api/UID/';
}
