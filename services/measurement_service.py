from database.database import SessionLocal
from models.measurement import CustomerMeasurement

class MeasurementService:
    @staticmethod
    def add_measurement(customer_id: int, measurement_name: str, upper: dict, lower: dict, extra: dict, notes: str = None):
        db = SessionLocal()
        try:
            measurement = CustomerMeasurement(
                customer_id=customer_id,
                measurement_name=measurement_name,
                upper_measurements=upper,
                lower_measurements=lower,
                extra_measurements=extra,
                notes=notes
            )
            db.add(measurement)
            db.commit()
            db.refresh(measurement)
            return measurement
        finally:
            db.close()

    @staticmethod
    def get_customer_measurements(customer_id: int):
        db = SessionLocal()
        try:
            return db.query(CustomerMeasurement)\
                     .filter(CustomerMeasurement.customer_id == customer_id)\
                     .order_by(CustomerMeasurement.created_at.desc())\
                     .all()
        finally:
            db.close()