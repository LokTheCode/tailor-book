<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/orders.php';

$product = config('product_name');
$error = '';
$orderNo = strtoupper(trim((string)($_GET['no'] ?? '')));
$order = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $action = post('action');

    if ($action === 'lookup') {
        if (!rate_limit('order_lookup', 20, 3600)) {
            $error = 'Too many attempts. Please try again in an hour.';
        } else {
            $found = find_order(post('order_no'));
            if ($found && strcasecmp($found['email'], post('email')) === 0) {
                remember_order($found['order_no']);
                redirect('/order.php?no=' . urlencode($found['order_no']));
            }
            $error = 'No order matches that order number and email. Check both and try again.';
        }
    }

    if ($action === 'payment' && can_view_order($orderNo)) {
        $order = find_order($orderNo);
        $ref = strtoupper(preg_replace('/\s+/', '', post('payment_ref')));
        if (!$order || !in_array($order['status'], ['awaiting_payment', 'payment_submitted', 'rejected'], true)) {
            redirect('/order.php?no=' . urlencode($orderNo));
        }
        if (!preg_match('/^[A-Z0-9]{6,30}$/', $ref)) {
            $error = 'Enter the transaction ID / UTR exactly as shown in your payment app (6 to 30 letters or numbers).';
        } else {
            db()->prepare("UPDATE orders SET payment_ref = ?, payment_submitted_at = ?, status = 'payment_submitted', updated_at = ? WHERE id = ?")
                ->execute([$ref, now(), now(), $order['id']]);
            $admin = (string)config('admin_notify_email');
            if ($admin) {
                send_mail($admin, "Payment submitted: {$order['order_no']}",
                    "{$order['name']} / {$order['shop_name']} says they paid " . money((int)$order['amount']) . ".\n"
                    . "Transaction ID / UTR: {$ref}\n\nCheck your bank or UPI app, then approve:\n" . site_url('admin/orders.php'));
            }
            flash('Thank you. We will check the payment and email your license key, usually within one working day.');
            redirect('/order.php?no=' . urlencode($orderNo));
        }
    }
}

if ($orderNo && can_view_order($orderNo)) {
    $order = find_order($orderNo);
}
$license = $order ? order_license((int)$order['id']) : null;
$qr = is_file(__DIR__ . '/assets/img/upi-qr.png') ? url('assets/img/upi-qr.png') : null;

page_header('Order status', 'Check your order and get your license key.', 'order');
?>
<section class="page-hero">
  <div class="wrap narrow">
    <h1><?= $order ? 'Order ' . e($order['order_no']) : 'Order status' ?></h1>
    <?php if (!$order): ?><p class="lead">Enter your order number and email to see your order, pay, or get your license key.</p><?php endif; ?>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap narrow">
<?php if (!$order): ?>
    <div class="card">
      <?php if ($error): ?><p class="alert alert-error"><?= e($error) ?></p><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?><input type="hidden" name="action" value="lookup">
        <div class="form-grid">
          <label>Order number <input name="order_no" placeholder="TB2026-0001" required></label>
          <label>Email <input name="email" type="email" required autocomplete="email"></label>
        </div>
        <button class="btn btn-primary" type="submit">Show my order</button>
      </form>
    </div>
