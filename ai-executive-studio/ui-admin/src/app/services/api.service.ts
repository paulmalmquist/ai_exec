import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = (window as any).__env?.apiBase ?? 'http://localhost:8000/orchestrator';

  async savePersona(body: unknown): Promise<string> {
    const response = await this.http.post<{ id: string; summary: string }>(`${this.baseUrl}/persona`, body).toPromise();
    return response?.summary ?? 'Persona saved.';
  }

  async uploadVoice(formData: FormData): Promise<unknown> {
    return this.http.post(`${this.baseUrl}/voice`, formData).toPromise();
  }

  async previewTts(payload: unknown): Promise<Blob> {
    return this.http.post(`${this.baseUrl}/preview`, payload, { responseType: 'blob' }).toPromise() as Promise<Blob>;
  }
}
