import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface RenderStage {
  name: string;
  status: 'queued' | 'running' | 'complete';
}

@Component({
  selector: 'app-render-queue',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './render-queue.component.html',
  styleUrls: ['./render-queue.component.css']
})
export class RenderQueueComponent {
  stages: RenderStage[] = [
    { name: 'tts', status: 'running' },
    { name: 'align', status: 'queued' },
    { name: 'lipsync', status: 'queued' },
    { name: 'avatar', status: 'queued' },
    { name: 'compose', status: 'queued' },
    { name: 'deliver', status: 'queued' }
  ];
}
