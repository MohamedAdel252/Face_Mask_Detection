import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebcamMask } from './webcam-mask';

describe('WebcamMask', () => {
  let component: WebcamMask;
  let fixture: ComponentFixture<WebcamMask>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WebcamMask],
    }).compileComponents();

    fixture = TestBed.createComponent(WebcamMask);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
