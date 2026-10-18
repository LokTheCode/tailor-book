<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$p = config('product_name');
$biz = config('business_name');

policy_page('Privacy Policy', "How {$biz} collects, uses and protects your personal data, and your rights under India's Digital Personal Data Protection Act, 2023.", function () use ($p, $biz) { ?>

<div class="notice">
  <strong>In short:</strong> we collect only what we need to sell you <?= e($p) ?>, deliver your license and support you.
  We do not sell your data or use it for advertising. Your shop's data inside <?= e($p) ?> (your customers, measurements
  and orders) stays on your computer and is never sent to us.
</div>

<h2>1. Who we are</h2>
<p><?= e($biz) ?> ("we", "us") sells the <?= e($p) ?> software and runs this website. We decide how and why your personal
data is used, so we are the <em>Data Fiduciary</em> under the Digital Personal Data Protection Act, 2023 (DPDP Act).</p>
<p>Address: <?= e(config('business_address')) ?><br>Email: <a href="mailto:<?= e(config('business_email')) ?>"><?= e(config('business_email')) ?></a> · Phone: <?= e(config('business_phone')) ?></p>

<h2>2. What we collect and why</h2>
<table>
  <tr><th>Personal data</th><th>When</th><th>What we use it for</th></tr>
  <tr><td>Name, shop name, mobile number, email, city, state, GSTIN (optional)</td><td>When you place an order</td>
      <td>To process your order, issue an invoice, email your license key, give you support, and tell you about updates to the software you bought.</td></tr>
  <tr><td>Payment transaction ID (UTR)</td><td>When you report a payment</td>
      <td>To match your payment with your order. We never ask for or store card numbers, UPI PINs or bank passwords.</td></tr>
  <tr><td>License key, a computer ID, computer name, app version, IP address</td><td>When you activate <?= e($p) ?> and when it checks for updates (about once a week)</td>
      <td>To make each license work on one computer, stop misuse of keys, and tell you about new versions. The computer ID is a one-way code made from your Windows installation; it does not reveal your files or data.</td></tr>
  <tr><td>Download records (license, time, IP address)</td><td>When you download the installer</td>
      <td>To limit downloads per license and stop keys being shared.</td></tr>
  <tr><td>Name, email, mobile (optional), your message</td><td>When you use the contact form</td>
      <td>To reply to you.</td></tr>
  <tr><td>Technical data (IP address, browser type)</td><td>When you visit the website</td>
      <td>To keep the website secure and working. Collected by our hosting provider's server logs.</td></tr>
</table>
<p>We collect personal data only from you, and only with your consent (given by ticking the box on our forms), or where the law allows us to without consent.</p>

<h2>3. Your shop's data inside <?= e($p) ?></h2>
<p><?= e($p) ?> stores everything you enter, such as your customers' names, mobile numbers, measurements, photos and orders,
<strong>only on your own computer</strong>. We do not receive, see or store it. For your customers' data, <em>you</em> are the Data Fiduciary
and are responsible for collecting it lawfully.</p>
<p>If you turn on WhatsApp or email messages in <?= e($p) ?>, messages go directly from your computer through the services you set up
(for example your own AiSensy account or email account). Those services' own privacy policies apply.</p>

<h2>4. Who we share data with</h2>
<p>We do not sell or rent your personal data. We share it only as needed with:</p>
<ul>
  <li><strong>Our hosting provider</strong> (Hostinger), which stores this website and its database.</li>
  <li><strong>Our email service</strong>, to send order and license emails.</li>
  <li><strong>A payment gateway</strong>, if we add online payments in future. This policy will be updated before that happens.</li>
  <li><strong>Government or law enforcement authorities</strong>, when the law requires it.</li>
</ul>

<h2>5. How long we keep it</h2>
<ul>
  <li><strong>Orders and invoices:</strong> for as long as tax and accounting laws require (usually 6 to 8 years). After that they are deleted.</li>
  <li><strong>License and activation records:</strong> while your license exists, so it keeps working, plus 1 year.</li>
  <li><strong>Download, activation and security logs:</strong> 1 year, as required by the DPDP Rules, then deleted.</li>
  <li><strong>Contact messages:</strong> up to 1 year after we last reply.</li>
</ul>

<h2>6. How we protect it</h2>
<p>The website uses HTTPS encryption. The database and license keys are stored outside the public part of the website, the admin area is
protected by a password and login limits, and only we can access your data. If a personal data breach happens, we will inform the Data
Protection Board of India and you as the DPDP Act requires.</p>

<h2>7. Your rights</h2>
<p>Under the DPDP Act you can:</p>
<ul>
  <li><strong>Access:</strong> ask what personal data we hold about you and how we use it.</li>
  <li><strong>Correct and update:</strong> ask us to fix or complete wrong or old data.</li>
  <li><strong>Erase:</strong> ask us to delete your data. We will delete what we no longer need by law; your license key keeps working.</li>
  <li><strong>Withdraw consent:</strong> at any time, as easily as you gave it, by emailing us. We will then stop using your data,
      except records the law requires us to keep. We may no longer be able to give you support or update notices.</li>
  <li><strong>Nominate:</strong> name another person to use these rights for you if you die or become unable to.</li>
  <li><strong>Complain:</strong> raise a grievance with us (below), and if you are not satisfied, with the
      <a href="https://www.dpb.gov.in" target="_blank" rel="noopener">Data Protection Board of India</a>.</li>
</ul>
<p>To use any of these rights, email our Grievance Officer from the email address you used with us. We reply within 30 days.</p>

<h2>8. Grievance Officer</h2>
<p><?= e(config('grievance_officer_name')) ?><br>
Email: <a href="mailto:<?= e(config('grievance_officer_email')) ?>"><?= e(config('grievance_officer_email')) ?></a><br>
Address: <?= e(config('business_address')) ?></p>

<h2>9. Cookies</h2>
<p>This website uses only one cookie: a session cookie that keeps forms secure and remembers your order page while you browse.
We do not use advertising or tracking cookies or analytics. If we show a YouTube video, it loads only when you click play, and then
YouTube's privacy policy applies.</p>

<h2>10. Children</h2>
<p><?= e($p) ?> is for businesses. We do not knowingly collect personal data of anyone under 18.</p>

<h2>11. Changes</h2>
<p>If we change this policy, we will update the date at the top and, for important changes, email customers.</p>
<?php });
