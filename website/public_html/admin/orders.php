<?php
require __DIR__ . '/_admin.php';

// ---- Add a sale by hand (cash, cheque, or a license for your own shop)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && post('action') === 'manual') {
    csrf_check();
    $name = post('name'); $shop = post('shop_name'); $email = strtolower(post('email'));
    $phone = preg_replace('/\D/', '', post('phone'));
    $amount = max(0, (int)post('amount'));
    if (mb_strlen($name) < 2 || mb_strlen($shop) < 2 || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($phone) < 10) {
        flash('Fill in name, shop, a valid email and a 10-digit mobile.', 'error');
        redirect('/admin/orders.php');
    }
    $orderNo = new_order_no();
    db()->prepare('INSERT INTO orders (order_no, name, shop_name, phone, email, city, state, amount, status, payment_ref,
                   admin_note, consent_at, consent_ip, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        ->execute([$orderNo, $name, $shop, $phone, $email, post('city'), post('state'), $amount, 'awaiting_payment',
                   post('payment_ref') ?: 'MANUAL', 'Added by admin', now(), 'admin', now(), now()]);
    $license = issue_license(find_order($orderNo));
    flash("Order {$orderNo} created and license {$license['license_key']} emailed to {$email}.");
    redirect('/admin/orders.php?status=paid');
}

$filters = [
    'payment_submitted' => 'To check',
    'awaiting_payment' => 'Waiting for payment',
    'paid' => 'Paid',
    'rejected' => 'Rejected',
    'all' => 'All',
];
$status = $_GET['status'] ?? 'payment_submitted';
if (!isset($filters[$status])) $status = 'all';
$search = trim((string)($_GET['q'] ?? ''));

$sql = 'SELECT * FROM orders WHERE 1=1';
$args = [];
if ($status !== 'all') { $sql .= ' AND status = ?'; $args[] = $status; }
if ($search !== '') {
    $sql .= ' AND (order_no LIKE ? OR name LIKE ? OR shop_name LIKE ? OR phone LIKE ? OR email LIKE ? OR payment_ref LIKE ?)';
    array_push($args, ...array_fill(0, 6, "%{$search}%"));
}
$sql .= ' ORDER BY id DESC LIMIT 200';
$q = db()->prepare($sql);
$q->execute($args);
$orders = $q->fetchAll();

admin_header('Orders', 'orders');
?>
<form method="get" class="actions" style="margin-bottom:16px">
  <?php foreach ($filters as $key => $label): ?>
    <a class="btn btn-sm <?= $key === $status ? 'btn-primary' : 'btn-ghost' ?>" href="?status=<?= e($key) ?>"><?= e($label) ?></a>
  <?php endforeach; ?>
  <input type="hidden" name="status" value="<?= e($status) ?>">
  <input name="q" value="<?= e($search) ?>" placeholder="Search name, phone, order, UTR" style="max-width:280px">
  <button class="btn btn-ghost btn-sm">Search</button>
</form>

<div class="table-wrap">
<table class="data">
  <tr><th>Order</th><th>Customer</th><th>Contact</th><th>Amount</th><th>Transaction ID</th><th>Status</th><th>Date</th></tr>
  <?php foreach ($orders as $o): ?>
    <tr>
      <td><a href="<?= BASE ?>/admin/order.php?id=<?= (int)$o['id'] ?>"><?= e($o['order_no']) ?></a></td>
      <td><?= e($o['name']) ?><br><span class="muted small"><?= e($o['shop_name']) ?>, <?= e($o['city']) ?></span></td>
      <td><?= e($o['phone']) ?><br><span class="muted small"><?= e($o['email']) ?></span></td>
      <td><?= e(money((int)$o['amount'])) ?></td>
      <td class="mono"><?= e($o['payment_ref'] ?: '-') ?></td>
      <td><span class="status status-<?= e($o['status']) ?>"><?= e(order_status_label($o['status'])) ?></span></td>
      <td><?= e(nice_datetime($o['created_at'])) ?></td>
    </tr>
  <?php endforeach; ?>
  <?php if (!$orders): ?><tr><td colspan="7" class="muted">No orders here.</td></tr><?php endif; ?>
</table>
</div>

<div class="card" style="margin-top:32px">
  <h2>Add a sale by hand</h2>
  <p class="muted">For cash or cheque payments, or a license for your own shop. The license is created and emailed straight away.</p>
  <form method="post" class="form">
    <?= csrf_field() ?><input type="hidden" name="action" value="manual">
    <div class="form-grid">
      <label>Name <input name="name" required></label>
      <label>Shop name <input name="shop_name" required></label>
      <label>Mobile <input name="phone" required></label>
      <label>Email <input name="email" type="email" required></label>
      <label>City <input name="city"></label>
      <label>State <select name="state"><option value=""></option><?php foreach (INDIAN_STATES as $st): ?><option><?= e($st) ?></option><?php endforeach; ?></select></label>
      <label>Amount received (₹) <input name="amount" type="number" min="0" value="<?= (int)config('price_inr') ?>"></label>
      <label>Payment reference <span class="hint">Cash, cheque no., etc.</span><input name="payment_ref" value="CASH"></label>
    </div>
    <button class="btn btn-primary" type="submit">Create order and send license</button>
  </form>
</div>
<?php admin_footer();
