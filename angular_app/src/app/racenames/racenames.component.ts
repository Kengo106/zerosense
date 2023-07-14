import { Component, OnInit } from '@angular/core';
import { RaceService } from '../race.service';
import { RaceNameObj } from '../race.interface';
import { formatDate } from '@angular/common';


@Component({
  selector: 'app-racenames',
  templateUrl: './racenames.component.html',
  styleUrls: ['./racenames.component.scss'],
  
})
export class RacenamesComponent implements OnInit {
  constructor( private raceService: RaceService ){}

  raceNames: RaceNameObj[] = [];
  date: any | null = null;
  raceNamesDisplay: RaceNameObj[] = [];

  dateFilter = (date: Date|null)=>{
    if (!date) {
      return false;
    }
    let selectableDateStrings = this.raceNames.map(item => item.date);
    let selectableDates = selectableDateStrings.map(dateString => {

      let [year, month, day] = dateString
      .split('年').join('-')
      .split('月').join('-')
      .split('日')[0].split('-').map(part => parseInt(part,10))
      let newDate = new Date(year, month - 1, day);
    

  
      return newDate;
    })
    return selectableDates.some(selectableDate => 
      date.getDate() === selectableDate.getDate() &&
      date.getMonth() === selectableDate.getMonth() &&
      date.getFullYear() === selectableDate.getFullYear()
      )
  }

  dateClass = (date: Date) => {
    let selectableDateStrings = this.raceNames.map(item => item.date);
    let selectableDates = selectableDateStrings.map(dateString => {
      let [year, month, day] = dateString
      .split('年').join('-')
      .split('月').join('-')
      .split('日')[0].split('-').map(part => parseInt(part,10))
      let newDate = new Date(year, month - 1, day);
  
      return newDate;
    });
  
    // If the date is one of the selectable dates, return a CSS class name
    if (selectableDates.some(selectableDate => 
      date.getDate() === selectableDate.getDate() &&
      date.getMonth() === selectableDate.getMonth() &&
      date.getFullYear() === selectableDate.getFullYear())) {
      return 'selectable-date';
    }
  
    // Otherwise, return an empty string (no class applied)
    return '';
  };
  

  ngOnInit(): void{
    this.getRaceNames();
    // console.log(this.raceNames)
  }

 check(){
  let formattedDate:any|null
  if(this.date){  formattedDate = this.date.toLocaleDateString('ja-JP',{
    year:"numeric",
    month: "long",
    day: "numeric",
  });}else{formattedDate = null}

  console.log(formattedDate);
  if(formattedDate){
    this.raceNamesDisplay = this.raceNames.filter(raceName => raceName.date === formattedDate)
  }else{
    this.raceNamesDisplay = this.raceNames
  }
  

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
      this.raceNamesDisplay = this.raceNames
    })
  }

}
