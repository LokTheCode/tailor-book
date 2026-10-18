"""
Tailor Book licensing.

How it works
------------
1. The customer buys a key (TB-XXXXX-XXXXX-XXXXX-XXXXX) on the website.
2. They type it into the activation screen. The app sends the key and this
   computer's ID to LICENSE_SERVER_URL/api/activate.php.
3. The server ties the key to this computer and returns a token signed with
   its private Ed25519 key. The token is saved in the data folder
   (license.json) and checked offline at every start with LICENSE_PUBLIC_KEY.
   A token copied to another computer does not work there.
4. About once a week the app asks the server whether the license is still
   active on this computer (it may have been moved to a new PC or revoked).
   If the server can't be reached the app keeps working.

Licensing is switched on when LICENSE_PUBLIC_KEY is set in config.py, and
always in the built .exe. Running from source without a key skips it.
"""

import hashlib
import json
import os
import platform
import sys
import urllib.error
import urllib.request
from base64 import urlsafe_b64decode
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from config import APP_VERSION
import config

CHECK_EVERY = timedelta(days=7)
TIMEOUT = 15


class LicenseError(Exception):
    """A problem to show the user, in plain words."""

    def __init__(self, message, code=""):
        super().__init__(message)
        self.code = code


@dataclass
class License:
    key: str
    name: str
    shop: str
    email: str
    issued: str

    @property
    def masked_key(self):
        parts = self.key.split("-")
        if len(parts) < 3:
            return self.key
        return "-".join([parts[0]] + ["•••••"] * (len(parts) - 2) + [parts[-1]])


# ==========================================================
# SETTINGS
# ==========================================================

def server_url():
    return (getattr(config, "LICENSE_SERVER_URL", "") or "").rstrip("/")


def public_key_hex():
    return (getattr(config, "LICENSE_PUBLIC_KEY", "") or "").strip()


def required():
    """True when the app must be activated before use."""
    return bool(public_key_hex()) or bool(getattr(sys, "frozen", False))


def configured():
    return bool(server_url()) and len(public_key_hex()) == 64


def buy_url():
    return f"{server_url()}/buy.php" if server_url() else (config.APP_WEBSITE or "")


def _license_file():
    from database.database import DB_PATH
    return Path(DB_PATH).parent / "license.json"


# ==========================================================
# THIS COMPUTER
# ==========================================================

def _raw_machine_id():
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            ) as key:
                return winreg.QueryValueEx(key, "MachineGuid")[0]
        except OSError:
            pass
    for path in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
        try:
            value = Path(path).read_text().strip()
            if value:
                return value
        except OSError:
            pass
    import uuid
    return f"{uuid.getnode():012x}-{platform.node()}"


def machine_id():
    """A one-way code for this Windows installation (64 hex characters)."""
    return hashlib.sha256(f"tailorbook:{_raw_machine_id()}".encode()).hexdigest()


def machine_name():
    return (os.environ.get("COMPUTERNAME") or platform.node() or "PC")[:80]


# ==========================================================
# ED25519 SIGNATURE CHECK (RFC 8032, pure Python)
# ==========================================================

_P = 2 ** 255 - 19
_Q = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_SQRT_M1 = pow(2, (_P - 1) // 4, _P)


def _add(a, b):
    A = (a[1] - a[0]) * (b[1] - b[0]) % _P
    B = (a[1] + a[0]) * (b[1] + b[0]) % _P
    C = 2 * a[3] * b[3] * _D % _P
    D = 2 * a[2] * b[2] % _P
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _P, G * H % _P, F * G % _P, E * H % _P)


def _mul(s, point):
    result = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            result = _add(result, point)
        point = _add(point, point)
        s >>= 1
    return result


def _equal(a, b):
    return (a[0] * b[2] - b[0] * a[2]) % _P == 0 and (a[1] * b[2] - b[1] * a[2]) % _P == 0


def _recover_x(y, sign):
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P:
        x = x * _SQRT_M1 % _P
    if (x * x - x2) % _P:
        return None
    if (x & 1) != sign:
        x = _P - x
    return x


def _decompress(data):
    if len(data) != 32:
        return None
    y = int.from_bytes(data, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _P)


_GY = 4 * pow(5, _P - 2, _P) % _P
_GX = _recover_x(_GY, 0)
_BASE = (_GX, _GY, 1, _GX * _GY % _P)


def ed25519_verify(public, message, signature):
    if len(public) != 32 or len(signature) != 64:
        return False
    A = _decompress(public)
    R = _decompress(signature[:32])
    if A is None or R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= _Q:
        return False
    h = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % _Q
    return _equal(_mul(s, _BASE), _add(R, _mul(h, A)))


