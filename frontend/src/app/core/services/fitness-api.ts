
import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface WeightEntry {
  id: number;
  recorded_on: string;
  weight_kg: string;
  created_at: string;
}

export interface WeightCreate {
  recorded_on: string;
  weight_kg: number;
}

export interface WorkoutEntry {
  id: number;
  recorded_on: string;
  pull_ups: number;
  push_ups: number;
  created_at: string;
}

export interface WorkoutCreate {
  recorded_on: string;
  pull_ups: number;
  push_ups: number;
}

@Injectable({
  providedIn: 'root',
})
export class FitnessApi {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/v1';

  getWeights(): Observable<WeightEntry[]> {
    return this.http.get<WeightEntry[]>(
      `${this.baseUrl}/weights`
    );
  }

  createWeight(data: WeightCreate): Observable<WeightEntry> {
    return this.http.post<WeightEntry>(
      `${this.baseUrl}/weights`,
      data
    );
  }

  updateWeight(
    date: string,
    data: WeightCreate
  ): Observable<WeightEntry> {
    return this.http.put<WeightEntry>(
      `${this.baseUrl}/weights/${date}`,
      data
    );
  }

  getWorkouts(): Observable<WorkoutEntry[]> {
    return this.http.get<WorkoutEntry[]>(
      `${this.baseUrl}/workouts`
    );
  }

  createWorkout(data: WorkoutCreate): Observable<WorkoutEntry> {
    return this.http.post<WorkoutEntry>(
      `${this.baseUrl}/workouts`,
      data
    );
  }

  updateWorkout(
    date: string,
    data: WorkoutCreate
  ): Observable<WorkoutEntry> {
    return this.http.put<WorkoutEntry>(
      `${this.baseUrl}/workouts/${date}`,
      data
    );
  }
}
