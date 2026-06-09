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
    buildContentsRail();
    revealMasthead();
  }

  // "In this lesson" contents rail — fills the corner below the tool panel.
  // Wraps the tiles in .sv-panel, then lists the article's h2s, scroll-synced.
  function buildContentsRail() {
    var sidebar = document.querySelector('#lesson-page .lesson-sidebar');
    if (!sidebar || sidebar.dataset.contentsRail) return;
    var heads = [].slice.call(document.querySelectorAll('#lesson-page .study-notes h2'));
    if (heads.length < 2) return;                       // nothing worth mapping
    if (!sidebar.querySelector('.sidebar-tool-tile')) return; // wait until tiles are built
    sidebar.dataset.contentsRail = '1';

    var panel = document.createElement('div');
    panel.className = 'sv-panel';
    while (sidebar.firstChild) panel.appendChild(sidebar.firstChild);
    sidebar.appendChild(panel);

    var rail = document.createElement('nav');
    rail.className = 'sv-contents';
    rail.setAttribute('aria-label', 'Lesson contents');
    rail.innerHTML = '<div class="sv-contents-title">In this lesson</div>';
    var links = heads.map(function (h, i) {
      if (!h.id) h.id = 'lesson-sec-' + i;
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.addEventListener('click', function (e) {
        e.preventDefault();
        h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      rail.appendChild(a);
      return a;
    });
    sidebar.appendChild(rail);

    buildPriorRecall(sidebar);

    var ticking = false, lastIdx = -2;
    function sync() {
      ticking = false;
      var idx = -1, threshold = window.innerHeight * 0.38;
      heads.forEach(function (h, i) { if (h.getBoundingClientRect().top < threshold) idx = i; });
      links.forEach(function (l, i) { l.classList.toggle('active', i === idx); });
      if (window.__svRecall && idx !== lastIdx && idx >= 0) window.__svRecall.deal(idx);
      lastIdx = idx;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(sync); }
    }, { passive: true });
    sync();
  }

  // DEMO: per-section SYNTHESIS questions (Tom's idea, 10 Jun) — each section
  // gets one question that combines THIS section's idea with something from a
  // previous lesson, forcing integration. Hand-written for one specimen lesson
  // to trial the experience; the real version is a pipeline job
  // (synthesis_questions jsonb per lesson, generated with prior-lesson context).
  var DEMO_SYNTH = {
    '/lesson/business-aqa/marketing/2': [
      { q: 'In Lesson 1 you used a market map to spot a gap for budget gym wear. Which of the three things market research collects — demand, competition, target market — would confirm the gap is worth filling?',
        a: 'Demand is the decisive check: a gap on the map only matters if enough people would actually buy budget gym wear. Competition research then confirms the space really is empty.' },
      { q: 'You segmented a market by age and income in Lesson 1. How would you design a survey so its results can be broken down by segment?',
        a: 'Include questions that record each respondent’s segment (age group, income band). Answers can then be split per segment and compared against the target market.' },
      { q: 'Which would better tell a business whether the over-50s segment you met in Lesson 1 is growing — its own customer survey, or government population data? Why?',
        a: 'Government data (secondary research): it shows whole-population trends over years. A survey only captures the business’s current customers at one moment.' },
      { q: 'A cinema targets two segments: families and film buffs. Which research type would reveal WHY film buffs visit less often — and which would show HOW MUCH each segment spends?',
        a: 'Qualitative research (interviews, focus groups) uncovers the why; quantitative research puts numbers on each segment’s spending.' },
      { q: 'Why might a business measure the size of ONE segment from Lesson 1 rather than the size of the whole market?',
        a: 'If it targets a segment, realistic demand is that segment’s size, not the whole market’s. Market share within the segment shows how well it is competing where it actually sells.' },
      { q: 'Research shows strong demand among 16–25s — but the market map from Lesson 1 shows that space is crowded with rivals. What decision might the business take?',
        a: 'Use the two together: rather than fight head-on, reposition toward a gap — an underserved segment where demand exists but competition is thin.' }
    ],
    // AQA History — Health & the People L7 (Pasteur, Koch & Germ Theory), the
    // unit's halfway hinge: every section recontextualises an earlier lesson
    '/lesson/history-aqa/britain-health-people/7': [
      { from: 'with Lesson 1',
        q: 'Miasma theory was wrong but still produced useful action. In Lesson 1 you met another wrong theory that shaped treatment for centuries. What did the two have in common?',
        a: 'The four humours. Both were coherent, actionable explanations — bleeding and purging to rebalance humours, cleaning and ventilation to clear bad air — and both blocked the search for the real, invisible cause of disease.' },
      { from: 'with Lesson 6',
        q: 'Jenner proved vaccination worked some 65 years before Pasteur published germ theory. What could Jenner NOT explain that Pasteur now could?',
        a: 'WHY it worked. Jenner’s vaccine came from observation, with no mechanism. Germ theory supplied one — a specific microbe causes the disease — which is why vaccines for new diseases could now be developed deliberately rather than stumbled upon.' },
      { from: 'with Lesson 4',
        q: 'Koch identified specific microbes using dyes and photography. How does his method echo what Vesalius did in Lesson 4 — and why do examiners love this comparison?',
        a: 'Both replaced trust in ancient authority with direct observation and proof: Vesalius dissected to correct Galen; Koch stained and photographed microbes to prove each disease had its own germ. The Science & Technology factor recurring across periods — ideal factor-essay evidence.' },
      { from: 'with Lesson 1',
        q: 'Compare Ehrlich’s Salvarsan 606 with the treatments a medieval doctor offered in Lesson 1. What fundamental shift does a “magic bullet” represent?',
        a: 'Medieval treatment aimed at the whole body’s balance (bleeding, purging). Salvarsan attacked one specific cause — the syphilis microbe. Treatment now followed the actual cause of disease, not a theory of balance.' },
      { from: 'with Lesson 2',
        q: 'In Lesson 2 the Church both helped and hindered progress. Britain lagged behind France and Germany on germ theory in the 1860s–70s. What is similar about WHY progress was slowed in each case?',
        a: 'Institutions and attitudes, not lack of evidence: medieval reverence for Galen and Church authority discouraged challenge; the Victorian medical establishment clung to miasma and distrusted foreign laboratory science. “Attitudes in society” as a hindering factor recurs.' },
      { from: 'with Lesson 3',
        q: 'During the Black Death (Lesson 3) ordinary people turned to prayer, flagellation and herbs. By the 1880s germ theory was proven — yet what stayed surprisingly similar in everyday medicine, and why?',
        a: 'Most people still used home remedies, patent medicines and unqualified healers — knowing the cause didn’t yet produce affordable cures. Understanding changed faster than treatment: change and continuity running side by side.' },
      { from: 'whole course',
        q: 'Pasteur was a chemist helping brewers; Jenner was a country doctor watching milkmaids. Use both to argue that “science and technology” alone does not explain progress.',
        a: 'Each breakthrough needed other factors too: Jenner — chance observation plus government compulsion (1853); Pasteur — industrial funding, the microscope, and rivalry with Koch. Progress comes from factors combining — the core argument the 16-marker rewards.' }
    ]
  };

  // QUICK RECALL v2 — spaced retrieval, not open-book recognition (Tom's call:
  // asking about the section on screen is "flashcards but cheating").
  // The card drills EARLIER lessons in this unit: content that is NOT in front
  // of you. Scroll boundaries deal the next card from a shuffled prior-lesson
  // deck. Lesson 1 of a unit has nothing to look back on -> no card.
  // When a DEMO_SYNTH set exists for this page, the card runs in synthesis
  // mode instead: the active SECTION picks the question (1:1), kicker says
  // 'Bring it together'.
  function makeRecallCard(sidebar, kicker) {
    var recall = document.createElement('div');
    recall.className = 'sv-recall';
    recall.innerHTML =
      '<div class="sv-recall-kicker"><span>' + kicker + '</span><span class="sv-recall-from"></span></div>' +
      '<p class="sv-recall-q"></p>' +
      '<p class="sv-recall-a" hidden></p>' +
      '<div class="sv-recall-actions">' +
        '<button type="button" class="sv-recall-btn sv-recall-btn--primary" data-act="reveal">Reveal answer</button>' +
      '</div>';
    sidebar.appendChild(recall);
    var els = {
      q: recall.querySelector('.sv-recall-q'),
      a: recall.querySelector('.sv-recall-a'),
      from: recall.querySelector('.sv-recall-from'),
      reveal: recall.querySelector('[data-act="reveal"]')
    };
    recall.addEventListener('click', function (e) {
      if (!e.target.closest('[data-act="reveal"]')) return;
      els.a.hidden = !els.a.hidden;
      els.reveal.textContent = els.a.hidden ? 'Reveal answer' : 'Hide answer';
    });
    els.show = function (c) {
      els.q.textContent = c.q;
      els.a.textContent = c.a;
      els.from.textContent = c.from || '';
      els.a.hidden = true;
      els.reveal.textContent = 'Reveal answer';
    };
    return els;
  }

  function buildPriorRecall(sidebar) {
    if (document.querySelector('.sv-recall')) return;
    var info = window._lessonOfTotal || {};

    // SYNTHESIS MODE (demo) — section index picks the question
    var synth = DEMO_SYNTH[location.pathname.replace(/\/$/, '')];
    if (synth && synth.length) {
      var sEls = makeRecallCard(sidebar, 'Bring it together');
      var sLast = -1;
      window.__svRecall = { deal: function (idx) {
        var n = Math.max(0, Math.min(typeof idx === 'number' ? idx : 0, synth.length - 1));
        if (n === sLast) return;
        sLast = n;
        sEls.show(synth[n]);
      } };
      window.__svRecall.deal(0);
      return;
    }

    // PRIOR-LESSON RECALL MODE — shuffled deck from earlier lessons
    var unitId = window._lessonUnitId;
    if (!unitId || !info.num || info.num <= 1) return;
    var client = window.supabase.createClient(
      'https://baipckgywpnwapobwtsy.supabase.co',
      'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
    );
    client.from('lessons')
      .select('lesson_number, title, flashcard_questions')
      .eq('unit_id', unitId)
      .lt('lesson_number', info.num)
      .order('lesson_number')
      .then(function (res) {
        var deck = [];
        ((res && res.data) || []).forEach(function (l) {
          (l.flashcard_questions || []).forEach(function (c) {
            deck.push({ q: c.question || c.q || '', a: c.answer || c.a || '',
                        from: 'Lesson ' + l.lesson_number + ' · ' + (l.title || '') });
          });
        });
        if (!deck.length || document.querySelector('.sv-recall')) return;
        for (var i = deck.length - 1; i > 0; i--) {       // shuffle once per visit
          var j = Math.floor(Math.random() * (i + 1));
          var t = deck[i]; deck[i] = deck[j]; deck[j] = t;
        }
        var els = makeRecallCard(sidebar, 'Quick recall');
        var n = -1;
        window.__svRecall = { deal: function () {
          n = (n + 1) % deck.length;
          els.show(deck[n]);
        } };
        window.__svRecall.deal();
      });
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
