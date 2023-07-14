import { Component, OnInit } from '@angular/core';
import { RaceService } from '../race.service';


interface RaceNameObj{
  date: string
  dayOfTheWeek: string
  name: string
  num: string
}

@Component({
  selector: 'app-racenames',
  templateUrl: './racenames.component.html',
  styleUrls: ['./racenames.component.scss'],
  
})
export class RacenamesComponent implements OnInit {
  constructor( private raceService: RaceService ){}

  raceNames: RaceNameObj[] = [];
  date: any;

  ngOnInit(): void{
    this.getRaceNames();
    console.log(this.raceNames)
  }

 check(){
  console.log(this.date)
 }

  getRaceNames(): void{
    this.raceService.getRaceNames().subscribe((data)=> {
      for(let race of data){
        let raceName = race.race_name;
        let raceNameArray = raceName.split(/[\（\）\ ]/).filter(Boolean);
        let raceNameObj: RaceNameObj = {
          date: raceNameArray[0],
          dayOfTheWeek: raceNameArray[1],
          name: raceNameArray[2],
          num: raceNameArray[3]
        };
        this.raceNames.push(raceNameObj);
      }
    })
  }

}
