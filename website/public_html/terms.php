<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$p = config('product_name');
$biz = config('business_name');
$months = (int)config('free_support_months', 3);

policy_page('Terms of Service', "The terms for buying and using {$p}, including the software license.", function () use ($p, $biz, $months) { ?>

<div class="notice">
  <strong>In short:</strong> you pay once and may use <?= e($p) ?> on one computer for your business, for as long as you like.
  Please don't share or resell your license key. Support is free for <?= $months ?> months. All sales are final.
</div>

<p>These terms are an agreement between you (the buyer) and <?= e($biz) ?> ("we", "us"). By placing an order, downloading or using
<?= e($p) ?>, you agree to them.</p>

<h2>1. The license</h2>
<p>When your payment is confirmed, we give you a license key. It lets you install and use <?= e($p) ?> on <strong>one computer</strong>
for your business, with no time limit (a "perpetual" license). The license is personal to you: it is non-exclusive and you may not
transfer it to another person or business without our written permission.</p>
<p>You buy a license to use the software, not the software itself. <?= e($biz) ?> keeps all rights, including copyright, in <?= e($p) ?>.</p>

<h2>2. Activation and changing computers</h2>
<ul>
  <li>Your key activates on the first computer you enter it on. Reinstalling on the same computer works with the same key.</li>
  <li>If you replace your computer, contact us and we will move the license to the new one. The old computer then stops working with that key.</li>
  <li><?= e($p) ?> connects to our server to activate, and about once a week to check the license and look for updates. It works
      offline between checks.</li>
  <li>To use <?= e($p) ?> on more computers, buy one license for each.</li>
</ul>

<h2>3. What you may not do</h2>
<ul>
  <li>Share, publish, sell or rent your license key or the software.</li>
  <li>Try to get around activation, or copy, decompile, reverse engineer or change the software.</li>
  <li>Remove our name, logo or copyright notices from the software.</li>
  <li>Use the software for anything unlawful, including sending spam or messages people have not agreed to receive.</li>
</ul>
<p>If you break these rules, we may deactivate your license without a refund.</p>

<h2>4. Updates and new features</h2>
<p>We may release updates that fix problems or improve features that already exist. These are free to download with your license key.
New features, modules or changes made for your shop are not included in the price. We decide whether to build them, and they may be
charged separately.</p>

<h2>5. Support</h2>
<p>Free support for <?= $months ?> months, and what it covers, is described in our <a href="/support-policy.php">Support Policy</a>.</p>

<h2>6. Your data and backups</h2>
<p>Your shop's data is stored on your computer, not with us. You are responsible for it, for keeping backups (<?= e($p) ?> can make them
automatically), and for having your customers' permission to store their details and send them messages. We cannot recover data from
your computer if it is lost and you have no backup.</p>

<h2>7. Third-party services</h2>
<p>Features such as WhatsApp messages (through AiSensy) and email use services you sign up for yourself. Their terms, charges and
availability are between you and them. We are not responsible for them.</p>

<h2>8. Price and payment</h2>
<p>The price shown when you order is the price you pay<?= config('price_includes_gst') ? ', including GST' : '' ?>. We may change prices for
future buyers; this does not affect licenses already bought.</p>

<h2>9. Refunds</h2>
<p>All sales are final. Please read our <a href="/refund.php">Refund &amp; Cancellation Policy</a> before you buy.</p>

<h2>10. Warranty and liability</h2>
<p>We build <?= e($p) ?> with care and fix problems reported during the support period, but we cannot promise it will be free of all errors
or suit every business. To the extent the law allows, the software is provided "as is", and our total liability to you for any claim is
limited to the amount you paid for the license. We are not liable for indirect losses such as lost profit or lost data.</p>

<h2>11. Ending the license</h2>
<p>You may stop using <?= e($p) ?> at any time. We may end your license if you seriously break these terms. Sections 3, 6, 10 and 12 continue
to apply after it ends.</p>

<h2>12. Law and disputes</h2>
<p>These terms are governed by the laws of India. We will first try to settle any dispute by talking to you. If that fails, the courts at
<?= e(config('jurisdiction_city')) ?> have jurisdiction.</p>

<h2>13. Contact</h2>
<p><?= e($biz) ?>, <?= e(config('business_address')) ?><br>
<a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a> · <?= e(config('business_phone')) ?></p>
<?php });
