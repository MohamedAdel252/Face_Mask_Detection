import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  @ViewChild('video') videoRef!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  apiUrl = 'http://localhost:8000/predict';

  selectedFile: File | null = null;
  previewUrl: string | null = null;
  result: { status: string; confidence: number; action: string } | null = null;
  loading = false;
  errorMessage = '';

  stream: MediaStream | null = null;
  intervalId: any = null;
  cameraRunning = false;

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) return;

    this.selectedFile = input.files[0];
    this.result = null;
    this.errorMessage = '';

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
      this.cdr.detectChanges();
    };
    reader.readAsDataURL(this.selectedFile);
  }

  async predict() {
    if (!this.selectedFile) return;

    this.loading = true;
    this.errorMessage = '';
    this.result = null;
    this.cdr.detectChanges();

    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);

    try {
      const res = await firstValueFrom(
  this.http.post<any>(this.apiUrl, formData)
);

this.result = res.prediction;

    } catch (err) {
      this.errorMessage = 'Prediction failed. Make sure the API is running and CORS is enabled.';
    }

    this.loading = false;
    this.cdr.detectChanges();
  }

  async startCamera() {
    this.errorMessage = '';
    this.result = null;

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
      });

      this.videoRef.nativeElement.srcObject = this.stream;
      this.cameraRunning = true;

      this.intervalId = setInterval(() => {
        this.captureAndPredict();
      }, 500);

    } catch (err) {
      this.errorMessage = 'Cannot access camera. Please allow camera permission.';
    }
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

    this.cameraRunning = false;
  }

  captureAndPredict() {
    const video = this.videoRef.nativeElement;
    const canvas = this.canvasRef.nativeElement;
    const context = canvas.getContext('2d');

    if (!context || video.videoWidth === 0 || video.videoHeight === 0) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append('file', blob, 'frame.jpg');

      try {
        const res = await firstValueFrom(
          this.http.post<any>(this.apiUrl, formData)
        );

        this.result = res.prediction;
        this.cdr.detectChanges();
      } catch (err) {
        console.error(err);
      }
    }, 'image/jpeg');
  }

  reset() {
    this.stopCamera();
    this.selectedFile = null;
    this.previewUrl = null;
    this.result = null;
    this.errorMessage = '';
    this.loading = false;
  }

  formatStatus(status: string): string {
    return status === 'with_mask' ? 'Mask Detected' : 'No Mask Detected';
  }

  getStatusClass(): string {
    if (!this.result) return '';
    return this.result.status === 'with_mask' ? 'success' : 'danger';
  }

  getConfidenceWidth(): string {
    if (!this.result) return '0%';
    return `${this.result.confidence}%`;
  }
}
