// Floating bug-report widget. Auto-injects a FAB and modal on every page that loads it.
// Captures the current page via html2canvas (lazy-loaded on first open) and sends to /api/bug-report.

(function () {
  // Skip on admin/teacher pages — the studyvault-auth session indicates they're a known role,
  // and a bug widget there clutters the UI. Students/free users have no such session.
  function isStaffPage() {
    var path = window.location.pathname || '';
    if (path.indexOf('/admin/') === 0 || path.indexOf('/teacher/') === 0) return true;
    return false;
  }
  if (isStaffPage()) return;

  // ---- Inject CSS ----
  var css = `
    .bugr-fab {
      position: fixed; right: 16px; bottom: 16px; z-index: 9990;
      width: 44px; height: 44px; border-radius: 50%;
      background: #2d2a26; color: #fff;
      border: 0; cursor: pointer;
      display: grid; place-items: center;
      box-shadow: 0 4px 14px rgba(45,42,38,0.22);
      transition: transform 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
    }
    .bugr-fab:hover { background: #4a463f; transform: translateY(-1px); box-shadow: 0 6px 18px rgba(45,42,38,0.28); }
    .bugr-fab:active { transform: translateY(0); }
    .bugr-fab svg { width: 20px; height: 20px; }
    .bugr-fab[hidden] { display: none; }
    @media print { .bugr-fab { display: none !important; } }

    .bugr-overlay {
      position: fixed; inset: 0; z-index: 9991;
      background: rgba(45,42,38,0.45);
      display: flex; align-items: center; justify-content: center;
      padding: 1.5rem;
      opacity: 0; visibility: hidden;
      transition: opacity 0.2s ease, visibility 0.2s ease;
    }
    .bugr-overlay.open { opacity: 1; visibility: visible; }
    .bugr-modal {
      background: #fff;
      border-radius: 18px;
      width: 100%; max-width: 520px;
      max-height: calc(100vh - 3rem);
      box-shadow: 0 20px 60px rgba(45,42,38,0.22);
      display: flex; flex-direction: column;
      transform: translateY(8px) scale(0.98);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      overflow: hidden;
    }
    .bugr-overlay.open .bugr-modal { transform: translateY(0) scale(1); }
    .bugr-header {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid #f0ede8;
      display: flex; align-items: center; gap: 0.7rem;
    }
    .bugr-header .bugr-icon {
      width: 32px; height: 32px; border-radius: 9px;
      background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
      color: #dc2626;
      display: grid; place-items: center;
      flex-shrink: 0;
    }
    .bugr-header .bugr-icon svg { width: 16px; height: 16px; }
    .bugr-header h2 {
      flex: 1; margin: 0;
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1rem; font-weight: 700; color: #2d2a26;
      line-height: 1.3;
    }
    .bugr-header h2 small {
      display: block; font-family: 'Inter', sans-serif;
      font-size: 0.78rem; font-weight: 500; color: #6b645c;
      margin-top: 0.1rem;
    }
    .bugr-close {
      background: transparent; border: 0; padding: 0.4rem;
      cursor: pointer; color: #6b645c; border-radius: 6px;
      display: grid; place-items: center;
      transition: background 0.15s ease;
    }
    .bugr-close:hover { background: #f0ede8; color: #2d2a26; }
    .bugr-close svg { width: 18px; height: 18px; }

    .bugr-body { padding: 1.1rem 1.25rem 1.25rem; overflow-y: auto; }
    .bugr-field { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 0.95rem; }
    .bugr-field > .bugr-label {
      font-family: 'Inter', sans-serif;
      font-size: 0.82rem; font-weight: 600; color: #4a463f;
    }
    .bugr-field .bugr-meta {
      font-weight: 400; font-size: 0.78rem; color: #9b9590;
      margin-left: 0.25rem;
    }
    .bugr-field textarea, .bugr-field input[type="email"] {
      font-family: 'Inter', sans-serif; font-size: 0.95rem;
      padding: 0.65rem 0.85rem;
      border: 1px solid #e0d9cc; border-radius: 10px;
      background: #fff; color: #2d2a26;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .bugr-field textarea { min-height: 90px; resize: vertical; line-height: 1.5; }
    .bugr-field textarea::placeholder, .bugr-field input::placeholder { color: #b8b1a6; }
    .bugr-field textarea:focus, .bugr-field input:focus {
      outline: 0; border-color: #dc2626; box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.14);
    }

    .bugr-page {
      font-size: 0.78rem; color: #6b645c;
      padding: 0.5rem 0.7rem;
      background: #faf8f5;
      border-radius: 8px;
      word-break: break-all;
      line-height: 1.4;
    }

    .bugr-screenshot {
      display: flex; align-items: center; gap: 0.7rem;
      padding: 0.7rem 0.85rem;
      background: #faf8f5; border-radius: 10px;
      margin-bottom: 0.95rem;
    }
    .bugr-screenshot input[type="checkbox"] { accent-color: #dc2626; width: 16px; height: 16px; flex-shrink: 0; }
    .bugr-screenshot label { font-size: 0.85rem; color: #4a463f; cursor: pointer; flex: 1; }
    .bugr-screenshot small { display: block; color: #9b9590; font-size: 0.75rem; margin-top: 0.1rem; }

    .bugr-footer {
      padding: 0.85rem 1.25rem 1rem;
      border-top: 1px solid #f0ede8;
      display: flex; justify-content: space-between; align-items: center; gap: 0.75rem;
      background: #fdfbf7;
    }
    .bugr-msg { font-size: 0.85rem; color: #6b645c; flex: 1; }
    .bugr-msg.error { color: #b91c1c; }
    .bugr-msg.success { color: #15803d; font-weight: 600; }
    .bugr-actions { display: flex; gap: 0.45rem; }
    .bugr-btn {
      font-family: 'Inter', sans-serif; font-size: 0.88rem; font-weight: 600;
      padding: 0.55rem 1.1rem; border-radius: 9px; cursor: pointer;
      transition: background 0.15s ease, transform 0.1s ease;
    }
    .bugr-btn:disabled { opacity: 0.55; cursor: default; }
    .bugr-btn-ghost { background: transparent; border: 1px solid #e0d9cc; color: #4a463f; }
    .bugr-btn-ghost:hover:not(:disabled) { background: #faf8f5; border-color: #c9c1b2; }
    .bugr-btn-primary { background: #2d2a26; color: #fff; border: 0; }
    .bugr-btn-primary:hover:not(:disabled) { background: #4a463f; }
    .bugr-btn-primary:active:not(:disabled) { transform: scale(0.97); }

    @media (max-width: 600px) {
      .bugr-fab { right: 12px; bottom: 12px; width: 42px; height: 42px; }
      .bugr-modal { max-height: 100vh; border-radius: 14px; }
    }
  `;
  var styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ---- Inject DOM ----
  var fab = document.createElement('button');
  fab.className = 'bugr-fab';
  fab.type = 'button';
  fab.setAttribute('aria-label', 'Report a bug');
  fab.title = 'Report a bug';
  fab.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/>' +
      '<path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/>' +
      '<path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/>' +
      '<path d="M12 20v-9"/>' +
      '<path d="M6.53 9C4.6 8.8 3 7.1 3 5"/>' +
      '<path d="M6 13H2"/>' +
      '<path d="M3 21c0-2.1 1.7-3.9 3.8-4"/>' +
      '<path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/>' +
      '<path d="M22 13h-4"/>' +
      '<path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/>' +
    '</svg>';
  document.body.appendChild(fab);

  var overlay = document.createElement('div');
  overlay.className = 'bugr-overlay';
  overlay.innerHTML =
    '<div class="bugr-modal" role="dialog" aria-modal="true" aria-labelledby="bugr-title">' +
      '<div class="bugr-header">' +
        '<span class="bugr-icon" aria-hidden="true">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>' +
          '</svg>' +
        '</span>' +
        '<h2 id="bugr-title">Report a bug<small>Tell us what went wrong and we\'ll take a look.</small></h2>' +
        '<button class="bugr-close" aria-label="Close">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="bugr-body">' +
        '<div class="bugr-field">' +
          '<label class="bugr-label" for="bugr-msg">What happened?</label>' +
          '<textarea id="bugr-msg" maxlength="2000" placeholder="e.g. The audio player won\'t load on this lesson."></textarea>' +
        '</div>' +
        '<div class="bugr-field">' +
          '<label class="bugr-label" for="bugr-email">Email <span class="bugr-meta">(optional, for updates)</span></label>' +
          '<input type="email" id="bugr-email" maxlength="200" placeholder="you@example.com">' +
        '</div>' +
        '<div class="bugr-field">' +
          '<span class="bugr-label">Page</span>' +
          '<div class="bugr-page" id="bugr-page-url"></div>' +
        '</div>' +
        '<div class="bugr-screenshot">' +
          '<input type="checkbox" id="bugr-include-screenshot" checked>' +
          '<label for="bugr-include-screenshot">' +
            'Include a screenshot of this page' +
            '<small>Helps us see exactly what you saw.</small>' +
          '</label>' +
        '</div>' +
      '</div>' +
      '<div class="bugr-footer">' +
        '<span class="bugr-msg" id="bugr-msg-text"></span>' +
        '<div class="bugr-actions">' +
          '<button type="button" class="bugr-btn bugr-btn-ghost" id="bugr-cancel">Cancel</button>' +
          '<button type="button" class="bugr-btn bugr-btn-primary" id="bugr-send">Send report</button>' +
        '</div>' +
      '</div>' +
    '</div>';
  document.body.appendChild(overlay);

  var msgEl = overlay.querySelector('#bugr-msg');
  var emailEl = overlay.querySelector('#bugr-email');
  var screenshotToggle = overlay.querySelector('#bugr-include-screenshot');
  var pageUrlEl = overlay.querySelector('#bugr-page-url');
  var sendBtn = overlay.querySelector('#bugr-send');
  var cancelBtn = overlay.querySelector('#bugr-cancel');
  var closeBtn = overlay.querySelector('.bugr-close');
  var msgText = overlay.querySelector('#bugr-msg-text');

  function setMsg(text, type) {
    msgText.textContent = text || '';
    msgText.className = 'bugr-msg' + (type ? ' ' + type : '');
  }

  function open() {
    pageUrlEl.textContent = window.location.href;
    setMsg('');
    overlay.classList.add('open');
    setTimeout(function () { msgEl.focus(); }, 200);
    document.addEventListener('keydown', onKey);
  }
  function close() {
    overlay.classList.remove('open');
    document.removeEventListener('keydown', onKey);
  }
  function onKey(e) {
    if (e.key === 'Escape') close();
  }

  fab.addEventListener('click', open);
  cancelBtn.addEventListener('click', close);
  closeBtn.addEventListener('click', close);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) close();
  });

  // Lazy-load html2canvas only when needed
  var h2cPromise = null;
  function loadHtml2Canvas() {
    if (h2cPromise) return h2cPromise;
    h2cPromise = new Promise(function (resolve, reject) {
      if (window.html2canvas) return resolve(window.html2canvas);
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
      s.async = true;
      s.onload = function () { resolve(window.html2canvas); };
      s.onerror = function () { reject(new Error('Could not load screenshot tool')); };
      document.head.appendChild(s);
    });
    return h2cPromise;
  }

  async function captureScreenshot() {
    try {
      var html2canvas = await loadHtml2Canvas();
      // Hide the modal during capture so the screenshot shows the actual page
      overlay.style.visibility = 'hidden';
      fab.style.visibility = 'hidden';
      var canvas = await html2canvas(document.documentElement, {
        backgroundColor: '#faf8f5',
        scale: Math.min(window.devicePixelRatio || 1, 1.5),
        useCORS: true,
        allowTaint: false,
        logging: false,
        windowWidth: document.documentElement.clientWidth,
        windowHeight: document.documentElement.clientHeight,
        x: window.scrollX,
        y: window.scrollY,
        width: document.documentElement.clientWidth,
        height: document.documentElement.clientHeight,
      });
      overlay.style.visibility = '';
      fab.style.visibility = '';

      // Downscale if huge — cap longest edge at 1600px
      var maxEdge = 1600;
      var srcW = canvas.width, srcH = canvas.height;
      var scale = Math.min(1, maxEdge / Math.max(srcW, srcH));
      var outCanvas = canvas;
      if (scale < 1) {
        outCanvas = document.createElement('canvas');
        outCanvas.width = Math.round(srcW * scale);
        outCanvas.height = Math.round(srcH * scale);
        outCanvas.getContext('2d').drawImage(canvas, 0, 0, outCanvas.width, outCanvas.height);
      }
      return outCanvas.toDataURL('image/jpeg', 0.78);
    } catch (e) {
      overlay.style.visibility = '';
      fab.style.visibility = '';
      console.warn('html2canvas failed', e);
      return null;
    }
  }

  sendBtn.addEventListener('click', async function () {
    var message = (msgEl.value || '').trim();
    var email = (emailEl.value || '').trim();
    if (!message) {
      setMsg('Please describe what happened.', 'error');
      msgEl.focus();
      return;
    }
    sendBtn.disabled = true;
    cancelBtn.disabled = true;
    setMsg('Sending...');

    var screenshot = null;
    if (screenshotToggle.checked) {
      setMsg('Capturing screenshot...');
      screenshot = await captureScreenshot();
      if (!screenshot) setMsg('Couldn\'t capture screenshot — sending without it.');
    }

    try {
      var resp = await fetch('/api/bug-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
          email: email,
          page_url: window.location.href,
          viewport_size: window.innerWidth + 'x' + window.innerHeight,
          screenshot: screenshot,
        }),
      });
      var json = {};
      try { json = await resp.json(); } catch (e) {}
      if (resp.ok && json.ok) {
        setMsg('Thanks — report received.', 'success');
        msgEl.value = '';
        emailEl.value = '';
        setTimeout(close, 1400);
      } else {
        setMsg((json && json.error) || 'Could not send right now.', 'error');
      }
    } catch (err) {
      setMsg('Network error — please try again.', 'error');
    } finally {
      sendBtn.disabled = false;
      cancelBtn.disabled = false;
    }
  });
})();
