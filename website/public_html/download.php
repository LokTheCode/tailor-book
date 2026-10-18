<?php
/*
 * Licensed download of the latest installer.
 *  - Website: email + license key (POST)
 *  - Desktop app "Update available": one-time link ?t=TOKEN from api/download-link.php
 * The installer itself lives in private/releases and is never reachable directly.
 */
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/orders.php';

$product = config('product_name');
$error = '';

function send_installer(array $license, array $release): void {
    $path = releases_dir() . '/' . basename($release['filename']);
    if (!is_file($path)) {
        http_response_code(404);
        exit('The installer file is missing on the server. Please contact support.');
    }

    $limit = (int)config('max_downloads_per_day', 5);
    $q = db()->prepare("SELECT COUNT(*) FROM downloads WHERE license_id = ? AND created_at >= ?");
    $q->execute([$license['id'], date('Y-m-d H:i:s', time() - 86400)]);
    if ((int)$q->fetchColumn() >= $limit) {
        flash("This license has reached its download limit for today ({$limit}). Please try again tomorrow or contact us.", 'error');
        redirect('/download.php');
    }

    db()->prepare('INSERT INTO downloads (license_id, version, ip, created_at) VALUES (?, ?, ?, ?)')
        ->execute([$license['id'], $release['version'], client_ip(), now()]);

    while (ob_get_level()) ob_end_clean();
    set_time_limit(0);
    $name = preg_replace('/[^A-Za-z0-9._-]/', '_', basename($release['filename']));
    header('Content-Type: application/vnd.microsoft.portable-executable');
    header('Content-Disposition: attachment; filename="' . $name . '"');
    header('Content-Length: ' . filesize($path));
    header('X-Content-Type-Options: nosniff');
    header('Cache-Control: private, no-store');
    readfile($path);
    exit;
}

$release = latest_release();

// ---- One-time link from the desktop app
if (isset($_GET['t'])) {
    $token = preg_replace('/[^a-f0-9]/', '', (string)$_GET['t']);
    $q = db()->prepare('SELECT l.* FROM download_tokens t JOIN licenses l ON l.id = t.license_id WHERE t.token = ? AND t.expires_at > ?');
    $q->execute([$token, time()]);
    $license = $q->fetch();
    db()->prepare('DELETE FROM download_tokens WHERE expires_at <= ?')->execute([time()]);
    if ($license && $license['status'] === 'active' && $release) {
        send_installer($license, $release);
    }
    $error = 'This download link has expired. Enter your email and license key below instead.';
}

// ---- Email + key form
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    if (!rate_limit('download', 15, 3600)) {
        $error = 'Too many attempts. Please try again in an hour.';
    } else {
        $license = find_license(post('license_key'));
        if (!$license || strcasecmp($license['email'], post('email')) !== 0) {
            $error = 'That email and license key do not match. Use the email you bought with, and copy the key from your email.';
        } elseif ($license['status'] !== 'active') {
            $error = 'This license is not active. Please contact us.';
        } elseif (!$release) {
            $error = 'The installer is being updated. Please try again in a little while.';
        } else {
            send_installer($license, $release);
        }
    }
}

page_header('Download', "Download {$product} with your license key.", 'download');
?>
<section class="page-hero">
  <div class="wrap narrow">
    <h1>Download <?= e($product) ?></h1>
    <p class="lead">Enter the email you bought with and your license key. Don't have a key yet? <a href="/buy.php">Buy a license</a>.</p>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap narrow">
    <div class="card">
      <?php if ($error): ?><p class="alert alert-error"><?= e($error) ?></p><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?>
        <div class="form-grid">
          <label>Email <input name="email" type="email" required autocomplete="email" value="<?= e(post('email')) ?>"></label>
          <label>License key <input name="license_key" required placeholder="TB-XXXXX-XXXXX-XXXXX-XXXXX" class="mono" value="<?= e(post('license_key')) ?>"></label>
        </div>
        <button class="btn btn-primary" type="submit"<?= $release ? '' : ' disabled' ?>>Download<?= $release ? ' version ' . e($release['version']) : '' ?></button>
      </form>
    </div>

    <?php if ($release): ?>
    <div class="card">
      <h2>Version <?= e($release['version']) ?></h2>
      <p class="muted small">Released <?= e(nice_date($release['created_at'])) ?> · <?= e(number_format($release['size'] / 1048576, 1)) ?> MB · Windows 10 and 11 (64-bit)</p>
      <?php if ($release['notes']): ?><div style="white-space:pre-line"><?= e($release['notes']) ?></div><?php endif; ?>
      <h3>Already installed?</h3>
      <p>Run the new installer over the old one. Your customers, orders and settings are kept. We still recommend a backup first: Settings &gt; Backup &gt; Back Up Now.</p>
      <?php if ($release['sha256']): ?><p class="muted small">SHA-256: <span class="mono" style="word-break:break-all"><?= e($release['sha256']) ?></span></p><?php endif; ?>
    </div>
    <?php endif; ?>
  </div>
</section>
<?php page_footer();
