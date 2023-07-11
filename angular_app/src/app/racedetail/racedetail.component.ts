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
  raceResult: any[] = [];
  raceOdds: any[] = [];
  flag: number = 0;

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
    this.raceaService.getResult(this.raceName).subscribe((data)=>{
      this.raceResult = data.result.sort((a:any,b:any)=>a.place_num-b.place_num);
      this.raceOdds = data.odds;
      console.log(this.raceResult);
    } )
  }

  sortResult(){
    this.raceResult.sort((a:any,b:any)=>((-1)**this.flag)*(b.place_num-a.place_num))
    this.flag = 1 -this.flag
  }

}


