from database.database import SessionLocal
from models.measurement import CustomerMeasurement
from models.customer import Customer


# ==========================================================
# CREATE
# ==========================================================

def create_measurement(data: dict) -> dict:

    db = SessionLocal()

    try:

        customer_id = data.get("customer_id")

        if not customer_id:
            raise ValueError("Customer is required.")

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found.")

        measurement_name = (
            data.get("measurement_name")
            or "Standard Fit"
        )

        measurement = CustomerMeasurement(
            customer_id=customer_id,
            measurement_name=measurement_name,

            upper_measurements=data.get(
                "upper_measurements"
            ),

            lower_measurements=data.get(
                "lower_measurements"
            ),

            extra_measurements=data.get(
                "extra_measurements"
            ),

            notes=data.get("notes"),
        )

        db.add(measurement)
        db.commit()
        db.refresh(measurement)

        return _measurement_to_dict(measurement)

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# ==========================================================
# GET ALL MEASUREMENTS FOR CUSTOMER
# ==========================================================

def get_measurements_by_customer(
    customer_id: int,
) -> list[dict]:

    db = SessionLocal()

    try:

        measurements = (
            db.query(CustomerMeasurement)
            .filter(
                CustomerMeasurement.customer_id == customer_id
            )
            .order_by(
                CustomerMeasurement.id.desc()
            )
            .all()
        )

        return [
            _measurement_to_dict(item)
            for item in measurements
        ]

    finally:

        db.close()


# ==========================================================
# GET SINGLE MEASUREMENT
# ==========================================================

def get_measurement_by_id(
    measurement_id: int,
) -> dict | None:

    db = SessionLocal()

    try:

        measurement = (
            db.query(CustomerMeasurement)
            .filter(
                CustomerMeasurement.id == measurement_id
            )
            .first()
        )

        if not measurement:
            return None

        return _measurement_to_dict(measurement)

    finally:

        db.close()


# ==========================================================
# UPDATE
# ==========================================================

def update_measurement(
    measurement_id: int,
    data: dict,
) -> dict | None:

    db = SessionLocal()

    try:

        measurement = (
            db.query(CustomerMeasurement)
            .filter(
                CustomerMeasurement.id == measurement_id
            )
            .first()
        )

        if not measurement:
            return None

        if "measurement_name" in data:
            measurement.measurement_name = (
                data["measurement_name"]
            )

        if "upper_measurements" in data:
            measurement.upper_measurements = (
                data["upper_measurements"]
            )

        if "lower_measurements" in data:
            measurement.lower_measurements = (
                data["lower_measurements"]
            )

        if "extra_measurements" in data:
            measurement.extra_measurements = (
                data["extra_measurements"]
            )

        if "notes" in data:
            measurement.notes = data["notes"]

        db.commit()
        db.refresh(measurement)

        return _measurement_to_dict(measurement)

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# ==========================================================
# DELETE
# ==========================================================

def delete_measurement(
    measurement_id: int,
) -> bool:

    db = SessionLocal()

    try:

        measurement = (
            db.query(CustomerMeasurement)
            .filter(
                CustomerMeasurement.id == measurement_id
            )
            .first()
        )

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
# SERIALIZER
# ==========================================================

def _measurement_to_dict(
    measurement: CustomerMeasurement,
) -> dict:

    return {
        "id": measurement.id,
        "customer_id": measurement.customer_id,
        "measurement_name": (
            measurement.measurement_name or ""
        ),

        "upper_measurements": (
            measurement.upper_measurements or {}
        ),

        "lower_measurements": (
            measurement.lower_measurements or {}
        ),

        "extra_measurements": (
            measurement.extra_measurements or {}
        ),

        "notes": measurement.notes or "",

        "created_at": (
            measurement.created_at.isoformat()
            if measurement.created_at
            else None
        ),

        "updated_at": (
            measurement.updated_at.isoformat()
            if measurement.updated_at
            else None
        ),
    }