import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RaceService {

  constructor(
    private http: HttpClient,
  ) {}

  getRaceNames(): Observable<any>  {
    const racenames = this.http.get<any>(this.racenameUrl)
    return racenames

  }
  
  
  getResult(raceName: string): Observable<any> {
    const url = `${this.raceresultUrl}?race_name=${raceName}`
    const raceresult = this.http.get<any>(url)
    return raceresult
  }


  private racenameUrl: string = 'http://127.0.0.1:8000/api/racename/';
  
  private raceresultUrl: string = 'http://127.0.0.1:8000/api/racename/';
}
