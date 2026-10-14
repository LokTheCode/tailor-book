from database.database import SessionLocal
from models.customer import Customer
from models.measurement import CustomerMeasurement


def create_customer(data: dict) -> dict:
    """Save a new customer to the database along with optional initial measurements."""
    db = SessionLocal()
    try:
        customer = Customer(
            name=data.get("name"),
            mobile=data.get("mobile"),
            alternate_mobile=data.get("alternate_mobile"),
            email=data.get("email"),
            gender=data.get("gender", "Male"),
            customer_type=data.get("customer_type", "Regular"),
            reference=data.get("reference"),
            address=data.get("address"),
            photo=data.get("photo_path") or data.get("photo"),
            is_active=data.get("is_active", True),
        )
        db.add(customer)
        db.flush()  # Generates customer.id before committing

        # Handle optional measurement payload during creation
        if "measurements" in data and isinstance(data["measurements"], dict):
            m_data = data["measurements"]
            measurement = CustomerMeasurement(
                customer_id=customer.id,
                measurement_name=m_data.get("measurement_name", "Standard Fit"),
                upper_measurements=m_data.get("upper_measurements"),
                lower_measurements=m_data.get("lower_measurements"),
                extra_measurements=m_data.get("extra_measurements"),
                notes=m_data.get("notes"),
            )
            db.add(measurement)

        db.commit()
        db.refresh(customer)

        return _customer_to_dict(customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_all_customers() -> list[dict]:
    """Fetch all active customers from the database."""
    db = SessionLocal()
    try:
        customers = (
            db.query(Customer)
            .filter(Customer.is_active == True)
            .order_by(Customer.id.desc())
            .all()
        )
        return [_customer_to_dict(c) for c in customers]
    finally:
        db.close()


def get_customer_by_id(customer_id: int) -> dict | None:
    """Fetch a single customer record by ID."""
    db = SessionLocal()
    try:
        customer = (
            db.query(Customer).filter(Customer.id == customer_id).first()
        )
        return _customer_to_dict(customer) if customer else None
    finally:
        db.close()


def update_customer(customer_id: int, data: dict) -> dict | None:
    """Update an existing customer safely while allowing explicit empty strings/cleared values."""
    db = SessionLocal()
    try:
        customer = (
            db.query(Customer).filter(Customer.id == customer_id).first()
        )
        if not customer:
            return None

        # Check explicit presence of key so fields can be cleared to empty strings or None
        if "name" in data:
            customer.name = data["name"]
        if "mobile" in data:
            customer.mobile = data["mobile"]
        if "alternate_mobile" in data:
            customer.alternate_mobile = data["alternate_mobile"]
        if "email" in data:
            customer.email = data["email"]
        if "gender" in data:
            customer.gender = data["gender"]
        if "customer_type" in data:
            customer.customer_type = data["customer_type"]
        if "reference" in data:
            customer.reference = data["reference"]
        if "address" in data:
            customer.address = data["address"]
        if "photo_path" in data:
            customer.photo = data["photo_path"]
        elif "photo" in data:
            customer.photo = data["photo"]
        if "is_active" in data:
            customer.is_active = data["is_active"]

        db.commit()
        db.refresh(customer)
        return _customer_to_dict(customer)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def delete_customer(customer_id: int) -> bool:
    """Soft delete a customer by setting is_active to False."""
    db = SessionLocal()
    try:
        customer = (
            db.query(Customer).filter(Customer.id == customer_id).first()
        )
        if customer:
            customer.is_active = False
            db.commit()
            return True
        return False
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _customer_to_dict(customer: Customer) -> dict:
    """Helper method to convert Customer model to a clean UI-ready dictionary."""
    return {
        "id": customer.id,
        "name": customer.name or "",
        "mobile": customer.mobile or "",
        "alternate_mobile": customer.alternate_mobile or "",
        "email": customer.email or "",
        "gender": customer.gender or "Male",
        "customer_type": customer.customer_type or "Regular",
        "reference": customer.reference or "",
        "address": customer.address or "",
        "photo": customer.photo or "",
        "photo_path": customer.photo or "",  # Native PySide6 key fallback
        "is_active": customer.is_active,
    }