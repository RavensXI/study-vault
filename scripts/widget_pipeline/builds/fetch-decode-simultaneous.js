/* fetch-decode-simultaneous
   Decode is the control unit working out what the fetched instruction means.
   It writes to no register. Fetch moves the instruction in; execute moves data.
   Every value shown or marked comes from simulating the cycle, so the reveal
   cannot disagree with the marking. */
(function () {
  'use strict';

  /* ---------- the machine ---------------------------------------------- */

  var PROGRAMS = [
    { code: { 0: 'LOAD 5', 1: 'ADD 6', 2: 'STORE 7' }, data: { 5: 12, 6: 7,  7: 0  } },
    { code: { 0: 'LOAD 6', 1: 'ADD 7', 2: 'STORE 5' }, data: { 5: 0,  6: 20, 7: 9  } },
    { code: { 0: 'LOAD 7', 1: 'ADD 5', 2: 'STORE 6' }, data: { 5: 6,  6: 0,  7: 15 } },
    { code: { 0: 'LOAD 5', 1: 'ADD 7', 2: 'STORE 6' }, data: { 5: 8,  6: 0,  7: 14 } },
    { code: { 0: 'LOAD 6', 1: 'ADD 5', 2: 'STORE 7' }, data: { 5: 11, 6: 9,  7: 0  } }
  ];

  var CODE_ADDR = [0, 1, 2];
  var DATA_ADDR = [5, 6, 7];
  var REGS = ['PC', 'MAR', 'MDR', 'CIR', 'ACC'];
  var REGNAME = { PC: 'Program Counter', MAR: 'MAR', MDR: 'MDR', CIR: 'CIR', ACC: 'Accumulator' };

  function startState(prog) {
    var mem = {};
    CODE_ADDR.forEach(function (a) { mem[a] = prog.code[a]; });
    DATA_ADDR.forEach(function (a) { mem[a] = prog.data[a]; });
    return { mem: mem, PC: 0, MAR: 0, MDR: 0, CIR: prog.code[0], ACC: 0 };
  }

  function clone(s) {
    return { mem: Object.assign({}, s.mem), PC: s.PC, MAR: s.MAR,
             MDR: s.MDR, CIR: s.CIR, ACC: s.ACC };
  }

  function parseInstr(text) {
    var bits = String(text).split(' ');
    return { op: bits[0], n: parseInt(bits[1], 10) };
  }

  /* stage 1 - the instruction travels from memory into the CPU */
  function stepFetch(s) {
    var n = clone(s);
    n.MAR = n.PC;
    n.PC = n.PC + 1;
    n.MDR = n.mem[n.MAR];
    n.CIR = n.MDR;
    return { state: n, writes: ['MAR', 'PC', 'MDR', 'CIR'], memWrite: null };
  }

  /* stage 2 - the control unit interprets. Nothing is written anywhere. */
  function stepDecode(s) {
    return { state: clone(s), writes: [], memWrite: null };
  }

  /* stage 3 - now data actually moves */
  function stepExecute(s) {
    var p = parseInstr(s.CIR), n = clone(s), w = ['MAR', 'MDR'], memWrite = null;
    n.MAR = p.n;
    if (p.op === 'STORE') {
      n.MDR = n.ACC;
      n.mem[p.n] = n.MDR;
      memWrite = p.n;
    } else {
      n.MDR = n.mem[p.n];
      n.ACC = (p.op === 'LOAD') ? n.MDR : n.ACC + n.MDR;
      w.push('ACC');
    }
    return { state: n, writes: w, memWrite: memWrite };
  }

  var STEP = { fetch: stepFetch, decode: stepDecode, execute: stepExecute };

  /* run whole instructions, then stop at the boundary the question needs */
  function stateBefore(prog, k, stage) {
    var s = startState(prog), i;
    for (i = 0; i < k; i++) {
      s = stepFetch(s).state;
      s = stepDecode(s).state;
      s = stepExecute(s).state;
    }
    if (stage === 'fetch') return s;
    s = stepFetch(s).state;
    if (stage === 'decode') return s;
    return stepDecode(s).state;
  }

  /* ---------- the question bank ---------------------------------------- */

  var BANK = [
    { stage: 'decode',  reg: 'ACC', k: 1 },
    { stage: 'fetch',   reg: 'CIR', k: 2 },
    { stage: 'execute', reg: 'ACC', k: 1 },
    { stage: 'decode',  reg: 'CIR', k: 2 },
    { stage: 'fetch',   reg: 'PC',  k: 1 },
    { stage: 'execute', reg: 'MDR', k: 2 },
    { stage: 'decode',  reg: 'MDR', k: 1 },
    { stage: 'execute', reg: 'MAR', k: 1 },
    { stage: 'fetch',   reg: 'MAR', k: 2 },
    { stage: 'decode',  reg: 'PC',  k: 1 },
    { stage: 'fetch',   reg: 'MDR', k: 1 },
    { stage: 'execute', reg: 'PC',  k: 1 },
    { stage: 'decode',  reg: 'ACC', k: 2 },
    { stage: 'execute', reg: 'ACC', k: 2 }
  ];

  function disp(v) { return String(v); }

  function shuffle(list, seed) {
    var a = list.slice(), s = (seed + 7) * 9301 + 49297, i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      s = (s * 9301 + 49297) % 233280;
      j = s % (i + 1);
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function buildRound(n) {
    var q = BANK[n % BANK.length];
    var prog = PROGRAMS[n % PROGRAMS.length];
    var before = stateBefore(prog, q.k, q.stage);
    var res = STEP[q.stage](before);
    var after = res.state;

    var instr = (q.stage === 'fetch') ? before.mem[before.PC] : before.CIR;
    var p = parseInstr(instr);
    var addr = (q.stage === 'fetch') ? before.PC : before.MAR;
    var operandValue = before.mem[p.n];

    /* what the accumulator becomes once this instruction has executed */
    var afterExec = stepExecute(q.stage === 'fetch'
      ? stepDecode(stepFetch(before).state).state
      : before).state;

    var correct = disp(after[q.reg]);
    var other = CODE_ADDR.map(function (a) { return before.mem[a]; })
                         .filter(function (t) { return t !== instr; })[0];

    /* the wrong picture each question exists to falsify must be on offer */
    var must = [];
    var key = q.stage + '/' + q.reg;
    if (key === 'fetch/PC')    must = [addr];
    if (key === 'fetch/MAR')   must = [addr + 1, p.n];
    if (key === 'fetch/CIR')   must = [before.CIR, other];
    if (key === 'fetch/MDR')   must = [before.MDR, other];
    if (key === 'decode/ACC')  must = [afterExec.ACC, operandValue, p.n];
    if (key === 'decode/CIR')  must = [p.n, other];
    if (key === 'decode/MDR')  must = [operandValue, p.n];
    if (key === 'decode/PC')   must = [before.PC + 1, addr];
    if (key === 'execute/ACC') must = [operandValue, p.n, afterExec.MDR];
    if (key === 'execute/MAR') must = [before.MAR, before.PC];
    if (key === 'execute/MDR') must = [before.ACC, p.n, operandValue];
    if (key === 'execute/PC')  must = [before.PC + 1, p.n];

    var seen = {}, chipList = [];
    function add(v) {
      if (v === undefined || v === null) return;
      var t = disp(v);
      if (seen[t] || chipList.length >= 6) return;
      seen[t] = true; chipList.push(t);
    }
    add(correct);
    must.forEach(add);
    REGS.forEach(function (k2) { add(before[k2]); });
    DATA_ADDR.forEach(function (a) { add(before.mem[a]); });
    add(other);

    return {
      q: q, before: before, after: after, writes: res.writes,
      memWrite: res.memWrite, instr: instr, op: p.op, n: p.n, addr: addr,
      operandValue: operandValue, afterExec: afterExec, correct: correct,
      choices: shuffle(chipList, n)
    };
  }

  /* ---------- what the feedback says ------------------------------------ */

  function mechanism(r) {
    var key = r.q.stage + '/' + r.q.reg;
    var a = r.addr, a1 = r.addr + 1;

    if (key === 'fetch/PC')
      return 'The PC is incremented during fetch, the moment its address ' + a +
             ' is copied into the MAR. It already points at the next instruction ' +
             'while this one has not even been decoded.';
    if (key === 'fetch/MAR')
      return 'The MAR takes the address from the PC before the PC steps on, so it holds ' +
             a + ', where this instruction came from, not ' + a1 + ', where the next one lives.';
    if (key === 'fetch/CIR')
      return 'Fetch is a journey, not an understanding: PC ' + a + ' into MAR, memory[' + a +
             '] into MDR, MDR into CIR. ' + r.instr + ' has arrived in the CPU, and nothing ' +
             'has been worked out about it yet.';
    if (key === 'fetch/MDR')
      return 'Memory always answers into the MDR, which copies the instruction on to the CIR. ' +
             'After fetch both hold ' + r.instr + ': the MDR is the doorway, the CIR is the seat.';

    if (r.q.stage === 'decode') {
      var head = 'Decode writes to no register. The control unit reads ' + r.instr +
                 ' in the CIR and works out what it means — opcode ' + r.op +
                 ', operand ' + r.n + '. ';
      if (r.q.reg === 'ACC' && r.op === 'STORE')
        return head + 'STORE copies the Accumulator out to memory, so even execute leaves it ' +
               'at ' + r.before.ACC + '.';
      if (r.q.reg === 'ACC')
        return head + 'The Accumulator only changes at execute, where ' + r.before.ACC +
               ' becomes ' + r.afterExec.ACC + '.';
      if (r.q.reg === 'CIR')
        return head + 'Understanding it does not use it up: the CIR still holds it afterwards.';
      if (r.q.reg === 'MDR')
        return head + 'It reads the CIR and moves no data, so the MDR still holds what fetch left there.';
      return head + 'The PC was incremented back in fetch, so decode finds it already pointing at ' +
             r.after.PC + '.';
    }

    if (key === 'execute/ACC' && r.op === 'STORE')
      return 'Execute changed the MAR and the MDR, not the Accumulator. STORE copies ' +
             r.before.ACC + ' out to memory[' + r.n + '], overwriting the ' + r.operandValue +
             ' that was there, and the Accumulator keeps its value.';
    if (key === 'execute/ACC')
      return 'Execute is where data really moves: the MAR takes ' + r.n + ', memory[' + r.n +
             '] = ' + r.operandValue + ' comes into the MDR, then the ALU ' +
             (r.op === 'LOAD' ? 'copies it into the Accumulator.'
                              : 'adds it to the ' + r.before.ACC + ' already there.');
    if (key === 'execute/MAR')
      return 'Execute reuses the MAR for the operand address, so it now holds ' + r.n +
             ', the data address, instead of ' + r.before.MAR +
             ', where the instruction itself came from.';
    if (key === 'execute/MDR' && r.op === 'STORE')
      return 'For STORE the traffic runs the other way: the Accumulator loads the MDR with ' +
             r.before.ACC + ', the MAR takes ' + r.n + ', and memory[' + r.n + '] is overwritten.';
    if (key === 'execute/MDR')
      return 'Everything read from memory arrives in the MDR first, so it now holds the data ' +
             r.operandValue + ' from address ' + r.n + ', not the instruction it held a moment ago.';
    return 'The PC was incremented during fetch and execute never touches it, which is why the ' +
           'CPU can already be pointing at ' + r.after.PC + ' while it works on this instruction.';
  }

  function verdict(r, picked) {
    var name = REGNAME[r.q.reg];
    var held = (disp(r.before[r.q.reg]) === r.correct) ? ' still holds ' : ' holds ';
    if (picked === r.correct)
      return 'Right — the ' + name + held + r.correct + '. ' + mechanism(r);
    return 'Not quite — you said ' + picked + '; the ' + name + held + r.correct +
           '. ' + mechanism(r);
  }

  /* ---------- the widget ------------------------------------------------ */

  var CSS =
  '.svw-fdx{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;' +
    'font-size:15px;line-height:1.45;-webkit-text-size-adjust:100%}' +
  '.svw-fdx *{box-sizing:border-box}' +
  '.svw-fdx__kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;' +
    'color:var(--svw-fdx-accent);margin:0 0 .1rem}' +
  '.svw-fdx__title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.14rem;' +
    'margin:0 0 .26rem;line-height:1.2}' +
  '.svw-fdx__frame{margin:0 0 .42rem;font-size:.84rem;color:#5b564e}' +
  '.svw-fdx__stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem .5rem}' +
  '.svw-fdx__lab{font-size:.64rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;' +
    'color:#8d8880;margin:0 0 .22rem}' +
  '.svw-fdx__lab--2{margin-top:.4rem}' +
  '.svw-fdx__grid{display:grid;gap:.28rem;grid-template-columns:repeat(auto-fit,minmax(90px,1fr))}' +
  '.svw-fdx__cell{background:#fff;border:1px solid #e8e2d9;border-radius:8px;padding:.17rem .34rem;line-height:1.22}' +
  '.svw-fdx__ck{display:block;font-size:.62rem;font-weight:700;letter-spacing:.06em;color:#8d8880}' +
  '.svw-fdx__dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:4px;' +
    'background:var(--svw-fdx-accent);visibility:hidden;vertical-align:middle}' +
  '.svw-fdx__cell.is-changed .svw-fdx__dot{visibility:visible}' +
  '.svw-fdx__cell.is-changed{border-color:var(--svw-fdx-accent);background:var(--svw-fdx-tint)}' +
  '.svw-fdx__cv{display:block;font-size:.82rem;font-weight:600;font-variant-numeric:tabular-nums;' +
    'white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
  '.svw-fdx__ask{margin:.44rem 0 .28rem;font-size:.86rem}' +
  '.svw-fdx__stg{font-weight:700;letter-spacing:.04em}' +
  '.svw-fdx__chips{display:flex;flex-wrap:wrap;gap:.32rem}' +
  '.svw-fdx__chip{font:inherit;font-size:.82rem;font-weight:600;font-variant-numeric:tabular-nums;' +
    'padding:.38rem .68rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;' +
    'color:#2d2a26;cursor:pointer;min-width:50px;line-height:1.2}' +
  '.svw-fdx__chip[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
  '.svw-fdx__chip.is-key{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}' +
  '.svw-fdx__chip:disabled{cursor:default}' +
  '.svw-fdx__act{display:flex;flex-wrap:wrap;align-items:center;gap:.45rem;margin:.44rem 0 0}' +
  '.svw-fdx__btn{font:inherit;font-size:.82rem;font-weight:600;padding:.48rem .95rem;' +
    'border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}' +
  '.svw-fdx__btn:disabled{background:#faf8f5;color:#a6a099;border-color:#ddd7cd;cursor:default}' +
  '.svw-fdx__btn--quiet{background:#faf8f5;color:#2d2a26;border-color:#ddd7cd}' +
  '.svw-fdx__run{font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}' +
  '.svw-fdx__cap{margin:.34rem 0 0;font-size:.84rem;line-height:1.45;min-height:38px}' +
  '.svw-fdx__sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
    'clip-path:inset(50%);white-space:nowrap;margin:0}' +
  '@media (max-width:440px){.svw-fdx__grid{grid-template-columns:repeat(auto-fit,minmax(82px,1fr))}}';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      getComputedStyle(root).getPropertyValue('--accent').trim() || '#8a6a4f';

    root.className = (root.className ? root.className + ' ' : '') + 'svw-fdx';
    root.style.setProperty('--svw-fdx-accent', accent);
    root.style.setProperty('--svw-fdx-tint', accent + '1f');

    var style = document.createElement('style');
    style.textContent = CSS;
    root.appendChild(style);

    root.appendChild(el('p', 'svw-fdx__kick', 'Fetch · decode · execute'));
    root.appendChild(el('h3', 'svw-fdx__title', 'Which stage changes what?'));
    root.appendChild(el('p', 'svw-fdx__frame',
      'A short program is running in memory. The panel shows the CPU part-way through it.'));

    var stage = el('div', 'svw-fdx__stage');
    var memLab = el('p', 'svw-fdx__lab', 'Memory');
    stage.appendChild(memLab);
    var memGrid = el('div', 'svw-fdx__grid');
    stage.appendChild(memGrid);
    var regLab = el('p', 'svw-fdx__lab svw-fdx__lab--2', 'Registers');
    stage.appendChild(regLab);
    var regGrid = el('div', 'svw-fdx__grid');
    stage.appendChild(regGrid);
    root.appendChild(stage);

    function makeCell(parent, label) {
      var c = el('div', 'svw-fdx__cell');
      var k = el('span', 'svw-fdx__ck');
      k.appendChild(el('span', 'svw-fdx__dot'));
      k.appendChild(document.createTextNode(label));
      var v = el('span', 'svw-fdx__cv', '');
      c.appendChild(k); c.appendChild(v);
      parent.appendChild(c);
      return { cell: c, val: v };
    }

    var memCells = {}, regCells = {};
    CODE_ADDR.concat(DATA_ADDR).forEach(function (a) {
      memCells[a] = makeCell(memGrid, String(a));
    });
    REGS.forEach(function (rg) { regCells[rg] = makeCell(regGrid, rg); });

    var ask = el('p', 'svw-fdx__ask');
    var askStage = el('span', 'svw-fdx__stg');
    var askRest = document.createTextNode('');
    ask.appendChild(document.createTextNode('Stage: '));
    ask.appendChild(askStage);
    ask.appendChild(askRest);
    root.appendChild(ask);

    var chipWrap = el('div', 'svw-fdx__chips');
    root.appendChild(chipWrap);
    var chips = [];
    for (var i = 0; i < 6; i++) {
      var b = el('button', 'svw-fdx__chip');
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      chipWrap.appendChild(b);
      chips.push(b);
      (function (btn) {
        btn.addEventListener('click', function () { pick(btn.textContent); });
      })(b);
    }

    var act = el('div', 'svw-fdx__act');
    var checkBtn = el('button', 'svw-fdx__btn', 'Check');
    checkBtn.type = 'button';
    checkBtn.disabled = true;
    var nextBtn = el('button', 'svw-fdx__btn svw-fdx__btn--quiet', 'Next');
    nextBtn.type = 'button';
    nextBtn.hidden = true;
    nextBtn.disabled = true;
    var run = el('span', 'svw-fdx__run', '');
    act.appendChild(checkBtn);
    act.appendChild(nextBtn);
    act.appendChild(run);
    root.appendChild(act);

    var cap = el('p', 'svw-fdx__cap', '');
    cap.setAttribute('aria-live', 'polite');
    root.appendChild(cap);

    var sr = el('p', 'svw-fdx__sr', '');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---- state ---- */
    var roundNo = 0, r = null, picked = null, committed = false;
    var streak = 0, mastered = false, attempted = 0;

    function publish(correct) {
      root.dataset.svState = JSON.stringify({
        streak: streak, mastered: mastered, attempted: attempted,
        stage: r ? r.q.stage : null, register: r ? r.q.reg : null,
        picked: picked, expected: r ? r.correct : null,
        correct: (correct === undefined) ? null : correct
      });
    }

    function paintState(s, writes, memWrite) {
      CODE_ADDR.concat(DATA_ADDR).forEach(function (a) {
        memCells[a].val.textContent = disp(s.mem[a]);
        memCells[a].cell.classList.toggle('is-changed', memWrite === a);
      });
      REGS.forEach(function (rg) {
        regCells[rg].val.textContent = disp(s[rg]);
        regCells[rg].cell.classList.toggle('is-changed', writes.indexOf(rg) !== -1);
      });
    }

    function runLine() {
      if (mastered) return 'Mastered';
      if (streak === 0) return '';
      return streak + ' right in a row — ' + (3 - streak) + ' more';
    }

    function newRound() {
      r = buildRound(roundNo);
      roundNo++;
      picked = null;
      committed = false;
      paintState(r.before, [], null);
      askStage.textContent = r.q.stage.toUpperCase();
      askRest.nodeValue = ' — what does the ' + REGNAME[r.q.reg] +
        ' hold when this stage ends?';
      chips.forEach(function (btn, idx) {
        var v = r.choices[idx];
        btn.hidden = (v === undefined);
        btn.disabled = (v === undefined);
        btn.textContent = (v === undefined) ? '' : v;
        btn.setAttribute('aria-pressed', 'false');
        btn.classList.remove('is-key');
      });
      checkBtn.hidden = false;
      checkBtn.disabled = true;
      nextBtn.hidden = true;
      nextBtn.disabled = true;
      cap.textContent = '';
      memLab.textContent = 'Memory';
      regLab.textContent = 'Registers';
      run.textContent = runLine();
      publish();
    }

    function pick(v) {
      if (committed) return;
      picked = v;
      chips.forEach(function (btn) {
        btn.setAttribute('aria-pressed', String(!btn.hidden && btn.textContent === v));
      });
      checkBtn.disabled = false;
      publish();
    }

    function commit() {
      if (committed || picked === null) return;
      committed = true;
      attempted++;
      var right = (picked === r.correct);
      streak = right ? streak + 1 : 0;
      var justMastered = right && streak >= 3 && !mastered;
      if (right && streak >= 3) mastered = true;

      paintState(r.after, r.writes, r.memWrite);
      chips.forEach(function (btn) {
        btn.disabled = true;
        if (!btn.hidden && btn.textContent === r.correct) btn.classList.add('is-key');
      });

      regLab.textContent = 'Registers · ' + r.q.stage + ' changed ' +
        (r.writes.length ? r.writes.join(' ') : 'nothing');
      if (r.memWrite !== null)
        memLab.textContent = 'Memory · execute overwrote ' + r.memWrite;

      var text = verdict(r, picked);
      if (justMastered) {
        text += ' Three in a row — you have it: fetch moves the instruction in, decode ' +
                'only works out what it means, execute moves the data.';
      }
      cap.textContent = text;
      sr.textContent = (r.writes.length
        ? 'This stage wrote to ' + r.writes.join(', ') + '. '
        : 'This stage wrote to no register. ') + text;
      run.textContent = mastered ? 'Mastered'
        : (right ? runLine() : 'Run reset — back to 0');
      checkBtn.hidden = true;
      checkBtn.disabled = true;
      nextBtn.hidden = false;
      nextBtn.disabled = false;
      nextBtn.textContent = mastered ? 'Another anyway' : 'Next';
      publish(right);
      nextBtn.focus();
    }

    checkBtn.addEventListener('click', commit);
    nextBtn.addEventListener('click', function () {
      newRound();
      for (var j = 0; j < chips.length; j++) {
        if (!chips[j].hidden) { chips[j].focus(); break; }
      }
    });

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'fetch-decode-simultaneous',
      title: 'Which stage changes what?',
      teaches: 'Decode is the control unit interpreting the instruction just fetched. It writes to no register: fetch moves the instruction into the CPU, execute moves the data.'
    },
    mount: mount
  };
})();
