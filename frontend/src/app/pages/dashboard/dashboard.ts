
import {
  Component,
  computed,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';

import {
  FitnessApi,
  WeightEntry,
  WorkoutEntry,
  WeightCreate,
  WorkoutCreate,
} from '../../core/services/fitness-api';

import {
  ProgressChart,
  ProgressPoint,
} from '../../shared/components/progress-chart/progress-chart';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [FormsModule, ProgressChart],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  private readonly fitnessApi = inject(FitnessApi);

  readonly weight = signal<number | null>(null);
  readonly pullUps = signal<number | null>(null);
  readonly pushUps = signal<number | null>(null);

  readonly weights = signal<WeightEntry[]>([]);
  readonly workouts = signal<WorkoutEntry[]>([]);

  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly error = signal('');
  readonly success = signal('');

  inputWeight: number | null = null;
  inputPullUps: number | null = null;
  inputPushUps: number | null = null;

  // Gewichtsdaten für Chart.js
  readonly weightChart = computed<ProgressPoint[]>(() =>
    this.weights().map((entry) => ({
      date: entry.recorded_on,
      value: Number(entry.weight_kg),
    }))
  );

  // Klimmzüge für Chart.js
  readonly pullUpsChart = computed<ProgressPoint[]>(() =>
    this.workouts().map((entry) => ({
      date: entry.recorded_on,
      value: entry.pull_ups,
    }))
  );

  // Liegestütze für Chart.js
  readonly pushUpsChart = computed<ProgressPoint[]>(() =>
    this.workouts().map((entry) => ({
      date: entry.recorded_on,
      value: entry.push_ups,
    }))
  );

  ngOnInit(): void {
    this.loadData();
  }

  private getToday(): string {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
  }

  loadData(): void {
    this.loading.set(true);
    this.error.set('');

    forkJoin({
      weights: this.fitnessApi.getWeights(),
      workouts: this.fitnessApi.getWorkouts(),
    }).subscribe({
      next: ({ weights, workouts }) => {
        this.weights.set(weights);
        this.workouts.set(workouts);

        this.weight.set(
          weights.length ? Number(weights[0].weight_kg) : null
        );

        this.pullUps.set(workouts[0]?.pull_ups ?? null);
        this.pushUps.set(workouts[0]?.push_ups ?? null);

        const today = this.getToday();

        const todayWeight = weights.find(
          (entry) => entry.recorded_on === today
        );

        const todayWorkout = workouts.find(
          (entry) => entry.recorded_on === today
        );

        this.inputWeight = todayWeight
          ? Number(todayWeight.weight_kg)
          : null;

        this.inputPullUps = todayWorkout?.pull_ups ?? null;
        this.inputPushUps = todayWorkout?.push_ups ?? null;

        this.loading.set(false);
      },
      error: (err) => {
        console.error('Loading failed:', err);
        this.error.set('Daten konnten nicht geladen werden.');
        this.loading.set(false);
      },
    });
  }

  saveValues(): void {
    this.error.set('');
    this.success.set('');

    if (
      this.inputWeight === null ||
      !Number.isFinite(this.inputWeight) ||
      this.inputWeight <= 0 ||
      this.inputWeight > 999.99 ||
      Math.round(this.inputWeight * 100) !==
        this.inputWeight * 100 ||
      this.inputPullUps === null ||
      this.inputPushUps === null ||
      !Number.isSafeInteger(this.inputPullUps) ||
      !Number.isSafeInteger(this.inputPushUps) ||
      this.inputPullUps < 0 ||
      this.inputPushUps < 0
    ) {
      this.error.set('Bitte alle drei Werte gültig eingeben.');
      return;
    }

    const today = this.getToday();

    const weightPayload: WeightCreate = {
      recorded_on: today,
      weight_kg: this.inputWeight,
    };

    const workoutPayload: WorkoutCreate = {
      recorded_on: today,
      pull_ups: this.inputPullUps,
      push_ups: this.inputPushUps,
    };

    const weightExists = this.weights().some(
      (entry) => entry.recorded_on === today
    );

    const workoutExists = this.workouts().some(
      (entry) => entry.recorded_on === today
    );

    const weightRequest = weightExists
      ? this.fitnessApi.updateWeight(today, weightPayload)
      : this.fitnessApi.createWeight(weightPayload);

    const workoutRequest = workoutExists
      ? this.fitnessApi.updateWorkout(today, workoutPayload)
      : this.fitnessApi.createWorkout(workoutPayload);

    this.saving.set(true);

    forkJoin({
      weight: weightRequest,
      workout: workoutRequest,
    }).subscribe({
      next: () => {
        this.saving.set(false);
        this.success.set('Deine Werte wurden gespeichert.');
        this.loadData();
      },
      error: (err) => {
        console.error('Saving failed:', err);
        this.saving.set(false);
        this.error.set(
          'Speichern fehlgeschlagen. Bitte Werte prüfen.'
        );
        this.loadData();
      },
    });
  }
}
