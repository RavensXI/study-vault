/* Quick check (test-out) shell — retrieval-strength branch.
   One full-screen frame with two numbered stages: the quick quiz, then one
   exam question marked by the AI. Four out of five on the quiz unlocks the
   question; half marks on the question and the lesson counts as covered.
   The shell HOSTS the existing quiz modal and practice section (moved in,
   moved back out), so there is one quiz and one practice component.

   Opens on arrival at an unread article lesson whose topic the student rated
   confident or getting there (sv-welcome.rag), and whenever the plan sends
   them with ?quiz=1. Never for practice sets or listening lessons.
   main.js calls: svTestoutShould(), svTestoutOpen(), svTestoutStage2(),
   svTestoutVerdict(ok). */
(function () {
  'use strict';
  var shell = null, moved = null, closedByUs = false;
  function pathKey() {
    var m = location.pathname.match(/\/lesson\/([^/]+)\/([^/]+)\/(\d+)/);
    return m ? { sub: m[1], unit: m[2], num: parseInt(m[3], 10) } : null;
  }
  function g(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function dismissedKey(p) { return 'sv-testout-seen:' + p.sub + '/' + p.unit + '/' + p.num; }

  /* should the check open on its own for this lesson? */
  window.svTestoutShould = function () {
    var p = pathKey(); if (!p) return false;
    if (document.querySelector('.sv-listening')) return false;
    try { if (sessionStorage.getItem(dismissedKey(p))) return false; } catch (e) {}
    var rag = (g('sv-welcome', {}).rag) || {};
    var r = rag[p.sub + '/' + p.unit];
    if (r !== 'g' && r !== 'a') return false;
    var done = g('sv-lessons-done', {})[p.sub + '/' + p.unit] || [];
    if (done.indexOf(p.num) >= 0) return false;
    var kc = g('sv-kc-log', {});
    if (kc[p.sub + '/' + p.unit + '/' + p.num]) return false;   /* already quizzed once: the plan brings it round */
    return true;
  };

  function lessonTitle() { var h = document.getElementById('lesson-title'); return h ? h.textContent.trim() : ''; }
  function unitName() { var u = document.getElementById('header-unit-label'); return (u && u.textContent.trim()) || window._unitName || 'this topic'; }
  function ratingWord() {
    var p = pathKey(); if (!p) return null;
    var r = ((g('sv-welcome', {}).rag) || {})[p.sub + '/' + p.unit];
    return r === 'g' ? 'confident' : r === 'a' ? 'getting there' : null;
  }
  function nextLessonHref() {
    var a = document.getElementById('nav-next-lesson');
    if (a && a.getAttribute('href') && a.getAttribute('href') !== '#' && a.style.display !== 'none') return a.getAttribute('href');
    var b = Array.prototype.find.call(document.querySelectorAll('a'), function (x) { return /next lesson/i.test(x.textContent) && x.getAttribute('href') && x.getAttribute('href') !== '#'; });
    return b ? b.getAttribute('href') : null;
  }

  function build() {
    var el = document.createElement('div');
    el.className = 'sv-testout'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Quick check');
    var word = ratingWord(), unit = unitName();
    var why = word
      ? 'You rated <b>' + unit + '</b> as <b>' + word + '</b>, so you can skip the full lesson if you can prove it.'
      : 'Your plan thinks you may already know this. Prove it and skip the full lesson.';
    el.innerHTML =
      '<div class="sv-to-inner">' +
        '<div class="sv-to-head">' +
          '<div class="sv-to-kicker">Quick check</div>' +
          '<h2 class="sv-to-title"></h2>' +
          '<p class="sv-to-deal">' + why + '</p>' +
        '</div>' +
        '<ol class="sv-to-stages">' +
          '<li class="cur"><span class="n">1</span><span class="t">Quiz<small>get at least 4 out of 5</small></span></li>' +
          '<li class="locked"><span class="n">2</span><span class="t">Exam question<small>at least half marks</small></span></li>' +
        '</ol>' +
        '<div class="sv-to-stage sv-to-s1"></div>' +
        '<div class="sv-to-stage sv-to-s2" hidden></div>' +
        '<div class="sv-to-verdict" hidden></div>' +
        '<div class="sv-to-foot"><button type="button" class="sv-to-skip">Complete the full lesson instead</button></div>' +
      '</div>';
    el.querySelector('.sv-to-title').textContent = lessonTitle();
    el.querySelector('.sv-to-skip').addEventListener('click', function () { close(true); });
    return el;
  }

  /* the shell owns Escape: the quiz's own Escape would close the quiz under us */
  function onKey(e) { if (e.key === 'Escape') { e.stopImmediatePropagation(); e.preventDefault(); } }

  function close(dismiss) {
    if (!shell) return;
    closedByUs = true;
    document.removeEventListener('keydown', onKey, true);
    var p = pathKey(); if (dismiss && p) { try { sessionStorage.setItem(dismissedKey(p), '1'); } catch (e) {} }
    /* put the practice section back where it lives */
    if (moved) { if (moved.next && moved.next.parentNode === moved.parent) moved.parent.insertBefore(moved.el, moved.next); else moved.parent.appendChild(moved.el); moved = null; }
    /* a quiz still inside the shell is closed with it */
    var ov = shell.querySelector('.kc-overlay'); if (ov) ov.remove();
    shell.remove(); shell = null;
    document.documentElement.classList.remove('sv-testout-open'); document.body.classList.remove('sv-testout-open');
    window.__svQuizFirst = false; window.__svTestoutStage = null;
  }

  window.svTestoutOpen = function () {
    if (shell) return;
    var p = pathKey(); if (!p) return;
    var btn = document.getElementById('knowledge-check-btn'); if (!btn) return;
    shell = build(); document.body.appendChild(shell);
    document.documentElement.classList.add('sv-testout-open'); document.body.classList.add('sv-testout-open');
    document.addEventListener('keydown', onKey, true);
    window.__svQuizFirst = true; closedByUs = false;
    /* open the quiz, then adopt its overlay into stage 1 */
    btn.click();
    var ov = document.querySelector('body > .kc-overlay');
    var s1 = shell.querySelector('.sv-to-s1');
    if (ov) s1.appendChild(ov);
    /* if the quiz closes on its own (its Close button, a stray click), that is "complete the full lesson" */
    var mo = new MutationObserver(function () {
      if (!shell || closedByUs) { mo.disconnect(); return; }
      if (!s1.querySelector('.kc-overlay') && !s1.hidden) { mo.disconnect(); close(true); }
    });
    mo.observe(s1, { childList: true });
    scrollTo(0, 0);
  };

  /* 4/5 — stage two: the practice section moves into the shell */
  window.svTestoutStage2 = function () {
    if (!shell) return false;
    var sec = document.getElementById('practice'); if (!sec) return false;
    var s1 = shell.querySelector('.sv-to-s1'), s2 = shell.querySelector('.sv-to-s2');
    var st = shell.querySelectorAll('.sv-to-stages li');
    st[0].className = 'done'; st[1].className = 'cur';
    s1.hidden = true; var ov = s1.querySelector('.kc-overlay'); if (ov) ov.remove();
    moved = { el: sec, parent: sec.parentNode, next: sec.nextSibling };
    s2.appendChild(sec); s2.hidden = false;
    window.__svTestoutStage = 'practice';
    var ta = document.getElementById('practice-answer'); if (ta) setTimeout(function () { ta.focus(); }, 300);
    shell.scrollTop = 0;
    return true;
  };

  /* the AI's mark is in: close the loop */
  window.svTestoutVerdict = function (ok, got, outOf) {
    if (!shell) return false;
    var st = shell.querySelectorAll('.sv-to-stages li');
    st[1].className = ok ? 'done' : 'cur';
    var v = shell.querySelector('.sv-to-verdict'); v.hidden = false; v.className = 'sv-to-verdict' + (ok ? ' ok' : '');
    var next = nextLessonHref();
    v.innerHTML = ok
      ? '<b>Covered.</b> ' + got + '/' + outOf + ' on the question — this lesson is done.' +
        '<span class="sv-to-acts">' + (next ? '<a class="kc-btn kc-btn-primary" href="' + next + '">Next lesson</a>' : '') + '<a class="kc-btn kc-btn-secondary" href="/classic">Back to my plan</a></span>'
      : '<b>Not this time.</b> ' + got + '/' + outOf + ' on the question.' +
        '<span class="sv-to-acts"><button type="button" class="kc-btn kc-btn-primary sv-to-full">Complete the full lesson</button></span>';
    var f = v.querySelector('.sv-to-full'); if (f) f.addEventListener('click', function () { close(true); });
    v.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return true;
  };
})();
