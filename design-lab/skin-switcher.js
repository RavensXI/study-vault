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
    setupMediaLauncher();
    buildToolTiles();
    upgradePrimaryIcons();
    buildPracticeTile();
    buildPanelWrap();
    buildRichVideoThumb();
    buildDemoFigure();
    setupExitIntercept();
    revealMasthead();
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
    setTimeout(tidy, 4200);   // safety: catch a slow async video-card render

    // (scroll-jump-past-hero experiment removed — felt jerky; plain scrolling wins)
  }
  if (document.body) init(); else document.addEventListener('DOMContentLoaded', init);
})();
