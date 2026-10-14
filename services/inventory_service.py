from database.database import SessionLocal
from models.inventory import InventoryItem
from models.inventory_transaction import InventoryTransaction

class InventoryService:

    @staticmethod
    def add_item(name: str, category: str, unit: str = "meter", quantity: float = 0.0, 
                 minimum_quantity: float = 5.0, cost_price: float = 0.0, 
                 selling_price: float = 0.0, sku: str = None, description: str = None) -> InventoryItem:
        """Creates a new inventory item and records initial stock if quantity > 0."""
        db = SessionLocal()
        try:
            item = InventoryItem(
                name=name, category=category, unit=unit, quantity=quantity,
                minimum_quantity=minimum_quantity, cost_price=cost_price,
                selling_price=selling_price, sku=sku, description=description
            )
            db.add(item)
            db.flush()

            if quantity > 0:
                txn = InventoryTransaction(
                    inventory_item_id=item.id,
                    transaction_type="IN",
                    quantity=quantity,
                    reference_type="INITIAL",
                    notes="Opening Stock"
                )
                db.add(txn)

            db.commit()
            db.refresh(item)
            return item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def record_stock_movement(item_id: int, transaction_type: str, quantity: float, 
                              reference_type: str = "MANUAL", reference_id: int = None, 
                              notes: str = None, created_by: int = None) -> InventoryItem:
        """
        Updates stock quantity and records transaction history.
        transaction_type: 'IN' (increases stock), 'OUT' (decreases stock)
        """
        db = SessionLocal()
        try:
            item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
            if not item:
                raise ValueError("Inventory item not found.")

            if transaction_type.upper() == "IN":
                item.quantity += quantity
            elif transaction_type.upper() == "OUT":
                if item.quantity < quantity:
                    raise ValueError(f"Insufficient stock for {item.name}. Available: {item.quantity}")
                item.quantity -= quantity
            else:
                item.quantity = quantity # Force adjustment

            txn = InventoryTransaction(
                inventory_item_id=item.id,
                transaction_type=transaction_type.upper(),
                quantity=quantity,
                reference_type=reference_type,
                reference_id=reference_id,
                notes=notes,
                created_by=created_by
            )
            db.add(txn)
            db.commit()
            db.refresh(item)
            return item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def get_all_items_ui():
        """Returns inventory items formatted directly for UI tables."""
        db = SessionLocal()
        try:
            items = db.query(InventoryItem).filter(InventoryItem.is_active == True).all()
            return [
                {
                    "id": i.id,
                    "name": i.name,
                    "category": i.category,
                    "stock": f"{i.quantity} {i.unit}",
                    "cost": i.cost_price,
                    "price": i.selling_price,
                    "status": "Low Stock" if i.quantity <= i.minimum_quantity else "In Stock"
                }
                for i in items
            ]
        finally:
            db.close()