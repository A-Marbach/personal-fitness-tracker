
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(ROOT_DIR / ".env")

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

DATABASE_URL = (
    "postgresql+psycopg://fitness_user:"
    f"{POSTGRES_PASSWORD}@127.0.0.1:5433/fitness_tracker"
)
