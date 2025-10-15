import { Routes } from '@angular/router';
import { PersonaStudioComponent } from './pages/persona-studio/persona-studio.component';
import { VoiceLabComponent } from './pages/voice-lab/voice-lab.component';
import { ScriptBuilderComponent } from './pages/script-builder/script-builder.component';
import { RenderQueueComponent } from './pages/render-queue/render-queue.component';
import { BrandingComponent } from './pages/branding/branding.component';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'persona' },
  { path: 'persona', component: PersonaStudioComponent },
  { path: 'voice', component: VoiceLabComponent },
  { path: 'script', component: ScriptBuilderComponent },
  { path: 'render', component: RenderQueueComponent },
  { path: 'branding', component: BrandingComponent }
];
