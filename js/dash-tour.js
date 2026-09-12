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
    { id: 'plan', title: 'Your plan for today',
      text: 'Every day, StudyVault picks three short things for you to do: a quick recap, one lesson, and a few flashcards. Press Start and it takes you through them one at a time. Most days it takes about 20 minutes.' },
    { id: 'revisit', title: 'Revisit: a quick recap',
      text: 'The first thing each day is a handful of questions on lessons you did a while ago. This is what stops you forgetting them. Get them right and you move on. Get them wrong and that lesson goes back on your list so you can do it again.' },
    { id: 'quickcheck', title: 'Already know a topic? Prove it and skip ahead',
      text: 'If you told us you feel confident about a topic, a lesson on it starts with a quick check instead of the full lesson. Get at least 4 out of 5 on the quiz, then at least half marks on an exam question, and that lesson is ticked off without reading it. If not, you do the lesson as normal.' },
    { id: 'books', title: 'Your subjects are the books',
      text: 'Each book on the shelf is one of your subjects. Tap a book to see its topics, then tap a topic to see its lessons. You can start any lesson from here. A book fills with colour from the bottom as you work through it.' },
    { id: 'rings', title: 'The coloured outlines',
      text: 'Each topic has an outline that tells you how well you know it right now. Green means it is secure. Amber means you are getting there. Red means it needs work. The colours change by themselves as you do quizzes, flashcards and exam questions.' },
    { id: 'week', title: 'How your week is going',
      text: 'Tap "This week" to see what you have done: the days you revised, the lessons you finished, the quizzes you passed and the flashcards you got right. On a Monday it shows you last week first, so you can see how it went.' },
    { id: 'flashcards', title: 'Flashcards',
      text: 'Flashcards are quick question-and-answer cards from the lessons you have done. Tap a card to see the answer, then say whether you got it right. Cards you get wrong come back sooner. Cards you know come back less often.' },
    { id: 'podcast', title: 'Listen while you do something else',
      text: 'The play button at the top plays a short podcast about one of your topics, a bit like a radio show. Use the skip button to change to another one. It keeps playing if you lock your phone, and finishing one counts as work on that lesson.' },
    { id: 'timer', title: 'The revision timer',
      text: 'Tap the timer at the top and choose 15, 25 or 45 minutes. It keeps counting as you move between pages, and it chimes when your time is up. Useful for deciding to do "just 25 minutes" and then stopping.' },
    { id: 'restday', title: 'Days off',
      text: 'When you set up your plan, you choose which days you revise. On your days off there is nothing you have to do. But if you fancy it, your plan shows what is coming up next, so you can get ahead. Anything you do on a day off is a bonus.' },
    { id: 'planner', title: 'Your exam countdown',
      text: 'The number at the top is how many days until your first exam. Tap it to see your whole plan on a calendar, right up to your last exam, including your days off and holidays. You can change your revising days and how long you revise here too.' },
    { id: 'reading', title: 'Make it easier on your eyes',
      text: 'Tap the moon at the top to switch to dark mode, make the text bigger, change to an easier-to-read font, or put a colour tint over the page. Whatever you pick stays on across every page, including the lessons.' }
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
    + '.svtour .vid{border-radius:0;min-height:0;height:100%;display:block}.svtour video{max-height:none;height:100%;width:100%;object-fit:contain}.svtour .side{padding:1rem 1.1rem 1.1rem}.svtour h3{font-size:1.15rem}.svtour p{font-size:.92rem}}'
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
