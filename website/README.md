# Tailor Book website (Hostinger)

The product site, the shop (order → payment → license key), license downloads, the
license server the desktop app talks to, and an admin panel. Plain PHP 8 + SQLite, so it
runs on Hostinger shared hosting with nothing extra to install.

```
website/
  public_html/   → goes into your domain's public_html (everyone can see it)
  private/       → goes NEXT TO public_html, never inside it (database, keys, installers)
```

## 1. First-time setup on Hostinger

1. **hPanel → Websites → your domain → Advanced → PHP Configuration**: choose PHP 8.1 or
   newer. Under *PHP extensions*, make sure `pdo_sqlite` and `sodium` are ticked.
   Under *PHP options*, set `upload_max_filesize` and `post_max_size` to `256M` if you
   want to upload installers through the admin page.
2. **hPanel → Security → SSL**: install the free SSL certificate (the site forces HTTPS).
3. **hPanel → Emails**: create a mailbox such as `no-reply@yourdomain.in` and note its
   password. Put the address in `mail_from` and `smtp_user`, and the password in
   `smtp_password` in `config.php`. Emails are then sent through `smtp.hostinger.com`
   and reach the inbox. Test it in **Admin → Account → Send test email**.
   There is no database to create: the site keeps its data in one SQLite file,
   `private/data/tailorbook.sqlite`, made automatically.
4. **Fill in your details:** copy `private/config.sample.php` to `private/config.php`
   and edit every line marked `FILL IN`: business name and address, email, phone, UPI ID,
   bank details, price, grievance officer, jurisdiction city, `site_url`
   (`https://www.yourdomain.in`).
5. **Upload** with *File Manager* (or FTP). Your home folder looks like
   `domains/yourdomain.in/`. Put the contents of `website/public_html` into
   `domains/yourdomain.in/public_html/`, and the `website/private` folder at
   `domains/yourdomain.in/private/`, so it sits beside `public_html`.
6. Open `https://www.yourdomain.in/setup.php`. It checks the server, creates your admin
   login and the license signing keys. After that it locks itself.
7. Log in at `/admin/` → **Releases**. Copy the two lines under *Desktop app connection*
   into the desktop project's `config.py`.
8. Optional: put your UPI QR code at `public_html/assets/img/upi-qr.png`, screenshots in
   `public_html/assets/screenshots/`, a demo video (see `assets/video/README.txt`).

**Keep `private/keys/` safe.** Download a copy of that folder to your PC. If the secret key
is lost, every activated copy keeps working, but new activations need a rebuilt app.

## 2. Selling

1. A customer fills the form at `/buy.php`, ticking the Terms and No-refund boxes.
2. They pay by UPI/bank and enter the transaction ID (UTR) on their order page. You get
   an email.
3. Check the money arrived, then **Admin → Orders → open order → Approve**. The license
   key is created and emailed, and appears on the customer's order page.
4. The customer downloads from `/download.php` with their email + key, installs, and
   enters the key in the app. The key locks to that one computer.

Sold offline? **Admin → Orders → Add a sale by hand** creates the license straight away.

New computer? **Admin → Licenses → Move to new PC**, then they enter the same key on the
new computer. The old one stops working at its next weekly check.

## 3. Releasing a new version

1. In the desktop project set the same new version in `config.py` (`APP_VERSION`) and
   `setup.iss` (`MyAppVersion`), e.g. `1.2.0`.
2. Build on Windows from the project folder:

   ```
   build.bat
   ```

   It needs Python and [Inno Setup 6](https://jrsoftware.org/isdl.php). It checks your
   license settings, builds `dist\TailorBook\TailorBook.exe` with PyInstaller, then the
   installer `installer_output\TailorBook_Setup_v1.2.0.exe`.
3. **Admin → Releases → Upload** (or upload to `private/releases/` by File Manager with the
   version in the file name) and write *What's new*.
4. Customers' apps show **Update to v1.2.0** in the top bar (and Settings → About →
   Check for updates). Running the new installer upgrades in place; their data is kept.

## 4. Before going live

- Read every policy page (`privacy.php`, `terms.php`, `refund.php`, `support-policy.php`,
  `delivery.php`) and have a lawyer review them. They are written to follow the DPDP
  Act 2023 and DPDP Rules 2025, but are not legal advice.
- India's DPDP Rules: most duties apply from 13 May 2027 (notice, security, breach
  reporting, rights, 1-year log retention). The site already does these.
- Place a test order with your own email and approve it end to end.

## Testing locally

```
cd website/public_html
php -S 127.0.0.1:8080
```

then open http://127.0.0.1:8080/setup.php (set `site_url` to `http://localhost:8080` in
`private/config.php`).
