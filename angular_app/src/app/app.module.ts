import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RacenamesComponent } from './racenames/racenames.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RacedetailComponent } from './racedetail/racedetail.component';
import { Location } from '@angular/common';

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
  ],
  providers: [Location],
  bootstrap: [AppComponent]
})
export class AppModule { }
