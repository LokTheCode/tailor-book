from sqlalchemy import or_

from database.database import SessionLocal

from models.inventory import InventoryItem


# ==========================================================
# INVENTORY LIST
# ==========================================================

def get_inventory_list(
    search="",
    category="All Categories",
    stock_status="All Stock",
    page=1,
    page_size=10
):

    db = SessionLocal()

    try:

        query = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.is_active == True
            )
        )

        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        if search:

            search_text = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    InventoryItem.name.ilike(
                        search_text
                    ),
                    InventoryItem.sku.ilike(
                        search_text
                    ),
                    InventoryItem.category.ilike(
                        search_text
                    ),
                )
            )

        # --------------------------------------------------
        # CATEGORY
        # --------------------------------------------------

        if (
            category
            and category != "All Categories"
        ):

            query = query.filter(
                InventoryItem.category == category
            )

        # --------------------------------------------------
        # STOCK FILTER
        # --------------------------------------------------

        if stock_status == "Low Stock":

            query = query.filter(
                InventoryItem.quantity
                <= InventoryItem.minimum_quantity
            )

        elif stock_status == "Out of Stock":

            query = query.filter(
                InventoryItem.quantity <= 0
            )

        elif stock_status == "In Stock":

            query = query.filter(
                InventoryItem.quantity
                > InventoryItem.minimum_quantity
            )

        # --------------------------------------------------
        # COUNT
        # --------------------------------------------------

        total_records = query.count()

        total_pages = (
            max(
                1,
                (total_records + page_size - 1)
                // page_size
            )
        )

        page = max(
            1,
            min(page, total_pages)
        )

        offset = (
            (page - 1) * page_size
        )

        items = (
            query
            .order_by(
                InventoryItem.name.asc()
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        result = []

        for item in items:

            if item.quantity <= 0:

                stock_status_text = "Out of Stock"

            elif (
                item.quantity
                <= item.minimum_quantity
            ):

                stock_status_text = "Low Stock"

            else:

                stock_status_text = "In Stock"

            result.append({

                "id": item.id,

                "name": item.name,

                "category": item.category,

                "sku": item.sku or "—",

                "unit": item.unit,

                "quantity": item.quantity,

                "minimum_quantity":
                    item.minimum_quantity,

                "cost_price":
                    item.cost_price or 0,

                "selling_price":
                    item.selling_price or 0,

                "description":
                    item.description or "",

                "stock_status":
                    stock_status_text,

            })

        return {
            "items": result,
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
        }

    finally:

        db.close()


# ==========================================================
# CATEGORIES
# ==========================================================

def get_inventory_categories():

    db = SessionLocal()

    try:

        rows = (
            db.query(
                InventoryItem.category
            )
            .filter(
                InventoryItem.is_active == True
            )
            .distinct()
            .order_by(
                InventoryItem.category.asc()
            )
            .all()
        )

        return [
            row[0]
            for row in rows
            if row[0]
        ]

    finally:

        db.close()


# ==========================================================
# STATS
# ==========================================================

def get_inventory_stats():

    db = SessionLocal()

    try:

        items = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.is_active == True
            )
            .all()
        )

        total_items = len(items)

        low_stock = sum(
            1
            for item in items
            if (
                item.quantity > 0
                and item.quantity
                <= item.minimum_quantity
            )
        )

        out_of_stock = sum(
            1
            for item in items
            if item.quantity <= 0
        )

        inventory_value = sum(
            (
                item.quantity
                * (item.cost_price or 0)
            )
            for item in items
        )

        return {

            "total_items":
                total_items,

            "low_stock":
                low_stock,

            "out_of_stock":
                out_of_stock,

            "inventory_value":
                inventory_value,
        }

    finally:

        db.close()