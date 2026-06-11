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
      vs.innerHTML = '<button class="sv-tool-btn" type="button">' + ICONS.video + '<span>Video</span></button>';
    }
    setupMediaLauncher();
    buildToolTiles();
    upgradePrimaryIcons();
    buildPanelWrap();
    setupExitIntercept();
    revealMasthead();
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
    while (sidebar.firstChild) panel.appendChild(sidebar.firstChild);
    sidebar.appendChild(panel);
  }

  // EXIT TICKET (Tom, 11 Jun) — synthesis stays, but ONE question per lesson
  // instead of per-section: a single "Before you go" task at the end of the
  // article that forces the student to combine this lesson with earlier ones.
  // Hand-written for two specimen lessons; the real version is a pipeline job
  // (one synthesis question per lesson, generated with prior-lesson context).
  var EXIT_TICKETS = {
    '/lesson/business-aqa/marketing/2': {
      q: 'Research shows strong demand among 16–25s — but the market map you drew in Lesson 1 shows that space is crowded with rivals. Using both lessons, what decision should the business take, and why?',
      a: 'Use the two together: rather than fight head-on, reposition toward a gap — an underserved segment where demand exists but competition is thin. Market research confirms the demand is real; the market map shows where the space is empty.'
    },
    '/lesson/history-aqa/britain-health-people/7': {
      q: 'Pasteur was a chemist helping brewers; Jenner was a country doctor watching milkmaids. Use both men to argue that “science and technology” alone does not explain medical progress.',
      a: 'Each breakthrough needed other factors too: Jenner — chance observation plus government compulsion (1853); Pasteur — industrial funding, the microscope, and rivalry with Koch. Progress comes from factors combining — the core argument the 16-marker rewards.'
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
        '<div class="sv-exit-kicker">Before you go</div>' +
        '<p class="sv-exit-q"></p>' +
        '<p class="sv-exit-a" hidden></p>' +
        '<div class="sv-exit-actions">' +
          '<button type="button" class="sv-exit-btn" data-act="reveal">Reveal a model answer</button>' +
          '<a class="sv-exit-continue" href="">Continue to next lesson &rarr;</a>' +
        '</div>' +
      '</div>';
    wrap.querySelector('.sv-exit-q').textContent = t.q;
    wrap.querySelector('.sv-exit-a').textContent = t.a;
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
    var hl = document.querySelector('.sv-hl-fab-stack');
    var tutor = document.querySelector('.tutor-dock');
    if (!hl && !tutor) return; // FABs not built yet
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
    var hlSvg = ICONS.highlight;
    var tutorSvg = ICONS.tutor;

    if (hl) {
      var ht = tile('Highlight', hlSvg, 'tile-highlight');
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
    var launcher = document.createElement('button');
    launcher.className = 'rm-launcher';
    launcher.innerHTML = ICONS.media
      + '<span class="rm-launcher-label">Related media</span>'
      + '<span class="rm-launcher-count">' + count + '</span>';
    media.appendChild(launcher);
    function open() { modal.hidden = false; document.body.style.overflow = 'hidden'; }
    function close() { modal.hidden = true; document.body.style.overflow = ''; }
    launcher.addEventListener('click', open);
    modal.querySelector('.rm-close').addEventListener('click', close);
    modal.querySelector('.rm-backdrop').addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  // BRIEF v2: one muted accent per subject (sandbox map keyed by base slug;
  // ships later via subjects.color). Used sparingly: kicker, links, progress fills.
  var ACCENTS = {
    'history': '#7d4f41',            // umber
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
  function applySubjectAccent() {
    var m = location.pathname.match(/^\/(?:lesson|practice|browse|guide)\/([a-z0-9-]+)/);
    if (!m) return;
    var slug = m[1].replace(/-(aqa|edexcel|ocr|ocr-b|eduqas|wjec|ncfe)$/, '');
    var c = ACCENTS[slug] || ACCENTS[slug.replace(/-2$/, '')];
    if (c) document.body.style.setProperty('--subject-accent', c);
  }

  function init() {
    // switcher bar hidden (Tom, 10 Jun) — Reader is the working skin; the bar
    // covered the top-right header buttons. Re-enable by appending `bar` again.
    set('reader');            // default to the bold structural redesign
    applySubjectAccent();
    setTimeout(tidy, 1200);
    setTimeout(tidy, 2600);

    // (scroll-jump-past-hero experiment removed — felt jerky; plain scrolling wins)
  }
  if (document.body) init(); else document.addEventListener('DOMContentLoaded', init);
})();
