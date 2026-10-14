from datetime import date

from database.database import SessionLocal

from models.order import Order
from models.order_item import OrderItem
from models.order_payment import OrderPayment


# ==========================================================
# ORDER NUMBER
# ==========================================================

def generate_order_number(db):

    last_order = (
        db.query(Order)
        .order_by(Order.id.desc())
        .first()
    )

    if not last_order:
        next_number = 1
    else:
        next_number = last_order.id + 1

    return f"ORD-{next_number:04d}"


# ==========================================================
# CREATE ORDER
# ==========================================================

def create_order(data):

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # Generate order number
        # --------------------------------------------------

        order_number = generate_order_number(db)

        # --------------------------------------------------
        # Create Order
        # --------------------------------------------------

        order = Order(

            order_number=order_number,

            customer_id=data["customer_id"],

            order_date=data["order_date"],

            delivery_date=data.get(
                "delivery_date"
            ),

            status=data.get(
                "status",
                "pending"
            ),

            subtotal=float(
                data.get(
                    "subtotal",
                    0
                )
            ),

            discount=float(
                data.get(
                    "discount",
                    0
                )
            ),

            tax=float(
                data.get(
                    "tax",
                    0
                )
            ),

            total_amount=float(
                data.get(
                    "total_amount",
                    0
                )
            ),

            advance_amount=float(
                data.get(
                    "advance_amount",
                    0
                )
            ),

            remaining_amount=float(
                data.get(
                    "remaining_amount",
                    0
                )
            ),

            description=data.get(
                "description"
            ),
        )

        db.add(order)

        db.flush()

        # --------------------------------------------------
        # Create Order Item
        # --------------------------------------------------

        quantity = int(
            data.get(
                "quantity",
                1
            )
        )

        unit_price = float(
            data.get(
                "unit_price",
                0
            )
        )

        item_total = (
            quantity * unit_price
        )

        item = OrderItem(

            order_id=order.id,

            garment_type=data.get(
                "garment_type",
                "Other"
            ),

            description=data.get(
                "item_description"
            ),

            quantity=quantity,

            unit_price=unit_price,

            discount=0,

            tax=0,

            total_amount=item_total,
        )

        db.add(item)

        db.flush()

        # --------------------------------------------------
        # Payment
        # --------------------------------------------------

        advance = float(
            data.get(
                "advance_amount",
                0
            )
        )

        if advance > 0:

            payment = OrderPayment(

                order_id=order.id,

                amount=advance,

                payment_date=data.get(
                    "order_date",
                    date.today().isoformat()
                ),

                payment_method=data.get(
                    "payment_method",
                    "cash"
                ),

                reference=data.get(
                    "payment_reference"
                ),

                notes=data.get(
                    "payment_notes"
                ),
            )

            db.add(payment)

        # --------------------------------------------------
        # Commit
        # --------------------------------------------------

        db.commit()

        db.refresh(order)

        return {
            "id": order.id,
            "order_number": order.order_number,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount,
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# UPDATE ORDER
# ==========================================================

def update_order(
    order_id,
    data
):

    db = SessionLocal()

    try:

        order = (
            db.query(Order)
            .filter(
                Order.id == order_id
            )
            .first()
        )

        if not order:
            return None

        # --------------------------------------------------
        # Update Order
        # --------------------------------------------------

        order.customer_id = data[
            "customer_id"
        ]

        order.order_date = data[
            "order_date"
        ]

        order.delivery_date = data.get(
            "delivery_date"
        )

        order.status = data.get(
            "status",
            "pending"
        )

        order.subtotal = float(
            data.get(
                "subtotal",
                0
            )
        )

        order.discount = float(
            data.get(
                "discount",
                0
            )
        )

        order.tax = float(
            data.get(
                "tax",
                0
            )
        )

        order.total_amount = float(
            data.get(
                "total_amount",
                0
            )
        )

        order.advance_amount = float(
            data.get(
                "advance_amount",
                0
            )
        )

        order.remaining_amount = float(
            data.get(
                "remaining_amount",
                0
            )
        )

        order.description = data.get(
            "description"
        )

        # --------------------------------------------------
        # Update first item
        # --------------------------------------------------

        item = (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id == order.id
            )
            .order_by(OrderItem.id.asc())
            .first()
        )

        if item:

            item.garment_type = data.get(
                "garment_type",
                "Other"
            )

            item.description = data.get(
                "item_description"
            )

            item.quantity = int(
                data.get(
                    "quantity",
                    1
                )
            )

            item.unit_price = float(
                data.get(
                    "unit_price",
                    0
                )
            )

            item.total_amount = (
                item.quantity *
                item.unit_price
            )

        else:

            item = OrderItem(

                order_id=order.id,

                garment_type=data.get(
                    "garment_type",
                    "Other"
                ),

                description=data.get(
                    "item_description"
                ),

                quantity=int(
                    data.get(
                        "quantity",
                        1
                    )
                ),

                unit_price=float(
                    data.get(
                        "unit_price",
                        0
                    )
                ),

                total_amount=(
                    int(
                        data.get(
                            "quantity",
                            1
                        )
                    )
                    *
                    float(
                        data.get(
                            "unit_price",
                            0
                        )
                    )
                ),
            )

            db.add(item)

        # --------------------------------------------------
        # Commit
        # --------------------------------------------------

        db.commit()

        db.refresh(order)

        return {
            "id": order.id,
            "order_number": order.order_number,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount,
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# DELETE ORDER
# ==========================================================

def delete_order(order_id):

    db = SessionLocal()

    try:

        order = (
            db.query(Order)
            .filter(
                Order.id == order_id
            )
            .first()
        )

        if not order:
            return False

        db.delete(order)

        db.commit()

        return True

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()