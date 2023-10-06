import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { HomeComponent } from './home/home.component';
import { NewgameComponent } from './newgame/newgame.component';
import { SerchgameComponent } from './serchgame/serchgame.component';
import { VoteComponent } from './vote/vote.component';
import { GamemainComponent } from './gamemain/gamemain.component';
import { TestComponent } from './test/test.component';
import { UpdatenameComponent } from './updatename/updatename.component';
import { PastracesComponent } from './pastraces/pastraces.component';
import { RaceresultComponent } from './raceresult/raceresult.component';
import { DeleteaccountComponent } from './deleteaccount/deleteaccount.component';
import { ExitgameComponent } from './exitgame/exitgame.component';

const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'account/login', component: LoginComponent },
    { path: 'account/signup', component: SignUpComponent },
    { path: 'home', component: HomeComponent },
    { path: 'newgame', component: NewgameComponent },
    { path: 'joingame', component: SerchgameComponent },
    { path: 'vote', component: VoteComponent },
    { path: 'gamemain', component: GamemainComponent },
    { path: 'test', component: TestComponent },
    { path: 'updatename', component: UpdatenameComponent },
    { path: 'pastraces', component: PastracesComponent },
    { path: 'raceresult', component: RaceresultComponent },
    { path: 'deleteacount', component: DeleteaccountComponent },
    { path: 'exitgame', component: ExitgameComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
})
export class AppRoutingModule {}
