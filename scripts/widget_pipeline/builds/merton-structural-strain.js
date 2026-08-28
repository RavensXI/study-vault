/* merton-structural-strain — Merton's five adaptations as structural responses. */
(function () {
  'use strict';

  var ADAPTATIONS = [
    { key: 'conformity', name: 'Conformity', goals: 'Accept', means: 'Accept',
      sig: 'keeping the goal and staying with the approved route' },
    { key: 'innovation', name: 'Innovation', goals: 'Accept', means: 'Reject',
      sig: 'keeping the goal but taking a route society does not approve' },
    { key: 'ritualism', name: 'Ritualism', goals: 'Reject', means: 'Accept',
      sig: 'giving up the goal but still going through the routine' },
    { key: 'retreatism', name: 'Retreatism', goals: 'Reject', means: 'Reject',
      sig: 'giving up the goal and the route together' },
    { key: 'rebellion', name: 'Rebellion', goals: 'Replace', means: 'Replace',
      sig: 'swapping both the goal and the route for new ones' }
  ];

  var BY_KEY = {};
  ADAPTATIONS.forEach(function (a) { BY_KEY[a.key] = a; });

  /* the row's own grid vocabulary, so feedback echoes the stage */
  function shape(a) {
    if (a.key === 'rebellion') return 'replace the goal and the route';
    return a.goals.toLowerCase() + ' the goal, ' + a.means.toLowerCase() + ' the route';
  }

  /* Original, neutral cases. Every adaptation appears; innovation rounds
     also offer the "bad person" answer so the misconception is enterable. */
  var CASES = [
    { id: 'inn1', join: 'but', name: 'Priya', answer: 'innovation',
      text: 'Priya wants the money her town counts as success. Her course was dropped and local jobs pay too little to save. She sells fake trainers online.',
      keeps: 'still wants the money',
      route: 'she is taking a route society does not approve',
      why: 'Merton argued the gap did this, not Priya’s character — anyone blocked that way feels the same pull.' },
    { id: 'con1', join: 'and', name: 'Devan', answer: 'conformity',
      text: 'Devan wants the trade career his family respects. Places are scarce and he was turned down twice. He stays on his course and applies again.',
      keeps: 'still wants the career',
      route: 'he is still on the approved route',
      why: 'Merton counted this as an adaptation too: blocked, and still on the approved route.' },
    { id: 'rit1', join: 'but', name: 'Maryam', answer: 'ritualism',
      text: 'Maryam wanted the manager’s job. After eight years of being passed over she no longer expects it. She still arrives early and obeys the rules.',
      keeps: 'has let go of the goal',
      route: 'she still follows the approved routine',
      why: 'Merton argued the routine can outlive the ambition it was meant to serve.' },
    { id: 'inn2', join: 'but', name: 'Corey', answer: 'innovation',
      text: 'Corey wants the money his friends treat as success. He left school without the qualifications employers ask for. He sells fake tickets online.',
      keeps: 'still wants the money',
      route: 'he is taking a route society does not approve',
      why: 'Merton argued the shut route, not the character, is what produced this.' },
    { id: 'reb1', join: 'and', name: 'Ella', answer: 'rebellion',
      text: 'Ella wanted a home of her own, but rents outrun any wage. She says private ownership is the wrong goal and campaigns for community housing.',
      keeps: 'has swapped the goal for a new one',
      route: 'she is pushing for a new route too',
      why: 'Merton argued rebellion does not only reject — it puts a new goal and a new route in place.' },
    { id: 'ret1', join: 'and', name: 'Nathan', answer: 'retreatism',
      text: 'Nathan chased the qualifications and the job for years. After many rejections he stopped applying, stopped seeing people and left the routine.',
      keeps: 'has given up the goal',
      route: 'he has given up the route as well',
      why: 'Merton called this the double rejection: no goal left and no route left.' },
    { id: 'inn3', join: 'but', name: 'Jamie', answer: 'innovation',
      text: 'Jamie needs the grades for the career he wants. His school dropped the subject and he cannot pay a tutor. He pays someone to sit his test.',
      keeps: 'still wants the grades',
      route: 'he is taking a route society does not approve',
      why: 'Merton argued the goal stayed while the approved route closed. The gap did the rest.' },
    { id: 'con2', join: 'and', name: 'Ola', answer: 'conformity',
      text: 'Ola wants a living from football, the measure of success at his club. The academy released him and trials cost money. He trains on and saves.',
      keeps: 'still wants the career',
      route: 'he is still on the approved route',
      why: 'Merton argued most blocked people stay on the approved route, and that this holds order together.' },
    { id: 'rit2', join: 'but', name: 'Rehana', answer: 'ritualism',
      text: 'Rehana no longer believes the grades bring the career she wanted; friends got them and got nowhere. She still hands in every homework on time.',
      keeps: 'no longer expects the goal',
      route: 'she still follows the approved routine',
      why: 'Merton argued the rules feel safe once the prize looks out of reach.' },
    { id: 'reb2', join: 'and', name: 'Tomas', answer: 'rebellion',
      text: 'Tomas no longer thinks owning things is success and has quit the job ladder. He grows food on shared land and argues for a better measure.',
      keeps: 'has swapped the goal for a new one',
      route: 'he is building a new route too',
      why: 'Merton argued rebellion swaps the goal and the route for new ones, rather than dropping out.' }
  ];

  var OPEN_CAP = 'Two questions each time: does the person keep the goal, and do they keep the approved route?';

  var MASTERY_LINE = 'Three in a row — you have it. All five are adaptations to one gap, so the structure sets what is on offer, not the person. Merton’s own limit: it fits crime done for gain better than violence, and most blocked people never offend.';

  var CSS = [
    '.svw-mss{font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;-webkit-font-smoothing:antialiased}',
    '.svw-mss *{box-sizing:border-box}',
    '.svw-mss .mss-kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--mss-accent)}',
    '.svw-mss .mss-title{margin:.14rem 0 0;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.14rem;line-height:1.24}',
    '.svw-mss .mss-frame{margin:.3rem 0 .55rem;font-size:.8rem;line-height:1.45;color:#5b564e}',
    '.svw-mss .mss-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.58rem .62rem .5rem}',
    '.svw-mss .mss-case{margin:0 0 .48rem;font-size:.84rem;line-height:1.42}',
    '.svw-mss .mss-head{display:grid;grid-template-columns:1fr 62px 62px;gap:.3rem;padding:0 .5rem .18rem;font-size:.66rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#8d8880}',
    '.svw-mss .mss-head span:not(:first-child){text-align:center}',
    '.svw-mss .mss-rows{display:flex;flex-direction:column;gap:.22rem}',
    '.svw-mss .mss-row{display:grid;grid-template-columns:1fr 62px 62px;gap:.3rem;align-items:center;width:100%;min-height:32px;padding:.28rem .5rem;text-align:left;font:inherit;font-size:.8rem;font-weight:600;color:#2d2a26;background:#fff;border:1px solid #e0d9cd;border-radius:9px;cursor:pointer}',
    '.svw-mss .mss-row .mss-cell{font-size:.72rem;font-weight:500;text-align:center;color:#5b564e;font-variant-numeric:tabular-nums}',
    '.svw-mss .mss-row .mss-nm{display:block;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}',
    '.svw-mss .mss-row .mss-tag{display:block;font-size:.66rem;font-weight:600;color:#8d8880;line-height:1.3}',
    '.svw-mss .mss-row.is-picked{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-mss .mss-row.is-picked .mss-cell,.svw-mss .mss-row.is-picked .mss-tag{color:#e6e2db}',
    '.svw-mss .mss-row.is-you{background:#f1ece4;border-color:#b8b1a5;color:#2d2a26}',
    '.svw-mss .mss-row.is-you .mss-cell,.svw-mss .mss-row.is-you .mss-tag{color:#5b564e}',
    '.svw-mss .mss-row.is-home{background:var(--mss-tint);border-color:var(--mss-accent);color:#2d2a26}',
    '.svw-mss .mss-row.is-home .mss-tag{color:var(--mss-accent)}',
    '.svw-mss .mss-row[disabled]{cursor:default;opacity:1}',
    '.svw-mss .mss-odd{display:block;width:100%;margin-top:.34rem;padding:.38rem .5rem;text-align:left;font:inherit;font-size:.78rem;font-weight:600;color:#5b564e;background:#fff;border:1px dashed #d5cec2;border-radius:9px;cursor:pointer}',
    '.svw-mss .mss-odd.is-picked{background:#2d2a26;border-style:solid;border-color:#2d2a26;color:#fff}',
    '.svw-mss .mss-odd.is-you{background:#f1ece4;border-style:solid;border-color:#b8b1a5;color:#2d2a26}',
    '.svw-mss .mss-bar{display:flex;align-items:center;gap:.6rem;margin-top:.55rem}',
    '.svw-mss .mss-run{flex:1;min-width:0;font-size:.72rem;line-height:1.3;color:#8d8880}',
    '.svw-mss .mss-go{flex:none;font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-mss .mss-go.is-live{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-mss .mss-cap{margin:.45rem 0 0;font-size:.8rem;line-height:1.45;color:#2d2a26;min-height:3.2em}',
    '.svw-mss .mss-cap b{font-weight:600}',
    '.svw-mss .mss-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-mss .mss-row:focus-visible,.svw-mss .mss-odd:focus-visible,.svw-mss .mss-go:focus-visible{outline:2px solid var(--mss-accent);outline-offset:2px}',
    '.svw-mss.mss-motion .mss-row,.svw-mss.mss-motion .mss-odd,.svw-mss.mss-motion .mss-go{transition:background-color .12s ease,border-color .12s ease,color .12s ease}'
  ].join('\n');

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'merton-structural-strain',
      title: 'Blocked routes, five adaptations',
      teaches: 'Merton’s five responses to strain are structural adaptations to blocked goals, not personality types.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#7a6a52';
      var reduced = !!ctx.reducedMotion;

      root.classList.add('svw-mss');
      if (!reduced) root.classList.add('mss-motion');
      root.style.setProperty('--mss-accent', accent);
      root.style.setProperty('--mss-tint', accent + '22');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      root.appendChild(el('p', 'mss-kick', 'Strain theory'));
      root.appendChild(el('h3', 'mss-title', 'Blocked routes, five adaptations'));
      root.appendChild(el('p', 'mss-frame',
        'Merton argued that society sets the same goals for everyone but does not open the approved routes to everyone. Decide which adaptation each response is.'));

      var stage = el('div', 'mss-stage');
      var caseP = el('p', 'mss-case');
      stage.appendChild(caseP);

      var head = el('div', 'mss-head');
      head.appendChild(el('span', null, 'Adaptation'));
      head.appendChild(el('span', null, 'Goals'));
      head.appendChild(el('span', null, 'Means'));
      stage.appendChild(head);

      var rowsWrap = el('div', 'mss-rows');
      var rowBtns = {};
      ADAPTATIONS.forEach(function (a) {
        var b = el('button', 'mss-row');
        b.type = 'button';
        var first = el('span');
        var nm = el('span', 'mss-nm', a.name);
        var tag = el('span', 'mss-tag', '');
        tag.hidden = true;
        first.appendChild(nm);
        first.appendChild(tag);
        first.style.minWidth = '0';
        b.appendChild(first);
        b.appendChild(el('span', 'mss-cell', a.goals));
        b.appendChild(el('span', 'mss-cell', a.means));
        b.addEventListener('click', function () { pick(a.key); });
        rowBtns[a.key] = { btn: b, tag: tag };
        rowsWrap.appendChild(b);
      });
      stage.appendChild(rowsWrap);

      var oddBtn = el('button', 'mss-odd', '“They’re just a bad person.”');
      oddBtn.type = 'button';
      oddBtn.addEventListener('click', function () { pick('bad'); });
      stage.appendChild(oddBtn);

      root.appendChild(stage);

      var bar = el('div', 'mss-bar');
      var run = el('p', 'mss-run', '');
      var go = el('button', 'mss-go', 'Check');
      go.type = 'button';
      bar.appendChild(run);
      bar.appendChild(go);
      root.appendChild(bar);

      var cap = el('p', 'mss-cap', '');
      root.appendChild(cap);

      var sr = el('p', 'mss-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---- state ---- */
      var order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      var seat = 0;
      var current = CASES[order[0]];
      var picked = null;
      var revealed = false;
      var streak = 0;
      var attempted = 0;
      var mastered = false;

      function sync(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted, round: current.id };
        if (extra) Object.keys(extra).forEach(function (k) { s[k] = extra[k]; });
        root.dataset.svState = JSON.stringify(s);
      }

      function clearMarks() {
        Object.keys(rowBtns).forEach(function (k) {
          var r = rowBtns[k];
          r.btn.classList.remove('is-picked', 'is-you', 'is-home');
          r.btn.disabled = false;
          r.tag.hidden = true;
          r.tag.textContent = '';
        });
        oddBtn.classList.remove('is-picked', 'is-you');
        oddBtn.disabled = false;
      }

      function renderCase() {
        caseP.textContent = current.text;
        oddBtn.hidden = current.answer !== 'innovation';
        clearMarks();
        picked = null;
        revealed = false;
        go.textContent = 'Check';
        go.classList.remove('is-live');
        cap.textContent = OPEN_CAP;
        sync();
      }

      function pick(key) {
        if (revealed) return;
        picked = key;
        Object.keys(rowBtns).forEach(function (k) {
          rowBtns[k].btn.classList.toggle('is-picked', k === key);
        });
        oddBtn.classList.toggle('is-picked', key === 'bad');
        go.classList.add('is-live');
        cap.textContent = OPEN_CAP;
        sr.textContent = (key === 'bad' ? 'They’re just a bad person' : BY_KEY[key].name) + ' chosen. Press Check.';
        sync({ picked: key });
      }

      function say(html) {
        cap.innerHTML = html;
        sr.textContent = cap.textContent;
      }

      function commit() {
        var right = BY_KEY[current.answer];
        var correct = picked === current.answer;
        attempted += 1;
        streak = correct ? streak + 1 : 0;
        var justMastered = false;
        if (correct && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        revealed = true;
        Object.keys(rowBtns).forEach(function (k) {
          var r = rowBtns[k];
          r.btn.classList.remove('is-picked');
          r.btn.disabled = true;
        });
        oddBtn.classList.remove('is-picked');
        oddBtn.disabled = true;

        var home = rowBtns[current.answer];
        home.btn.classList.add('is-home');
        home.tag.hidden = false;
        home.tag.textContent = current.name + ' lands here';

        if (!correct) {
          if (picked === 'bad') {
            oddBtn.classList.add('is-you');
          } else {
            var yours = rowBtns[picked];
            yours.btn.classList.add('is-you');
            yours.tag.hidden = false;
            yours.tag.textContent = 'your answer';
          }
        }

        var body;
        if (correct && justMastered) {
          body = '<b>Right — ' + right.name + '.</b> ' + MASTERY_LINE;
        } else if (correct) {
          body = '<b>Right — ' + right.name + ':</b> ' + shape(right) + '. ' + current.why;
        } else if (picked === 'bad') {
          body = '<b>Not quite — you said they are just a bad person.</b> The grid has no row for that: it sorts by structure, not character. ' +
                 current.name + ' wants what everyone is taught to want; the approved route closed. That is <b>' + right.name + '</b>.';
        } else {
          var chose = BY_KEY[picked];
          body = '<b>Not quite — you said ' + chose.name + ':</b> ' + shape(chose) + '. ' +
                 current.name + ' ' + current.keeps + ', ' + current.join + ' ' + current.route + '. That is <b>' + right.name + '</b>.';
        }
        say(body);

        if (mastered) {
          run.textContent = correct ? 'You have it. Keep going if you want.'
                                   : 'You had it — that one slipped. Worth another.';
          go.textContent = 'Another anyway';
        } else if (streak === 0) {
          run.textContent = 'Run back to zero — three in a row finishes it.';
          go.textContent = 'Next case';
        } else {
          run.textContent = streak + ' right in a row — ' + (3 - streak) + ' more and you have it.';
          go.textContent = 'Next case';
        }
        go.classList.remove('is-live');
        sync({ picked: picked, correct: correct });
      }

      go.addEventListener('click', function () {
        if (revealed) {
          seat = (seat + 1) % order.length;
          current = CASES[order[seat]];
          renderCase();
          sr.textContent = 'New case. ' + current.text;
          return;
        }
        if (!picked) {
          say('Choose a row of the grid first — or the line under it, if you think that is the real answer.');
          return;
        }
        commit();
      });

      renderCase();
    }
  };
}());
