/* Kenilworth Castle: reading the plan
   One plan, one prediction per round: why does this feature stand where it
   stands? Commit first, then the plan shows the relationship that answers it.
   Self-contained: no imports, no network, every selector scoped to .svw-kenil. */
(function () {
  'use strict';

  var CSS = [
'.svw-kenil{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
'.svw-kenil *{box-sizing:border-box}',
'.svw-kenil p{margin:0}',
'.svw-kenil .k-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--k-acc);margin:0 0 .2rem}',
'.svw-kenil .k-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.18;margin:0 0 .32rem}',
'.svw-kenil .k-frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .5rem}',
'.svw-kenil .k-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.3rem;margin:0 auto .55rem;max-width:380px}',
'.svw-kenil .k-plan{display:block;width:100%;height:auto}',
'.svw-kenil .k-slot{min-height:178px}',
'.svw-kenil .k-q{font-size:.85rem;font-weight:600;line-height:1.38;margin:0 0 .45rem}',
'.svw-kenil .k-opts{display:flex;flex-direction:column;gap:.34rem}',
'.svw-kenil .k-opt{display:block;width:100%;text-align:left;font:inherit;font-size:.82rem;line-height:1.35;font-weight:500;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .6rem;cursor:pointer}',
'.svw-kenil .k-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-kenil .k-opt[disabled]{cursor:default;opacity:.55}',
'.svw-kenil .k-fb{display:none}',
'.svw-kenil .k-fb.on{display:block}',
'.svw-kenil .k-flag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 .25rem}',
'.svw-kenil .k-flag.ok{color:#4f7d63}',
'.svw-kenil .k-flag.no{color:#5b564e}',
'.svw-kenil .k-say{font-size:.84rem;line-height:1.46;margin:0 0 .32rem}',
'.svw-kenil .k-note{font-size:.75rem;line-height:1.45;color:#8d8880;margin:0}',
'.svw-kenil .k-act{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin-top:.55rem}',
'.svw-kenil .k-run{font-size:.76rem;line-height:1.35;color:#5b564e;font-variant-numeric:tabular-nums}',
'.svw-kenil .k-go{flex:0 0 auto;font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
'.svw-kenil .k-go[disabled]{background:#faf8f5;color:#a9a39a;border-color:#ddd7cd;cursor:default}',
'.svw-kenil .k-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
'.svw-kenil .k-water{fill:#dbe3e6;stroke:#b6c3c9;stroke-width:1}',
'.svw-kenil .k-rock{fill:#f0e7d7;stroke:#cdbfa3;stroke-width:1}',
'.svw-kenil .k-wall{fill:none;stroke:#2d2a26;stroke-width:1.6}',
'.svw-kenil .k-court{fill:#faf8f5;stroke:#8d8880;stroke-width:1}',
'.svw-kenil .k-bldg{fill:#fff;stroke:#2d2a26;stroke-width:1.1}',
'.svw-kenil .k-garden{fill:#eaeee0;stroke:#2d2a26;stroke-width:1.1}',
'.svw-kenil .k-dam{fill:#e4dccd;stroke:#2d2a26;stroke-width:1.1}',
'.svw-kenil .k-cway{fill:none;stroke:#5b564e;stroke-width:1.1;stroke-dasharray:4 3}',
'.svw-kenil .k-lab{font-family:Inter,system-ui,sans-serif;font-size:10px;fill:#2d2a26}',
'.svw-kenil .k-lab.m{fill:#5b564e}',
'.svw-kenil .k-lead{stroke:#8d8880;stroke-width:.8;fill:none}',
'.svw-kenil .k-hi{stroke:var(--k-acc);stroke-width:2.4}',
'.svw-kenil .k-fill{fill:var(--k-acc);fill-opacity:.2}',
'.svw-kenil .k-rel{display:none}',
'.svw-kenil .k-rel.on{display:block}',
'.svw-kenil .k-relline{fill:none;stroke:var(--k-acc);stroke-width:1.6;stroke-dasharray:5 3}',
'.svw-kenil .k-arrow{fill:var(--k-acc)}',
'.svw-kenil .k-tag{font-family:Inter,system-ui,sans-serif;font-size:10px;font-weight:600;fill:#2d2a26;paint-order:stroke;stroke:#faf8f5;stroke-width:2.6;stroke-linejoin:round}'
  ].join('\n');

  /* ---- the plan -------------------------------------------------------- */
  var PLAN = [
'<svg class="k-plan" viewBox="0 0 320 148" role="img" aria-label="Plan of Kenilworth Castle: the great mere to the west, the dam and causeway along the south, and the walled outcrop holding the keep, great hall, Leicester’s Building, garden and gatehouse.">',
  '<defs><marker id="kmA" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">',
  '<path class="k-arrow" d="M0,0 L8,4 L0,8 z"/></marker></defs>',
  '<g class="k-lead"><path d="M13,16 L13,5 M10,9 L13,5 L16,9"/></g>',
  '<text class="k-lab m" x="13" y="26" text-anchor="middle">N</text>',
  '<path id="k-mere" class="k-water" d="M148,28 C116,16 60,18 36,32 C12,44 10,74 28,88 L148,90 Z"/>',
  '<polygon id="k-dam" class="k-dam" points="24,86 214,92 214,106 24,100"/>',
  '<path id="k-cway" class="k-cway" d="M18,93 L212,99"/>',
  '<rect id="k-rock" class="k-rock" x="150" y="14" width="142" height="80" rx="13"/>',
  '<rect id="k-wall" class="k-wall" x="150" y="14" width="142" height="80" rx="13"/>',
  '<rect class="k-bldg" x="206" y="89" width="16" height="9"/>',
  '<rect id="k-garden" class="k-garden" x="230" y="18" width="54" height="14" rx="2"/>',
  '<rect class="k-court" x="176" y="34" width="106" height="52" rx="2"/>',
  '<rect id="k-keep" class="k-bldg" x="238" y="38" width="38" height="20"/>',
  '<rect id="k-hall" class="k-bldg" x="180" y="38" width="34" height="44"/>',
  '<rect id="k-leic" class="k-bldg" x="238" y="64" width="38" height="18"/>',
  '<rect id="k-gate" class="k-bldg" x="254" y="4" width="28" height="12" rx="2"/>',
  '<text class="k-lab" x="78" y="84" text-anchor="middle">The great mere</text>',
  '<text class="k-lab m" x="26" y="115" text-anchor="start">Dam · tiltyard · causeway</text>',
  '<text class="k-lab" x="257" y="52" text-anchor="middle">Keep</text>',
  '<text class="k-lab" x="197" y="56" text-anchor="middle">Great</text>',
  '<text class="k-lab" x="197" y="67" text-anchor="middle">hall</text>',
  '<text class="k-lab" x="257" y="29" text-anchor="middle">Garden</text>',
  '<text class="k-lab" x="248" y="12" text-anchor="end">Gatehouse</text>',
  '<path class="k-lead" d="M257,82 L257,103"/>',
  '<text class="k-lab" x="257" y="116" text-anchor="middle">Leicester’s</text>',
  '<text class="k-lab" x="257" y="128" text-anchor="middle">Building</text>',
  '<g id="rel-dam" class="k-rel">',
    '<path class="k-relline" d="M18,93 L204,99" marker-end="url(#kmA)"/>',
    '<path class="k-relline" d="M96,76 L96,62" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="96" y="52" text-anchor="middle">water held back</text>',
    '<text class="k-tag" x="112" y="132" text-anchor="middle">the only way in</text>',
  '</g>',
  '<g id="rel-mere" class="k-rel">',
    '<path class="k-relline" d="M18,93 L204,99" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="80" y="52" text-anchor="middle">no attack this side</text>',
    '<text class="k-tag" x="112" y="132" text-anchor="middle">one narrow crossing</text>',
  '</g>',
  '<g id="rel-hall" class="k-rel">',
    '<path class="k-relline" d="M176,60 L124,60" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="84" y="52" text-anchor="middle">safe side, so windows</text>',
  '</g>',
  '<g id="rel-leic" class="k-rel">',
    '<path class="k-relline" d="M178,106 L242,86" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="100" y="132" text-anchor="middle">first thing you see</text>',
  '</g>',
  '<g id="rel-garden" class="k-rel">',
    '<path class="k-relline" d="M252,50 L252,34" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="84" y="44" text-anchor="middle">looked down on</text>',
    '<text class="k-tag" x="84" y="57" text-anchor="middle">from the keep</text>',
  '</g>',
  '<g id="rel-keep" class="k-rel">',
    '<text class="k-tag" x="82" y="44" text-anchor="middle">keep first, 1120s</text>',
    '<text class="k-tag" x="82" y="57" text-anchor="middle">wall round it, 1210s</text>',
  '</g>',
  '<g id="rel-gate" class="k-rel">',
    '<path class="k-relline" d="M316,2 L290,8" marker-end="url(#kmA)"/>',
    '<text class="k-tag" x="84" y="52" text-anchor="middle">new door, north road</text>',
  '</g>',
  '<g id="rel-arc" class="k-rel">',
    '<text class="k-tag" x="84" y="44" text-anchor="middle">1210s: stop an army</text>',
    '<text class="k-tag" x="84" y="57" text-anchor="middle">1570s: impress a guest</text>',
  '</g>',
'</svg>'
  ].join('');

  /* ---- the rounds ------------------------------------------------------ */
  var ROUNDS = [
  { id: 'dam', hi: ['k-dam'], rel: 'rel-dam',
    q: 'The dam runs along the castle’s southern side. Why was it built there?',
    opts: [
      { ok: true, t: 'It holds the streams back to fill the mere, and the road in runs along its top.',
        fb: 'the dam does two jobs with one bank of earth: it floods the valley into the mere, and its flat top carries the causeway. The castle chose where every visitor walked.' },
      { t: 'It drains water away from the walls so the outer bailey stays dry.',
        fb: 'you said the dam drains water away. It does the opposite: it traps the brooks and floods the valley to make the mere. Here the water is the defence, not the problem.' },
      { t: 'It follows the easiest ground, and the road just ended up on top of it.',
        fb: 'you said the ground decided it. The dam had to cross the valley to hold water back, and that fixed its line. The road came second, using the one dry ridge across the flooded ground.' }
    ],
    note: 'Historians usually credit the dam and water defences to King John’s works of the 1210s.' },

  { id: 'mere', hi: ['k-mere'], rel: 'rel-mere',
    q: 'The mere flooded about 111 acres of the valley. What did that do to an attacker?',
    opts: [
      { ok: true, t: 'It squeezed any attack onto one narrow causeway, covered by the gate.',
        fb: 'water turns a whole side into a wall nobody can climb. In 1266 the attacks across the water all failed, and after about six months hunger, not storming, beat the garrison.' },
      { t: 'It gave the garrison endless water and fish, so a siege could not starve them.',
        fb: 'you said the mere fed the defenders. It did not save them: in 1266 they held out about six months, then surrendered from hunger and disease. What the mere stopped was the assault.' },
      { t: 'It looked impressive, but the walls did the real defending.',
        fb: 'you said the walls did the work. On the mere side there was hardly anything to attack: in 1266 the water beat every assault, and only hunger ended the siege.' }
    ],
    note: 'The siege of 1266 lasted roughly six months and ended in surrender, not in a successful attack.' },

  { id: 'hall', hi: ['k-hall'], rel: 'rel-hall',
    q: 'Gaunt’s great hall of the 1370s fills the west range, windows facing the mere. Why that side?',
    opts: [
      { ok: true, t: 'The mere already defended that side, so the wall could be opened up with glass.',
        fb: 'one phase pays for the next. The water made the west side unattackable, so 150 years later Gaunt could cut tall windows into it. Defence first, then display on top of it.' },
      { t: 'The west wall was the oldest, thickest stone, so it could carry the roof.',
        fb: 'you said the old stone carried it. Gaunt’s hall is new work, on its own vaulted undercroft. What the west side offered was safety: the mere covered it, so the wall could hold windows.' },
      { t: 'It was the last stretch of courtyard still empty.',
        fb: 'you said it filled the space left over. The west range gave Gaunt the one side no attacker could reach, plus a view over the water. He built where the mere had already done the defending.' }
    ],
    note: 'Phase order: keep 1120s, John’s wall and dam 1210s, Gaunt’s hall 1370s–80s, Leicester’s works 1560s–70s.' },

  { id: 'leic', hi: ['k-leic'], rel: 'rel-leic',
    q: 'Leicester’s new apartments for the queen fill the court’s south-east corner. Why there?',
    opts: [
      { ok: true, t: 'They rise straight above the causeway, so an arriving guest sees them first.',
        fb: 'the building is aimed at the visitor. Cross the dam and a tall new block of glass and brick fills the skyline above the old wall. Leicester was spending to be seen.' },
      { t: 'They sit behind the keep, giving the queen quiet rooms away from the gate.',
        fb: 'you said privacy. Leicester’s block is the loudest thing on the plan: storey after storey of window, facing the way visitors came in. Quiet rooms would have gone deeper into the court.' },
      { t: 'It was the one corner of the court still free.',
        fb: 'you said it was the last free corner. The corner is the point: it looks straight down the causeway. A block that size went where it would be seen.' }
    ],
    note: 'Elizabeth I stayed nineteen days at Kenilworth in July 1575; Leicester’s works were built for visits like it.' },

  { id: 'garden', hi: ['k-garden'], rel: 'rel-garden',
    q: 'Leicester’s garden was laid out on the strip north of the keep. Why that patch of ground?',
    opts: [
      { ok: true, t: 'It lies under the keep’s windows, so it could be looked down on from indoors.',
        fb: 'the garden is made to be seen from above. Dudley put large new windows into the old keep wall facing it, so the best view of the garden came from the rooms inside.' },
      { t: 'It was the only flat, sheltered ground outside the castle walls.',
        fb: 'you said outside the walls. The garden sits inside King John’s outer wall, sheltered by the keep. That is the point: enclosed, private, and under the windows Dudley had just enlarged.' },
      { t: 'Gardens went wherever there was spare ground.',
        fb: 'you said spare ground. This patch was chosen: it is what the keep’s new windows look down onto. A garden built for a royal guest had to be visible from the rooms she was using.' }
    ],
    note: 'The garden is known mainly from Robert Langham’s letter of 1575; the one on the site today is a modern reconstruction.' },

  { id: 'keep', hi: ['k-keep'], rel: 'rel-keep',
    q: 'The keep stands on the highest point, everything else built round it. Which phase is it from?',
    opts: [
      { ok: true, t: 'The Norman castle of the 1120s — the first building, that the rest grew around.',
        fb: 'the keep is the oldest thing here. Read outwards for the order: keep on the high ground in the 1120s, John’s wall and dam round it ninety years later, then Gaunt’s hall, then Leicester’s work.' },
      { t: 'King John’s works of the 1210s — it stands inside the wall he built.',
        fb: 'you said the 1210s because the wall encloses it. Being inside a wall does not date a building: John’s wall went round a keep already about ninety years old. The wall follows the keep.' },
      { t: 'Gaunt’s rebuilding of the 1370s — the grandest block must be the newest.',
        fb: 'you said Gaunt. His work is the great hall on the west range, the one with the big windows. The keep is thick-walled Norman work of the 1120s, built to be held rather than admired.' }
    ],
    note: 'Phase order: keep 1120s, John’s wall and dam 1210s, Gaunt’s hall 1370s–80s, Leicester’s works 1560s–70s.' },

  { id: 'gate', hi: ['k-gate'], rel: 'rel-gate',
    q: 'Leicester’s gatehouse was built on the north side in the 1570s. What was new about that?',
    opts: [
      { ok: true, t: 'It made a grand new front door for guests arriving by road from the north.',
        fb: 'a second and showier way in, on the side the road came from. It looks military, with turrets and battlements, but by the 1570s that was fashion. The old gate by the dam still worked.' },
      { t: 'It replaced the old south gate, which had collapsed.',
        fb: 'you said the old gate had gone. The tower at the causeway end was still standing and still in use. Leicester added an entrance rather than replacing one, on the side his guests rode in from.' },
      { t: 'It was a serious defence, added because attack was still expected.',
        fb: 'you said defence. The battlements and turrets are the costume, not the job: by the 1570s nobody expected to hold Kenilworth against an army. It is a front door dressed as a castle gate.' }
    ],
    note: 'Leicester’s gatehouse still stands almost complete, the easiest of his works to read on the ground.' },

  { id: 'arc', hi: ['k-wall', 'k-dam', 'k-gate', 'k-leic', 'k-garden'], rel: 'rel-arc',
    q: 'Compare King John’s dam and walls with Leicester’s building work. What changed between them?',
    opts: [
      { ok: true, t: 'The shape stayed; the job changed — from stopping an army to impressing a guest.',
        fb: 'Leicester built inside the medieval castle rather than over it. Wall, keep and mere all stayed, and became scenery: the water carried a pageant in 1575 and the old towers framed the approach.' },
      { t: 'The defences were pulled down to make room for the palace.',
        fb: 'you said the defences came down. They stood right through Leicester’s work, and he built among them. The castle was only broken up later, slighted after the Civil War in 1650.' },
      { t: 'Nothing really changed — each owner added rooms wherever there was room.',
        fb: 'you said nothing changed. John’s dam and walls had to stop an army; Leicester’s gatehouse, apartments and garden had to impress one visitor in 1575. Same stones, opposite purpose.' }
    ],
    note: 'The mere was drained after the castle was slighted in 1650, which is why the valley is dry today.' }
  ];

  /* ---- mount ----------------------------------------------------------- */
  /* ctx.reducedMotion needs no branch: the widget has no transition, no
     animation and no timer of any kind, so nothing moves unasked. */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

    var wrap = document.createElement('div');
    wrap.className = 'svw-kenil';
    wrap.style.setProperty('--k-acc', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    wrap.insertAdjacentHTML('beforeend',
      '<p class="k-kick">Historic environment</p>' +
      '<p class="k-title">Kenilworth Castle: reading the plan</p>' +
      '<p class="k-frame">One plan of Kenilworth: the sandstone outcrop, the great mere, and four building ' +
      'phases from the 1120s to the 1570s. Work out why each marked feature stands where it does.</p>' +
      '<div class="k-stage">' + PLAN + '</div>' +
      '<div class="k-slot">' +
        '<p class="k-q" id="kq"></p>' +
        '<div class="k-opts" id="kopts" role="group" aria-labelledby="kq"></div>' +
        '<div class="k-fb" id="kfb">' +
          '<span class="k-flag" id="kflag"></span>' +
          '<p class="k-say" id="ksay"></p>' +
          '<p class="k-note" id="knote"></p>' +
        '</div>' +
      '</div>' +
      '<div class="k-act"><p class="k-run" id="krun"></p>' +
        '<button type="button" class="k-go" id="kgo" disabled>Check</button></div>' +
      '<p class="k-sr" id="ksr" aria-live="polite"></p>');

    root.appendChild(wrap);

    var svg    = wrap.querySelector('.k-plan');
    var elQ    = wrap.querySelector('#kq');
    var elOpts = wrap.querySelector('#kopts');
    var elFb   = wrap.querySelector('#kfb');
    var elFlag = wrap.querySelector('#kflag');
    var elSay  = wrap.querySelector('#ksay');
    var elNote = wrap.querySelector('#knote');
    var elRun  = wrap.querySelector('#krun');
    var elGo   = wrap.querySelector('#kgo');
    var elSr   = wrap.querySelector('#ksr');

    var btns = [], i;
    for (i = 0; i < 3; i++) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'k-opt';
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', onPick);
      elOpts.appendChild(b);
      btns.push(b);
    }

    var state = { streak: 0, mastered: false, attempted: 0 };
    var order = [], cursor = 0, round = null, shown = null, picked = -1, revealed = false;

    function shuffle(a) {
      for (var j = a.length - 1; j > 0; j--) {
        var k = Math.floor(Math.random() * (j + 1)), t = a[j]; a[j] = a[k]; a[k] = t;
      }
      return a;
    }

    function nextRound() {
      if (cursor >= order.length) {
        var last = order.length ? order[order.length - 1] : -1;
        order = shuffle(ROUNDS.map(function (_, n) { return n; }));
        if (order[0] === last && order.length > 1) {
          var t = order[0]; order[0] = order[1]; order[1] = t;
        }
        cursor = 0;
      }
      round = ROUNDS[order[cursor++]];
      shown = shuffle(round.opts.slice());
      picked = -1;
      revealed = false;

      elQ.textContent = round.q;
      for (var m = 0; m < btns.length; m++) {
        btns[m].textContent = shown[m].t;
        btns[m].setAttribute('aria-pressed', 'false');
      }
      elOpts.style.display = '';
      elFb.classList.remove('on');
      elGo.textContent = 'Check';
      elGo.disabled = true;
      clearPlan();
      mark(round.hi, 'k-hi');
      mark(round.hi.filter(noWash), 'k-fill');
      publish();
    }

    function clearPlan() {
      var hi = svg.querySelectorAll('.k-hi, .k-fill');
      for (var a = 0; a < hi.length; a++) hi[a].classList.remove('k-hi', 'k-fill');
      var rel = svg.querySelectorAll('.k-rel.on');
      for (var c = 0; c < rel.length; c++) rel[c].classList.remove('on');
    }

    function noWash(id) { return id !== 'k-wall' && id !== 'k-mere'; }

    function mark(ids, cls) {
      for (var d = 0; d < ids.length; d++) {
        var el = svg.querySelector('#' + ids[d]);
        if (el) el.classList.add(cls);
      }
    }

    function onPick(ev) {
      if (revealed) return;
      var b = ev.currentTarget;
      picked = btns.indexOf(b);
      for (var e = 0; e < btns.length; e++) {
        btns[e].setAttribute('aria-pressed', btns[e] === b ? 'true' : 'false');
      }
      elGo.disabled = false;
      publish();
    }

    function reveal() {
      revealed = true;
      state.attempted++;
      var right = !!shown[picked].ok;
      if (right) {
        state.streak++;
        if (state.streak >= 3) state.mastered = true;
      } else {
        state.streak = 0;
      }

      elFlag.textContent = right ? 'Right' : 'Not quite';
      elFlag.className = 'k-flag ' + (right ? 'ok' : 'no');
      elSay.textContent = '— ' + shown[picked].fb +
        (right && state.streak === 3
          ? ' That is three in a row: every phase here answers the one before it.'
          : '');
      elNote.textContent = round.note;
      elOpts.style.display = 'none';
      elFb.classList.add('on');

      var relEl = svg.querySelector('#' + round.rel);
      if (relEl) relEl.classList.add('on');
      mark(round.hi.filter(noWash), 'k-fill');

      if (state.streak >= 3) {
        elRun.textContent = 'Three in a row — you have it.';
        elGo.textContent = 'Another anyway';
      } else if (right) {
        elRun.textContent = state.streak === 1
          ? '1 right in a row — two more.'
          : '2 right in a row — one more.';
        elGo.textContent = 'Next feature';
      } else {
        elRun.textContent = state.attempted > 1 ? 'Run back to nought.' : '';
        elGo.textContent = 'Next feature';
      }
      elSr.textContent = (right ? 'Right. ' : 'Not quite. ') + elSay.textContent;
      publish();
    }

    elGo.addEventListener('click', function () {
      if (!revealed) {
        if (picked < 0) return;
        reveal();
      } else {
        nextRound();
      }
      elGo.focus();
    });

    wrap.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !revealed && picked >= 0) {
        picked = -1;
        for (var g = 0; g < btns.length; g++) btns[g].setAttribute('aria-pressed', 'false');
        elGo.disabled = true;
        publish();
      }
    });

    function publish() {
      root.dataset.svState = JSON.stringify({
        feature: round ? round.id : null,
        picked: picked,
        revealed: revealed,
        streak: state.streak,
        mastered: state.mastered,
        attempted: state.attempted
      });
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: 'kenilworth-spatial-system',
      title: 'Kenilworth Castle: reading the plan',
      teaches: 'Kenilworth as one spatial system: outcrop, mere and building phases answering each other, defence giving way to display.'
    },
    mount: mount
  };
})();
