from database.database import Base
from database.database import engine

# Import all models
from models.customer import Customer

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")