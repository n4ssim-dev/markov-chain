from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "wikipedia.db"

RAW_DIR.mkdir(parents=True, exist_ok=True)

from .run import main

__all__ = ["PROJECT_ROOT", "RAW_DIR", "DB_PATH", "main"]