import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-persona-studio',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './persona-studio.component.html',
  styleUrls: ['./persona-studio.component.css']
})
export class PersonaStudioComponent {
  form = this.fb.group({
    name: [''],
    styleGuidelines: ['Confident, analytical, willing to argue'],
    assertiveness: [70],
    formality: [50],
    argumentativeness: [80],
    riskPosture: ['medium']
  });

  sampleOutput = '';

  constructor(private readonly fb: FormBuilder, private readonly api: ApiService) {}

  async save(): Promise<void> {
    const body = {
      name: this.form.value.name,
      style_guidelines: this.form.value.styleGuidelines,
      argumentation_level: this.form.value.argumentativeness,
      risk_posture: this.form.value.riskPosture
    };
    this.sampleOutput = await this.api.savePersona(body);
  }
}
