import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-script-builder',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './script-builder.component.html',
  styleUrls: ['./script-builder.component.css']
})
export class ScriptBuilderComponent {
  context = '';
  tone = 'confident';
  audience = 'board';
  draft = '';
  prosody = {
    rate: 0,
    pitch: 0,
    pauses: 0
  };
}
