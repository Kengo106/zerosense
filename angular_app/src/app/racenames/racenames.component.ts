import { Component, OnInit } from '@angular/core';
import { RaceService } from '../race.service';

@Component({
  selector: 'app-racenames',
  templateUrl: './racenames.component.html',
  styleUrls: ['./racenames.component.scss']
})
export class RacenamesComponent implements OnInit {
  constructor( private raceService: RaceService ){}

  raceNames: any[] = [];

  ngOnInit(): void{
    this.getRaceNames();
  }

  getRaceNames(): void{
    this.raceService.getRaceNames().subscribe((data)=> {this.raceNames=data})
  }

}
