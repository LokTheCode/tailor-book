<?php
require __DIR__ . '/_admin.php';

$id = (int)($_GET['id'] ?? 0);
$q = db()->prepare('SELECT * FROM orders WHERE id = ?');
$q->execute([$id]);
$order = $q->fetch();
if (!$order) { flash('Order not found.', 'error'); redirect('/admin/orders.php'); }
$self = '/admin/order.php?id=' . $id;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    switch (post('action')) {
        case 'approve':
            $license = issue_license($order);
            flash("Payment approved. License {$license['license_key']} emailed to {$order['email']}.");
            break;
        case 'reject':
            db()->prepare("UPDATE orders SET status = 'rejected', admin_note = ?, updated_at = ? WHERE id = ?")
                ->execute([post('note') ?: null, now(), $id]);
            send_mail($order['email'], "Payment not found for order {$order['order_no']}",
                "Hello {$order['name']},\n\nWe could not find your payment for order {$order['order_no']}."
                . (post('note') ? "\n\n" . post('note') : '')
                . "\n\nPlease check the transaction ID on your order page or reply to this email:\n" . site_url('order.php') . "\n\n" . config('business_name'));
            audit('payment_rejected', $order['order_no']);
            flash('Order marked as payment not received. The customer has been emailed.');
            break;
        case 'resend':
            $license = order_license($id);
            if ($license) { email_license($order, $license); flash('License email sent again.'); }
            break;
        case 'erase':
            // DPDP: erase personal data on request; keep order number and amount for tax records
            db()->prepare("UPDATE orders SET name = 'Erased', shop_name = 'Erased', phone = '-', email = ?, city = NULL,
                           state = NULL, gstin = NULL, consent_ip = NULL, admin_note = 'Personal data erased on request',
                           updated_at = ? WHERE id = ?")
                ->execute(['erased-' . $id . '@invalid', now(), $id]);
            db()->prepare("UPDATE licenses SET name = 'Erased', shop_name = 'Erased', email = ?, machine_name = NULL WHERE order_id = ?")
                ->execute(['erased-' . $id . '@invalid', $id]);
            audit('personal_data_erased', $order['order_no']);
            flash('Personal data erased. The order number, amount and license key are kept for your accounts.');
            break;
    }
    redirect($self);
}

$license = order_license($id);
admin_header('Order ' . $order['order_no'], 'orders');
?>
<p><a href="<?= BASE ?>/admin/orders.php">&larr; All orders</a></p>
<div class="card">
  <p><span class="status status-<?= e($order['status']) ?>"><?= e(order_status_label($order['status'])) ?></span></p>
  <table class="data">
    <tr><th>Name</th><td><?= e($order['name']) ?></td></tr>
    <tr><th>Shop</th><td><?= e($order['shop_name']) ?></td></tr>
    <tr><th>Mobile</th><td><a href="tel:<?= e($order['phone']) ?>"><?= e($order['phone']) ?></a> · <a href="https://wa.me/91<?= e($order['phone']) ?>" target="_blank" rel="noopener">WhatsApp</a></td></tr>
    <tr><th>Email</th><td><a href="mailto:<?= e($order['email']) ?>"><?= e($order['email']) ?></a></td></tr>
    <tr><th>Place</th><td><?= e(trim($order['city'] . ', ' . $order['state'], ', ')) ?></td></tr>
    <?php if ($order['gstin']): ?><tr><th>GSTIN</th><td class="mono"><?= e($order['gstin']) ?></td></tr><?php endif; ?>
    <tr><th>Amount</th><td><?= e(money((int)$order['amount'])) ?></td></tr>
    <tr><th>Transaction ID</th><td class="mono"><?= e($order['payment_ref'] ?: '-') ?><?= $order['payment_submitted_at'] ? ' <span class="muted small">(' . e(nice_datetime($order['payment_submitted_at'])) . ')</span>' : '' ?></td></tr>
    <tr><th>Ordered</th><td><?= e(nice_datetime($order['created_at'])) ?></td></tr>
    <tr><th>Consent given</th><td><?= e(nice_datetime($order['consent_at'])) ?></td></tr>
    <?php if ($order['admin_note']): ?><tr><th>Note</th><td><?= e($order['admin_note']) ?></td></tr><?php endif; ?>
  </table>
</div>

<?php if ($license): ?>
<div class="card">
  <h2>License</h2>
  <p class="keybox"><?= e($license['license_key']) ?></p>
  <p>Status: <span class="status status-<?= e($license['status']) ?>"><?= e(ucfirst($license['status'])) ?></span>
    · <?= $license['machine_id'] ? 'Activated on ' . e($license['machine_name'] ?: 'a computer') . ' (' . e(nice_date($license['activated_at'])) . ')' : 'Not activated yet' ?></p>
  <div class="actions">
    <form method="post" class="inline-form"><?= csrf_field() ?><input type="hidden" name="action" value="resend"><button class="btn btn-ghost btn-sm">Email the key again</button></form>
    <a class="btn btn-ghost btn-sm" href="<?= BASE ?>/admin/licenses.php?q=<?= e(urlencode($license['license_key'])) ?>">Manage license</a>
  </div>
</div>
<?php elseif (in_array($order['status'], ['payment_submitted', 'awaiting_payment', 'rejected'], true)): ?>
<div class="card">
  <h2>Payment</h2>
  <p>Check that <strong><?= e(money((int)$order['amount'])) ?></strong> arrived<?= $order['payment_ref'] ? ' with transaction ID <strong class="mono">' . e($order['payment_ref']) . '</strong>' : '' ?> in your bank or UPI app.</p>
  <div class="actions">
    <form method="post" class="inline-form" onsubmit="return confirm('Approve this payment and email the license key?')">
      <?= csrf_field() ?><input type="hidden" name="action" value="approve">
      <button class="btn btn-ok">Payment received: send license</button>
    </form>
  </div>
  <form method="post" class="form" style="margin-top:20px">
    <?= csrf_field() ?><input type="hidden" name="action" value="reject">
    <label>Payment not found? Message to the customer <span class="hint">Optional</span>
      <input name="note" placeholder="e.g. The transaction ID does not match any payment."></label>
    <button class="btn btn-danger btn-sm">Payment not received</button>
  </form>
</div>
<?php endif; ?>

<div class="card">
  <h2>Privacy request</h2>
  <p class="muted">If this customer asks you to delete their data (DPDP Act), erase it here. The order number, amount and license key stay for your tax records; the license keeps working.</p>
  <form method="post" onsubmit="return confirm('Erase this customer\'s name, phone, email and address? This cannot be undone.')">
    <?= csrf_field() ?><input type="hidden" name="action" value="erase">
    <button class="btn btn-ghost btn-sm">Erase personal data</button>
  </form>
</div>
<?php admin_footer();
