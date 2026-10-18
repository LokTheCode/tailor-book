<?php
/*
 * Loaded by every page: settings, database, session, helpers.
 */

declare(strict_types=1);

// ---------------------------------------------------------------
// Private folder (outside public_html when possible)
// ---------------------------------------------------------------
$privateCandidates = [
    dirname(__DIR__, 2) . '/private',   // domains/site/private  (recommended)
    dirname(__DIR__) . '/private',      // public_html/private   (protected by .htaccess)
];
$PRIVATE = null;
foreach ($privateCandidates as $candidate) {
    if (is_dir($candidate)) { $PRIVATE = realpath($candidate); break; }
}
if ($PRIVATE === null || !is_file($PRIVATE . '/config.php')) {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    exit("Website not configured yet.\n\n"
        . ($PRIVATE === null
            ? "The 'private' folder was not found. Put it next to this site's public_html folder:\n  " . dirname(__DIR__, 2) . "/private\n"
            : "In the folder {$PRIVATE}\ncopy config.sample.php to config.php and fill in your details.\n"));
}
define('PRIVATE_DIR', $PRIVATE);

$CONFIG = require PRIVATE_DIR . '/config.php';
date_default_timezone_set($CONFIG['timezone'] ?? 'Asia/Kolkata');

// Web path of this site, e.g. "" at the domain root or "/tailor-project/public_html"
// in a sub-folder. Every link and redirect starts with it.
define('BASE', (function (): string {
    // 1. From the running script: SCRIPT_NAME "/tailor-project/public_html/admin/index.php"
    //    minus its path inside the site "admin/index.php" -> "/tailor-project/public_html"
    $site = realpath(dirname(__DIR__));
    $file = realpath((string)($_SERVER['SCRIPT_FILENAME'] ?? ''));
    $name = str_replace('\\', '/', (string)($_SERVER['SCRIPT_NAME'] ?? ''));
    if ($site && $file && str_starts_with($file, $site . DIRECTORY_SEPARATOR)) {
        $inside = '/' . str_replace('\\', '/', substr($file, strlen($site) + 1));
        if ($name !== '' && str_ends_with($name, $inside)) {
            return rtrim(substr($name, 0, -strlen($inside)), '/');
        }
    }
    // 2. From the document root
    $docRoot = realpath((string)($_SERVER['DOCUMENT_ROOT'] ?? ''));
    if ($docRoot && $site && str_starts_with($site, $docRoot)) {
        return rtrim(str_replace('\\', '/', substr($site, strlen($docRoot))), '/');
    }
    // 3. From site_url in config.php
    return rtrim((string)(parse_url((string)($GLOBALS['CONFIG']['site_url'] ?? ''), PHP_URL_PATH) ?? ''), '/');
})());

/** Link to a page of this site: url('buy.php') -> /tailor-project/public_html/buy.php */
function url(string $path = ''): string {
    return BASE . '/' . ltrim($path, '/');
}

function config(string $key, $default = null) {
    global $CONFIG;
    return $CONFIG[$key] ?? $default;
}

// ---------------------------------------------------------------
// Errors: log, never show details to visitors
// ---------------------------------------------------------------
ini_set('display_errors', '0');
ini_set('log_errors', '1');
ini_set('error_log', PRIVATE_DIR . '/data/php-errors.log');

// ---------------------------------------------------------------
// Database (SQLite file in private/data)
// ---------------------------------------------------------------
const DB_SCHEMA_VERSION = 1;

function db(): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $dir = PRIVATE_DIR . '/data';
    if (!is_dir($dir)) mkdir($dir, 0750, true);
    $pdo = new PDO('sqlite:' . $dir . '/tailorbook.sqlite');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $pdo->exec('PRAGMA foreign_keys = ON');
    $pdo->exec('PRAGMA busy_timeout = 5000');
    if ((int)$pdo->query('PRAGMA user_version')->fetchColumn() < DB_SCHEMA_VERSION) {
        db_migrate();
        $pdo->exec('PRAGMA user_version = ' . DB_SCHEMA_VERSION);
    }
    return $pdo;
}

