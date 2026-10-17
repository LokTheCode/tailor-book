"""App settings stored in the `settings` table (key / value).

Use get() / get_bool() / get_int() / get_list() anywhere in the app.
Every key has a default here, so a missing row is never a problem.
"""

from database.database import SessionLocal
from models.setting import Setting


# key -> (default value, description)
DEFAULTS = {
    # ---------------- General ----------------
    "currency_symbol": ("₹", "Currency symbol shown before amounts"),
    "rows_per_page": ("10", "Default rows per page in lists"),

    # ---------------- Shop details ----------------
    "shop_name": ("Dev Tailors", "Name of the tailoring shop"),
    "shop_owner": ("", "Owner name"),
    "shop_phone": ("", "Contact phone number"),
    "shop_email": ("", "Contact email address"),
    "shop_address": ("", "Shop address"),
    "shop_gstin": ("", "GST number"),
    "shop_logo": ("", "Path to the shop logo (copied into the app folder)"),

    # ---------------- Invoice ----------------
    "invoice_prefix": ("INV-", "Prefix for invoice numbers"),
    "order_prefix": ("ORD-", "Prefix for order numbers"),
    "default_gst_percent": ("18", "Default GST % on new garments in an order"),
    "invoice_paper": ("A4", "A4 or Thermal 80mm"),
    "invoice_show_logo": ("1", "Show logo on invoices"),
    "invoice_terms": ("Goods once sold will not be taken back.", "Terms printed on invoices"),
    "invoice_footer": ("Thank you for your business!", "Footer line on invoices"),

    # ---------------- WhatsApp (AiSensy) ----------------
    "wa_enabled": ("0", "Send WhatsApp messages through AiSensy"),
    "wa_api_key": ("", "AiSensy API key"),
    "wa_api_url": ("https://backend.aisensy.com/campaign/t1/api", "AiSensy campaign API URL"),
    "wa_country_code": ("+91", "Country code added to 10-digit numbers"),
    "wa_campaign_order_created": ("", "AiSensy campaign for 'order received'"),
    "wa_params_order_created": ("{customer_name}, {order_number}, {delivery_date}", "Template values"),
    "wa_campaign_order_ready": ("", "AiSensy campaign for 'order ready'"),
    "wa_params_order_ready": ("{customer_name}, {order_number}, {balance}", "Template values"),
    "wa_campaign_order_delivered": ("", "AiSensy campaign for 'order delivered'"),
    "wa_params_order_delivered": ("{customer_name}, {order_number}", "Template values"),

    # ---------------- Email (SMTP) ----------------
    "email_enabled": ("0", "Send emails"),
    "smtp_host": ("smtp.gmail.com", "SMTP server"),
    "smtp_port": ("587", "SMTP port"),
    "smtp_security": ("STARTTLS", "STARTTLS, SSL or None"),
    "smtp_username": ("", "SMTP login"),
    "smtp_password": ("", "SMTP password / app password"),
    "email_from_name": ("", "Sender name (defaults to shop name)"),
    "email_from_address": ("", "Sender email (defaults to SMTP login)"),
    "email_subject_order_created": ("Order {order_number} received", "Email subject"),
    "email_body_order_created": (
        "Dear {customer_name},\n\nWe have received your order {order_number}. "
        "Expected delivery: {delivery_date}.\n\nThank you,\n{shop_name}",
        "Email body",
    ),
    "email_subject_order_ready": ("Your order {order_number} is ready", "Email subject"),
    "email_body_order_ready": (
        "Dear {customer_name},\n\nYour order {order_number} is ready for pickup. "
        "Balance due: {balance}.\n\nThank you,\n{shop_name}",
        "Email body",
    ),
    "email_subject_order_delivered": ("Order {order_number} delivered", "Email subject"),
    "email_body_order_delivered": (
        "Dear {customer_name},\n\nYour order {order_number} has been delivered. "
        "We hope you love it!\n\nThank you,\n{shop_name}",
        "Email body",
    ),

    # ---------------- Notifications ----------------
    "notify_order_created_wa": ("0", "WhatsApp when an order is created"),
    "notify_order_created_email": ("0", "Email when an order is created"),
    "notify_order_ready_wa": ("1", "WhatsApp when an order is ready"),
    "notify_order_ready_email": ("1", "Email when an order is ready"),
    "notify_order_delivered_wa": ("0", "WhatsApp when an order is delivered"),
    "notify_order_delivered_email": ("0", "Email when an order is delivered"),

    # ---------------- Backup ----------------
    "backup_folder": ("", "Folder for backups (empty = Documents\\TailorBackups)"),
    "backup_daily": ("1", "Make one automatic backup every day"),
    "last_auto_backup_date": ("", "Date of the last daily backup (YYYY-MM-DD)"),
    "backup_on_exit": ("1", "Make a backup when the app closes"),
    "backup_keep": ("10", "How many automatic backups to keep"),
    "last_backup_at": ("", "When the last backup was made"),

    # ---------------- Measurements ----------------
    "measurement_unit": ("inch", "inch or cm"),
    "garment_types": ("Shirt, Pant, Suit, Blazer, Kurta, Sherwani", "Garment types"),

    # ---------------- Appearance ----------------
    "accent_color": ("Blue", "Blue, Purple, Green, Orange or Pink"),
    "font_size": ("Normal", "Small, Normal or Large"),
}


def _defaults(key):
    return DEFAULTS.get(key, ("", ""))


def get(key: str, default: str | None = None) -> str:
    """Return a setting as text (the built-in default if not saved yet)."""
    db = SessionLocal()
    try:
        row = db.query(Setting).filter(Setting.key == key).first()
        if row is not None and row.value is not None:
            return row.value
    finally:
        db.close()
    return _defaults(key)[0] if default is None else default


def get_many(keys) -> dict:
    """Return several settings at once (one database query)."""
    keys = list(keys)
    values = {key: _defaults(key)[0] for key in keys}
    db = SessionLocal()
    try:
        for row in db.query(Setting).filter(Setting.key.in_(keys)):
            if row.value is not None:
                values[row.key] = row.value
    finally:
        db.close()
    return values


def get_all() -> dict:
    return get_many(DEFAULTS.keys())


def get_bool(key: str) -> bool:
    return str(get(key)).strip().lower() in ("1", "true", "yes", "on")


def get_int(key: str, fallback: int = 0) -> int:
    try:
        return int(str(get(key)).strip())
    except ValueError:
        return fallback


def get_float(key: str, fallback: float = 0.0) -> float:
    try:
        return float(str(get(key)).strip())
    except ValueError:
        return fallback


def get_list(key: str) -> list[str]:
    """A comma separated setting as a list, e.g. garment_types."""
    return [item.strip() for item in str(get(key)).split(",") if item.strip()]


def set_many(values: dict) -> None:
    """Save several settings in one transaction."""
    db = SessionLocal()
    try:
        existing = {
            row.key: row
            for row in db.query(Setting).filter(Setting.key.in_(list(values)))
        }
        for key, value in values.items():
            if isinstance(value, bool):
                value = "1" if value else "0"
            value = "" if value is None else str(value)
            row = existing.get(key)
            if row is None:
                db.add(Setting(key=key, value=value, description=_defaults(key)[1]))
            else:
                row.value = value
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def set(key: str, value) -> None:  # noqa: A001 - mirrors get()
    set_many({key: value})


def currency(amount) -> str:
    """Format an amount with the configured currency symbol."""
    try:
        return f"{get('currency_symbol')}{float(amount or 0):,.2f}"
    except (TypeError, ValueError):
        return f"{get('currency_symbol')}0.00"
