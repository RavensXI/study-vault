/* ==========================================================================
   Newton's third law — name the partner force.

   The student is given one force in a scenario and must commit to its third
   law partner in three parts: what TYPE it is, which OBJECT it acts on, and
   which DIRECTION it points. The stage lists the objects in the scenario as
   rows, so "which object does this force act on?" is a physical place on the
   screen rather than an abstraction. On commit, the partner arrow lands in
   the correct object's row and the student's arrow lands in theirs — the gap
   between the two rows is the whole lesson.

   The classic wrong answer (pairing a book's weight with the table's normal
   contact force) is committable in every relevant scenario and carries its
   own diagnosis: same object, different type, so it fails the test twice.
   ========================================================================== */
(function () {
  'use strict';

  /* ---- force types -------------------------------------------------- */
  var TYPES = {
    grav:     { label: 'Gravitational',   phrase: 'a gravitational pull',  noun: 'gravity' },
    normal:   { label: 'Normal contact',  phrase: 'a normal contact force', noun: 'contact' },
    push:     { label: 'Contact push',    phrase: 'a contact push',        noun: 'a push' },
    friction: { label: 'Friction',        phrase: 'a friction force',      noun: 'friction' },
    upthrust: { label: 'Upthrust',        phrase: 'an upthrust',           noun: 'upthrust' },
    magnetic: { label: 'Magnetic',        phrase: 'a magnetic force',      noun: 'magnetism' }
  };

  var UP    = { key: 'up',   label: 'Upwards',   arrow: '↑', phrase: 'upwards' };
  var DOWN  = { key: 'down', label: 'Downwards', arrow: '↓', phrase: 'downwards' };
  var FWD   = { key: 'fwd',  label: 'Forwards',  arrow: '→', phrase: 'forwards' };
  var BACK  = { key: 'back', label: 'Backwards', arrow: '←', phrase: 'backwards' };

  /* ---- the scenario bank -------------------------------------------- */
  var SCENARIOS = [
    {
      id: 'book',
      frame: 'A book lies still on a table. The Earth pulls the book down with a weight of 12 N. Which force is the third law partner of that pull?',
      given: 'The Earth pulls the book down with 12 N — one half of an interaction pair.',
      objects: [
        { key: 'book',  label: 'the book' },
        { key: 'table', label: 'the table' },
        { key: 'earth', label: 'the Earth' }
      ],
      types: ['grav', 'normal', 'friction'],
      dirs: [UP, DOWN],
      namedObj: 'book',
      namedChip: { arrow: '↓', text: 'Earth pulls it down · 12 N' },
      givenDirPhrase: 'downwards',
      answer: { type: 'grav', obj: 'earth', dir: 'up' },
      partnerChip: { arrow: '↑', text: 'Book pulls it up · 12 N' },
      partnerLine: 'the book pulls the Earth up with 12 N',
      rightWhy: 'One force on the book, one on the Earth — different objects, so this pair can never cancel.',
      trap: { type: 'normal', obj: 'book', dir: 'up' },
      trapText: 'It fails the test twice: it acts on the same object as the weight, and it is a different type. Weight pairs with weight — the book pulls the Earth up with 12 N.'
    },
    {
      id: 'swimmer',
      frame: 'A swimmer pushes backwards on the water with her hands, with a force of 120 N. Which force is the third law partner of that push?',
      given: 'The swimmer pushes the water backwards with 120 N — one half of an interaction pair.',
      objects: [
        { key: 'swimmer', label: 'the swimmer' },
        { key: 'water',   label: 'the water' },
        { key: 'wall',    label: 'the pool wall' }
      ],
      types: ['push', 'grav', 'upthrust'],
      dirs: [FWD, BACK],
      namedObj: 'water',
      namedChip: { arrow: '←', text: 'Swimmer pushes it back · 120 N' },
      givenDirPhrase: 'backwards',
      answer: { type: 'push', obj: 'swimmer', dir: 'fwd' },
      partnerChip: { arrow: '→', text: 'Water pushes her on · 120 N' },
      partnerLine: 'the water pushes her forwards with 120 N',
      rightWhy: 'She moves because that push acts on her, not on the water — the two forces sit on different objects.',
      trap: { type: 'push', obj: 'water', dir: 'fwd' },
      trapText: 'Both forces would then act on the water, and there they really would cancel. A pair puts one force on each object: the water pushes the swimmer forwards with 120 N.'
    },
    {
      id: 'rocket',
      frame: 'A rocket engine pushes the exhaust gas downwards with a force of 30 kN. Which force is the third law partner of that push?',
      given: 'The rocket pushes the exhaust gas down with 30 kN — one half of an interaction pair.',
      objects: [
        { key: 'rocket', label: 'the rocket' },
        { key: 'gas',    label: 'the exhaust gas' },
        { key: 'earth',  label: 'the Earth' }
      ],
      types: ['push', 'grav', 'friction'],
      dirs: [UP, DOWN],
      namedObj: 'gas',
      namedChip: { arrow: '↓', text: 'Rocket pushes it down · 30 kN' },
      givenDirPhrase: 'downwards',
      answer: { type: 'push', obj: 'rocket', dir: 'up' },
      partnerChip: { arrow: '↑', text: 'Gas pushes it up · 30 kN' },
      partnerLine: 'the gas pushes the rocket up with 30 kN',
      rightWhy: 'Equal and opposite, but one force acts on the gas and one on the rocket — which is why the rocket can accelerate.',
      trap: { type: 'grav', obj: 'rocket', dir: 'down' },
      trapText: 'That is the rocket’s weight, and its own partner is the rocket pulling the Earth up. A push pairs with a push: the exhaust gas pushes the rocket up with 30 kN.'
    },
    {
      id: 'walk',
      frame: 'As you walk, your shoe pushes backwards on the ground with a friction force of 150 N. Which force is the third law partner of that push?',
      given: 'Your shoe pushes the ground backwards with 150 N — one half of an interaction pair.',
      objects: [
        { key: 'shoe',   label: 'your shoe' },
        { key: 'ground', label: 'the ground' },
        { key: 'air',    label: 'the air' }
      ],
      types: ['friction', 'normal', 'grav'],
      dirs: [FWD, BACK, UP],
      namedObj: 'ground',
      namedChip: { arrow: '←', text: 'Shoe pushes it back · 150 N' },
      givenDirPhrase: 'backwards',
      answer: { type: 'friction', obj: 'shoe', dir: 'fwd' },
      partnerChip: { arrow: '→', text: 'Ground pushes it on · 150 N' },
      partnerLine: 'the ground pushes your shoe forwards with 150 N',
      rightWhy: 'You are driven forwards by the ground, not by your own backward push — that one acts on the ground.',
      trap: { type: 'normal', obj: 'shoe', dir: 'up' },
      trapText: 'The ground does push you up, but that force pairs with your shoe pressing down on the ground. Friction pairs with friction: the ground pushes your shoe forwards with 150 N.'
    },
    {
      id: 'moon',
      frame: 'The Earth pulls the Moon towards it with a gravitational force of 2.0 × 10²⁰ N. Which force is the third law partner of that pull?',
      given: 'The Earth pulls the Moon with 2.0 × 10²⁰ N — one half of an interaction pair.',
      objects: [
        { key: 'moon',  label: 'the Moon' },
        { key: 'earth', label: 'the Earth' },
        { key: 'sun',   label: 'the Sun' }
      ],
      types: ['grav', 'push', 'magnetic'],
      dirs: [
        { key: 'tomoon',  label: 'Towards the Moon',  arrow: '→', phrase: 'towards the Moon' },
        { key: 'toearth', label: 'Towards the Earth', arrow: '←', phrase: 'towards the Earth' }
      ],
      namedObj: 'moon',
      namedChip: { arrow: '←', text: 'Earth pulls it in · 2.0 × 10²⁰ N' },
      givenDirPhrase: 'towards the Earth',
      answer: { type: 'grav', obj: 'earth', dir: 'tomoon' },
      partnerChip: { arrow: '→', text: 'Moon pulls it in · 2.0 × 10²⁰ N' },
      partnerLine: 'the Moon pulls the Earth with the same 2.0 × 10²⁰ N',
      rightWhy: 'Equal in size even though the Earth is about 81 times more massive — a pair is always equal.',
      trap: { type: 'grav', obj: 'moon', dir: 'toearth' },
      trapText: 'That is the force you were given, restated. Its partner acts on the other object: the Moon pulls the Earth towards it with the same 2.0 × 10²⁰ N.'
    }
  ];

  var CSS = [
    '.svw-n3l{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-n3l *{box-sizing:border-box}',
    '.svw-n3l .n3-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--n3a)}',
    '.svw-n3l .n3-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.22;margin:.16rem 0 .3rem}',
    '.svw-n3l .n3-frame{font-size:.86rem;line-height:1.45;margin:0 0 .48rem;color:#3a3630}',
    '.svw-n3l .n3-frame b{font-weight:600;color:#2d2a26}',
    '.svw-n3l .n3-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .55rem}',
    '.svw-n3l .n3-row{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:.5rem;min-height:32px;padding:.08rem 0}',
    '.svw-n3l .n3-row + .n3-row{border-top:1px solid #efe9e0}',
    '.svw-n3l .n3-obj{font-size:.74rem;font-weight:600;color:#5b564e;white-space:nowrap}',
    '.svw-n3l .n3-slot{display:flex;flex-wrap:wrap;gap:.3rem;justify-content:flex-end}',
    '.svw-n3l .n3-chip{display:inline-flex;align-items:center;gap:.32rem;font-size:.72rem;font-weight:600;',
    '  padding:.18rem .45rem;border-radius:8px;border:1px solid #e0d9cd;background:#fff;color:#2d2a26;white-space:nowrap}',
    '.svw-n3l .n3-chip i{font-style:normal;font-size:.86rem;line-height:1}',
    '.svw-n3l .n3-chip--right{border-color:var(--n3a);background:var(--n3tint);color:#2d2a26}',
    '.svw-n3l .n3-chip--yours{border-style:dashed;border-color:#c9c2b6;color:#7a746b;background:transparent}',
    '.svw-n3l .n3-groups{margin:.5rem 0 0}',
    '.svw-n3l .n3-group + .n3-group{margin-top:.42rem}',
    '.svw-n3l .n3-lab{display:flex;align-items:center;gap:.35rem;font-size:.75rem;font-weight:600;color:#5b564e;margin:0 0 .22rem}',
    '.svw-n3l .n3-step{display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;border-radius:50%;',
    '  background:var(--n3tint);color:#5b564e;font-size:.6rem;font-weight:700;flex:0 0 auto}',
    '.svw-n3l .n3-opts{display:flex;flex-wrap:wrap;gap:.3rem}',
    '.svw-n3l .n3-opt{font-family:inherit;font-size:.76rem;font-weight:600;color:#2d2a26;padding:.4rem .7rem;',
    '  border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;cursor:pointer;line-height:1.15}',
    '.svw-n3l .n3-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-n3l .n3-opt:disabled{opacity:.55;cursor:default}',
    '.svw-n3l .n3-go{display:flex;align-items:center;gap:.55rem;margin:.5rem 0 0}',
    '.svw-n3l .n3-btn{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;',
    '  border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-n3l .n3-btn:disabled{background:#faf8f5;border-color:#ddd7cd;color:#a09a90;cursor:default}',
    '.svw-n3l .n3-streak{font-size:.72rem;font-weight:600;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-n3l .n3-streak.n3-done{color:#4f7d63}',
    '.svw-n3l .n3-cap{font-size:.84rem;line-height:1.45;color:#3a3630;margin:.5rem 0 0;padding-top:.45rem;',
    '  border-top:1px solid #efe9e0;min-height:5rem}',
    '.svw-n3l .n3-cap b{font-weight:700}',
    '.svw-n3l .n3-cap b.n3-ok{color:#4f7d63}',
    '.svw-n3l .n3-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-n3l:not(.n3-rm) .n3-opt,.svw-n3l:not(.n3-rm) .n3-btn{transition:background-color .13s ease,color .13s ease,border-color .13s ease}',
    '.svw-n3l.n3-wide .n3-group{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:.6rem}',
    '.svw-n3l.n3-wide .n3-lab{margin:0}',
    '.svw-n3l.n3-wide .n3-group + .n3-group{margin-top:.34rem}'
  ].join('\n');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'newtons-third-law-different-objects',
      title: 'Name the partner force',
      teaches: 'A Newton’s third law pair is the same type, equal in size and opposite in direction, with one force on each of two different objects — which is why a pair never cancels.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      root.textContent = '';

      var accent = '';
      try { accent = (window.getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) {}
      if (!/^#[0-9a-fA-F]{6}$/.test(accent)) accent = /^#[0-9a-fA-F]{6}$/.test(ctx.accent || '') ? ctx.accent : '#8a6a4f';

      var wrap = el('div', 'svw-n3l');
      if (ctx.reducedMotion) wrap.className += ' n3-rm';
      wrap.style.setProperty('--n3a', accent);
      wrap.style.setProperty('--n3tint', accent + '22');
      wrap.appendChild(el('style', null, CSS));

      /* width is known synchronously: root is already in the document */
      function applyWidth() {
        var w = root.clientWidth || 0;
        if (w >= 520) { if (wrap.className.indexOf('n3-wide') < 0) wrap.className += ' n3-wide'; }
        else { wrap.className = wrap.className.replace(/\s*n3-wide/, ''); }
      }

      wrap.appendChild(el('div', 'n3-kick', 'Newton’s third law'));
      wrap.appendChild(el('h3', 'n3-title', 'Name the partner force'));

      var frame = el('p', 'n3-frame');
      wrap.appendChild(frame);

      var stage = el('div', 'n3-stage');
      wrap.appendChild(stage);

      var groups = el('div', 'n3-groups');
      wrap.appendChild(groups);

      var gType = makeGroup('1', 'Type of force');
      var gObj  = makeGroup('2', 'Acts on which object');
      var gDir  = makeGroup('3', 'Direction');
      groups.appendChild(gType.node);
      groups.appendChild(gObj.node);
      groups.appendChild(gDir.node);

      var go = el('div', 'n3-go');
      var btn = el('button', 'n3-btn', 'Check the pair');
      btn.type = 'button';
      var streak = el('span', 'n3-streak', '');
      go.appendChild(btn);
      go.appendChild(streak);
      wrap.appendChild(go);

      var cap = el('p', 'n3-cap');
      wrap.appendChild(cap);

      var sr = el('p', 'n3-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      function makeGroup(step, label) {
        var g = el('div', 'n3-group');
        var lab = el('div', 'n3-lab');
        lab.appendChild(el('span', 'n3-step', step));
        lab.appendChild(el('span', null, label));
        var opts = el('div', 'n3-opts');
        opts.setAttribute('role', 'group');
        opts.setAttribute('aria-label', label);
        g.appendChild(lab);
        g.appendChild(opts);
        return { node: g, opts: opts };
      }

      /* ---- state ---------------------------------------------------- */
      var st = {
        sc: null,
        picked: { type: null, obj: null, dir: null },
        committed: false,
        correct: null,
        streak: 0,
        attempted: 0,
        mastered: false
      };
      var order = [], ptr = 0, last = -1;

      function reshuffle() {
        order = SCENARIOS.map(function (s, i) { return i; });
        for (var i = order.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var t = order[i]; order[i] = order[j]; order[j] = t;
        }
        if (order[0] === last && order.length > 1) {
          var t2 = order[0]; order[0] = order[1]; order[1] = t2;
        }
        ptr = 0;
      }

      function pushState() {
        root.dataset.svState = JSON.stringify({
          scenario: st.sc ? st.sc.id : null,
          picked: st.picked,
          committed: st.committed,
          correct: st.correct,
          streak: st.streak,
          mastered: st.mastered,
          attempted: st.attempted
        });
      }

      /* ---- helpers on the current scenario -------------------------- */
      function objLabel(key) {
        for (var i = 0; i < st.sc.objects.length; i++) {
          if (st.sc.objects[i].key === key) return st.sc.objects[i].label;
        }
        return key;
      }
      function dirBy(key) {
        for (var i = 0; i < st.sc.dirs.length; i++) {
          if (st.sc.dirs[i].key === key) return st.sc.dirs[i];
        }
        return null;
      }

      /* ---- build a round -------------------------------------------- */
      function newRound() {
        if (ptr >= order.length) reshuffle();
        var idx = order[ptr++];
        last = idx;
        st.sc = SCENARIOS[idx];
        st.picked = { type: null, obj: null, dir: null };
        st.committed = false;
        st.correct = null;

        frame.textContent = st.sc.frame;

        /* stage rows: one per object in the scenario */
        stage.textContent = '';
        var slots = {};
        st.sc.objects.forEach(function (o) {
          var row = el('div', 'n3-row');
          row.appendChild(el('span', 'n3-obj', o.label));
          var slot = el('span', 'n3-slot');
          row.appendChild(slot);
          stage.appendChild(row);
          slots[o.key] = slot;
        });
        st.slots = slots;
        addChip(slots[st.sc.namedObj], st.sc.namedChip.arrow, st.sc.namedChip.text, '');

        /* option buttons */
        fill(gType.opts, st.sc.types.map(function (k) {
          return { key: k, label: TYPES[k].label };
        }), 'type');
        fill(gObj.opts, st.sc.objects, 'obj');
        fill(gDir.opts, st.sc.dirs, 'dir');

        btn.textContent = 'Check the pair';
        btn.disabled = true;
        renderCaption();
        renderStreak();
        pushState();
      }

      function addChip(slot, arrow, text, mod) {
        var c = el('span', 'n3-chip' + (mod ? ' ' + mod : ''));
        c.appendChild(el('i', null, arrow));
        c.appendChild(el('span', null, text));
        slot.appendChild(c);
        return c;
      }

      function fill(container, items, dim) {
        container.textContent = '';
        items.forEach(function (it) {
          var b = el('button', 'n3-opt', it.label);
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () { pick(dim, it.key, container); });
          container.appendChild(b);
        });
      }

      function pick(dim, key, container) {
        if (st.committed) return;
        st.picked[dim] = key;
        var kids = container.children;
        var items = dim === 'type' ? st.sc.types
                  : dim === 'obj'  ? st.sc.objects.map(function (o) { return o.key; })
                  : st.sc.dirs.map(function (d) { return d.key; });
        for (var i = 0; i < kids.length; i++) {
          kids[i].setAttribute('aria-pressed', items[i] === key ? 'true' : 'false');
        }
        btn.disabled = !(st.picked.type && st.picked.obj && st.picked.dir);
        renderCaption();
        pushState();
      }

      /* ---- caption --------------------------------------------------- */
      function claimParts() {
        var out = [];
        if (st.picked.type) out.push(TYPES[st.picked.type].phrase);
        if (st.picked.obj) out.push('on ' + objLabel(st.picked.obj));
        if (st.picked.dir) out.push(dirBy(st.picked.dir).phrase);
        return out;
      }

      function renderCaption() {
        cap.textContent = '';
        var parts = claimParts();
        if (!parts.length) { cap.appendChild(document.createTextNode(st.sc.given)); return; }
        cap.appendChild(document.createTextNode('Your claim so far: ' + parts.join(', ') + '.'));
      }

      function renderStreak() {
        if (st.mastered) {
          streak.className = 'n3-streak n3-done';
          streak.textContent = '3 in a row — you have it';
        } else if (st.streak === 2) {
          streak.className = 'n3-streak';
          streak.textContent = '2 in a row — one more';
        } else if (st.streak === 1) {
          streak.className = 'n3-streak';
          streak.textContent = '1 in a row';
        } else {
          streak.className = 'n3-streak';
          streak.textContent = '';
        }
      }

      /* ---- the diagnosis, derived from the committed answer ---------- */
      function echo() {
        return TYPES[st.picked.type].phrase + ' on ' + objLabel(st.picked.obj) +
               ', ' + dirBy(st.picked.dir).phrase;
      }

      function clause() {
        var a = st.sc.answer;
        if (st.picked.obj === st.sc.namedObj) {
          return 'That puts both forces on ' + objLabel(st.sc.namedObj) +
                 '; a pair puts one on each object';
        }
        if (st.picked.obj !== a.obj) {
          return 'The pair is between ' + objLabel(st.sc.namedObj) + ' and ' +
                 objLabel(a.obj) + ', not ' + objLabel(st.picked.obj);
        }
        if (st.picked.type !== a.type) {
          return 'A pair is always the same type — ' + TYPES[a.type].noun +
                 ' pairs with ' + TYPES[a.type].noun;
        }
        return 'A pair points the opposite way, and the given force acts ' +
               st.sc.givenDirPhrase;
      }

      function isTrap() {
        var t = st.sc.trap;
        return st.picked.type === t.type && st.picked.obj === t.obj && st.picked.dir === t.dir;
      }

      function commit() {
        var a = st.sc.answer;
        st.committed = true;
        st.attempted++;
        st.correct = (st.picked.type === a.type && st.picked.obj === a.obj && st.picked.dir === a.dir);
        var justMastered = false;
        if (st.correct) {
          st.streak++;
          if (st.streak >= 3 && !st.mastered) { st.mastered = true; justMastered = true; }
        } else {
          st.streak = 0;
        }

        /* reveal on the stage: the partner lands on the right object */
        addChip(st.slots[a.obj], st.sc.partnerChip.arrow, st.sc.partnerChip.text, 'n3-chip--right');
        if (!st.correct && st.picked.obj !== a.obj) {
          addChip(st.slots[st.picked.obj], dirBy(st.picked.dir).arrow, 'Your answer', 'n3-chip--yours');
        }

        /* lock the choices so the verdict cannot be fiddled towards */
        [gType.opts, gObj.opts, gDir.opts].forEach(function (c) {
          for (var i = 0; i < c.children.length; i++) c.children[i].disabled = true;
        });

        /* the caption */
        cap.textContent = '';
        var mark = el('b', st.correct ? 'n3-ok' : null, st.correct ? 'Right — ' : 'Not quite — ');
        cap.appendChild(mark);
        var body;
        if (st.correct && justMastered) {
          body = 'you said ' + echo() + ': ' + st.sc.partnerLine +
                 '. Three in a row — you have it: same type, equal size, opposite direction, ' +
                 'one force on each object — so a pair never cancels.';
        } else if (st.correct) {
          body = 'you said ' + echo() + ': ' + st.sc.partnerLine + '. ' + st.sc.rightWhy;
        } else if (isTrap()) {
          body = 'you said ' + echo() + '. ' + st.sc.trapText;
        } else {
          body = 'you said ' + echo() + '. ' + clause() + '. The partner: ' +
                 TYPES[a.type].phrase + ' on ' + objLabel(a.obj) + ', ' + dirBy(a.dir).phrase + '.';
        }
        cap.appendChild(document.createTextNode(body));
        sr.textContent = (st.correct ? 'Correct. ' : 'Not correct. ') + body;

        btn.textContent = st.mastered ? 'Another anyway' : 'Next scenario';
        btn.disabled = false;
        renderStreak();
        pushState();
      }

      btn.addEventListener('click', function () {
        if (st.committed) { newRound(); btn.focus(); }
        else if (st.picked.type && st.picked.obj && st.picked.dir) commit();
      });

      /* Escape clears an uncommitted answer */
      wrap.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape' || st.committed) return;
        if (!st.picked.type && !st.picked.obj && !st.picked.dir) return;
        st.picked = { type: null, obj: null, dir: null };
        [gType.opts, gObj.opts, gDir.opts].forEach(function (c) {
          for (var i = 0; i < c.children.length; i++) c.children[i].setAttribute('aria-pressed', 'false');
        });
        btn.disabled = true;
        renderCaption();
        sr.textContent = 'Answer cleared.';
        pushState();
      });

      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(applyWidth);
        ro.observe(root);
      }

      reshuffle();
      applyWidth();
      newRound();
    }
  };
})();
