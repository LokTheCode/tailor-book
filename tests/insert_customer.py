from config.database import SessionLocal
from models.customer import Customer

db = SessionLocal()

customer = Customer(
    name="Lokesh",
    mobile="9876543210",
    whatsapp="9876543210",
    email="lokesh@gmail.com",
    address="Delhi"
)

db.add(customer)
db.commit()

print("Customer inserted successfully.")

db.close()