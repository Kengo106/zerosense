import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RacenamesComponent } from './racenames.component';

describe('RacenamesComponent', () => {
  let component: RacenamesComponent;
  let fixture: ComponentFixture<RacenamesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RacenamesComponent]
    });
    fixture = TestBed.createComponent(RacenamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
