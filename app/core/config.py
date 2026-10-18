import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://usuario:pass@localhost:5432/libreria",
)
ECHO_SQL = os.getenv("ECHO_SQL", "false").lower() == "true"
