<?php
define('ADMIN_PUBLIC', true);
require __DIR__ . '/_admin.php';

if (current_admin()) redirect('/admin/');
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    if (!rate_limit('admin_login', 8, 900)) {
        $error = 'Too many attempts. Wait 15 minutes and try again.';
    } else {
        $q = db()->prepare('SELECT * FROM admins WHERE username = ?');
        $q->execute([post('username')]);
        $admin = $q->fetch();
        if ($admin && password_verify(post('password'), $admin['password_hash'])) {
            session_regenerate_id(true);
            $_SESSION['admin_id'] = $admin['id'];
            $_SESSION['admin_seen'] = time();
            audit('login', $admin['username'] . ' from ' . client_ip());
            redirect('/admin/');
        }
        $error = 'Wrong username or password.';
    }
}

page_header('Admin login');
?>
<section class="page-hero"><div class="wrap narrow"><h1>Admin login</h1></div></section>
<section class="section" style="padding-top:16px"><div class="wrap narrow">
  <div class="card">
    <?php if ($error): ?><p class="alert alert-error"><?= e($error) ?></p><?php endif; ?>
    <form method="post" class="form">
      <?= csrf_field() ?>
      <label>Username <input name="username" required autocomplete="username"></label>
      <label>Password <input name="password" type="password" required autocomplete="current-password"></label>
      <button class="btn btn-primary" type="submit">Log in</button>
    </form>
  </div>
</div></section>
<?php page_footer();
