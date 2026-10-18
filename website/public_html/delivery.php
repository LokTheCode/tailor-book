<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$p = config('product_name');

policy_page('Delivery Policy', "{$p} is delivered digitally. Nothing is shipped.", function () use ($p) { ?>

<h2>How you receive <?= e($p) ?></h2>
<ol>
  <li>You place an order and pay by UPI or bank transfer, then enter the transaction ID on your order page.</li>
  <li>We confirm the payment, usually within one working day.</li>
  <li>Your license key is emailed to you and shown on your order page.</li>
  <li>You download the installer from our <a href="/download.php">download page</a> with your email and license key.</li>
</ol>
<p>There is no physical product and no shipping charge. Delivery is complete when your license key is issued.</p>

<h2>Didn't get your license key?</h2>
<ul>
  <li>Check your spam or junk folder for an email from <?= e(config('mail_from')) ?>.</li>
  <li>Open your <a href="/order.php">order page</a> with your order number and email; your key appears there once issued.</li>
  <li>Still nothing after 2 working days? <a href="/contact.php">Contact us</a> with your order number.</li>
</ul>
<?php });
