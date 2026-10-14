from datetime import datetime

from sqlalchemy import func, or_

from database.database import SessionLocal

from models.order import Order
from models.order_item import OrderItem
from models.order_payment import OrderPayment
from models.customer import Customer


# ==========================================================
# HELPERS
# ==========================================================

def _parse_date(value):

    if not value:
        return None

    if hasattr(value, "toString"):

        value = value.toString(
            "yyyy-MM-dd"
        )

    if isinstance(value, str):

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return None

    return value


# ==========================================================
# ORDER LIST
# ==========================================================

def get_order_list(

    search="",

    status="All Status",

    payment="All Payments",

    tailor="All Tailors",

    date_value=None,

    page=1,

    page_size=10,
):

    db = SessionLocal()

    try:

        query = (
            db.query(
                Order,
                Customer
            )
            .join(
                Customer,
                Customer.id == Order.customer_id
            )
        )

        # ==================================================
        # SEARCH
        # ==================================================

        if search:

            search_text = (
                f"%{search.strip()}%"
            )

            query = query.filter(

                or_(

                    Order.order_number.ilike(
                        search_text
                    ),

                    Customer.name.ilike(
                        search_text
                    ),

                    Customer.mobile.ilike(
                        search_text
                    ),

                    Order.description.ilike(
                        search_text
                    )
                )
            )

        # ==================================================
        # STATUS
        # ==================================================

        if (
            status
            and status != "All Status"
        ):

            query = query.filter(
                Order.status
                == status.lower()
            )

        # ==================================================
        # DATE
        # ==================================================

        selected_date = _parse_date(
            date_value
        )

        if selected_date:

            query = query.filter(
                Order.order_date
                == selected_date.isoformat()
            )

        # ==================================================
        # TOTAL RECORDS
        # ==================================================

        total_records = query.count()

        # ==================================================
        # PAGINATION
        # ==================================================

        total_pages = max(
            1,
            (
                total_records
                + page_size
                - 1
            )
            // page_size
        )

        page = min(
            max(
                page,
                1
            ),
            total_pages
        )

        offset = (
            page - 1
        ) * page_size

        rows = (
            query
            .order_by(
                Order.id.desc()
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        # ==================================================
        # BUILD ITEMS
        # ==================================================

        items = []

        for order, customer in rows:

            first_item = (
                db.query(OrderItem)
                .filter(
                    OrderItem.order_id
                    == order.id
                )
                .order_by(
                    OrderItem.id.asc()
                )
                .first()
            )

            # ------------------------------------------------
            # Garment text
            # ------------------------------------------------

            garments = ""

            quantity = 0

            if first_item:

                garments = (
                    first_item.garment_type
                )

                quantity = (
                    first_item.quantity
                )

            # ------------------------------------------------
            # Payment
            # ------------------------------------------------

            paid = float(
                order.advance_amount
                or 0
            )

            total = float(
                order.total_amount
                or 0
            )

            if paid >= total:

                payment_status = "Paid"

            elif paid > 0:

                payment_status = "Partial"

            else:

                payment_status = "Pending"

            # ------------------------------------------------
            # Payment filter
            # ------------------------------------------------

            if (
                payment
                and payment != "All Payments"
                and payment != payment_status
            ):

                continue

            # ------------------------------------------------
            # Progress
            # ------------------------------------------------

            progress = get_order_progress(
                order.status
            )

            # ------------------------------------------------
            # Overdue
            # ------------------------------------------------

            overdue = False

            if order.delivery_date:

                try:

                    delivery = datetime.strptime(
                        order.delivery_date,
                        "%Y-%m-%d"
                    ).date()

                    today = datetime.today().date()

                    if (
                        delivery < today
                        and order.status
                        not in (
                            "delivered",
                            "cancelled"
                        )
                    ):

                        overdue = True

                except ValueError:

                    pass

            items.append({

                "id":
                    order.id,

                "order_number":
                    order.order_number,

                "customer_id":
                    order.customer_id,

                "customer_name":
                    customer.name or "",

                "mobile":
                    customer.mobile or "",

                "garments":
                    garments,

                "quantity":
                    quantity,

                "delivery_date":
                    order.delivery_date,

                "payment_status":
                    payment_status,

                "paid":
                    paid,

                "total_amount":
                    total,

                "remaining_amount":
                    float(
                        order.remaining_amount
                        or 0
                    ),

                "progress":
                    progress,

                "status":
                    order.status,

                "tailor":
                    "—",

                "overdue":
                    overdue,

                "description":
                    order.description or "",

                "item":
                    (
                        {
                            "garment_type":
                                first_item.garment_type,

                            "description":
                                first_item.description,

                            "quantity":
                                first_item.quantity,

                            "unit_price":
                                first_item.unit_price,
                        }
                        if first_item
                        else None
                    ),

                "order_date":
                    order.order_date,

                "discount":
                    float(
                        order.discount or 0
                    ),

                "tax":
                    float(
                        order.tax or 0
                    ),

                "advance_amount":
                    paid,
            })

        return {

            "items":
                items,

            "current_page":
                page,

            "total_pages":
                total_pages,

            "total_records":
                len(items)
                if payment != "All Payments"
                else total_records,
        }

    finally:

        db.close()


# ==========================================================
# PROGRESS
# ==========================================================

def get_order_progress(status):

    progress_map = {

        "pending": 10,

        "received": 15,

        "measurement": 25,

        "cutting": 40,

        "stitching": 65,

        "ironing": 80,

        "trial": 90,

        "ready": 95,

        "delivered": 100,

        "cancelled": 0,
    }

    return progress_map.get(
        (status or "").lower(),
        0
    )


# ==========================================================
# STATISTICS
# ==========================================================

def get_order_stats():

    db = SessionLocal()

    try:

        total = (
            db.query(Order)
            .count()
        )

        cutting = (
            db.query(Order)
            .filter(
                Order.status == "cutting"
            )
            .count()
        )

        stitching = (
            db.query(Order)
            .filter(
                Order.status == "stitching"
            )
            .count()
        )

        trial = (
            db.query(Order)
            .filter(
                Order.status == "trial"
            )
            .count()
        )

        ready = (
            db.query(Order)
            .filter(
                Order.status == "ready"
            )
            .count()
        )

        delivered = (
            db.query(Order)
            .filter(
                Order.status == "delivered"
            )
            .count()
        )

        # --------------------------------------------------
        # Pending payment
        # --------------------------------------------------

        pending_payment = (
            db.query(
                func.coalesce(
                    func.sum(
                        Order.remaining_amount
                    ),
                    0
                )
            )
            .filter(
                Order.remaining_amount > 0
            )
            .scalar()
        )

        # --------------------------------------------------
        # Overdue
        # --------------------------------------------------

        today = datetime.today().date().isoformat()

        overdue = (
            db.query(Order)
            .filter(
                Order.delivery_date < today,

                Order.status.notin_([
                    "delivered",
                    "cancelled"
                ])
            )
            .count()
        )

        return {

            "total":
                total,

            "cutting":
                cutting,

            "stitching":
                stitching,

            "trial":
                trial,

            "ready":
                ready,

            "delivered":
                delivered,

            "pending_payment":
                float(
                    pending_payment or 0
                ),

            "overdue":
                overdue,
        }

    finally:

        db.close()