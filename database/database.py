import os
import sys
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_db_path() -> str:
    """Returns absolute path to store tailor.db safely in user AppData folder."""
    if sys.platform == "win32":
        # %LOCALAPPDATA%\TailorManagement
        base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        # ~/Library/Application Support/TailorManagement
        base_dir = Path.home() / "Library" / "Application Support"
    else:
        # Linux / Unix
        base_dir = Path.home() / ".config"

    app_dir = base_dir / "TailorManagement"
    app_dir.mkdir(parents=True, exist_ok=True)  # Creates folder if it doesn't exist
    return str(app_dir / "tailor.db")


# Construct absolute SQLite database URL
DB_PATH = get_db_path()
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine setup
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for multithreaded Qt apps
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db():
    """Provides a transactional database session for context management.
    
    Usage:
        with get_db() as db:
            db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initializes tables in the SQLite database."""
    Base.metadata.create_all(bind=engine)