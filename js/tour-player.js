/* The tour player (Tom, 13 Sep 2026): one modal that steps through short muted
   clips with a title and a plain-language description each. Used by the
   dashboard tour (js/dash-tour.js) and the lesson tour (js/lesson-tour.js).
   Clips come from scripts/dashboard_tour/record.py; each set has its own
   manifest.json listing desktop and phone files per step id.

     var t = svTourPlayer({ key: 'sv-dash-tour-v1', manifest: '/assets/tour/manifest.json',
                            kicker: 'Show me around', steps: [{ id, title, text }, ...] });
     t.open(0); t.close();                                                                   */
(function () {
  'use strict';
  var CSS = ''
    + '.sv-tourclips{position:fixed;inset:0;z-index:10060;background:rgba(20,14,8,.55);display:grid;place-items:center;padding:16px}'
    + '.sv-tourclips[hidden]{display:none}body.sv-tourclips-open{overflow:hidden}'
    + '.sv-tourclips .card{width:min(96vw,860px);max-height:94vh;overflow:auto;background:var(--card,#fffdf8);color:var(--ink,#26231e);border:1px solid var(--line,#e4dfd2);border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.4);display:grid;grid-template-columns:minmax(0,1.35fr) minmax(240px,1fr);font-family:"Schibsted Grotesk",system-ui,sans-serif;position:relative}'
    + '.sv-tourclips .vid{background:#1a1613;display:grid;place-items:center;min-height:200px;border-radius:10px 0 0 10px;overflow:hidden}'
    + '.sv-tourclips video{display:block;width:100%;height:auto;max-height:80vh;object-fit:contain}'
    + '.sv-tourclips .side{padding:1.3rem 1.4rem 1.1rem;display:flex;flex-direction:column;gap:.6rem;min-width:0}'
    + '.sv-tourclips .kick{font-size:.72rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--mut,#84806f)}'
    + '.sv-tourclips h3{margin:0;font-family:Literata,Georgia,serif;font-weight:600;font-size:1.3rem;line-height:1.2}'
    + '.sv-tourclips p{margin:0;font-family:Literata,Georgia,serif;font-size:.98rem;line-height:1.55;color:var(--sec,#57534a);flex:1}'
    + '.sv-tourclips .dots{display:flex;gap:5px;flex-wrap:wrap}.sv-tourclips .dots i{width:7px;height:7px;border-radius:50%;background:var(--line,#e4dfd2);display:block}.sv-tourclips .dots i.on{background:#c06325}'
    + '.sv-tourclips .btns{display:flex;gap:8px;align-items:center;margin-top:.2rem}'
    + '.sv-tourclips .btns button{font:600 .9rem "Schibsted Grotesk",system-ui,sans-serif;border:1px solid var(--line,#e4dfd2);background:var(--paper,#f6f1e7);color:var(--ink,#26231e);border-radius:4px;padding:.5rem .95rem;cursor:pointer}'
    + '.sv-tourclips .btns button.next{background:#c06325;border-color:#c06325;color:#fff;margin-left:auto}.sv-tourclips .btns button.next:hover{filter:brightness(1.06)}'
    + '.sv-tourclips .btns button:disabled{opacity:.4;cursor:default}'
    + '.sv-tourclips .x{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;border:none;background:rgba(0,0,0,.45);color:#fff;font-size:18px;cursor:pointer;z-index:2}'
    + '.sv-tourclips .step{font-size:.78rem;color:var(--mut,#84806f);font-variant-numeric:tabular-nums}'
    + '@media (max-width:700px){.sv-tourclips{padding:0;align-items:end}.sv-tourclips .card{width:100%;max-height:100dvh;height:100dvh;grid-template-columns:1fr;grid-template-rows:minmax(0,1fr) auto;border-radius:0}'
    + '.sv-tourclips .vid{border-radius:0;min-height:0;height:100%;display:block}.sv-tourclips video{max-height:none;height:100%;width:100%;object-fit:contain}.sv-tourclips .side{padding:1rem 1.1rem 1.1rem}.sv-tourclips h3{font-size:1.15rem}.sv-tourclips p{font-size:.92rem}}'
    /* lesson pages carry their own palette variables; the card stays paper there too */
    + 'body[data-skin] .sv-tourclips .card{--card:#fffdf8;--ink:#26231e;--sec:#57534a;--mut:#84806f;--line:#e4dfd2;--paper:#f6f1e7}'
    + 'body.dark-mode .sv-tourclips .card{--card:#211f1c;--ink:#ece9e4;--sec:#b3aea6;--mut:#8a857c;--line:#36332e;--paper:#181614}'
    + 'body.dark-mode .sv-tourclips .x{background:rgba(255,255,255,.18)}';

  function phone() { return matchMedia('(max-width:700px)').matches; }

  window.svTourPlayer = function (cfg) {
    var STEPS = cfg.steps, KEY = cfg.key, el = null, idx = 0, manifest = null;
    function mark() { try { localStorage.setItem(KEY, '1'); } catch (e) {} if (window.svProgressPushSoon) svProgressPushSoon(); }
    function build() {
      if (el) return el;
      if (!document.getElementById('sv-tourclips-css')) { var st = document.createElement('style'); st.id = 'sv-tourclips-css'; st.textContent = CSS; document.head.appendChild(st); }
      el = document.createElement('div'); el.className = 'sv-tourclips'; el.hidden = true; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', cfg.kicker || 'Show me around');
      el.innerHTML = '<div class="card"><button type="button" class="x" aria-label="Close">×</button>'
        + '<div class="vid"><video muted autoplay loop playsinline preload="auto"></video></div>'
        + '<div class="side"><span class="kick"></span><h3></h3><p></p><div class="dots"></div>'
        + '<div class="btns"><button type="button" class="back">Back</button><span class="step"></span><button type="button" class="next">Next</button></div></div></div>';
      el.querySelector('.kick').textContent = cfg.kicker || 'Show me around';
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
      var go = function () { el.hidden = false; document.body.classList.add('sv-tourclips-open'); show(at || 0); mark(); };
      if (manifest) go();
      else fetch(cfg.manifest).then(function (r) { return r.json(); }).then(function (m) { manifest = m; go(); }).catch(function () { manifest = {}; go(); });
    }
    function close() { if (!el) return; el.hidden = true; document.body.classList.remove('sv-tourclips-open'); var v = el.querySelector('video'); try { v.pause(); } catch (e) {} }
    function seen() { try { return !!localStorage.getItem(KEY); } catch (e) { return true; } }
    return { open: open, close: close, seen: seen, isOpen: function () { return !!el && !el.hidden; } };
  };
})();