<?php else: ?>
    <div class="card">
      <p><span class="status status-<?= e($order['status']) ?>"><?= e(order_status_label($order['status'])) ?></span></p>
      <table class="data">
        <tr><th>Name</th><td><?= e($order['name']) ?></td></tr>
        <tr><th>Shop</th><td><?= e($order['shop_name']) ?></td></tr>
        <tr><th>Amount</th><td><?= e(money((int)$order['amount'])) ?></td></tr>
        <tr><th>Ordered on</th><td><?= e(nice_datetime($order['created_at'])) ?></td></tr>
        <?php if ($order['payment_ref']): ?><tr><th>Transaction ID</th><td class="mono"><?= e($order['payment_ref']) ?></td></tr><?php endif; ?>
      </table>
    </div>

  <?php if ($order['status'] === 'paid' && $license): ?>
    <div class="card">
      <h2>Your license key</h2>
      <div class="copy-row">
        <pre class="keybox" id="license-key"><?= e($license['license_key']) ?></pre>
        <button class="btn btn-ghost" type="button" data-copy="license-key">Copy</button>
      </div>
      <p class="muted small">We have also emailed it to <?= e($order['email']) ?>. It activates on one computer.</p>
      <form method="post" action="<?= BASE ?>/download.php" class="form" style="margin-top:16px">
        <?= csrf_field() ?>
        <input type="hidden" name="email" value="<?= e($order['email']) ?>">
        <input type="hidden" name="license_key" value="<?= e($license['license_key']) ?>">
        <button class="btn btn-primary" type="submit">Download <?= e($product) ?></button>
      </form>
      <h3>After downloading</h3>
      <ol>
        <li>Open the downloaded file and follow the installer.</li>
        <li>Open <?= e($product) ?> and enter your license key.</li>
        <li>Log in and set your shop name in Settings &gt; Shop Details.</li>
      </ol>
    </div>

  <?php else: ?>
    <?php if ($order['status'] === 'rejected'): ?>
      <p class="alert alert-error">We could not find this payment.<?= $order['admin_note'] ? ' ' . e($order['admin_note']) : '' ?>
        <br>Please check the transaction ID below or <a href="<?= BASE ?>/contact.php">contact us</a>.</p>
    <?php endif; ?>
    <div class="card">
      <h2><?= $order['status'] === 'payment_submitted' ? 'We are checking your payment' : 'Pay ' . e(money((int)$order['amount'])) ?></h2>
      <?php if ($order['status'] === 'payment_submitted'): ?>
        <p>We have your transaction ID. You will get your license key by email once the payment is confirmed, usually within one working day. Entered the wrong ID? Correct it below.</p>
      <?php endif; ?>
      <div class="pay-grid">
        <div class="pay-box">
          <h3>UPI</h3>
          <dl>
            <dt>UPI ID</dt><dd class="mono"><?= e(config('upi_id')) ?></dd>
            <dt>Name</dt><dd><?= e(config('upi_payee')) ?></dd>
            <dt>Amount</dt><dd><?= e(money((int)$order['amount'])) ?></dd>
            <dt>Note</dt><dd class="mono"><?= e($order['order_no']) ?></dd>
          </dl>
          <?php if ($qr): ?><img src="<?= e($qr) ?>" alt="UPI QR code" width="180" style="margin:8px 0"><?php endif; ?>
          <a class="btn btn-ghost btn-sm" href="<?= e(upi_link($order)) ?>">Open UPI app</a>
          <p class="muted small" style="margin-top:8px">The button works on a phone with a UPI app.</p>
        </div>
        <?php if (trim((string)config('bank_details'))): ?>
        <div class="pay-box">
          <h3>Bank transfer</h3>
          <p style="white-space:pre-line"><?= e((string)config('bank_details')) ?></p>
          <p class="muted small">Use <?= e($order['order_no']) ?> as the payment reference.</p>
        </div>
        <?php endif; ?>
      </div>

      <h3 style="margin-top:24px">After paying, enter the transaction ID</h3>
      <?php if ($error): ?><p class="alert alert-error"><?= e($error) ?></p><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?><input type="hidden" name="action" value="payment">
        <label>Transaction ID / UTR <span class="hint">12 digits for UPI, shown in your payment app</span>
          <input name="payment_ref" value="<?= e((string)$order['payment_ref']) ?>" required></label>
        <button class="btn btn-primary" type="submit">I have paid</button>
      </form>
    </div>
  <?php endif; ?>
<?php endif; ?>
  </div>
</section>
<?php page_footer();
