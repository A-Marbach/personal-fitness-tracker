
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.weight import WeightEntry
from app.schemas.weight import WeightCreate, WeightResponse


router = APIRouter(
    prefix="/api/v1/weights",
    tags=["Weights"],
)


@router.post(
    "",
    response_model=WeightResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_weight(
    payload: WeightCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(WeightEntry).where(
            WeightEntry.recorded_on == payload.recorded_on
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Weight entry already exists for this date",
        )

    entry = WeightEntry(**payload.model_dump())
    db.add(entry)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Weight entry already exists for this date",
        ) from None

    db.refresh(entry)
    return entry


@router.get("", response_model=list[WeightResponse])
def list_weights(db: Session = Depends(get_db)):
    return db.scalars(
        select(WeightEntry).order_by(
            WeightEntry.recorded_on.desc()
        )
    ).all()


@router.put(
    "/{recorded_on}",
    response_model=WeightResponse,
)
def update_weight(
    recorded_on: date,
    payload: WeightCreate,
    db: Session = Depends(get_db),
):
    entry = db.scalar(
        select(WeightEntry).where(
            WeightEntry.recorded_on == recorded_on
        )
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Weight entry not found",
        )

    if payload.recorded_on != recorded_on:
        raise HTTPException(
            status_code=422,
            detail="Date in URL and body must match",
        )

    entry.weight_kg = payload.weight_kg

    db.commit()
    db.refresh(entry)

    return entry
