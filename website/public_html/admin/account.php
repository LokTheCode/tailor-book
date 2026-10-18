<?php
require __DIR__ . '/_admin.php';

$admin = current_admin();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    if (post('action') === 'test_mail') {
        $to = post('to');
        if (!filter_var($to, FILTER_VALIDATE_EMAIL)) {
            flash('Enter a valid email address.', 'error');
        } elseif (send_mail($to, 'Test email from ' . config('product_name'),
            "This is a test email from your website.\n\nIf you can read this, license and order emails will arrive too.\n\n" . site_url(), $mailError)) {
            flash("Test email sent to {$to}. Check the inbox (and spam folder).");
        } else {
            flash('Email not sent: ' . $mailError, 'error');
        }
        redirect('/admin/account.php');
    }
    $q = db()->prepare('SELECT password_hash FROM admins WHERE id = ?');
    $q->execute([$admin['id']]);
    if (!password_verify(post('current'), (string)$q->fetchColumn())) {
        flash('Current password is wrong.', 'error');
    } elseif (strlen(post('new')) < 10 || post('new') !== post('confirm')) {
        flash('The new password must be at least 10 characters and typed the same twice.', 'error');
    } else {
        db()->prepare('UPDATE admins SET password_hash = ? WHERE id = ?')->execute([password_hash(post('new'), PASSWORD_DEFAULT), $admin['id']]);
        audit('password_changed', $admin['username']);
        flash('Password changed.');
    }
    redirect('/admin/account.php');
}

$log = db()->query('SELECT * FROM audit_log ORDER BY id DESC LIMIT 50')->fetchAll();
admin_header('Account', 'account');
?>
<div class="card">
  <h2>Change password</h2>
  <p class="muted">Logged in as <?= e($admin['username']) ?>.</p>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <div class="form-grid">
      <label>Current password <input type="password" name="current" required autocomplete="current-password"></label>
      <span></span>
      <label>New password <input type="password" name="new" required minlength="10" autocomplete="new-password"></label>
      <label>Confirm new password <input type="password" name="confirm" required minlength="10" autocomplete="new-password"></label>
    </div>
    <button class="btn btn-primary">Change password</button>
  </form>
</div>
<div class="card">
  <h2>Email</h2>
  <p class="muted">Sending from <?= e((string)config('mail_from')) ?>
    <?= config('smtp_password') ? 'through ' . e((string)config('smtp_host', 'smtp.hostinger.com')) . ' (SMTP)' : 'with PHP mail(). Add smtp_password in config.php so emails don&rsquo;t go to spam.' ?></p>
  <form method="post" class="form">
    <?= csrf_field() ?><input type="hidden" name="action" value="test_mail">
    <div class="form-grid">
      <label>Send a test email to <input type="email" name="to" required value="<?= e((string)config('admin_notify_email')) ?>"></label>
    </div>
    <button class="btn btn-ghost">Send test email</button>
  </form>
</div>
<h2>Activity</h2>
<div class="table-wrap"><table class="data">
  <tr><th>When</th><th>What</th><th>Details</th></tr>
  <?php foreach ($log as $row): ?>
    <tr><td><?= e(nice_datetime($row['created_at'])) ?></td><td><?= e(str_replace('_', ' ', $row['action'])) ?></td><td class="small"><?= e((string)$row['detail']) ?></td></tr>
  <?php endforeach; ?>
</table></div>
<?php admin_footer();
