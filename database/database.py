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
    """Create the database file, every table and any missing columns.

    Safe to run on every start: on a new PC it builds everything from
    scratch, and on an existing database it only adds what is missing.
    """
    # Importing the models registers every table on Base.metadata.
    # Without this, create_all() would only know about tables that
    # happened to be imported earlier.
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _add_missing_columns()


def _add_missing_columns():
    """Add columns that were added to a model after the table was created.

    create_all() never changes an existing table, so an older tailor.db
    would be missing new columns (for example admins.permissions).
    SQLite can add simple columns with ALTER TABLE ... ADD COLUMN.
    """
    from datetime import datetime
    from sqlalchemy import inspect, text, Boolean, Integer, Float, Numeric, DateTime, Date

    inspector = inspect(engine)

    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue

            existing = {col["name"] for col in inspector.get_columns(table.name)}

            for column in table.columns:
                if column.name in existing or column.primary_key:
                    continue

                col_type = column.type.compile(dialect=engine.dialect)
                ddl = f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {col_type}'

                if not column.nullable:
                    # Existing rows need a value for a NOT NULL column
                    default = column.default.arg if column.default is not None and column.default.is_scalar else None

                    if isinstance(default, bool):
                        literal = "1" if default else "0"
                    elif isinstance(default, (int, float)):
                        literal = str(default)
                    elif isinstance(default, str):
                        literal = "'" + default.replace("'", "''") + "'"
                    elif isinstance(column.type, (DateTime, Date)):
                        # SQLite only accepts a constant default here
                        literal = "'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'"
                    elif isinstance(column.type, (Boolean, Integer, Float, Numeric)):
                        literal = "0"
                    else:
                        literal = "''"

                    ddl += f" NOT NULL DEFAULT {literal}"

                conn.execute(text(ddl))
                print(f"Database: added column {table.name}.{column.name}")