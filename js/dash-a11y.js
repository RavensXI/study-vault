/* Dark mode and reading settings on the dashboards (Tom, 13 Sep 2026).
   The lesson pages already keep dark mode, text size, the reading font and the
   colour overlay in localStorage `studyvault-a11y` (js/main.js, js/reader-skin.js,
   account-synced). This applies the same prefs to the classic dashboard and the
   desk, and adds one control in the top bar: a moon button opening a small
   "Reading" sheet. Set something here and the lessons follow, and vice versa.
   Simplify language and Focus mode stay lesson-only — they act on prose. */
(function () {
  'use strict';
  var KEY = 'studyvault-a11y';
  var FONTS = [
    { key: 'default', name: 'Default', css: '' },
    { key: 'atkinson', name: 'Atkinson Hyperlegible', css: "'Atkinson Hyperlegible',sans-serif" },
    { key: 'andika', name: 'Andika', css: "'Andika',sans-serif" }
  ];
  var OV = { yellow: '#fde047', blue: '#93c5fd', pink: '#f9a8d4', green: '#86efac', peach: '#fdba74', aqua: '#67e8f9' };
  function prefs() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(patch) { var p = prefs(); for (var k in patch) p[k] = patch[k]; try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {} if (window.svProgressPushSoon) svProgressPushSoon(); }

  var CSS = ''
    /* the control in the top bar */
    + '.svset{width:32px;height:32px;flex:none;border-radius:50%;border:1px solid var(--line,#e4dfd2);background:var(--card,#fffdf8);color:var(--sec,#57534a);cursor:pointer;display:grid;place-items:center;padding:0;transition:border-color .15s,color .15s}'
    + '.svset:hover{border-color:#c06325;color:#c06325}.svset svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    + '.svset[aria-expanded="true"]{border-color:#c06325;color:#c06325}'
    /* the sheet */
    + '.svset-pop{position:fixed;z-index:960;width:min(92vw,300px);background:var(--card,#fffdf8);color:var(--ink,#26231e);border:1px solid var(--line,#e4dfd2);border-radius:10px;box-shadow:0 14px 40px rgba(20,14,6,.22);padding:.7rem .85rem .85rem;font-family:"Schibsted Grotesk",system-ui,sans-serif;font-size:.88rem}'
    + '.svset-pop[hidden]{display:none}'
    + '.svset-pop h4{margin:0 0 .5rem;font-size:.72rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--mut,#84806f)}'
    + '.svset-pop .row{display:flex;align-items:center;justify-content:space-between;gap:.6rem;padding:.42rem 0;border-top:1px solid var(--linel,#efeadf)}'
    + '.svset-pop .row:first-of-type{border-top:none}.svset-pop .row>span:first-child{font-weight:600}'
    + '.svset-pop .sw{position:relative;width:38px;height:22px;border-radius:11px;border:1px solid var(--line,#e4dfd2);background:var(--paper,#f6f1e7);cursor:pointer;padding:0;flex:none}'
    + '.svset-pop .sw::after{content:"";position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:var(--sec,#57534a);transition:transform .18s}'
    + '.svset-pop .sw[aria-checked="true"]{background:#c06325;border-color:#c06325}.svset-pop .sw[aria-checked="true"]::after{background:#fff;transform:translateX(16px)}'
    + '.svset-pop .seg{display:flex;gap:4px}.svset-pop .seg button{font:600 .8rem "Schibsted Grotesk",system-ui,sans-serif;color:var(--sec,#57534a);background:var(--paper,#f6f1e7);border:1px solid var(--line,#e4dfd2);border-radius:4px;padding:.3rem .55rem;cursor:pointer;min-width:34px}'
    + '.svset-pop .seg button:hover{border-color:#c06325;color:#c06325}.svset-pop .seg button[aria-pressed="true"]{background:#c06325;border-color:#c06325;color:#fff}'
    + '.svset-pop .fonts{display:flex;flex-direction:column;gap:4px;width:100%}.svset-pop .fonts button{text-align:left;font-size:.9rem;padding:.36rem .6rem}'
    + '.svset-pop .fonts button.atkinson{font-family:"Atkinson Hyperlegible",sans-serif}.svset-pop .fonts button.andika{font-family:Andika,sans-serif}'
    + '.svset-pop .chips{display:flex;gap:6px;flex-wrap:wrap}.svset-pop .chips button{width:24px;height:24px;border-radius:50%;border:1px solid rgba(0,0,0,.18);cursor:pointer;padding:0;position:relative}'
    + '.svset-pop .chips button.none{background:var(--card,#fffdf8)}.svset-pop .chips button.none::after{content:"";position:absolute;left:4px;right:4px;top:50%;height:1.5px;background:var(--sec,#57534a);transform:rotate(-40deg)}'
    + '.svset-pop .chips button[aria-pressed="true"]{box-shadow:0 0 0 2px var(--card,#fffdf8),0 0 0 3.5px #c06325}'
    + '.svset-pop .col{flex-direction:column;align-items:stretch}.svset-pop .col>span:first-child{margin-bottom:.35rem}'
    + '.svset-pop input[type=range]{width:100%;accent-color:#c06325;margin:.35rem 0 0}'
    /* the colour overlay itself: a tinted sheet over everything, like the lessons */
    + '.sv-ovsheet{position:fixed;inset:0;pointer-events:none;z-index:9000;mix-blend-mode:multiply;opacity:var(--overlay-intensity,.45)}'
    + '.sv-ovsheet[hidden]{display:none}'
    /* dark surfaces for the shared pieces that carry their own light colours */
    + 'body.dark-mode .sv-avmenu{background:#211f1c;color:#ece9e4;border-color:#36332e}body.dark-mode .sv-avmenu .who{color:#8a857c;border-color:#2b2925}'
    + 'body.dark-mode .sv-avmenu button,body.dark-mode .sv-avmenu a{color:#ece9e4}body.dark-mode .sv-avmenu button:hover,body.dark-mode .sv-avmenu a:hover{background:#2b2925}'
    + 'body.dark-mode .wu-card{background:#211f1c;color:#ece9e4;border-color:#36332e}body.dark-mode .wu-opt{background:#181614;border-color:#36332e;color:#ece9e4}'
    + 'body.dark-mode .wu-opt.correct{background:#1c2f24;color:#9fd3b4}body.dark-mode .wu-opt.wrong{background:#3a221c;color:#f0a893}'
    + 'body.dark-mode .wu-go{background:#ece9e4;color:#181614}body.dark-mode .wu-go:hover{background:#fff}'
    + 'body.dark-mode .wu-sum p,body.dark-mode .wu-line{color:#b3aea6}body.dark-mode .wu-line{border-color:#2b2925}body.dark-mode .wu-line.ok b{color:#9fd3b4}body.dark-mode .wu-line b{color:#f0a893}'
    + 'body.dark-mode .wu-kick{color:#d9a27a}body.dark-mode .wu-dots i{background:#36332e}'
    + 'body.dark-mode .plsheet{background:#181614;color:#ece9e4}body.dark-mode .plctl,body.dark-mode .plday,body.dark-mode .pldaysheet,body.dark-mode .wkday button,body.dark-mode .plbtn,body.dark-mode .plnav button,body.dark-mode .plsheet .x{background:#211f1c;color:#ece9e4;border-color:#36332e}'
    + 'body.dark-mode .plday.hol{background:#2e2a1c;border-color:#4a4228}body.dark-mode .wkday button[aria-pressed="true"],body.dark-mode .plbtn.dark{background:#c9b48f;border-color:#c9b48f;color:#181614}';

  function inject() {
    if (document.getElementById('svset-css')) return;
    var st = document.createElement('style'); st.id = 'svset-css'; st.textContent = CSS; document.head.appendChild(st);
  }
  var fontsLoaded = false;
  function loadFonts() {
    if (fontsLoaded) return; fontsLoaded = true;
    var l = document.createElement('link'); l.rel = 'stylesheet';
    l.href = 'https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Andika:ital,wght@0,400;0,700;1,400;1,700&display=swap';
    document.head.appendChild(l);
  }
  /* ---- apply ---- */
  function applyDark(on) { document.body.classList.toggle('dark-mode', !!on); document.documentElement.classList.toggle('dark-mode', !!on); }
  function applySize(step) {
    var s = Math.max(-1, Math.min(2, +step || 0));
    document.documentElement.style.fontSize = s === 0 ? '' : ({ '-1': '94%', '1': '108%', '2': '116%' })[String(s)];
    return s;
  }
  function applyFont(key) {
    var f = FONTS.filter(function (x) { return x.key === key; })[0] || FONTS[0];
    if (f.css) { loadFonts(); document.body.style.setProperty('--read', f.css); document.body.style.setProperty('--font-read', f.css); }
    else { document.body.style.removeProperty('--read'); document.body.style.removeProperty('--font-read'); }
    return f.key;
  }
  var sheet = null;
  function applyOverlay(colour, intensity) {
    if (!sheet) { sheet = document.createElement('div'); sheet.className = 'sv-ovsheet'; sheet.hidden = true; document.body.appendChild(sheet); }
    if (colour && OV[colour]) { sheet.style.background = OV[colour]; sheet.hidden = false; } else sheet.hidden = true;
    var v = typeof intensity === 'number' ? intensity : 45;
    document.body.style.setProperty('--overlay-intensity', (v / 100).toFixed(2));
  }
  function applyAll() {
    var p = prefs();
    applyDark(p.darkMode); applySize(p.fontSize); applyFont(p.readingFont); applyOverlay(p.overlay, p.overlayIntensity);
  }

  /* ---- the control + sheet ---- */
  function build(where, before) {
    inject();
    var b = document.createElement('button'); b.type = 'button'; b.className = 'svset';
    b.setAttribute('aria-label', 'Dark mode and reading settings'); b.title = 'Dark mode and reading settings';
    b.setAttribute('aria-haspopup', 'true'); b.setAttribute('aria-expanded', 'false');
    b.innerHTML = '<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
    if (before && before.parentNode === where) where.insertBefore(b, before); else where.appendChild(b);
    var pop = document.createElement('div'); pop.className = 'svset-pop'; pop.hidden = true;
    pop.innerHTML = '<h4>Reading</h4>'
      + '<div class="row"><span>Dark mode</span><button type="button" class="sw" role="switch" aria-checked="false" aria-label="Dark mode"></button></div>'
      + '<div class="row"><span>Text size</span><span class="seg" role="group" aria-label="Text size"><button type="button" data-size="-1">A−</button><button type="button" data-size="0">A</button><button type="button" data-size="1">A+</button><button type="button" data-size="2">A++</button></span></div>'
      + '<div class="row col"><span>Reading font</span><span class="seg fonts" role="group" aria-label="Reading font">'
      + FONTS.map(function (f) { return '<button type="button" class="' + f.key + '" data-font="' + f.key + '">' + f.name + '</button>'; }).join('') + '</span></div>'
      + '<div class="row col"><span>Colour overlay</span><span class="chips" role="group" aria-label="Colour overlay"><button type="button" class="none" data-ov="" title="No overlay"></button>'
      + Object.keys(OV).map(function (k) { return '<button type="button" data-ov="' + k + '" title="' + k[0].toUpperCase() + k.slice(1) + ' overlay" style="background:' + OV[k] + '"></button>'; }).join('')
      + '</span><input type="range" min="10" max="100" step="5" aria-label="Overlay intensity" hidden></div>';
    document.body.appendChild(pop);
    var sw = pop.querySelector('.sw'), sizes = pop.querySelectorAll('[data-size]'), fonts = pop.querySelectorAll('[data-font]'), chips = pop.querySelectorAll('[data-ov]'), range = pop.querySelector('input[type=range]');
    function sync() {
      var p = prefs();
      sw.setAttribute('aria-checked', p.darkMode ? 'true' : 'false');
      var s = Math.max(-1, Math.min(2, +p.fontSize || 0));
      sizes.forEach(function (x) { x.setAttribute('aria-pressed', +x.dataset.size === s ? 'true' : 'false'); });
      var f = p.readingFont || 'default';
      fonts.forEach(function (x) { x.setAttribute('aria-pressed', x.dataset.font === f ? 'true' : 'false'); });
      var o = p.overlay || '';
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x.dataset.ov === o ? 'true' : 'false'); });
      range.hidden = !o; range.value = typeof p.overlayIntensity === 'number' ? p.overlayIntensity : 45;
    }
    sw.addEventListener('click', function () { var on = sw.getAttribute('aria-checked') !== 'true'; applyDark(on); save({ darkMode: on }); sync(); });
    sizes.forEach(function (x) { x.addEventListener('click', function () { var s = applySize(x.dataset.size); save({ fontSize: s }); sync(); }); });
    fonts.forEach(function (x) { x.addEventListener('click', function () { var k = applyFont(x.dataset.font); save({ readingFont: k }); sync(); }); });
    chips.forEach(function (x) { x.addEventListener('click', function () { var p = prefs(); applyOverlay(x.dataset.ov, p.overlayIntensity); save({ overlay: x.dataset.ov }); sync(); }); });
    range.addEventListener('input', function () { var p = prefs(); applyOverlay(p.overlay, +range.value); save({ overlayIntensity: +range.value }); });
    function place() { var r = b.getBoundingClientRect(); pop.style.top = (r.bottom + 8) + 'px'; pop.style.right = Math.max(8, window.innerWidth - r.right) + 'px'; pop.style.left = ''; }
    function open() { sync(); place(); pop.hidden = false; b.setAttribute('aria-expanded', 'true'); }
    function close() { pop.hidden = true; b.setAttribute('aria-expanded', 'false'); }
    b.addEventListener('click', function (e) { e.stopPropagation(); if (pop.hidden) open(); else close(); });
    document.addEventListener('click', function (e) { if (!pop.hidden && !pop.contains(e.target) && e.target !== b) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    window.addEventListener('resize', function () { if (!pop.hidden) place(); });
    return b;
  }
  function mount() {
    var top = document.querySelector('.top'); if (!top || document.querySelector('.svset')) return;
    /* classic: before "Cosy desk" (avatar / sign-up button stay last). desk: before the avatar in its right-hand group */
    var av = top.querySelector('.avatar'), cosy = top.querySelector('.cosy');
    var where = av ? av.parentNode : top, before = cosy && cosy.parentNode === where ? cosy : av;
    build(where, before);
  }
  applyAll();
  window.svDashA11y = { apply: applyAll, prefs: prefs, save: save };
  /* prefs can arrive from the account after boot (account-sync merges) — re-apply then */
  window.addEventListener('storage', function (e) { if (e.key === KEY) applyAll(); });
  document.addEventListener('sv-account-synced', applyAll);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