# ==========================================================
# TOKEN
# ==========================================================

def _b64(text):
    return urlsafe_b64decode(text + "=" * (-len(text) % 4))


def read_token(token):
    """The license in a signed token, or None if it isn't valid for this PC."""
    try:
        body, signature = token.split(".")
        payload_bytes = _b64(body)
        if not ed25519_verify(bytes.fromhex(public_key_hex()), payload_bytes, _b64(signature)):
            return None
        data = json.loads(payload_bytes)
    except (ValueError, TypeError):
        return None
    if data.get("p") != "tailorbook" or data.get("m") != machine_id():
        return None
    return License(
        key=data.get("k", ""),
        name=data.get("n", ""),
        shop=data.get("s", ""),
        email=data.get("e", ""),
        issued=data.get("i", ""),
    )


def _load():
    try:
        return json.loads(_license_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save(data):
    path = _license_file()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def current():
    """The activated license on this PC, or None."""
    if not public_key_hex():
        return None
    token = _load().get("token")
    return read_token(token) if token else None


def remove():
    try:
        _license_file().unlink()
    except OSError:
        pass


# ==========================================================
# SERVER
# ==========================================================

def _request(path, data=None):
    if not server_url():
        raise LicenseError("The license server address is not set in this copy of the app.")
    url = f"{server_url()}/api/{path}"
    body = json.dumps(data).encode() if data is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"TailorBook/{APP_VERSION}",
        },
        method="POST" if body is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            reply = json.loads(error.read().decode("utf-8"))
        except ValueError:
            reply = {}
        raise LicenseError(
            reply.get("message") or f"The license server returned an error ({error.code}).",
            reply.get("error", "http"),
        )
    except (urllib.error.URLError, TimeoutError, OSError):
        raise LicenseError(
            "Could not reach the license server. Check your internet connection and try again.",
            "offline",
        )
    except ValueError:
        raise LicenseError("The license server sent an unexpected reply. Please try again later.")


def normalize_key(key):
    key = "".join(ch for ch in key.upper() if ch.isalnum())
    if key.startswith("TB"):
        key = key[2:]
    if len(key) != 20:
        return ""
    return "TB-" + "-".join(key[i:i + 5] for i in range(0, 20, 5))


def activate(key):
    """Activate this PC with a key. Returns the License or raises LicenseError."""
    clean = normalize_key(key)
    if not clean:
        raise LicenseError("That doesn't look like a license key. It should look like TB-XXXXX-XXXXX-XXXXX-XXXXX.")
    reply = _request("activate.php", {
        "key": clean,
        "machine_id": machine_id(),
        "machine_name": machine_name(),
        "app_version": APP_VERSION,
    })
    token = reply.get("token", "")
    license_ = read_token(token)
    if not license_:
        raise LicenseError("The license server's reply could not be verified. Please contact support.")
    _save({"token": token, "last_check": datetime.now().isoformat(timespec="seconds")})
    return license_


def check_due():
    data = _load()
    try:
        last = datetime.fromisoformat(data.get("last_check", ""))
    except ValueError:
        return True
    return datetime.now() - last >= CHECK_EVERY


def check():
    """Ask the server about this PC's license.

    Returns "active", "revoked", "moved" or "invalid". On "revoked", "moved"
    or "invalid" the saved license is removed. Raises LicenseError when the
    server can't be reached (the app keeps working).
    """
    license_ = current()
    if not license_:
        return "invalid"
    reply = _request("check.php", {
        "key": license_.key,
        "machine_id": machine_id(),
        "app_version": APP_VERSION,
    })
    status = reply.get("status", "active")
    if status in ("revoked", "moved", "invalid"):
        remove()
    else:
        data = _load()
        data["last_check"] = datetime.now().isoformat(timespec="seconds")
        _save(data)
    return status


STATUS_MESSAGES = {
    "revoked": "This license has been deactivated. Please contact support.",
    "moved": "This license has been moved to another computer, so it no longer works on this one.",
    "invalid": "This license is no longer valid. Please contact support.",
}


# ==========================================================
# UPDATES
# ==========================================================

def _version_tuple(version):
    parts = []
    for piece in str(version).split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits or 0))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def is_newer(version, than=APP_VERSION):
    return bool(version) and _version_tuple(version) > _version_tuple(than)


def latest():
    """Newest published version: dict with version, released, notes, size_mb, download_page."""
    return _request("latest.php")


def download_link():
    """A 30-minute download link for the newest installer (needs an activated license)."""
    license_ = current()
    if not license_:
        return f"{server_url()}/download.php"
    reply = _request("download-link.php", {"key": license_.key, "machine_id": machine_id()})
    return reply["url"]
