import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RaceresultComponent } from './raceresult.component';

describe('RaceresultComponent', () => {
  let component: RaceresultComponent;
  let fixture: ComponentFixture<RaceresultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RaceresultComponent]
    });
    fixture = TestBed.createComponent(RaceresultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
