import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RacenamesComponent } from './racenames/racenames.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RacedetailComponent } from './racedetail/racedetail.component';
import { Location } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, MAT_DATE_LOCALE, DateAdapter } from '@angular/material/core';
import { FormsModule } from '@angular/forms';
import { JPDateAdapter } from './jpdate-adapter';



@NgModule({
  declarations: [
    AppComponent,
    RacenamesComponent,
    RacedetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    FormsModule,
  ],
  providers: [
    Location,
    {provide: MAT_DATE_LOCALE, useValue: 'ja-JP'},
    {provide: DateAdapter, useClass: JPDateAdapter},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
