<?php
/*
 * First-time setup. Open https://yourdomain.in/setup.php once:
 * checks the server, creates the database, your admin login and the
 * license signing keys. Locked after it runs.
 */
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$checks = [
    'PHP 8.0 or newer'            => version_compare(PHP_VERSION, '8.0.0', '>='),
    'SQLite (pdo_sqlite)'         => extension_loaded('pdo_sqlite'),
    'Sodium (license signing)'    => function_exists('sodium_crypto_sign_keypair'),
    'private/data is writable'    => is_writable(PRIVATE_DIR . '/data') || @mkdir(PRIVATE_DIR . '/data', 0750, true),
    'private/keys is writable'    => is_writable(PRIVATE_DIR . '/keys') || @mkdir(PRIVATE_DIR . '/keys', 0750, true),
    'private/releases exists'     => is_dir(PRIVATE_DIR . '/releases') || @mkdir(PRIVATE_DIR . '/releases', 0750, true),
    'site_url filled in'          => !str_contains((string)config('site_url'), 'yourdomain'),
];
$allOk = !in_array(false, $checks, true);
$error = '';
$publicKey = '';

if (!is_installed() && $_SERVER['REQUEST_METHOD'] === 'POST' && $allOk) {
    csrf_check();
    $username = post('username');
    $password = post('password');
    if (!preg_match('/^[A-Za-z0-9_.@-]{3,40}$/', $username)) {
        $error = 'Username: 3-40 letters, numbers or . _ @ -';
    } elseif (strlen($password) < 10) {
        $error = 'Password must be at least 10 characters.';
    } elseif ($password !== post('password2')) {
        $error = 'Passwords do not match.';
    } else {
        db_migrate();
        db()->prepare('INSERT INTO admins (username, password_hash, created_at) VALUES (?, ?, ?)')
            ->execute([$username, password_hash($password, PASSWORD_DEFAULT), now()]);

        $pair = sodium_crypto_sign_keypair();
        file_put_contents(PRIVATE_DIR . '/keys/signing.key', sodium_bin2hex(sodium_crypto_sign_secretkey($pair)));
        file_put_contents(PRIVATE_DIR . '/keys/signing.pub', sodium_bin2hex(sodium_crypto_sign_publickey($pair)));
        @chmod(PRIVATE_DIR . '/keys/signing.key', 0600);
        file_put_contents(PRIVATE_DIR . '/data/installed.lock', now());
        audit('setup', "admin {$username} created");
        $publicKey = signing_public_key_hex();
    }
}

page_header('Setup');
?>
<section class="page-hero"><div class="wrap narrow"><h1>Website setup</h1></div></section>
<section class="section"><div class="wrap narrow">
<?php if ($publicKey): ?>
  <div class="card">
    <h2>Setup complete</h2>
    <p>Your admin login is ready: <a href="<?= BASE ?>/admin/">open the admin panel</a>.</p>
    <h3>One more step: connect the desktop app</h3>
    <p>Copy this public key into <code>config.py</code> of the desktop app as
       <code>LICENSE_PUBLIC_KEY</code>, set <code>LICENSE_SERVER_URL</code> to
       <code><?= e(rtrim((string)config('site_url'), '/')) ?></code>, then build the installer.</p>
    <pre class="keybox"><?= e($publicKey) ?></pre>
    <p class="muted small">You can see this key again any time in Admin &gt; Releases.</p>
  </div>
<?php elseif (is_installed()): ?>
  <div class="card"><h2>Already set up</h2><p>Go to the <a href="<?= BASE ?>/admin/">admin panel</a>.</p></div>
<?php else: ?>
  <div class="card">
    <h2>Server check</h2>
    <ul class="checklist">
      <?php foreach ($checks as $label => $ok): ?>
        <li class="<?= $ok ? 'ok' : 'bad' ?>"><?= $ok ? '✔' : '✖' ?> <?= e($label) ?></li>
      <?php endforeach; ?>
    </ul>
    <?php if (!$allOk): ?>
      <p class="alert alert-error">Fix the items marked ✖ (see the guide), then reload this page.</p>
    <?php else: ?>
      <h2>Create your admin login</h2>
      <?php if ($error): ?><p class="alert alert-error"><?= e($error) ?></p><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?>
        <label>Username <input name="username" required autocomplete="username"></label>
        <label>Password (10+ characters) <input name="password" type="password" required minlength="10" autocomplete="new-password"></label>
        <label>Confirm password <input name="password2" type="password" required minlength="10" autocomplete="new-password"></label>
        <button class="btn btn-primary" type="submit">Finish setup</button>
      </form>
    <?php endif; ?>
  </div>
<?php endif; ?>
</div></section>
<?php page_footer();
