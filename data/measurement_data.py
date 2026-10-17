"""Measurement list (search, filter, paging) and statistics."""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import and_, func, or_

from data.measurement_crud import _measurement_to_dict, guess_garment
from database.database import SessionLocal
from models.customer import Customer
from models.measurement import CustomerMeasurement
from services import settings_service


# ==========================================================
# HELPERS
# ==========================================================

def _utc_range(day: date):
    """Start/end of a local calendar day, in UTC (how created_at is stored)."""
    start_local = datetime.combine(day, time.min).astimezone()
    end_local = start_local + timedelta(days=1)
    to_utc = lambda value: value.astimezone(timezone.utc).replace(tzinfo=None)  # noqa: E731
    return to_utc(start_local), to_utc(end_local)


def _garment_filter(garment: str):
    """Match the saved garment, or (for older rows) a name starting with it."""
    return or_(
        func.lower(CustomerMeasurement.garment) == garment.lower(),
        and_(
            or_(CustomerMeasurement.garment.is_(None), CustomerMeasurement.garment == ""),
            CustomerMeasurement.measurement_name.ilike(f"{garment}%"),
        ),
    )


# ==========================================================
# LIST MEASUREMENTS
# ==========================================================

def get_measurement_list(
    search: str = "",
    garment: str = "All Garments",
    date_value=None,
    page: int = 1,
    page_size: int = 10,
):
    """date_value: None for all dates, or a date / QDate for one local day."""

    db = SessionLocal()
    try:
        query = (
            db.query(CustomerMeasurement, Customer)
            .join(Customer, Customer.id == CustomerMeasurement.customer_id)
        )

        search = (search or "").strip()
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    Customer.name.ilike(like),
                    Customer.mobile.ilike(like),
                    CustomerMeasurement.measurement_name.ilike(like),
                    CustomerMeasurement.garment.ilike(like),
                )
            )

        if garment and garment != "All Garments":
            query = query.filter(_garment_filter(garment))

        if date_value is not None:
            if hasattr(date_value, "toPython"):
                date_value = date_value.toPython()
            start, end = _utc_range(date_value)
            query = query.filter(
                CustomerMeasurement.updated_at >= start,
                CustomerMeasurement.updated_at < end,
            )

        total_records = query.count()
        total_pages = max(1, (total_records + page_size - 1) // page_size)
        page = max(1, min(page, total_pages))

        rows = (
            query
            .order_by(CustomerMeasurement.updated_at.desc(), CustomerMeasurement.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        garments = settings_service.get_list("garment_types")
        items = []
        for measurement, customer in rows:
            item = _measurement_to_dict(measurement, customer)
            if not item["garment"]:
                item["garment"] = guess_garment(item["measurement_name"], garments)
            items.append(item)

        return {
            "items": items,
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
        }
    finally:
        db.close()


# ==========================================================
# STATISTICS
# ==========================================================

def get_measurement_stats():
    db = SessionLocal()
    try:
        count = func.count(CustomerMeasurement.id)

        total = db.query(count).scalar() or 0

        start, end = _utc_range(date.today())
        today_count = (
            db.query(count)
            .filter(CustomerMeasurement.created_at >= start, CustomerMeasurement.created_at < end)
            .scalar() or 0
        )
        updated_today = (
            db.query(count)
            .filter(CustomerMeasurement.updated_at >= start, CustomerMeasurement.updated_at < end)
            .scalar() or 0
        )
        customers = (
            db.query(func.count(func.distinct(CustomerMeasurement.customer_id))).scalar() or 0
        )

        def by_garment(name):
            return db.query(count).filter(_garment_filter(name)).scalar() or 0

        return {
            "total": total,
            "shirts": by_garment("Shirt"),
            "pants": by_garment("Pant"),
            "suits": by_garment("Suit"),
            "today": today_count,
            "updated_today": updated_today,
            "customers": customers,
        }
    finally:
        db.close()
