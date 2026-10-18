# Tailor Book

**Tailor shop management, made simple.** A Windows desktop app for tailoring
shops and boutiques: customers, measurements, orders, inventory, reports,
WhatsApp and email updates, and daily backups. Works offline; all data stays
on the shop's PC.

## Features

- Customers with photos, search and Excel export
- Measurements per garment, in inches or cm
- Orders with payments, status tracking and order numbering
- Inventory and stock movements
- Reports exported to formatted Excel
- WhatsApp (AiSensy) and email notifications, and marketing campaigns
- Users with roles (admin, sub admin) and page-by-page access
- 6 colour themes, custom accent colour, keyboard shortcuts
- Automatic daily backup and one-click restore

## Run from source

```
pip install -r requirements.txt
python main.py
```

Data is stored in `%LOCALAPPDATA%\TailorBook` (database, photos, logo).

## Build the installer (Windows)

1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php).
2. Run `build.bat` in the project folder.
3. The installer is written to `installer_output\TailorBook_Setup_v<version>.exe`.

## Branding

- Product name, version and support details: `config.py`
- Logo and icons: `assets/brand/`
- Installer name, publisher and version: `setup.iss`
- Each customer sets their own shop name and logo in Settings > Shop Details.
