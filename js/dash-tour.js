/* "Show me around": the dashboard tour (Tom, 13 Sep 2026).
   Short muted clips of the demo students' dashboards, one per feature, with a
   title and two sentences each — so a new student sees the revisit slot, the
   quick check, a rest day and the rest even though their own dashboard has
   none of those states yet. Opens once on the first dashboard visit
   (sv-dash-tour-v1, account-synced), then from "Show me around" in the footer
   and the avatar menu; ?tour=1 forces it. Clips are recorded by
   scripts/dashboard_tour/record.py into assets/tour/ (manifest.json). */
(function () {
  'use strict';
  var KEY = 'sv-dash-tour-v1';
  var STEPS = [
    { id: 'plan', title: 'Here’s your plan',
      text: 'Three things for today, in order, and a Start button that runs them one after another. The lesson in the middle is the one the plan wants next.' },
    { id: 'revisit', title: 'The revisit',
      text: 'A few quick questions on lessons you learned a while ago, before they fade. Get them right and the topic stays secure; slip, and the lesson comes back into your plan to redo.' },
    { id: 'quickcheck', title: 'The quick check',
      text: 'Rated a topic confident? A lesson opens with a quick check first: get at least 4 out of 5, then at least half marks on an exam question, and you skip the full lesson.' },
    { id: 'books', title: 'Your subjects',
      text: 'Pick a book off the shelf to see its topics, then a topic to see its lessons. Books colour in from the bottom as you learn.' },
    { id: 'rings', title: 'What the rings mean',
      text: 'Each topic wears a ring: green is secure, amber is developing, red is emerging. They move as your quizzes, cards and marked answers come in, not just when you say so.' },
    { id: 'week', title: 'This week',
      text: 'Tap the week chip for the real numbers: days revised, lessons covered, quizzes passed, cards right. On Mondays it shows last week once, so you can see how it went.' },
    { id: 'flashcards', title: 'Flashcards',
      text: 'The cards due today, shuffled across your subjects. Tap to flip, then say whether you had it. Done for the day? “Want more?” keeps going.' },
    { id: 'podcast', title: 'Podcasts',
      text: 'Press play in the top bar for a podcast on one of your topics, and skip to the next. Finishing one counts towards that lesson.' },
    { id: 'timer', title: 'The revision timer',
      text: 'Tap the timer for 15, 25 or 45 minutes. It follows you from page to page and chimes when the time is up.' },
    { id: 'restday', title: 'Rest days',
      text: 'On a day you don’t revise, the plan shows what is up next instead, so if you do sit down you know where to start. Anything you do counts as a bonus.' },
    { id: 'planner', title: 'Your exam countdown',
      text: 'Tap the countdown for the whole plan: every day to your last paper, with rest days, holidays and the real exam dates once the boards publish them.' },
    { id: 'reading', title: 'Dark mode and reading settings',
      text: 'The moon opens dark mode, text size, a reading font and colour overlays. Set them here or in a lesson: they follow you everywhere.' }
  ];
  var manifest = null, dq = new URLSearchParams(location.search);
  function phone() { return matchMedia('(max-width:700px)').matches; }
  function g(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function mark() { try { localStorage.setItem(KEY, '1'); } catch (e) {} if (window.svProgressPushSoon) svProgressPushSoon(); }

  var CSS = ''
    + '.svtour{position:fixed;inset:0;z-index:980;background:rgba(20,14,8,.55);display:grid;place-items:center;padding:16px}'
    + '.svtour[hidden]{display:none}body.svtour-open{overflow:hidden}'
    + '.svtour .card{width:min(96vw,860px);max-height:94vh;overflow:auto;background:var(--card,#fffdf8);color:var(--ink,#26231e);border:1px solid var(--line,#e4dfd2);border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.4);display:grid;grid-template-columns:minmax(0,1.35fr) minmax(240px,1fr);font-family:"Schibsted Grotesk",system-ui,sans-serif;position:relative}'
    + '.svtour .vid{background:#1a1613;display:grid;place-items:center;min-height:200px;border-radius:10px 0 0 10px;overflow:hidden}'
    + '.svtour video{display:block;width:100%;height:auto;max-height:80vh;object-fit:contain}'
    + '.svtour .side{padding:1.3rem 1.4rem 1.1rem;display:flex;flex-direction:column;gap:.6rem;min-width:0}'
    + '.svtour .kick{font-size:.72rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--mut,#84806f)}'
    + '.svtour h3{margin:0;font-family:Literata,Georgia,serif;font-weight:600;font-size:1.3rem;line-height:1.2}'
    + '.svtour p{margin:0;font-family:Literata,Georgia,serif;font-size:.98rem;line-height:1.55;color:var(--sec,#57534a);flex:1}'
    + '.svtour .dots{display:flex;gap:5px;flex-wrap:wrap}.svtour .dots i{width:7px;height:7px;border-radius:50%;background:var(--line,#e4dfd2);display:block}.svtour .dots i.on{background:#c06325}'
    + '.svtour .btns{display:flex;gap:8px;align-items:center;margin-top:.2rem}'
    + '.svtour .btns button{font:600 .9rem "Schibsted Grotesk",system-ui,sans-serif;border:1px solid var(--line,#e4dfd2);background:var(--paper,#f6f1e7);color:var(--ink,#26231e);border-radius:4px;padding:.5rem .95rem;cursor:pointer}'
    + '.svtour .btns button.next{background:#c06325;border-color:#c06325;color:#fff;margin-left:auto}.svtour .btns button.next:hover{filter:brightness(1.06)}'
    + '.svtour .btns button:disabled{opacity:.4;cursor:default}'
    + '.svtour .x{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;border:none;background:rgba(0,0,0,.45);color:#fff;font-size:18px;cursor:pointer;z-index:2}'
    + '.svtour .step{font-size:.78rem;color:var(--mut,#84806f);font-variant-numeric:tabular-nums}'
    + '@media (max-width:700px){.svtour{padding:0;align-items:end}.svtour .card{width:100%;max-height:100dvh;height:100dvh;grid-template-columns:1fr;grid-template-rows:minmax(0,1fr) auto;border-radius:0}'
    + '.svtour .vid{border-radius:0;min-height:0}.svtour video{max-height:none;height:100%;width:auto;max-width:100%}.svtour .side{padding:1rem 1.1rem 1.1rem}.svtour h3{font-size:1.15rem}.svtour p{font-size:.92rem}}'
    + 'body.dark-mode .svtour .x{background:rgba(255,255,255,.18)}';

  var el = null, idx = 0;
  function build() {
    if (el) return el;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    el = document.createElement('div'); el.className = 'svtour'; el.hidden = true; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', 'Show me around');
    el.innerHTML = '<div class="card"><button type="button" class="x" aria-label="Close">×</button>'
      + '<div class="vid"><video muted autoplay loop playsinline preload="auto"></video></div>'
      + '<div class="side"><span class="kick">Show me around</span><h3></h3><p></p><div class="dots"></div>'
      + '<div class="btns"><button type="button" class="back">Back</button><span class="step"></span><button type="button" class="next">Next</button></div></div></div>';
    document.body.appendChild(el);
    var dots = el.querySelector('.dots'); STEPS.forEach(function () { dots.appendChild(document.createElement('i')); });
    el.querySelector('.x').addEventListener('click', close);
    el.querySelector('.back').addEventListener('click', function () { show(idx - 1); });
    el.querySelector('.next').addEventListener('click', function () { if (idx >= STEPS.length - 1) close(); else show(idx + 1); });
    el.addEventListener('click', function (e) { if (e.target === el) close(); });
    document.addEventListener('keydown', function (e) {
      if (el.hidden) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') show(idx + 1); else if (e.key === 'ArrowLeft') show(idx - 1);
    });
    return el;
  }
  function src(step) {
    var m = manifest && manifest[step.id], s = m && (m[phone() ? 'phone' : 'desktop'] || m.desktop || m.phone);
    return s || null;
  }
  function show(i) {
    idx = Math.max(0, Math.min(STEPS.length - 1, i));
    var s = STEPS[idx], v = el.querySelector('video'), f = src(s);
    el.querySelector('h3').textContent = s.title; el.querySelector('p').textContent = s.text;
    el.querySelector('.step').textContent = (idx + 1) + ' of ' + STEPS.length;
    el.querySelector('.back').disabled = idx === 0;
    el.querySelector('.next').textContent = idx === STEPS.length - 1 ? 'Done' : 'Next';
    [].forEach.call(el.querySelectorAll('.dots i'), function (d, k) { d.classList.toggle('on', k === idx); });
    v.innerHTML = '';
    if (f) {
      if (f.webm) { var s1 = document.createElement('source'); s1.src = f.webm; s1.type = 'video/webm'; v.appendChild(s1); }
      if (f.mp4) { var s2 = document.createElement('source'); s2.src = f.mp4; s2.type = 'video/mp4'; v.appendChild(s2); }
      v.load(); v.play && v.play().catch(function () {});
      v.parentNode.style.display = '';
    } else v.parentNode.style.display = 'none';
  }
  function open(at) {
    build();
    var go = function () { el.hidden = false; document.body.classList.add('svtour-open'); show(at || 0); mark(); };
    if (manifest) go();
    else fetch('/assets/tour/manifest.json').then(function (r) { return r.json(); }).then(function (m) { manifest = m; go(); }).catch(function () { manifest = {}; go(); });
  }
  function close() { if (!el) return; el.hidden = true; document.body.classList.remove('svtour-open'); var v = el.querySelector('video'); try { v.pause(); } catch (e) {} }
  window.svDashTour = { open: open, close: close };

  /* doors: the footer link (every dashboard), the avatar menu item (signed in — see dash-data.js) */
  function doors() {
    var row = document.querySelector('.legalrow');
    if (row && !row.querySelector('.tourlink')) {
      var a = document.createElement('a'); a.href = '#'; a.className = 'tourlink'; a.textContent = 'Show me around';
      a.addEventListener('click', function (e) { e.preventDefault(); open(0); });
      row.insertBefore(document.createTextNode(' · '), row.firstChild); row.insertBefore(a, row.firstChild);
    }
  }
  function boot() {
    doors();
    if (dq.get('tour') === '1') { setTimeout(function () { open(0); }, 900); return; }
    if (dq.get('demo') || dq.get('arrange') || dq.get('tour') === '0') return;
    if (g(KEY)) return;
    /* first dashboard visit: let the page settle, then show them round once */
    setTimeout(function () { if (!g(KEY)) open(0); }, 1600);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
