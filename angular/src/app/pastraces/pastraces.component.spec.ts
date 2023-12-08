import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PastracesComponent } from './pastraces.component';

describe('PastracesComponent', () => {
  let component: PastracesComponent;
  let fixture: ComponentFixture<PastracesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PastracesComponent]
    });
    fixture = TestBed.createComponent(PastracesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
