/**
 * Anonymous-visitor welcome modal.
 *
 * Fires once per browser when:
 *   - The visitor has no school session and no free-user prefs
 *   - They're not signed in as admin/teacher
 *   - localStorage `sv-anon-welcome-seen` flag is unset
 *
 * Loaded on browse.html / lesson.html / practice.html. Acts as a friendly
 * nudge toward personalisation rather than a hard gate — anonymous deep
 * links (from social posts) now land on default-board content instead of
 * being bounced to the homepage wizard.
 */
(function () {
  var SEEN_KEY = 'sv-anon-welcome-seen';

  // Bail if a logged-in / personalised user.
  if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive()) return;
  if (typeof FreeUser !== 'undefined' && FreeUser.isActive()) return;

  // Bail if admin / teacher session present.
  try {
    var auth = JSON.parse(sessionStorage.getItem('studyvault-auth'))
            || JSON.parse(localStorage.getItem('studyvault-auth'));
    if (auth && (auth.role === 'admin' || auth.role === 'teacher')) return;
  } catch (e) {}

  // Bail if already seen.
  try {
    if (localStorage.getItem(SEEN_KEY) === '1') return;
  } catch (e) {
    return; // no localStorage → assume third-party context, don't nag.
  }

  function setSeen() {
    try { localStorage.setItem(SEEN_KEY, '1'); } catch (e) {}
  }

  // Detect which exam board the visitor is currently looking at, based on the
  // URL slug. Returns a display name (e.g. "AQA", "Edexcel") or null when the
  // page isn't a recognised content URL.
  //
  // Logic:
  //   1. Suffixed slugs (e.g. "english-literature-edexcel") → board from suffix
  //   2. Unsuffixed multi-board slugs → look up the default board (per the
  //      slug map at index.html:2253)
  //   3. Unknown subjects → return null; modal falls back to generic copy
  function detectBoard() {
    var match = window.location.pathname.match(/^\/(?:browse|lesson|practice)\/([^/]+)/);
    if (!match) return null;
    var slug = match[1];

    var suffixes = [
      ['-edexcel-a', 'Edexcel A'],
      ['-edexcel-b', 'Edexcel B'],
      ['-edexcel',   'Edexcel'],
      ['-aqa',       'AQA'],
      ['-ocr',       'OCR'],
      ['-eduqas',    'Eduqas'],
      ['-wjec',      'WJEC'],
      ['-ncfe',      'NCFE'],
    ];
    for (var i = 0; i < suffixes.length; i++) {
      if (slug.indexOf(suffixes[i][0], slug.length - suffixes[i][0].length) !== -1) {
        return suffixes[i][1];
      }
    }

    var defaults = {
      'english-language':   'AQA',
      'english-literature': 'AQA',
      'maths':              'Edexcel',
      'science':            'AQA',
      'geography':          'AQA',
      'history':            'AQA',
      'religious-education':'AQA',
      'separate-sciences':  'AQA',
      'business':           'Edexcel',
      'health-social-care': 'Pearson Edexcel',
      'hospitality-catering':'WJEC',
      'music':              'Eduqas',
      'music-technology':   'NCFE',
    };
    return defaults[slug] || null;
  }

  function buildModal() {
    var board = detectBoard();
    var leadParagraph = board
      ? 'You\'re currently looking at the <strong>' + board + '</strong> version. '
        + 'If your school uses a different exam board, tell us and we\'ll switch the content over.'
      : 'You can keep browsing — but if you tell us your exam board, we\'ll show you '
        + 'the right content for the subjects you actually take.';

    var overlay = document.createElement('div');
    overlay.className = 'anon-welcome-overlay';
    overlay.innerHTML = (
      '<div class="anon-welcome-modal" role="dialog" aria-modal="true" aria-labelledby="anon-welcome-title">'
    +   '<div class="anon-welcome-icon" aria-hidden="true">'
    +     '<svg viewBox="0 0 2048 2048" width="34" height="34" fill="currentColor">'
    +       '<path d="M 1006.55 384.5 C 1126.34 383.508 1224.86 424.385 1296.99 497.419 C 1360.21 560.738 1398.86 644.469 1406.04 733.658 C 1408.66 765.139 1407.27 812.813 1407.19 845.206 C 1429.72 844.275 1447.74 845.081 1465.32 844.677 C 1495.06 843.994 1535.25 840.392 1535.47 882.388 L 1535.36 1317.69 L 1535.32 1438.19 C 1535.26 1507.75 1538.75 1557.74 1484.85 1611.82 C 1460.86 1635.66 1430.61 1652.23 1397.59 1659.62 C 1375.13 1664.65 1350.12 1663.97 1327.09 1663.93 L 791.843 1663.77 C 753.977 1663.77 680.267 1666.52 646.687 1658.7 C 616.228 1651.35 588.323 1635.91 565.929 1614 C 532.163 1581.54 512.105 1536.9 512.157 1490.19 L 512.46 1090.95 L 512.437 949.482 C 512.426 925.408 512.016 901.145 513.113 877.152 C 513.68 864.772 526.116 849.163 538.208 846.652 C 551.022 843.991 567.128 844.956 580.366 844.959 C 600.487 844.856 620.61 844.943 640.73 845.219 C 639.551 827.347 640.432 805.755 640.372 787.686 C 640.3 766.215 640.741 742.607 643.073 721.312 C 651.702 644.63 683.654 572.444 734.615 514.5 C 806.373 432.129 899.065 391.821 1006.55 384.5 z M 716.467 845.223 C 818.381 844.143 921.774 845.464 1023.95 845.099 L 1331.64 844.834 C 1330.34 831.289 1331.21 811.921 1331.49 799.241 C 1331.8 783.652 1331.59 768.058 1330.86 752.483 C 1326.9 666.541 1286.96 586.231 1220.82 531.214 C 1176.33 494.282 1122.33 470.636 1065.02 462.987 C 938.331 462.331 863.078 491.197 801.283 555.598 C 753.658 605.045 724.17 669.155 717.618 737.494 C 714.147 772.586 716.753 809.897 716.467 845.223 z"/>'
    +     '</svg>'
    +   '</div>'
    +   '<h2 class="anon-welcome-title" id="anon-welcome-title">First time at Study Vault?</h2>'
    +   '<div class="anon-welcome-body">'
    +     '<p>' + leadParagraph + '</p>'
    +     '<p>Takes 30 seconds. Only do it once.</p>'
    +   '</div>'
    +   '<div class="anon-welcome-buttons">'
    +     '<button type="button" class="anon-welcome-btn anon-welcome-btn--primary" data-action="personalise">Personalise</button>'
    +     '<button type="button" class="anon-welcome-btn anon-welcome-btn--ghost" data-action="dismiss">Keep browsing</button>'
    +   '</div>'
    + '</div>'
    );
    return overlay;
  }

  function show() {
    if (!document.body) return;
    var overlay = buildModal();
    document.body.appendChild(overlay);
    // Force layout so the transition kicks in.
    void overlay.offsetWidth;
    overlay.classList.add('active');

    function close() {
      setSeen();
      overlay.classList.remove('active');
      setTimeout(function () { if (overlay.parentNode) overlay.remove(); }, 260);
    }

    overlay.addEventListener('click', function (e) {
      var action = e.target && e.target.dataset && e.target.dataset.action;
      if (action === 'personalise') {
        setSeen();
        // ?personalise=1 tells the homepage to skip the school welcome modal
        // and open the free-tier subject picker directly.
        window.location.href = '/?personalise=1';
        return;
      }
      if (action === 'dismiss' || e.target === overlay) {
        close();
      }
    });

    // Esc to dismiss.
    document.addEventListener('keydown', function onKey(e) {
      if (e.key === 'Escape') {
        document.removeEventListener('keydown', onKey);
        close();
      }
    });
  }

  // Wait briefly so the page renders before the modal appears.
  function start() { setTimeout(show, 900); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
