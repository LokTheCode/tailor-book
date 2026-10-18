<?php
/*
 * POST {"key", "machine_id"} from an activated app
 * -> {"ok": true, "url": "https://.../download.php?t=..."}  (valid 30 minutes)
 */
require __DIR__ . '/_api.php';
require_post();

if (!rate_limit('download_link', 20, 3600)) fail('rate_limited', 'Too many requests. Please try again later.', 429);

$in = input();
$license = find_license((string)($in['key'] ?? ''));
$machine = clean_machine_id($in['machine_id'] ?? '');

if (!$license || $license['status'] !== 'active') fail('invalid_key', 'This license is not active.', 403);
if (!$license['machine_id'] || !hash_equals($license['machine_id'], $machine)) {
    fail('wrong_machine', 'This license is activated on another computer.', 403);
}
if (!latest_release()) fail('no_release', 'No installer is available yet.', 404);

$token = bin2hex(random_bytes(20));
db()->prepare('INSERT INTO download_tokens (token, license_id, expires_at) VALUES (?, ?, ?)')
    ->execute([$token, $license['id'], time() + 1800]);

respond(['ok' => true, 'url' => site_url('download.php?t=' . $token)]);
