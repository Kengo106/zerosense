import { Component, OnInit } from '@angular/core';
import { SessionService } from '../service/session.service';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { RaceService } from '../service/race.service';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { AppComponent } from '../app.component';
import { GameService } from '../service/game.service';
import { Game } from '../race.interface';

@Component({
    selector: 'app-updatename',
    templateUrl: './updatename.component.html',
    styleUrls: ['./updatename.component.scss'],
})
export class UpdatenameComponent implements OnInit {
    currentUserName: string = '';
    currentUid: string = '';
    gameClear: Game = {
        id: '',
        gamename: '',
        start: '',
        end: '',
    };

    constructor(
        private sessionService: SessionService,
        private afauth: AngularFireAuth,
        private raceService: RaceService,
        private router: Router,
        private location: Location,
        private gameService: GameService,
    ) {}
    ngOnInit(): void {
        this.gameService.gameSubject.next(this.gameClear);
        this.sessionService.username$.subscribe((name) => (this.currentUserName = name));
        this.sessionService.uid$.subscribe((uid) => (this.currentUid = uid));
    }

    async updataName(): Promise<void> {
        const currentUser = await this.afauth.currentUser;
        try {
            if (currentUser) {
                await currentUser.updateProfile({
                    displayName: this.currentUserName,
                });

                this.raceService
                    .updateUserName(this.currentUserName, this.currentUid)
                    .subscribe((response: any) => {
                        alert(response.message);
                    });
            } else {
                alert();
            }
        } catch {
            alert();
        }
    }

    goBack() {
        this.location.back();
    }
}
