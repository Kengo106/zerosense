import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { RaceService } from '../race.service';


@Component({
  selector: 'app-racedetail',
  templateUrl: './racedetail.component.html',
  styleUrls: ['./racedetail.component.scss']
})
export class RacedetailComponent implements OnInit {

  raceName: string = '';
  raceResult: any[] = []

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private raceaService: RaceService,
  ){}

  ngOnInit(){
    this.getRaceName();
    this.getRaceResult();
  }

  getRaceName(){
    this.raceName = String(this.route.snapshot.paramMap.get('race_name'))
  }

  goBack(){
    this.location.back()
  }

  getRaceResult(){
    this.raceaService.getResult(this.raceName).subscribe((data)=>{this.raceResult = data.sort((a:any,b:any)=>a.place_num-b.place_num);console.log(this.raceResult);} )

  }

}


