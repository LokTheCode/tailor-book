// Tailor Book website: menu, video, screenshot viewer, copy buttons.
(function () {
  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // YouTube loads only after the visitor clicks play (no tracking before that)
  document.querySelectorAll('[data-youtube]').forEach(function (button) {
    button.addEventListener('click', function () {
      var id = button.getAttribute('data-youtube');
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      frame.title = 'Tailor Book demo video';
      frame.allow = 'autoplay; encrypted-media; picture-in-picture';
      frame.allowFullscreen = true;
      button.replaceWith(frame);
    });
  });

  // Screenshot viewer
  var box = document.querySelector('.lightbox');
  if (box) {
    var boxImg = box.querySelector('img');
    var close = function () { box.classList.remove('open'); boxImg.removeAttribute('src'); };
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () {
        boxImg.src = b.getAttribute('data-full');
        boxImg.alt = b.getAttribute('data-alt') || '';
        box.classList.add('open');
        box.querySelector('button').focus();
      });
    });
    box.addEventListener('click', function (e) { if (e.target === box || e.target.tagName === 'BUTTON') close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  // Copy license key
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = document.getElementById(b.getAttribute('data-copy')).textContent.trim();
      navigator.clipboard.writeText(text).then(function () {
        var label = b.textContent;
        b.textContent = 'Copied';
        setTimeout(function () { b.textContent = label; }, 1500);
      });
    });
  });
})();
