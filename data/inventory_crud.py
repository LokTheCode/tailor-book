from sqlalchemy.orm import Session

from database.database import SessionLocal

from models.inventory import InventoryItem
from models.inventory_transaction import InventoryTransaction


# ==========================================================
# INVENTORY ITEM
# ==========================================================

def create_inventory_item(data):

    db: Session = SessionLocal()

    try:

        item = InventoryItem(
            name=data["name"],
            category=data["category"],
            sku=data.get("sku"),
            unit=data.get("unit", "meter"),
            quantity=float(data.get("quantity", 0)),
            minimum_quantity=float(
                data.get("minimum_quantity", 5)
            ),
            cost_price=float(
                data.get("cost_price", 0)
            ),
            selling_price=float(
                data.get("selling_price", 0)
            ),
            description=data.get("description"),
            is_active=True,
        )

        db.add(item)

        db.commit()

        db.refresh(item)

        # --------------------------------------------------
        # Opening stock transaction
        # --------------------------------------------------

        opening_quantity = float(
            data.get("quantity", 0)
        )

        if opening_quantity > 0:

            transaction = InventoryTransaction(
                inventory_item_id=item.id,
                transaction_type="IN",
                quantity=opening_quantity,
                reference_type="OPENING",
                notes="Opening stock",
            )

            db.add(transaction)

            db.commit()

        return item

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# GET ITEM
# ==========================================================

def get_inventory_item(item_id):

    db: Session = SessionLocal()

    try:

        return (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

    finally:

        db.close()


# ==========================================================
# UPDATE ITEM
# ==========================================================

def update_inventory_item(item_id, data):

    db: Session = SessionLocal()

    try:

        item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

        if not item:
            return None

        item.name = data["name"]
        item.category = data["category"]
        item.sku = data.get("sku")
        item.unit = data.get("unit", "meter")
        item.minimum_quantity = float(
            data.get("minimum_quantity", 5)
        )
        item.cost_price = float(
            data.get("cost_price", 0)
        )
        item.selling_price = float(
            data.get("selling_price", 0)
        )
        item.description = data.get("description")

        db.commit()

        db.refresh(item)

        return item

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# DELETE ITEM - SOFT DELETE
# ==========================================================

def delete_inventory_item(item_id):

    db: Session = SessionLocal()

    try:

        item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

        if not item:
            return False

        item.is_active = False

        db.commit()

        return True

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# STOCK IN
# ==========================================================

def stock_in(
    item_id,
    quantity,
    reference_type="MANUAL",
    reference_id=None,
    notes=None,
    created_by=None
):

    db: Session = SessionLocal()

    try:

        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError(
                "Stock quantity must be greater than zero."
            )

        item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

        if not item:
            raise ValueError(
                "Inventory item not found."
            )

        item.quantity += quantity

        transaction = InventoryTransaction(
            inventory_item_id=item.id,
            transaction_type="IN",
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
            created_by=created_by,
        )

        db.add(transaction)

        db.commit()

        db.refresh(item)

        return item

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# STOCK OUT
# ==========================================================

def stock_out(
    item_id,
    quantity,
    reference_type="MANUAL",
    reference_id=None,
    notes=None,
    created_by=None
):

    db: Session = SessionLocal()

    try:

        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError(
                "Stock quantity must be greater than zero."
            )

        item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

        if not item:
            raise ValueError(
                "Inventory item not found."
            )

        if quantity > item.quantity:

            raise ValueError(
                f"Insufficient stock. "
                f"Available: {item.quantity} {item.unit}"
            )

        item.quantity -= quantity

        transaction = InventoryTransaction(
            inventory_item_id=item.id,
            transaction_type="OUT",
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
            created_by=created_by,
        )

        db.add(transaction)

        db.commit()

        db.refresh(item)

        return item

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# STOCK ADJUSTMENT
# ==========================================================

def adjust_stock(
    item_id,
    new_quantity,
    notes=None,
    created_by=None
):

    db: Session = SessionLocal()

    try:

        new_quantity = float(new_quantity)

        if new_quantity < 0:

            raise ValueError(
                "Stock quantity cannot be negative."
            )

        item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.id == item_id,
                InventoryItem.is_active == True
            )
            .first()
        )

        if not item:
            raise ValueError(
                "Inventory item not found."
            )

        old_quantity = item.quantity

        difference = new_quantity - old_quantity

        item.quantity = new_quantity

        transaction = InventoryTransaction(
            inventory_item_id=item.id,
            transaction_type="ADJUSTMENT",
            quantity=difference,
            reference_type="MANUAL",
            notes=(
                f"{notes or 'Stock adjustment'} | "
                f"Old: {old_quantity} | "
                f"New: {new_quantity}"
            ),
            created_by=created_by,
        )

        db.add(transaction)

        db.commit()

        db.refresh(item)

        return item

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==========================================================
# TRANSACTIONS
# ==========================================================

def get_inventory_transactions(item_id):

    db: Session = SessionLocal()

    try:

        transactions = (
            db.query(InventoryTransaction)
            .filter(
                InventoryTransaction.inventory_item_id
                == item_id
            )
            .order_by(
                InventoryTransaction.id.desc()
            )
            .all()
        )

        return transactions

    finally:

        db.close()