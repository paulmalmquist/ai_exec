import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

interface ExecutiveProfile {
  name: string;
  role: string;
  focus: string[];
  decisionThemes: string[];
  dataInputs: string[];
  methods: string[];
  leadershipSignals: string[];
}

@Component({
  selector: 'app-executive-automation',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './executive-automation.component.html',
  styleUrls: ['./executive-automation.component.css']
})
export class ExecutiveAutomationComponent {
  readonly profiles: ExecutiveProfile[] = [
    {
      name: 'Jaymie Gelino',
      role: 'Global COO, Project & Development Services',
      focus: [
        'Global operating model consistency',
        'Process simplification and scalable growth',
        'Resource allocation across regions',
        'Technology investments for delivery performance'
      ],
      decisionThemes: [
        'Standardize best practices across markets',
        'Balance strategic expansion with operational rigor',
        'Drive efficiency, safety, and margin performance'
      ],
      dataInputs: [
        'Portfolio financials and margin trends',
        'Operational KPIs (schedule adherence, utilization, safety)',
        'Client pipeline and satisfaction signals',
        'Risk registers and scenario analyses'
      ],
      methods: [
        'Financial and operational modeling',
        'Earned Value Management (EVM)',
        'Scenario planning and risk-adjusted portfolio planning',
        'Continuous improvement / Lean workflows'
      ],
      leadershipSignals: [
        'Simplification and consistency as operating principles',
        'Talent-first approach with specialized expertise',
        'Client-centric, forward-looking strategy'
      ]
    },
    {
      name: 'Scott Kessling',
      role: 'COO, Americas PDS & Project Management Leader',
      focus: [
        'Regional delivery performance and quality',
        'Process/tool standardization and adoption',
        'Integrated data visibility across projects',
        'Scaling capacity for major client programs'
      ],
      decisionThemes: [
        'Select and implement project management platforms',
        'Set performance targets and risk review cadence',
        'Translate global strategy into regional execution'
      ],
      dataInputs: [
        'Real-time project status dashboards',
        'Schedule/cost variance and earned value metrics',
        'Client feedback and program forecasts',
        'Market intelligence (labor, regulatory, permitting)'
      ],
      methods: [
        'Predictive analytics and AI forecasting',
        'Portfolio optimization frameworks',
        'Financial modeling for resource scenarios',
        'Continuous improvement benchmarks'
      ],
      leadershipSignals: [
        'Technology-forward and transparency focused',
        'Collaborative, cross-team operating rhythm',
        'Operational excellence as baseline expectation'
      ]
    }
  ];

  readonly automationPatterns = [
    {
      title: 'Data-driven decision loops',
      description: 'Prioritize automated ingestion of project KPIs, risk metrics, and client signals into a single decision cockpit.'
    },
    {
      title: 'Portfolio-level optimization',
      description: 'Score projects and initiatives for ROI, risk, and resource demand to rebalance capacity continuously.'
    },
    {
      title: 'Scenario & risk automation',
      description: 'Run Monte Carlo and what-if simulations for cost volatility, schedule shifts, and staffing constraints.'
    },
    {
      title: 'Standardized delivery playbooks',
      description: 'Codify best practices and enforce workflow checklists for consistency across regions and teams.'
    },
    {
      title: 'Real-time visibility & integration',
      description: 'Integrate project management, finance, and talent systems to eliminate siloed reporting.'
    },
    {
      title: 'Client-adaptive strategy',
      description: 'Capture client feedback and market signals to shift focus toward growth sectors or service gaps.'
    },
    {
      title: 'Talent & knowledge management',
      description: 'Track skill coverage, identify capability gaps, and preserve lessons learned for reuse.'
    }
  ];

  form = this.fb.group({
    portfolioSnapshot: [''],
    decisionCadence: [''],
    dataSources: [''],
    automationGaps: [''],
    integrationNeeds: [''],
    successMetrics: [''],
    governanceConstraints: [''],
    changeManagement: ['']
  });

  savedAt = '';
  savedEntries: Array<{ label: string; value: string }> = [];

  constructor(private readonly fb: FormBuilder) {}

  save(): void {
    this.savedAt = new Date().toLocaleString();
    const labels: Record<string, string> = {
      portfolioSnapshot: 'Current portfolio snapshot',
      decisionCadence: 'Decision cadence & owners',
      dataSources: 'Data sources & dashboards',
      automationGaps: 'Automation gaps to close',
      integrationNeeds: 'Integration or tooling needs',
      successMetrics: 'Success metrics & targets',
      governanceConstraints: 'Governance or compliance constraints',
      changeManagement: 'Change management considerations'
    };

    this.savedEntries = Object.entries(this.form.value)
      .map(([key, value]) => ({
        label: labels[key] ?? key,
        value: (value ?? '').toString()
      }))
      .filter((entry) => entry.value.trim().length > 0);
  }
}
