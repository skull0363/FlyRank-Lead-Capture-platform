from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./dev_fallback.db"
    import warnings
    warnings.warn(
        "DATABASE_URL is not set -- falling back to a local SQLite file "
        "(sqlite:///./dev_fallback.db). Set DATABASE_URL in your .env for "
        "Postgres (see docker-compose.yml / .env.example).",
        stacklevel=2,
    )

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()