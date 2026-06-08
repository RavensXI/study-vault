/* Design-lab skin switcher — localhost only. Flips body[data-skin] so the
   real lesson re-skins live. Not shipped; remove the <script> to drop it. */
(function () {
  if (location.hostname !== '127.0.0.1' && location.hostname !== 'localhost') return;

  var SKINS = [['', 'Today'], ['reader', 'Reader'], ['paper', 'Paper'], ['ink', 'Ink'], ['crisp', 'Crisp']];

  var style = document.createElement('style');
  style.textContent =
    '#skin-lab{position:fixed;top:10px;right:12px;z-index:99999;display:flex;gap:.35rem;align-items:center;' +
    'background:#1b1916;color:#e8e2d6;font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;' +
    'padding:.45rem .6rem;border-radius:9px;box-shadow:0 6px 24px rgba(0,0,0,.35)}' +
    '#skin-lab b{color:#c9a23f;letter-spacing:.1em;text-transform:uppercase;margin-right:.4rem;font-weight:600}' +
    '#skin-lab button{font:inherit;cursor:pointer;background:transparent;color:#cdc6b8;border:1px solid #3a352d;' +
    'border-radius:5px;padding:.3rem .6rem}' +
    '#skin-lab button:hover{color:#fff;border-color:#6a6253}' +
    '#skin-lab button[aria-pressed="true"]{background:#c9a23f;color:#1b1916;border-color:#c9a23f;font-weight:600}';
  document.head.appendChild(style);

  var bar = document.createElement('div');
  bar.id = 'skin-lab';
  bar.innerHTML = '<b>Skin</b>' + SKINS.map(function (s) {
    return '<button data-skin="' + s[0] + '">' + s[1] + '</button>';
  }).join('');

  function set(skin) {
    if (skin) document.body.dataset.skin = skin; else delete document.body.dataset.skin;
    document.body.classList.toggle('dark-mode', skin === 'ink'); // reuse battle-tested dark coverage
    [].forEach.call(bar.querySelectorAll('button'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-skin') === skin);
    });
  }
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (b) set(b.getAttribute('data-skin'));
  });

  // clear onboarding overlays + force scroll-reveal so the page is fully visible
  function tidy() {
    document.querySelectorAll('[class*="tour"],[class*="coach"],[class*="tutorial"],[class*="walkthrough"],[class*="spotlight"],.anon-welcome-overlay,[class*="whats-new"]')
      .forEach(function (e) { e.remove(); });
    document.querySelectorAll('[class*="sv-reveal"],.lesson-header .lesson-number,.lesson-header h1,.lesson-hero-image,.lesson-sidebar,.study-notes > *,.exam-tip,.conclusion,.practice-section')
      .forEach(function (e) { e.classList.add('sv-visible'); });
    // DESIGN-LAB: Video as a compact button tile (would open the video modal on real lessons)
    var vs = document.getElementById('sidebar-video-section');
    if (vs && !vs.dataset.tilebtn) {
      vs.dataset.tilebtn = '1';
      vs.style.display = '';
      vs.innerHTML = '<button class="sv-tool-btn" type="button">'
        + '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polygon points="10,9 15,12 10,15" fill="currentColor" stroke="none"/></svg>'
        + '<span>Video</span></button>';
    }
    setupMediaLauncher();
    buildToolTiles();
    revealMasthead();
  }

  // Relocate the floating Highlight + Ask-the-tutor buttons into the sidebar as tiles
  function buildToolTiles() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    if (!sidebar || sidebar.dataset.toolTiles) return;
    var hl = document.querySelector('.sv-hl-fab-stack');
    var tutor = document.querySelector('.tutor-dock');
    if (!hl && !tutor) return; // FABs not built yet
    sidebar.dataset.toolTiles = '1';

    function tile(label, svg) {
      var sec = document.createElement('div');
      sec.className = 'sidebar-section sidebar-tool-tile';
      var b = document.createElement('button');
      b.className = 'sv-tool-btn'; b.type = 'button';
      b.innerHTML = svg + '<span class="sv-tool-label">' + label + '</span>';
      sec.appendChild(b);
      sidebar.appendChild(sec);
      return { btn: b, label: b.querySelector('.sv-tool-label') };
    }
    var hlSvg = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l-4 4v3h3l4-4"/><path d="M13 7l4 4"/><path d="M16 4l4 4-9 9"/></svg>';
    var tutorSvg = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';

    if (hl) {
      var ht = tile('Highlight', hlSvg);
      var syncHl = function () {
        var on = /sv-hl-mode/.test(document.body.className);
        ht.btn.classList.toggle('sv-tool-btn--active', on);
        ht.label.textContent = on ? 'Exit highlight' : 'Highlight';
      };
      ht.btn.addEventListener('click', function () {
        var on = /sv-hl-mode/.test(document.body.className);
        var t = document.querySelector(on ? '.sv-hl-fab--exit' : '.sv-hl-fab--enter');
        if (t) t.click();
        setTimeout(syncHl, 60);
      });
      syncHl();
    }
    if (tutor) {
      var tt = tile('Ask the tutor', tutorSvg);
      tt.btn.addEventListener('click', function () {
        var d = document.querySelector('.tutor-dock');
        if (d) (d.querySelector('button,[role="button"]') || d).click();
      });
    }
  }

  function revealMasthead() {
    var mh = document.querySelector('.lesson-masthead');
    if (!mh || mh.dataset.revealed) return;
    mh.dataset.revealed = '1';
    mh.classList.add('show-title');                                       // visible on load
    setTimeout(function () { mh.classList.remove('show-title'); }, 3000); // then fades to a clean image
  }

  function setupMediaLauncher() {
    var media = document.getElementById('sidebar-media');
    if (!media || media.dataset.launcher) return;
    var title = media.querySelector('.sidebar-section-title');
    var content = [].slice.call(media.children).filter(function (c) { return c !== title; });
    if (!content.length) return;
    media.dataset.launcher = '1';
    var count = media.querySelectorAll('a.sidebar-media-item').length;
    var modal = document.createElement('div');
    modal.className = 'rm-modal'; modal.hidden = true;
    modal.innerHTML = '<div class="rm-backdrop"></div><div class="rm-panel">'
      + '<button class="rm-close" aria-label="Close">×</button>'
      + '<h2 class="rm-title">Related media</h2><div class="rm-body"></div></div>';
    document.body.appendChild(modal);
    var mbody = modal.querySelector('.rm-body');
    content.forEach(function (n) { mbody.appendChild(n); }); // move real nodes (links keep working)
    var launcher = document.createElement('button');
    launcher.className = 'rm-launcher';
    launcher.innerHTML = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 9h18M9 14h6"/></svg>'
      + '<span class="rm-launcher-label">Browse related media</span>'
      + '<span class="rm-launcher-count">' + count + ' resources</span>';
    media.appendChild(launcher);
    function open() { modal.hidden = false; document.body.style.overflow = 'hidden'; }
    function close() { modal.hidden = true; document.body.style.overflow = ''; }
    launcher.addEventListener('click', open);
    modal.querySelector('.rm-close').addEventListener('click', close);
    modal.querySelector('.rm-backdrop').addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  function init() {
    document.body.appendChild(bar);
    set('reader');            // default to the bold structural redesign
    setTimeout(tidy, 1200);
    setTimeout(tidy, 2600);

    // EXPERIMENT: first scroll-down from the very top jumps past the hero to the content
    var jumpLock = false;
    window.addEventListener('wheel', function (e) {
      if (document.body.dataset.skin !== 'reader' || jumpLock) return;
      if (window.scrollY < 40 && e.deltaY > 0) {
        var lb = document.querySelector('#lesson-page .lesson-body');
        if (!lb) return;
        e.preventDefault();
        jumpLock = true;
        lb.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(function () { jumpLock = false; }, 1000);
      }
    }, { passive: false });
  }
  if (document.body) init(); else document.addEventListener('DOMContentLoaded', init);
})();
