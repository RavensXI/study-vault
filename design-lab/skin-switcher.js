/* Design-lab skin switcher — localhost + Vercel PREVIEW deployments only
   (the desk-world demo Tom can share). Never fires on the production domain.
   Not shipped; remove the <script> to drop it. */
(function () {
  var host = location.hostname;
  if (host !== '127.0.0.1' && host !== 'localhost' && !/\.vercel\.app$/.test(host)) return;

  // The Bindery brand kit is local-only (gitignored — trademark clearance
  // pending, must not enter the public repo). Only swap the wordmark when the
  // asset actually exists; deployed previews keep the StudyVault wordmark.
  // Bindery wordmark swap DISABLED (Tom, 9 Jul) — lessons show the StudyVault
  // wordmark again. To re-enable the Bindery masthead exploration, restore the
  // probe below (it adds .has-bindery when the local-only lockup asset exists).
  // var binderyProbe = new Image();
  // binderyProbe.onload = function () { document.body.classList.add('has-bindery'); };
  // binderyProbe.src = '/design-lab/assets/brand/bindery-lockup.svg';

  var SKINS = [['', 'Today'], ['reader', 'Reader'], ['desk', 'Desk'], ['paper', 'Paper'], ['ink', 'Ink'], ['crisp', 'Crisp']];

  var style = document.createElement('style');
  style.textContent =
    '#skin-lab{position:fixed;top:10px;right:12px;z-index:99999;display:flex;gap:.35rem;align-items:center;' +
    'background:#1b1916;color:#e8e2d6;font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;' +
    'padding:.45rem .6rem;border-radius:9px;box-shadow:0 6px 24px rgba(0,0,0,.35)}' +
    '#skin-lab b{color:#c9a23f;letter-spacing:.1em;text-transform:uppercase;margin-right:.4rem;font-weight:600}' +
    '#skin-lab button{font:inherit;cursor:pointer;background:transparent;color:#cdc6b8;border:1px solid #3a352d;' +
    'border-radius:5px;padding:.3rem .6rem}' +
    '#skin-lab button:hover{color:#fff;border-color:#6a6253}' +
    '#skin-lab button[aria-pressed="true"]{background:#c9a23f;color:#1b1916;border-color:#c9a23f;font-weight:600}' +
    '#hero-image.sv-lw-hold{opacity:0 !important}'; // held while the painted swap decides
  document.head.appendChild(style);

  var bar = document.createElement('div');
  bar.id = 'skin-lab';
  bar.innerHTML = '<b>Skin</b>' + SKINS.map(function (s) {
    return '<button data-skin="' + s[0] + '">' + s[1] + '</button>';
  }).join('');

  function set(skin) {
    // 'desk' = reader's structure wearing the illustrated-desk world:
    // warm paper, Bindery masthead, painted hero with the title below.
    var desk = skin === 'desk';
    var eff = desk ? 'reader' : skin;
    document.body.classList.toggle('desk-world', desk);
    if (eff) document.body.dataset.skin = eff; else delete document.body.dataset.skin;
    // ink IS a dark skin; otherwise leave dark-mode alone — it belongs to the
    // accessibility toolbar (prefs.darkMode), not the skin switcher.
    if (skin === 'ink') document.body.classList.add('dark-mode');
    applySubjectAccent();
    wireDeskHome();
    [].forEach.call(bar.querySelectorAll('button'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-skin') === skin);
    });
  }
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (b) set(b.getAttribute('data-skin'));
  });

  // LINE-AND-WASH PILOT (localhost only) — if a refined hero exists for this
  // lesson's hero image (built by _designlab_lw_pilot.py), swap it in so the
  // real lesson page shows the signature ink-and-wash treatment. Keyed by the
  // lesson's stored hero URL (query stripped); lessons with no refined variant
  // (e.g. Pro refused a person photo) simply keep their photo.
  // captions for OUR generated art (prompt-only where the source photo is
  // CC BY-SA): swapped heroes get the illustration caption, not the photo credit
  var LW_CAPTIONS = {
    'https://upload.wikimedia.org/wikipedia/commons/0/07/Gr%C3%A4f_%26_Stift_automobile_of_Archduke_Franz_Ferdinand_of_Austria-0486.jpg':
      'The Gräf & Stift touring car on the Appel Quay, Sarajevo, 28 June 1914 · ink & wash illustration',
    'https://upload.wikimedia.org/wikipedia/commons/3/39/Doom_painting%2C_St_Thomas%27s_church_-_geograph.org.uk_-_8141542.jpg':
      'A church Doom painting: Christ in judgement between heaven and hell · ink & wash illustration'
  };
  var LW_POS = {   // art-specific framing for swapped heroes
    'https://upload.wikimedia.org/wikipedia/commons/0/07/Gr%C3%A4f_%26_Stift_automobile_of_Archduke_Franz_Ferdinand_of_Austria-0486.jpg': 'center 62%'
  };
  var LW_MANIFEST = null;
  fetch('/design-lab/_lw_manifest.json')
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (m) { LW_MANIFEST = m || {}; trySwapHero(0); heroGuard(); })
    .catch(function () { LW_MANIFEST = {}; heroGuard(); });

  // ── no photo flash: the observer fires in the SAME task the loader sets the
  // hero src, so a to-be-painted photo is swapped before it can ever paint.
  // While the manifest is still in flight the hero is held invisible; pages
  // with no painted variant unhold as soon as the decision is in (2s cap).
  function unholdHero() {
    var img = document.getElementById('hero-image');
    if (img) img.classList.remove('sv-lw-hold');
  }
  function heroGuard() {
    var img = document.getElementById('hero-image');
    if (!img) return;
    var src = img.getAttribute('src');
    if (!src || img.dataset.lwSwapped) return;
    if (!LW_MANIFEST) { img.classList.add('sv-lw-hold'); return; }
    if (LW_MANIFEST[lwNorm(src)]) {
      img.classList.add('sv-lw-hold');
      trySwapHero(999);
      if (img.complete) unholdHero();
      else {
        img.addEventListener('load', unholdHero, { once: true });
        img.addEventListener('error', unholdHero, { once: true });
      }
    } else unholdHero();
  }
  (function () {
    var img = document.getElementById('hero-image');
    if (img) {
      new MutationObserver(heroGuard).observe(img, { attributes: true, attributeFilter: ['src'] });
      heroGuard();
    }
  })();
  setTimeout(unholdHero, 2000);   // safety: never leave a hero hidden
  // captions for the demo-path paintings live in a sidecar (generated by
  // scripts/_designlab_lw_demo_paths.py) — merge before/while swaps retry
  fetch('/design-lab/_lw_captions_demo.json')
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (c) {
      for (var k in c) if (!LW_CAPTIONS[k]) LW_CAPTIONS[k] = c[k];
      // if the hero swapped before this file landed, apply its caption now
      var img = document.getElementById('hero-image');
      var cap = img && LW_CAPTIONS[img.dataset.lwSrcKey];
      var capEl = document.getElementById('hero-caption');
      if (cap && capEl) capEl.textContent = cap;
    })
    .catch(function () {});
  function lwNorm(u) { return (u || '').split('?')[0]; }
  function trySwapHero(attempt) {
    if (!LW_MANIFEST) return;
    var img = document.getElementById('hero-image');
    if (!img || !img.getAttribute('src')) {
      if (attempt < 50) setTimeout(function () { trySwapHero(attempt + 1); }, 200);
      return;
    }
    if (img.dataset.lwSwapped) return;
    var lw = LW_MANIFEST[lwNorm(img.getAttribute('src'))] || LW_MANIFEST[lwNorm(img.src)];
    if (lw) {
      img.dataset.lwSwapped = '1'; img.removeAttribute('srcset');
      var srcKey = lwNorm(img.getAttribute('src'));
      img.dataset.lwSrcKey = srcKey;
      img.src = lw;
      var cap = LW_CAPTIONS[srcKey], capEl = document.getElementById('hero-caption');
      if (cap && capEl) capEl.textContent = cap;
      if (LW_POS[srcKey]) img.style.objectPosition = LW_POS[srcKey];
      // the video-overview card thumbnails the hero — keep it in the same world
      // whichever of the two built first (it snapshots hero src at build time)
      var vh = document.querySelector('.sv-video-hero');
      if (vh) vh.src = lw;
    }
  }

  // OLD production first-visit onboarding to strip in the reader redesign:
  // anon-welcome ("First time at StudyVault?"), whats-new ("recently built"
  // toast), lesson-tutorial tooltips, and any legacy coach/walkthrough/spotlight
  // — but NOT our own sv-tour feature tour.
  // NB: .sv-tutorial-spotlight is a MARKER the old loader tutorial puts on
  // REAL content (it hid/deleted the practice section on fresh visits) —
  // never match it, and clear any stranded markers.
  var OLD_ONBOARDING = '[class*="tour"]:not([class*="sv-tour"]),[class*="coach"],[class*="tutorial"]:not(.sv-tutorial-spotlight),[class*="walkthrough"],[class*="spotlight"]:not([class*="sv-tour"]):not(.sv-tutorial-spotlight),.anon-welcome-overlay,[class*="whats-new"]';
  function stripOldOnboarding(root) {
    (root || document).querySelectorAll(OLD_ONBOARDING).forEach(function (e) { e.remove(); });
    (root || document).querySelectorAll('.sv-tutorial-spotlight').forEach(function (e) {
      e.classList.remove('sv-tutorial-spotlight');
    });
  }
  // Remove the instant they're inserted (deferred onboarding scripts add them
  // after load) so they never flash. CSS in reskin also hides them from first
  // paint; this guarantees removal regardless of skin-CSS timing.
  function watchOldOnboarding() {
    if (!document.body || document.body.dataset.obWatch) return;
    document.body.dataset.obWatch = '1';
    stripOldOnboarding();
    coBrandSchoolLogo();   // relocate now if the logo was already injected
    new MutationObserver(function (muts) {
      for (var i = 0; i < muts.length; i++) {
        var added = muts[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if (n.matches && n.matches(OLD_ONBOARDING)) { n.remove(); continue; }
          if (n.querySelector && n.querySelector(OLD_ONBOARDING)) stripOldOnboarding(n);
        }
      }
      // school-session.js injects the logo mid-header after load — move it into
      // the wordmark lockup the instant it appears, so it doesn't flash centre
      // then jump left.
      coBrandSchoolLogo();
    }).observe(document.body, { childList: true, subtree: true });
  }

  // clear onboarding overlays + force scroll-reveal so the page is fully visible
  function tidy() {
    stripOldOnboarding();
    document.querySelectorAll('[class*="sv-reveal"],.lesson-header .lesson-number,.lesson-header h1,.lesson-hero-image,.lesson-sidebar,.study-notes > *,.exam-tip,.conclusion,.practice-section')
      .forEach(function (e) { e.classList.add('sv-visible'); });
    setupMediaLauncher();
    buildToolTiles();
    upgradePrimaryIcons();
    buildPracticeTile();
    buildPanelWrap();
    buildRichVideoThumb();
    buildDemoFigure();
    setupExitIntercept();
    fixLessonNavArrows();
    coBrandSchoolLogo();         // school account: lock the school logo beside the wordmark
    buildFocusToggle();          // before evenA11yDividers so it gets a divider
    buildOverlayControl();       // collapse the swatch row into a button + popover
    buildReadingPanel();         // A-/A+ + spacing + reading-font picker (replaces OpenDyslexic)
    killHighlighter();           // cut feature (Round 25) — clear any active mode + disable
    fixProgressCount();          // recount "X of N" from VISIBLE items (highlight task hidden)
    evenA11yDividers();
    revealMasthead();
    trySwapHero(0);              // line-and-wash pilot: swap in the refined hero if one exists
    buildTourReplay();
    buildUtilityRow();      // embed bug + replay-tour in the panel, under the video
    maybeStartTour();
  }

  // UTILITY BUTTONS (Tom, 14 Jun) — cutting the highlighter freed space at the
  // foot of the (sticky) panel; the bug + replay-tour buttons looked stray
  // floating in the corner. Embed them in the panel FLOW under the video as a
  // squared side-by-side pair. The floating .tutor-dock is retired (CSS hides
  // it; the panel tutor tile covers "Ask the Tutor"). lesson-tutor.js's
  // adoptBugButton tries to grab the bug ONCE — a small observer reclaims it
  // into our row if it does (microtask, so no visible flicker).
  function buildUtilityRow() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    if (!sidebar || !sidebar.dataset.panelWrap) return;   // wait until the panel is wrapped (so the row sits after the video, not swept into .sv-panel)
    var bug = document.querySelector('.bugr-fab');
    var tour = document.querySelector('.sv-tour-replay');
    var row = sidebar.querySelector('.sv-utility-row');
    if (!row) {
      row = document.createElement('div');
      row.className = 'sv-utility-row';
      sidebar.appendChild(row);   // after the video (sidebar's last child)
    }
    if (bug) {
      if (!bug.querySelector('.bugr-fab-label')) {
        var bl = document.createElement('span');
        bl.className = 'bugr-fab-label'; bl.textContent = 'Report a problem';
        bug.appendChild(bl);
      }
      if (bug.parentNode !== row) row.appendChild(bug);
      // reclaim if the tutor dock's adoptBugButton steals it back
      if (!sidebar.dataset.fabReclaim) {
        sidebar.dataset.fabReclaim = '1';
        new MutationObserver(function () {
          var b = document.querySelector('.bugr-fab');
          if (b && b.parentNode !== row && document.body.contains(row)) row.appendChild(b);
        }).observe(document.body, { childList: true, subtree: true });
      }
    }
    if (tour) {
      var ts = tour.querySelector('span'); if (ts) ts.textContent = 'Replay tour';
      if (tour.parentNode !== row) row.appendChild(tour);
    }
    if (tour && row.contains(tour)) row.classList.add('sv-util-ready');  // reveal once populated (no flash)
  }

  // persistent "replay the tour" control (bottom-left; the tour's last step
  // points at it). Clicking re-runs the tour from the start.
  function buildTourReplay() {
    if (document.querySelector('.sv-tour-replay')) return;
    var b = document.createElement('button');
    b.className = 'sv-tour-replay'; b.type = 'button';
    b.setAttribute('aria-label', 'Replay the page tour');
    b.setAttribute('title', 'Replay the page tour');
    b.innerHTML =
      '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<circle cx="12" cy="12" r="9"/>' +
      '<path d="M9.3 9.1a2.7 2.7 0 0 1 5.2 1c0 1.8-2.6 2.3-2.6 3.4"/>' +
      '<circle cx="12" cy="16.9" r="1" fill="currentColor" stroke="none"/></svg>' +
      '<span>Tour</span>';
    b.addEventListener('click', function () { startTour(); });
    document.body.appendChild(b);
  }

  // FEATURE TOUR (Tom, 13 Jun) — a clean first-visit walkthrough: dim the page,
  // spotlight one feature at a time, small caption card with Back/Next/Skip.
  // Shows once (localStorage); re-run anytime with window.svStartTour().
  var tourStarted = false, tourPolling = false;
  // A step targets one selector (sel) or a group whose union is spotlit (sels).
  // Steps whose targets are all absent/hidden are dropped (e.g. video).
  var TOUR_STEPS = [
    { sel: '.a11y-toolbar', pad: 6, title: 'Set up your reading',
      body: 'Dark mode, a dyslexia-friendly font, simpler language, bigger text and colour overlays — make the page comfortable to read.' },
    { trigger: 'bubbles', sel: '#lesson-page .study-notes p.sv-chunk', pad: 14, title: 'Stuck on a sentence?',
      body: 'Tap any paragraph and these options pop up — simplify the wording, have it explained a different way, or ask the tutor.' },
    { sel: '.key-fact', pad: 8, title: 'Helpers in the text',
      body: 'Key facts are boxed like this, underlined words show a definition when you tap them, and the lightbulbs offer quick revision tips as you read.' },
    { sel: '.sidebar-progress-section', pad: 8, title: 'Track your progress',
      body: 'This fills in as you work through the lesson, so you can always see how far you have got.' },
    { sels: ['.sidebar-knowledge-check', '.tile-practice'], pad: 10, title: 'Test yourself',
      body: 'Quick Quiz, Flashcards and exam-style Practice questions are all here — the fastest way to check what has stuck.' },
    { sels: ['.sidebar-media', '.tile-tutor'], pad: 10, title: 'Explore and dig in',
      body: 'Hand-picked media to go deeper, and a tutor on hand to explain anything a different way.' },
    { sel: '#sidebar-video-section .sidebar-video', pad: 8, title: 'Watch the overview',
      body: 'A short video explainer for the lesson. Tap it to play full-size.' },
    { sel: '.lesson-nav-link--next', pad: 8, title: 'Before you go',
      body: 'When you move to the next lesson, we’ll ask one question that links it back to something you already learned — that’s what makes it stick.' },
    { sel: '.sv-tour-replay', pad: 10, title: 'Replay any time',
      body: 'New to all this? Tap here whenever you like to run through the tour again.' }
  ];
  // first visible element of a step (for scrolling), and the union rect to spotlight
  function tourFirstEl(s) {
    var sels = s.sels || [s.sel];
    for (var i = 0; i < sels.length; i++) {
      var e = document.querySelector(sels[i]);
      if (e && e.getBoundingClientRect().height > 4) return e;
    }
    return null;
  }
  function tourRect(s) {
    var sels = s.sels || [s.sel], rects = [];
    sels.forEach(function (sel) {
      var e = document.querySelector(sel);
      if (e) { var r = e.getBoundingClientRect(); if (r.height > 4) rects.push(r); }
    });
    if (!rects.length) return null;
    var l = Math.min.apply(null, rects.map(function (r) { return r.left; }));
    var t = Math.min.apply(null, rects.map(function (r) { return r.top; }));
    var rt = Math.max.apply(null, rects.map(function (r) { return r.right; }));
    var b = Math.max.apply(null, rects.map(function (r) { return r.bottom; }));
    return { left: l, top: t, right: rt, bottom: b, width: rt - l, height: b - t };
  }
  function maybeStartTour() {
    if (tourPolling || tourStarted) return;
    if (new URLSearchParams(location.search).get('notour') === '1')
      try { localStorage.setItem('sv-reader-tour-v1', '1'); } catch (e) {}   // QA staging
    if (localStorage.getItem('sv-reader-tour-v1')) return;
    tourPolling = true;
    // poll until the async-loaded panel + a11y bar exist (fixed tidy timers
    // can fire before the loader finishes), then start once
    (function poll(n) {
      if (tourStarted || localStorage.getItem('sv-reader-tour-v1')) { tourPolling = false; return; }
      if (document.querySelector('.sv-panel') && document.querySelector('.a11y-toolbar')) {
        tourPolling = false; startTour(); return;
      }
      if (n > 0) setTimeout(function () { poll(n - 1); }, 500);
      else tourPolling = false;
    })(20);
  }
  function startTour() {
    if (document.querySelector('.sv-tour-card')) return;
    tourStarted = true;
    // keep a step if its target exists (or, for a triggered step, its required
    // source element exists — the spotlight target appears once triggered)
    var steps = TOUR_STEPS.filter(function (s) {
      return s.req ? document.querySelector(s.req) : tourRect(s);
    });
    if (!steps.length) return;
    // The paragraph-menu step shows a STATIC replica of the simplify / explain /
    // ask-the-tutor menu over the first paragraph (reliable — no dependency on
    // simplify's fragile open/close + scroll-dismiss timing). Same look.
    var demoMenu = null;
    var DEMO_OPTS = [
      ['Simplify wording', '<path d="M4 7h16"/><path d="M4 12h10"/><path d="M4 17h7"/>'],
      ['Explain it differently', '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>'],
      ['Ask the tutor', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>']
    ];
    function showDemoMenu() {
      var p = document.querySelector('#lesson-page .study-notes p.sv-chunk') ||
              document.querySelector('#lesson-page .study-notes p');
      if (!p) return;
      if (!demoMenu) {
        demoMenu = document.createElement('div');
        demoMenu.className = 'sv-tour-demo-menu';
        demoMenu.innerHTML = DEMO_OPTS.map(function (o) {
          return '<span class="sv-tour-demo-bubble" title="' + o[0] + '">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
            'stroke-linecap="round" stroke-linejoin="round">' + o[1] + '</svg></span>';
        }).join('');
        document.body.appendChild(demoMenu);
      }
      var r = p.getBoundingClientRect();
      demoMenu.style.left = Math.round(r.left + 26) + 'px';
      demoMenu.style.top = Math.round(r.top + r.height / 2 - 23) + 'px';
      demoMenu.style.display = 'flex';
    }
    function hideDemoMenu() { if (demoMenu) demoMenu.style.display = 'none'; }
    var i = 0;
    function el(tag, cls) { var e = document.createElement(tag); e.className = cls; return e; }
    var block = el('div', 'sv-tour-block');
    var spot = el('div', 'sv-tour-spot');
    var card = el('div', 'sv-tour-card');
    card.innerHTML =
      '<div class="sv-tour-kicker"></div>' +
      '<div class="sv-tour-title"></div>' +
      '<p class="sv-tour-body"></p>' +
      '<div class="sv-tour-foot"><span class="sv-tour-dots">' +
        steps.map(function () { return '<i></i>'; }).join('') +
      '</span><span class="sv-tour-btns">' +
        '<button type="button" class="sv-tour-skip" data-act="skip">Skip</button>' +
        '<button type="button" class="sv-tour-back" data-act="back">Back</button>' +
        '<button type="button" class="sv-tour-next" data-act="next">Next</button>' +
      '</span></div>';
    document.body.appendChild(block);
    document.body.appendChild(spot);
    document.body.appendChild(card);

    // place the card on the side of the spotlight with the most room, clamped
    // on-screen, never overlapping the spot
    function placeCard(r) {
      var cw = card.offsetWidth, ch = card.offsetHeight, vw = innerWidth, vh = innerHeight, m = 14, g = 18, left, top;
      var roomBelow = vh - r.bottom, roomAbove = r.top, roomRight = vw - r.right, roomLeft = r.left;
      if (roomRight >= cw + g) {                 // to the right of the spotlight
        left = r.right + g; top = clamp(r.top, m, vh - ch - m);
      } else if (roomLeft >= cw + g) {           // to the left
        left = r.left - cw - g; top = clamp(r.top, m, vh - ch - m);
      } else if (roomBelow >= ch + g) {          // below
        top = r.bottom + g; left = clamp(r.left, m, vw - cw - m);
      } else {                                   // above
        top = Math.max(m, r.top - ch - g); left = clamp(r.left, m, vw - cw - m);
      }
      card.style.left = left + 'px'; card.style.top = top + 'px';
    }
    function clamp(v, lo, hi) { return Math.max(lo, Math.min(v, hi)); }
    // keep the spotlight (and card) glued to the current step's target every
    // frame — rides the element as the page settles, no glide-vs-scroll snap
    function syncSpot() {
      var s = steps[i], r = tourRect(s); if (!r) return;
      var pad = s.pad || 8;
      spot.style.left = (r.left - pad) + 'px'; spot.style.top = (r.top - pad) + 'px';
      spot.style.width = (r.width + pad * 2) + 'px'; spot.style.height = (r.height + pad * 2) + 'px';
      placeCard(r);
    }
    function fadeIn() { setTimeout(function () { spot.style.opacity = '1'; card.style.opacity = '1'; }, 30); }
    // reposition while the card is faded out: the spot relocates in one clean
    // instant move (no glide-under-then-snap), the card cross-fades the step
    function reposition(n) {
      i = n;
      var s = steps[n];
      card.querySelector('.sv-tour-kicker').textContent = 'Step ' + (n + 1) + ' of ' + steps.length;
      card.querySelector('.sv-tour-title').textContent = s.title;
      card.querySelector('.sv-tour-body').textContent = s.body;
      card.querySelector('.sv-tour-back').style.visibility = n === 0 ? 'hidden' : 'visible';
      card.querySelector('.sv-tour-next').textContent = n === steps.length - 1 ? 'Done' : 'Next';
      [].forEach.call(card.querySelectorAll('.sv-tour-dots i'), function (d, k) { d.classList.toggle('on', k === n); });
      hideDemoMenu();
      if (s.trigger === 'bubbles') {
        var p = document.querySelector('#lesson-page .study-notes p.sv-chunk') ||
                document.querySelector('#lesson-page .study-notes p');
        if (p) p.scrollIntoView({ block: 'center', behavior: 'auto' });
        showDemoMenu();
        syncSpot();
        transitioning = false;
        fadeIn();
        return;
      }
      var first = tourFirstEl(s);
      if (first) first.scrollIntoView({ block: 'center', behavior: 'auto' });
      syncSpot();
      transitioning = false;
      fadeIn();
    }
    var firstShow = true, transitioning = false;
    function show(n) {
      if (firstShow) { firstShow = false; reposition(n); return; }  // no fade-out on first
      transitioning = true;                                  // freeze the tracker
      spot.style.opacity = '0'; card.style.opacity = '0';    // whole spotlight fades out as ONE
      setTimeout(function () { reposition(n); }, 200);        // move unseen, then fade back in
    }
    // glue spot + card to the target (paused mid-transition so it relocates once)
    var tracker = setInterval(function () { if (!transitioning) syncSpot(); }, 90);
    // lock the page: programmatic scrollIntoView still works, the user can't
    // scroll the highlighted element out from under the spotlight
    function preventScroll(e) { e.preventDefault(); }
    function preventScrollKeys(e) {
      if (e.target.closest('.sv-tour-card')) return;
      if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' ', 'Spacebar'].indexOf(e.key) !== -1) e.preventDefault();
    }
    window.addEventListener('wheel', preventScroll, { passive: false });
    window.addEventListener('touchmove', preventScroll, { passive: false });
    window.addEventListener('keydown', preventScrollKeys, true);
    function finish() {
      localStorage.setItem('sv-reader-tour-v1', '1');
      clearInterval(tracker);
      window.removeEventListener('wheel', preventScroll, { passive: false });
      window.removeEventListener('touchmove', preventScroll, { passive: false });
      window.removeEventListener('keydown', preventScrollKeys, true);
      if (demoMenu) demoMenu.remove();
      [block, spot, card].forEach(function (e) { e.remove(); });
      document.removeEventListener('keydown', onKey);
      tourStarted = false;
    }
    function onKey(e) {
      if (e.key === 'Escape') finish();
      else if (e.key === 'ArrowRight') (i < steps.length - 1 ? show(i + 1) : finish());
      else if (e.key === 'ArrowLeft' && i > 0) show(i - 1);
    }
    card.addEventListener('click', function (e) {
      var b = e.target.closest('[data-act]'); if (!b) return;
      var a = b.getAttribute('data-act');
      if (a === 'skip') finish();
      else if (a === 'back') { if (i > 0) show(i - 1); }
      else { if (i < steps.length - 1) show(i + 1); else finish(); }
    });
    document.addEventListener('keydown', onKey);
    show(0);
  }
  window.svStartTour = startTour;   // re-run from console any time

  // Normalise the a11y bar's dividers: the markup's .a11y-separator spans are
  // inconsistent (missing between Simplify and the font-size group). Drop them
  // and insert one .a11y-divider before each top-level control, so with the
  // toolbar's space-between a divider sits centred in every gap, evenly.
  function evenA11yDividers() {
    var tb = document.querySelector('.a11y-toolbar');
    if (!tb || tb.dataset.evenDiv) return;
    if (!tb.querySelector('.a11y-overlay-group')) return;   // wait for full bar
    tb.dataset.evenDiv = '1';
    [].forEach.call(tb.querySelectorAll('.a11y-separator'), function (s) { s.remove(); });
    var controls = [].filter.call(tb.children, function (c) {
      return c.classList.contains('a11y-btn') ||
             c.classList.contains('a11y-font-size-group') ||
             c.classList.contains('a11y-overlay-group');
    });
    controls.forEach(function (c) {
      var d = document.createElement('span');
      d.className = 'a11y-divider';
      tb.insertBefore(d, c);
    });
    // terminal spacer so the last control (Overlay) centres in its slot rather
    // than hugging the right edge (space-between pins the final item to the edge)
    if (!tb.querySelector('.a11y-bar-end')) {
      var end = document.createElement('span');
      end.className = 'a11y-bar-end';
      tb.appendChild(end);
    }
  }

  // FOCUS MODE (Tom, 13 Jun) — replaces the highlighter. A Reading-bar toggle
  // that dims the article into a soft gradient: the paragraph at your reading
  // line is full-contrast, the rest ease out the further they are, so text
  // comes into focus as you scroll. Keeps text size unchanged (readable).
  var focusOn = false, focusRAF = false;
  function focusUpdate() {
    if (!focusOn) return;
    var vh = window.innerHeight;
    var center = vh * 0.40;          // focal line, a touch above middle
    var dead = vh * 0.085;           // crisp band: the line you're on stays razor-sharp
    var span = vh * 0.52;            // distance over which it fully defocuses
    [].forEach.call(document.querySelectorAll('#lesson-page .study-notes > *'), function (p) {
      var r = p.getBoundingClientRect();
      // distance to the NEAREST EDGE (0 if the focal line runs through it), so a
      // tall paragraph you're reading stays lit instead of dimming by its midpoint.
      // Symmetric: text scrolled PAST (above) defocuses just like text ahead (below).
      var d = center < r.top ? r.top - center : (center > r.bottom ? center - r.bottom : 0);
      var t = Math.min(1, Math.max(0, d - dead) / span);   // 0 = sharp, 1 = fully out
      p.style.opacity = (1 - t * 0.82).toFixed(3);          // 1.0 → ~0.18
      p.style.filter = t > 0.02 ? 'blur(' + (t * 3.6).toFixed(2) + 'px)' : '';  // depth-of-field defocus
    });
  }
  function clearFocus() {
    [].forEach.call(document.querySelectorAll('#lesson-page .study-notes > *'), function (p) { p.style.opacity = ''; p.style.filter = ''; });
  }
  function setFocus(on, silent) {
    focusOn = on;
    document.body.classList.toggle('sv-focus-mode', on);
    var b = document.querySelector('.a11y-focus-toggle');
    if (b) b.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (!silent) localStorage.setItem('sv-focus-mode', on ? '1' : '0');
    if (on) focusUpdate(); else clearFocus();
  }
  window.addEventListener('scroll', function () {
    if (!focusOn || focusRAF) return;
    focusRAF = true; requestAnimationFrame(function () { focusRAF = false; focusUpdate(); });
  }, { passive: true });
  // Focus mode's per-paragraph filter:blur + will-change promotes each paragraph
  // to its own compositor layer, which ESCAPES the frosting modals' backdrop-filter
  // (the lesson text stayed sharp behind the frost). While any frosting modal is
  // open, flag the body so CSS drops that blur and the backdrop frosts uniformly.
  (function watchFrostModals() {
    if (!document.body || document.body.dataset.frostWatch) return;
    document.body.dataset.frostWatch = '1';
    var SEL = '.kc-overlay, .fc-modal-overlay, .pq-backdrop, .sv-exit-backdrop';
    // VISIBLE, not merely present: the practice .pq-backdrop lives in the DOM
    // permanently and is toggled via its modal's `hidden` attribute, so check
    // for rendered client rects (0 when an ancestor is display:none).
    function visible(el) { return el && el.getClientRects().length > 0; }
    function sync() {
      var open = [].some.call(document.querySelectorAll(SEL), visible);
      var was = document.body.classList.contains('sv-modal-open');
      if (open === was) return;
      document.body.classList.toggle('sv-modal-open', open);
      if (was && !open && focusOn) focusUpdate();   // restore the gradient on close
    }
    // childList catches KC/flashcard overlays (added/removed); attributeFilter
    // ['hidden'] catches the practice modal (toggled, not re-created). NOT 'style'
    // — the focus engine mutates paragraph styles every scroll frame and would
    // spam the observer.
    new MutationObserver(sync).observe(document.body,
      { childList: true, subtree: true, attributes: true, attributeFilter: ['hidden'] });
  })();
  function buildFocusToggle() {
    var tb = document.querySelector('.a11y-toolbar');
    if (!tb || tb.dataset.focusBtn) return;
    var simplify = tb.querySelector('.a11y-simplify-toggle');
    if (!simplify) return;                              // wait for the toolbar
    tb.dataset.focusBtn = '1';
    var b = document.createElement('button');
    b.className = 'a11y-btn a11y-focus-toggle';
    b.setAttribute('aria-pressed', 'false');
    b.setAttribute('title', 'Focus mode — eases everything but what you’re reading');
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/></svg>' +
      '<span>Focus</span>';
    simplify.parentNode.insertBefore(b, simplify.nextSibling);   // group with the other toggles
    b.addEventListener('click', function () { setFocus(!focusOn); });
    if (localStorage.getItem('sv-focus-mode') === '1') setFocus(true, true);
  }

  // HIGHLIGHTER CUT (Tom, 14 Jun) — the feature was replaced by Focus mode
  // (Round 25), but production still builds its triggers: the "Highlight notes"
  // checklist task (data-task="highlight-mode", in the sidebar progress section
  // AND the gutter rail) and the floating FAB. The triggers are hidden via
  // reskin CSS; here we clear any ACTIVE highlight mode (marker cursor /
  // ::selection colour) and set sv-hl-enabled=0 so it won't bootstrap a FAB or
  // re-apply stored highlights on future loads.
  function killHighlighter() {
    var b = document.body;
    b.classList.remove('sv-hl-mode', 'sv-hl-color-yellow', 'sv-hl-color-green', 'sv-hl-color-pink', 'sv-hl-color-blue');
    try { localStorage.setItem('sv-hl-mode', '0'); localStorage.setItem('sv-hl-enabled', '0'); } catch (e) {}
  }

  // With the highlight task hidden, main.js's "X of N complete" still counts it
  // (N = tasks.length). Recompute from the VISIBLE items instead, and keep it
  // corrected via an observer — syncAll() rewrites the summary + bar on every
  // task completion, so a one-shot fix would revert. The "only write if changed"
  // guard stops the observer looping on its own edits.
  function fixProgressCount() {
    var section = document.querySelector('.sidebar-progress-section');
    if (!section) return;
    function apply() {
      var summary = section.querySelector('.lesson-progress-summary');
      if (!summary) return;
      var items = [].slice.call(section.querySelectorAll('.lesson-progress-item'))
        .filter(function (it) { return it.getClientRects().length > 0; });   // exclude the hidden highlight task
      var total = items.length;
      var done = items.filter(function (it) { return it.classList.contains('completed'); }).length;
      var wp = section.dataset.svPct;
      var want = done + ' of ' + total + (wp !== undefined ? ' · ' + wp + '%' : ' complete');
      if (summary.textContent !== want) summary.textContent = want;
      if (!section.dataset.doneTip) { section.dataset.doneTip = '1';
        var bar0 = section.querySelector('.lesson-progress-bar');
        if (bar0) bar0.title = 'The dashes mark the done line — a lesson counts as complete from 50%'; }
      var fill = section.querySelector('.lesson-progress-bar-fill');
      // the bar shows WEIGHTED depth (LESSON_COMPLETION_SPEC.md) when main.js
      // provides it; the count-based fallback covers older pages
      var wpct = section.dataset.svPct !== undefined ? section.dataset.svPct
        : (total ? Math.round(done / total * 100) : 0);
      if (fill) { var w = wpct + '%'; if (fill.style.width !== w) fill.style.width = w; }
    }
    apply();
    if (!section.dataset.countFix) {
      section.dataset.countFix = '1';
      new MutationObserver(apply).observe(section,
        { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['class', 'style'] });
    }
  }

  // OVERLAY CONTROL (Tom, 13 Jun) — the bare swatch row ate the bar and the
  // pastel tints were too weak to help anyone who needs them. Collapse it to a
  // single "Overlay" button that opens a popover holding the colours + an
  // INTENSITY slider. The original swatch <button>s are MOVED (not rebuilt)
  // into the popover, so main.js's setOverlay() wiring keeps working untouched;
  // we only add the trigger, the slider, and a current-colour dot.
  // Deeper tints live in reskin.css; keep this map in sync with them so the
  // chips preview the real colour. Intensity drives --overlay-intensity (the
  // ::after opacity) and persists in the same studyvault-a11y prefs blob.
  var OV_COL = { yellow: '#fde047', blue: '#93c5fd', pink: '#f9a8d4', green: '#86efac', peach: '#fdba74', aqua: '#67e8f9' };
  function ovPrefs() { try { return JSON.parse(localStorage.getItem('studyvault-a11y')) || {}; } catch (e) { return {}; } }
  function applyOvIntensity(v) { document.body.style.setProperty('--overlay-intensity', (v / 100).toFixed(2)); }
  function buildOverlayControl() {
    var tb = document.querySelector('.a11y-toolbar');
    if (!tb) return;
    var group = tb.querySelector('.a11y-overlay-group');
    if (!group || group.dataset.collapsed) return;
    var swatches = [].slice.call(group.querySelectorAll('.a11y-overlay'));
    if (!swatches.length) return;
    group.dataset.collapsed = '1';

    var label = group.querySelector('.a11y-overlay-label');
    if (label) label.style.display = 'none';

    // trigger button, styled like the other a11y controls
    var btn = document.createElement('button');
    btn.className = 'a11y-btn a11y-overlay-toggle';
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('title', 'Colour overlay');
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5c3.2 3.9 5.5 6.7 5.5 9.4a5.5 5.5 0 0 1-11 0c0-2.7 2.3-5.5 5.5-9.4z"/></svg>' +
      '<span>Overlay</span><span class="a11y-overlay-dot" hidden></span>';
    group.appendChild(btn);

    // popover (appended to body, fixed + above the tint sheet so chips read true)
    var pop = document.createElement('div');
    pop.className = 'a11y-overlay-pop'; pop.hidden = true;
    var chips = document.createElement('div'); chips.className = 'a11y-overlay-chips';
    swatches.forEach(function (sw) {
      if (sw.dataset.overlay) sw.style.background = OV_COL[sw.dataset.overlay] || sw.style.background;
      chips.appendChild(sw);
    });
    var intRow = document.createElement('div'); intRow.className = 'a11y-overlay-intensity';
    var intLabel = document.createElement('span'); intLabel.textContent = 'Intensity';
    var range = document.createElement('input');
    range.type = 'range'; range.min = '10'; range.max = '100'; range.step = '5';
    range.setAttribute('aria-label', 'Overlay intensity');
    intRow.appendChild(intLabel); intRow.appendChild(range);
    pop.appendChild(chips); pop.appendChild(intRow);
    document.body.appendChild(pop);

    // intensity: load saved (default 45), apply, persist on input
    var saved = ovPrefs().overlayIntensity;
    if (typeof saved !== 'number') saved = 45;
    range.value = saved; applyOvIntensity(saved);
    range.addEventListener('input', function () {
      applyOvIntensity(this.value);
      var p = ovPrefs(); p.overlayIntensity = +this.value;
      try { localStorage.setItem('studyvault-a11y', JSON.stringify(p)); } catch (e) {}
    });

    // dot reflects the active swatch (main.js toggles .active on the buttons)
    function updateDot() {
      var on = chips.querySelector('.a11y-overlay.active');
      var col = on && on.dataset.overlay;
      var dot = btn.querySelector('.a11y-overlay-dot');
      if (col) { dot.hidden = false; dot.style.background = OV_COL[col] || ''; btn.classList.add('on'); }
      else { dot.hidden = true; btn.classList.remove('on'); }
    }
    swatches.forEach(function (sw) { sw.addEventListener('click', updateDot); });
    updateDot();

    // open / close + viewport-aware placement (right-aligned under the trigger)
    function place() { placePop(btn, pop, 244); }
    function openPop() { pop.hidden = false; place(); btn.setAttribute('aria-expanded', 'true'); }
    function closePop() { pop.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); pop.hidden ? openPop() : closePop(); });
    document.addEventListener('click', function (e) {
      if (!pop.hidden && !pop.contains(e.target) && !btn.contains(e.target)) closePop();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !pop.hidden) closePop(); });
    window.addEventListener('resize', function () { if (!pop.hidden) place(); });
    window.addEventListener('scroll', function () { if (!pop.hidden) place(); }, { passive: true });
  }

  // Shared popover placement: right-aligned to the trigger, FLIPS above it
  // when the viewport below is cramped, clamps to a scrollable max-height,
  // and is re-placed on scroll so it stays glued to its button. (Fixes: menu
  // opened near the bottom was cut off and unreachable — it neither scrolled
  // with the page nor within itself.)
  function placePop(btn, pop, defW) {
    var r = btn.getBoundingClientRect();
    var h = pop.offsetHeight || 320;
    var below = window.innerHeight - r.bottom - 17;
    var above = r.top - 17;
    var top;
    if (below < h && above > below) {
      pop.style.maxHeight = Math.min(h, above) + 'px';
      top = Math.max(8, r.top - 9 - Math.min(h, above));
    } else {
      pop.style.maxHeight = Math.max(120, below) + 'px';
      top = r.bottom + 9;
    }
    pop.style.top = top + 'px';
    var w = pop.offsetWidth || defW;
    pop.style.left = Math.max(8, Math.min(r.right - w, window.innerWidth - w - 8)) + 'px';
  }

  // READ YOUR WAY (Tom, 13 Jun) — one popover for text size + spacing + reading
  // font, replacing the inline A-/A+ group and the OpenDyslexic toggle. Per the
  // dyslexia-font report: OpenDyslexic is deprecated (null/negative evidence);
  // the win is adjustable SPACING (the crowding lever) plus a small choice of
  // disambiguation-first reading faces — Atkinson Hyperlegible + Andika. The
  // existing A-/A+ buttons are MOVED in (main.js wiring intact); spacing drives
  // --read-space; font sets an inline --font-read. Persists in studyvault-a11y.
  var RD_FONTS = [
    { key: 'default', name: 'Default', note: 'Literata', css: "'Literata',Georgia,serif" },
    { key: 'atkinson', name: 'Atkinson Hyperlegible', note: 'Clear letter shapes', css: "'Atkinson Hyperlegible',sans-serif" },
    { key: 'andika', name: 'Andika', note: 'Soft, literacy-friendly', css: "'Andika',sans-serif" }
  ];
  function rdPrefs() { try { return JSON.parse(localStorage.getItem('studyvault-a11y')) || {}; } catch (e) { return {}; } }
  function rdSave(patch) { var p = rdPrefs(); for (var k in patch) p[k] = patch[k]; try { localStorage.setItem('studyvault-a11y', JSON.stringify(p)); } catch (e) {} }
  function rdApplyFont(css) { if (css) document.body.style.setProperty('--font-read', css); else document.body.style.removeProperty('--font-read'); }
  function rdApplySpace(v) { document.body.style.setProperty('--read-space', (v / 100).toFixed(2)); }
  function buildReadingPanel() {
    var tb = document.querySelector('.a11y-toolbar');
    if (!tb || tb.dataset.readingPanel) return;
    var sizeGroup = tb.querySelector('.a11y-font-size-group');
    if (!sizeGroup) return;                 // wait for the full bar
    tb.dataset.readingPanel = '1';

    // deprecate OpenDyslexic: remove the toggle + strip any persisted class
    var dys = tb.querySelector('.a11y-dyslexia-toggle');
    if (dys) dys.remove();
    document.body.classList.remove('dyslexia-font');

    // trigger button (placed where A-/A+ used to sit — before the overlay group)
    var btn = document.createElement('button');
    btn.className = 'a11y-btn a11y-reading-toggle';
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('title', 'Read your way — size, spacing and reading fonts');
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V5h16v2"/><path d="M9 5v14"/>' +
      '<path d="M7 19h4"/><path d="M15 13v-1h6v1"/><path d="M18 12v7"/><path d="M16.5 19h3"/></svg>' +
      '<span>Read your way</span>';
    var ovGroup = tb.querySelector('.a11y-overlay-group');
    tb.insertBefore(btn, ovGroup || null);

    // popover
    var pop = document.createElement('div');
    pop.className = 'a11y-reading-pop'; pop.hidden = true;

    // SIZE — relocate the existing A-/A+ group (keeps main.js setFontSize wiring)
    var s1 = document.createElement('div'); s1.className = 'a11y-rd-section';
    s1.innerHTML = '<span class="a11y-rd-label">Text size</span>';
    s1.appendChild(sizeGroup);

    // SPACING — slider drives --read-space
    var s2 = document.createElement('div'); s2.className = 'a11y-rd-section';
    s2.innerHTML = '<span class="a11y-rd-label">Line &amp; letter spacing</span>';
    var range = document.createElement('input');
    range.type = 'range'; range.min = '0'; range.max = '100'; range.step = '5';
    range.className = 'a11y-rd-slider'; range.setAttribute('aria-label', 'Line and letter spacing');
    s2.appendChild(range);

    // FONT — pick-list, each previewed in its own face
    var s3 = document.createElement('div'); s3.className = 'a11y-rd-section';
    s3.innerHTML = '<span class="a11y-rd-label">Reading font</span>';
    var fonts = document.createElement('div'); fonts.className = 'a11y-rd-fonts';
    s3.appendChild(fonts);

    pop.appendChild(s1); pop.appendChild(s2); pop.appendChild(s3);
    document.body.appendChild(pop);

    // ---- spacing wiring ----
    var savedSpace = rdPrefs().readingSpace;
    if (typeof savedSpace !== 'number') savedSpace = 0;
    range.value = savedSpace; rdApplySpace(savedSpace);
    range.addEventListener('input', function () { rdApplySpace(this.value); rdSave({ readingSpace: +this.value }); });

    // ---- font wiring ----
    function setFontActive(key) {
      [].forEach.call(fonts.children, function (b) { b.classList.toggle('active', b.dataset.font === key); });
      btn.classList.toggle('on', key && key !== 'default');   // lit when a reading-aid face is on
    }
    RD_FONTS.forEach(function (f) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'a11y-rd-font'; b.dataset.font = f.key;
      b.innerHTML = '<span><span style="font-family:' + f.css + '">' + f.name + '</span>' +
        '<small>' + f.note + '</small></span><span class="a11y-rd-check">✓</span>';
      b.addEventListener('click', function () { rdApplyFont(f.key === 'default' ? '' : f.css); setFontActive(f.key); rdSave({ readingFont: f.key }); });
      fonts.appendChild(b);
    });
    var savedFont = rdPrefs().readingFont || 'default';
    var sf = RD_FONTS.filter(function (f) { return f.key === savedFont; })[0] || RD_FONTS[0];
    rdApplyFont(sf.key === 'default' ? '' : sf.css); setFontActive(sf.key);

    // ---- reset: size + spacing + font back to StudyVault defaults ----
    var reset = document.createElement('button');
    reset.type = 'button'; reset.className = 'a11y-rd-reset';
    reset.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>' +
      '<span>Reset to default</span>';
    reset.addEventListener('click', function () {
      rdApplyFont(''); setFontActive('default');
      range.value = 0; rdApplySpace(0);
      rdSave({ readingFont: 'default', readingSpace: 0 });
      // size back to step 0 by driving the real A-/A+ buttons (keeps main.js synced)
      var cls = document.body.className;
      var step = /font-size-down-1/.test(cls) ? -1 : /font-size-up-1/.test(cls) ? 1 : /font-size-up-2/.test(cls) ? 2 : 0;
      var up = sizeGroup.querySelector('.a11y-font-up'), down = sizeGroup.querySelector('.a11y-font-down');
      while (step < 0) { up.click(); step++; }
      while (step > 0) { down.click(); step--; }
    });
    pop.appendChild(reset);

    // ---- open / close + placement (right-aligned under the trigger) ----
    function place() { placePop(btn, pop, 282); }
    function openPop() { pop.hidden = false; place(); btn.setAttribute('aria-expanded', 'true'); }
    function closePop() { pop.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); pop.hidden ? openPop() : closePop(); });
    document.addEventListener('click', function (e) {
      if (!pop.hidden && !pop.contains(e.target) && !btn.contains(e.target)) closePop();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !pop.hidden) closePop(); });
    window.addEventListener('resize', function () { if (!pop.hidden) place(); });
    window.addEventListener('scroll', function () { if (!pop.hidden) place(); }, { passive: true });
  }

  // SCHOOL CO-BRAND (Tom, 14 Jun) — on a school account, school-session.js
  // injects .header-school-logo before the nav. Move it INTO .header-brand so it
  // forms a "StudyVault │ Unity College" lockup beside the wordmark and travels
  // with it (incl. the ≥1400px gutter position). No-op for free/anon users.
  function coBrandSchoolLogo() {
    var brand = document.querySelector('.header-brand');
    var logo = document.querySelector('.header-school-logo');
    if (!brand || !logo || brand.dataset.cobrand) return;
    brand.dataset.cobrand = '1';
    var divider = document.createElement('span');
    divider.className = 'header-cobrand-divider';
    divider.setAttribute('aria-hidden', 'true');
    brand.appendChild(divider);
    brand.appendChild(logo);   // relocate the injected logo into the lockup
  }

  // The loader bakes literal ← / → glyphs into the Prev/Next labels — they read
  // cheap. Strip them and substitute a refined stroked SVG arrow beside the
  // text (prev = leading left arrow, next = trailing right arrow).
  function fixLessonNavArrows() {
    [['#nav-prev-lesson', false], ['#nav-next-lesson', true]].forEach(function (pair) {
      var a = document.querySelector(pair[0]);
      if (!a || a.dataset.arrowFixed) return;
      var isNext = pair[1];
      var label = a.textContent.replace(/[←→]/g, '').trim();
      if (!label) return;
      a.dataset.arrowFixed = '1';
      var head = isNext
        ? '<line x1="4" y1="12" x2="18" y2="12"/><polyline points="12 6 18 12 12 18"/>'
        : '<line x1="20" y1="12" x2="6" y2="12"/><polyline points="12 6 6 12 12 18"/>';
      var arrow = '<svg class="nav-arrow" viewBox="0 0 24 24" width="15" height="15" fill="none" ' +
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + head + '</svg>';
      var span = '<span>' + label + '</span>';
      a.innerHTML = isNext ? (span + arrow) : (arrow + span);
    });
  }

  // DEMO: L7 has no real video, but Tom wants to SEE the corner player card.
  // Upgrade the REAL R2/Drive video card (loader-rendered "thumb + play"
  // variant) into a YouTube-style thumbnail composed from the lesson's own
  // hero image. Only swaps the card's VISUAL children, never the container,
  // so the loader's click->openVideoModal listener survives. YouTube embeds
  // (iframe, no play button) keep their own thumbnail and are left alone.
  function buildRichVideoThumb() {
    var card = document.querySelector('#sidebar-video-section .sidebar-video');
    if (!card || card.dataset.richThumb) return;
    // only the R2/Drive play-card has a play button or generic thumb; an empty
    // iframe means the loader hasn't finished yet — bail and catch it next tidy
    if (!card.querySelector('.sidebar-video-play') && !card.querySelector('.sidebar-video-thumb')) return;
    card.dataset.richThumb = '1';

    var hero = document.getElementById('hero-image');
    var heroSrc = hero && hero.src ? hero.src : '';
    var title = (document.getElementById('lesson-title') || {}).textContent || '';
    card.classList.add('sv-video-thumb-rich');
    card.innerHTML =
      (heroSrc ? '<img class="sv-video-hero" alt="">' : '') +
      '<div class="sv-video-scrim"></div>' +
      '<span class="sv-video-dur"></span>' +   /* filled from the real file below */
      '<button class="sidebar-video-play" aria-label="Play video overview">' +
        '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 19,12 8,19"/></svg>' +
      '</button>' +
      '<div class="sv-video-meta">' +
        '<span class="sv-video-kicker">Video overview</span>' +
        '<span class="sv-video-ttl"></span>' +
      '</div>';
    if (heroSrc) card.querySelector('.sv-video-hero').src = heroSrc;
    card.querySelector('.sv-video-ttl').textContent = title;
    fillVideoDuration(card.querySelector('.sv-video-dur'));
  }

  // Read the true running time off the real R2 MP4 (the <video> element
  // exposes .duration once metadata loads). Only direct-file videos expose
  // this; Drive/YouTube embeds don't, so the badge stays hidden (:empty).
  function fillVideoDuration(badge) {
    if (!badge || !window.supabase || !window._lessonId) return;
    var c = window.supabase.createClient(
      'https://baipckgywpnwapobwtsy.supabase.co',
      'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
    );
    c.from('lessons').select('youtube_video_id').eq('id', window._lessonId).then(function (r) {
      var url = r && r.data && r.data[0] && r.data[0].youtube_video_id;
      if (!url) return;
      var isDirect = /\.(mp4|webm)(\?|$)/i.test(url) || url.indexOf('r2.dev/') !== -1;
      if (!isDirect) return;                      // embeds can't be probed
      var probe = document.createElement('video');
      probe.preload = 'metadata'; probe.muted = true; probe.src = url;
      probe.style.cssText = 'position:absolute;width:0;height:0;opacity:0;pointer-events:none';
      probe.addEventListener('loadedmetadata', function () {
        var d = probe.duration;
        if (isFinite(d) && d > 0) {
          var s = Math.round(d), m = Math.floor(s / 60), ss = s % 60;
          badge.textContent = m + ':' + (ss < 10 ? '0' : '') + ss;
        }
        probe.remove();
      });
      document.body.appendChild(probe);
    });
  }

  // Practice questions move OFF the page bottom and INTO the panel as the
  // third primary (Tom, 11 Jun: "no reason they should be at the bottom —
  // we only put them there because we ran out of space on the right").
  // The live .practice-section node is MOVED into a modal (listeners survive),
  // so AI marking / send-to-teacher keep working untouched.
  function buildPracticeTile() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    var section = document.querySelector('.practice-section');
    if (!sidebar || !section || sidebar.dataset.practiceTile) return;
    if (!window.practiceQuestions || !window.practiceQuestions.length) return;
    if (!sidebar.querySelector('.sidebar-tool-tile')) return; // keep build order stable
    sidebar.dataset.practiceTile = '1';

    var sec = document.createElement('div');
    sec.className = 'sidebar-section tile-practice';
    var b = document.createElement('button');
    b.className = 'sv-practice-btn'; b.type = 'button';
    b.innerHTML = ICONS.practice + '<span>Practice Questions</span>';
    sec.appendChild(b);
    var panel = sidebar.querySelector('.sv-panel');
    (panel || sidebar).appendChild(sec);

    var modal = document.createElement('div');
    modal.className = 'pq-modal';
    modal.hidden = true;
    modal.innerHTML = '<div class="pq-backdrop"></div>' +
      '<div class="pq-panel" role="dialog" aria-modal="true" aria-label="Practice questions">' +
        '<button type="button" class="pq-close" aria-label="Close">&times;</button>' +
      '</div>';
    modal.querySelector('.pq-panel').appendChild(section); // move, don't clone
    document.body.appendChild(modal);

    function close() { modal.hidden = true; }
    b.addEventListener('click', function () { modal.hidden = false; });
    modal.querySelector('.pq-close').addEventListener('click', close);
    modal.querySelector('.pq-backdrop').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });
  }

  // Wrap the sidebar tiles in .sv-panel — the column's single object.
  // (Companion card / contents rail / per-section recall removed 11 Jun:
  // Tom — corner felt cobbled together; synthesis lives at article end now.)
  function buildPanelWrap() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    if (!sidebar || sidebar.dataset.panelWrap) return;
    if (!sidebar.querySelector('.sidebar-tool-tile')) return; // wait until tiles are built
    sidebar.dataset.panelWrap = '1';

    var panel = document.createElement('div');
    panel.className = 'sv-panel';
    var video = null;
    while (sidebar.firstChild) {
      // the video keeps its native player card and lives BELOW the panel in
      // the freed corner (Tom, 11 Jun) — looks like a player, opens the modal
      if (sidebar.firstChild.id === 'sidebar-video-section') {
        video = sidebar.firstChild;
        sidebar.removeChild(video);
        continue;
      }
      panel.appendChild(sidebar.firstChild);
    }
    sidebar.appendChild(panel);
    if (video) sidebar.appendChild(video);
  }

  // DEMO: one generated diagram mid-article — relief for the text wall AND a
  // genuine REPLACE (Tom): a gpt-image-2 diagram of Pasteur's swan-neck flask
  // experiment carries the experiment the prose only had room to name, so the
  // sentence shortens to point at it. The real version is a content job.
  var DEMO_FIGURES = {
    '/lesson/history-aqa/britain-health-people/7': {
      src: '/design-lab/assets/pasteur-swan-neck.png',
      afterPara: 'swan-necked flask',   // drop the figure right after this paragraph
      caption: 'Pasteur’s swan-neck flask experiment. Boiled broth in an intact swan-neck flask stays clear — airborne microbes are trapped in the bend, never reaching it. Snap the neck and the same broth clouds within days. This is how he proved germs come from the air, not from the broth itself.',
      replace: {
        find: 'By using a microscope and a series of swan-necked flask experiments, Pasteur showed that microbes carried in the air caused fermentation and decay. ',
        with: 'Using a microscope, he traced fermentation and decay to microbes carried in the air — proving it with the swan-neck flask experiment shown below. '
      }
    }
  };

  function buildDemoFigure() {
    var f = DEMO_FIGURES[location.pathname.replace(/\/$/, '')];
    if (!f || document.querySelector('.sv-article-figure')) return;
    var paras = [].slice.call(document.querySelectorAll('#lesson-page .study-notes p'));
    if (!paras.length) return;
    var host = null;
    for (var i = 0; i < paras.length; i++) {
      if (paras[i].textContent.indexOf(f.afterPara) !== -1) { host = paras[i]; break; }
    }
    if (!host) return;
    if (f.replace && host.innerHTML.indexOf(f.replace.find) !== -1) {
      host.innerHTML = host.innerHTML.replace(f.replace.find, f.replace.with);
    }
    var fig = document.createElement('figure');
    fig.className = 'sv-article-figure sv-visible';
    fig.innerHTML = '<img loading="lazy" alt="">' + '<figcaption></figcaption>';
    fig.querySelector('img').src = f.src;
    fig.querySelector('img').alt = f.caption;
    fig.querySelector('figcaption').textContent = f.caption;
    host.parentNode.insertBefore(fig, host.nextSibling);   // right after the paragraph
  }

  // EXIT TICKET (Tom, 11 Jun) — ONE synthesis question per lesson, fired on
  // Next-lesson click. QUESTION TEMPLATE (Tom): open with "In Lesson N, you
  // learned that ..." — restate the prior knowledge explicitly, THEN ask the
  // question that synthesises it with THIS lesson. `from` names the source
  // lesson in the modal header. Hand-written for two specimen lessons; the
  // real version is a pipeline job (generated with prior-lesson context).
  var EXIT_TICKETS = {
    '/lesson/business-aqa/marketing/2': {
      from: 'Draws on Lesson 1',
      q: 'In Lesson 1, you learned that a market map can reveal a gap in the market — a space where customer demand isn’t being served by any rival. This lesson showed how market research measures demand. Suppose research finds strong demand among 16–25s, but your market map shows that space is crowded with competitors. Using both lessons, what decision should the business take, and why?',
      a: 'Use the two together: rather than fight head-on, reposition toward a gap — an underserved segment where demand exists but competition is thin. Market research proves the demand is real; the market map shows where the space is empty.'
    },
    '/lesson/history-aqa/britain-health-people/7': {
      from: 'Draws on Lesson 6',
      q: 'In Lesson 6, you learned that Jenner proved vaccination worked — a country doctor acting on chance observation of milkmaids, with no idea WHY it worked. In this lesson, Pasteur — a chemist paid by brewers — finally supplied the explanation. Use both men to argue that “science and technology” alone does not explain medical progress.',
      a: 'Each breakthrough needed other factors too: Jenner — chance observation plus government compulsion (the 1853 Vaccination Act); Pasteur — industrial funding, the microscope, and rivalry with Koch. Progress comes from factors combining — the core argument the 16-marker rewards.'
    }
  };

  // The ticket fires on the way OUT: clicking either "Next lesson" control
  // (header pill or article-foot nav) intercepts ONCE per lesson per session
  // and asks the synthesis question. Continue is always one click — answering
  // is invited, never extorted. Second click passes straight through.
  function setupExitIntercept() {
    if (document.body.dataset.exitIntercept) return;
    var t = EXIT_TICKETS[location.pathname.replace(/\/$/, '')];
    if (!t) return;
    document.body.dataset.exitIntercept = '1';
    var KEY = 'sv-exit-asked:' + location.pathname;

    document.addEventListener('click', function (e) {
      var link = e.target.closest('#nav-next-lesson, .lesson-nav-link--next');
      if (!link || !link.href) return;
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // new-tab etc.
      if (sessionStorage.getItem(KEY)) return;
      e.preventDefault();
      e.stopPropagation();                       // beat the page-transition handler
      sessionStorage.setItem(KEY, '1');
      openExitModal(t, link.href);
    }, true);
  }

  function openExitModal(t, nextHref) {
    var wrap = document.createElement('div');
    wrap.className = 'sv-exit-modal';
    wrap.innerHTML =
      '<div class="sv-exit-backdrop"></div>' +
      '<div class="sv-exit-card" role="dialog" aria-modal="true" aria-label="Before you go">' +
        '<button type="button" class="sv-exit-close" aria-label="Stay on this lesson">&times;</button>' +
        '<div class="sv-exit-kicker"><span>Before you go</span><span class="sv-exit-from"></span></div>' +
        '<p class="sv-exit-q"></p>' +
        '<p class="sv-exit-a" hidden></p>' +
        '<div class="sv-exit-actions">' +
          '<button type="button" class="sv-exit-btn" data-act="reveal">Reveal a model answer</button>' +
          '<a class="sv-exit-continue" href="">Continue to next lesson &rarr;</a>' +
        '</div>' +
      '</div>';
    wrap.querySelector('.sv-exit-q').textContent = t.q;
    wrap.querySelector('.sv-exit-a').textContent = t.a;
    wrap.querySelector('.sv-exit-from').textContent = t.from || '';
    wrap.querySelector('.sv-exit-continue').href = nextHref;
    var a = wrap.querySelector('.sv-exit-a'), rv = wrap.querySelector('[data-act="reveal"]');
    rv.addEventListener('click', function () {
      a.hidden = !a.hidden;
      rv.textContent = a.hidden ? 'Reveal a model answer' : 'Hide the model answer';
    });
    function close() { wrap.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    wrap.querySelector('.sv-exit-close').addEventListener('click', close);
    wrap.querySelector('.sv-exit-backdrop').addEventListener('click', close);
    document.addEventListener('keydown', onKey);
    document.body.appendChild(wrap);
    wrap.querySelector('.sv-exit-continue').focus();
  }

  // Duotone icon set (soft filled shape + bold glyph) — replaces the generic
  // thin-stroke icons, which read cheap against the editorial type
  var ICONS = {
    quiz: '<svg viewBox="0 0 24 24" width="26" height="26"><circle cx="12" cy="12" r="10" fill="currentColor" opacity=".15"/><path d="M9.4 9.2a2.7 2.7 0 0 1 5.25.9c0 1.8-2.7 2.45-2.7 3.55" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="16.9" r="1.25" fill="currentColor"/></svg>',
    cards: '<svg viewBox="0 0 24 24" width="26" height="26"><rect x="3" y="7.5" width="13.5" height="11" rx="2.2" fill="currentColor" opacity=".15"/><rect x="7.5" y="4" width="13.5" height="11" rx="2.2" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    practice: '<svg viewBox="0 0 24 24" width="24" height="24"><rect x="4" y="2.5" width="13" height="19" rx="2.2" fill="currentColor" opacity=".15"/><path d="M8 8h7M8 12h7M8 16h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M20.6 11.6l-5.4 5.4-2.2.7.7-2.2 5.4-5.4a1.06 1.06 0 0 1 1.5 1.5z" fill="currentColor"/></svg>',
    video: '<svg viewBox="0 0 24 24" width="19" height="19"><rect x="2.5" y="5" width="19" height="14" rx="3" fill="currentColor" opacity=".15"/><path d="M10.2 9.3v5.4c0 .5.55.8.98.52l4.3-2.7a.62.62 0 0 0 0-1.05l-4.3-2.7a.62.62 0 0 0-.98.53z" fill="currentColor"/></svg>',
    media: '<svg viewBox="0 0 24 24" width="19" height="19"><rect x="3" y="3" width="8.2" height="8.2" rx="2" fill="currentColor"/><rect x="12.8" y="3" width="8.2" height="8.2" rx="2" fill="currentColor" opacity=".35"/><rect x="3" y="12.8" width="8.2" height="8.2" rx="2" fill="currentColor" opacity=".35"/><rect x="12.8" y="12.8" width="8.2" height="8.2" rx="2" fill="currentColor"/></svg>',
    highlight: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M14.2 4.6l5.2 5.2L11 18.2l-5.8 1.4a.5.5 0 0 1-.6-.6L6 13.2l8.2-8.6z" fill="currentColor" opacity=".15"/><path d="M14.4 4.4l2-2a2 2 0 0 1 2.8 0l2.4 2.4a2 2 0 0 1 0 2.8l-2 2-5.2-5.2z" fill="currentColor"/><path d="M3.5 21.5h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    tutor: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M12 3a9 9 0 0 1 9 9 9 9 0 0 1-9 9H4.5a1 1 0 0 1-.7-1.7l1.8-1.8A8.96 8.96 0 0 1 3 12a9 9 0 0 1 9-9z" fill="currentColor" opacity=".15"/><circle cx="8.2" cy="12" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/><circle cx="15.8" cy="12" r="1.3" fill="currentColor"/></svg>'
  };

  // Swap the Quick Quiz / Flashcards stroke icons for the duotone marks
  function upgradePrimaryIcons() {
    [['.knowledge-check-btn svg', ICONS.quiz], ['#sidebar-flashcard-btn svg', ICONS.cards]].forEach(function (d) {
      var el = document.querySelector(d[0]);
      if (!el || el.dataset.duotone) return;
      var t = document.createElement('span');
      t.innerHTML = d[1];
      var n = t.firstChild;
      n.dataset.duotone = '1';
      el.replaceWith(n);
    });
  }

  // Relocate the floating Highlight + Ask-the-tutor buttons into the sidebar as tiles
  function buildToolTiles() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    if (!sidebar || sidebar.dataset.toolTiles) return;
    var tutor = document.querySelector('.tutor-dock');
    if (!tutor) return; // FAB not built yet
    sidebar.dataset.toolTiles = '1';

    function tile(label, svg, cls) {
      var sec = document.createElement('div');
      sec.className = 'sidebar-section sidebar-tool-tile ' + (cls || '');
      var b = document.createElement('button');
      b.className = 'sv-tool-btn'; b.type = 'button';
      b.innerHTML = svg + '<span class="sv-tool-label">' + label + '</span>';
      sec.appendChild(b);
      sidebar.appendChild(sec);
      return { btn: b, label: b.querySelector('.sv-tool-label') };
    }
    var tutorSvg = ICONS.tutor;

    // Highlight tile removed (Tom, 13 Jun): highlighting is a low-utility study
    // technique; its focus/reading-aid value is now served by Focus mode.
    if (tutor) {
      var tt = tile('Ask the tutor', tutorSvg, 'tile-tutor');
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
    // drop the raw category emoji — clashes with the redesign's icon language;
    // the heading becomes a clean accent caps label instead
    [].forEach.call(mbody.querySelectorAll('.sidebar-collapsible-toggle span'), function (s) {
      s.textContent = s.textContent.replace(/^[^\w(]+/, '').trim();
    });
    // TRUE masonry: drop each category card into the currently-shortest column
    // (CSS columns only balance total height — they leave the gap Tom saw)
    var cards = [].slice.call(mbody.querySelectorAll('.sidebar-collapsible'));
    var feed = mbody.querySelector('.sidebar-podcast-feed');
    var panel = modal.querySelector('.rm-panel');
    var PAD = 54, COLW = 270, GAP = 18;
    // lay the cards into n balanced columns, size the panel to wrap them
    function renderCols(n) {
      panel.style.width = Math.min(n * COLW + (n - 1) * GAP + PAD, Math.round(window.innerWidth * 0.94)) + 'px';
      var wrap = document.createElement('div'); wrap.className = 'rm-cols';
      var cols = [];
      for (var k = 0; k < n; k++) { var c = document.createElement('div'); c.className = 'rm-col'; wrap.appendChild(c); cols.push(c); }
      mbody.innerHTML = '';
      mbody.appendChild(wrap);
      // pass 1: measure each card at the real column width
      var measured = cards.map(function (card) { cols[0].appendChild(card); return { card: card, h: card.offsetHeight }; });
      measured.forEach(function (o) { cols[0].removeChild(o.card); });
      // pass 2: tallest-first into the currently-shortest column (LPT balancing)
      measured.sort(function (a, b) { return b.h - a.h; });
      var hts = []; for (var k = 0; k < n; k++) hts.push(0);
      measured.forEach(function (o) {
        var m = 0; for (var k = 1; k < n; k++) if (hts[k] < hts[m]) m = k;
        cols[m].appendChild(o.card); hts[m] += o.h + GAP;
      });
      if (feed) mbody.appendChild(feed);
    }
    function masonry() {
      if (modal.hidden) return;
      var maxByVp = Math.max(1, Math.floor((window.innerWidth * 0.94 - PAD) / (COLW + GAP)));
      var cap = Math.min(cards.length, maxByVp, 4);   // up to 4 cols when it helps
      var n = Math.max(1, Math.min(3, cap));
      renderCols(n);
      // too tall to fit without a scroll? spread it WIDER (add a column) rather
      // than shrink the text — keeps it readable, uses the horizontal space
      while (panel.scrollHeight > panel.clientHeight + 2 && n < cap) { n++; renderCols(n); }
    }
    var launcher = document.createElement('button');
    launcher.className = 'rm-launcher';
    launcher.innerHTML = ICONS.media
      + '<span class="rm-launcher-label">Related media</span>'
      + '<span class="rm-launcher-count">' + count + '</span>';
    media.appendChild(launcher);
    function open() { modal.hidden = false; document.body.style.overflow = 'hidden'; masonry(); }
    function close() { modal.hidden = true; document.body.style.overflow = ''; }
    launcher.addEventListener('click', open);
    modal.querySelector('.rm-close').addEventListener('click', close);
    modal.querySelector('.rm-backdrop').addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    var rt; window.addEventListener('resize', function () {
      if (modal.hidden) return; clearTimeout(rt); rt = setTimeout(masonry, 150);
    });
  }

  // BRIEF v2: one muted accent per subject (sandbox map keyed by base slug;
  // ships later via subjects.color). Used sparingly: kicker, links, progress fills.
  // the desk's own subject colours (dash-desk4 notebook tabs) — in desk-world
  // mode the lesson inherits the SAME accent as its tab on the desk
  var DESK_ACCENTS = {
    'maths': '#4e5f66', 'mathematics': '#4e5f66',
    'english-language': '#5b7285', 'english-literature': '#7d5a78',
    'science': '#4e6e5d', 'combined-science': '#4e6e5d',
    'history': '#8a5a44', 'geography': '#6d7a4e', 'spanish': '#a2643f',
    'computer-science': '#54606e', 'religious-studies': '#6f5b91'
  };
  var ACCENTS = {
    'history': '#3f5e78',            // deep slate-blue (was a muddy umber)
    'geography': '#5f7155',          // moss
    'science': '#44696c',            // slate teal
    'combined-science': '#44696c',
    'separate-sciences': '#44696c',
    'maths': '#535f8a',              // muted indigo
    'mathematics': '#535f8a',
    'statistics': '#535f8a',
    'english-literature': '#71506b', // plum
    'english-language': '#4a708c',   // dusty azure
    'business': '#8a6c42',           // ochre
    'economics': '#6e6440',          // olive
    'psychology': '#84576b',         // rosewood
    'sociology': '#5e6a7d',          // slate blue
    'religious-education': '#6f5b91',// muted violet
    'religious-studies': '#6f5b91',
    'computer-science': '#3f6478',   // petrol
    'physical-education': '#3e6e5f', // pine
    'sport-science': '#3e6e5f',
    'sport-coaching-principles': '#3e6e5f',
    'drama': '#8a4f5c',              // muted crimson
    'music': '#5b5286',              // heather
    'music-technology': '#5b5286',
    'spanish': '#9a5b38',            // terracotta
    'french': '#4c5f93',             // cornflower ink
    'german': '#6e5640',             // walnut
    'food-technology': '#8c5e3a',
    'food-preparation-nutrition': '#8c5e3a',
    'design-technology': '#5f666f',  // graphite
    'engineering': '#5f666f',
    'electronics': '#5f666f',
    'creative-imedia': '#54486e',    // ink violet
    'media-studies': '#54486e',
    'film-studies': '#54486e',
    'astronomy': '#3d5a78',
    'citizenship': '#6b5a45',
    'geology': '#6e6248',
    'retail-business': '#8a6c42',
    'health-social-care': '#84576b',
    'it': '#3f6478'
  };
  // In the desk world, HOME is Sam's desk: the brand mark and the Home nav
  // link lead back to the dashboard, closing the desk → lesson → desk loop.
  function wireDeskHome() {
    if (!document.body.classList.contains('desk-world')) return;
    var brand = document.querySelector('a.header-brand');
    if (brand) brand.setAttribute('href', '/desk');
    [].forEach.call(document.querySelectorAll('.header-nav a, a.back-link'), function (a) {
      if (a.getAttribute('href') === '/') a.setAttribute('href', '/desk');
    });
  }

  function applySubjectAccent() {
    var m = location.pathname.match(/^\/(?:lesson|practice|browse|guide)\/([a-z0-9-]+)/);
    if (!m) return;
    var slug = m[1].replace(/-(aqa|edexcel|ocr|ocr-b|eduqas|wjec|ncfe)$/, '');
    var deskMode = document.body.classList.contains('desk-world');
    var c = (deskMode && (DESK_ACCENTS[slug] || DESK_ACCENTS[slug.replace(/-2$/, '')])) ||
            ACCENTS[slug] || ACCENTS[slug.replace(/-2$/, '')];
    if (c) document.body.style.setProperty('--subject-accent', c);
  }

  function init() {
    if (location.search.indexOf('notour') !== -1) {
      try { localStorage.setItem('sv-reader-tour-v1', '1'); } catch (e) {}
    }
    // the OLD loader tutorial is replaced by the reader tour — its tooltip is
    // stripped under this skin, so if it ever starts it strands mid-step with
    // a spotlight marker stuck on real content. Retire it before it can run.
    try {
      localStorage.setItem('sv-lesson-tutorial-done', '1');
      localStorage.setItem('sv-highlight-tutorial-done', '1');
    } catch (e) {}
    // switcher bar hidden (Tom, 10 Jun) — Reader is the working skin; the bar
    // covered the top-right header buttons. Re-enable by appending `bar` again.
    var reqSkin = new URLSearchParams(location.search).get('skin');
    set(reqSkin !== null ? reqSkin : 'desk');   // default: desk-world (?skin=reader to compare)
  if (new URLSearchParams(location.search).get('dark') === '1') document.body.classList.add('dark-mode');   // QA staging
    applySubjectAccent();
    watchOldOnboarding();     // kill the first-visit onboarding flash from the start
    setTimeout(tidy, 1200);
    setTimeout(tidy, 2600);
    setTimeout(tidy, 4200);   // safety: catch a slow async video-card render

    // (scroll-jump-past-hero experiment removed — felt jerky; plain scrolling wins)
  }
  if (document.body) init(); else document.addEventListener('DOMContentLoaded', init);
})();

// throwaway computed-style probe (QA): ?csprobe=1 writes colours into <title>
if (new URLSearchParams(location.search).get('csprobe') === '1') {
  setTimeout(function () {
    try {
      var lg = getComputedStyle(document.querySelector('.header-logo'));
      var bd = getComputedStyle(document.body);
      var hd = getComputedStyle(document.querySelector('.page-header'));
      document.title = 'CS|logo=' + lg.color + '|tp=' + bd.getPropertyValue('--text-primary')
        + '|hdrbg=' + hd.backgroundColor + '|cls=' + document.body.className;
    } catch (e) { document.title = 'CS|ERR ' + e.message; }
  }, 600);
}
