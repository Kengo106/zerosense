import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RacedetailComponent } from './racedetail/racedetail.component';
import { RacenamesComponent } from './racenames/racenames.component';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { HomeComponent } from './home/home.component';
import { NewgameComponent } from './newgame/newgame.component';
import { SerchgameComponent } from './serchgame/serchgame.component';

const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'racenames', component: RacenamesComponent },
    { path: 'racedetail/:race_name', component: RacedetailComponent },
    { path: 'account/login', component: LoginComponent },
    { path: 'account/signup', component: SignUpComponent },
    { path: 'home', component: HomeComponent },
    { path: 'newgame', component: NewgameComponent },
    { path: 'joingame', component: SerchgameComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
})
export class AppRoutingModule {}
