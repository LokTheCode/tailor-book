"""WhatsApp (AiSensy) and email (SMTP) messages to customers.

WhatsApp
--------
AiSensy sends WhatsApp *template* messages through "API campaigns":

1. In AiSensy, create a template (e.g. "Hi {{1}}, your order {{2}} is
   ready") and get it approved by WhatsApp.
2. Create an API campaign using that template and set it Live.
3. In this app, Settings > WhatsApp: paste your AiSensy API key and the
   campaign name, and list the values for {{1}}, {{2}}, ... in order,
   e.g. "{customer_name}, {order_number}".

Email
-----
Any SMTP account works. For Gmail, turn on 2-step verification and use
an App Password (not your normal password).

Placeholders available in messages
----------------------------------
{customer_name} {mobile} {email} {order_number} {order_date}
{delivery_date} {status} {total} {advance} {balance}
{shop_name} {shop_phone} {shop_address}
"""

import json
import smtplib
import ssl
import threading
import urllib.error
import urllib.request
from email.message import EmailMessage
from email.utils import formataddr

from database.database import SessionLocal
from models.customer import Customer
from models.message_log import MessageLog
from models.order import Order
from config import APP_NAME
from services import settings_service

EVENTS = {
    "order_created": "Order received",
    "order_ready": "Order ready",
    "order_delivered": "Order delivered",
}

PLACEHOLDERS = [
    "customer_name", "mobile", "email",
    "order_number", "order_date", "delivery_date", "status",
    "total", "advance", "balance",
    "shop_name", "shop_phone", "shop_address",
]

TIMEOUT_SECONDS = 20


class _Blank(dict):
    """Unknown placeholders become empty text instead of an error."""

    def __missing__(self, key):
        return ""


def render(template: str, context: dict) -> str:
    try:
        return (template or "").format_map(_Blank(context))
    except (ValueError, IndexError, KeyError, AttributeError):
        # A stray { or } in the text: replace only the known placeholders
        text = template or ""
        for key, value in context.items():
            text = text.replace("{" + key + "}", str(value))
        return text


def render_params(param_template: str, context: dict) -> list[str]:
    """'{customer_name}, {order_number}' -> ['Amit', 'ORD-0004'].

    Split first, then fill in, so commas inside values (like 1,200.00)
    don't create extra parameters.
    """
    parts = [p.strip() for p in (param_template or "").split(",")]
    return [render(p, context) for p in parts if p]


# ==========================================================
# CONTEXT (values for placeholders)
# ==========================================================

def shop_context() -> dict:
    values = settings_service.get_many(["shop_name", "shop_phone", "shop_address"])
    return values


def customer_context(customer: Customer) -> dict:
    context = shop_context()
    context.update({
        "customer_name": customer.name or "",
        "mobile": customer.mobile or "",
        "email": customer.email or "",
    })
    return context


def order_context(order_id: int):
    """Return (customer, context) for an order, or (None, None)."""
    db = SessionLocal()
    try:
        order = db.get(Order, order_id)
        if not order:
            return None, None
        customer = db.get(Customer, order.customer_id)
        if not customer:
            return None, None

        context = customer_context(customer)
        context.update({
            "order_number": order.order_number or "",
            "order_date": order.order_date or "",
            "delivery_date": order.delivery_date or "",
            "status": (order.status or "").title(),
            "total": settings_service.currency(order.total_amount),
            "advance": settings_service.currency(order.advance_amount),
            "balance": settings_service.currency(order.remaining_amount),
        })
        db.expunge(customer)
        return customer, context
    finally:
        db.close()


# ==========================================================
# LOW-LEVEL SENDERS
# ==========================================================

def normalize_phone(mobile: str) -> str:
    """Add the country code to a 10-digit number: 9876543210 -> +919876543210."""
    digits = "".join(ch for ch in (mobile or "") if ch.isdigit())
    code = settings_service.get("wa_country_code").strip() or "+91"
    if not code.startswith("+"):
        code = "+" + code
    if len(digits) == 10:
        return f"{code}{digits}"
    return f"+{digits}" if digits else ""


