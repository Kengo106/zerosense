export interface RaceNameObj {
    date: string;
    dayOfTheWeek: string;
    name: string;
    num: string;
}

export interface Race {
    grade: string;
    name: string;
    date: string;
    voted: boolean | null;
}

export interface VoteForm {
    first: number | null; //HorseのID
    second: number | null;
    third: number | null;
    comment: string | null;
}
