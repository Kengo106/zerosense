import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExitgameComponent } from './exitgame.component';

describe('ExitgameComponent', () => {
  let component: ExitgameComponent;
  let fixture: ComponentFixture<ExitgameComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExitgameComponent]
    });
    fixture = TestBed.createComponent(ExitgameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