function db_migrate(): void {
    db()->exec(<<<SQL
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        order_no TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        shop_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        city TEXT, state TEXT, gstin TEXT,
        amount INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'awaiting_payment',
        payment_ref TEXT, payment_submitted_at TEXT,
        admin_note TEXT,
        consent_at TEXT NOT NULL, consent_ip TEXT,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY,
        license_key TEXT NOT NULL UNIQUE,
        order_id INTEGER REFERENCES orders(id),
        name TEXT NOT NULL, shop_name TEXT, email TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        machine_id TEXT, machine_name TEXT, app_version TEXT,
        activated_at TEXT, last_seen_at TEXT,
        activations INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS releases (
        id INTEGER PRIMARY KEY,
        version TEXT NOT NULL UNIQUE,
        filename TEXT NOT NULL,
        size INTEGER NOT NULL DEFAULT 0,
        sha256 TEXT,
        notes TEXT,
        published INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY,
        license_id INTEGER NOT NULL REFERENCES licenses(id),
        version TEXT, ip TEXT, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS download_tokens (
        token TEXT PRIMARY KEY,
        license_id INTEGER NOT NULL REFERENCES licenses(id),
        expires_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT,
        message TEXT NOT NULL, is_read INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY,
        kind TEXT NOT NULL, ip TEXT NOT NULL, created_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS attempts_kind_ip ON attempts(kind, ip, created_at);
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY,
        action TEXT NOT NULL, detail TEXT, created_at TEXT NOT NULL
    );
    SQL);
}

function now(): string { return date('Y-m-d H:i:s'); }

function audit(string $action, string $detail = ''): void {
    db()->prepare('INSERT INTO audit_log (action, detail, created_at) VALUES (?, ?, ?)')
        ->execute([$action, $detail, now()]);
}

// ---------------------------------------------------------------
// Session & security
// ---------------------------------------------------------------
function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    session_name('tbsid');
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => BASE . '/',
        'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
}

