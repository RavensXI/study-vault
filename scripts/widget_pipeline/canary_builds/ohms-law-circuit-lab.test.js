'use strict';
const path = require('path');

let ok = 0, fail = 0, harness = 0;

function reportInvariant(text, passed, detail) {
  if (passed) {
    console.log(`PASS: ${text}`);
    ok++;
  } else {
    console.log(`FAIL: ${text}${detail ? ' [' + detail + ']' : ''}`);
    fail++;
  }
}

function harnessError(msg) {
  console.log(`HARNESS-ERROR: ${msg}`);
  harness++;
}

function safeStringify(v) {
  try { return JSON.stringify(v); } catch (e) { return String(v); }
}

function num(x) {
  return typeof x === 'number' && Number.isFinite(x);
}

function finish() {
  console.log(`RESULT ok=${ok} fail=${fail} harness=${harness}`);
  process.exit(fail > 0 ? 1 : 0);
}

function main() {
  const modPath = process.argv[2];
  if (!modPath) {
    harnessError('no module path given as argv[2]');
    finish();
    return;
  }

  let W;
  try {
    W = require(path.resolve(modPath));
  } catch (e) {
    harnessError('require of widget module failed: ' + e.message);
    finish();
    return;
  }

  if (!W || typeof W.initialState !== 'function' || typeof W.apply !== 'function' ||
      typeof W.derive !== 'function' || typeof W.regions !== 'function' ||
      typeof W.caption !== 'function') {
    harnessError('widget module missing required function(s) on exported object');
    finish();
    return;
  }

  const records = []; // {voltage, resistance, current, power, dotSpeed}
  const visited = new Set();
  let queue = [];

  let s0;
  try {
    s0 = W.initialState();
  } catch (e) {
    harnessError('initialState() threw: ' + e.message);
    finish();
    return;
  }

  queue.push(s0);

  const maxStates = 300;
  let count = 0;

  while (queue.length > 0 && count < maxStates) {
    const state = queue.shift();
    let key;
    try {
      key = JSON.stringify(state);
    } catch (e) {
      harnessError('a visited state could not be JSON-serialized: ' + e.message);
      continue;
    }
    if (visited.has(key)) continue;
    visited.add(key);
    count++;

    // derive check
    let derived;
    let deriveThrew = false;
    try {
      derived = W.derive(state);
    } catch (e) {
      fail++;
      console.log(`FAIL: derive(state) threw on a visited state [${e.message}] state=${key}`);
      deriveThrew = true;
    }

    if (!deriveThrew) {
      let derivedOk = true;
      let badDetail = '';
      if (derived && typeof derived === 'object') {
        for (const k of Object.keys(derived)) {
          const v = derived[k];
          if (v === undefined || (typeof v === 'number' && (Number.isNaN(v) || !Number.isFinite(v)))) {
            derivedOk = false;
            badDetail = `field ${k} = ${v}`;
            break;
          }
        }
      } else {
        derivedOk = false;
        badDetail = 'derive() did not return an object';
      }
      if (!derivedOk) {
        fail++;
        console.log(`FAIL: derive(state) returned invalid field [${badDetail}] state=${key}`);
      } else {
        ok++;
      }
    }

    // caption check
    try {
      const cap = W.caption(state, derived);
      if (typeof cap !== 'string' || cap.length === 0) {
        fail++;
        console.log(`FAIL: caption(state, derived) did not return non-empty string state=${key}`);
      } else {
        ok++;
      }
    } catch (e) {
      fail++;
      console.log(`FAIL: caption(state, derived) threw [${e.message}] state=${key}`);
    }

    // regions check
    let regions = [];
    try {
      const r = W.regions(state, 600, 300);
      if (!Array.isArray(r)) throw new Error('regions() did not return an array');
      regions = r;
      ok++;
    } catch (e) {
      fail++;
      console.log(`FAIL: regions(state,600,300) threw or invalid [${e.message}] state=${key}`);
      regions = [];
    }

    // record for invariant checks (best-effort; assumes state exposes voltage/resistance directly,
    // matching the control keys 'voltage' and 'resistance' per spec)
    if (derived && typeof derived === 'object' && !deriveThrew) {
      records.push({
        voltage: state ? state.voltage : undefined,
        resistance: state ? state.resistance : undefined,
        current: derived.current,
        power: derived.power,
        dotSpeed: derived.dotSpeed
      });
    }

    // gather actions
    const actions = [];
    for (const r of regions) {
      if (r && r.action !== undefined) actions.push(r.action);
    }
    if (Array.isArray(W.controls)) {
      for (const c of W.controls) {
        if (!c || c.key === undefined) continue;
        const vals = new Set();
        if (typeof c.min === 'number') vals.add(c.min);
        if (typeof c.max === 'number') vals.add(c.max);
        if (typeof c.min === 'number' && typeof c.max === 'number') vals.add((c.min + c.max) / 2);
        for (const v of vals) {
          actions.push({ t: 'set', key: c.key, v: v });
        }
      }
    }

    for (const a of actions) {
      let before;
      try {
        before = JSON.stringify(state);
      } catch (e) {
        harnessError('state could not be serialized before apply: ' + e.message);
        continue;
      }
      let newState;
      try {
        newState = W.apply(state, a);
      } catch (e) {
        fail++;
        console.log(`FAIL: apply(state, action) threw for action ${safeStringify(a)} [${e.message}] state=${key}`);
        continue;
      }
      let after;
      try {
        after = JSON.stringify(state);
      } catch (e) {
        harnessError('state could not be serialized after apply: ' + e.message);
        continue;
      }
      if (before !== after) {
        fail++;
        console.log(`FAIL: apply(state, action) mutated original state for action ${safeStringify(a)} state=${key}`);
      } else {
        ok++;
      }

      if (count < maxStates) {
        let newKey = null;
        try { newKey = JSON.stringify(newState); } catch (e) { newKey = null; }
        if (newKey !== null && !visited.has(newKey)) {
          queue.push(newState);
        }
      }
    }
  }

  // ---- Invariant checks based on collected records ----

  function forEachPair(cb) {
    for (let i = 0; i < records.length; i++) {
      for (let j = 0; j < records.length; j++) {
        if (i === j) continue;
        cb(records[i], records[j]);
      }
    }
  }

  // 1: current = voltage / resistance
  try {
    let pass = true, detail = '';
    for (const r of records) {
      if (!num(r.voltage) || !num(r.resistance) || r.resistance === 0) continue;
      const expected = r.voltage / r.resistance;
      if (!num(r.current) || Math.abs(r.current - expected) > 1e-9 + 1e-9 * Math.abs(expected)) {
        pass = false;
        detail = `voltage=${r.voltage} resistance=${r.resistance} current=${r.current} expected=${expected}`;
        break;
      }
    }
    reportInvariant('for any params, derived.current equals params.voltage / params.resistance within 1e-9', pass, detail);
  } catch (e) {
    harnessError('invariant check (current=V/R) threw: ' + e.message);
  }

  // 2: power = voltage * current
  try {
    let pass = true, detail = '';
    for (const r of records) {
      if (!num(r.voltage) || !num(r.current)) continue;
      const expected = r.voltage * r.current;
      if (!num(r.power) || Math.abs(r.power - expected) > 1e-9 + 1e-9 * Math.abs(expected)) {
        pass = false;
        detail = `voltage=${r.voltage} current=${r.current} power=${r.power} expected=${expected}`;
        break;
      }
    }
    reportInvariant('for any params, derived.power equals params.voltage * derived.current within 1e-9', pass, detail);
  } catch (e) {
    harnessError('invariant check (power=V*I) threw: ' + e.message);
  }

  // 3: increasing voltage, resistance fixed => current never decreases
  try {
    let pass = true, detail = '';
    forEachPair((a, b) => {
      if (!pass) return;
      if (!num(a.voltage) || !num(b.voltage) || !num(a.resistance) || !num(b.resistance)) return;
      if (!num(a.current) || !num(b.current)) return;
      if (Math.abs(a.resistance - b.resistance) < 1e-9 && a.voltage > b.voltage + 1e-12) {
        if (a.current < b.current - 1e-9) {
          pass = false;
          detail = `resistance=${a.resistance} v1=${b.voltage} i1=${b.current} v2=${a.voltage} i2=${a.current}`;
        }
      }
    });
    reportInvariant('increasing params.voltage while holding params.resistance fixed never decreases derived.current', pass, detail);
  } catch (e) {
    harnessError('invariant check (voltage monotonic) threw: ' + e.message);
  }

  // 4: increasing resistance, voltage fixed => current never increases
  try {
    let pass = true, detail = '';
    forEachPair((a, b) => {
      if (!pass) return;
      if (!num(a.voltage) || !num(b.voltage) || !num(a.resistance) || !num(b.resistance)) return;
      if (!num(a.current) || !num(b.current)) return;
      if (Math.abs(a.voltage - b.voltage) < 1e-9 && a.resistance > b.resistance + 1e-12) {
        if (a.current > b.current + 1e-9) {
          pass = false;
          detail = `voltage=${a.voltage} r1=${b.resistance} i1=${b.current} r2=${a.resistance} i2=${a.current}`;
        }
      }
    });
    reportInvariant('increasing params.resistance while holding params.voltage fixed never increases derived.current', pass, detail);
  } catch (e) {
    harnessError('invariant check (resistance monotonic) threw: ' + e.message);
  }

  // 5: voltage doubled, resistance fixed => current doubles
  try {
    let pass = true, detail = '';
    let found = false;
    forEachPair((a, b) => {
      if (!pass) return;
      if (!num(a.voltage) || !num(b.voltage) || !num(a.resistance) || !num(b.resistance)) return;
      if (!num(a.current) || !num(b.current)) return;
      if (Math.abs(a.resistance - b.resistance) < 1e-9 &&
          Math.abs(b.voltage - 2 * a.voltage) < 1e-9 * Math.max(1, Math.abs(a.voltage))) {
        found = true;
        const expected = 2 * a.current;
        if (Math.abs(b.current - expected) > 1e-6 * Math.max(1, Math.abs(expected))) {
          pass = false;
          detail = `v1=${a.voltage} i1=${a.current} v2=${b.voltage} i2=${b.current} expected=${expected}`;
        }
      }
    });
    reportInvariant('if params.voltage is doubled and params.resistance held fixed, derived.current doubles within 1e-6 relative tolerance',
      pass, found ? detail : (detail || 'no matching pairs found in explored state space (vacuous pass)'));
  } catch (e) {
    harnessError('invariant check (voltage doubling) threw: ' + e.message);
  }

  // 6: resistance doubled, voltage fixed => current halved
  try {
    let pass = true, detail = '';
    let found = false;
    forEachPair((a, b) => {
      if (!pass) return;
      if (!num(a.voltage) || !num(b.voltage) || !num(a.resistance) || !num(b.resistance)) return;
      if (!num(a.current) || !num(b.current)) return;
      if (Math.abs(a.voltage - b.voltage) < 1e-9 &&
          Math.abs(b.resistance - 2 * a.resistance) < 1e-9 * Math.max(1, Math.abs(a.resistance))) {
        found = true;
        const expected = a.current / 2;
        if (Math.abs(b.current - expected) > 1e-6 * Math.max(1, Math.abs(expected))) {
          pass = false;
          detail = `r1=${a.resistance} i1=${a.current} r2=${b.resistance} i2=${b.current} expected=${expected}`;
        }
      }
    });
    reportInvariant('if params.resistance is doubled and params.voltage held fixed, derived.current is halved within 1e-6 relative tolerance',
      pass, found ? detail : (detail || 'no matching pairs found in explored state space (vacuous pass)'));
  } catch (e) {
    harnessError('invariant check (resistance doubling) threw: ' + e.message);
  }

  // 7: current is 0 when voltage is 0, for any positive resistance
  try {
    let pass = true, detail = '';
    for (const r of records) {
      if (!num(r.voltage) || !num(r.resistance) || !num(r.current)) continue;
      if (Math.abs(r.voltage) < 1e-12 && r.resistance > 0) {
        if (Math.abs(r.current) > 1e-9) {
          pass = false;
          detail = `voltage=${r.voltage} resistance=${r.resistance} current=${r.current}`;
          break;
        }
      }
    }
    reportInvariant('derived.current is 0 when params.voltage is 0, for any positive params.resistance', pass, detail);
  } catch (e) {
    harnessError('invariant check (zero voltage) threw: ' + e.message);
  }

  // 8: dotSpeed non-negative monotonic function of current
  try {
    let pass = true, detail = '';
    for (const r of records) {
      if (num(r.dotSpeed) && r.dotSpeed < -1e-9) {
        pass = false;
        detail = `dotSpeed=${r.dotSpeed} is negative`;
        break;
      }
    }
    if (pass) {
      forEachPair((a, b) => {
        if (!pass) return;
        if (!num(a.current) || !num(b.current) || !num(a.dotSpeed) || !num(b.dotSpeed)) return;
        if (a.current >= b.current + 1e-9