from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.workout import WorkoutEntry
from app.schemas.workout import WorkoutCreate, WorkoutResponse


router = APIRouter(
    prefix="/api/v1/workouts",
    tags=["Workouts"],
)


@router.post(
    "",
    response_model=WorkoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workout(
    payload: WorkoutCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(WorkoutEntry).where(
            WorkoutEntry.recorded_on == payload.recorded_on
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Workout already exists for this date",
        )

    entry = WorkoutEntry(**payload.model_dump())
    db.add(entry)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Workout already exists for this date",
        ) from None

    db.refresh(entry)
    return entry


@router.get("", response_model=list[WorkoutResponse])
def list_workouts(db: Session = Depends(get_db)):
    return db.scalars(
        select(WorkoutEntry).order_by(
            WorkoutEntry.recorded_on.desc()
        )
    ).all()


@router.put("/{recorded_on}", response_model=WorkoutResponse)
def update_workout(
    recorded_on: date,
    payload: WorkoutCreate,
    db: Session = Depends(get_db),
):
    entry = db.scalar(
        select(WorkoutEntry).where(
            WorkoutEntry.recorded_on == recorded_on
        )
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found",
        )

    if payload.recorded_on != recorded_on:
        raise HTTPException(
            status_code=422,
            detail="Date in URL and body must match",
        )

    entry.pull_ups = payload.pull_ups
    entry.push_ups = payload.push_ups

    db.commit()
    db.refresh(entry)

    return entry