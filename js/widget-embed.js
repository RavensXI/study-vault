/* ============================================
   Lesson widget embed — inline strip + modal.

   A widget is 400-600px tall; dropping that into the middle of the prose
   costs a screenful of scrolling and breaks the reading. So the lesson
   carries a compact strip (~110px) saying what the interactive is and
   what you will do, and the widget itself opens in a modal — which on a
   phone is a genuine upgrade, since full screen is more room, not less.

   The widget file is fetched only when the student opens it, so a lesson
   nobody interacts with pays nothing.
   ============================================ */
(function () {
  'use strict';

  var MAP = {
    'science-aqa/physics-paper-1/4': {
      file: 'series-voltage-split',
      label: 'Predict the voltmeter',
      line: 'Two resistors, one loop. Say where the volts go before you find out.',
      after: 'Parallel Circuits'
    },
    'history-aqa/elizabethan-england/13': {
      file: 'armada-chain-of-consequence',
      label: 'Put the disaster in order',
      line: 'Five links, shuffled. Commit to the chain, then see what forced what.',
      after: 'The Long Way Home'
    }
  };

  var BASE = '/scripts/widget_pipeline/builds/';

  var CSS = [
    '.sv-embed-strip{display:flex;align-items:center;gap:1rem;margin:2rem 0;padding:.95rem 1.1rem;',
    'background:#fff;border:1px solid #e8e3db;border-radius:14px;box-shadow:0 1px 2px rgba(45,42,38,.04)}',
    '.sv-embed-strip .sv-es-txt{flex:1 1 auto;min-width:0}',
    '.sv-embed-strip .sv-es-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--accent,#8a6a4f);margin-bottom:.15rem}',
    '.sv-embed-strip .sv-es-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.02rem;',
    'font-weight:600;color:#2d2a26;line-height:1.25}',
    '.sv-embed-strip .sv-es-line{font-size:.84rem;color:#5b564e;margin-top:.15rem;line-height:1.4}',
    '.sv-embed-strip .sv-es-go{flex:0 0 auto;font:inherit;font-size:.85rem;font-weight:600;',
    'padding:.55rem 1.1rem;border-radius:10px;background:#2d2a26;color:#fff;border:1px solid #2d2a26;cursor:pointer}',
    '.sv-embed-strip .sv-es-go:hover{background:#413d37}',
    '@media (max-width:560px){.sv-embed-strip{flex-direction:column;align-items:stretch;gap:.7rem}',
    '.sv-embed-strip .sv-es-go{width:100%}}',
    '.sv-modal{position:fixed;inset:0;z-index:9000;display:flex;align-items:center;justify-content:center;',
    'padding:1.5rem;background:rgba(45,42,38,.55)}',
    '.sv-modal-inner{background:#fff;border-radius:16px;max-width:940px;width:100%;max-height:92vh;',
    'overflow:auto;padding:1.1rem;position:relative}',
    '.sv-modal-close{position:absolute;top:.6rem;right:.7rem;z-index:2;width:34px;height:34px;',
    'border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;font-size:1.1rem;line-height:1}',
    '@media (max-width:560px){.sv-modal{padding:0}.sv-modal-inner{max-height:100vh;height:100%;border-radius:0}}'
  ].join('');

  function css() {
    if (document.getElementById('sv-embed-css')) return;
    var s = document.createElement('style');
    s.id = 'sv-embed-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function accentOf(node) {
    var v = getComputedStyle(node).getPropertyValue('--accent').trim();
    return v || '#8a6a4f';
  }

  function openModal(cfg, strip) {
    var overlay = document.createElement('div');
    overlay.className = 'sv-modal';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', cfg.label);
    var inner = document.createElement('div');
    inner.className = 'sv-modal-inner';
    var close = document.createElement('button');
    close.className = 'sv-modal-close';
    close.setAttribute('aria-label', 'Close');
    close.innerHTML = '&times;';
    var mount = document.createElement('div');
    inner.appendChild(close);
    inner.appendChild(mount);
    overlay.appendChild(inner);
    document.body.appendChild(overlay);

    var lastFocus = document.activeElement;
    document.body.style.overflow = 'hidden';

    function shut() {
      overlay.remove();
      document.body.style.overflow = '';
      document.removeEventListener('keydown', onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function onKey(e) {
      if (e.key === 'Escape') { shut(); return; }
      if (e.key !== 'Tab') return;
      var f = inner.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    }
    close.addEventListener('click', shut);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) shut(); });
    document.addEventListener('keydown', onKey);
    close.focus();

    mount.textContent = 'Loading...';
    fetch(BASE + cfg.file + '.js')
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function (src) {
        var tag = document.createElement('script');
        tag.textContent = src;
        document.head.appendChild(tag);
        if (!window.SVWidget || !window.SVWidget.mount) throw new Error('widget did not register');
        var W = window.SVWidget;
        window.SVWidget = null;
        mount.textContent = '';
        var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
        W.mount(mount, { accent: accentOf(strip), reducedMotion: !!reduced });
      })
      .catch(function (e) {
        mount.textContent = 'This interactive could not load (' + e.message + ').';
      });
  }

  function inject() {
    var m = location.pathname.match(/\/lesson\/([^/]+)\/([^/]+)\/(\d+)/);
    var cfg = m && MAP[m[1] + '/' + m[2] + '/' + m[3]];
    if (!cfg || document.querySelector('.sv-embed-strip')) return;
    var heads = document.querySelectorAll('#lesson-content h2, .lesson-content h2, article h2');
    var target = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].textContent.trim().indexOf(cfg.after) === 0) { target = heads[i]; break; }
    }
    if (!target) return;
    css();
    var strip = document.createElement('div');
    strip.className = 'sv-embed-strip';
    strip.innerHTML =
      '<div class="sv-es-txt"><div class="sv-es-kick">Interactive</div>' +
      '<div class="sv-es-title"></div><div class="sv-es-line"></div></div>';
    strip.querySelector('.sv-es-title').textContent = cfg.label;
    strip.querySelector('.sv-es-line').textContent = cfg.line;
    var go = document.createElement('button');
    go.className = 'sv-es-go';
    go.type = 'button';
    go.textContent = 'Try it';
    go.addEventListener('click', function () { openModal(cfg, strip); });
    strip.appendChild(go);
    target.parentNode.insertBefore(strip, target);
  }

  /* Hook the loader's post-render callback.

     CAREFUL: js/lesson-widgets.js wraps the same function, and each file
     re-arms on DOMContentLoaded. If each guards only on its OWN marker,
     they wrap each other's wrapper forever and the first real call blows
     the stack - taking every lesson feature down with it, not just this
     strip. So: we skip only on OUR marker (so we still wrap lesson-widgets'
     wrapper and actually run), and we stamp __svw on the wrapper we install
     so lesson-widgets' own re-arm sees itself and stops. */
  function arm() {
    var f = window.initLessonFeatures;
    if (typeof f !== 'function') return;
    if (f.__svEmbed) return;               // we are already in the chain
    var wrapped = function () {
      var r = f.apply(this, arguments);
      try { inject(); } catch (e) {}
      return r;
    };
    wrapped.__svEmbed = true;
    wrapped.__svw = true;                  // stop lesson-widgets re-wrapping us
    window.initLessonFeatures = wrapped;
  }
  arm();
  document.addEventListener('DOMContentLoaded', arm);
})();
