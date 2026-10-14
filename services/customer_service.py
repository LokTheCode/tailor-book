from database.database import SessionLocal
from models.customer import Customer

class CustomerService:
    @staticmethod
    def create_customer(data: dict) -> Customer:
        db = SessionLocal()
        try:
            customer = Customer(**data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return customer
        finally:
            db.close()

    @staticmethod
    def get_all_customers(search_query: str = None):
        db = SessionLocal()
        try:
            query = db.query(Customer).filter(Customer.is_active == True)
            if search_query:
                query = query.filter(
                    (Customer.name.ilike(f"%{search_query}%")) |
                    (Customer.mobile.ilike(f"%{search_query}%"))
                )
            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_customer_by_id(customer_id: int) -> Customer:
        db = SessionLocal()
        try:
            return db.query(Customer).filter(Customer.id == customer_id).first()
        finally:
            db.close()

    # Add these methods inside CustomerService:

    @staticmethod
    def get_customers_for_table():
        """Returns list of dictionary rows directly injectable into QTableWidget."""
        db = SessionLocal()
        try:
            customers = db.query(Customer).filter(Customer.is_active == True).order_by(Customer.id.desc()).all()
            return [
                {
                    "id": c.id,
                    "name": c.name,
                    "mobile": c.mobile,
                    "gender": c.gender or "-",
                    "type": c.customer_type,
                    "reference": c.reference or "-"
                }
                for c in customers
            ]
        finally:
            db.close()

    @staticmethod
    def get_customers_for_dropdown():
        """Returns list formatted for QComboBox: [{'id': 1, 'display': 'Rahul Sharma (9876543210)'}]"""
        db = SessionLocal()
        try:
            customers = db.query(Customer).filter(Customer.is_active == True).all()
            return [{"id": c.id, "display": f"{c.name} ({c.mobile})"} for c in customers]
        finally:
            db.close()