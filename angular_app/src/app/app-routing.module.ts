import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RacedetailComponent } from './racedetail/racedetail.component';
import { RacenamesComponent } from './racenames/racenames.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  {path: '', redirectTo: 'racenames', pathMatch: 'full'},
  { path: 'racenames', component: RacenamesComponent}, 
  { path: 'racedetail/:race_name', component: RacedetailComponent},
  { path: 'login', component: LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
