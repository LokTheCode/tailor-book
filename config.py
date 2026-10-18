DEBUG = False

# ==========================================================
# PRODUCT BRANDING (Tailor Book)
# ==========================================================
# Your product's name, shown on the login screen, in About and in the
# installer. The CUSTOMER's shop name is separate: they set it in
# Settings > Shop Details and it shows in the sidebar, window title,
# invoices and messages.
APP_NAME = "Tailor Book"
APP_TAGLINE = "Tailor shop management, made simple"

# Keep APP_VERSION in step with MyAppVersion in setup.iss
APP_VERSION = "1.1.0"

# Shown in Settings > About when filled in
APP_PUBLISHER = "Tailor Book"
APP_WEBSITE = ""        # e.g. "https://www.yourdomain.in"
SUPPORT_PHONE = ""      # e.g. "+91 98xxxxxxxx"
SUPPORT_EMAIL = ""      # e.g. "support@yourdomain.in"

# Folder name for the database, photos and logo, e.g.
# %LOCALAPPDATA%\TailorBook on Windows
DATA_FOLDER_NAME = "TailorBook"

# ==========================================================
# LICENSING AND UPDATES
# ==========================================================
# Your website, where the license server runs (no trailing slash), and the
# public key shown in the website's Admin > Releases page after setup.php.
# When LICENSE_PUBLIC_KEY is set (and always in the built .exe) the app asks
# for a license key before the login screen. Leave both empty while you
# develop from source.
LICENSE_SERVER_URL = ""   # e.g. "https://www.yourdomain.in"
LICENSE_PUBLIC_KEY = ""   # 64 hex characters
