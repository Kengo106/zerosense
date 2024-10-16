import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClient, HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { Location } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, MAT_DATE_LOCALE, DateAdapter } from '@angular/material/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
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
import { TestComponent } from './test/test.component';
import { UpdatenameComponent } from './updatename/updatename.component';

import { PastracesComponent } from './pastraces/pastraces.component';
import { RaceresultComponent } from './raceresult/raceresult.component';
import { DeleteaccountComponent } from './deleteaccount/deleteaccount.component';
import { ClipboardModule } from 'ngx-clipboard';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ExitgameComponent } from './exitgame/exitgame.component';
import { TopComponent } from './top/top.component';

@NgModule({
    declarations: [
        AppComponent,
        LoginComponent,
        HeaderComponent,
        SignUpComponent,
        NewgameComponent,
        HomeComponent,
        SerchgameComponent,
        VoteComponent,
        GamemainComponent,
        TestComponent,
        UpdatenameComponent,
        PastracesComponent,
        RaceresultComponent,
        DeleteaccountComponent,
        ExitgameComponent,
        TopComponent,
    ],
    imports: [
        ClipboardModule,
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatInputModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatProgressSpinnerModule,
        FormsModule,
        provideFirebaseApp(() => initializeApp(environment.firebase)),
        provideAuth(() => getAuth()),
        AngularFireModule.initializeApp(environment.firebase),
        AngularFireAuthModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken', // Djangoのデフォルトと一致
            headerName: 'X-CSRFToken', // Djangoのデフォルトと一致
        }),
        ReactiveFormsModule,
    ],
    providers: [
        Location,
        { provide: MAT_DATE_LOCALE, useValue: 'ja-JP' },
        { provide: DateAdapter, useClass: JPDateAdapter },
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
