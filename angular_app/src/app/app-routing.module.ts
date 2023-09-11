import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { HomeComponent } from './home/home.component';
import { NewgameComponent } from './newgame/newgame.component';
import { SerchgameComponent } from './serchgame/serchgame.component';
import { VoteComponent } from './vote/vote.component';
import { GamemainComponent } from './gamemain/gamemain.component';

const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'account/login', component: LoginComponent },
    { path: 'account/signup', component: SignUpComponent },
    { path: 'home', component: HomeComponent },
    { path: 'newgame', component: NewgameComponent },
    { path: 'joingame', component: SerchgameComponent },
    { path: 'vote', component: VoteComponent },
    { path: 'gamemain', component: GamemainComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
})
export class AppRoutingModule {}
