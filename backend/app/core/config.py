
import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(ROOT_DIR / ".env")

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "fitness_tracker")
DB_USER = os.getenv("DB_USER", "fitness_user")

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:"
    f"{quote(POSTGRES_PASSWORD, safe='')}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
