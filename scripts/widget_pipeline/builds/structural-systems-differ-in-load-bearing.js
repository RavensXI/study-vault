/* Structural systems differ in load-bearing.
   One section through a building; the student commits to which parts carry
   the load (or which can be taken out), then the load path is drawn.
   Every verdict, arrow and sentence is derived from part.carries, so the
   reveal cannot drift from the answer. */
(function () {
  'use strict';

  var ID = 'structural-systems-differ-in-load-bearing';

  /* ---------------------------------------------------------------- draw */

  function arrow(x1, y1, x2, y2) {
    var a = Math.atan2(y2 - y1, x2 - x1), h = 7.5, w = 4.4;
    var bx = x2 - Math.cos(a) * h, by = y2 - Math.sin(a) * h;
    var nx = Math.cos(a + Math.PI / 2) * w, ny = Math.sin(a + Math.PI / 2) * w;
    var r = function (n) { return Math.round(n * 10) / 10; };
    var pts = r(x2) + ' ' + r(y2) + ',' + r(bx + nx) + ' ' + r(by + ny) + ',' + r(bx - nx) + ' ' + r(by - ny);
    return '<line class="halo" x1="' + x1 + '" y1="' + y1 + '" x2="' + r(bx) + '" y2="' + r(by) + '"/>' +
           '<line class="ld" x1="' + x1 + '" y1="' + y1 + '" x2="' + r(bx) + '" y2="' + r(by) + '"/>' +
           '<polygon class="ldh" points="' + pts + '"/>';
  }

  function soil() {
    var s = '<rect class="soil" x="0" y="162" width="400" height="38"/>' +
            '<line class="gl" x1="2" y1="162" x2="398" y2="162"/>';
    for (var x = 12; x < 400; x += 26) {
      s += '<line class="hatch" x1="' + x + '" y1="170" x2="' + (x - 9) + '" y2="184"/>';
    }
    return s;
  }

  function ribs(x, y, w, h, n) {
    var s = '', i, gx;
    for (i = 1; i < n; i++) { gx = x + (w * i / n); s += '<line class="rib" x1="' + gx + '" y1="' + (y + 2) + '" x2="' + gx + '" y2="' + (y + h - 2) + '"/>'; }
    return s;
  }

  function panes(x, y, w, h, n) {
    return '<rect class="sh glass" x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"/>' + ribs(x, y, w, h, n);
  }

  /* --------------------------------------------------------------- model */

  var BUILDINGS = {

    cottage: {
      alt: 'Section through a two-storey brick and block cottage.',
      scenery:
        soil() +
        '<path class="roofp" d="M50 58 L200 16 L350 58 Z"/>' +
        '<line class="hair" x1="66" y1="58" x2="334" y2="58"/>' +
        '<rect class="slab" x="66" y="157" width="268" height="5"/>',
      parts: {
        ext: {
          name: 'Cavity walls', carries: true, badge: [74, 88],
          why: 'the roof and both floors land on them and run straight down the masonry',
          svg: '<rect class="sh brick" x="66" y="58" width="16" height="104"/>' +
               '<rect class="sh brick" x="318" y="58" width="16" height="104"/>' +
               '<line class="crs" x1="66" y1="96" x2="82" y2="96"/><line class="crs" x1="318" y1="96" x2="334" y2="96"/>' +
               '<line class="crs" x1="66" y1="130" x2="82" y2="130"/><line class="crs" x1="318" y1="130" x2="334" y2="130"/>' +
               '<line class="crs" x1="66" y1="78" x2="82" y2="78"/><line class="crs" x1="318" y1="78" x2="334" y2="78"/>' +
               '<line class="crs" x1="66" y1="113" x2="82" y2="113"/><line class="crs" x1="318" y1="113" x2="334" y2="113"/>' +
               '<line class="crs" x1="66" y1="147" x2="82" y2="147"/><line class="crs" x1="318" y1="147" x2="334" y2="147"/>'
        },
        joists: {
          name: 'Floor joists', carries: true, badge: [288, 108],
          why: 'they bridge the floor load across the room onto the walls at each end',
          svg: '<rect class="sh timber" x="82" y="104" width="236" height="8"/>' + ribs(82, 104, 236, 8, 12)
        },
        spine: {
          name: 'Spine wall', carries: true, badge: [199, 140],
          why: 'the joists sit on it, so half the first floor comes down it',
          svg: '<rect class="sh brick" x="192" y="112" width="14" height="50"/><line class="crs" x1="192" y1="138" x2="206" y2="138"/>'
        },
        stud: {
          name: 'Stud partition', carries: false, badge: [254, 78],
          whyNot: 'it only divides two bedrooms, and the roof trusses above span outer wall to outer wall',
          svg: '<rect class="sh timber" x="249" y="58" width="9" height="46"/>' +
               '<line class="rib" x1="253.5" y1="60" x2="253.5" y2="102"/>' +
               '<line class="rib" x1="249" y1="72" x2="258" y2="72"/><line class="rib" x1="249" y1="88" x2="258" y2="88"/>'
        },
        found: {
          name: 'Strip foundations', carries: true, badge: [74, 173],
          why: 'they spread the whole weight along the soil under every load-bearing wall',
          svg: '<rect class="sh conc" x="58" y="162" width="32" height="17"/>' +
               '<rect class="sh conc" x="310" y="162" width="32" height="17"/>' +
               '<rect class="sh conc" x="185" y="162" width="28" height="17"/>'
        }
      },
      path: arrow(165, 32, 106, 51) + arrow(235, 32, 294, 51) +
            arrow(74, 64, 74, 154) + arrow(326, 64, 326, 154) + arrow(199, 118, 199, 154) +
            arrow(74, 182, 74, 194) + arrow(199, 182, 199, 194) + arrow(326, 182, 326, 194)
    },

    office: {
      alt: 'Section through a three-storey steel-framed office.',
      scenery:
        soil() +
        '<rect class="slab" x="88" y="29" width="227" height="5"/>' +
        '<rect class="slab" x="88" y="71" width="227" height="5"/>' +
        '<rect class="slab" x="88" y="114" width="227" height="5"/>' +
        '<rect class="slab" x="88" y="157" width="227" height="5"/>',
      parts: {
        cols: {
          name: 'Steel columns', carries: true, badge: [201, 58],
          why: 'every beam ends on a column, so all of it comes down the steel',
          svg: '<rect class="sh steel" x="88" y="34" width="11" height="128"/>' +
               '<rect class="sh steel" x="196" y="34" width="11" height="128"/>' +
               '<rect class="sh steel" x="304" y="34" width="11" height="128"/>'
        },
        beams: {
          name: 'Steel beams', carries: true, badge: [258, 80],
          why: 'the floor slabs rest on them and they pass it sideways into the columns',
          svg: '<rect class="sh steel" x="88" y="34" width="227" height="8"/>' +
               '<rect class="sh steel" x="88" y="76" width="227" height="8"/>' +
               '<rect class="sh steel" x="88" y="119" width="227" height="8"/>'
        },
        infill: {
          name: 'Blockwork infill', carries: false, badge: [146, 145],
          whyNot: 'it just fills the gap between two columns',
          svg: '<rect class="sh block" x="99" y="127" width="97" height="35"/>' +
               '<line class="crs" x1="99" y1="139" x2="196" y2="139"/><line class="crs" x1="99" y1="151" x2="196" y2="151"/>'
        },
        glaze: {
          name: 'Glazing panels', carries: false, badge: [146, 58],
          whyNot: 'it is a weather skin hung on the frame',
          svg: panes(99, 42, 97, 34, 3) + panes(207, 42, 97, 34, 3) + panes(99, 84, 97, 35, 3)
        },
        wallp: {
          name: 'Plasterboard partition', carries: false, badge: [252, 145],
          whyNot: 'it is plasterboard on light studs, dividing space only',
          svg: '<rect class="sh timber" x="248" y="127" width="7" height="35"/>'
        },
        pads: {
          name: 'Pad foundations', carries: true, badge: [201, 173],
          why: 'each pad spreads one column load into the ground',
          svg: '<rect class="sh conc" x="76" y="162" width="35" height="17"/>' +
               '<rect class="sh conc" x="184" y="162" width="35" height="17"/>' +
               '<rect class="sh conc" x="292" y="162" width="35" height="17"/>'
        }
      },
      path: arrow(150, 22, 104, 26) + arrow(252, 22, 300, 26) +
            arrow(150, 70, 104, 70) + arrow(252, 70, 300, 70) +
            arrow(150, 113, 104, 113) + arrow(252, 113, 300, 113) +
            arrow(93.5, 44, 93.5, 154) + arrow(201.5, 44, 201.5, 154) + arrow(309.5, 44, 309.5, 154) +
            arrow(93.5, 182, 93.5, 194) + arrow(201.5, 182, 201.5, 194) + arrow(309.5, 182, 309.5, 194)
    },

    portal: {
      alt: 'Section through a single-storey steel portal frame showroom.',
      scenery:
        soil() +
        '<path class="sheet" d="M64 62 L200 23 L336 62"/>' +
        '<rect class="slab" x="64" y="157" width="272" height="5"/>',
      parts: {
        pcol: {
          name: 'Portal columns', carries: true, badge: [76, 140],
          why: 'the rafters drive their load into them at the haunch',
          svg: '<rect class="sh steel" x="70" y="66" width="12" height="96"/>' +
               '<rect class="sh steel" x="318" y="66" width="12" height="96"/>'
        },
        rafter: {
          name: 'Rafters', carries: true, badge: [148, 46],
          why: 'sheeting, wind and snow all run down the slope to the eaves',
          svg: '<path class="sh steelline" d="M70 66 L200 28 L330 66"/>' +
               '<polygon class="sh steel" points="70 50,112 60,70 68"/>' +
               '<polygon class="sh steel" points="330 50,288 60,330 68"/>'
        },
        purlin: {
          name: 'Purlins', carries: true, badge: [252, 42],
          why: 'they carry the sheeting across to the rafters and hold the rafters straight',
          svg: '<rect class="sh steel" x="105" y="43" width="8" height="8"/>' +
               '<rect class="sh steel" x="137" y="34" width="8" height="8"/>' +
               '<rect class="sh steel" x="170" y="24" width="8" height="8"/>' +
               '<rect class="sh steel" x="235" y="28" width="8" height="8"/>' +
               '<rect class="sh steel" x="267" y="37" width="8" height="8"/>' +
               '<rect class="sh steel" x="300" y="47" width="8" height="8"/>'
        },
        clad: {
          name: 'Wall cladding', carries: false, badge: [62, 92],
          whyNot: 'it is a thin skin screwed to side rails, keeping the weather out',
          svg: '<rect class="sh clad" x="56" y="60" width="13" height="102"/>' + ribs(56, 60, 13, 102, 4) +
               '<rect class="sh clad" x="331" y="60" width="13" height="44"/>' + ribs(331, 60, 13, 44, 2)
        },
        shop: {
          name: 'Shopfront glazing', carries: false, badge: [337, 132],
          whyNot: 'it sits in the wall line, so the frames either side carry that strip of roof',
          svg: panes(331, 104, 13, 58, 3)
        },
        pads: {
          name: 'Pad foundations', carries: true, badge: [76, 173],
          why: 'the pads and holding-down bolts take each column foot into the ground',
          svg: '<rect class="sh conc" x="58" y="162" width="36" height="17"/>' +
               '<rect class="sh conc" x="306" y="162" width="36" height="17"/>'
        }
      },
      path: arrow(182, 34, 112, 55) + arrow(218, 34, 288, 55) +
            arrow(76, 74, 76, 154) + arrow(324, 74, 324, 154) +
            arrow(76, 182, 76, 194) + arrow(324, 182, 324, 194)
    }
  };

  /* Rounds alternate building and question so nothing repeats back to back.
     "carry" wants the load path; "open" wants what can be taken out. */
  var ROUNDS = [
    {
      id: 'cottage-carry', b: 'cottage', ask: 'carry', opts: ['ext', 'spine', 'stud', 'found'],
      frame: 'A two-storey cottage in brick and block — cellular construction. Select every part that carries load down into the ground.',
      teach: 'In cellular construction the walls are the structure: roof and floor loads run down the masonry into strip footings under every load-bearing wall.'
    },
    {
      id: 'office-open', b: 'office', ask: 'open', opts: ['infill', 'glaze', 'cols', 'wallp'],
      frame: 'A tenant wants one open-plan floor in this steel-framed office. Select every part that could be taken out without propping the structure.',
      teach: 'The frame already carries everything, so the skin between columns is free. That is why frames give open-plan floors and full-height glass.'
    },
    {
      id: 'portal-carry', b: 'portal', ask: 'carry', opts: ['rafter', 'pcol', 'clad', 'pads'],
      frame: 'A car showroom built as a steel portal frame, clear across the full span. Select every part that carries load down into the ground.',
      teach: 'A portal frame is a rigid hoop of column and rafter: load runs down the rafters, turns the corner at the haunch and goes down the columns into pads.'
    },
    {
      id: 'cottage-open', b: 'cottage', ask: 'open', opts: ['spine', 'stud', 'ext', 'joists'],
      frame: 'The owners want to knock through, upstairs and down, in this cottage. Select every part that could be taken out without propping the structure.',
      teach: 'Only the stud partition is dead weight. Opening the spine wall needs props and a steel beam (an RSJ) on piers, because the floor lands on it.'
    },
    {
      id: 'office-carry', b: 'office', ask: 'carry', opts: ['cols', 'beams', 'infill', 'pads'],
      frame: 'A three-storey office built as a rectangular steel frame. Select every part that carries load down into the ground.',
      teach: 'A rectangular frame gathers everything onto beams and columns, then onto pad foundations. The walls between are infill: they hold up only themselves.'
    },
    {
      id: 'portal-open', b: 'portal', ask: 'open', opts: ['clad', 'purlin', 'pcol', 'shop'],
      frame: 'This showroom wants a wider window and a doorway in the side wall. Select every part that could be taken out without propping the structure.',
      teach: 'Cladding and shopfront glazing only keep the weather out, so the side wall can open up. Purlins are structure — they carry the sheeting to the rafters.'
    }
  ];

  var LETTERS = ['A', 'B', 'C', 'D'];

  /* ----------------------------------------------------------------- css */

  var CSS = [
    '.svw-ssb{font:400 .88rem/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;display:flex;flex-direction:column;gap:.68rem}',
    '.svw-ssb *{box-sizing:border-box}',
    '.svw-ssb [hidden]{display:none!important}',
    '.svw-ssb .kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--acc)}',
    '.svw-ssb .ttl{margin:.12rem 0 .3rem;font:600 1.2rem/1.22 "Source Serif 4",Georgia,serif;color:#2d2a26}',
    '.svw-ssb .frame{margin:0;font-size:.86rem;line-height:1.45;color:#413d37}',
    '.svw-ssb .run{margin:.3rem 0 0;min-height:1.1em;font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-ssb .body{display:grid;gap:.7rem;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));align-items:start}',
    '.svw-ssb .stage{width:100%;max-width:344px;margin:0 auto;aspect-ratio:400/200;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;overflow:hidden}',
    '.svw-ssb .stage svg{display:block;width:100%;height:100%}',
    '.svw-ssb .side{display:flex;flex-direction:column;gap:.5rem}',
    '.svw-ssb .opts{display:grid;gap:.4rem;grid-template-columns:repeat(auto-fit,minmax(148px,1fr))}',
    '.svw-ssb .opt{display:flex;align-items:center;gap:.4rem;text-align:left;font:600 .8rem/1.25 inherit;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .5rem;cursor:pointer}',
    '.svw-ssb .opt .ky{flex:0 0 auto;width:17px;height:17px;border-radius:50%;background:#fff;border:1px solid #d9d2c6;font-size:.68rem;font-weight:700;display:flex;align-items:center;justify-content:center;color:#5b564e}',
    '.svw-ssb .opt .nm{flex:1 1 auto}',
    '.svw-ssb .opt .mk{flex:0 0 auto;font-size:.82rem;font-weight:700;color:#8d8880}',
    '.svw-ssb .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ssb .opt[aria-pressed="true"] .ky{background:#fff;color:#2d2a26;border-color:#fff}',
    '.svw-ssb .opt.ok{background:#f2f6f3;border-color:#4f7d63;color:#2d2a26}',
    '.svw-ssb .opt.ok .ky{background:#4f7d63;color:#fff;border-color:#4f7d63}',
    '.svw-ssb .opt.ok .mk{color:#4f7d63}',
    '.svw-ssb .opt.no{background:#faf8f5;border-color:#c9c2b6;color:#5b564e}',
    '.svw-ssb .opt.miss{background:#faf8f5;border:1px dashed var(--acc);color:#2d2a26}',
    '.svw-ssb .opt.miss .mk{color:var(--acc);font-size:.7rem;font-weight:600}',
    '.svw-ssb .opt:disabled{cursor:default}',
    '.svw-ssb .cmd{display:flex;gap:.5rem;align-items:center}',
    '.svw-ssb .go{flex:1 1 auto;font:600 .82rem/1 inherit;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.55rem .95rem;cursor:pointer}',
    '.svw-ssb .go[disabled]{background:#efeae2;border-color:#e0d9cd;color:#a49e94;cursor:default}',
    '.svw-ssb .nxt{flex:1 1 auto;font:600 .82rem/1 inherit;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.55rem .95rem;cursor:pointer}',
    '.svw-ssb .cap{margin:0;font-size:.84rem;line-height:1.5;color:#413d37;min-height:3.4em}',
    '.svw-ssb .cap b{color:#2d2a26}',
    '.svw-ssb .cap.win b{color:#4f7d63}',
    '.svw-ssb .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    /* drawing */
    '.svw-ssb .soil{fill:#eae2d3}',
    '.svw-ssb .gl{stroke:#8f8271;stroke-width:1.8}',
    '.svw-ssb .hatch{stroke:#bcb09a;stroke-width:1}',
    '.svw-ssb .hair{stroke:#8f8271;stroke-width:1.2}',
    '.svw-ssb .rib,.svw-ssb .crs{stroke:#9c8f7b;stroke-width:.7;opacity:.85}',
    '.svw-ssb .roofp{fill:#ded5c4;stroke:#8f8271;stroke-width:1.6;stroke-linejoin:round}',
    '.svw-ssb .slab{fill:#cec5b4;stroke:none}',
    '.svw-ssb .sheet{fill:none;stroke:#a89d8a;stroke-width:2.4}',
    '.svw-ssb .brick{fill:#ded4c2;stroke:#8a7c69;stroke-width:1.3}',
    '.svw-ssb .timber{fill:#ece0c8;stroke:#a38c60;stroke-width:1.3}',
    '.svw-ssb .conc{fill:#cfc8ba;stroke:#867e70;stroke-width:1.3}',
    '.svw-ssb .block{fill:#dbd5c9;stroke:#8a7c69;stroke-width:1.3}',
    '.svw-ssb .glass{fill:#d5e0e1;stroke:#8b9c9d;stroke-width:1.2}',
    '.svw-ssb .clad{fill:#e4dfd4;stroke:#9a9284;stroke-width:1.2}',
    '.svw-ssb .steel{fill:#514b43;stroke:#332f2a;stroke-width:1}',
    '.svw-ssb .steelline{fill:none;stroke:#514b43;stroke-width:8;stroke-linejoin:round;stroke-linecap:round}',
    '.svw-ssb .p.on .sh{fill:var(--tint);stroke:var(--acc);stroke-width:2}',
    '.svw-ssb .p.on .steelline{fill:none;stroke:var(--acc)}',
    '.svw-ssb .p.off{opacity:.42}',
    '.svw-ssb .halo{stroke:#faf8f5;stroke-width:4.6;stroke-linecap:round;opacity:.9}',
    '.svw-ssb .ld{stroke:var(--acc);stroke-width:2.1;stroke-linecap:round}',
    '.svw-ssb .ldh{fill:var(--acc);stroke:#faf8f5;stroke-width:.7}',
    '.svw-ssb .bdg circle{fill:#fff;stroke:#2d2a26;stroke-width:1.3}',
    '.svw-ssb .bdg text{fill:#2d2a26;font:700 11px Inter,system-ui,sans-serif;text-anchor:middle}',
    '.svw-ssb .bdg.on circle{fill:#2d2a26}',
    '.svw-ssb .bdg.on text{fill:#fff}',
    '.svw-ssb .bdg.hold circle{fill:var(--acc);stroke:var(--acc)}',
    '.svw-ssb .bdg.hold text{fill:#fff}',
    '.svw-ssb:not(.nomo) .opt,.svw-ssb:not(.nomo) .go{transition:background .14s ease,border-color .14s ease,color .14s ease}'
  ].join('');

  /* --------------------------------------------------------------- mount */

  function mount(root, ctx) {
    ctx = ctx || {};
    var acc = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
    var tint = /^#[0-9a-f]{6}$/i.test(acc) ? acc + '2e' : 'rgba(45,42,38,.12)';

    root.innerHTML = '';
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var w = document.createElement('div');
    w.className = 'svw-ssb' + (ctx.reducedMotion ? ' nomo' : '');
    w.style.setProperty('--acc', acc);
    w.style.setProperty('--tint', tint);
    w.innerHTML =
      '<div class="hd">' +
        '<p class="kick">Load path</p>' +
        '<h3 class="ttl">Which parts are holding it up?</h3>' +
        '<p class="frame"></p>' +
        '<p class="run"></p>' +
      '</div>' +
      '<div class="body">' +
        '<div class="stage"><svg viewBox="0 0 400 200" role="img" aria-label=""></svg></div>' +
        '<div class="side">' +
          '<div class="opts"></div>' +
          '<div class="cmd">' +
            '<button type="button" class="go" disabled>Check the load path</button>' +
            '<button type="button" class="nxt" hidden>Next building</button>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<p class="cap">Every part of a building has weight, and all of it has to reach the soil. The question is which route it takes.</p>' +
      '<p class="sr" aria-live="polite"></p>';
    root.appendChild(w);

    var el = {
      frame: w.querySelector('.frame'), run: w.querySelector('.run'),
      svg: w.querySelector('svg'), opts: w.querySelector('.opts'),
      go: w.querySelector('.go'), nxt: w.querySelector('.nxt'),
      cap: w.querySelector('.cap'), sr: w.querySelector('.sr')
    };

    /* four option buttons, built once and re-labelled each round */
    var btns = [];
    for (var i = 0; i < 4; i++) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'opt';
      b.setAttribute('aria-pressed', 'false');
      b.innerHTML = '<span class="ky"></span><span class="nm"></span><span class="mk"></span>';
      b.addEventListener('click', onPick);
      el.opts.appendChild(b);
      btns.push(b);
    }
    el.go.addEventListener('click', commit);
    el.nxt.addEventListener('click', function () { next(); });

    var S = {
      i: Math.floor(Math.random() * ROUNDS.length),
      r: null, b: null, picked: [], done: false,
      streak: 0, mastered: false, attempted: 0, correct: null
    };

    function publish() {
      root.dataset.svState = JSON.stringify({
        round: S.r ? S.r.id : null,
        ask: S.r ? S.r.ask : null,
        picked: S.picked.filter(Boolean).length,
        correct: S.correct,
        streak: S.streak,
        mastered: S.mastered,
        attempted: S.attempted
      });
    }

    function answerOf(k) {
      var p = S.b.parts[k];
      return S.r.ask === 'carry' ? p.carries : !p.carries;
    }

    function drawStage() {
      var s = S.b.scenery;
      var keys = Object.keys(S.b.parts), k, j;
      for (j = 0; j < keys.length; j++) {
        k = keys[j];
        s += '<g class="p" data-p="' + k + '">' + S.b.parts[k].svg + '</g>';
      }
      if (S.done) s += '<g class="lp">' + S.b.path + '</g>';
      for (j = 0; j < S.r.opts.length; j++) {
        k = S.r.opts[j];
        var bd = S.b.parts[k].badge;
        s += '<g class="bdg" data-g="' + k + '"><circle cx="' + bd[0] + '" cy="' + bd[1] + '" r="9.5"/>' +
             '<text x="' + bd[0] + '" y="' + (bd[1] + 4) + '">' + LETTERS[j] + '</text></g>';
      }
      el.svg.innerHTML = s;
      el.svg.setAttribute('aria-label', S.b.alt);
      syncStage();
    }

    function syncStage() {
      var j, k, g;
      for (j = 0; j < S.r.opts.length; j++) {
        k = S.r.opts[j];
        g = el.svg.querySelector('[data-p="' + k + '"]');
        if (g) g.classList.toggle('on', !!S.picked[j] && !S.done);
        var bg = el.svg.querySelector('[data-g="' + k + '"]');
        if (bg) {
          bg.classList.toggle('on', !!S.picked[j] && !S.done);
          bg.classList.toggle('hold', S.done && S.b.parts[k].carries);
        }
      }
      if (S.done) {
        var all = el.svg.querySelectorAll('.p');
        for (j = 0; j < all.length; j++) {
          var pk = all[j].getAttribute('data-p');
          all[j].classList.toggle('off', !S.b.parts[pk].carries);
        }
      }
    }

    function loadRound() {
      S.r = ROUNDS[S.i];
      S.b = BUILDINGS[S.r.b];
      S.picked = [false, false, false, false];
      S.done = false;
      S.correct = null;
      el.frame.textContent = S.r.frame;
      for (var j = 0; j < 4; j++) {
        var b = btns[j], k = S.r.opts[j];
        b.className = 'opt';
        b.disabled = false;
        b.setAttribute('aria-pressed', 'false');
        b.querySelector('.ky').textContent = LETTERS[j];
        b.querySelector('.nm').textContent = S.b.parts[k].name;
        b.querySelector('.mk').textContent = '';
      }
      el.go.hidden = false;
      el.go.disabled = true;
      el.nxt.hidden = true;
      el.cap.className = 'cap';
      drawStage();
      runLine();
      publish();
    }

    function runLine() {
      if (S.mastered) { el.run.textContent = 'You have it — keep going if you want another.'; return; }
      if (S.streak === 1) { el.run.textContent = '1 right in a row — two more and you have it.'; return; }
      if (S.streak === 2) { el.run.textContent = '2 right in a row — one more and you have it.'; return; }
      el.run.textContent = S.attempted ? 'Run at nought — three in a row ends it.' : '';
    }

    function onPick(e) {
      if (S.done) return;
      var b = e.currentTarget, j = btns.indexOf(b);
      S.picked[j] = !S.picked[j];
      b.setAttribute('aria-pressed', S.picked[j] ? 'true' : 'false');
      syncStage();
      el.go.disabled = !S.picked.some(Boolean);
      publish();
    }

    function names(list) {
      if (!list.length) return 'nothing';
      if (list.length === 1) return list[0];
      return list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1];
    }
    function lower(n) { return n.charAt(0).toLowerCase() + n.slice(1); }

    function commit() {
      if (S.done) return;
      var hadFocus = document.activeElement === el.go;
      var chosen = [], wrongIn = [], missed = [], j, k, p;
      for (j = 0; j < 4; j++) {
        k = S.r.opts[j]; p = S.b.parts[k];
        if (S.picked[j]) chosen.push(k);
        if (S.picked[j] && !answerOf(k)) wrongIn.push(k);
        if (!S.picked[j] && answerOf(k)) missed.push(k);
      }
      var right = !wrongIn.length && !missed.length;
      S.done = true;
      S.attempted++;
      S.correct = right;
      if (right) { S.streak++; if (S.streak >= 3) S.mastered = true; }
      else S.streak = 0;

      for (j = 0; j < 4; j++) {
        k = S.r.opts[j];
        btns[j].disabled = true;
        btns[j].setAttribute('aria-pressed', 'false');
        if (S.picked[j] && answerOf(k)) { btns[j].className = 'opt ok'; btns[j].querySelector('.mk').textContent = '✓'; }
        else if (S.picked[j]) { btns[j].className = 'opt no'; btns[j].querySelector('.mk').textContent = '✕'; }
        else if (answerOf(k)) { btns[j].className = 'opt miss'; btns[j].querySelector('.mk').textContent = 'missed'; }
        else { btns[j].className = 'opt'; }
      }

      el.cap.innerHTML = feedback(chosen, wrongIn, missed, right);
      el.cap.className = 'cap' + (right ? ' win' : '');
      el.go.hidden = true;
      el.nxt.hidden = false;
      el.nxt.textContent = S.mastered ? 'Another anyway' : 'Next building';
      drawStage();
      runLine();
      if (S.mastered) {
        el.run.textContent = 'You have it — another if you want one.';
      }
      el.sr.textContent = (right ? 'Correct. ' : 'Not quite. ') + el.cap.textContent;
      if (hadFocus) el.nxt.focus();
      publish();
    }

    function nm(k) { return S.b.parts[k].name; }

    function feedback(chosen, wrongIn, missed, right) {
      var pickedNames = chosen.map(nm), lead, body;
      if (right) {
        lead = '<b>Right —</b> you picked ' + names(pickedNames) + '. ';
        if (S.mastered) {
          return lead + '<b>Three in a row.</b> You can read a load path now: in a cellular building it runs down the walls themselves; in a frame it runs down columns and beams, which is why the walls between them can open up.';
        }
        return lead + S.r.teach;
      }
      lead = '<b>Not quite —</b> you picked ' + names(pickedNames) + '. ';
      if (S.r.ask === 'open') {
        if (wrongIn.length) {
          body = 'Take out the ' + lower(nm(wrongIn[0])) + ' and nothing holds what sits above it: ' +
                 S.b.parts[wrongIn[0]].why + '.';
        } else {
          body = 'You left the ' + names(missed.map(nm).map(lower)) + ' in, but ' +
                 S.b.parts[missed[0]].whyNot + '.';
        }
      } else {
        if (wrongIn.length) {
          body = 'the ' + lower(nm(wrongIn[0])) + ' carries nothing but itself — ' +
                 S.b.parts[wrongIn[0]].whyNot + '.';
        } else {
          body = 'You left out the ' + names(missed.map(nm).map(lower)) + ': ' +
                 S.b.parts[missed[0]].why + '.';
        }
      }
      return lead + body.charAt(0).toUpperCase() + body.slice(1);
    }

    function next() {
      S.i = (S.i + 1) % ROUNDS.length;
      loadRound();
      btns[0].focus();
    }

    loadRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Trace the load path',
      teaches: 'Load-bearing (cellular) walls carry the building down through the walls themselves, while a frame carries it on columns and beams and leaves the walls between as infill that can be opened up.'
    },
    mount: mount
  };
})();
