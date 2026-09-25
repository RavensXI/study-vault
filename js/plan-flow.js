/* ============ Plan flow: today's plan as one run, not separate pages ============
   Start on a dashboard begins a run (sessionStorage, this tab only): revisit or warm-up, then
   the lesson, then flashcards. Between steps a short "what's next" screen ticks off the step just
   finished and names the next one, then carries on by itself.
     svFlow.begin({first:'Revisit'|'Warm-up', lesson:{url,title}, home})   on Start
     svFlow.run()                                                          the run, or null
     svFlow.bridge(doneStep, next, go)   doneStep 'first'|'lesson'|'cards'; next 'lesson'|'cards'|null
     svFlow.lessonDone()                 on a lesson page when the run's lesson completes */
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
    '.svf-lessonbar{position:fixed;left:50%;bottom:20px;transform:translate(-50%,20px);z-index:9999;display:flex;align-items:center;gap:14px;opacity:0;' +
    'background:#2d2a26;color:#fff;border-radius:12px;padding:.7rem .8rem .7rem 1.2rem;box-shadow:0 10px 30px rgba(0,0,0,.25);font:500 .95rem Inter,system-ui,sans-serif;transition:opacity .3s,transform .3s}' +
    '.svf-lessonbar.on{opacity:1;transform:translate(-50%,0)}' +
    '.svf-lessonbar button{border:0;border-radius:8px;padding:.55rem 1rem;background:#fff;color:#2d2a26;font:600 .92rem Inter,system-ui,sans-serif;cursor:pointer}';
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

  /* on a lesson page: when the run's lesson completes, offer the next step (never interrupt reading) */
  function lessonDone() {
    var r = get(); if (!r || !r.lesson || r.done.lesson) return false;
    var path = function (u) { try { return new URL(u, location.origin).pathname.replace(/\/$/, ''); } catch (e) { return u; } };
    if (path(r.lesson.url) !== path(location.pathname)) return false;
    r.done.lesson = true; put(r); style();
    var bar = document.createElement('div'); bar.className = 'svf-lessonbar';
    bar.innerHTML = '<span>Lesson done ✓</span><button type="button">Next: flashcards →</button>';
    document.body.appendChild(bar);
    requestAnimationFrame(function () { bar.classList.add('on'); });
    bar.querySelector('button').onclick = function () {
      bar.remove(); r.done.lesson = false; put(r);   /* bridge ticks it on screen */
      bridge('lesson', 'cards', function () { location.href = (r.home || '/classic') + '?cards=1'; });
    };
    return true;
  }

  window.svFlow = { begin: begin, run: get, bridge: bridge, lessonDone: lessonDone, end: end };
})();
