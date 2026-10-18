<?php
require __DIR__ . '/_admin.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $q = db()->prepare('SELECT * FROM licenses WHERE id = ?');
    $q->execute([(int)post('id')]);
    $license = $q->fetch();
    if ($license) {
        switch (post('action')) {
            case 'move':
                // Free the key so it can be activated on the customer's new computer.
                // The old computer stops working at its next weekly online check.
                db()->prepare('UPDATE licenses SET machine_id = NULL, machine_name = NULL WHERE id = ?')->execute([$license['id']]);
                audit('license_moved', $license['license_key']);
                flash("{$license['license_key']} can now be activated on a new computer.");
                break;
            case 'revoke':
                db()->prepare("UPDATE licenses SET status = 'revoked' WHERE id = ?")->execute([$license['id']]);
                audit('license_revoked', $license['license_key']);
                flash("{$license['license_key']} deactivated. The app stops working at its next online check.");
                break;
            case 'restore':
                db()->prepare("UPDATE licenses SET status = 'active' WHERE id = ?")->execute([$license['id']]);
                audit('license_restored', $license['license_key']);
                flash("{$license['license_key']} is active again.");
                break;
        }
    }
    back('/admin/licenses.php');
}

$search = trim((string)($_GET['q'] ?? ''));
$sql = 'SELECT l.*, o.order_no, o.phone,
          (SELECT COUNT(*) FROM downloads d WHERE d.license_id = l.id) AS downloads
        FROM licenses l LEFT JOIN orders o ON o.id = l.order_id';
$args = [];
if ($search !== '') {
    $sql .= ' WHERE l.license_key LIKE ? OR l.name LIKE ? OR l.shop_name LIKE ? OR l.email LIKE ? OR o.phone LIKE ? OR o.order_no LIKE ?';
    $args = array_fill(0, 6, "%{$search}%");
}
$sql .= ' ORDER BY l.id DESC LIMIT 300';
$q = db()->prepare($sql);
$q->execute($args);
$licenses = $q->fetchAll();
$back = '/admin/licenses.php' . ($search !== '' ? '?q=' . urlencode($search) : '');

admin_header('Licenses', 'licenses');
?>
<form method="get" class="actions" style="margin-bottom:16px">
  <input name="q" value="<?= e($search) ?>" placeholder="Search key, name, shop, phone, email" style="max-width:340px">
  <button class="btn btn-ghost btn-sm">Search</button>
</form>
<p class="muted small">Each key works on one computer. If a customer changes computer, use <strong>Move to new PC</strong>, then they enter the same key on the new computer.</p>

<div class="table-wrap">
<table class="data">
  <tr><th>License key</th><th>Customer</th><th>Computer</th><th>Version</th><th>Last seen</th><th>Downloads</th><th>Status</th><th></th></tr>
  <?php foreach ($licenses as $l): ?>
    <tr>
      <td class="mono"><?= e($l['license_key']) ?><br><span class="muted small"><?= e($l['order_no'] ?? '') ?></span></td>
      <td><?= e($l['name']) ?><br><span class="muted small"><?= e($l['shop_name']) ?> · <?= e($l['phone'] ?? '') ?></span></td>
      <td><?= $l['machine_id'] ? e($l['machine_name'] ?: 'Activated') . '<br><span class="muted small">since ' . e(nice_date($l['activated_at'])) . '</span>' : '<span class="muted">Not activated</span>' ?></td>
      <td><?= e($l['app_version'] ?: '-') ?></td>
      <td><?= e(nice_date($l['last_seen_at'])) ?></td>
      <td><?= (int)$l['downloads'] ?></td>
      <td><span class="status status-<?= e($l['status']) ?>"><?= e(ucfirst($l['status'])) ?></span></td>
      <td>
        <div class="actions">
        <?php if ($l['machine_id']): ?>
          <form method="post" class="inline-form" onsubmit="return confirm('Free this key for a new computer? The old computer will stop working at its next online check.')">
            <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><input type="hidden" name="back" value="<?= e($back) ?>">
            <input type="hidden" name="action" value="move"><button class="btn btn-ghost btn-sm">Move to new PC</button>
          </form>
        <?php endif; ?>
        <?php if ($l['status'] === 'active'): ?>
          <form method="post" class="inline-form" onsubmit="return confirm('Deactivate this license? The app will stop working for this customer.')">
            <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><input type="hidden" name="back" value="<?= e($back) ?>">
            <input type="hidden" name="action" value="revoke"><button class="btn btn-ghost btn-sm">Deactivate</button>
          </form>
        <?php else: ?>
          <form method="post" class="inline-form">
            <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><input type="hidden" name="back" value="<?= e($back) ?>">
            <input type="hidden" name="action" value="restore"><button class="btn btn-ghost btn-sm">Reactivate</button>
          </form>
        <?php endif; ?>
        </div>
      </td>
    </tr>
  <?php endforeach; ?>
  <?php if (!$licenses): ?><tr><td colspan="8" class="muted">No licenses yet.</td></tr><?php endif; ?>
</table>
</div>
<?php admin_footer();
