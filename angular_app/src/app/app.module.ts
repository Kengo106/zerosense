import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RacenamesComponent } from './racenames/racenames.component';
import { HttpClient, HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { RacedetailComponent } from './racedetail/racedetail.component';
import { Location } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, MAT_DATE_LOCALE, DateAdapter } from '@angular/material/core';
import { FormsModule } from '@angular/forms';
import { JPDateAdapter } from './calender/jpdate-adapter';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { environment } from '../environments/environment';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { LoginComponent } from './login/login.component';
import { AngularFireModule } from '@angular/fire/compat';
import { AngularFireAuthModule } from '@angular/fire/compat/auth';
import { HeaderComponent } from './header/header.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { NewgameComponent } from './newgame/newgame.component';
import { HomeComponent } from './home/home.component';
import { SerchgameComponent } from './serchgame/serchgame.component';
import { VoteComponent } from './vote/vote.component';
import { GamemainComponent } from './gamemain/gamemain.component';

@NgModule({
    declarations: [
        AppComponent,
        RacenamesComponent,
        RacedetailComponent,
        LoginComponent,
        HeaderComponent,
        SignUpComponent,
        NewgameComponent,
        HomeComponent,
        SerchgameComponent,
        VoteComponent,
        GamemainComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule,
        MatDatepickerModule,
        MatNativeDateModule,
        FormsModule,
        provideFirebaseApp(() => initializeApp(environment.firebase)),
        provideAuth(() => getAuth()),
        AngularFireModule.initializeApp(environment.firebase),
        AngularFireAuthModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken', // Djangoのデフォルトと一致
            headerName: 'X-CSRFToken', // Djangoのデフォルトと一致
        }),
    ],
    providers: [
        Location,
        { provide: MAT_DATE_LOCALE, useValue: 'ja-JP' },
        { provide: DateAdapter, useClass: JPDateAdapter },
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
