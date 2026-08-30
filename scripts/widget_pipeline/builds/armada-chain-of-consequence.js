/* ============================================================
   The Armada's chain of disaster  --  History, Historic Environment 2027
   Lesson 13: "The Spanish Armada".

   Misconception attacked: the campaign was decided by English gunnery,
   or simply by "the weather". The lesson teaches a chain of geographic
   and logistical consequences, and the storm belongs at the END of it,
   as a consequence, not at the start as a cause.

   Two things happen here, and only one has an answer:
     - the map panel is free reading: six sites of this seaborne "site",
       each with its geographic feature and what that feature caused;
     - the chain is the task: five links, shuffled, reordered by tapping
       one statement then another to swap them. NOTHING is marked until
       "Check the chain" is pressed (commit before feedback). Only then
       does the widget rebuild the true chain, mark which steps the
       student had in the right place, and print the "so..." clause that
       makes each link force the next.

   Every figure and date is the lesson's own: 27 July (Calais roadstead),
   the night of 28 July (eight fireships), 29 July (Gravelines), and the
   north-about route home. No claim is made that the lesson does not make.
   ============================================================ */
window.SVWidget = {
  meta: {
    id: 'armada-chain-of-consequence',
    title: 'The Armada’s chain of disaster',
    teaches: 'The Armada was destroyed by a chain of geographic and logistical consequences — no deep-water port, an exposed anchorage, fireships, cut anchor cables, storm coasts — with the storm last in the chain, not first.'
  },

  mount: function (root, ctx) {
    'use strict';

    var reduced = !!(ctx && ctx.reducedMotion);
    var accent = '';
    /* read the accent from OUR OWN node: two layers set --accent and they disagree */
    try { accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) {}
    if (!accent) { accent = (ctx && ctx.accent) || '#8a6a4f'; }

    /* ================= content ================= */

    /* LINKS are stored in the true causal order; index === true step. */
    var LINKS = [
      {
        id: 'port',
        text: 'No deep-water port for the fleet to wait in',
        brief: 'the missing port',
        note: 'Parma’s invasion army was ready in Flanders — but his ports at Dunkirk and Nieuwpoort were too shallow for the Armada’s great ships, and Dutch gunboats patrolled outside.',
        why: 'so the fleet had to wait in open water',
        reason: 'The missing port starts the chain: the Armada had nowhere safe to wait for Parma’s army.'
      },
      {
        id: 'roadstead',
        text: 'Forced to anchor in open water off Calais',
        brief: 'the open roadstead',
        note: 'On 27 July the Armada anchored off Calais in open water — not a harbour. No shelter from wind or attack; it was simply the only place left to wait for Parma.',
        why: 'so the packed fleet was an easy target for fireships',
        reason: 'The open anchorage comes next: the fleet only lay there because no harbour could take it.'
      },
      {
        id: 'fireships',
        text: 'Fireships sent into the crowded anchorage',
        brief: 'the fireships',
        note: 'On the night of 28 July the English set eight ships ablaze and let the wind carry them into the anchored fleet, their loaded guns firing as they burned.',
        why: 'so captains cut their anchor cables to escape',
        reason: 'The fireships only worked because the fleet was already anchored close together in open water.'
      },
      {
        id: 'cables',
        text: 'Anchor cables cut to escape',
        brief: 'the cut cables',
        note: 'No time to raise the anchors: captains cut the cables and left their best anchors on the seabed — the very anchors they would need to survive a storm.',
        why: 'so the fleet had no anchors to hold it off a rocky coast',
        reason: 'The cables were cut to escape the fireships, so the fireships come before them.'
      },
      {
        id: 'wrecks',
        text: 'Wrecked on Scottish and Irish coasts',
        brief: 'the wrecks',
        note: 'Sailing home the long way round, autumn gales drove the battered, anchorless ships onto some of the most dangerous coasts in Europe.',
        why: '',
        reason: 'The wrecks come last: without anchors, ships caught in gales had no way to keep themselves off the rocks.'
      }
    ];
    var N = LINKS.length;

    var GUNS = 'English gunfire never broke the crescent formation — one night of fireships did.';

    var SITES = [
      { name: 'The Lizard', head: 'The Lizard, 19 July',
        feature: 'Chains of hilltop beacons ran along the south coast and inland to London.',
        result: 'The alarm crossed southern England in hours; Philip’s planners worked on months-old news.',
        x: 61, y: 167 },
      { name: 'Plymouth to Wight', head: 'Plymouth to the Isle of Wight',
        feature: 'English home ports lay close behind — powder, shot, food, repairs — and the wind mostly favoured the English.',
        result: 'A week of running battle never broke the crescent, but every Spanish mile led further from help.',
        x: 88, y: 159 },
      { name: 'Calais anchorage', head: 'Calais anchorage, 27 July',
        feature: 'Not a harbour — open water, exposed to wind and attack, because there was nowhere else to go.',
        result: 'Ships anchored close together in the dark — the one target fireships could not miss.',
        x: 126, y: 142 },
      { name: 'Gravelines', head: 'Gravelines, 29 July',
        feature: 'The English finally closed to point-blank range, and the wind drove the scattered fleet towards the Zeeland sandbanks.',
        result: 'A last-minute wind change let the Armada escape north into the North Sea — but the way home through the Channel was now closed.',
        x: 133, y: 140 },
      { name: 'Parma’s ports', head: 'Dunkirk and Nieuwpoort',
        feature: 'Parma’s embarkation ports were shallow, fringed by sandbanks and blockaded by Dutch flyboats.',
        result: 'No deep-water port on the invasion coast: the Armada could reach Parma but never wait for him.',
        x: 141, y: 138 },
      { name: 'Scotland & Ireland', head: 'Scotland and Ireland',
        feature: 'Autumn gales, no anchors, storm-damaged hulls and starving crews on Europe’s most dangerous coasts.',
        result: 'Perhaps half the fleet never reached Spain; far more men died of drowning, disease and hunger than to guns.',
        x: 17, y: 92 }
    ];

    /* ================= state ================= */
    var order = [];          /* position -> link index: the student's working chain */
    var attempt = null;      /* snapshot of `order` at the moment Check was pressed */
    var selected = -1;       /* position currently picked up, or -1 */
    var checked = false;
    var openSite = -1;
    var visited = {};

    function scoreOf(arr) {
      var n = 0, i;
      for (i = 0; i < N; i++) { if (arr[i] === i) { n++; } }
      return n;
    }
    function sameAs(a, b) {
      if (!a || !b) { return false; }
      for (var i = 0; i < N; i++) { if (a[i] !== b[i]) { return false; } }
      return true;
    }
    /* a fresh chain that is never already right, never nearly right, and never
       the one just used -- so pressing Check is always a real commit */
    function shuffle(previous) {
      var a, guard = 0;
      do {
        a = [];
        for (var i = 0; i < N; i++) { a.push(i); }
        for (var j = N - 1; j > 0; j--) {
          var k = Math.floor(Math.random() * (j + 1)), t = a[j];
          a[j] = a[k]; a[k] = t;
        }
        guard++;
      } while ((scoreOf(a) > 1 || sameAs(a, previous)) && guard < 200);
      return a;
    }

    /* ================= styles (every selector scoped to .svw-arm) ================= */
    var CSS = [
      '.svw-arm{background:#fff;border-radius:16px;padding:.85rem .95rem .95rem;',
        'color:#2d2a26;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;box-sizing:border-box}',
      '.svw-arm *{box-sizing:border-box}',
      '.svw-arm .a-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;',
        'color:var(--a);margin:0 0 .1rem}',
      '.svw-arm .a-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;',
        'line-height:1.2;margin:0 0 .5rem}',
      '.svw-arm .a-main{display:grid;gap:.6rem;align-items:start}',
      '.svw-arm.is-wide .a-main{grid-template-columns:minmax(205px,1fr) minmax(240px,1fr);gap:.8rem}',
      /* --- map panel --- */
      '.svw-arm .a-map{position:relative;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
        'padding:.35rem;display:flex;gap:.4rem;align-items:stretch}',
      /* The map is a locator, not the main event: in one-column mode it stops
         growing at 165px wide (about 184px tall), which is what keeps a
         500-600px card inside the height budget. */
      '.svw-arm .a-svg{flex:0 0 46%;width:46%;max-width:165px;height:auto;display:block}',
      '.svw-arm.is-wide .a-svg{max-width:none}',
      '.svw-arm .a-list{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;',
        'gap:.1rem;min-width:0}',
      '.svw-arm .a-site{display:flex;align-items:center;gap:.35rem;width:100%;text-align:left;',
        'background:transparent;border:1px solid transparent;border-radius:8px;padding:.22rem .3rem;',
        'font:inherit;font-size:.7rem;font-weight:600;line-height:1.15;color:#5b564e;cursor:pointer}',
      '.svw-arm .a-site .d{flex:0 0 7px;height:7px;border-radius:50%;background:var(--a);opacity:.4}',
      '.svw-arm .a-site:hover{border-color:#e0d9cd;color:#2d2a26}',
      '.svw-arm .a-site.seen .d{opacity:1}',
      '.svw-arm .a-site.on{background:#fff;border-color:var(--a);color:#2d2a26}',
      '.svw-arm .a-site.on .d{opacity:1}',
      /* the site note lies over the map, so reading costs no height */
      '.svw-arm .a-pop{position:absolute;inset:4px;background:#fff;border:1px solid #e2dbd0;',
        'border-radius:10px;padding:.5rem .55rem;display:none;flex-direction:column;',
        'justify-content:center;gap:.26rem}',
      '.svw-arm .a-pop.on{display:flex}',
      '.svw-arm .a-pop h4{margin:0;font-size:.78rem;font-weight:700;padding-right:1.1rem}',
      '.svw-arm .a-pop p{margin:0;font-size:.73rem;line-height:1.34;color:#5b564e}',
      '.svw-arm .a-pop p.r{color:#2d2a26}',
      '.svw-arm .a-x{position:absolute;top:1px;right:2px;background:transparent;border:0;cursor:pointer;',
        'font:inherit;font-size:.95rem;line-height:1;color:#8d8880;padding:.3rem .38rem}',
      '.svw-arm .a-x:hover{color:#2d2a26}',
      /* --- the chain --- */
      '.svw-arm .a-lab{font-size:.72rem;font-weight:600;color:#5b564e;margin:0 0 .28rem}',
      '.svw-arm .a-row{display:flex;align-items:center;gap:.45rem;width:100%;text-align:left;',
        'background:#faf8f5;border:1px solid #e8e2d9;border-radius:10px;padding:.3rem .42rem;',
        'font:inherit;font-size:.79rem;line-height:1.25;color:#2d2a26;cursor:pointer}',
      '.svw-arm .a-row:hover{border-color:#cdc4b5}',
      '.svw-arm .a-row.sel{background:#fff;border-color:var(--a);box-shadow:inset 0 0 0 1px var(--a)}',
      '.svw-arm .a-row[disabled]{opacity:1;cursor:default}',
      '.svw-arm .a-row.miss .a-t{color:#8d8880}',
      '.svw-arm .a-n{flex:0 0 17px;height:17px;border-radius:5px;background:#ece6dc;color:#5b564e;',
        'font-size:.64rem;font-weight:700;display:flex;align-items:center;justify-content:center;',
        'font-variant-numeric:tabular-nums}',
      '.svw-arm .a-row.hit .a-n{background:#4f7d63;color:#fff}',
      '.svw-arm .a-t{flex:1 1 auto;min-width:0}',
      '.svw-arm .a-m{flex:0 0 13px;text-align:center;font-size:.82rem;font-weight:700;color:#a49c90}',
      '.svw-arm .a-row.hit .a-m{color:#4f7d63}',
      '.svw-arm .a-link{display:flex;align-items:center;gap:.3rem;padding-left:22px;min-height:12px;',
        'color:#8d8880;font-size:.7rem;line-height:1.2}',
      '.svw-arm .a-link .v{color:#c3bbac;font-size:.72rem}',
      /* --- action + caption --- */
      '.svw-arm .a-act{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-top:.5rem}',
      '.svw-arm .a-btn{font:inherit;font-size:.82rem;font-weight:600;padding:.44rem .9rem;',
        'border-radius:10px;background:#faf8f5;color:#2d2a26;border:1px solid #ddd7cd;cursor:pointer}',
      '.svw-arm .a-btn:hover{border-color:#b9b0a2}',
      '.svw-arm .a-btn.primary{background:#2d2a26;color:#fff;border-color:#2d2a26}',
      '.svw-arm .a-cap{font-size:.85rem;line-height:1.5;color:#5b564e;margin:.45rem 0 0;min-height:2.6em}',
      '.svw-arm .a-cap b{color:#2d2a26;font-weight:600}',
      '.svw-arm button:focus-visible{outline:2px solid var(--a);outline-offset:2px}',
      '.svw-arm .a-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;',
        'clip:rect(0 0 0 0);white-space:nowrap;border:0}',
      reduced ? '' : '.svw-arm .a-row,.svw-arm .a-site,.svw-arm .a-btn{transition:background .16s ease,border-color .16s ease,color .16s ease}',
      '@media (max-width:400px){.svw-arm{padding:.7rem .75rem .8rem}}'
    ].join('');

    /* ================= the map =================
       Every coastline point is a real place plotted on a plain lat/lon grid:
       x = (lon + 12) * 9.44, y = (61 - lat) * 14.6, so 1 px is about 7.1 km
       east-west and 6.8 km north-south. The outline is simplified, not
       distorted: the Bristol Channel, the Moray and Forth firths, the Wash,
       the Cotentin and the Flanders coast all sit where they belong, which is
       the point of showing a map at all. */
    var SVG = [
      '<svg class="a-svg" viewBox="0 0 170 190" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">',
      '<rect x="0" y="0" width="170" height="190" rx="6" fill="#dde7ee"/>',
      /* France, Flanders and the Low Countries */
      '<path d="M65.1,183.3 L80.2,179.6 L94.4,180.3 L95.3,169.3 L98.1,165.2 L102.9,169.3 L114.2,167.9 ',
      'L123.6,161.3 L128.3,157.7 L128.3,150.1 L130.6,146.7 L133.3,146.1 L135.6,145.5 L139.1,144.1 ',
      'L140.6,142.6 L145.3,137.9 L149.1,134.3 L152,131.4 L158.1,117.5 L165.2,110.9 L170,108 L170,190 ',
      'L58,190 Z" fill="#ece4d6" stroke="#c6bcac" stroke-width="0.7"/>',
      /* Britain */
      '<path d="M59.5,159.8 L70.8,146 L85,140.1 L63.3,135.5 L63.3,132.6 L74.6,124.1 L68,119 L70.8,112.4 ',
      'L82.1,111.7 L85,105.9 L84.5,100.7 L79.3,94.9 L79.3,88.3 L67,92.7 L68.9,80.3 L59.5,83.2 L56.6,67.1 ',
      'L54.8,62.1 L60.5,52.6 L66.1,35 L85,34.5 L79.3,42.3 L73.6,51.1 L85,48.2 L94.4,48.2 L93.5,56.2 ',
      'L89.7,62.7 L83,72.3 L89.7,73 L94.4,75.9 L100,87.6 L107.6,94.9 L114.2,108 L116.1,118.3 L125.5,118.3 ',
      'L129.8,124.1 L125.5,132.9 L119.8,138.7 L126.4,140.2 L125.6,144.2 L122.4,147.7 L115.6,150 ',
      'L105.7,150.3 L101,151 L90.1,153.4 L78.8,157.6 L74.2,155.4 L64.2,161.4 Z" ',
      'fill="#ece4d6" stroke="#c6bcac" stroke-width="0.7"/>',
      /* Ireland */
      '<path d="M43.4,81.8 L56.6,84.7 L61.4,93.4 L54.3,111.7 L56.6,119.7 L52.8,128.5 L42.5,130 L33,135.5 ',
      'L20.7,139.2 L17,130 L22.7,122.6 L19.8,111.7 L17.9,97.8 L32.1,97.8 L34,93.4 L34.9,85.4 Z" ',
      'fill="#ece4d6" stroke="#c6bcac" stroke-width="0.7"/>',
      /* Orkney, Shetland, the Hebrides: the wrecking isles */
      '<g fill="#ece4d6" stroke="#c6bcac" stroke-width="0.6">',
      '<ellipse cx="85" cy="29.2" rx="3.4" ry="2.2"/><ellipse cx="100.9" cy="10.2" rx="1.7" ry="3.4"/>',
      '<ellipse cx="49.1" cy="40.9" rx="2.4" ry="3.8"/><ellipse cx="44.3" cy="49.6" rx="1.7" ry="3"/>',
      '<ellipse cx="47.2" cy="59.9" rx="1.5" ry="2.3"/></g>',
      /* the Zeeland sandbanks */
      '<g fill="#c6bcac">',
      '<circle cx="144" cy="133" r="0.8"/><circle cx="148" cy="131" r="0.8"/><circle cx="151.5" cy="129" r="0.8"/>',
      '<circle cx="146" cy="136" r="0.8"/><circle cx="150" cy="134" r="0.8"/></g>',
      /* wreck marks: west of Ireland, and off the northern isles */
      '<g stroke="#a49a8b" stroke-width="0.8" stroke-linecap="round">',
      '<path d="M10,99 l3,3 M13,99 l-3,3"/><path d="M8,116 l3,3 M11,116 l-3,3"/>',
      '<path d="M13,131 l3,3 M16,131 l-3,3"/><path d="M56,27 l3,3 M59,27 l-3,3"/>',
      '<path d="M41,35 l3,3 M44,35 l-3,3"/></g>',
      /* the route: up the Channel, round Scotland, down past Ireland, home */
      '<path d="M44,190 C52,182 56,174 62,167 C70,163 78,161 88,159 C98,156 104,155 112,151 ',
      'C118,148 122,145 126,142 C132,139 136,137 140,133 C146,127 150,122 151,112 ',
      'C152,100 148,88 140,76 C130,60 116,44 100,32 C94,27 90,24 85,22 C76,19 68,20 60,26 ',
      'C50,34 42,44 36,56 C28,72 20,86 14,102 C10,114 8,126 9,138 C10,152 14,166 22,177 ',
      'C25,182 28,186 30,190" fill="none" stroke="', accent, '" ',
      'stroke-width="1.4" stroke-linecap="round" stroke-dasharray="3.5 3"/>',
      '<g fill="', accent, '">',
      '<polygon points="98,152.4 104,155.3 98,158.2"/>',
      '<polygon points="75,18.2 68.5,21 75,23.8"/>',
      '<polygon points="8.4,115 13.8,116.4 10.2,121"/></g>',
      /* orientation labels */
      '<g fill="#93897c" font-family="Inter,system-ui,sans-serif" font-size="8" font-weight="600" letter-spacing="0.5">',
      '<text x="35" y="112" text-anchor="middle">IRELAND</text>',
      '<text x="75" y="56" text-anchor="middle">SCOTLAND</text>',
      '<text x="106" y="129" text-anchor="middle">ENGLAND</text>',
      '<text x="107" y="177" text-anchor="middle">FRANCE</text>',
      '<text x="31" y="187" font-size="6.5" letter-spacing="0.2">from Spain</text></g>',
      '<g class="a-pins"></g>',
      '</svg>'
    ].join('');

    /* ================= build the DOM once, then mutate it ================= */
    function mk(tag, cls, txt) {
      var e = document.createElement(tag);
      if (cls) { e.className = cls; }
      if (txt != null) { e.textContent = txt; }
      return e;
    }
    function svgEl(tag, attrs) {
      var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
      for (var k in attrs) { if (attrs.hasOwnProperty(k)) { e.setAttribute(k, attrs[k]); } }
      return e;
    }

    root.className = (root.className ? root.className + ' ' : '') + 'svw-arm';
    root.style.setProperty('--a', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    root.appendChild(style);

    root.appendChild(mk('div', 'a-kick', 'Interactive'));
    root.appendChild(mk('h3', 'a-title', 'The Armada’s chain of disaster'));

    var main = mk('div', 'a-main');
    root.appendChild(main);

    /* --- map panel --- */
    var mapWrap = mk('div', 'a-map');
    mapWrap.innerHTML = SVG;
    var svg = mapWrap.querySelector('svg');
    var pinG = mapWrap.querySelector('.a-pins');

    var siteList = mk('div', 'a-list');
    var siteBtns = SITES.map(function (s, i) {
      var b = mk('button', 'a-site');
      b.type = 'button';
      b.appendChild(mk('span', 'd'));
      b.appendChild(mk('span', null, s.name));
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function () { toggleSite(i); });
      siteList.appendChild(b);
      return b;
    });
    mapWrap.appendChild(siteList);

    /* Pins are a pointer shortcut only. The named list is the accessible
       route, so the map adds no duplicate tab stops and no tiny key targets. */
    var pins = SITES.map(function (s, i) {
      var g = svgEl('g', { style: 'cursor:pointer' });
      var ring = svgEl('circle', { cx: s.x, cy: s.y, r: 5.5, fill: 'none',
        stroke: accent, 'stroke-width': 1, opacity: 0 });
      var dot = svgEl('circle', { cx: s.x, cy: s.y, r: 2.4, fill: accent,
        stroke: '#fff', 'stroke-width': 0.9 });
      var hit = svgEl('circle', { cx: s.x, cy: s.y, r: 7, fill: 'transparent' });
      g.appendChild(ring); g.appendChild(dot); g.appendChild(hit);
      g.addEventListener('click', function () { toggleSite(i); });
      pinG.appendChild(g);
      return { ring: ring, dot: dot };
    });

    var pop = mk('div', 'a-pop');
    pop.setAttribute('aria-live', 'polite');
    var popX = mk('button', 'a-x', '×');
    popX.type = 'button';
    popX.setAttribute('aria-label', 'Close this site note');
    popX.addEventListener('click', function () { toggleSite(openSite); });
    var popH = mk('h4', null, '');
    var popF = mk('p', 'f', '');
    var popR = mk('p', 'r', '');
    pop.appendChild(popX); pop.appendChild(popH); pop.appendChild(popF); pop.appendChild(popR);
    mapWrap.appendChild(pop);
    main.appendChild(mapWrap);

    /* --- the chain --- */
    var chain = mk('div', 'a-chain');
    chain.appendChild(mk('div', 'a-lab', 'The chain: first cause at the top'));
    var rows = [], whys = [];
    for (var p = 0; p < N; p++) {
      var r = mk('button', 'a-row');
      r.type = 'button';
      var txt = mk('span', 'a-t', '');
      var mark = mk('span', 'a-m', '');
      r.appendChild(mk('span', 'a-n', String(p + 1)));
      r.appendChild(txt);
      r.appendChild(mark);
      (function (pos, btn) {
        btn.addEventListener('click', function () { tapRow(pos); });
      })(p, r);
      chain.appendChild(r);
      rows.push({ btn: r, txt: txt, mark: mark });
      if (p < N - 1) {
        var lk = mk('div', 'a-link');
        lk.appendChild(mk('span', 'v', '↓'));
        var lt = mk('span', 'w', '');
        lk.appendChild(lt);
        chain.appendChild(lk);
        whys.push(lt);
      }
    }
    main.appendChild(chain);

    /* --- action + caption --- */
    var act = mk('div', 'a-act');
    var goBtn = mk('button', 'a-btn primary', 'Check the chain');
    goBtn.type = 'button';
    goBtn.addEventListener('click', function () { if (checked) { reset(); } else { check(); } });
    act.appendChild(goBtn);
    root.appendChild(act);

    var cap = mk('p', 'a-cap', '');
    cap.setAttribute('aria-live', 'polite');
    root.appendChild(cap);

    var sr = mk('p', 'a-sr', '');
    root.appendChild(sr);

    /* ================= behaviour ================= */
    var capHTML = '';

    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    function intro() {
      return 'Five links in one chain. Each one was forced by the link before it.';
    }

    function toggleSite(i) {
      if (i < 0) { return; }
      openSite = (openSite === i) ? -1 : i;
      if (openSite >= 0) {
        visited[SITES[openSite].name] = true;
        popH.textContent = SITES[openSite].head;
        popF.textContent = SITES[openSite].feature;
        popR.textContent = '→ ' + SITES[openSite].result;
      }
      render();
    }

    /* tap one statement to pick it up, tap another to swap them.
       No verdict of any kind happens here. */
    function tapRow(pos) {
      if (checked) { return; }
      if (selected === -1) {
        selected = pos;
        capHTML = esc(LINKS[order[pos]].note);
      } else if (selected === pos) {
        selected = -1;
        capHTML = intro();
      } else {
        var moved = order[selected];
        order[selected] = order[pos];
        order[pos] = moved;
        selected = -1;
        capHTML = esc(LINKS[moved].note);
      }
      render();
    }

    function check() {
      attempt = order.slice();
      order = [];
      for (var i = 0; i < N; i++) { order.push(i); }   /* rebuild as the true chain */
      checked = true;
      selected = -1;
      capHTML = verdict();
      render();
      goBtn.focus();
    }

    function reset() {
      order = shuffle(attempt);
      attempt = null;
      checked = false;
      selected = -1;
      capHTML = intro();
      render();
      rows[0].btn.focus();
    }

    /* the reveal: name what the student did, then why the true link belongs
       there, then the thing the whole lesson is arguing against */
    function verdict() {
      if (scoreOf(attempt) === N) {
        return '<b>Right.</b> And English gunfire is not in the chain at all: a week of it never broke ' +
               'the crescent — the fireships did that in one night, and the lost anchors finished the ' +
               'fleet off Scotland and Ireland.';
      }
      var i = 0;
      while (i < N && attempt[i] === i) { i++; }
      return 'You had <b>' + esc(LINKS[attempt[i]].brief) + '</b> at step ' + (i + 1) + '. ' +
             esc(LINKS[i].reason) + ' ' + esc(GUNS);
    }

    function render() {
      var i;
      syncWide();
      for (i = 0; i < N; i++) {
        var link = LINKS[order[i]];
        var hit = checked && attempt[i] === i;
        rows[i].txt.textContent = link.text;
        rows[i].btn.classList.toggle('sel', !checked && selected === i);
        rows[i].btn.classList.toggle('hit', !!hit);
        rows[i].btn.classList.toggle('miss', checked && !hit);
        rows[i].btn.setAttribute('aria-pressed', (!checked && selected === i) ? 'true' : 'false');
        rows[i].mark.textContent = checked ? (hit ? '✓' : '✗') : '';
        rows[i].btn.disabled = checked;
        var lab = 'Step ' + (i + 1) + ': ' + link.text;
        if (checked) {
          lab += hit ? '. You had this one here.'
                     : '. You had this at step ' + (attempt.indexOf(order[i]) + 1) + '.';
        }
        rows[i].btn.setAttribute('aria-label', lab);
      }
      for (i = 0; i < whys.length; i++) {
        whys[i].textContent = checked ? LINKS[i].why : '';
      }
      for (i = 0; i < SITES.length; i++) {
        var on = (openSite === i);
        siteBtns[i].classList.toggle('on', on);
        siteBtns[i].classList.toggle('seen', !!visited[SITES[i].name]);
        siteBtns[i].setAttribute('aria-expanded', on ? 'true' : 'false');
        pins[i].ring.setAttribute('opacity', on ? '1' : '0');
        pins[i].dot.setAttribute('r', on ? '3.4' : '2.4');
      }
      pop.classList.toggle('on', openSite >= 0);
      root.classList.toggle('is-checked', checked);
      goBtn.textContent = checked ? 'Shuffle and try again' : 'Check the chain';
      goBtn.className = 'a-btn' + (checked ? '' : ' primary');
      cap.innerHTML = capHTML;
      sr.textContent = 'Chain now reads: ' + order.map(function (k, n) {
        return (n + 1) + ' ' + LINKS[k].text;
      }).join('; ') + '.';
      setState();
    }

    function setState() {
      var shown = (checked ? attempt : order).map(function (k) { return LINKS[k].id; });
      var n = 0, k;
      for (k in visited) { if (visited.hasOwnProperty(k)) { n++; } }
      root.dataset.svState = JSON.stringify({
        chain: shown,
        checked: checked,
        score: checked ? scoreOf(attempt) : 0,
        correct: checked ? (scoreOf(attempt) === N) : false,
        selected: selected,
        openSite: openSite >= 0 ? SITES[openSite].name : null,
        sitesRead: n
      });
    }

    /* two columns as soon as the card can give both readable line lengths --
       measured on the card itself, not the viewport */
    function syncWide() {
      var w = root.clientWidth || 0;
      /* Two columns from 500px of card: below that the statement column
         drops under ~30 characters a line; above it, staying single-column
         costs more than it saves - at a 560px stage the one-column card ran
         619px, over the 600px budget (found by the check harness). */
      var wide = w >= 500;
      root.classList.toggle('is-wide', wide);
      svg.style.flexBasis = wide ? '50%' : '46%';
      svg.style.width = wide ? '50%' : '46%';
    }
    /* Escape closes an open site note, and drops a picked-up statement */
    root.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' && e.keyCode !== 27) { return; }
      if (openSite >= 0) { toggleSite(openSite); }
      else if (selected >= 0) { selected = -1; capHTML = intro(); render(); }
    });

    /* belt and braces: the observer covers a resize, the window listener covers
       browsers without one, and render() re-checks on every interaction, so a
       widget mounted into a modal that is still hidden corrects itself on the
       first frame it is seen. No repeating timer. */
    if (window.ResizeObserver) { new ResizeObserver(syncWide).observe(root); }
    if (window.addEventListener) { window.addEventListener('resize', syncWide); }
    if (window.requestAnimationFrame) { requestAnimationFrame(syncWide); }

    order = shuffle(null);
    capHTML = intro();
    syncWide();
    render();
  }
};
