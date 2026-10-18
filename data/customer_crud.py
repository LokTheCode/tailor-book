"""Customer create / read / update / delete.

All customer changes from the UI go through this module, so the rules
(validation, duplicate mobile check, photo storage, safe delete) live in
one place.
"""

import re
import shutil
import time
from datetime import timezone
from pathlib import Path

from database.database import DB_PATH, SessionLocal
from models.customer import Customer
from models.measurement import CustomerMeasurement
from models.order import Order


# Shared by the customer form and the customer list filter
CUSTOMER_TYPES = ["Regular", "VIP", "Wholesale", "Corporate"]
GENDERS = ["Male", "Female", "Other"]

# Customer photos are copied here so they survive the original file
# being moved or deleted (next to tailor.db, e.g.
# %LOCALAPPDATA%\TailorBook\customer_photos on Windows)
PHOTO_DIR = Path(DB_PATH).parent / "customer_photos"

MOBILE_PATTERN = re.compile(r"^\d{10}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CustomerError(Exception):
    """A problem with the customer data, with a message for the user."""


class CustomerHasOrders(CustomerError):
    """Raised when deleting a customer who still has orders."""

    def __init__(self, order_count):
        self.order_count = order_count
        super().__init__(
            f"This customer has {order_count} order{'s' if order_count != 1 else ''}, "
            "so they can't be deleted. Deactivate them instead to hide them "
            "from new orders while keeping their history."
        )


# ==========================================================
# VALIDATION
# ==========================================================

def validate_customer(data: dict, customer_id: int | None = None) -> None:
    """Raise CustomerError if the data can't be saved."""

    name = (data.get("name") or "").strip()
    mobile = (data.get("mobile") or "").strip()
    alternate = (data.get("alternate_mobile") or "").strip()
    email = (data.get("email") or "").strip()

    if not name:
        raise CustomerError("Customer name is required.")
    if not MOBILE_PATTERN.match(mobile):
        raise CustomerError("Mobile number must be exactly 10 digits.")
    if alternate and not MOBILE_PATTERN.match(alternate):
        raise CustomerError("Alternate mobile must be exactly 10 digits.")
    if alternate and alternate == mobile:
        raise CustomerError("Alternate mobile can't be the same as the mobile number.")
    if email and not EMAIL_PATTERN.match(email):
        raise CustomerError("Enter a valid email address, or leave it empty.")

    customer_type = data.get("customer_type")
    if customer_type and normalize_type(customer_type) not in CUSTOMER_TYPES:
        raise CustomerError(f"Unknown customer type: {customer_type}")

    db = SessionLocal()
    try:
        query = db.query(Customer).filter(Customer.mobile == mobile)
        if customer_id:
            query = query.filter(Customer.id != customer_id)
        existing = query.first()
        if existing:
            raise CustomerError(
                f"Mobile {mobile} is already used by {existing.name} (ID {existing.id})."
            )
    finally:
        db.close()


def normalize_type(value: str | None) -> str:
    """Match a stored type like 'vip' or 'regular' to its display name."""
    for known in CUSTOMER_TYPES:
        if (value or "").strip().lower() == known.lower():
            return known
    return value or "Regular"


def _clean(data: dict) -> dict:
    """Trim text and turn empty optional fields into None."""
    cleaned = {}
    for key in ("name", "mobile", "alternate_mobile", "email", "reference", "address"):
        if key in data:
            value = (data.get(key) or "").strip()
            cleaned[key] = value or None
    if cleaned.get("email"):
        cleaned["email"] = cleaned["email"].lower()
    for key in ("gender", "is_active"):
        if key in data:
            cleaned[key] = data[key]
    if "customer_type" in data:
        cleaned["customer_type"] = normalize_type(data["customer_type"])
    return cleaned


# ==========================================================
# PHOTO
# ==========================================================

def store_photo(source: str | None, customer_id: int) -> str | None:
    """Copy a chosen photo into the app's photo folder and return the new path.

    Returns the path unchanged if it is already stored there, and None
    if there is no photo or the file no longer exists.
    """
    if not source:
        return None

    source_path = Path(source)
    if not source_path.is_file():
        return None

    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    if source_path.parent.resolve() == PHOTO_DIR.resolve():
        return str(source_path)

    target = PHOTO_DIR / f"customer_{customer_id}_{int(time.time())}{source_path.suffix.lower()}"
    shutil.copy2(source_path, target)
    return str(target)


def _remove_stored_photo(path: str | None) -> None:
    """Delete a photo only if it lives in the app's own photo folder."""
    if not path:
        return
    photo = Path(path)
    try:
        if photo.is_file() and photo.parent.resolve() == PHOTO_DIR.resolve():
            photo.unlink()
    except OSError:
        pass


# ==========================================================
# CREATE
# ==========================================================

def create_customer(data: dict) -> dict:
    """Validate and save a new customer (with optional first measurement)."""
    validate_customer(data)
    values = _clean(data)

    db = SessionLocal()
    try:
        customer = Customer(
            name=values["name"],
            mobile=values["mobile"],
            alternate_mobile=values.get("alternate_mobile"),
            email=values.get("email"),
            gender=values.get("gender") or "Male",
            customer_type=values.get("customer_type") or "Regular",
            reference=values.get("reference"),
            address=values.get("address"),
            is_active=values.get("is_active", True),
        )
        db.add(customer)
        db.flush()  # Generates customer.id before committing

        customer.photo = store_photo(data.get("photo_path") or data.get("photo"), customer.id)

        # Handle optional measurement payload during creation
        if isinstance(data.get("measurements"), dict):
            m_data = data["measurements"]
            db.add(CustomerMeasurement(
                customer_id=customer.id,
                measurement_name=m_data.get("measurement_name", "Standard Fit"),
                upper_measurements=m_data.get("upper_measurements"),
                lower_measurements=m_data.get("lower_measurements"),
                extra_measurements=m_data.get("extra_measurements"),
                notes=m_data.get("notes"),
            ))

        db.commit()
        db.refresh(customer)
        return _customer_to_dict(customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==========================================================
# READ
# ==========================================================

def get_all_customers() -> list[dict]:
    """All active customers, newest first (used by order and measurement forms)."""
    db = SessionLocal()
    try:
        customers = (
            db.query(Customer)
            .filter(Customer.is_active == True)  # noqa: E712
            .order_by(Customer.id.desc())
            .all()
        )
        return [_customer_to_dict(c) for c in customers]
    finally:
        db.close()


def get_customer_by_id(customer_id: int) -> dict | None:
    db = SessionLocal()
    try:
        customer = db.get(Customer, customer_id)
        return _customer_to_dict(customer) if customer else None
    finally:
        db.close()


# ==========================================================
# UPDATE
# ==========================================================

def update_customer(customer_id: int, data: dict) -> dict | None:
    """Validate and update a customer. Returns None if it doesn't exist."""
    db = SessionLocal()
    try:
        customer = db.get(Customer, customer_id)
        if not customer:
            return None

        # Fill in fields not being changed so validation sees the full record
        merged = _customer_to_dict(customer)
        merged.update(data)
        if "customer_type" not in data:
            merged.pop("customer_type")  # only check the type when it's being changed
        validate_customer(merged, customer_id=customer_id)

        for key, value in _clean(data).items():
            setattr(customer, key, value)

        if "photo_path" in data or "photo" in data:
            new_photo = data.get("photo_path") if "photo_path" in data else data.get("photo")
            stored = store_photo(new_photo, customer.id)
            if stored != customer.photo:
                _remove_stored_photo(customer.photo)
            customer.photo = stored

        db.commit()
        db.refresh(customer)
        return _customer_to_dict(customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def set_customer_active(customer_id: int, active: bool) -> bool:
    """Activate or deactivate a customer (inactive customers are hidden
    from the order and measurement forms but keep their history)."""
    db = SessionLocal()
    try:
        customer = db.get(Customer, customer_id)
        if not customer:
            return False
        customer.is_active = bool(active)
        db.commit()
        return True
    finally:
        db.close()


# ==========================================================
# DELETE
# ==========================================================

def count_customer_orders(customer_id: int) -> int:
    db = SessionLocal()
    try:
        return db.query(Order).filter(Order.customer_id == customer_id).count()
    finally:
        db.close()


def delete_customer(customer_id: int) -> bool:
    """Permanently delete a customer and their measurements.

    Raises CustomerHasOrders if they have orders, because deleting them
    would leave orders pointing at a customer that no longer exists.
    Use set_customer_active(customer_id, False) for those customers.
    """
    db = SessionLocal()
    try:
        customer = db.get(Customer, customer_id)
        if not customer:
            return False

        order_count = db.query(Order).filter(Order.customer_id == customer_id).count()
        if order_count:
            raise CustomerHasOrders(order_count)

        photo = customer.photo
        db.delete(customer)  # measurements are removed by the model's cascade
        db.commit()
        _remove_stored_photo(photo)
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==========================================================
# HELPERS
# ==========================================================

def _local_date(value) -> str:
    """created_at is stored in UTC; show it as a local date."""
    if not value:
        return ""
    return value.replace(tzinfo=timezone.utc).astimezone().strftime("%d %b %Y")


def _customer_to_dict(customer: Customer) -> dict:
    """Convert a Customer row to a plain dict for the UI."""
    return {
        "id": customer.id,
        "name": customer.name or "",
        "mobile": customer.mobile or "",
        "alternate_mobile": customer.alternate_mobile or "",
        "email": customer.email or "",
        "gender": customer.gender or "Male",
        "customer_type": normalize_type(customer.customer_type),
        "reference": customer.reference or "",
        "address": customer.address or "",
        "photo": customer.photo or "",
        "photo_path": customer.photo or "",
        "is_active": bool(customer.is_active),
        "created_at": _local_date(customer.created_at),
    }
