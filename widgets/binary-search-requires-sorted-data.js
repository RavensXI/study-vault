/* Widget: binary-search-requires-sorted-data
 * Trace a binary search. Predict the outcome and the exact number of
 * comparisons. Every round is executed by the real algorithm below, so the
 * examined indices, the discarded halves, the comparison count and the
 * found/missing verdict are computed, never asserted.
 */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- model */

  /* Canonical GCSE binary search.
     mid = floor((low + high) / 2)  -> the left-hand middle when two are level.
     One comparison per item examined. */
  function runBinary(list, target) {
    var low = 0, high = list.length - 1, steps = [], comparisons = 0;
    while (low <= high) {
      var mid = Math.floor((low + high) / 2);
      comparisons += 1;
      var step = { low: low, high: high, mid: mid, value: list[mid], dir: 'hit' };
      steps.push(step);
      if (list[mid] === target) {
        return { found: true, at: mid, comparisons: comparisons, steps: steps,
                 endLow: low, endHigh: high };
      }
      if (list[mid] < target) { step.dir = 'right'; low = mid + 1; }
      else { step.dir = 'left'; high = mid - 1; }
    }
    return { found: false, at: -1, comparisons: comparisons, steps: steps,
             endLow: low, endHigh: high };
  }

  function isSorted(list) {
    for (var i = 1; i < list.length; i++) { if (list[i] < list[i - 1]) return false; }
    return true;
  }

  /* Linear search: checks needed to answer the same question. */
  function linearChecks(list, target) {
    for (var i = 0; i < list.length; i++) { if (list[i] === target) return i + 1; }
    return list.length;
  }

  /* The step at which the target's index fell outside the live window. */
  function lostAt(steps, targetIndex) {
    if (targetIndex < 0) return null;
    for (var i = 0; i < steps.length; i++) {
      var s = steps[i];
      var inOld = targetIndex >= s.low && targetIndex <= s.high;
      if (!inOld) continue;
      var nLow = s.low, nHigh = s.high;
      if (s.dir === 'right') nLow = s.mid + 1;
      else if (s.dir === 'left') nHigh = s.mid - 1;
      else return null;
      if (targetIndex < nLow || targetIndex > nHigh) {
        return { index: i, value: s.value, side: s.dir === 'right' ? 'left' : 'right' };
      }
    }
    return null;
  }

  /* Round pool. Lists hand-chosen; every consequence is computed at mount. */
  var POOL = [
    { list: [12, 25, 31, 44, 58, 63, 79, 84, 91], target: 84 },
    { list: [40, 57, 12, 88, 34, 96, 21, 73, 65], target: 57 },
    { list: [15, 23, 38, 42, 56, 61, 77], target: 50 },
    { list: [12, 25, 31, 44, 58, 63, 79, 84, 91], target: 12 },
    { list: [88, 12, 95, 30, 41, 23, 67, 76, 19], target: 76 },
    { list: [63, 41, 88, 17, 92, 25, 70, 36, 59, 14, 80], target: 88 },
    { list: [8, 16, 23, 37, 45, 52, 60, 68, 74, 81, 95], target: 74 },
    { list: [72, 15, 48, 91, 33, 60, 27, 84, 19, 55, 40], target: 15 }
  ];

  function buildRound(spec) {
    var r = {};
    r.list = spec.list.slice();
    r.target = spec.target;
    r.sorted = isSorted(r.list);
    r.targetIndex = r.list.indexOf(r.target);
    r.linear = linearChecks(r.list, r.target);
    r.res = runBinary(r.list, r.target);
    r.lost = lostAt(r.res.steps, r.targetIndex);
    r.sizes = r.res.steps.map(function (s) { return s.high - s.low + 1; });
    return r;
  }

  var ROUNDS = POOL.map(buildRound);
  var MAX_N = ROUNDS.reduce(function (m, r) { return Math.max(m, r.list.length); }, 0);

  /* ------------------------------------------------------------- language */

  function plural(n, word) { return n + ' ' + word + (n === 1 ? '' : 's'); }

  function outcomePhrase(r) {
    return r.res.found
      ? 'it found ' + r.target + ' in ' + plural(r.res.comparisons, 'comparison')
      : 'it made ' + plural(r.res.comparisons, 'comparison') +
        ' and reported ' + r.target + ' missing';
  }

  function mechanism(r) {
    var sizes = r.sizes.join(' → ');
    if (r.sorted && r.res.found) {
      return 'The list is sorted, so every comparison deletes a half that could not ' +
             'hold ' + r.target + ': ' + sizes + ' items left. One at a time would be ' +
             plural(r.linear, 'check') + '.';
    }
    if (r.sorted && !r.res.found) {
      return 'The list is sorted, so each discarded half genuinely could not hold ' +
             r.target + ' — this "not in the list" can be trusted. A linear search ' +
             'needs all ' + plural(r.linear, 'check') + ' to say the same.';
    }
    if (!r.sorted && !r.res.found) {
      var s = 'The list is not sorted. ' + r.target + ' is sitting at index ' +
              r.targetIndex + ': ';
      s += r.lost
        ? 'seeing ' + r.lost.value + ' in the middle, the search threw away the ' +
          r.lost.side + ' half that held it. '
        : 'the halving stepped straight past it. ';
      return s + 'A linear search finds it on check ' + r.linear + '.';
    }
    return 'The list is not sorted, so nothing guaranteed ' + r.target + ' was in the ' +
           'half it kept — that was luck, not method. On another unsorted list the ' +
           'same ' + plural(r.res.comparisons, 'comparison') + ' can bin the target.';
  }

  function feedback(r, pick) {
    var right = (pick.outcome === (r.res.found ? 'find' : 'miss')) &&
                pick.count === r.res.comparisons;
    var head;
    if (right) {
      head = '<b class="ok">Right —</b> ' + outcomePhrase(r) + '.';
    } else {
      head = '<b class="no">Not quite —</b> you said it ' +
             (pick.outcome === 'find' ? 'finds ' : 'misses ') + r.target + ' in ' +
             plural(pick.count, 'comparison') + '. What happened: ' + outcomePhrase(r) + '.';
    }
    var tail = '';
    if (!right && pick.outcome === 'find' && !r.res.found) {
      tail = ' It never even looks at index ' + r.targetIndex + '.';
    } else if (!right && pick.count >= r.linear && r.res.comparisons < pick.count) {
      tail = ' It does not walk the list one at a time.';
    }
    return { right: right, html: head + ' ' + mechanism(r) + tail };
  }

  /* ------------------------------------------------------------------ CSS */

  var CSS = [
    '.svw-bsq{font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;',
    'background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1.15rem;',
    'box-sizing:border-box;line-height:1.45;position:relative;}',
    '.svw-bsq *{box-sizing:border-box;}',
    '.svw-bsq .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--bsq-accent);margin:0 0 .18rem;}',
    '.svw-bsq h3.ttl{font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
    'font-size:1.22rem;margin:0 0 .3rem;line-height:1.2;}',
    '.svw-bsq .frame{font-size:.84rem;color:#5b564e;margin:0 0 .7rem;}',
    '.svw-bsq .frame b{color:#2d2a26;}',
    '.svw-bsq .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
    'padding:.6rem .55rem .5rem;}',
    '.svw-bsq .marks,.svw-bsq .strip,.svw-bsq .idx{display:grid;gap:3px;}',
    '.svw-bsq .marks{height:15px;align-items:end;}',
    '.svw-bsq .mark{font-size:.66rem;font-weight:700;text-align:center;',
    'color:var(--bsq-accent);font-variant-numeric:tabular-nums;line-height:1;}',
    '.svw-bsq .cell{font-family:inherit;font-size:.78rem;font-weight:600;',
    'font-variant-numeric:tabular-nums;padding:.3rem .1rem;border-radius:7px;',
    'border:1px solid #e0d9cd;background:#fff;color:#2d2a26;text-align:center;',
    'cursor:pointer;min-width:0;}',
    '.svw-bsq .cell.dim{opacity:.3;}',
    '.svw-bsq .cell.seen{border-color:#2d2a26;border-width:2px;padding:calc(.3rem - 1px) 0;}',
    '.svw-bsq .cell.hit{background:#2d2a26;color:#fff;border-color:#2d2a26;}',
    '.svw-bsq .cell.tgt{border:2px dotted var(--bsq-accent);opacity:1;',
    'padding:calc(.3rem - 1px) 0;}',
    '.svw-bsq .cell.tap{border-color:var(--bsq-accent);}',
    '.svw-bsq .idx span{font-size:.66rem;color:#8d8880;text-align:center;',
    'font-variant-numeric:tabular-nums;line-height:1.3;}',
    '.svw-bsq .read{font-size:.74rem;color:#8d8880;margin:.35rem 0 0;min-height:1.1em;',
    'font-variant-numeric:tabular-nums;}',
    '.svw-bsq .steplab{font-size:.78rem;font-weight:600;margin:.7rem 0 .3rem;}',
    '.svw-bsq .steplab i{font-style:normal;color:var(--bsq-accent);}',
    '.svw-bsq .row{display:flex;flex-wrap:wrap;gap:5px;}',
    '.svw-bsq button{font-family:inherit;}',
    '.svw-bsq .opt{flex:1 1 130px;font-size:.8rem;font-weight:600;padding:.45rem .5rem;',
    'border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;',
    'cursor:pointer;}',
    '.svw-bsq .num{font-size:.8rem;font-weight:600;padding:.34rem 0;min-width:30px;',
    'flex:0 0 auto;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;',
    'color:#2d2a26;cursor:pointer;font-variant-numeric:tabular-nums;}',
    '.svw-bsq .opt[aria-pressed="true"],.svw-bsq .num[aria-pressed="true"]',
    '{background:#2d2a26;color:#fff;border-color:#2d2a26;}',
    '.svw-bsq .go{margin-top:.6rem;font-size:.82rem;font-weight:600;',
    'padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;',
    'background:#2d2a26;color:#fff;cursor:pointer;}',
    '.svw-bsq .go.is-off{background:#faf8f5;color:#8d8880;border-color:#ddd7cd;}',
    '.svw-bsq .again{margin-top:.7rem;font-size:.82rem;font-weight:600;',
    'padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;',
    'background:#faf8f5;color:#2d2a26;cursor:pointer;}',
    '.svw-bsq .said{font-size:.8rem;font-weight:600;margin:.65rem 0 0;}',
    '.svw-bsq .said span{color:#8d8880;font-weight:400;}',
    '.svw-bsq .run{font-size:.76rem;color:#8d8880;margin:.35rem 0 0;min-height:1.05em;}',
    '.svw-bsq .run.done{color:#4f7d63;font-weight:600;}',
    '.svw-bsq .cap{font-size:.84rem;line-height:1.5;margin:.6rem 0 0;min-height:3em;}',
    '.svw-bsq .cap .ok{color:#4f7d63;}',
    '.svw-bsq .cap .no{color:#2d2a26;}',
    '.svw-bsq .sr{position:absolute;width:1px;height:1px;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;}',
    '.svw-bsq.motion .cell,.svw-bsq.motion .opt,.svw-bsq.motion .num',
    '{transition:background-color .15s ease,opacity .2s ease,border-color .15s ease;}',
    '@media (min-width:620px){.svw-bsq .num{min-width:34px;}',
    '.svw-bsq .cell{font-size:.85rem;padding:.38rem .1rem;}}'
  ].join('');

  /* ---------------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: 'binary-search-requires-sorted-data',
      title: 'Trace the binary search',
      teaches: 'Binary search halves the list by checking the middle item; the ' +
               'discard is only safe because the list is sorted, so on unsorted ' +
               'data the search can throw away the half holding the target.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#96502f';
      var reduced = !!ctx.reducedMotion;

      if (!root.querySelector('style[data-bsq]')) {
        var st = document.createElement('style');
        st.setAttribute('data-bsq', '1');
        st.textContent = CSS;
        root.appendChild(st);
      }

      var w = document.createElement('div');
      w.className = 'svw-bsq' + (reduced ? '' : ' motion');
      w.style.setProperty('--bsq-accent', accent);
      root.appendChild(w);

      w.innerHTML =
        '<p class="kick">Searching algorithms</p>' +
        '<h3 class="ttl">Trace the binary search</h3>' +
        '<p class="frame" id="bsq-frame"></p>' +
        '<div class="stage">' +
          '<div class="marks" id="bsq-marks"></div>' +
          '<div class="strip" id="bsq-strip"></div>' +
          '<div class="idx" id="bsq-idx"></div>' +
          '<p class="read" id="bsq-read"></p>' +
        '</div>' +
        '<div id="bsq-ask">' +
          '<p class="steplab"><i>1</i> &middot; <span id="bsq-q1"></span></p>' +
          '<div class="row">' +
            '<button type="button" class="opt" id="bsq-find" aria-pressed="false"></button>' +
            '<button type="button" class="opt" id="bsq-miss" aria-pressed="false"></button>' +
          '</div>' +
          '<p class="steplab"><i>2</i> &middot; How many comparisons?</p>' +
          '<div class="row" id="bsq-nums"></div>' +
          '<button type="button" class="go is-off" id="bsq-go">Run the search</button>' +
        '</div>' +
        '<p class="said" id="bsq-said" hidden></p>' +
        '<p class="run" id="bsq-run"></p>' +
        '<p class="cap" id="bsq-cap"></p>' +
        '<button type="button" class="again" id="bsq-next" hidden>Next list</button>' +
        '<p class="sr" id="bsq-sr" aria-live="polite"></p>';

      var $ = function (id) { return w.querySelector('#bsq-' + id); };
      var elFrame = $('frame'), elMarks = $('marks'), elStrip = $('strip'),
          elIdx = $('idx'), elRead = $('read'), elQ1 = $('q1'), elFind = $('find'),
          elMiss = $('miss'), elNums = $('nums'), elGo = $('go'), elAsk = $('ask'),
          elSaid = $('said'), elNext = $('next'),
          elRun = $('run'), elCap = $('cap'), elSr = $('sr');

      /* Cells, index labels and markers built once at the widest round. */
      var cells = [], marks = [], idxs = [], nums = [];
      var i;
      for (i = 0; i < MAX_N; i++) {
        var m = document.createElement('div');
        m.className = 'mark';
        elMarks.appendChild(m); marks.push(m);

        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'cell';
        b.dataset.i = String(i);
        elStrip.appendChild(b); cells.push(b);

        var s = document.createElement('span');
        elIdx.appendChild(s); idxs.push(s);
      }
      for (i = 1; i <= MAX_N; i++) {
        var n = document.createElement('button');
        n.type = 'button';
        n.className = 'num';
        n.textContent = String(i);
        n.dataset.n = String(i);
        n.setAttribute('aria-pressed', 'false');
        n.setAttribute('aria-label', plural(i, 'comparison'));
        elNums.appendChild(n); nums.push(n);
      }

      var order = [0, 1, 2, 3, 4, 5, 6, 7];
      var pos = 0, round = null, pick = { outcome: null, count: null };
      var streak = 0, attempted = 0, mastered = false, committed = false;

      var inspect = null, lastCorrect = null;

      function setState() {
        var d = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) {
          d.round = pos + 1;
          d.sorted = round.sorted;
          d.target = round.target;
          d.comparisons = round.res.comparisons;
          d.outcome = round.res.found ? 'found' : 'missing';
        }
        d.committed = committed;
        d.picked = pick.outcome;
        d.pickedCount = pick.count;
        if (inspect !== null) d.inspect = inspect;
        if (committed) d.correct = lastCorrect;
        root.dataset.svState = JSON.stringify(d);
      }

      function paint() {
        var r = round, n = r.list.length;
        elStrip.style.gridTemplateColumns = 'repeat(' + n + ',minmax(0,1fr))';
        elMarks.style.gridTemplateColumns = elStrip.style.gridTemplateColumns;
        elIdx.style.gridTemplateColumns = elStrip.style.gridTemplateColumns;

        var seen = {}, k;
        for (k = 0; k < r.res.steps.length; k++) { seen[r.res.steps[k].mid] = k + 1; }
        var lo = committed ? r.res.endLow : 0;
        var hi = committed ? r.res.endHigh : r.list.length - 1;

        for (k = 0; k < MAX_N; k++) {
          var c = cells[k];
          if (k >= n) { c.hidden = true; marks[k].hidden = true; idxs[k].hidden = true; continue; }
          c.hidden = false; marks[k].hidden = false; idxs[k].hidden = false;
          c.textContent = String(r.list[k]);
          c.setAttribute('aria-label', 'Index ' + k + ', value ' + r.list[k]);
          idxs[k].textContent = String(k);
          c.className = 'cell';
          marks[k].textContent = '';
          if (!committed) continue;
          if (seen[k]) { marks[k].textContent = String(seen[k]); }
          var dropped = (k < lo || k > hi) && !(r.res.found && k === r.res.at);
          if (r.res.found && k === r.res.at) c.className = 'cell hit';
          else if (seen[k]) c.className = 'cell seen' + (dropped ? ' dim' : '');
          else if (dropped) c.className = 'cell dim';
          if (!r.res.found && k === r.targetIndex) c.className = 'cell tgt';
        }
      }

      function newRound() {
        if (pos >= order.length) { pos = 0; }
        round = ROUNDS[order[pos]];
        committed = false;
        pick = { outcome: null, count: null };
        elFrame.innerHTML =
          'A binary search runs on this list, looking for <b>' + round.target + '</b>. ' +
          'It checks the middle item, then throws away the half the target cannot be in. ' +
          'Some of these lists are sorted; some are not.';
        elQ1.textContent = 'Does it find ' + round.target + '?';
        elFind.textContent = 'Finds ' + round.target;
        elMiss.textContent = 'Reports it missing';
        elFind.setAttribute('aria-pressed', 'false');
        elMiss.setAttribute('aria-pressed', 'false');
        for (var k = 0; k < MAX_N; k++) {
          nums[k].hidden = k >= round.list.length;
          nums[k].setAttribute('aria-pressed', 'false');
        }
        elRead.textContent = 'Middle = the left-hand one when two are level.';
        elAsk.hidden = false;
        elSaid.hidden = true;
        elNext.hidden = true;
        elRun.textContent = '';
        elGo.classList.add('is-off');
        elCap.innerHTML = '';
        inspect = null;
        lastCorrect = null;
        paint();
        setState();
      }

      function refreshGo() {
        var ready = pick.outcome && pick.count;
        elGo.classList.toggle('is-off', !ready);
        elGo.setAttribute('aria-disabled', ready ? 'false' : 'true');
      }

      function chooseOutcome(v) {
        if (committed) return;
        pick.outcome = v;
        elFind.setAttribute('aria-pressed', v === 'find' ? 'true' : 'false');
        elMiss.setAttribute('aria-pressed', v === 'miss' ? 'true' : 'false');
        refreshGo();
        setState();
      }

      function chooseCount(v) {
        if (committed) return;
        pick.count = v;
        for (var k = 0; k < MAX_N; k++) {
          nums[k].setAttribute('aria-pressed', (k + 1) === v ? 'true' : 'false');
        }
        refreshGo();
        setState();
      }

      function commit() {
        if (committed) return;
        if (!pick.outcome || !pick.count) {
          elCap.innerHTML = 'Choose both parts: does it find ' + round.target +
            ', and in how many comparisons?';
          inspect = null;
          setState();
          return;
        }
        committed = true;
        attempted += 1;
        var f = feedback(round, pick);
        lastCorrect = f.right;
        streak = f.right ? streak + 1 : 0;
        if (streak >= 3) mastered = true;

        paint();

        var trace = round.res.steps.map(function (s) { return s.value; }).join(' → ');
        elRead.textContent = 'Checked ' + trace + ' — ' +
          (round.res.found ? 'match at index ' + round.res.at : 'no match');
        elSaid.innerHTML = '<span>Your call:</span> ' +
          (pick.outcome === 'find' ? 'finds ' + round.target : 'reports it missing') +
          ', ' + plural(pick.count, 'comparison');
        elAsk.hidden = true;
        elSaid.hidden = false;
        elNext.hidden = false;
        elCap.innerHTML = f.html;

        if (mastered && streak >= 3) {
          elRun.className = 'run done';
          elRun.textContent = 'Three in a row — you have it: the halving is only ' +
            'safe on a sorted list.';
          elNext.textContent = 'Another anyway';
        } else {
          elRun.className = 'run';
          elRun.textContent = streak === 0
            ? 'Run reset — two more in a row from here.'
            : plural(streak, 'right') + ' in a row — ' +
              (streak === 2 ? 'one more and you have it.' : 'two more and you have it.');
          elNext.textContent = mastered ? 'Another anyway' : 'Next list';
        }
        elSr.textContent = (f.right ? 'Correct. ' : 'Incorrect. ') +
          outcomePhrase(round) + '.';
        setState();
      }

      elFind.addEventListener('click', function () { chooseOutcome('find'); });
      elMiss.addEventListener('click', function () { chooseOutcome('miss'); });
      elNums.addEventListener('click', function (e) {
        var t = e.target.closest ? e.target.closest('.num') : null;
        if (t) chooseCount(parseInt(t.dataset.n, 10));
      });
      elStrip.addEventListener('click', function (e) {
        var t = e.target.closest ? e.target.closest('.cell') : null;
        if (!t || committed) return;
        var k = parseInt(t.dataset.i, 10);
        for (var j = 0; j < MAX_N; j++) { cells[j].classList.remove('tap'); }
        t.classList.add('tap');
        inspect = k;
        elRead.textContent = 'Index ' + k + ' holds ' + round.list[k] + '.';
        setState();
      });
      elGo.addEventListener('click', commit);
      elNext.addEventListener('click', function () { pos += 1; newRound(); elFind.focus(); });
      w.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape' || committed) return;
        pick = { outcome: null, count: null };
        elFind.setAttribute('aria-pressed', 'false');
        elMiss.setAttribute('aria-pressed', 'false');
        for (var k = 0; k < MAX_N; k++) { nums[k].setAttribute('aria-pressed', 'false'); }
        for (k = 0; k < MAX_N; k++) { cells[k].classList.remove('tap'); }
        elRead.textContent = 'Middle = the left-hand one when two are level.';
        inspect = null;
        refreshGo();
        setState();
      });

      newRound();
    }
  };
})();
