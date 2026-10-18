<?php
/*
 * POST {"key", "machine_id", "app_version"}  (the app calls this about once a week)
 * -> {"ok": true, "status": "active" | "revoked" | "moved" | "invalid"}
 * "moved" = the license now belongs to another computer.
 */
require __DIR__ . '/_api.php';
require_post();

if (!rate_limit('check', 120, 3600)) fail('rate_limited', 'Too many requests.', 429);

$in = input();
$license = find_license((string)($in['key'] ?? ''));
$machine = clean_machine_id($in['machine_id'] ?? '');

if (!$license) respond(['ok' => true, 'status' => 'invalid']);
if ($license['status'] !== 'active') respond(['ok' => true, 'status' => 'revoked']);
if (!$license['machine_id'] || !$machine || !hash_equals($license['machine_id'], $machine)) {
    respond(['ok' => true, 'status' => 'moved']);
}

db()->prepare('UPDATE licenses SET last_seen_at = ?, app_version = ? WHERE id = ?')
    ->execute([now(), clean_text($in['app_version'] ?? '', 20), $license['id']]);

respond(['ok' => true, 'status' => 'active']);
