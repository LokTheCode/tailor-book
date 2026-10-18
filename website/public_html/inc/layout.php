<?php
/* Shared page header and footer. */

function page_header(string $title, string $description = '', string $active = '', bool $dark = false): void {
    $product = config('product_name', 'Tailor Book');
    $fullTitle = $title === $product ? "{$product} - " . config('tagline') : "{$title} | {$product}";
    $description = $description ?: config('tagline');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    $nav = [
        'features' => ['/#features', 'Features'],
        'pricing'  => ['/#pricing', 'Pricing'],
        'faq'      => ['/#faq', 'FAQ'],
        'download' => ['/download.php', 'Download'],
        'order'    => ['/order.php', 'Order status'],
    ];
    ?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($fullTitle) ?></title>
<meta name="description" content="<?= e($description) ?>">
<meta property="og:title" content="<?= e($fullTitle) ?>">
<meta property="og:description" content="<?= e($description) ?>">
<meta property="og:image" content="<?= e(site_url('assets/img/logo.png')) ?>">
<link rel="icon" type="image/png" href="<?= BASE ?>/assets/img/favicon.png">
<link rel="apple-touch-icon" href="<?= BASE ?>/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="<?= BASE ?>/assets/css/site.css?v=1">
</head>
<body class="<?= $dark ? 'page-dark' : 'page-light' ?>">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="wrap header-row">
    <a class="brand" href="<?= BASE ?>/" aria-label="<?= e($product) ?> home">
      <img src="<?= BASE ?>/assets/img/icon.png" alt="" width="36" height="36">
      <span><?= e($product) ?></span>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <nav id="site-nav" class="site-nav">
      <?php foreach ($nav as $key => [$href, $label]): ?>
        <a href="<?= e(url($href)) ?>"<?= $active === $key ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
      <?php endforeach; ?>
      <a class="btn btn-primary btn-sm" href="<?= BASE ?>/buy.php">Buy now</a>
    </nav>
  </div>
</header>
<main id="main">
<?php
    $flash = flash();
    if ($flash) {
        echo '<div class="wrap"><div class="alert alert-' . e($flash[0]) . '" role="status">' . e($flash[1]) . '</div></div>';
    }
}

function page_footer(): void {
    $product = config('product_name', 'Tailor Book');
    ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-footer" href="<?= BASE ?>/">
        <img src="<?= BASE ?>/assets/img/icon.png" alt="" width="32" height="32">
        <span><?= e($product) ?></span>
      </a>
      <p class="muted"><?= e(config('tagline')) ?>.<br>Windows desktop software for tailors and boutiques.</p>
    </div>
    <div>
      <h3>Product</h3>
      <a href="<?= BASE ?>/#features">Features</a>
      <a href="<?= BASE ?>/#pricing">Pricing</a>
      <a href="<?= BASE ?>/buy.php">Buy a license</a>
      <a href="<?= BASE ?>/download.php">Download</a>
      <a href="<?= BASE ?>/order.php">Order status</a>
    </div>
    <div>
      <h3>Policies</h3>
      <a href="<?= BASE ?>/privacy.php">Privacy Policy</a>
      <a href="<?= BASE ?>/terms.php">Terms of Service</a>
      <a href="<?= BASE ?>/refund.php">Refund &amp; Cancellation</a>
      <a href="<?= BASE ?>/support-policy.php">Support Policy</a>
      <a href="<?= BASE ?>/delivery.php">Delivery Policy</a>
    </div>
    <div>
      <h3>Contact</h3>
      <a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a>
      <a href="tel:<?= e(preg_replace('/\s+/', '', (string)config('business_phone'))) ?>"><?= e(config('business_phone')) ?></a>
      <a href="<?= BASE ?>/contact.php">Contact form</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <?= date('Y') ?> <?= e(config('business_name')) ?>. All rights reserved.</span>
    <span><?= e($product) ?> is sold by <?= e(config('business_name')) ?>.</span>
  </div>
</footer>
<script src="<?= BASE ?>/assets/js/site.js?v=1" defer></script>
</body>
</html>
<?php
}

/** A legal/policy page body wrapper. */
function policy_page(string $title, string $intro, callable $body): void {
    page_header($title, $intro);
    ?>
    <section class="page-hero">
      <div class="wrap narrow">
        <h1><?= e($title) ?></h1>
        <p class="lead"><?= e($intro) ?></p>
        <p class="muted small">Last updated: <?= e(nice_date((string)config('policies_updated'))) ?></p>
      </div>
    </section>
    <section class="section">
      <div class="wrap narrow prose">
        <?php $body(); ?>
      </div>
    </section>
    <?php
    page_footer();
}
