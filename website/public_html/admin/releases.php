<?php
require __DIR__ . '/_admin.php';

function ini_bytes(string $value): int {
    $value = trim($value);
    $unit = strtolower(substr($value, -1));
    $n = (int)$value;
    return match ($unit) { 'g' => $n * 1073741824, 'm' => $n * 1048576, 'k' => $n * 1024, default => $n };
}
$maxUpload = min(ini_bytes((string)ini_get('upload_max_filesize')), ini_bytes((string)ini_get('post_max_size')));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // A too-large upload arrives with an empty $_POST (no CSRF token)
    if (empty($_POST) && (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
        flash('The file is bigger than this server allows through the browser (' . round($maxUpload / 1048576) . ' MB). Upload it with File Manager or FTP instead (see below).', 'error');
        redirect('/admin/releases.php');
    }
    csrf_check();
    $action = post('action');

    if ($action === 'upload') {
        $file = $_FILES['installer'] ?? null;
        $version = post('version');
        if (!preg_match('/^\d+\.\d+(\.\d+)?$/', $version)) {
            flash('Enter the version like 1.2.0 (the same as APP_VERSION in config.py).', 'error');
        } elseif (!$file || $file['error'] !== UPLOAD_ERR_OK) {
            flash('Upload failed (error ' . (int)($file['error'] ?? -1) . '). For big files use File Manager or FTP.', 'error');
        } elseif (strtolower(pathinfo($file['name'], PATHINFO_EXTENSION)) !== 'exe') {
            flash('Upload the installer .exe file from installer_output.', 'error');
        } else {
            $name = "TailorBook_Setup_v{$version}.exe";
            move_uploaded_file($file['tmp_name'], releases_dir() . '/' . $name);
            sync_releases();
            db()->prepare('UPDATE releases SET notes = ? WHERE version = ?')->execute([post('notes') ?: null, $version]);
            audit('release_uploaded', $version);
            flash("Version {$version} uploaded. Customers can download it now, and the app will offer the update.");
        }
    }

    if ($action === 'save') {
        db()->prepare('UPDATE releases SET notes = ?, published = ? WHERE id = ?')
            ->execute([post('notes') ?: null, post('published') ? 1 : 0, (int)post('id')]);
        flash('Release saved.');
    }

    if ($action === 'delete') {
        $q = db()->prepare('SELECT * FROM releases WHERE id = ?');
        $q->execute([(int)post('id')]);
        if ($r = $q->fetch()) {
            @unlink(releases_dir() . '/' . basename($r['filename']));
            db()->prepare('DELETE FROM releases WHERE id = ?')->execute([$r['id']]);
            audit('release_deleted', $r['version']);
            flash("Version {$r['version']} deleted.");
        }
    }
    redirect('/admin/releases.php');
}

sync_releases();
$releases = db()->query('SELECT * FROM releases')->fetchAll();
usort($releases, fn($a, $b) => version_compare($b['version'], $a['version']));
$latest = latest_release();

admin_header('Releases', 'releases');
?>
<div class="card">
  <h2>Upload a new version</h2>
  <ol>
    <li>In the desktop project, set the new version in <code>config.py</code> (<code>APP_VERSION</code>) and <code>setup.iss</code> (<code>MyAppVersion</code>).</li>
    <li>Run <code>build.bat</code>. The installer is created in <code>installer_output</code>.</li>
    <li>Upload it here. Customers can download it straight away, and the app shows <em>Update available</em> the next time it starts.</li>
  </ol>
  <form method="post" enctype="multipart/form-data" class="form">
    <?= csrf_field() ?><input type="hidden" name="action" value="upload">
    <div class="form-grid">
      <label>Version <input name="version" placeholder="1.2.0" required pattern="\d+\.\d+(\.\d+)?"></label>
      <label>Installer (.exe) <span class="hint">Up to <?= round($maxUpload / 1048576) ?> MB through the browser</span><input type="file" name="installer" accept=".exe" required></label>
    </div>
    <label>What's new <span class="hint">Shown on the download page and in the app</span><textarea name="notes" rows="3" placeholder="- Fixed: ..."></textarea></label>
    <button class="btn btn-primary">Upload</button>
  </form>
  <h3>Bigger file? Use Hostinger File Manager or FTP</h3>
  <p>Upload the .exe into the <code>private/releases</code> folder (next to <code>public_html</code>). Name it with the version, e.g.
    <code>TailorBook_Setup_v1.2.0.exe</code>. It appears in the list below automatically; add release notes there.</p>
</div>

<h2>Versions</h2>
<div class="table-wrap">
<table class="data">
  <tr><th>Version</th><th>File</th><th>Size</th><th>Added</th><th>Notes / visible</th><th></th></tr>
  <?php foreach ($releases as $r): ?>
    <tr>
      <td><strong><?= e($r['version']) ?></strong><?= $latest && $latest['id'] === $r['id'] ? ' <span class="status status-paid">Latest</span>' : '' ?></td>
      <td class="mono small"><?= e($r['filename']) ?><?= is_file(releases_dir() . '/' . $r['filename']) ? '' : '<br><span style="color:#B91C1C">file missing</span>' ?></td>
      <td><?= e(number_format($r['size'] / 1048576, 1)) ?> MB</td>
      <td><?= e(nice_date($r['created_at'])) ?></td>
      <td>
        <form method="post" class="form" style="gap:8px">
          <?= csrf_field() ?><input type="hidden" name="action" value="save"><input type="hidden" name="id" value="<?= (int)$r['id'] ?>">
          <textarea name="notes" rows="2"><?= e((string)$r['notes']) ?></textarea>
          <label class="check"><input type="checkbox" name="published" value="1"<?= $r['published'] ? ' checked' : '' ?>><span>Customers can download this version</span></label>
          <button class="btn btn-ghost btn-sm">Save</button>
        </form>
      </td>
      <td>
        <form method="post" onsubmit="return confirm('Delete version <?= e($r['version']) ?> and its file?')">
          <?= csrf_field() ?><input type="hidden" name="action" value="delete"><input type="hidden" name="id" value="<?= (int)$r['id'] ?>">
          <button class="btn btn-ghost btn-sm">Delete</button>
        </form>
      </td>
    </tr>
  <?php endforeach; ?>
  <?php if (!$releases): ?><tr><td colspan="6" class="muted">No versions yet.</td></tr><?php endif; ?>
</table>
</div>

<div class="card" style="margin-top:32px">
  <h2>Desktop app connection</h2>
  <p>These two lines go in the desktop app's <code>config.py</code> before you build it:</p>
  <pre class="keybox">LICENSE_SERVER_URL = "<?= e(rtrim((string)config('site_url'), '/')) ?>"
LICENSE_PUBLIC_KEY = "<?= e(signing_public_key_hex()) ?>"</pre>
  <p class="muted small">The public key only checks licenses; it can't create them. The matching secret key stays in <code>private/keys</code> on the server. Never share or delete it, or existing licenses stop working.</p>
</div>
<?php admin_footer();
