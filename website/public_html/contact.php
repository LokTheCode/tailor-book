<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$errors = [];
$sent = false;
$v = ['name' => '', 'email' => '', 'phone' => '', 'message' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    foreach ($v as $k => $_) $v[$k] = post($k);
    if (post('website') !== '') redirect('/');   // honeypot
    if (mb_strlen($v['name']) < 2) $errors[] = 'Enter your name.';
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Enter a valid email address so we can reply.';
    if (mb_strlen($v['message']) < 10) $errors[] = 'Write a message of at least 10 characters.';
    if (empty($_POST['consent'])) $errors[] = 'Please agree to us using your details to reply.';
    if (!$errors && !rate_limit('contact', 5, 3600)) $errors[] = 'Too many messages. Please try again later or call us.';

    if (!$errors) {
        db()->prepare('INSERT INTO messages (name, email, phone, message, created_at) VALUES (?, ?, ?, ?, ?)')
            ->execute([$v['name'], strtolower($v['email']), $v['phone'], mb_substr($v['message'], 0, 5000), now()]);
        $admin = (string)config('admin_notify_email');
        if ($admin) {
            send_mail($admin, 'New message from ' . $v['name'],
                "{$v['name']} <{$v['email']}> {$v['phone']}\n\n{$v['message']}\n\n" . site_url('admin/messages.php'));
        }
        $sent = true;
        $v = array_map(fn() => '', $v);
    }
}

page_header('Contact', 'Questions about ' . config('product_name') . '? Contact us.');
?>
<section class="page-hero">
  <div class="wrap narrow">
    <h1>Contact us</h1>
    <p class="lead">Questions before buying, help with installation, or support? We usually reply within one working day.</p>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap narrow">
    <div class="card">
      <table class="data">
        <tr><th>Business</th><td><?= e(config('business_name')) ?></td></tr>
        <tr><th>Address</th><td><?= e(config('business_address')) ?></td></tr>
        <tr><th>Phone / WhatsApp</th><td><a href="tel:<?= e(preg_replace('/\s+/', '', (string)config('business_phone'))) ?>"><?= e(config('business_phone')) ?></a></td></tr>
        <tr><th>Email</th><td><a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a></td></tr>
        <?php if (config('support_hours')): ?><tr><th>Hours</th><td><?= e(config('support_hours')) ?></td></tr><?php endif; ?>
      </table>
    </div>
    <div class="card">
      <h2>Send a message</h2>
      <?php if ($sent): ?><p class="alert alert-ok">Message sent. We will reply to your email soon.</p><?php endif; ?>
      <?php foreach ($errors as $err): ?><p class="alert alert-error"><?= e($err) ?></p><?php endforeach; ?>
      <form method="post" class="form">
        <?= csrf_field() ?>
        <div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          <label>Name <input name="name" value="<?= e($v['name']) ?>" required autocomplete="name"></label>
          <label>Email <input name="email" type="email" value="<?= e($v['email']) ?>" required autocomplete="email"></label>
          <label>Mobile <span class="hint">Optional</span><input name="phone" value="<?= e($v['phone']) ?>" autocomplete="tel"></label>
        </div>
        <label>Message <textarea name="message" rows="5" required><?= e($v['message']) ?></textarea></label>
        <label class="check"><input type="checkbox" name="consent" value="1"><span>I agree to my details being used to reply to this message, as described in the <a href="<?= BASE ?>/privacy.php" target="_blank">Privacy Policy</a>.</span></label>
        <button class="btn btn-primary" type="submit">Send message</button>
      </form>
    </div>
  </div>
</section>
<?php page_footer();
