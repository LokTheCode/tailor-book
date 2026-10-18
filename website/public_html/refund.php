<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$p = config('product_name');

policy_page('Refund & Cancellation Policy', "{$p} is a digital product. All sales are final once your license key is issued.", function () use ($p) { ?>

<div class="notice">
  <strong>No refunds and no returns.</strong> <?= e($p) ?> is delivered instantly as a download with a license key, which cannot be
  returned. Once your license key has been issued, the sale is final.
</div>

<h2>Before you buy</h2>
<p>Please make sure <?= e($p) ?> suits your shop before you pay. Look at the features, screenshots and video on our website, check the
system requirements (Windows 10 or 11, 64-bit, 4 GB RAM), and <a href="<?= BASE ?>/contact.php">ask us any questions</a>. We are happy to help.</p>

<h2>Cancelling an order</h2>
<ul>
  <li><strong>Before you pay:</strong> simply don't pay. Unpaid orders are not charged and are deleted later.</li>
  <li><strong>After you pay, but before we issue your license key:</strong> email us with your order number and we will cancel the order
      and refund the full amount.</li>
  <li><strong>After your license key is issued:</strong> the order cannot be cancelled or refunded.</li>
</ul>

<h2>When we do refund</h2>
<p>Even after a key is issued, we refund in these cases:</p>
<ul>
  <li>You paid twice for the same order, or paid more than the order amount. We refund the extra amount.</li>
  <li>We could not deliver a working license key within 7 days of confirming your payment, and could not fix the problem.</li>
</ul>

<h2>What is not a reason for a refund</h2>
<ul>
  <li>Changing your mind, or no longer needing the software.</li>
  <li>Not using the software, or using it for less time than expected.</li>
  <li>Problems with your computer, Windows, printer or internet, or with third-party services such as AiSensy or your email provider.</li>
  <li>Wanting a feature that <?= e($p) ?> does not have. New features are quoted separately; see the <a href="<?= BASE ?>/support-policy.php">Support Policy</a>.</li>
  <li>Problems we can fix: if something does not work as described, contact us during your support period and we will fix it.</li>
</ul>

<h2>Paid support and custom work</h2>
<p>Payments for paid support after the free period, and for custom features, are also non-refundable once the work has started.</p>

<h2>How refunds are paid</h2>
<p>Approved refunds are paid back to the same UPI ID or bank account you paid from, within 7 working days.</p>

<h2>Contact</h2>
<p>Email <a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a> or call <?= e(config('business_phone')) ?> with your order number.</p>
<?php });
