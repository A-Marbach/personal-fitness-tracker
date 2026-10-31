import pytest

from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.dependencies import get_db
from app.models.weight import WeightEntry


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


def test_create_weight(client):
    response = client.post(
        "/api/v1/weights",
        json={
            "recorded_on": "2026-10-31",
            "weight_kg": 110,
        },
    )

    assert response.status_code == 201
    assert response.json()["weight_kg"] == "110.00"


def test_list_weights(client):
    client.post(
        "/api/v1/weights",
        json={
            "recorded_on": "2026-10-31",
            "weight_kg": 110,
        },
    )

    response = client.get("/api/v1/weights")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_weight(client):
    payload = {
        "recorded_on": "2026-10-31",
        "weight_kg": 110,
    }

    client.post("/api/v1/weights", json=payload)

    response = client.post(
        "/api/v1/weights",
        json=payload,
    )

    assert response.status_code == 409


def test_invalid_weight(client):
    response = client.post(
        "/api/v1/weights",
        json={
            "recorded_on": "2026-10-31",
            "weight_kg": -10,
        },
    )

    assert response.status_code == 422
