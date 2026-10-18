<?php
require __DIR__ . '/_admin.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $id = (int)post('id');
    if (post('action') === 'read') db()->prepare('UPDATE messages SET is_read = 1 WHERE id = ?')->execute([$id]);
    if (post('action') === 'delete') db()->prepare('DELETE FROM messages WHERE id = ?')->execute([$id]);
    redirect('/admin/messages.php');
}

$messages = db()->query('SELECT * FROM messages ORDER BY is_read, id DESC LIMIT 300')->fetchAll();
admin_header('Messages', 'messages');
?>
<?php foreach ($messages as $m): ?>
  <div class="card"<?= $m['is_read'] ? ' style="opacity:.75"' : '' ?>>
    <p><strong><?= e($m['name']) ?></strong> · <a href="mailto:<?= e($m['email']) ?>"><?= e($m['email']) ?></a>
      <?= $m['phone'] ? ' · <a href="tel:' . e($m['phone']) . '">' . e($m['phone']) . '</a>' : '' ?>
      <span class="muted small"> · <?= e(nice_datetime($m['created_at'])) ?></span></p>
    <p style="white-space:pre-line"><?= e($m['message']) ?></p>
    <div class="actions">
      <?php if (!$m['is_read']): ?>
        <form method="post" class="inline-form"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$m['id'] ?>"><input type="hidden" name="action" value="read"><button class="btn btn-ghost btn-sm">Mark as read</button></form>
      <?php endif; ?>
      <form method="post" class="inline-form" onsubmit="return confirm('Delete this message?')"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$m['id'] ?>"><input type="hidden" name="action" value="delete"><button class="btn btn-ghost btn-sm">Delete</button></form>
    </div>
  </div>
<?php endforeach; ?>
<?php if (!$messages): ?><p class="muted">No messages yet.</p><?php endif; ?>
<?php admin_footer();
