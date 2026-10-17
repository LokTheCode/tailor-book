"""Users, roles, page access and passwords.

Roles
-----
super_admin  The owner account. Always exists, can open every page and
             manage everyone. Hidden from the Users list.
admin        Opens the pages ticked in its access list. With "Users"
             access it can add and edit sub-admins (not other admins).
sub_admin    Opens the pages ticked in its access list. Can never
             manage users.

Every user can change their own password from the top bar.
"""

import re

from sqlalchemy import func

from database.database import SessionLocal
from models.admin import Admin
from services.auth_service import AuthService


# ==========================================================
# SUPER ADMIN
# ==========================================================
# Created automatically on every start if it is missing (see
# ensure_super_admin). Only the password *hash* is stored here.
# Default password: the one you set up for LK141997@gmail.com.
# Changing it from the app updates the database; it is not reset
# on the next start.

SUPER_ADMIN_EMAIL = "lk141997@gmail.com"
SUPER_ADMIN_NAME = "Super Admin"
SUPER_ADMIN_PASSWORD_HASH = (
    "pbkdf2:sha256:600000$zX1gdljIHi2tVLZI$"
    "c3af5913d7e18e242429dea3e5dd1b7caab7287bde64f939a7c918f718a18438"
)


# ==========================================================
# ROLES & PAGES
# ==========================================================

SUPER_ADMIN = "super_admin"
ADMIN = "admin"
SUB_ADMIN = "sub_admin"

ROLE_LABELS = {
    SUPER_ADMIN: "Super Admin",
    ADMIN: "Admin",
    SUB_ADMIN: "Sub Admin",
}

# Page key -> label, in sidebar order
PAGES = {
    "dashboard": "Dashboard",
    "customers": "Customers",
    "measurements": "Measurements",
    "orders": "Orders",
    "inventory": "Inventory",
    "reports": "Reports",
    "settings": "Settings",
    "users": "Users",
}

# Ticked by default when a new user is created
DEFAULT_ACCESS = {
    ADMIN: ["dashboard", "customers", "measurements", "orders", "inventory", "reports", "settings"],
    SUB_ADMIN: ["dashboard", "customers", "measurements", "orders"],
}

MIN_PASSWORD_LENGTH = 8
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserError(Exception):
    """Raised with a message that can be shown to the user as-is."""


# ==========================================================
# HELPERS
# ==========================================================

def _parse_permissions(text):
    return [p for p in (text or "").split(",") if p in PAGES]


def _to_dict(admin):
    return {
        "id": admin.id,
        "name": admin.name,
        "email": admin.email,
        "phone": admin.phone or "",
        "role": admin.role,
        "role_label": ROLE_LABELS.get(admin.role, admin.role),
        "permissions": list(PAGES) if admin.role == SUPER_ADMIN else _parse_permissions(admin.permissions),
        "is_active": bool(admin.is_active),
    }


def _clean_permissions(role, permissions):
    allowed = [p for p in PAGES if p in set(permissions or [])]
    if role == SUB_ADMIN and "users" in allowed:
        allowed.remove("users")  # sub-admins can never manage users
    return allowed


def _check_access(permissions):
    if not permissions:
        raise UserError("Give access to at least one page.")


def _check_password(password):
    if len(password or "") < MIN_PASSWORD_LENGTH:
        raise UserError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")


def _check_fields(name, email):
    if not (name or "").strip():
        raise UserError("Name is required.")
    if not EMAIL_PATTERN.match((email or "").strip()):
        raise UserError("Enter a valid email address.")


# ==========================================================
# ACCESS CHECKS (use these from the UI)
# ==========================================================

def can_open(user, page):
    """True if this logged-in user may open the given page key."""
    if not user:
        return False
    if user.get("role") == SUPER_ADMIN:
        return True
    if page == "users" and user.get("role") != ADMIN:
        return False
    return page in user.get("permissions", [])


def manageable_roles(user):
    """Roles this user may create or edit on the Users page."""
    if user.get("role") == SUPER_ADMIN:
        return [ADMIN, SUB_ADMIN]
    if user.get("role") == ADMIN and can_open(user, "users"):
        return [SUB_ADMIN]
    return []


def _ensure_can_manage(actor, target_role):
    if target_role not in manageable_roles(actor):
        raise UserError("You don't have permission to manage this user.")


# ==========================================================
# SERVICE
# ==========================================================

