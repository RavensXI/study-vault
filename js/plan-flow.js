/* ============ Plan flow: today's plan as one run, not separate pages ============
   Start on a dashboard begins a run (sessionStorage, this tab only): revisit or warm-up, then
   the lesson, then flashcards. Between steps a short "what's next" screen ticks off the step just
   finished and names the next one, then carries on by itself.
     svFlow.begin({first:'Revisit'|'Warm-up', lesson:{url,title}, home})   on Start
     svFlow.run()                                                          the run, or null
     svFlow.bridge(doneStep, next, go)   doneStep 'first'|'lesson'|'cards'; next 'lesson'|'cards'|null
     svFlow.lessonProgress({pct,complete,next})   from the lesson page (js/main.js) on load and every change */
(function () {
  'use strict';
  var KEY = 'sv-run';
  var today = function () { return new Date().toISOString().slice(0, 10); };
  function get() { try { var r = JSON.parse(sessionStorage.getItem(KEY)); return r && r.date === today() ? r : null; } catch (e) { return null; } }
  function put(r) { try { sessionStorage.setItem(KEY, JSON.stringify(r)); } catch (e) {} }
  function end() { try { sessionStorage.removeItem(KEY); } catch (e) {} }
  var reduced = function () { return matchMedia('(prefers-reduced-motion: reduce)').matches; };

  var css =
    '.svf{position:fixed;inset:0;z-index:10000;display:grid;place-items:center;background:rgba(250,248,245,.94);backdrop-filter:blur(6px);opacity:0;transition:opacity .3s ease;font-family:Inter,system-ui,sans-serif;color:#2d2a26}' +
    '.svf.on{opacity:1}' +
    '.svf-box{width:min(420px,calc(100vw - 40px));text-align:center}' +
    '.svf-steps{list-style:none;margin:0 auto 28px;padding:0;text-align:left;display:inline-block}' +
    '.svf-steps li{display:flex;align-items:center;gap:12px;padding:7px 0;font-size:1rem;color:#8a857c;transition:color .3s}' +
    '.svf-steps li.done{color:#2d2a26}' +
    '.svf-steps li.next{color:#2d2a26;font-weight:600}' +
    '.svf-steps i{flex:none;width:24px;height:24px;border-radius:50%;border:2px solid #cfc8bb;position:relative;transition:background .3s,border-color .3s}' +
    '.svf-steps li.done i{background:#4e7a4a;border-color:#4e7a4a}' +
    '.svf-steps li.done i::after{content:"";position:absolute;left:7px;top:3px;width:6px;height:11px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}' +
    '.svf-steps li.just i{animation:svf-pop .5s cubic-bezier(.3,1.5,.5,1)}' +
    '.svf-steps li.next i{border-color:#2d2a26}' +
    '@keyframes svf-pop{0%{transform:scale(.4)}100%{transform:scale(1)}}' +
    '.svf h2{font:700 1.9rem/1.2 "Source Serif 4",Georgia,serif;margin:0 0 6px}' +
    '.svf p{margin:0 0 24px;color:#57534a;font-size:1.02rem}' +
    '.svf button{border:0;border-radius:10px;padding:.8rem 1.6rem;font:600 1rem Inter,system-ui,sans-serif;cursor:pointer;background:#2d2a26;color:#fff}' +
    '.svf .svf-bar{height:3px;background:#e8e2d6;border-radius:2px;margin:18px auto 0;width:120px;overflow:hidden}' +
    '.svf .svf-bar b{display:block;height:100%;width:0;background:#2d2a26;transition:width linear}' +
    'body.dark-mode .svf{background:rgba(24,22,20,.94);color:#ece9e4}body.dark-mode .svf h2,body.dark-mode .svf-steps li.done,body.dark-mode .svf-steps li.next{color:#ece9e4}' +
    'body.dark-mode .svf p{color:#b3aea6}body.dark-mode .svf button{background:#ece9e4;color:#181614}body.dark-mode .svf .svf-bar b{background:#ece9e4}' +
    '.svf-card{position:fixed;right:20px;bottom:20px;z-index:9999;width:min(340px,calc(100vw - 24px));background:var(--bg-card,#fffdf8);color:var(--text-primary,#2d2a26);' +
    'border:1px solid var(--border-light,#e4dfd2);border-radius:var(--radius,8px);padding:.85rem 1rem 1rem;box-shadow:0 12px 34px rgba(40,28,12,.16);' +
    'font:500 .9rem var(--font-ui,Inter,system-ui,sans-serif);opacity:0;transform:translateY(24px);transition:opacity .3s,transform .35s cubic-bezier(.16,1,.3,1)}' +
    'body[data-skin="reader"] .svf-card{border-radius:4px}' +
    '.svf-card.on{opacity:1;transform:none}' +
    '.svf-card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:.9rem}' +
    '.svf-card-h{font:600 .78rem var(--font-ui,Inter,system-ui,sans-serif);letter-spacing:.09em;text-transform:uppercase;color:var(--text-muted,#84806f)}' +
    '.svf-card-x{border:0;background:none;font-size:1.25rem;line-height:1;color:var(--text-muted,#84806f);cursor:pointer;padding:0 2px}' +
    '.svf-card .lesson-progress-bar{margin:0 0 .95rem}' +
    '.svf-card-act:empty{display:none}.svf-card-act .kc-btn{width:100%;text-align:center}' +
    '.svf-card.pulse{animation:svf-pulse 1.1s ease 2}' +
    '@keyframes svf-pulse{0%,100%{box-shadow:0 12px 34px rgba(40,28,12,.16),0 0 0 0 rgba(62,125,88,.45)}50%{box-shadow:0 12px 34px rgba(40,28,12,.16),0 0 0 10px rgba(62,125,88,0)}}' +
    '.svf-meter{width:84px;height:5px;border-radius:3px;background:var(--border-lighter,#efeadf);overflow:hidden;flex:none}' +
    '.svf-meter b{display:block;height:100%;background:var(--accent,#2d2a26);border-radius:3px;transition:width .5s ease}' +
    '.svf-nudge .kc-modal{max-width:400px}.svf-nbody{padding:1.1rem 1.25rem .4rem;font:1rem/1.5 var(--font-read,Georgia,serif);color:var(--text-primary,#2d2a26)}' +
    '.svf-nacts{display:flex;justify-content:flex-end;gap:.5rem;padding:1rem 1.25rem 1.15rem}' +
    '.svf-flash{animation:svf-flash 1.4s ease}@keyframes svf-flash{0%,100%{background:transparent}30%{background:color-mix(in srgb,var(--accent,#e9c46a) 18%,transparent)}}' +
    '@media (max-width:600px){.svf-card{left:12px;right:12px;bottom:12px;width:auto}}';
  function style() { if (document.getElementById('svf-css')) return; var s = document.createElement('style'); s.id = 'svf-css'; s.textContent = css; document.head.appendChild(s); }
  function esc(t) { var d = document.createElement('div'); d.textContent = t || ''; return d.innerHTML; }

  function begin(o) {
    var prev = get();
    put({ date: today(), first: o.first || 'Warm-up', lesson: o.lesson || null, home: o.home || location.pathname,
          done: prev && prev.lesson && o.lesson && prev.lesson.url === o.lesson.url ? prev.done : { first: false, lesson: false, cards: false } });
  }

  /* the in-between screen */
  function bridge(doneStep, next, go) {
    var r = get(); if (!r) { if (go) go(); return; }
    r.done[doneStep] = true; put(r);
    style();
    var rows = [['first', r.first], ['lesson', r.lesson ? r.lesson.title : 'Lesson'], ['cards', 'Flashcards']];
    var head = next === 'lesson' ? 'Lesson time' : next === 'cards' ? 'Flashcard time' : 'That’s today done';
    var sub = next === 'lesson' ? esc(r.lesson ? r.lesson.title : '') : next === 'cards' ? 'A few quick cards to lock it in.' : 'Nice work.';
    var el = document.createElement('div'); el.className = 'svf'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-live', 'polite');
    el.innerHTML = '<div class="svf-box"><ul class="svf-steps">' + rows.map(function (x) {
        return '<li class="' + (r.done[x[0]] ? 'done' : '') + (x[0] === doneStep ? ' just' : '') + (x[0] === next ? ' next' : '') + '"><i></i><span>' + esc(x[1]) + '</span></li>'; }).join('') +
      '</ul><h2>' + head + '</h2><p>' + sub + '</p><button type="button">' + (next ? 'Go' : 'Back to my plan') + '</button>' +
      (next ? '<div class="svf-bar"><b></b></div>' : '') + '</div>';
    /* the tick lands a beat after the screen does */
    var just = el.querySelector('li.just'); if (just) just.classList.remove('done');
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('on'); setTimeout(function () { if (just) just.classList.add('done'); }, reduced() ? 0 : 350); });
    var gone = false;
    var leave = function () { if (gone) return; gone = true;
      if (!next) { end(); el.classList.remove('on'); setTimeout(function () { el.remove(); if (go) go(); }, 300); return; }
      if (go) go(); setTimeout(function () { el.remove(); }, 1500); };
    el.querySelector('button').onclick = leave;
    el.querySelector('button').focus({ preventScroll: true });
    if (next) {   /* carries on by itself */
      var ms = reduced() ? 3500 : 2600, bar = el.querySelector('.svf-bar b');
      requestAnimationFrame(function () { bar.style.transitionDuration = ms + 'ms'; bar.style.width = '100%'; });
      setTimeout(leave, ms);
    }
  }

  /* ---- on a lesson page, the run's lesson: when something gets done, the lesson's progress bar pops up
     from the bottom, fills to where it now is and offers the next thing (taking them to it); past the
     line it offers the flashcards. Clicking away before the line asks once, gently. ---- */
  /* how each activity reads: imperative for the card, -ing for the prompt */
  var DO = { 'practice-question': ['Answer an exam question', 'Answering an exam question'], 'flashcards': ['Revise with the flashcards', 'Revising with the flashcards'],
    'revision-task': ['Do a revision task', 'Doing a revision task'], 'knowledge-check': ['Take the quick quiz', 'Taking the quick quiz'],
    'video': ['Watch the video', 'Watching the video'], 'podcast': ['Listen to the podcast', 'Listening to the podcast'],
    'interactive': ['Master the interactive', 'Mastering the interactive'], 'listen': ['Listen to the whole piece', 'Listening to the whole piece'] };
  var doing = function (n, i) { return (DO[n.id] || ['Keep going', 'A little more'])[i]; };
  var path = function (u) { try { return new URL(u, location.origin).pathname.replace(/\/$/, ''); } catch (e) { return u; } };
  function onRunLesson() { var r = get(); return !!(r && r.lesson && path(r.lesson.url) === path(location.pathname)); }
  var card = null, state = null, guarded = false, hideT = 0, lastPct = null;
  function toCards() {
    var r = get(); if (!r) return; closeCard(true);
    bridge('lesson', 'cards', function () { location.href = (r.home || '/classic') + '?cards=1'; });
  }
  /* where each activity lives on the lesson page: open it, or scroll to it */
  function goTo(id) {
    closeCard(true);
    var q = function (sel) { return document.querySelector(sel); };
    var scroll = function (el, then) { if (!el) return false; el.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'center' });
      el.classList.remove('svf-flash'); void el.offsetWidth; el.classList.add('svf-flash'); if (then) setTimeout(then, reduced() ? 0 : 550); return true; };
    var click = function (sel) { var b = q(sel); if (b) { b.click(); return true; } return false; };
    var ok =
      id === 'practice-question' ? (q('.sv-practice-btn')   /* the reading skin keeps the exam question in a panel */
        ? (click('.sv-practice-btn'), setTimeout(function () { var t = q('#practice-answer'); if (t) t.focus(); }, 300), true)
        : scroll(q('#practice'), function () { var t = q('#practice-answer'); if (t) t.focus({ preventScroll: true }); })) :
      id === 'knowledge-check' ? click('#knowledge-check-btn') :
      id === 'flashcards' ? click('#sidebar-flashcard-btn') :
      id === 'podcast' ? (click('.audio-tab[data-mode="podcast"]'), scroll(q('.audio-tab[data-mode="podcast"]'))) :
      id === 'video' ? scroll(q('#sidebar-video-section')) :
      id === 'revision-task' ? scroll(q('.revision-tip-btn')) :
      id === 'interactive' ? scroll(q('.sv-embed-strip')) :
      id === 'listen' ? scroll(q('.sv-listening')) : false;
    if (!ok) scroll([].slice.call(document.querySelectorAll('.lesson-progress-item[data-task="' + id + '"],.gutter-progress-item[data-task="' + id + '"]')).filter(function (x) { return x.getClientRects().length; })[0]);
  }
  function closeCard(now) {
    clearTimeout(hideT); if (!card) return; var c = card; card = null;
    c.classList.remove('on'); setTimeout(function () { c.remove(); }, now ? 0 : 320);
  }
  /* the lesson's own progress bar, popped up from the bottom when something is done: it fills from
     where it was to where it is now, then offers the next thing (or, past the line, the flashcards) */
  function popCard(from, p) {
    closeCard(true); style();
    var c = card = document.createElement('div'); c.className = 'svf-card'; c.setAttribute('role', 'status');
    var n = p.next;
    c.innerHTML = '<div class="svf-card-top"><span class="svf-card-h">' + (p.complete ? 'Lesson done \u2713' : n && n.finishes ? 'One more to finish' : 'Lesson progress') + '</span>' +
      '<button type="button" class="svf-card-x" aria-label="Close">×</button></div>' +
      '<div class="lesson-progress-bar"><div class="lesson-progress-bar-fill" style="width:' + from + '%"></div></div>' +
      '<div class="svf-card-act">' + (p.complete
        ? '<button type="button" class="kc-btn kc-btn-primary svf-go">Next: flashcards \u2192</button>'
        : n ? '<button type="button" class="kc-btn kc-btn-secondary svf-go">' + esc(doing(n, 0)) + ' \u2192</button>' : '') + '</div>';
    document.body.appendChild(c);
    c.querySelector('.svf-card-x').onclick = function () { closeCard(); };
    var go = c.querySelector('.svf-go'); if (go) go.onclick = p.complete ? toCards : function () { goTo(n.id); };
    requestAnimationFrame(function () { c.classList.add('on');
      setTimeout(function () { var f = c.querySelector('.lesson-progress-bar-fill'); f.style.transition = 'width 1s cubic-bezier(.16,1,.3,1)'; f.style.width = p.pct + '%'; }, reduced() ? 0 : 380);
      if (p.complete) setTimeout(function () { if (c === card) c.classList.add('pulse'); }, 1300); });
    /* it goes by itself, unless it's carrying them on to the flashcards (then it waits) */
    var arm = function () { clearTimeout(hideT); if (!p.complete) hideT = setTimeout(function () { if (c === card) closeCard(); }, 7000); };
    c.addEventListener('mouseenter', function () { clearTimeout(hideT); }); c.addEventListener('mouseleave', arm); c.addEventListener('focusin', function () { clearTimeout(hideT); });
    arm();
  }
  function lessonProgress(p) {
    if (!onRunLesson()) return;
    var prev = lastPct; lastPct = p.pct; state = p; guard();
    if (prev === null) { if (p.complete) popCard(p.pct, p); return; }     /* on arrival: only if it's already done */
    if (p.pct > prev || (p.complete && !(card && card.querySelector('.svf-go.kc-btn-primary')))) popCard(prev, p);
  }
  /* leaving before the line: one gentle prompt, not a wall */
  function guard() {
    if (guarded) return; guarded = true;
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || !state || state.complete || !onRunLesson() || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      var u; try { u = new URL(a.href, location.href); } catch (x) { return; }
      if (u.origin !== location.origin || (u.pathname === location.pathname)) return;
      e.preventDefault(); e.stopPropagation();
      nudge(function () { location.href = u.href; });
    }, true);
  }
  function nudge(leave) {
    style();
    /* the lesson page's own modal (the quick quiz's), so it looks like part of the lesson */
    var el = document.createElement('div'); el.className = 'kc-overlay svf-nudge'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true');
    var n = state.next;
    el.innerHTML = '<div class="kc-modal"><div class="kc-header"><span class="kc-title">Nearly there</span></div>' +
      '<div class="svf-nbody">' + (n ? esc(doing(n, 1)) + (n.finishes ? ' would finish this lesson.' : ' gets you closest to finishing it.') : 'A little more finishes this lesson.') + '</div>' +
      '<div class="svf-nacts"><button type="button" class="kc-btn kc-btn-secondary svf-leave">Leave anyway</button><button type="button" class="kc-btn kc-btn-primary svf-stay">Keep going</button></div></div>';
    document.body.appendChild(el);
    var close = function () { el.remove(); };
    el.querySelector('.svf-stay').onclick = function () { close(); if (n) setTimeout(function () { goTo(n.id); }, 250); };
    el.querySelector('.svf-leave').onclick = function () { close(); leave(); };
    el.querySelector('.svf-stay').focus({ preventScroll: true });
    el.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  window.svFlow = { begin: begin, run: get, bridge: bridge, lessonProgress: lessonProgress, onRunLesson: onRunLesson, end: end };
})();
