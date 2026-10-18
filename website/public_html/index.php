<?php
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/layout.php';

$product = config('product_name');
$price = (int)config('price_inr');
$supportMonths = (int)config('free_support_months', 3);

// Screenshots: any images in assets/screenshots, in file-name order
$shots = [];
foreach (glob(__DIR__ . '/assets/screenshots/*.{png,jpg,jpeg,webp}', GLOB_BRACE) ?: [] as $path) {
    $file = basename($path);
    $caption = ucfirst(trim(str_replace(['-', '_'], ' ', preg_replace('/^\d+[-_ ]*|\.\w+$/', '', $file))));
    $shots[] = ['src' => '/assets/screenshots/' . rawurlencode($file), 'caption' => $caption];
}
sort($shots);

$youtube = trim((string)config('youtube_video_id'));
$videoFile = trim((string)config('video_file'));
$hasVideoFile = $videoFile && is_file(__DIR__ . '/assets/video/' . basename($videoFile));

function icon(string $name): string {
    $paths = [
        'users'   => '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        'ruler'   => '<path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4Z"/><path d="m7.5 10.5 2 2M10.5 7.5l2 2M13.5 4.5l2 2M4.5 13.5l2 2"/>',
        'orders'  => '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
        'chat'    => '<path d="M21 11.5a8.4 8.4 0 0 1-12.6 7.3L3 21l2.2-5.4A8.4 8.4 0 1 1 21 11.5Z"/>',
        'chart'   => '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
        'box'     => '<path d="M21 8 12 3 3 8v8l9 5 9-5V8Z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
        'shield'  => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
        'backup'  => '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
        'palette' => '<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2a10 10 0 0 0 0 20c1 0 1.7-.8 1.7-1.7 0-.4-.2-.8-.4-1.1-.3-.3-.4-.7-.4-1.1 0-1 .8-1.7 1.7-1.7H17a5 5 0 0 0 5-5C22 6 17.5 2 12 2Z"/>',
        'offline' => '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    ];
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $paths[$name] . '</svg>';
}

$features = [
    ['users', 'Customers', 'Name, mobile, photo and address for every customer, with quick search and an Excel export.'],
    ['ruler', 'Measurements', 'Save measurements by garment (shirt, pant, suit, kurta...) in inches or cm and reuse them for the next order.'],
    ['orders', 'Orders and payments', 'Garments, delivery dates, advance and balance. Track each order from cutting to delivered.'],
    ['chat', 'WhatsApp and email updates', 'Tell customers automatically when their order is ready, and send festival offers to your customer list. WhatsApp needs your own AiSensy account.'],
    ['chart', 'Reports', 'Sales, customers and stock for any period, downloaded as a ready-to-print Excel file.'],
    ['box', 'Fabric and stock', 'Keep count of fabric, buttons and zippers, with low-stock warnings.'],
    ['shield', 'Staff logins', 'Give each staff member their own login and choose which pages they can open.'],
    ['backup', 'Daily backup', 'A copy of everything is saved every day. Restore it on a new computer in one click.'],
    ['palette', 'Your look', 'Six colour themes, light and dark, any accent colour, and your shop name on every screen.'],
    ['offline', 'Works without internet', 'Everything is stored on your computer. Internet is only needed to activate and to send messages.'],
];

$faqs = [
    ['Is this a one-time payment?', "Yes. You pay " . money($price) . " once and use {$product} for as long as you like on one computer. There is no monthly or yearly fee."],
    ['What do I need to run it?', 'A Windows 10 or Windows 11 computer (64-bit) with at least 4 GB RAM and 1 GB free disk space. Internet is needed once to activate the license.'],
    ['Can I use it on more than one computer?', 'One license works on one computer. If you change your computer, contact us and we will move your license to the new one. For a second computer, buy a second license.'],
    ['Where is my shop data kept?', "On your own computer. We do not receive or see your customers, measurements or orders. {$product} makes a backup every day to a folder you choose, such as a USB drive or Google Drive folder."],
    ['Does it work on mobile?', "Not yet. {$product} is a Windows desktop program."],
    ['What does support include?', "For {$supportMonths} months after purchase we help with installation, questions and bug fixes for the features that exist today, free. After that, support is paid. New features or changes made for your shop are quoted separately."],
    ['Can I get a refund?', 'No. Because the software is delivered instantly as a download with a license key, all sales are final. Please watch the video, look at the screenshots and ask us any questions before you buy.'],
    ['How do I get updates?', "When we release a new version with fixes, {$product} tells you and you can download it with your license key. Updates for existing features are free."],
];

page_header($product, 'Tailor shop software for Windows: customers, measurements, orders, payments, WhatsApp updates and reports. One-time payment.');
?>

<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>The order book for your tailoring shop.</h1>
      <p class="lead">Customers, measurements, orders and payments in one Windows app. Pay once and use it for as long as you like. No monthly fee.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/buy.php">Buy for <?= e(money($price)) ?></a>
        <a class="btn btn-ghost" href="#features">See what it does</a>
      </div>
      <p class="hero-note">One-time payment<?= config('price_includes_gst') ? ', GST included' : '' ?>. <?= (int)$supportMonths ?> months of free support.</p>
    </div>

    <div class="app-window" role="img" aria-label="Illustration of the <?= e($product) ?> app showing a customer's shirt measurements and today's orders">
      <div class="app-titlebar"><i></i><i></i><i></i></div>
      <div class="app-body">
        <div class="app-side">
          <div class="shop"><img src="/assets/img/icon.png" alt="">Sharma Tailors</div>
          <div class="item">Dashboard</div>
          <div class="item">Customers</div>
          <div class="item on">Measurements</div>
          <div class="item">Orders</div>
          <div class="item">Reports</div>
        </div>
        <div class="app-main">
          <div class="title">Rahul Verma · Shirt</div>
          <div class="app-card">
            <div class="label">Upper body (inches)</div>
            <div class="measure-grid">
              <span><small>Chest</small><b>40</b></span>
              <span><small>Shoulder</small><b>18</b></span>
              <span><small>Sleeve</small><b>24.5</b></span>
              <span><small>Neck</small><b>15.5</b></span>
              <span><small>Length</small><b>30</b></span>
              <span><small>Waist</small><b>34</b></span>
            </div>
          </div>
          <div class="app-card">
            <div class="label">Today's deliveries</div>
            <div class="app-row"><span>ORD-0142 · 2 shirts</span><span class="pill ready">Ready</span></div>
            <div class="app-row"><span>ORD-0145 · Sherwani</span><span class="pill stitching">Stitching</span></div>
            <div class="app-row"><span>ORD-0147 · Blouse</span><span class="pill pending">Pending</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="tape-band" aria-hidden="true">
    <div class="tape"><ol><?php for ($i = 0; $i <= 40; $i++) echo '<li>' . $i . '</li>'; ?></ol></div>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    <div class="section-head">
      <h2>Everything your counter book does, without the lost pages</h2>
      <p class="lead">Made for tailors and boutiques. No training needed: if you can use WhatsApp, you can use <?= e($product) ?>.</p>
    </div>
    <ul class="feature-list">
      <?php foreach ($features as [$ic, $title, $text]): ?>
        <li><?= icon($ic) ?><div><h3><?= e($title) ?></h3><p><?= e($text) ?></p></div></li>
      <?php endforeach; ?>
    </ul>
  </div>
</section>

<?php if ($youtube || $hasVideoFile): ?>
<section class="section" id="video">
  <div class="wrap narrow">
    <div class="section-head"><h2>See it in two minutes</h2></div>
    <div class="video-box">
      <?php if ($hasVideoFile): ?>
        <video controls preload="metadata" poster="/assets/img/logo.png">
          <source src="/assets/video/<?= e(rawurlencode(basename($videoFile))) ?>" type="video/mp4">
        </video>
      <?php else: ?>
        <button class="video-play" data-youtube="<?= e($youtube) ?>" aria-label="Play the demo video">
          <div><span>▶</span>Play video<br><small class="muted">Loads from YouTube</small></div>
        </button>
      <?php endif; ?>
    </div>
  </div>
</section>
<?php endif; ?>

<?php if ($shots): ?>
<section class="section" id="screenshots">
  <div class="wrap">
    <div class="section-head"><h2>Screenshots</h2></div>
    <div class="gallery">
      <?php foreach ($shots as $shot): ?>
        <figure>
          <button data-full="<?= e($shot['src']) ?>" data-alt="<?= e($shot['caption']) ?>" aria-label="Enlarge: <?= e($shot['caption']) ?>">
            <img src="<?= e($shot['src']) ?>" alt="<?= e($shot['caption']) ?>" loading="lazy">
          </button>
          <figcaption><?= e($shot['caption']) ?></figcaption>
        </figure>
      <?php endforeach; ?>
    </div>
  </div>
  <div class="lightbox" role="dialog" aria-label="Screenshot"><button class="btn btn-ghost btn-sm">Close</button><img alt=""></div>
</section>
<?php endif; ?>

<section class="section" id="themes">
  <div class="wrap">
    <div class="section-head">
      <h2>Light, dark or colourful</h2>
      <p class="lead">Pick one of six themes and any accent colour you like. Your shop name stays at the top of the menu.</p>
    </div>
    <div class="media-frame">
      <img src="/assets/img/themes.png" alt="The six colour themes: Midnight, Classic Light, Ocean, Royal Purple, Sunrise and Mint" loading="lazy" width="1656" height="788">
    </div>
  </div>
</section>

<hr class="stitch wrap">

<section class="section" id="how">
  <div class="wrap">
    <div class="section-head"><h2>How buying works</h2></div>
    <ol class="steps">
      <li><h3>Fill the form</h3><p>Your name, shop name, mobile and email.</p></li>
      <li><h3>Pay by UPI or bank</h3><p>Then enter the transaction ID so we can match your payment.</p></li>
      <li><h3>Get your license key</h3><p>We check the payment and email your key, usually within one working day.</p></li>
      <li><h3>Download and activate</h3><p>Install <?= e($product) ?>, enter the key, and start adding customers.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="pricing">
  <div class="wrap">
    <div class="section-head"><h2>One price. Yours to keep.</h2></div>
    <div class="pricing">
      <div class="price-side">
        <div><?= e($product) ?> license</div>
        <div class="amount"><?= e(money($price)) ?></div>
        <div class="muted">One-time payment<?= config('price_includes_gst') ? ', inclusive of GST' : '' ?>. For one computer.</div>
        <a class="btn btn-primary" href="/buy.php">Buy now</a>
        <p class="muted small" style="margin-top:14px">All sales are final. See the <a href="/refund.php" style="color:#C7D2FE">refund policy</a>.</p>
      </div>
      <ul class="price-list">
        <li>Every feature on this page</li>
        <li>Use it for life on one computer</li>
        <li><?= (int)$supportMonths ?> months of free support by phone, WhatsApp and email</li>
        <li>Free updates that fix and improve existing features</li>
        <li>Your data stays on your computer</li>
        <li class="no">New features or changes made for your shop are quoted separately</li>
        <li class="no">Support after <?= (int)$supportMonths ?> months is paid</li>
      </ul>
    </div>
  </div>
</section>

<section class="section faq" id="faq">
  <div class="wrap narrow">
    <h2>Questions</h2>
    <?php foreach ($faqs as [$q, $a]): ?>
      <details><summary><?= e($q) ?></summary><p><?= e($a) ?></p></details>
    <?php endforeach; ?>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Ready to close the paper register?</h2>
        <p>Questions first? Call <?= e(config('business_phone')) ?> or <a href="/contact.php" style="color:#C7D2FE">send us a message</a>.</p>
      </div>
      <a class="btn btn-primary" href="/buy.php">Buy <?= e($product) ?></a>
    </div>
  </div>
</section>

<?php page_footer();
