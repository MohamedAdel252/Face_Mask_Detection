import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-webcam-mask',
  templateUrl: './webcam-mask.html',
  styleUrls: ['./webcam-mask.css']
})
export class WebcamMaskComponent {
  @ViewChild('video') videoRef!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  result: any = null;
  stream: MediaStream | null = null;
  intervalId: any = null;

  apiUrl = 'http://127.0.0.1:8000/predict';

  constructor(private http: HttpClient) {}

  async startCamera() {
    this.stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });

    this.videoRef.nativeElement.srcObject = this.stream;

    this.intervalId = setInterval(() => {
      this.captureAndSendFrame();
    }, 500);
  }

  stopCamera() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }

  captureAndSendFrame() {
    const video = this.videoRef.nativeElement;
    const canvas = this.canvasRef.nativeElement;
    const context = canvas.getContext('2d');

    if (!context || video.videoWidth === 0 || video.videoHeight === 0) {
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append('file', blob, 'frame.jpg');

      this.http.post(this.apiUrl, formData).subscribe({
        next: (res) => {
          this.result = res;
        },
        error: (err) => {
          console.error(err);
        }
      });
    }, 'image/jpeg');
  }
}
