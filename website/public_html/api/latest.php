<?php
/* GET -> the newest published version, for the app's "Update available" check. */
require __DIR__ . '/_api.php';

$release = latest_release();
if (!$release) respond(['ok' => true, 'version' => null]);

respond([
    'ok' => true,
    'version' => $release['version'],
    'released' => substr($release['created_at'], 0, 10),
    'notes' => (string)$release['notes'],
    'size_mb' => round($release['size'] / 1048576, 1),
    'download_page' => site_url('download.php'),
]);
