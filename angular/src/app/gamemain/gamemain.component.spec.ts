import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamemainComponent } from './gamemain.component';

describe('GamemainComponent', () => {
  let component: GamemainComponent;
  let fixture: ComponentFixture<GamemainComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GamemainComponent]
    });
    fixture = TestBed.createComponent(GamemainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
