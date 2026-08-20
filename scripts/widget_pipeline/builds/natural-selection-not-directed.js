/* natural-selection-not-directed
   Variation exists first, by random mutation. The environment only decides
   which of the varieties already present leave more offspring. Individuals
   do not change to order, and a population with no inherited variation for
   a trait does not shift at all.

   The student is shown a real population (12 individuals, visible variation
   or the lack of it) plus whether the trait is inherited, then commits to one
   of four accounts of what happens over the generations. The correct account
   changes from round to round, so it cannot be guessed from the scenario.

   Outcomes are computed from an allele-frequency model, never hand-authored.
*/
(function () {
  'use strict';

  var N = 12;
  var NOTHING = 'No inherited variation to act on — no shift';

  /* --- the scenarios ------------------------------------------------- */
  /* start   : how many of the 12 already carry the favoured variant
     heritable : is the visible difference caused by alleles?
     wOther  : relative chance the OTHER variant survives to breed
     gens    : generations the question asks about                        */

  var SCEN = [
    {
      id: 'moths',
      frame: 'Soot has blackened the tree trunks where these peppered moths rest by day. Predict what happens to the population over 12 generations.',
      fav: 'dark', alt: 'pale',
      fact: 'Wing colour is inherited.',
      start: 1, heritable: true, wOther: 0.72, gens: 12,
      opts: {
        shift: 'Dark wings become common over the generations',
        lifetime: 'Each moth darkens its wings and passes it on',
        need: 'The moths darken because they need camouflage',
        nothing: NOTHING
      },
      fb: {
        shift: 'The dark allele was already there, from a random mutation, before the soot. On sooty bark pale moths are eaten more, so dark moths breed more.',
        lifetime: 'A change an insect makes in its own life is not written into its alleles, so it cannot be passed on. The dark form was already in the population.',
        need: 'Needing camouflage cannot create it. The dark allele was already there by chance; the soot only decided which moths lived long enough to breed.',
        nothing: 'Look again at the population: one moth in twelve already has dark wings, and wing colour is inherited, so selection had something to act on.'
      }
    },
    {
      id: 'bacteria-resistant',
      frame: 'A patient takes an antibiotic, and it reaches this population of bacteria. Predict what happens to the population over 8 generations.',
      fav: 'resistant', alt: 'non-resistant',
      fact: 'Resistance is inherited.',
      start: 1, heritable: true, wOther: 0.05, gens: 8,
      opts: {
        shift: 'Resistance becomes common over the generations',
        lifetime: 'Each bacterium toughens up and passes it on',
        need: 'They become resistant because they need to be',
        nothing: NOTHING
      },
      fb: {
        shift: 'One bacterium already carried the resistance allele, from a random mutation before the drug arrived. The rest are killed, so its descendants take over.',
        lifetime: 'A bacterium cannot toughen itself to order. The resistant one already carried the allele; the antibiotic only removed the rest.',
        need: 'Needing resistance does not create it. The allele arose by chance beforehand, and the drug simply killed every bacterium without it.',
        nothing: 'One bacterium in twelve already carries the resistance allele, and resistance is inherited, so the antibiotic has plenty to select.'
      }
    },
    {
      id: 'rabbits',
      frame: 'The climate where these rabbits live is cooling, winter by winter. Predict what happens to the population over 15 generations.',
      fav: 'thick', alt: 'thin',
      fact: 'Fur thickness is inherited.',
      start: 3, heritable: true, wOther: 0.78, gens: 15,
      opts: {
        shift: 'Thick fur becomes common over the generations',
        lifetime: 'Each rabbit thickens its fur and passes it on',
        need: 'The rabbits grow thicker fur because it is cold',
        nothing: NOTHING
      },
      fb: {
        shift: 'Thicker-furred rabbits were already there, from random mutation. Cold winters kill more thin-furred rabbits, so thick-furred ones leave more young.',
        lifetime: 'A rabbit’s coat may thicken in one winter, but that change is not in its alleles, so its young do not inherit it. The variation was already there.',
        need: 'Cold does not order fur to grow. Some rabbits already had thicker fur by chance, and those were the ones that survived to breed.',
        nothing: 'Three rabbits in twelve already have thicker fur, and fur thickness is inherited, so the cold has something to select.'
      }
    },
    {
      id: 'bacteria-none',
      frame: 'A new antibiotic is used on this population of bacteria. Predict what happens to the population over 8 generations.',
      fav: 'resistant', alt: 'non-resistant',
      fact: 'Resistance is inherited.',
      start: 0, heritable: true, wOther: 0, gens: 8,
      opts: {
        shift: 'Resistance becomes common over the generations',
        lifetime: 'Each bacterium toughens up and passes it on',
        need: 'They become resistant because they need to be',
        nothing: NOTHING
      },
      fb: {
        shift: 'Resistance cannot spread if no bacterium has it. Selection only works on variation that is already present, and here there is none, so all twelve die.',
        lifetime: 'A bacterium cannot toughen itself to order, and not one of these carries a resistance allele, so the antibiotic kills every one.',
        need: 'Needing resistance does not create it. No bacterium here carries the allele, so the whole population is killed.',
        nothing: 'Not one bacterium carries a resistance allele, so the antibiotic has no variation to act on. The population is wiped out, not converted.'
      }
    },
    {
      id: 'deer',
      frame: 'A run of harsh winters begins, and larger deer come through them better. Predict what happens to this herd over 12 generations.',
      fav: 'large', alt: 'small',
      fact: 'Size here comes from food, not alleles.',
      start: 5, heritable: false, wOther: 0.8, gens: 12,
      opts: {
        shift: 'Large size becomes common over the generations',
        lifetime: 'Each deer builds up and its calves are larger',
        need: 'The deer grow larger because winters demand it',
        nothing: NOTHING
      },
      fb: {
        shift: 'Larger deer do come through the winter better, but their size came from the food they found, not from alleles, so nothing extra reaches their calves.',
        lifetime: 'A body built up in one life is not written into the alleles. Every calf starts from its own genes, so the herd does not shift.',
        need: 'Needing a bigger body does not create one, and this size difference is not inherited, so it cannot spread through the herd.',
        nothing: 'The size difference came from how much food each deer found, not from its alleles. Larger deer survive better, but their calves are not born larger.'
      }
    },
    {
      id: 'beetles',
      frame: 'These beetles live on a windswept island, where flying insects are often blown out to sea. Predict what happens over 14 generations.',
      fav: 'short', alt: 'long',
      fact: 'Wing length is inherited.',
      start: 2, heritable: true, wOther: 0.75, gens: 14,
      opts: {
        shift: 'Short wings become common over the generations',
        lifetime: 'Each beetle shortens its wings and passes it on',
        need: 'The beetles’ wings shorten because of the wind',
        nothing: NOTHING
      },
      fb: {
        shift: 'Short-winged beetles were already there by chance. Long-winged ones blow out to sea more often, so short wings spread: not stronger, just better suited.',
        lifetime: 'Wind cannot rewrite a beetle’s alleles, and a wing worn down in one life is not inherited. The short-winged form was already there.',
        need: 'Wind does not order wings to shorten. A few beetles already had short wings by chance, and they were the ones not blown out to sea.',
        nothing: 'Two beetles in twelve already have short wings, and wing length is inherited, so the wind has something to select.'
      }
    },
    {
      id: 'copper-grass',
      frame: 'This grass is spreading onto a heap of copper-mine spoil, where the soil is poisoned. Predict what happens over 10 generations.',
      fav: 'tolerant', alt: 'not tolerant',
      fact: 'Copper tolerance is inherited.',
      start: 1, heritable: true, wOther: 0.35, gens: 10,
      opts: {
        shift: 'Copper tolerance spreads through the population',
        lifetime: 'Each plant hardens to copper and passes it on',
        need: 'The grass becomes tolerant because it must be',
        nothing: NOTHING
      },
      fb: {
        shift: 'A few plants already carried alleles for copper tolerance. The rest die in the poisoned soil, so tolerant plants set nearly all the seed.',
        lifetime: 'A plant cannot harden itself to copper to order, and nothing gained in one life reaches its seed. The tolerant plants were already there.',
        need: 'Poisoned soil does not create tolerance. One plant in twelve already carried the alleles, and it was the one left to set seed.',
        nothing: 'One plant in twelve already tolerates copper, and tolerance is inherited, so the poisoned soil has something to select.'
      }
    },
    {
      id: 'snails',
      frame: 'Birds have begun hunting these snails by sight on a beach of dark pebbles. Predict what happens over 10 generations.',
      fav: 'dark', alt: 'pale',
      fact: 'Shell colour is inherited.',
      start: 0, heritable: true, wOther: 0.5, gens: 10,
      opts: {
        shift: 'Dark shells become common over the generations',
        lifetime: 'Each snail darkens its shell and passes it on',
        need: 'The snails darken because they need camouflage',
        nothing: NOTHING
      },
      fb: {
        shift: 'Dark shells cannot spread if no snail has one. Selection can only act on variation that is already present, and here every snail is pale.',
        lifetime: 'A snail cannot darken its own shell to order, and none carry an allele for a dark shell, so nothing dark can appear.',
        need: 'Needing camouflage does not create it. No snail here carries a dark-shell allele, so the birds simply take them all alike.',
        nothing: 'Not one snail carries an allele for a dark shell, so the birds have no variation to select. The population is thinned, but its colour does not shift.'
      }
    },
    {
      id: 'sunflowers',
      frame: 'A hedge now shades this field of sunflowers, so only the tallest plants reach the light. Predict what happens over 10 generations.',
      fav: 'tall', alt: 'short',
      fact: 'Height here comes from the soil, not alleles.',
      start: 4, heritable: false, wOther: 0.7, gens: 10,
      opts: {
        shift: 'Tall plants become common over the generations',
        lifetime: 'Each plant stretches taller and its seed too',
        need: 'The plants grow taller because of the shade',
        nothing: NOTHING
      },
      fb: {
        shift: 'The tall plants do reach the light, but their height came from rich soil, not alleles, so their seed is no taller than any other.',
        lifetime: 'Stretching towards the light in one season does not change a plant’s alleles, so its seed does not inherit the extra height.',
        need: 'Shade does not order a plant to grow taller, and this height difference came from the soil, so it cannot be passed on.',
        nothing: 'The height difference came from the soil each plant rooted in, not from its alleles, so the tallest plants pass no extra height to their seed.'
      }
    }
  ];

  var KEYS = ['shift', 'lifetime', 'need', 'nothing'];

  /* --- the model ------------------------------------------------------ */
  /* One locus, two variants. Each generation the favoured variant's share
     is reweighted by relative survival to breeding. Counts are integers, so
     success is never decided on a float comparison.                       */
  function model(s) {
    if (!s.heritable) {
      return { end: s.start, shift: 0, wipeout: false };
    }
    var p = s.start / N;
    var wipeout = (s.start === 0 && s.wOther === 0);
    for (var g = 0; g < s.gens; g++) {
      var fav = p * 1;
      var oth = (1 - p) * s.wOther;
      p = (fav + oth) > 0 ? fav / (fav + oth) : 0;
    }
    var end = Math.round(p * N);
    return { end: end, shift: end - s.start, wipeout: wipeout };
  }

  /* The correct account is read off the model, not stored beside it. */
  function correctKey(s) {
    var m = model(s);
    return (!m.wipeout && m.shift >= 4) ? 'shift' : 'nothing';
  }

  var CSS = [
    '.svw-nsnd{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;display:flex;flex-direction:column;gap:9px}',
    '.svw-nsnd *,.svw-nsnd *::before,.svw-nsnd *::after{box-sizing:border-box}',
    '.svw-nsnd .nsnd-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--nsnd-accent);margin:0 0 3px}',
    '.svw-nsnd .nsnd-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.14rem;line-height:1.25;margin:0 0 5px}',
    '.svw-nsnd .nsnd-frame{font-size:.82rem;line-height:1.45;margin:0;max-width:66ch;color:#3c3833}',
    '.svw-nsnd .nsnd-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .6rem}',
    '.svw-nsnd .nsnd-strip{display:block;width:100%;max-width:380px;height:auto}',
    '.svw-nsnd .nsnd-count{font-size:.76rem;line-height:1.4;margin:4px 0 0;font-variant-numeric:tabular-nums}',
    '.svw-nsnd .nsnd-fact{font-size:.76rem;line-height:1.4;margin:2px 0 0;color:#8d8880}',
    '.svw-nsnd .nsnd-dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--nsnd-accent);vertical-align:baseline}',
    '.svw-nsnd .nsnd-dot--alt{background:#fff;border:1.4px solid #c9c1b4}',
    '.svw-nsnd .nsnd-opts{display:grid;grid-template-columns:1fr;gap:5px;margin:0}',
    '.svw-nsnd.is-wide .nsnd-opts{grid-template-columns:1fr 1fr}',
    '.svw-nsnd .nsnd-opt{font-family:inherit;font-size:.8rem;font-weight:500;line-height:1.35;text-align:left;padding:.42rem .6rem;border:1px solid #ddd7cd;border-radius:10px;background:#fff;color:#2d2a26;cursor:pointer}',
    '.svw-nsnd .nsnd-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-nsnd .nsnd-opt[disabled]{cursor:default;opacity:.5}',
    '.svw-nsnd .nsnd-opt[disabled][aria-pressed="true"]{opacity:1}',
    '.svw-nsnd .nsnd-opt.is-right{opacity:1;border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-nsnd .nsnd-action{display:flex;align-items:center;gap:10px;flex-wrap:wrap}',
    '.svw-nsnd .nsnd-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.48rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-nsnd .nsnd-go[disabled]{background:#faf8f5;color:#a49d93;border-color:#ddd7cd;cursor:default}',
    '.svw-nsnd .nsnd-streak{font-size:.74rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-nsnd .nsnd-cap{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.58rem .7rem;min-height:92px}',
    '.svw-nsnd .nsnd-cap[hidden]{display:none}',
    '.svw-nsnd .nsnd-cap p{margin:0;font-size:.8rem;line-height:1.5;max-width:66ch}',
    '.svw-nsnd .nsnd-cap b{font-weight:600}',
    '.svw-nsnd .nsnd-ind{fill:#fff;stroke:#c9c1b4;stroke-width:1.4}',
    '.svw-nsnd .nsnd-ind.is-fav{fill:var(--nsnd-accent);stroke:var(--nsnd-accent)}',
    '.svw-nsnd .nsnd-ind.is-dead{fill:#ece7de;stroke:#d9d2c5}',
    '.svw-nsnd.is-motion .nsnd-ind{transition:fill .4s ease,stroke .4s ease}',
    '.svw-nsnd .nsnd-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}'
  ].join('\n');

  var SVGNS = 'http://www.w3.org/2000/svg';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function lower(s) { return s.charAt(0).toLowerCase() + s.slice(1); }

  window.SVWidget = {
    meta: {
      id: 'natural-selection-not-directed',
      title: 'What happens to the population?',
      teaches: 'Variation exists first by random mutation; the environment only selects among the variants already present, and populations shift while individuals do not.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var reduced = !!ctx.reducedMotion;

      var wrap = el('div', 'svw-nsnd');
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';
      wrap.style.setProperty('--nsnd-accent', accent);
      if (!reduced) wrap.classList.add('is-motion');

      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      /* --- header ---------------------------------------------------- */
      var head = el('div', 'nsnd-head');
      head.appendChild(el('p', 'nsnd-kick', 'Evolution'));
      var h = el('h3', 'nsnd-title', 'What happens to the population?');
      head.appendChild(h);
      var frame = el('p', 'nsnd-frame', '');
      head.appendChild(frame);
      wrap.appendChild(head);

      /* --- stage: the population ------------------------------------- */
      var stage = el('div', 'nsnd-stage');
      var svg = document.createElementNS(SVGNS, 'svg');
      svg.setAttribute('viewBox', '0 0 324 46');
      svg.setAttribute('class', 'nsnd-strip');
      svg.setAttribute('role', 'img');
      var dots = [];
      for (var i = 0; i < N; i++) {
        var c = document.createElementNS(SVGNS, 'circle');
        c.setAttribute('cx', String(16 + i * 26.5));
        c.setAttribute('cy', '23');
        c.setAttribute('r', '9.5');
        c.setAttribute('class', 'nsnd-ind');
        svg.appendChild(c);
        dots.push(c);
      }
      stage.appendChild(svg);
      var count = el('p', 'nsnd-count');
      var fact = el('p', 'nsnd-fact', '');
      stage.appendChild(count);
      stage.appendChild(fact);
      wrap.appendChild(stage);

      /* --- the four accounts ----------------------------------------- */
      var opts = el('div', 'nsnd-opts');
      var btns = KEYS.map(function (k) {
        var b = el('button', 'nsnd-opt', '');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { choose(k); });
        opts.appendChild(b);
        return b;
      });
      wrap.appendChild(opts);

      /* --- commit ----------------------------------------------------- */
      var action = el('div', 'nsnd-action');
      var go = el('button', 'nsnd-go', 'Check');
      go.type = 'button';
      go.disabled = true;
      var streak = el('span', 'nsnd-streak', '');
      action.appendChild(go);
      action.appendChild(streak);
      wrap.appendChild(action);

      /* --- caption ---------------------------------------------------- */
      var cap = el('div', 'nsnd-cap');
      cap.hidden = true;
      var capP = el('p', null, '');
      cap.appendChild(capP);
      wrap.appendChild(cap);

      var sr = el('p', 'nsnd-sr', '');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);
      if (root.clientWidth >= 520) wrap.classList.add('is-wide');
      if (typeof ResizeObserver === 'function') {
        new ResizeObserver(function () {
          wrap.classList.toggle('is-wide', root.clientWidth >= 520);
        }).observe(root);
      }

      /* --- state ------------------------------------------------------ */
      var order = [0];
      var rest = [];
      for (var q = 1; q < SCEN.length; q++) rest.push(q);
      for (var r = rest.length - 1; r > 0; r--) {
        var j = Math.floor(Math.random() * (r + 1));
        var t = rest[r]; rest[r] = rest[j]; rest[j] = t;
      }
      order = order.concat(rest);

      var pos = 0;
      var scen = SCEN[order[0]];
      var layout = scatter(scen);
      var picked = null;
      var revealed = false;
      var run = 0, mastered = false, attempted = 0;

      /* a fixed, deterministic scatter so the same individuals stay put
         between the before and after views */
      function scatter(s) {
        var seed = s.id.length * 7 + s.start * 13 + s.gens;
        var idx = [];
        for (var k = 0; k < N; k++) idx.push(k);
        for (var m = N - 1; m > 0; m--) {
          seed = (seed * 1103515245 + 12345) % 2147483648;
          var p2 = seed % (m + 1);
          var tmp = idx[m]; idx[m] = idx[p2]; idx[p2] = tmp;
        }
        return idx;
      }

      function paint(k, dead) {
        var favSet = {};
        for (var a = 0; a < k; a++) favSet[layout[a]] = true;
        for (var b = 0; b < N; b++) {
          var cls = 'nsnd-ind';
          if (dead) cls += ' is-dead';
          else if (favSet[b]) cls += ' is-fav';
          dots[b].setAttribute('class', cls);
        }
      }

      function countLine(label, favN, altN, dead) {
        count.textContent = '';
        count.appendChild(document.createTextNode(label + ' — '));
        if (dead) {
          count.appendChild(document.createTextNode('none survive'));
          return;
        }
        count.appendChild(el('span', 'nsnd-dot'));
        count.appendChild(document.createTextNode(' ' + scen.fav + ' ' + favN + '  ·  '));
        count.appendChild(el('span', 'nsnd-dot nsnd-dot--alt'));
        count.appendChild(document.createTextNode(' ' + scen.alt + ' ' + altN));
      }

      function state() {
        root.dataset.svState = JSON.stringify({
          scenario: scen.id,
          choice: picked,
          committed: revealed,
          correct: revealed ? (picked === correctKey(scen)) : null,
          streak: run,
          mastered: mastered,
          attempted: attempted
        });
      }

      function render() {
        frame.textContent = scen.frame;
        fact.textContent = scen.fact;
        for (var a = 0; a < KEYS.length; a++) {
          btns[a].textContent = scen.opts[KEYS[a]];
          btns[a].disabled = false;
          btns[a].setAttribute('aria-pressed', 'false');
          btns[a].classList.remove('is-right');
        }
        paint(scen.start, false);
        countLine('Now', scen.start, N - scen.start, false);
        cap.hidden = true;
        capP.textContent = '';
        go.textContent = 'Check';
        go.disabled = true;
        svg.setAttribute('aria-label',
          'A population of 12. ' + scen.start + ' ' + scen.fav + ', ' +
          (N - scen.start) + ' ' + scen.alt + '.');
        state();
      }

      function choose(k) {
        if (revealed) return;
        picked = k;
        for (var a = 0; a < KEYS.length; a++) {
          btns[a].setAttribute('aria-pressed', KEYS[a] === k ? 'true' : 'false');
        }
        go.disabled = false;
        state();
      }

      function say(html) {
        capP.textContent = '';
        var parts = html.split('|');
        for (var a = 0; a < parts.length; a++) {
          if (a % 2) capP.appendChild(el('b', null, parts[a]));
          else capP.appendChild(document.createTextNode(parts[a]));
        }
        cap.hidden = false;
      }

      function commit() {
        var m = model(scen);
        var key = correctKey(scen);
        var right = picked === key;
        revealed = true;
        attempted++;

        paint(m.end, m.wipeout);
        if (m.wipeout) countLine('After the antibiotic', 0, 0, true);
        else countLine('After ' + scen.gens + ' generations', m.end, N - m.end, false);

        for (var a = 0; a < KEYS.length; a++) {
          btns[a].disabled = true;
          if (KEYS[a] === key) btns[a].classList.add('is-right');
        }

        var lostRun = (!right && run > 0);
        run = right ? run + 1 : 0;
        var justMastered = right && run >= 3 && !mastered;
        if (right && run >= 3) mastered = true;

        var text;
        if (right) {
          text = '|Right| — you said “' + lower(scen.opts[key]) +
                 '”. ' + scen.fb[key];
        } else {
          text = '|Not quite| — you said “' + lower(scen.opts[picked]) +
                 '”. ' + scen.fb[picked];
          if (lostRun) text += ' Your run resets to zero.';
        }
        if (justMastered) {
          text += ' |Three in a row — you have it.| Variation comes first, at ' +
                  'random; the environment only picks among the varieties ' +
                  'already there.';
        }
        say(text);

        streak.textContent = mastered ? (run + ' in a row')
          : run === 0 ? ''
          : run === 1 ? '1 in a row'
          : '2 in a row — one more';

        go.textContent = mastered ? 'Another anyway' : 'Next scenario';
        go.disabled = false;
        sr.textContent = capP.textContent;
        state();
      }

      function next() {
        pos = (pos + 1) % order.length;
        scen = SCEN[order[pos]];
        layout = scatter(scen);
        picked = null;
        revealed = false;
        render();
        btns[0].focus();
      }

      go.addEventListener('click', function () {
        if (revealed) next(); else if (picked) commit();
      });

      render();
    }
  };
})();
