export class Session {
    login: boolean;

    constructor(){
        this.login = false
    }

    reset(): Session{
        this.login = false;
        return this;
    }
}

export class Password{
    email: string;
    pasword: string;
    passwordConfirmation : string;

    constructor(){
        this.email = '';
        this.pasword = '';
        this.passwordConfirmation = '';
    }

    reset(): void{
        this.email = '';
        this.pasword = '';
        this.passwordConfirmation = '';
    }
}
