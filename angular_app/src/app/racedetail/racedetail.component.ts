import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';


@Component({
  selector: 'app-racedetail',
  templateUrl: './racedetail.component.html',
  styleUrls: ['./racedetail.component.scss']
})
export class RacedetailComponent implements OnInit {

  racename: string = '';

  constructor(
    private route: ActivatedRoute,
    private location: Location
  ){}

  ngOnInit(){
    this.getRaceName();
  }

  getRaceName(){
    this.racename = String(this.route.snapshot.paramMap.get('race_name'))
  }

  goBack(){
    this.location.back()
  }

}