def send_whatsapp(phone: str, user_name: str, campaign: str, params: list[str]):
    """Send one AiSensy API campaign message. Returns (ok, detail)."""

    api_key = settings_service.get("wa_api_key").strip()
    url = settings_service.get("wa_api_url").strip()

    if not api_key:
        return False, "AiSensy API key is not set (Settings > WhatsApp)."
    if not campaign:
        return False, "No AiSensy campaign name set for this message."
    if not phone:
        return False, "Customer has no mobile number."

    payload = {
        "apiKey": api_key,
        "campaignName": campaign,
        "destination": phone,
        "userName": user_name or "Customer",
        "templateParams": params,
        "source": APP_NAME,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", "replace")[:500]
            return 200 <= response.status < 300, body or f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")[:500]
        return False, f"AiSensy error {error.code}: {body}"
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return False, f"Couldn't reach AiSensy: {getattr(error, 'reason', error)}"


def send_email(to_address: str, subject: str, body: str):
    """Send one plain-text email over SMTP. Returns (ok, detail)."""

    s = settings_service.get_many([
        "smtp_host", "smtp_port", "smtp_security", "smtp_username", "smtp_password",
        "email_from_name", "email_from_address", "shop_name",
    ])

    if not s["smtp_host"] or not s["smtp_username"]:
        return False, "SMTP server or login is not set (Settings > Email)."
    if not to_address:
        return False, "Customer has no email address."

    sender = s["email_from_address"] or s["smtp_username"]
    message = EmailMessage()
    message["From"] = formataddr((s["email_from_name"] or s["shop_name"], sender))
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    try:
        port = int(s["smtp_port"] or 587)
        security = (s["smtp_security"] or "STARTTLS").upper()
        context = ssl.create_default_context()

        if security == "SSL":
            server = smtplib.SMTP_SSL(s["smtp_host"], port, timeout=TIMEOUT_SECONDS, context=context)
        else:
            server = smtplib.SMTP(s["smtp_host"], port, timeout=TIMEOUT_SECONDS)

        with server:
            if security == "STARTTLS":
                server.starttls(context=context)
            if s["smtp_password"]:
                server.login(s["smtp_username"], s["smtp_password"])
            server.send_message(message)
        return True, "Sent"
    except smtplib.SMTPAuthenticationError:
        return False, "Email login failed. For Gmail, use an App Password."
    except (smtplib.SMTPException, OSError, ValueError) as error:
        return False, f"Email failed: {error}"


# ==========================================================
# LOGGING
# ==========================================================

def _log(channel, event, recipient, ok, detail, customer_id=None, order_id=None):
    db = SessionLocal()
    try:
        db.add(MessageLog(
            customer_id=customer_id,
            order_id=order_id,
            channel=channel,
            event=event,
            recipient=recipient or "-",
            status="sent" if ok else "failed",
            detail=(detail or "")[:1000],
        ))
        db.commit()
    except Exception as error:
        db.rollback()
        print(f"Could not log message: {error}")
    finally:
        db.close()


def recent_logs(limit: int = 200) -> list[dict]:
    db = SessionLocal()
    try:
        rows = (
            db.query(MessageLog, Customer.name)
            .outerjoin(Customer, Customer.id == MessageLog.customer_id)
            .order_by(MessageLog.id.desc())
            .limit(limit)
            .all()
        )
        from data.measurement_crud import local_time
        return [
            {
                "time": local_time(log.created_at),
                "customer": name or "-",
                "channel": log.channel,
                "event": EVENTS.get(log.event, log.event.title()),
                "recipient": log.recipient,
                "status": log.status,
                "detail": log.detail or "",
            }
            for log, name in rows
        ]
    finally:
        db.close()


# ==========================================================
# ORDER NOTIFICATIONS
# ==========================================================

def notify_order_event(order_id: int, event: str) -> list[tuple]:
    """Send the WhatsApp / email for an order event if turned on.

    Returns a list of (channel, ok, detail) for what was attempted.
    """
    if event not in EVENTS:
        return []

    s = settings_service
    want_wa = s.get_bool("wa_enabled") and s.get_bool(f"notify_{event}_wa")
    want_email = s.get_bool("email_enabled") and s.get_bool(f"notify_{event}_email")
    if not (want_wa or want_email):
        return []

    customer, context = order_context(order_id)
    if customer is None:
        return []

    results = []

    if want_wa:
        phone = normalize_phone(customer.mobile)
        ok, detail = send_whatsapp(
            phone,
            customer.name,
            s.get(f"wa_campaign_{event}").strip(),
            render_params(s.get(f"wa_params_{event}"), context),
        )
        _log("whatsapp", event, phone, ok, detail, customer.id, order_id)
        results.append(("whatsapp", ok, detail))

    if want_email and customer.email:
        ok, detail = send_email(
            customer.email,
            render(s.get(f"email_subject_{event}"), context),
            render(s.get(f"email_body_{event}"), context),
        )
        _log("email", event, customer.email, ok, detail, customer.id, order_id)
        results.append(("email", ok, detail))

    return results


def notify_order_event_async(order_id: int, event: str) -> None:
    """Same as notify_order_event, without making the app wait."""
    threading.Thread(
        target=notify_order_event, args=(order_id, event), daemon=True
    ).start()


# ==========================================================
# MARKETING
# ==========================================================

AUDIENCES = [
    "All active customers",
    "Customer type",
    "Ordered in the last N days",
    "No order in the last N days",
]


def audience(kind: str, customer_type: str = "", days: int = 30, channel: str = "whatsapp") -> list[dict]:
    """Customers for a marketing message.

    Only customers with a mobile (WhatsApp) or email (email) are returned.
    """
    from datetime import date, timedelta

    from sqlalchemy import func

    db = SessionLocal()
    try:
        query = db.query(Customer).filter(Customer.is_active == True)  # noqa: E712

        if kind == "Customer type" and customer_type:
            query = query.filter(func.lower(Customer.customer_type) == customer_type.lower())

        if kind in ("Ordered in the last N days", "No order in the last N days"):
            since = (date.today() - timedelta(days=max(1, int(days)))).isoformat()
            recent = db.query(Order.customer_id).filter(Order.order_date >= since)
            if kind.startswith("Ordered"):
                query = query.filter(Customer.id.in_(recent))
            else:
                query = query.filter(~Customer.id.in_(recent))

        if channel == "email":
            query = query.filter(Customer.email.isnot(None), Customer.email != "")
        else:
            query = query.filter(Customer.mobile.isnot(None), Customer.mobile != "")

        return [
            {"id": c.id, "name": c.name, "mobile": c.mobile, "email": c.email or ""}
            for c in query.order_by(Customer.name).all()
        ]
    finally:
        db.close()


def send_marketing_one(customer: dict, channel: str, campaign: str = "", params: str = "",
                       subject: str = "", body: str = ""):
    """Send one marketing message (used by the Marketing page's worker)."""
    db = SessionLocal()
    try:
        row = db.get(Customer, customer["id"])
        context = customer_context(row) if row else shop_context()
    finally:
        db.close()

    if channel == "email":
        ok, detail = send_email(customer["email"], render(subject, context), render(body, context))
        recipient = customer["email"]
    else:
        recipient = normalize_phone(customer["mobile"])
        ok, detail = send_whatsapp(recipient, customer["name"], campaign.strip(), render_params(params, context))

    _log(channel, "marketing", recipient, ok, detail, customer["id"])
    return ok, detail


# ==========================================================
# TESTS (Settings buttons)
# ==========================================================

def sample_context() -> dict:
    context = shop_context()
    context.update({
        "customer_name": "Test Customer", "mobile": "9876543210", "email": "",
        "order_number": f"{settings_service.get('order_prefix')}0001",
        "order_date": "01 Jan 2026", "delivery_date": "05 Jan 2026", "status": "Ready",
        "total": settings_service.currency(1500), "advance": settings_service.currency(500),
        "balance": settings_service.currency(1000),
    })
    return context


def test_whatsapp(mobile: str, event: str = "order_ready"):
    phone = normalize_phone(mobile)
    ok, detail = send_whatsapp(
        phone, "Test Customer",
        settings_service.get(f"wa_campaign_{event}").strip(),
        render_params(settings_service.get(f"wa_params_{event}"), sample_context()),
    )
    _log("whatsapp", "test", phone, ok, detail)
    return ok, detail


def test_email(to_address: str):
    context = sample_context()
    ok, detail = send_email(
        to_address,
        render(settings_service.get("email_subject_order_ready"), context),
        render(settings_service.get("email_body_order_ready"), context),
    )
    _log("email", "test", to_address, ok, detail)
    return ok, detail
