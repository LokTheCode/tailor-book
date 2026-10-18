<?php
/* Order and license helpers shared by the public pages and the admin panel. */

const INDIAN_STATES = [
    'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
    'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
    'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
    'West Bengal', 'Outside India',
];

const ORDER_STATUS_LABELS = [
    'awaiting_payment' => 'Waiting for payment',
    'payment_submitted' => 'Payment being checked',
    'paid' => 'Paid - license issued',
    'rejected' => 'Payment not received',
];

function order_status_label(string $status): string {
    return ORDER_STATUS_LABELS[$status] ?? ucfirst(str_replace('_', ' ', $status));
}

function find_order(string $orderNo): ?array {
    $q = db()->prepare('SELECT * FROM orders WHERE order_no = ?');
    $q->execute([strtoupper(trim($orderNo))]);
    return $q->fetch() ?: null;
}

function order_license(int $orderId): ?array {
    $q = db()->prepare('SELECT * FROM licenses WHERE order_id = ? ORDER BY id DESC LIMIT 1');
    $q->execute([$orderId]);
    return $q->fetch() ?: null;
}

function find_license(string $key): ?array {
    $key = normalize_key($key);
    if ($key === '') return null;
    $q = db()->prepare('SELECT * FROM licenses WHERE license_key = ?');
    $q->execute([$key]);
    return $q->fetch() ?: null;
}

/** Orders this visitor may see without typing their email again. */
function remember_order(string $orderNo): void {
    start_session();
    $_SESSION['orders'] = array_unique(array_merge($_SESSION['orders'] ?? [], [$orderNo]));
}

function can_view_order(string $orderNo): bool {
    start_session();
    return in_array($orderNo, $_SESSION['orders'] ?? [], true);
}

function upi_link(array $order): string {
    return 'upi://pay?' . http_build_query([
        'pa' => config('upi_id'),
        'pn' => config('upi_payee'),
        'am' => number_format((float)$order['amount'], 2, '.', ''),
        'cu' => 'INR',
        'tn' => config('product_name') . ' ' . $order['order_no'],
    ], '', '&', PHP_QUERY_RFC3986);
}

/** Mark an order paid and create its license. Returns the license. */
function issue_license(array $order): array {
    $existing = order_license((int)$order['id']);
    if ($existing) return $existing;

    $pdo = db();
    $pdo->beginTransaction();
    $key = new_license_key();
    $pdo->prepare('INSERT INTO licenses (license_key, order_id, name, shop_name, email, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)')
        ->execute([$key, $order['id'], $order['name'], $order['shop_name'], $order['email'], 'active', now()]);
    $pdo->prepare("UPDATE orders SET status = 'paid', updated_at = ? WHERE id = ?")->execute([now(), $order['id']]);
    $pdo->commit();

    $license = find_license($key);
    email_license($order, $license);
    audit('license_issued', "{$order['order_no']} -> {$key}");
    return $license;
}

function email_license(array $order, array $license): bool {
    $product = config('product_name');
    $support = (int)config('free_support_months', 3);
    $body = "Hello {$order['name']},\n\n"
        . "Thank you for buying {$product}. Your payment for order {$order['order_no']} is confirmed.\n\n"
        . "Your license key:\n\n    {$license['license_key']}\n\n"
        . "Next steps:\n"
        . "1. Download the installer: " . site_url('download.php') . "\n"
        . "   (enter this email address and your license key)\n"
        . "2. Install {$product} and open it.\n"
        . "3. Enter your license key when asked. It activates on this one computer.\n\n"
        . "Keep this email safe. You will need the key if you reinstall Windows.\n\n"
        . "Free support for {$support} months: " . config('business_phone') . " / " . config('business_email') . "\n\n"
        . config('business_name') . "\n";
    return send_mail($order['email'], "Your {$product} license key ({$order['order_no']})", $body);
}

function email_order_received(array $order): void {
    $product = config('product_name');
    $body = "Hello {$order['name']},\n\n"
        . "We have received your order {$order['order_no']} for {$product} (" . money((int)$order['amount']) . ").\n\n"
        . "To complete it, pay by UPI to " . config('upi_id') . " (" . config('upi_payee') . ")"
        . (config('bank_details') ? " or by bank transfer:\n" . config('bank_details') . "\n" : ".\n")
        . "\nThen enter the transaction ID (UTR) on your order page:\n" . site_url('order.php') . "\n"
        . "(order number {$order['order_no']} and this email address)\n\n"
        . "We will email your license key as soon as the payment is confirmed.\n\n"
        . config('business_name') . "\n";
    send_mail($order['email'], "Order {$order['order_no']} received - {$product}", $body);

    $admin = (string)config('admin_notify_email');
    if ($admin) {
        send_mail($admin, "New order {$order['order_no']} - {$order['shop_name']}",
            "New order {$order['order_no']}\n{$order['name']} / {$order['shop_name']}\n{$order['phone']} / {$order['email']}\n"
            . "{$order['city']}, {$order['state']}\nAmount: " . money((int)$order['amount']) . "\n\n" . site_url('admin/orders.php'));
    }
}
