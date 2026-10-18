<?php
/* Shared by the desktop-app API endpoints: JSON in, JSON out. */
require dirname(__DIR__) . '/inc/bootstrap.php';
require dirname(__DIR__) . '/inc/orders.php';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function respond(array $data, int $code = 200): void {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function fail(string $code, string $message, int $http = 400): void {
    respond(['ok' => false, 'error' => $code, 'message' => $message], $http);
}

if (!is_installed()) fail('not_ready', 'The license server is not set up yet.', 503);

/** JSON body (or form fields) as an array. */
function input(): array {
    $raw = file_get_contents('php://input') ?: '';
    $data = json_decode($raw, true);
    return is_array($data) ? $data : $_POST;
}

function require_post(): void {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('method', 'Use POST.', 405);
}

function clean_machine_id($value): string {
    $value = strtolower((string)$value);
    return preg_match('/^[a-f0-9]{32,64}$/', $value) ? $value : '';
}

function clean_text($value, int $max): string {
    return mb_substr(trim(preg_replace('/[\x00-\x1F\x7F]/u', '', (string)$value)), 0, $max);
}
