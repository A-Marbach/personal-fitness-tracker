
import { Component, computed, input } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import type { ChartData, ChartOptions } from 'chart.js';

export interface ProgressPoint {
  date: string;
  value: number;
}

@Component({
  selector: 'app-progress-chart',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './progress-chart.html',
  styleUrl: './progress-chart.scss',
})
export class ProgressChart {
  readonly title = input.required<string>();
  readonly unit = input.required<string>();
  readonly color = input<string>('#60a5fa');
  readonly points = input<ProgressPoint[]>([]);

  readonly chartData = computed<ChartData<'line'>>(() => {
    const entries = [...this.points()].sort(
      (a, b) => a.date.localeCompare(b.date)
    );

    return {
      labels: entries.map((entry) =>
        new Date(`${entry.date}T12:00:00`).toLocaleDateString(
          'de-DE',
          { day: '2-digit', month: '2-digit' }
        )
      ),
      datasets: [
        {
          data: entries.map((entry) => entry.value),
          label: this.title(),
          borderColor: this.color(),
          backgroundColor: this.color(),
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6,
          fill: false,
        },
      ],
    };
  });

  readonly chartOptions = computed<ChartOptions<'line'>>(() => ({
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context) =>
            `${context.parsed.y ?? '–'} ${this.unit()}`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#94a3b8',
          maxTicksLimit: 6,
        },
        grid: {
          display: false,
        },
      },
      y: {
        ticks: {
          color: '#94a3b8',
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.12)',
        },
      },
    },
  }));
}
