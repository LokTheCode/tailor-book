<?php
/*
 * POST {"key": "TB-...", "machine_id": "<hex>", "machine_name": "...", "app_version": "1.1.0"}
 * A key activates on ONE computer. Activating again on the same computer
 * (e.g. after reinstalling) works; another computer is refused until an
 * admin moves the license (Admin > Licenses > Move to new PC).
 */
require __DIR__ . '/_api.php';
require_post();

if (!rate_limit('activate', 20, 3600)) fail('rate_limited', 'Too many attempts. Please try again in an hour.', 429);

$in = input();
$license = find_license((string)($in['key'] ?? ''));
$machine = clean_machine_id($in['machine_id'] ?? '');
$machineName = clean_text($in['machine_name'] ?? '', 80);
$version = clean_text($in['app_version'] ?? '', 20);

if ($machine === '') fail('bad_request', 'Missing computer ID. Please update the app.');
if (!$license) fail('invalid_key', 'This license key is not valid. Check it and try again.', 404);
if ($license['status'] !== 'active') fail('revoked', 'This license has been deactivated. Please contact support.', 403);

if ($license['machine_id'] && !hash_equals($license['machine_id'], $machine)) {
    fail('in_use', 'This license key is already activated on another computer. '
        . 'Each key works on one computer. To move it to this computer, contact support.', 409);
}

$first = !$license['machine_id'];
db()->prepare('UPDATE licenses SET machine_id = ?, machine_name = ?, app_version = ?, activated_at = COALESCE(activated_at, ?),
               last_seen_at = ?, activations = activations + 1 WHERE id = ?')
    ->execute([$machine, $machineName, $version, now(), now(), $license['id']]);
audit($first ? 'activated' : 'reactivated', "{$license['license_key']} on {$machineName}");

$token = sign_license([
    'p' => 'tailorbook',
    'v' => 1,
    'k' => $license['license_key'],
    'm' => $machine,
    'n' => $license['name'],
    's' => (string)$license['shop_name'],
    'e' => $license['email'],
    'i' => date('Y-m-d'),
]);

respond([
    'ok' => true,
    'token' => $token,
    'license' => ['name' => $license['name'], 'shop' => $license['shop_name'], 'email' => $license['email']],
]);
