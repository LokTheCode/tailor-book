<?php
/* Shared by every admin page: login check and the admin menu. */
require dirname(__DIR__) . '/inc/bootstrap.php';
require dirname(__DIR__) . '/inc/layout.php';
require dirname(__DIR__) . '/inc/orders.php';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: private, no-store');

if (!is_installed()) redirect('/setup.php');
start_session();

function current_admin(): ?array {
    if (empty($_SESSION['admin_id'])) return null;
    // Sign out after 8 hours of inactivity
    if (time() - ($_SESSION['admin_seen'] ?? 0) > 8 * 3600) { unset($_SESSION['admin_id']); return null; }
    $_SESSION['admin_seen'] = time();
    $q = db()->prepare('SELECT id, username FROM admins WHERE id = ?');
    $q->execute([$_SESSION['admin_id']]);
    return $q->fetch() ?: null;
}

if (!defined('ADMIN_PUBLIC') && !current_admin()) redirect('/admin/login.php');

function admin_header(string $title, string $active): void {
    page_header("Admin: {$title}");
    $counts = db()->query("SELECT
        (SELECT COUNT(*) FROM orders WHERE status = 'payment_submitted') AS to_check,
        (SELECT COUNT(*) FROM messages WHERE is_read = 0) AS unread")->fetch();
    $items = [
        'dashboard' => ['/admin/', 'Dashboard'],
        'orders'    => ['/admin/orders.php', 'Orders' . ($counts['to_check'] ? " ({$counts['to_check']} to check)" : '')],
        'licenses'  => ['/admin/licenses.php', 'Licenses'],
        'releases'  => ['/admin/releases.php', 'Releases'],
        'messages'  => ['/admin/messages.php', 'Messages' . ($counts['unread'] ? " ({$counts['unread']})" : '')],
        'account'   => ['/admin/account.php', 'Account'],
    ];
    echo '<section class="page-hero" style="padding-bottom:0"><div class="wrap"><h1>' . e($title) . '</h1>';
    echo '<nav class="admin-nav" aria-label="Admin">';
    foreach ($items as $key => [$href, $label]) {
        echo '<a href="' . e(url($href)) . '"' . ($key === $active ? ' aria-current="page"' : '') . '>' . e($label) . '</a>';
    }
    echo '<a href="' . e(url('admin/logout.php')) . '">Log out</a></nav></div></section>';
    echo '<section class="section" style="padding-top:8px"><div class="wrap">';
}

function admin_footer(): void {
    echo '</div></section>';
    page_footer();
}

function back(string $fallback = '/admin/'): void {
    $to = $_POST['back'] ?? $fallback;
    if (is_string($to) && BASE !== '' && str_starts_with($to, BASE . '/')) $to = substr($to, strlen(BASE));
    redirect(is_string($to) && str_starts_with($to, '/admin/') ? $to : $fallback);
}
