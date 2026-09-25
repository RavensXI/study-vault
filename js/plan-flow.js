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
    '.svf-lessonbar{position:fixed;left:50%;bottom:18px;transform:translate(-50%,20px);z-index:9999;display:flex;align-items:center;gap:14px;opacity:0;' +
    'background:var(--bg-card,#fffdf8);color:var(--text-primary,#2d2a26);border:1px solid var(--border-light,#e4dfd2);border-radius:var(--radius,8px);padding:.6rem .7rem .6rem 1rem;' +
    'box-shadow:0 8px 28px rgba(40,28,12,.14);font:500 .9rem var(--font-ui,Inter,system-ui,sans-serif);transition:opacity .3s,transform .3s}' +
    'body[data-skin="reader"] .svf-lessonbar{border-radius:4px}' +
    '.svf-lessonbar.on{opacity:1;transform:translate(-50%,0)}' +
    '.svf-lessonbar.done{border-color:#3e7d58}.svf-lessonbar.done>span{color:#2c5940;font-weight:600}' +
    '.svf-lessonbar.pulse{animation:svf-pulse 1.1s ease 2}' +
    '@keyframes svf-pulse{0%,100%{box-shadow:0 8px 28px rgba(40,28,12,.14),0 0 0 0 rgba(62,125,88,.45)}50%{box-shadow:0 8px 28px rgba(40,28,12,.14),0 0 0 10px rgba(62,125,88,0)}}' +
    '.svf-meter{width:84px;height:5px;border-radius:3px;background:var(--border-lighter,#efeadf);overflow:hidden;flex:none}' +
    '.svf-meter b{display:block;height:100%;background:var(--accent,#2d2a26);border-radius:3px;transition:width .5s ease}' +
    '.svf-nudge .kc-modal{max-width:400px}.svf-nbody{padding:1.1rem 1.25rem .4rem;font:1rem/1.5 var(--font-read,Georgia,serif);color:var(--text-primary,#2d2a26)}' +
    '.svf-nacts{display:flex;justify-content:flex-end;gap:.5rem;padding:1rem 1.25rem 1.15rem}' +
    '.svf-flash{animation:svf-flash 1.4s ease}@keyframes svf-flash{0%,100%{background:transparent}30%{background:color-mix(in srgb,var(--accent,#e9c46a) 18%,transparent)}}' +
    'html.svf-barred body{padding-bottom:90px}' +
    '@media (max-width:600px){.svf-lessonbar{left:12px;right:12px;transform:translateY(20px);bottom:12px;font-size:.85rem}.svf-lessonbar.on{transform:none}.svf-lessonbar>span:nth-child(2){flex:1}.svf-meter{width:48px}}';
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

  /* ---- on a lesson page, the run's lesson: a bar at the foot shows how far through it is and one
     thing that would finish it; past the line it turns into "Lesson done · Next: flashcards" (with a
     pulse, so it's noticed). Clicking away before the line asks once, gently. ---- */
  /* how each activity reads: imperative for the bar, -ing for the prompt */
  var DO = { 'practice-question': ['Answer an exam question', 'Answering an exam question'], 'flashcards': ['Revise with the flashcards', 'Revising with the flashcards'],
    'revision-task': ['Do a revision task', 'Doing a revision task'], 'knowledge-check': ['Take the quick quiz', 'Taking the quick quiz'],
    'video': ['Watch the video', 'Watching the video'], 'podcast': ['Listen to the podcast', 'Listening to the podcast'],
    'interactive': ['Master the interactive', 'Mastering the interactive'], 'listen': ['Listen to the whole piece', 'Listening to the whole piece'] };
  var doing = function (n, i) { return (DO[n.id] || ['Keep going', 'A little more'])[i]; };
  var path = function (u) { try { return new URL(u, location.origin).pathname.replace(/\/$/, ''); } catch (e) { return u; } };
  function onRunLesson() { var r = get(); return !!(r && r.lesson && path(r.lesson.url) === path(location.pathname)); }
  var bar = null, state = null, guarded = false;
  function toCards() {
    var r = get(); if (!r) return; if (bar) { bar.remove(); bar = null; document.documentElement.classList.remove('svf-barred'); }
    bridge('lesson', 'cards', function () { location.href = (r.home || '/classic') + '?cards=1'; });
  }
  function showTask(id) {
    var el = [].slice.call(document.querySelectorAll('.lesson-progress-item[data-task="' + id + '"],.gutter-progress-item[data-task="' + id + '"]'))
      .filter(function (x) { return x.getClientRects().length; })[0];
    if (!el) return;
    el.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'center' });
    el.classList.remove('svf-flash'); void el.offsetWidth; el.classList.add('svf-flash');
  }
  function lessonProgress(p) {
    if (!onRunLesson()) return;
    style(); state = p;
    if (!bar) { bar = document.createElement('div'); bar.className = 'svf-lessonbar'; bar.setAttribute('role', 'status'); document.body.appendChild(bar);
      document.documentElement.classList.add('svf-barred');   /* room under the page so the bar never covers its last links */
      requestAnimationFrame(function () { bar.classList.add('on'); }); }
    var wasDone = bar.classList.contains('done');
    if (p.complete) {
      bar.classList.add('done');
      bar.innerHTML = '<span>Lesson done \u2713</span><button type="button" class="kc-btn kc-btn-primary">Next: flashcards \u2192</button>';
      bar.querySelector('button').onclick = toCards;
      if (!wasDone && bar.dataset.seen) { bar.classList.remove('pulse'); void bar.offsetWidth; bar.classList.add('pulse'); }
    } else {
      bar.classList.remove('done');
      var pct = Math.min(100, Math.round(p.pct / 50 * 100));   /* the bar fills to the finishing line, not to 100% of everything */
      bar.innerHTML = '<span class="svf-meter"><b style="width:' + pct + '%"></b></span><span>' + (p.next ? esc(doing(p.next, 0)) + (p.next.finishes ? ' to finish' : ' next') : 'Keep going') + '</span>' +
        (p.next ? '<button type="button" class="kc-btn kc-btn-secondary">Show me</button>' : '');
      var sb = bar.querySelector('button'); if (sb) sb.onclick = function () { showTask(p.next.id); };
    }
    bar.dataset.seen = '1';
    guard();
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
    el.querySelector('.svf-stay').onclick = function () { close(); if (n) setTimeout(function () { showTask(n.id); }, 250); };
    el.querySelector('.svf-leave').onclick = function () { close(); leave(); };
    el.querySelector('.svf-stay').focus({ preventScroll: true });
    el.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  window.svFlow = { begin: begin, run: get, bridge: bridge, lessonProgress: lessonProgress, onRunLesson: onRunLesson, end: end };
})();
