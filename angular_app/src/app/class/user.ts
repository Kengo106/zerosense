export class Session {
    login: boolean;
    username: string;

    constructor(){

        this.login = false
        this.username = ""
    }

    reset(): Session{
        this.login = false;
        this.username = ""
        return this;
    }
}

export class Password{
    username: string;
    email: string;
    password: string;
    passwordConfirmation : string;

    constructor(){
        this.username = "";
        this.email = '';
        this.password = '';
        this.passwordConfirmation = '';
    }

    reset(): void{
        this.username = '';
        this.email = '';
        this.password = '';
        this.passwordConfirmation = '';
    }
}
