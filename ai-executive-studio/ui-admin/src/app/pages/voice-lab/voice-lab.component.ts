import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-voice-lab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './voice-lab.component.html',
  styleUrls: ['./voice-lab.component.css']
})
export class VoiceLabComponent {
  selectedFiles: FileList | null = null;
  previewText = 'The quarterly outlook remains strong.';
  previewUrl: string | null = null;

  constructor(private readonly api: ApiService) {}

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFiles = input.files;
  }

  async upload(): Promise<void> {
    if (!this.selectedFiles?.length) {
      return;
    }
    const formData = new FormData();
    Array.from(this.selectedFiles).forEach((file) => formData.append('files', file));
    await this.api.uploadVoice(formData);
    alert('Voice uploaded');
  }
}
