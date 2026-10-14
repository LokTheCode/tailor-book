from datetime import datetime

from sqlalchemy import func, or_

from database.database import SessionLocal
from models.customer import Customer
from models.measurement import CustomerMeasurement


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

    db = SessionLocal()

    try:

        query = (
            db.query(
                CustomerMeasurement,
                Customer,
            )
            .join(
                Customer,
                Customer.id
                == CustomerMeasurement.customer_id,
            )
        )

        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        search = (search or "").strip()

        if search:

            search_value = f"%{search}%"

            query = query.filter(
                or_(
                    Customer.name.ilike(
                        search_value
                    ),

                    Customer.mobile.ilike(
                        search_value
                    ),

                    CustomerMeasurement.measurement_name.ilike(
                        search_value
                    ),
                )
            )

        # --------------------------------------------------
        # GARMENT
        # --------------------------------------------------

        if garment and garment != "All Garments":

            query = query.filter(
                CustomerMeasurement.measurement_name.ilike(
                    f"{garment}%"
                )
            )

        # --------------------------------------------------
        # DATE
        # --------------------------------------------------

        if date_value:

            if hasattr(date_value, "toPython"):

                date_value = date_value.toPython()

            query = query.filter(
                func.date(
                    CustomerMeasurement.created_at
                ) == date_value
            )

        # --------------------------------------------------
        # TOTAL
        # --------------------------------------------------

        total_records = query.count()

        total_pages = max(
            1,
            (
                total_records + page_size - 1
            ) // page_size
        )

        page = max(
            1,
            min(page, total_pages)
        )

        offset = (
            page - 1
        ) * page_size

        rows = (
            query
            .order_by(
                CustomerMeasurement.id.desc()
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        data = []

        for measurement, customer in rows:

            data.append({

                "id": measurement.id,

                "customer_id":
                    measurement.customer_id,

                "customer_name":
                    customer.name or "",

                "mobile":
                    customer.mobile or "",

                "measurement_name":
                    measurement.measurement_name or "",

                "created_at":
                    measurement.created_at,

                "updated_at":
                    measurement.updated_at,

                "notes":
                    measurement.notes or "",

                "upper_measurements":
                    measurement.upper_measurements or {},

                "lower_measurements":
                    measurement.lower_measurements or {},

                "extra_measurements":
                    measurement.extra_measurements or {},

            })

        return {
            "items": data,
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

        total = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .scalar()
            or 0
        )

        today = datetime.now().date()

        today_count = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .filter(
                func.date(
                    CustomerMeasurement.created_at
                ) == today
            )
            .scalar()
            or 0
        )

        updated_today = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .filter(
                func.date(
                    CustomerMeasurement.updated_at
                ) == today
            )
            .scalar()
            or 0
        )

        customers = (
            db.query(
                func.count(
                    func.distinct(
                        CustomerMeasurement.customer_id
                    )
                )
            )
            .scalar()
            or 0
        )

        shirts = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .filter(
                CustomerMeasurement.measurement_name.ilike(
                    "Shirt%"
                )
            )
            .scalar()
            or 0
        )

        pants = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .filter(
                CustomerMeasurement.measurement_name.ilike(
                    "Pant%"
                )
            )
            .scalar()
            or 0
        )

        suits = (
            db.query(
                func.count(
                    CustomerMeasurement.id
                )
            )
            .filter(
                CustomerMeasurement.measurement_name.ilike(
                    "Suit%"
                )
            )
            .scalar()
            or 0
        )

        return {

            "total": total,

            "shirts": shirts,

            "pants": pants,

            "suits": suits,

            "today": today_count,

            "updated_today": updated_today,

            "customers": customers,

        }

    finally:

        db.close()