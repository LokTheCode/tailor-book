from datetime import date, datetime, timedelta

from sqlalchemy import func, or_

from database.database import SessionLocal

from models.customer import Customer
from models.order import Order
from models.order_item import OrderItem
from models.order_payment import OrderPayment
from models.inventory import InventoryItem
from models.inventory_transaction import InventoryTransaction


# ==========================================================
# DATE RANGE HELPERS
# ==========================================================

def get_date_range(
    period="today",
    start_date=None,
    end_date=None,
):
    """
    Returns:

        start_date: datetime.date
        end_date: datetime.date

    Supported periods:

        today
        week
        month
        year
        custom
    """

    today = date.today()

    period = (
        str(period or "today")
        .strip()
        .lower()
    )

    # ------------------------------------------------------
    # TODAY
    # ------------------------------------------------------

    if period == "today":

        return today, today

    # ------------------------------------------------------
    # THIS WEEK
    # Monday -> Sunday
    # ------------------------------------------------------

    if period == "week":

        start = (
            today
            - timedelta(
                days=today.weekday()
            )
        )

        end = start + timedelta(
            days=6
        )

        return start, end

    # ------------------------------------------------------
    # THIS MONTH
    # ------------------------------------------------------

    if period == "month":

        start = today.replace(
            day=1
        )

        if today.month == 12:

            next_month = date(
                today.year + 1,
                1,
                1,
            )

        else:

            next_month = date(
                today.year,
                today.month + 1,
                1,
            )

        end = next_month - timedelta(
            days=1
        )

        return start, end

    # ------------------------------------------------------
    # THIS YEAR
    # ------------------------------------------------------

    if period == "year":

        start = date(
            today.year,
            1,
            1,
        )

        end = date(
            today.year,
            12,
            31,
        )

        return start, end

    # ------------------------------------------------------
    # CUSTOM
    # ------------------------------------------------------

    if period == "custom":

        if isinstance(
            start_date,
            datetime,
        ):
            start_date = (
                start_date.date()
            )

        if isinstance(
            end_date,
            datetime,
        ):
            end_date = (
                end_date.date()
            )

        if isinstance(
            start_date,
            str,
        ):
            start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d",
            ).date()

        if isinstance(
            end_date,
            str,
        ):
            end_date = datetime.strptime(
                end_date,
                "%Y-%m-%d",
            ).date()

        if not start_date:
            start_date = today

        if not end_date:
            end_date = today

        if start_date > end_date:

            start_date, end_date = (
                end_date,
                start_date,
            )

        return start_date, end_date

    # Fallback

    return today, today


# ==========================================================
# DATE FORMAT
# ==========================================================

def format_date_value(value):
    """
    Converts a date/datetime/string into YYYY-MM-DD.
    """

    if value is None:
        return ""

    if isinstance(
        value,
        datetime,
    ):
        return value.strftime(
            "%Y-%m-%d"
        )

    if isinstance(
        value,
        date,
    ):
        return value.strftime(
            "%Y-%m-%d"
        )

    value = str(value).strip()

    if not value:
        return ""

    # Already ISO
    try:

        return datetime.strptime(
            value[:10],
            "%Y-%m-%d",
        ).strftime(
            "%Y-%m-%d"
        )

    except ValueError:
        pass

    # DD/MM/YYYY
    try:

        return datetime.strptime(
            value[:10],
            "%d/%m/%Y",
        ).strftime(
            "%Y-%m-%d"
        )

    except ValueError:
        pass

    # DD-MM-YYYY
    try:

        return datetime.strptime(
            value[:10],
            "%d-%m-%Y",
        ).strftime(
            "%Y-%m-%d"
        )

    except ValueError:
        pass

    return value


# ==========================================================
# ORDER DATE FILTER
# ==========================================================

def apply_order_date_filter(
    query,
    start_date,
    end_date,
):
    """
    Order.order_date is currently String.

    This expects order_date to be stored as:
        YYYY-MM-DD

    which is what the current Order form should use.
    """

    start_text = start_date.strftime(
        "%Y-%m-%d"
    )

    end_text = end_date.strftime(
        "%Y-%m-%d"
    )

    return query.filter(
        func.substr(
            Order.order_date,
            1,
            10,
        ) >= start_text,
        func.substr(
            Order.order_date,
            1,
            10,
        ) <= end_text,
    )


# ==========================================================
# ORDER REPORT
# ==========================================================

