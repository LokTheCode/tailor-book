"""Measurement create / read / update / delete, with validation."""

import re
from datetime import timezone

from database.database import SessionLocal
from models.customer import Customer
from models.measurement import CustomerMeasurement

# Upper and lower body values must be numbers (e.g. 38 or 15.5).
# Extra measurements may be text (collar type, pocket style, ...).
NUMBER_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,2})?$")


class MeasurementError(ValueError):
    """A problem with the measurement data, with a message for the user."""


# ==========================================================
# VALIDATION
# ==========================================================

def _clean_values(values: dict | None, numeric: bool, section: str) -> dict:
    """Drop empty fields and check number fields."""
    cleaned = {}
    for key, value in (values or {}).items():
        text = str(value if value is not None else "").strip()
        if not text:
            continue
        if numeric:
            text = text.replace(",", ".")
            if not NUMBER_PATTERN.match(text) or float(text) <= 0:
                label = key.replace("_", " ").title()
                raise MeasurementError(
                    f"{section}: '{label}' must be a number like 38 or 15.5 (you entered '{value}')."
                )
        cleaned[key] = text
    return cleaned


def validate_measurement(data: dict) -> dict:
    """Return cleaned data or raise MeasurementError."""
    if not data.get("customer_id"):
        raise MeasurementError("Please select a customer.")

    name = (data.get("measurement_name") or "").strip()
    if not name:
        raise MeasurementError("Please enter a measurement name.")

    upper = _clean_values(data.get("upper_measurements"), True, "Upper body")
    lower = _clean_values(data.get("lower_measurements"), True, "Lower body")
    extra = _clean_values(data.get("extra_measurements"), False, "Extra")

    if not (upper or lower or extra):
        raise MeasurementError("Enter at least one measurement value.")

    return {
        "customer_id": int(data["customer_id"]),
        "measurement_name": name[:100],
        "garment": (data.get("garment") or "").strip() or None,
        "upper_measurements": upper,
        "lower_measurements": lower,
        "extra_measurements": extra,
        "notes": (data.get("notes") or "").strip() or None,
    }


# ==========================================================
# CREATE
# ==========================================================

def create_measurement(data: dict) -> dict:
    values = validate_measurement(data)

    db = SessionLocal()
    try:
        customer = db.get(Customer, values["customer_id"])
        if not customer:
            raise MeasurementError("Customer not found.")

        measurement = CustomerMeasurement(**values)
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
        return _measurement_to_dict(measurement, customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==========================================================
# READ
# ==========================================================

def get_measurements_by_customer(customer_id: int) -> list[dict]:
    db = SessionLocal()
    try:
        rows = (
            db.query(CustomerMeasurement)
            .filter(CustomerMeasurement.customer_id == customer_id)
            .order_by(CustomerMeasurement.id.desc())
            .all()
        )
        return [_measurement_to_dict(item) for item in rows]
    finally:
        db.close()


def get_measurement_by_id(measurement_id: int) -> dict | None:
    db = SessionLocal()
    try:
        measurement = db.get(CustomerMeasurement, measurement_id)
        if not measurement:
            return None
        return _measurement_to_dict(measurement, measurement.customer)
    finally:
        db.close()


# ==========================================================
# UPDATE
# ==========================================================

def update_measurement(measurement_id: int, data: dict) -> dict | None:
    values = validate_measurement(data)

    db = SessionLocal()
    try:
        measurement = db.get(CustomerMeasurement, measurement_id)
        if not measurement:
            return None

        if not db.get(Customer, values["customer_id"]):
            raise MeasurementError("Customer not found.")

        for key, value in values.items():
            setattr(measurement, key, value)

        db.commit()
        db.refresh(measurement)
        return _measurement_to_dict(measurement, measurement.customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==========================================================
# DELETE
# ==========================================================

def delete_measurement(measurement_id: int) -> bool:
    db = SessionLocal()
    try:
        measurement = db.get(CustomerMeasurement, measurement_id)
        if not measurement:
            return False
        db.delete(measurement)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==========================================================
# HELPERS
# ==========================================================

def guess_garment(measurement_name: str, garments: list[str]) -> str:
    """For older rows without a garment, use the name if it starts with one."""
    name = (measurement_name or "").lower()
    for garment in garments:
        if name.startswith(garment.lower()):
            return garment
    return ""


def local_time(value):
    """Timestamps are stored in UTC; convert to the PC's local time."""
    if not value:
        return None
    return value.replace(tzinfo=timezone.utc).astimezone()


def _measurement_to_dict(measurement: CustomerMeasurement, customer: Customer | None = None) -> dict:
    created = local_time(measurement.created_at)
    updated = local_time(measurement.updated_at)
    return {
        "id": measurement.id,
        "customer_id": measurement.customer_id,
        "customer_name": customer.name if customer else "",
        "mobile": customer.mobile if customer else "",
        "measurement_name": measurement.measurement_name or "",
        "garment": measurement.garment or "",
        "upper_measurements": measurement.upper_measurements or {},
        "lower_measurements": measurement.lower_measurements or {},
        "extra_measurements": measurement.extra_measurements or {},
        "notes": measurement.notes or "",
        "created_at": created,
        "updated_at": updated,
    }
