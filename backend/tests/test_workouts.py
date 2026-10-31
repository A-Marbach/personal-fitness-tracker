
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.dependencies import get_db
from app.main import app
from app.models.workout import WorkoutEntry


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_create_workout(client):
    response = client.post(
        "/api/v1/workouts",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 8,
            "push_ups": 25,
        },
    )

    assert response.status_code == 201
    assert response.json()["pull_ups"] == 8
    assert response.json()["push_ups"] == 25


def test_list_workouts(client):
    client.post(
        "/api/v1/workouts",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 8,
            "push_ups": 25,
        },
    )

    response = client.get("/api/v1/workouts")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_workout(client):
    payload = {
        "recorded_on": "2026-10-31",
        "pull_ups": 8,
        "push_ups": 25,
    }

    assert client.post(
        "/api/v1/workouts", json=payload
    ).status_code == 201

    response = client.post(
        "/api/v1/workouts", json=payload
    )

    assert response.status_code == 409


def test_invalid_workout(client):
    response = client.post(
        "/api/v1/workouts",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": -1,
            "push_ups": 25,
        },
    )

    assert response.status_code == 422


def test_update_workout(client):
    client.post(
        "/api/v1/workouts",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 0,
            "push_ups": 0,
        },
    )

    response = client.put(
        "/api/v1/workouts/2026-10-31",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 8,
            "push_ups": 25,
        },
    )

    assert response.status_code == 200
    assert response.json()["pull_ups"] == 8
    assert response.json()["push_ups"] == 25


def test_update_nonexistent_workout(client):
    response = client.put(
        "/api/v1/workouts/2026-10-31",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 8,
            "push_ups": 25,
        },
    )

    assert response.status_code == 404


def test_update_mismatched_date(client):
    client.post(
        "/api/v1/workouts",
        json={
            "recorded_on": "2026-10-31",
            "pull_ups": 0,
            "push_ups": 0,
        },
    )

    response = client.put(
        "/api/v1/workouts/2026-10-31",
        json={
            "recorded_on": "2026-11-01",
            "pull_ups": 8,
            "push_ups": 25,
        },
    )

    assert response.status_code == 422