def get_order_report(
    period="today",
    start_date=None,
    end_date=None,
):
    """
    Returns order report data for selected date range.
    """

    start_date, end_date = get_date_range(
        period,
        start_date,
        end_date,
    )

    db = SessionLocal()

    try:

        query = (
            db.query(
                Order,
                Customer.name.label(
                    "customer_name"
                ),
                Customer.mobile.label(
                    "customer_mobile"
                ),
            )
            .join(
                Customer,
                Customer.id
                == Order.customer_id,
            )
        )

        query = apply_order_date_filter(
            query,
            start_date,
            end_date,
        )

        query = query.order_by(
            Order.order_date.desc(),
            Order.id.desc(),
        )

        rows = query.all()

        result = []

        for order, customer_name, customer_mobile in rows:

            result.append({
                "order_id": order.id,
                "order_number": order.order_number,
                "customer_id": order.customer_id,
                "customer_name": customer_name or "",
                "customer_mobile": customer_mobile or "",
                "order_date": format_date_value(
                    order.order_date
                ),
                "delivery_date": format_date_value(
                    order.delivery_date
                ),
                "status": order.status or "",
                "subtotal": float(
                    order.subtotal or 0
                ),
                "discount": float(
                    order.discount or 0
                ),
                "tax": float(
                    order.tax or 0
                ),
                "total_amount": float(
                    order.total_amount or 0
                ),
                "advance_amount": float(
                    order.advance_amount or 0
                ),
                "remaining_amount": float(
                    order.remaining_amount or 0
                ),
                "description": (
                    order.description or ""
                ),
            })

        return {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "items": result,
            "total_records": len(result),
        }

    finally:

        db.close()


# ==========================================================
# ORDER SUMMARY
# ==========================================================

def get_order_summary(
    period="today",
    start_date=None,
    end_date=None,
):
    """
    Returns summary statistics for selected period.
    """

    data = get_order_report(
        period,
        start_date,
        end_date,
    )

    orders = data["items"]

    total_orders = len(
        orders
    )

    revenue = sum(
        item["total_amount"]
        for item in orders
    )

    delivered = sum(
        1
        for item in orders
        if str(
            item["status"]
        ).lower()
        == "delivered"
    )

    pending = sum(
        1
        for item in orders
        if str(
            item["status"]
        ).lower()
        in (
            "pending",
            "cutting",
            "stitching",
            "ready",
        )
    )

    advance = sum(
        item["advance_amount"]
        for item in orders
    )

    remaining = sum(
        item["remaining_amount"]
        for item in orders
    )

    return {
        "total_orders": total_orders,
        "revenue": revenue,
        "delivered": delivered,
        "pending": pending,
        "advance": advance,
        "remaining": remaining,
    }


# ==========================================================
# CUSTOMER REPORT
# ==========================================================

def get_customer_report(
    period="today",
    start_date=None,
    end_date=None,
):
    """
    Customers who placed orders in selected period.

    This makes the customer report useful for business
    activity instead of simply showing every customer.
    """

    start_date, end_date = get_date_range(
        period,
        start_date,
        end_date,
    )

    db = SessionLocal()

    try:

        query = (
            db.query(
                Customer,
                func.count(
                    Order.id
                ).label(
                    "order_count"
                ),
                func.sum(
                    Order.total_amount
                ).label(
                    "revenue"
                ),
                func.max(
                    Order.order_date
                ).label(
                    "last_order"
                ),
            )
            .join(
                Order,
                Order.customer_id
                == Customer.id,
            )
        )

        query = apply_order_date_filter(
            query,
            start_date,
            end_date,
        )

        query = query.filter(
            Customer.is_active == True
        )

        query = query.group_by(
            Customer.id
        )

        query = query.order_by(
            func.sum(
                Order.total_amount
            ).desc()
        )

        rows = query.all()

        result = []

        for customer, order_count, revenue, last_order in rows:

            result.append({
                "customer_id": customer.id,
                "customer_name": customer.name or "",
                "mobile": customer.mobile or "",
                "email": customer.email or "",
                "customer_type": (
                    customer.customer_type
                    or ""
                ),
                "reference": (
                    customer.reference
                    or ""
                ),
                "orders": int(
                    order_count or 0
                ),
                "revenue": float(
                    revenue or 0
                ),
                "last_order": format_date_value(
                    last_order
                ),
            })

        return {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "items": result,
            "total_records": len(result),
        }

    finally:

        db.close()


# ==========================================================
# CUSTOMER COUNT
# ==========================================================

def get_customer_report_count(
    period="today",
    start_date=None,
    end_date=None,
):
    data = get_customer_report(
        period,
        start_date,
        end_date,
    )

    return len(
        data["items"]
    )


# ==========================================================
# INVENTORY REPORT
# ==========================================================

