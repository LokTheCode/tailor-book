from database.database import SessionLocal
from models import Admin, Setting, Customer, CustomerMeasurement, Order
from services.user_service import UserService

def seed_initial_data():
    # 1. The super admin account must always exist
    UserService.ensure_super_admin()

    db = SessionLocal()
    try:
        # 2. Seed Default Settings if empty
        if db.query(Setting).count() == 0:
            default_settings = [
                Setting(key="shop_name", value="Dev Tailors", description="Name of the tailoring shop"),
                Setting(key="shop_phone", value="9876543210", description="Contact phone number"),
                Setting(key="shop_email", value="info@devtailor.com", description="Contact email address"),
                Setting(key="shop_address", value="Delhi", description="Physical shop address"),
                Setting(key="currency", value="INR", description="Default application currency"),
                Setting(key="invoice_prefix", value="INV-", description="Prefix for invoice generation"),
                Setting(key="order_prefix", value="ORD-", description="Prefix for order tracking")
            ]
            db.add_all(default_settings)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()