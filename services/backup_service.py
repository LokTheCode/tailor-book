"""Backup and restore of everything the app stores.

A backup is a single .zip file containing:
  tailor.db          the database (customers, orders, measurements, settings...)
  customer_photos/   customer photos
  branding/          shop logo
"""

import sqlite3
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from database.database import DB_PATH, engine
from services import settings_service

DATA_DIR = Path(DB_PATH).parent
EXTRA_FOLDERS = ["customer_photos", "branding"]
AUTO_PREFIX = "Auto_"


class BackupError(Exception):
    pass


def backup_folder() -> Path:
    folder = settings_service.get("backup_folder").strip()
    path = Path(folder) if folder else Path.home() / "Documents" / "TailorBackups"
    path.mkdir(parents=True, exist_ok=True)
    return path


def backup_now(auto: bool = False) -> Path:
    """Create a backup zip and return its path."""
    folder = backup_folder()
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"{AUTO_PREFIX if auto else ''}TailorBackup_{stamp}"
    target = folder / f"{name}.zip"
    counter = 2
    while target.exists():  # never overwrite an existing backup
        target = folder / f"{name}_{counter}.zip"
        counter += 1

    with tempfile.TemporaryDirectory() as tmp:
        # sqlite's backup API gives a consistent copy even while the app is open
        copy_path = Path(tmp) / "tailor.db"
        source = sqlite3.connect(DB_PATH)
        dest = sqlite3.connect(copy_path)
        try:
            source.backup(dest)
        finally:
            dest.close()
            source.close()

        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(copy_path, "tailor.db")
            for name in EXTRA_FOLDERS:
                folder_path = DATA_DIR / name
                if folder_path.is_dir():
                    for file in folder_path.rglob("*"):
                        if file.is_file():
                            archive.write(file, f"{name}/{file.relative_to(folder_path).as_posix()}")

    settings_service.set("last_backup_at", datetime.now().strftime("%d %b %Y, %I:%M %p"))

    if auto:
        _prune_auto_backups(folder)

    return target


def daily_backup_if_due() -> Path | None:
    """Make today's automatic backup if it hasn't been made yet.

    Called when the app starts and every 30 minutes while it's open,
    so a shop that keeps the app open all day still gets one backup a day.
    """
    if not settings_service.get_bool("backup_daily"):
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    if settings_service.get("last_auto_backup_date") == today:
        return None

    path = backup_now(auto=True)
    settings_service.set("last_auto_backup_date", today)
    return path


def _prune_auto_backups(folder: Path) -> None:
    keep = max(1, settings_service.get_int("backup_keep", 10))
    autos = sorted(folder.glob(f"{AUTO_PREFIX}TailorBackup_*.zip"), reverse=True)
    for old in autos[keep:]:
        try:
            old.unlink()
        except OSError:
            pass


def list_backups() -> list[Path]:
    return sorted(backup_folder().glob("*TailorBackup_*.zip"), reverse=True)


def restore(zip_path: str) -> Path:
    """Replace the current data with a backup.

    A safety backup of the current data is made first and its path is
    returned. The app must be restarted afterwards.
    """
    zip_path = Path(zip_path)
    try:
        with zipfile.ZipFile(zip_path) as archive:
            names = archive.namelist()
            if "tailor.db" not in names:
                raise BackupError("This file is not a Tailor ERP backup (tailor.db is missing).")

            with tempfile.TemporaryDirectory() as tmp:
                archive.extract("tailor.db", tmp)
                check = sqlite3.connect(Path(tmp) / "tailor.db")
                try:
                    tables = {r[0] for r in check.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                finally:
                    check.close()
                if "customers" not in tables:
                    raise BackupError("The database in this backup looks damaged.")

                safety = backup_now(auto=False)

                # Close all database connections before replacing the file
                engine.dispose()

                restored = sqlite3.connect(Path(tmp) / "tailor.db")
                current = sqlite3.connect(DB_PATH)
                try:
                    restored.backup(current)
                finally:
                    current.close()
                    restored.close()

            for name in EXTRA_FOLDERS:
                members = [m for m in names if m.startswith(f"{name}/") and not m.endswith("/")]
                for member in members:
                    archive.extract(member, DATA_DIR)

    except zipfile.BadZipFile:
        raise BackupError("This file is not a valid backup .zip file.")

    return safety
