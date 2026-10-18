<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/orders.php';

$product = config('product_name');
$price = (int)config('price_inr');
$errors = [];
$v = ['name' => '', 'shop_name' => '', 'phone' => '', 'email' => '', 'city' => '', 'state' => '', 'gstin' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    foreach ($v as $k => $_) $v[$k] = post($k);

    if (post('website') !== '') {                 // honeypot: bots fill hidden fields
        redirect('/');
    }
    if (mb_strlen($v['name']) < 2) $errors['name'] = 'Enter your full name.';
    if (mb_strlen($v['shop_name']) < 2) $errors['shop_name'] = 'Enter your shop name.';
    $digits = preg_replace('/\D/', '', $v['phone']);
    if (strlen($digits) === 12 && str_starts_with($digits, '91')) $digits = substr($digits, 2);
    if (!preg_match('/^[6-9]\d{9}$/', $digits)) $errors['phone'] = 'Enter a 10-digit mobile number.';
    else $v['phone'] = $digits;
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Enter a valid email address. Your license key is sent here.';
    if ($v['city'] === '') $errors['city'] = 'Enter your city.';
    if (!in_array($v['state'], INDIAN_STATES, true)) $errors['state'] = 'Choose your state.';
    $v['gstin'] = strtoupper(str_replace(' ', '', $v['gstin']));
    if ($v['gstin'] !== '' && !preg_match('/^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]$/', $v['gstin'])) {
        $errors['gstin'] = 'This does not look like a GSTIN. Leave it empty if you do not have one.';
    }
    if (empty($_POST['agree_terms'])) $errors['agree_terms'] = 'Please accept the Terms of Service and Privacy Policy.';
    if (empty($_POST['agree_refund'])) $errors['agree_refund'] = 'Please confirm you understand that all sales are final.';

    if (!$errors && !rate_limit('order', 5, 3600)) {
        $errors['form'] = 'Too many orders from this connection. Please try again in an hour or contact us.';
    }

    if (!$errors) {
        $orderNo = new_order_no();
        db()->prepare('INSERT INTO orders (order_no, name, shop_name, phone, email, city, state, gstin, amount, status,
                       consent_at, consent_ip, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
            ->execute([$orderNo, $v['name'], $v['shop_name'], $v['phone'], strtolower($v['email']), $v['city'],
                       $v['state'], $v['gstin'] ?: null, $price, 'awaiting_payment', now(), client_ip(), now(), now()]);
        $order = find_order($orderNo);
        email_order_received($order);
        remember_order($orderNo);
        redirect('/order.php?no=' . urlencode($orderNo));
    }
}

function field_error(array $errors, string $key): string {
    return isset($errors[$key]) ? '<span class="hint" style="color:#B91C1C">' . e($errors[$key]) . '</span>' : '';
}

page_header('Buy ' . $product, "Buy a {$product} license: one-time payment of " . money($price) . '.');
?>
<section class="page-hero">
  <div class="wrap narrow">
    <h1>Buy <?= e($product) ?></h1>
    <p class="lead"><?= e(money($price)) ?> one-time<?= config('price_includes_gst') ? ', GST included' : '' ?>. One license for one computer, with <?= (int)config('free_support_months') ?> months of free support.</p>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap narrow">
    <div class="card">
      <?php if (!empty($errors['form'])): ?><p class="alert alert-error"><?= e($errors['form']) ?></p><?php endif; ?>
      <?php if ($errors && empty($errors['form'])): ?><p class="alert alert-error">Please check the highlighted fields.</p><?php endif; ?>
      <form method="post" class="form" novalidate>
        <?= csrf_field() ?>
        <div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          <label>Your name <input name="name" value="<?= e($v['name']) ?>" required autocomplete="name"><?= field_error($errors, 'name') ?></label>
          <label>Shop name <input name="shop_name" value="<?= e($v['shop_name']) ?>" required autocomplete="organization"><?= field_error($errors, 'shop_name') ?></label>
          <label>Mobile number <input name="phone" value="<?= e($v['phone']) ?>" required inputmode="tel" autocomplete="tel"><?= field_error($errors, 'phone') ?></label>
          <label>Email <input name="email" type="email" value="<?= e($v['email']) ?>" required autocomplete="email"><span class="hint">Your license key is sent here.</span><?= field_error($errors, 'email') ?></label>
          <label>City <input name="city" value="<?= e($v['city']) ?>" required autocomplete="address-level2"><?= field_error($errors, 'city') ?></label>
          <label>State
            <select name="state" required>
              <option value="">Choose...</option>
              <?php foreach (INDIAN_STATES as $state): ?>
                <option<?= $v['state'] === $state ? ' selected' : '' ?>><?= e($state) ?></option>
              <?php endforeach; ?>
            </select><?= field_error($errors, 'state') ?>
          </label>
          <label>GSTIN <span class="hint">Optional, for a GST invoice</span><input name="gstin" value="<?= e($v['gstin']) ?>"><?= field_error($errors, 'gstin') ?></label>
        </div>

        <div class="notice small">
          We use these details only to process your order, send your license key, give you support and tell you about updates
          to <?= e($product) ?>. We do not sell or share them for marketing. You can ask us to see, correct or delete them at any time.
          See our <a href="<?= BASE ?>/privacy.php" target="_blank">Privacy Policy</a>.
        </div>

        <label class="check"><input type="checkbox" name="agree_terms" value="1"<?= !empty($_POST['agree_terms']) ? ' checked' : '' ?>>
          <span>I agree to the <a href="<?= BASE ?>/terms.php" target="_blank">Terms of Service</a> and <a href="<?= BASE ?>/privacy.php" target="_blank">Privacy Policy</a>, and I consent to my details being used as described above.</span></label>
        <?= field_error($errors, 'agree_terms') ?>
        <label class="check"><input type="checkbox" name="agree_refund" value="1"<?= !empty($_POST['agree_refund']) ? ' checked' : '' ?>>
          <span>I understand that this is a digital product and <strong>all sales are final with no refunds</strong> (see the <a href="<?= BASE ?>/refund.php" target="_blank">Refund Policy</a>).</span></label>
        <?= field_error($errors, 'agree_refund') ?>

        <button class="btn btn-primary" type="submit">Place order for <?= e(money($price)) ?></button>
        <p class="muted small">Next you'll see how to pay by UPI or bank transfer.</p>
      </form>
    </div>
  </div>
</section>
<?php page_footer();
