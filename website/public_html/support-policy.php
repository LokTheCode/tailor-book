<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$p = config('product_name');
$months = (int)config('free_support_months', 3);

policy_page('Support Policy', "Free support for {$months} months after you buy {$p}, and what happens after that.", function () use ($p, $months) { ?>

<div class="notice">
  <strong>In short:</strong> for <?= $months ?> months after your license is issued, we help you for free with the features
  <?= e($p) ?> has today. After that, support is paid. New features are not part of support and are quoted separately.
</div>

<h2>Free support: first <?= $months ?> months</h2>
<p>Starts on the day your license key is issued. Included:</p>
<ul>
  <li>Help installing <?= e($p) ?> and activating your license.</li>
  <li>Answers to "how do I..." questions about existing features.</li>
  <li>Fixing bugs: anything that does not work as described on our website.</li>
  <li>Moving your license to a new computer.</li>
  <li>Help setting up WhatsApp (AiSensy) and email inside <?= e($p) ?>.</li>
</ul>

<h2>After <?= $months ?> months</h2>
<p><?= e($p) ?> keeps working: your license never expires. Support from us is then paid. <?= e(config('paid_support_note')) ?></p>
<p>Updates that fix problems in existing features stay free to download with your license key, whenever we release them.</p>

<h2>Not included in support</h2>
<ul>
  <li><strong>New features or changes</strong> made for your shop. Tell us what you need and we will give you a quote. We decide which features to build.</li>
  <li>Entering your data, or training staff beyond the basics.</li>
  <li>Problems with your computer, Windows, printer, antivirus or internet.</li>
  <li>Third-party services such as AiSensy, WhatsApp or your email provider, including their charges.</li>
  <li>Recovering data you deleted or lost without a backup.</li>
</ul>

<h2>How to get help</h2>
<ul>
  <li>Phone / WhatsApp: <?= e(config('business_phone')) ?></li>
  <li>Email: <a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a></li>
  <?php if (config('support_hours')): ?><li>Hours: <?= e(config('support_hours')) ?></li><?php endif; ?>
</ul>
<p>Please tell us your license key or order number, what you were doing, and what happened. A screenshot helps. We usually reply within
one working day.</p>
<?php });
