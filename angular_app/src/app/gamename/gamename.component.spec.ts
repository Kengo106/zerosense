import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamenameComponent } from './gamename.component';

describe('GamenameComponent', () => {
  let component: GamenameComponent;
  let fixture: ComponentFixture<GamenameComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GamenameComponent]
    });
    fixture = TestBed.createComponent(GamenameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
