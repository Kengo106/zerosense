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
  flagPlace: number = 0;
  flagOddsTan: number = 0;

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
    console.log(this.raceName)
  }

  goBack(){
    this.location.back()
  }

  getRaceResult(){
    this.raceaService.getResult(this.raceName).subscribe((data)=>{
      this.raceResult = data.map((item: any)=>({
        created_at: item.RaceResult.created_at,
        horse_name: item.RaceResult.horse_name,
        horse_number: item.RaceResult.horse_number,
        odds_fuku_max: item.Odds.odds_fuku_max,
        odds_fuku_min: item.Odds.odds_fuku_min,
        odds_tan: item.Odds.odds_tan,
        h_weight: item.RaceResult.h_weight,
        jockey_name: item.RaceResult.jockey_name,
        place_num: item.RaceResult.place_num,
        pop: item.RaceResult.pop,
        time: item.RaceResult.time,
        trainer_name: item.RaceResult.trainer_name,
      }))
      console.log(this.raceResult);
      this.raceResult.sort((a:any,b:any)=>(a.place_num-b.place_num))
    } )
  }

  sortPlace(){
    this.raceResult.sort((a:any,b:any)=>((-1)**this.flagPlace)*(b.place_num-a.place_num))
    this.flagPlace = 1 - this.flagPlace
  }
  sortOddsTan(){
    this.raceResult.sort((a:any,b:any)=>((-1)**this.flagOddsTan)*(b.odds_tan-a.odds_tan))
    this.flagOddsTan = 1 - this.flagOddsTan
  }

}