function e(?string $text): string {
    return htmlspecialchars((string)$text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function csrf_token(): string {
    start_session();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function csrf_field(): string {
    return '<input type="hidden" name="csrf" value="' . e(csrf_token()) . '">';
}

function csrf_check(): void {
    start_session();
    $sent = $_POST['csrf'] ?? '';
    if (!is_string($sent) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $sent)) {
        http_response_code(400);
        exit('This form has expired. Please go back, refresh the page and try again.');
    }
}

function client_ip(): string {
    return substr((string)($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0'), 0, 45);
}

/** True if this IP made fewer than $max attempts of $kind in the last $seconds; records the attempt. */
function rate_limit(string $kind, int $max, int $seconds): bool {
    $pdo = db();
    $since = time() - $seconds;
    $pdo->prepare('DELETE FROM attempts WHERE created_at < ?')->execute([time() - 86400]);
    $q = $pdo->prepare('SELECT COUNT(*) FROM attempts WHERE kind = ? AND ip = ? AND created_at >= ?');
    $q->execute([$kind, client_ip(), $since]);
    if ((int)$q->fetchColumn() >= $max) return false;
    $pdo->prepare('INSERT INTO attempts (kind, ip, created_at) VALUES (?, ?, ?)')
        ->execute([$kind, client_ip(), time()]);
    return true;
}

function redirect(string $path): void {
    if (str_starts_with($path, '/') && !str_starts_with($path, '//') && !str_starts_with($path, BASE . '/')) {
        $path = BASE . $path;
    }
    header('Location: ' . $path);
    exit;
}

function flash(?string $message = null, string $type = 'ok'): ?array {
    start_session();
    if ($message !== null) { $_SESSION['flash'] = [$type, $message]; return null; }
    $value = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $value;
}

function post(string $key): string {
    $value = $_POST[$key] ?? '';
    return is_string($value) ? trim($value) : '';
}

// ---------------------------------------------------------------
// Formatting
// ---------------------------------------------------------------
function money(int|float $rupees): string {
    return '₹' . number_format((float)$rupees, 0, '.', ',');
}

function nice_date(?string $value): string {
    return $value ? date('d M Y', strtotime($value)) : '-';
}

function nice_datetime(?string $value): string {
    return $value ? date('d M Y, h:i A', strtotime($value)) : '-';
}

function site_url(string $path = ''): string {
    return rtrim((string)config('site_url'), '/') . '/' . ltrim($path, '/');
}

// ---------------------------------------------------------------
// Keys & numbers
// ---------------------------------------------------------------
/** TB-XXXXX-XXXXX-XXXXX-XXXXX using letters/digits that can't be confused (no 0/O, 1/I/L). */
function new_license_key(): string {
    $alphabet = '23456789ABCDEFGHJKMNPQRSTUVWXYZ';
    do {
        $groups = [];
        for ($g = 0; $g < 4; $g++) {
            $group = '';
            for ($i = 0; $i < 5; $i++) $group .= $alphabet[random_int(0, strlen($alphabet) - 1)];
            $groups[] = $group;
        }
        $key = 'TB-' . implode('-', $groups);
        $q = db()->prepare('SELECT 1 FROM licenses WHERE license_key = ?');
        $q->execute([$key]);
    } while ($q->fetchColumn());
    return $key;
}

function normalize_key(string $key): string {
    $key = strtoupper(preg_replace('/[^A-Za-z0-9]/', '', $key));
    if (str_starts_with($key, 'TB')) $key = substr($key, 2);
    if (strlen($key) !== 20) return '';
    return 'TB-' . implode('-', str_split($key, 5));
}

function new_order_no(): string {
    $year = date('Y');
    $q = db()->prepare("SELECT COUNT(*) FROM orders WHERE order_no LIKE ?");
    $q->execute(["TB{$year}-%"]);
    $n = (int)$q->fetchColumn() + 1;
    return sprintf('TB%s-%04d', $year, $n);
}

// ---------------------------------------------------------------
// Email (PHP mail(); on Hostinger send from a mailbox on your domain)
// ---------------------------------------------------------------
/**
 * Send a plain-text email. Uses your mailbox over SMTP when smtp_password is
 * set in config.php (recommended: lands in the inbox, not spam), otherwise
 * PHP mail(). Failures are written to private/data/php-errors.log.
 */
function send_mail(string $to, string $subject, string $body, ?string &$error = null): bool {
    $error = null;
    try {
        if ((string)config('smtp_password') !== '') {
            smtp_send($to, $subject, $body);
            return true;
        }
        $fromAddress = (string)config('mail_from');
        $headers = mail_headers($to, $subject, false);
        unset($headers['To'], $headers['Subject']);
        if (!@mail($to, mb_encode_mimeheader($subject, 'UTF-8'), $body, $headers, '-f' . $fromAddress)) {
            throw new RuntimeException('PHP mail() could not send. Set the smtp_ settings in config.php.');
        }
        return true;
    } catch (Throwable $e) {
        $error = $e->getMessage();
        error_log("Email to {$to} failed ({$subject}): {$error}");
        return false;
    }
}

function mail_headers(string $to, string $subject, bool $full = true): array {
    $fromAddress = (string)config('mail_from');
    $fromName = (string)config('mail_from_name', config('product_name'));
    $domain = substr(strrchr($fromAddress, '@') ?: '@localhost', 1);
    return [
        'Date' => date('r'),
        'From' => mb_encode_mimeheader($fromName, 'UTF-8') . " <{$fromAddress}>",
        'To' => $to,
        'Subject' => mb_encode_mimeheader($subject, 'UTF-8'),
        'Reply-To' => (string)config('business_email', $fromAddress),
        'Message-ID' => '<' . bin2hex(random_bytes(12)) . '@' . $domain . '>',
        'MIME-Version' => '1.0',
        'Content-Type' => 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding' => '8bit',
        'X-Mailer' => 'TailorBook',
    ];
}

/** Minimal SMTP client: SSL (port 465) or STARTTLS (587), AUTH LOGIN. */
function smtp_send(string $to, string $subject, string $body): void {
    $host = (string)config('smtp_host', 'smtp.hostinger.com');
    $port = (int)config('smtp_port', 465);
    $secure = (string)config('smtp_secure', $port === 465 ? 'ssl' : 'tls');   // ssl | tls | none
    $user = (string)config('smtp_user', config('mail_from'));
    $pass = (string)config('smtp_password');
    $from = (string)config('mail_from');

    $context = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $socket = @stream_socket_client(($secure === 'ssl' ? 'ssl://' : 'tcp://') . "{$host}:{$port}",
        $errno, $errstr, 20, STREAM_CLIENT_CONNECT, $context);
    if (!$socket) throw new RuntimeException("Could not connect to {$host}:{$port} ({$errstr})");
    stream_set_timeout($socket, 20);

    $read = function () use ($socket): string {
        $reply = '';
        while (($line = fgets($socket, 1024)) !== false) {
            $reply .= $line;
            if (strlen($line) < 4 || $line[3] !== '-') break;
        }
        return $reply;
    };
    $send = function (string $command, array $expect, bool $secret = false) use ($socket, $read): string {
        if ($command !== '') fwrite($socket, $command . "\r\n");
        $reply = $read();
        if (!in_array((int)substr($reply, 0, 3), $expect, true)) {
            $shown = $secret ? 'login' : strtok($command, "\r\n");
            throw new RuntimeException('SMTP server said: ' . trim($reply ?: 'no reply') . " (after {$shown})");
        }
        return $reply;
    };

    try {
        $helo = parse_url((string)config('site_url'), PHP_URL_HOST) ?: 'localhost';
        $send('', [220]);
        $send("EHLO {$helo}", [250]);
        if ($secure === 'tls') {
            $send('STARTTLS', [220]);
            if (!stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('Could not start TLS encryption.');
            }
            $send("EHLO {$helo}", [250]);
        }
        $send('AUTH LOGIN', [334]);
        $send(base64_encode($user), [334], true);
        try {
            $send(base64_encode($pass), [235], true);
        } catch (RuntimeException $e) {
            throw new RuntimeException('Email login failed: check smtp_user and smtp_password in config.php.');
        }
        $send("MAIL FROM:<{$from}>", [250]);
        $send("RCPT TO:<{$to}>", [250, 251]);
        $send('DATA', [354]);

        $message = '';
        foreach (mail_headers($to, $subject) as $name => $value) $message .= "{$name}: {$value}\r\n";
        $text = preg_replace("/\r\n|\r|\n/", "\r\n", $body);
        $text = preg_replace('/^\./m', '..', $text);          // dot-stuffing
        $send($message . "\r\n" . $text . "\r\n.", [250], true);
        $send('QUIT', [221]);
    } finally {
        fclose($socket);
    }
}

// ---------------------------------------------------------------
// Releases (installer files in private/releases)
// ---------------------------------------------------------------
function releases_dir(): string {
    $dir = PRIVATE_DIR . '/releases';
    if (!is_dir($dir)) mkdir($dir, 0750, true);
    return $dir;
}

/** Add any installer files uploaded by FTP / File Manager to the releases table. */
function sync_releases(): void {
    foreach (glob(releases_dir() . '/*.exe') ?: [] as $path) {
        $file = basename($path);
        if (!preg_match('/v?(\d+\.\d+(?:\.\d+)?)/i', $file, $m)) continue;
        $version = $m[1];
        $q = db()->prepare('SELECT id, filename, size FROM releases WHERE version = ?');
        $q->execute([$version]);
        $row = $q->fetch();
        $size = filesize($path);
        if (!$row) {
            db()->prepare('INSERT INTO releases (version, filename, size, sha256, created_at) VALUES (?, ?, ?, ?, ?)')
                ->execute([$version, $file, $size, hash_file('sha256', $path), now()]);
        } elseif ($row['filename'] !== $file || (int)$row['size'] !== $size) {
            db()->prepare('UPDATE releases SET filename = ?, size = ?, sha256 = ? WHERE id = ?')
                ->execute([$file, $size, hash_file('sha256', $path), $row['id']]);
        }
    }
}

function latest_release(): ?array {
    sync_releases();
    $rows = db()->query('SELECT * FROM releases WHERE published = 1')->fetchAll();
    $rows = array_filter($rows, fn($r) => is_file(releases_dir() . '/' . $r['filename']));
    if (!$rows) return null;
    usort($rows, fn($a, $b) => version_compare($b['version'], $a['version']));
    return $rows[0];
}

// ---------------------------------------------------------------
// License signing (Ed25519, keys created by setup.php)
// ---------------------------------------------------------------
function signing_secret_key(): string {
    $hex = @file_get_contents(PRIVATE_DIR . '/keys/signing.key');
    if (!$hex) throw new RuntimeException('Signing key missing: run setup.php');
    return sodium_hex2bin(trim($hex));
}

function signing_public_key_hex(): string {
    return trim((string)@file_get_contents(PRIVATE_DIR . '/keys/signing.pub'));
}

function b64url(string $data): string {
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}

/** Signed activation token the desktop app stores and checks offline. */
function sign_license(array $payload): string {
    $json = json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    $signature = sodium_crypto_sign_detached($json, signing_secret_key());
    return b64url($json) . '.' . b64url($signature);
}

function is_installed(): bool {
    return is_file(PRIVATE_DIR . '/keys/signing.key') && is_file(PRIVATE_DIR . '/data/installed.lock');
}