class UserService:

    # ------------------------------------------------------
    # Startup
    # ------------------------------------------------------

    @staticmethod
    def ensure_super_admin():
        """Make sure the super admin account exists and can log in.

        Creates it with the default password if missing. If it exists,
        it is kept active with the super_admin role, but its password is
        left alone so a changed password is not undone.
        """
        db = SessionLocal()
        try:
            admin = db.query(Admin).filter(func.lower(Admin.email) == SUPER_ADMIN_EMAIL.lower()).first()

            if admin is None:
                db.add(Admin(
                    name=SUPER_ADMIN_NAME,
                    email=SUPER_ADMIN_EMAIL,
                    password_hash=SUPER_ADMIN_PASSWORD_HASH,
                    role=SUPER_ADMIN,
                    permissions=",".join(PAGES),
                    is_active=True,
                ))
            else:
                admin.role = SUPER_ADMIN
                admin.is_active = True

            # Users from before page access existed have no access list.
            # Give them their role's defaults so they can still work.
            # (The Users page never saves an empty list.)
            for legacy in db.query(Admin).filter(
                Admin.role.in_([ADMIN, SUB_ADMIN]),
                (Admin.permissions == "") | (Admin.permissions.is_(None)),
            ):
                legacy.permissions = ",".join(DEFAULT_ACCESS[legacy.role])

            db.commit()
        finally:
            db.close()

    # ------------------------------------------------------
    # Login
    # ------------------------------------------------------

    @staticmethod
    def authenticate(email, password):
        """Return the user as a dict, or None if the login is wrong."""
        db = SessionLocal()
        try:
            admin = (
                db.query(Admin)
                .filter(func.lower(Admin.email) == (email or "").strip().lower(), Admin.is_active == True)  # noqa: E712
                .first()
            )
            if admin and AuthService.verify_password(password, admin.password_hash):
                return _to_dict(admin)
            return None
        finally:
            db.close()

    @staticmethod
    def get(user_id):
        db = SessionLocal()
        try:
            admin = db.get(Admin, user_id)
            return _to_dict(admin) if admin else None
        finally:
            db.close()

    # ------------------------------------------------------
    # List
    # ------------------------------------------------------

    @staticmethod
    def list_users(actor):
        """Users the actor can see. The super admin is never listed."""
        roles = manageable_roles(actor)
        if not roles:
            return []

        db = SessionLocal()
        try:
            rows = (
                db.query(Admin)
                .filter(Admin.role.in_(roles))
                .order_by(Admin.role, Admin.name)
                .all()
            )
            return [_to_dict(r) for r in rows]
        finally:
            db.close()

    # ------------------------------------------------------
    # Create / update
    # ------------------------------------------------------

    @staticmethod
    def create_user(actor, name, email, phone, role, permissions, password, is_active=True):
        _ensure_can_manage(actor, role)
        _check_fields(name, email)
        _check_password(password)
        _check_access(_clean_permissions(role, permissions))

        email = email.strip().lower()

        db = SessionLocal()
        try:
            if db.query(Admin).filter(func.lower(Admin.email) == email.lower()).first():
                raise UserError("A user with this email already exists.")

            admin = Admin(
                name=name.strip(),
                email=email,
                phone=(phone or "").strip() or None,
                password_hash=AuthService.hash_password(password),
                role=role,
                permissions=",".join(_clean_permissions(role, permissions)),
                is_active=bool(is_active),
            )
            db.add(admin)
            db.commit()
            return _to_dict(admin)
        finally:
            db.close()

    @staticmethod
    def update_user(actor, user_id, name, email, phone, role, permissions, new_password="", is_active=True):
        """Update a user. Leave new_password empty to keep the current one."""
        _check_fields(name, email)
        _check_access(_clean_permissions(role, permissions))
        if new_password:
            _check_password(new_password)

        email = email.strip().lower()

        db = SessionLocal()
        try:
            admin = db.get(Admin, user_id)
            if admin is None:
                raise UserError("User not found.")

            # Must be allowed to manage both the current and the new role
            _ensure_can_manage(actor, admin.role)
            _ensure_can_manage(actor, role)

            if admin.id == actor.get("id") and not is_active:
                raise UserError("You can't deactivate your own account.")

            clash = db.query(Admin).filter(func.lower(Admin.email) == email.lower(), Admin.id != admin.id).first()
            if clash:
                raise UserError("A user with this email already exists.")

            admin.name = name.strip()
            admin.email = email
            admin.phone = (phone or "").strip() or None
            admin.role = role
            admin.permissions = ",".join(_clean_permissions(role, permissions))
            admin.is_active = bool(is_active)
            if new_password:
                admin.password_hash = AuthService.hash_password(new_password)

            db.commit()
            return _to_dict(admin)
        finally:
            db.close()

    @staticmethod
    def set_active(actor, user_id, active):
        db = SessionLocal()
        try:
            admin = db.get(Admin, user_id)
            if admin is None:
                raise UserError("User not found.")
            _ensure_can_manage(actor, admin.role)
            if admin.id == actor.get("id") and not active:
                raise UserError("You can't deactivate your own account.")
            admin.is_active = bool(active)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def delete_user(actor, user_id):
        db = SessionLocal()
        try:
            admin = db.get(Admin, user_id)
            if admin is None:
                raise UserError("User not found.")
            _ensure_can_manage(actor, admin.role)
            if admin.id == actor.get("id"):
                raise UserError("You can't delete your own account.")
            db.delete(admin)
            db.commit()
        finally:
            db.close()

    # ------------------------------------------------------
    # Passwords
    # ------------------------------------------------------

    @staticmethod
    def change_own_password(user_id, current_password, new_password, confirm_password):
        """Change the logged-in user's own password."""
        if new_password != confirm_password:
            raise UserError("New password and confirmation do not match.")
        _check_password(new_password)

        db = SessionLocal()
        try:
            admin = db.get(Admin, user_id)
            if admin is None:
                raise UserError("User not found.")
            if not AuthService.verify_password(current_password, admin.password_hash):
                raise UserError("Current password is incorrect.")
            if AuthService.verify_password(new_password, admin.password_hash):
                raise UserError("New password must be different from the current one.")

            admin.password_hash = AuthService.hash_password(new_password)
            db.commit()
        finally:
            db.close()
