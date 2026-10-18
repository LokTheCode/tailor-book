<?php
define('ADMIN_PUBLIC', true);
require __DIR__ . '/_admin.php';
$_SESSION = [];
session_destroy();
redirect('/admin/login.php');
