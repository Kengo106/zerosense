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

  private racenameUrl: string = 'http://127.0.0.1:8000/api/racename/';
}
