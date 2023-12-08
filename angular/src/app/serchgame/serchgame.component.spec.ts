import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SerchgameComponent } from './serchgame.component';

describe('SerchgameComponent', () => {
  let component: SerchgameComponent;
  let fixture: ComponentFixture<SerchgameComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SerchgameComponent]
    });
    fixture = TestBed.createComponent(SerchgameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
