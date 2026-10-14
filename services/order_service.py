from datetime import datetime
from database.database import SessionLocal
from models.order import Order
from models.order_item import OrderItem
from models.order_payment import OrderPayment

class OrderService:

    @staticmethod
    def generate_order_number() -> str:
        """Generates sequential order numbers like ORD-000001."""
        db = SessionLocal()
        try:
            last_order = db.query(Order).order_by(Order.id.desc()).first()
            next_id = (last_order.id + 1) if last_order else 1
            return f"ORD-{next_id:06d}"
        finally:
            db.close()

    @classmethod
    def create_order(cls, customer_id: int, items_data: list, advance_amount: float = 0.0, 
                     discount: float = 0.0, tax: float = 0.0, delivery_date: str = None, 
                     description: str = None, created_by: int = None) -> Order:
        """
        Creates an order with items and records an advance payment if provided.
        items_data format: 
        [
            {"garment_type": "Shirt", "quantity": 2, "unit_price": 800, "description": "Blue Silk", "measurement_id": 1},
            {"garment_type": "Pant", "quantity": 1, "unit_price": 1000}
        ]
        """
        db = SessionLocal()
        try:
            order_number = cls.generate_order_number()
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 1. Calculate item subtotal
            subtotal = sum(item["quantity"] * item["unit_price"] for item in items_data)
            total_amount = max(0.0, subtotal - discount + tax)
            remaining_amount = max(0.0, total_amount - advance_amount)

            # 2. Create Order record
            order = Order(
                order_number=order_number,
                customer_id=customer_id,
                order_date=order_date,
                delivery_date=delivery_date,
                status="pending",
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                total_amount=total_amount,
                advance_amount=advance_amount,
                remaining_amount=remaining_amount,
                description=description,
                created_by=created_by
            )
            db.add(order)
            db.flush() # Retrieves order.id

            # 3. Create Order Items
            for item in items_data:
                qty = item.get("quantity", 1)
                unit_p = item.get("unit_price", 0.0)
                item_total = qty * unit_p
                
                order_item = OrderItem(
                    order_id=order.id,
                    garment_type=item["garment_type"],
                    description=item.get("description", ""),
                    quantity=qty,
                    unit_price=unit_p,
                    total_amount=item_total,
                    measurement_id=item.get("measurement_id")
                )
                db.add(order_item)

            # 4. Record Advance Payment (if any)
            if advance_amount > 0:
                payment = OrderPayment(
                    order_id=order.id,
                    amount=advance_amount,
                    payment_date=order_date,
                    payment_method="cash",
                    notes="Advance Payment on Order Creation",
                    created_by=created_by
                )
                db.add(payment)

            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def add_payment(order_id: int, amount: float, payment_method: str = "cash", 
                    reference: str = None, notes: str = None, created_by: int = None) -> Order:
        """Adds a payment to an existing order and recalculates the balance."""
        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise ValueError(f"Order #{order_id} not found.")

            payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payment = OrderPayment(
                order_id=order.id,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method,
                reference=reference,
                notes=notes,
                created_by=created_by
            )
            db.add(payment)

            # Recalculate remaining balance
            total_paid = sum(p.amount for p in order.payments) + amount
            order.remaining_amount = max(0.0, order.total_amount - total_paid)

            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def update_status(order_id: int, new_status: str) -> Order:
        """Updates order status: pending, cutting, stitching, ready, delivered, cancelled."""
        valid_statuses = ["pending", "cutting", "stitching", "ready", "delivered", "cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {valid_statuses}")

        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise ValueError(f"Order #{order_id} not found.")

            order.status = new_status
            db.commit()
            db.refresh(order)
            return order
        finally:
            db.close()

    @staticmethod
    def get_order_details(order_id: int):
        """Fetches an order with items, customer details, and payments."""
        db = SessionLocal()
        try:
            return db.query(Order).filter(Order.id == order_id).first()
        finally:
            db.close()

    # Add these methods inside OrderService:

    @staticmethod
    def get_orders_for_table(status_filter: str = None):
        """Returns order records directly formatted for PySide6 table display."""
        db = SessionLocal()
        try:
            query = db.query(Order)
            if status_filter and status_filter.lower() != "all":
                query = query.filter(Order.status == status_filter)
            
            orders = query.order_by(Order.id.desc()).all()
            return [
                {
                    "id": o.id,
                    "order_number": o.order_number,
                    "customer_name": o.customer.name if o.customer else "Unknown",
                    "customer_mobile": o.customer.mobile if o.customer else "-",
                    "date": o.order_date,
                    "delivery": o.delivery_date or "-",
                    "status": o.status.title(),
                    "total": f"₹{o.total_amount:,.2f}",
                    "remaining": f"₹{o.remaining_amount:,.2f}"
                }
                for o in orders
            ]
        finally:
            db.close()

    @staticmethod
    def get_dashboard_summary():
        """Returns total counts and metrics for the Dashboard cards."""
        db = SessionLocal()
        try:
            all_orders = db.query(Order).all()
            total_orders = len(all_orders)
            pending_orders = sum(1 for o in all_orders if o.status in ["pending", "cutting", "stitching"])
            total_revenue = sum(o.total_amount for o in all_orders)
            total_pending_balance = sum(o.remaining_amount for o in all_orders)

            return {
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "total_revenue": f"₹{total_revenue:,.2f}",
                "pending_balance": f"₹{total_pending_balance:,.2f}"
            }
        finally:
            db.close()