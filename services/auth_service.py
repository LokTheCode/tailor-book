from werkzeug.security import generate_password_hash, check_password_hash
from database.database import SessionLocal
from models.admin import Admin

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        db = SessionLocal()
        try:
            admin = db.query(Admin).filter(Admin.email == email, Admin.is_active == True).first()
            if admin and cls.verify_password(password, admin.password_hash):
                return admin
            return None
        finally:
            db.close()