def get_inventory_report(
    period="today",
    start_date=None,
    end_date=None,
):
    """
    Inventory report is based on inventory transactions
    occurring in the selected date range.
    """

    start_date, end_date = get_date_range(
        period,
        start_date,
        end_date,
    )

    db = SessionLocal()

    try:

        start_datetime = datetime.combine(
            start_date,
            datetime.min.time(),
        )

        end_datetime = datetime.combine(
            end_date,
            datetime.max.time(),
        )

        query = (
            db.query(
                InventoryTransaction,
                InventoryItem.name.label(
                    "item_name"
                ),
                InventoryItem.sku.label(
                    "sku"
                ),
                InventoryItem.category.label(
                    "category"
                ),
                InventoryItem.unit.label(
                    "unit"
                ),
            )
            .join(
                InventoryItem,
                InventoryItem.id
                == InventoryTransaction.inventory_item_id,
            )
        )

        query = query.filter(
            InventoryTransaction.created_at
            >= start_datetime,
            InventoryTransaction.created_at
            <= end_datetime,
        )

        query = query.order_by(
            InventoryTransaction.created_at.desc(),
            InventoryTransaction.id.desc(),
        )

        rows = query.all()

        result = []

        for transaction, item_name, sku, category, unit in rows:

            result.append({
                "transaction_id": transaction.id,
                "item_id": transaction.inventory_item_id,
                "item_name": item_name or "",
                "sku": sku or "",
                "category": category or "",
                "transaction_type": (
                    transaction.transaction_type
                    or ""
                ),
                "quantity": float(
                    transaction.quantity or 0
                ),
                "unit": unit or "",
                "reference_type": (
                    transaction.reference_type
                    or ""
                ),
                "reference_id": (
                    transaction.reference_id
                    or ""
                ),
                "notes": (
                    transaction.notes
                    or ""
                ),
                "created_at": (
                    transaction.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if transaction.created_at
                    else ""
                ),
            })

        return {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "items": result,
            "total_records": len(result),
        }

    finally:

        db.close()


# ==========================================================
# INVENTORY CURRENT STOCK
# ==========================================================

def get_inventory_current_stock():

    db = SessionLocal()

    try:

        items = (
            db.query(
                InventoryItem
            )
            .filter(
                InventoryItem.is_active
                == True
            )
            .order_by(
                InventoryItem.name.asc()
            )
            .all()
        )

        result = []

        for item in items:

            result.append({
                "item_id": item.id,
                "name": item.name or "",
                "category": (
                    item.category
                    or ""
                ),
                "sku": (
                    item.sku
                    or ""
                ),
                "unit": (
                    item.unit
                    or ""
                ),
                "quantity": float(
                    item.quantity or 0
                ),
                "minimum_quantity": float(
                    item.minimum_quantity
                    or 0
                ),
                "cost_price": float(
                    item.cost_price or 0
                ),
                "selling_price": float(
                    item.selling_price or 0
                ),
                "inventory_value": (
                    float(
                        item.quantity or 0
                    )
                    * float(
                        item.cost_price or 0
                    )
                ),
            })

        return result

    finally:

        db.close()


# ==========================================================
# INVENTORY SUMMARY
# ==========================================================

def get_inventory_report_summary(
    period="today",
    start_date=None,
    end_date=None,
):

    data = get_inventory_report(
        period,
        start_date,
        end_date,
    )

    transactions = data[
        "items"
    ]

    stock_in = sum(
        item["quantity"]
        for item in transactions
        if item["transaction_type"]
        == "IN"
    )

    stock_out = sum(
        item["quantity"]
        for item in transactions
        if item["transaction_type"]
        == "OUT"
    )

    adjustments = sum(
        item["quantity"]
        for item in transactions
        if item["transaction_type"]
        == "ADJUSTMENT"
    )

    current_stock = (
        get_inventory_current_stock()
    )

    inventory_value = sum(
        item["inventory_value"]
        for item in current_stock
    )

    return {
        "transaction_count": len(
            transactions
        ),
        "stock_in": stock_in,
        "stock_out": stock_out,
        "adjustments": adjustments,
        "inventory_value": inventory_value,
        "current_stock_items": len(
            current_stock
        ),
    }


# ==========================================================
# OVERALL REPORT
# ==========================================================

def get_overall_report(
    period="today",
    start_date=None,
    end_date=None,
):

    order_data = get_order_report(
        period,
        start_date,
        end_date,
    )

    customer_data = get_customer_report(
        period,
        start_date,
        end_date,
    )

    inventory_data = get_inventory_report(
        period,
        start_date,
        end_date,
    )

    return {
        "period": period,
        "start_date": order_data[
            "start_date"
        ],
        "end_date": order_data[
            "end_date"
        ],
        "orders": order_data[
            "items"
        ],
        "customers": customer_data[
            "items"
        ],
        "inventory": inventory_data[
            "items"
        ],
    }