<?php
require __DIR__ . '/_admin.php';

$s = db()->query("SELECT
    (SELECT COUNT(*) FROM orders WHERE status = 'payment_submitted') AS to_check,
    (SELECT COUNT(*) FROM orders WHERE status = 'awaiting_payment') AS awaiting,
    (SELECT COUNT(*) FROM orders WHERE status = 'paid') AS paid,
    (SELECT COALESCE(SUM(amount), 0) FROM orders WHERE status = 'paid') AS revenue,
    (SELECT COUNT(*) FROM licenses WHERE status = 'active' AND machine_id IS NOT NULL) AS activated,
    (SELECT COUNT(*) FROM licenses WHERE status = 'active' AND machine_id IS NULL) AS not_activated,
    (SELECT COUNT(*) FROM downloads WHERE created_at >= datetime('now', '-30 days')) AS downloads_30d
")->fetch();
$release = latest_release();
$recent = db()->query('SELECT * FROM orders ORDER BY id DESC LIMIT 8')->fetchAll();

admin_header('Dashboard', 'dashboard');
?>
<?php if ($s['to_check']): ?>
  <p class="alert alert-info"><strong><?= (int)$s['to_check'] ?> payment<?= $s['to_check'] > 1 ? 's' : '' ?> to check.</strong>
    Match the transaction ID in your bank / UPI app, then approve. <a href="/admin/orders.php?status=payment_submitted">Check payments</a></p>
<?php endif; ?>
<?php if (!$release): ?>
  <p class="alert alert-error">No installer uploaded yet, so customers can't download. <a href="/admin/releases.php">Upload one</a></p>
<?php endif; ?>

<div class="stats">
  <div class="stat"><b><?= (int)$s['to_check'] ?></b><span>Payments to check</span></div>
  <div class="stat"><b><?= (int)$s['awaiting'] ?></b><span>Waiting for payment</span></div>
  <div class="stat"><b><?= (int)$s['paid'] ?></b><span>Licenses sold</span></div>
  <div class="stat"><b><?= e(money((int)$s['revenue'])) ?></b><span>Revenue</span></div>
  <div class="stat"><b><?= (int)$s['activated'] ?></b><span>Activated</span></div>
  <div class="stat"><b><?= (int)$s['not_activated'] ?></b><span>Not activated yet</span></div>
  <div class="stat"><b><?= (int)$s['downloads_30d'] ?></b><span>Downloads (30 days)</span></div>
  <div class="stat"><b><?= $release ? e($release['version']) : '-' ?></b><span>Latest version</span></div>
</div>

<h2>Recent orders</h2>
<div class="table-wrap">
<table class="data">
  <tr><th>Order</th><th>Customer</th><th>Phone</th><th>Amount</th><th>Status</th><th>Date</th></tr>
  <?php foreach ($recent as $o): ?>
    <tr>
      <td><a href="/admin/order.php?id=<?= (int)$o['id'] ?>"><?= e($o['order_no']) ?></a></td>
      <td><?= e($o['name']) ?><br><span class="muted small"><?= e($o['shop_name']) ?></span></td>
      <td><?= e($o['phone']) ?></td>
      <td><?= e(money((int)$o['amount'])) ?></td>
      <td><span class="status status-<?= e($o['status']) ?>"><?= e(order_status_label($o['status'])) ?></span></td>
      <td><?= e(nice_datetime($o['created_at'])) ?></td>
    </tr>
  <?php endforeach; ?>
  <?php if (!$recent): ?><tr><td colspan="6" class="muted">No orders yet. Share your website link to get your first sale.</td></tr><?php endif; ?>
</table>
</div>
<?php admin_footer();
