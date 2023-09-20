import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { EmailAuthProvider } from 'firebase/auth';
import { RaceService } from '../service/race.service';
import { SessionService } from '../service/session.service';

@Component({
    selector: 'app-deleteaccount',
    templateUrl: './deleteaccount.component.html',
    styleUrls: ['./deleteaccount.component.scss'],
})
export class DeleteaccountComponent implements OnInit {
    email: string = '';
    password: string = '';
    uid: string = '';

    constructor(
        private Afauth: AngularFireAuth,
        private raceService: RaceService,
        private sessinoService: SessionService,
    ) {}

    ngOnInit(): void {
        this.sessinoService.uid$.subscribe((currentUid) => (this.uid = currentUid));
    }

    async deleteAccount() {
        const user = await this.Afauth.currentUser;
        if (user) {
            const credentials = EmailAuthProvider.credential(user.email!, this.password);
            try {
                await user.reauthenticateWithCredential(credentials);
                const yesNoFlag = window.confirm('アカウントを削除してもいいですか？');
                if (yesNoFlag) {
                    this.raceService.deleteAccount(this.uid).subscribe(async (responce) => {
                        console.log(responce);
                        await user.delete();
                        alert('アカウントを削除しました');
                    });
                }
            } catch {
                alert('パスワードを確認できませんでした。');
            }
        }
    }
}
