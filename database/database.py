import os
import sys
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Folder used before the app was renamed to Tailor Book
OLD_DATA_FOLDER_NAME = "TailorManagement"


def _base_dir() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    return Path.home() / ".config"


def _move_old_data(old_dir: Path, new_dir: Path) -> None:
    """One-time copy of data from the old folder into the new one.

    The old folder is left untouched as a safety copy. File paths saved
    in the database (customer photos, shop logo) are updated to point at
    the new folder.
    """
    import shutil
    import sqlite3

    shutil.copytree(old_dir, new_dir)

    db_file = new_dir / "tailor.db"
    old_prefix, new_prefix = str(old_dir), str(new_dir)
    try:
        conn = sqlite3.connect(db_file)
        with conn:
            conn.execute(
                "UPDATE customers SET photo = REPLACE(photo, ?, ?) WHERE photo LIKE ?",
                (old_prefix, new_prefix, old_prefix + "%"),
            )
            conn.execute(
                "UPDATE settings SET value = REPLACE(value, ?, ?) WHERE key = 'shop_logo' AND value LIKE ?",
                (old_prefix, new_prefix, old_prefix + "%"),
            )
        conn.close()
    except sqlite3.Error as error:
        # Paths still work: the old folder (and its photos) is kept
        print(f"Could not update saved file paths: {error}")


def get_db_path() -> str:
    r"""Path of tailor.db in the user's app-data folder.

    Windows: %LOCALAPPDATA%\TailorBook\tailor.db
    """
    from config import DATA_FOLDER_NAME

    base_dir = _base_dir()
    app_dir = base_dir / DATA_FOLDER_NAME
    old_dir = base_dir / OLD_DATA_FOLDER_NAME

    if not app_dir.exists() and (old_dir / "tailor.db").exists():
        try:
            _move_old_data(old_dir, app_dir)
        except OSError as error:
            # Couldn't copy: keep using the old folder rather than start empty
            print(f"Using old data folder ({error})")
            return str(old_dir / "tailor.db")

    app_dir.mkdir(parents=True, exist_ok=True)
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