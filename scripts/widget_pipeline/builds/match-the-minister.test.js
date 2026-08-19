'use strict';

const path = require('path');

function fail(msg) {
  console.log('FAIL: ' + msg);
  return false;
}

function isFiniteNumber(x) {
  return typeof x === 'number' && Number.isFinite(x);
}

function checkNoBadFields(obj, ctx) {
  if (obj === undefined || obj === null) {
    return `${ctx}: result is null/undefined`;
  }
  for (const k of Object.keys(obj)) {
    const v = obj[k];
    if (v === undefined) return `${ctx}: field '${k}' is undefined`;
    if (typeof v === 'number' && !Number.isFinite(v)) {
      return `${ctx}: field '${k}' is NaN/Infinity (${v})`;
    }
  }
  return null;
}

let modPath = process.argv[2];
if (!modPath) {
  console.error('Usage: node test.js <widget-path>');
  process.exit(1);
}
modPath = path.resolve(process.cwd(), modPath);

let W;
try {
  W = require(modPath);
} catch (e) {
  console.log('FAIL: could not require widget module: ' + e.message);
  console.log('RESULT ok=0 fail=1');
  process.exit(1);
}

let ok = 0;
let failCount = 0;
function pass(msg) {
  ok++;
  console.log('PASS: ' + msg);
}
function record(cond, msg) {
  if (cond) {
    pass(msg);
  } else {
    failCount++;
    fail(msg);
  }
}

// ---- Build sweep of param combinations from controls ----
let controls = Array.isArray(W.controls) ? W.controls : [];
let usesSteps = typeof W.steps === 'function' && controls.length === 0;

function valuesForControl(c) {
  const vals = new Set();
  if (typeof c.min === 'number') vals.add(c.min);
  if (typeof c.max === 'number') vals.add(c.max);
  if (typeof c.value === 'number') vals.add(c.value);
  // toggle-like (0/1) get both booleans-as-numbers already covered by min/max
  if (typeof c.min === 'number' && typeof c.max === 'number' && typeof c.step === 'number' && c.step > 0) {
    const span = c.max - c.min;
    if (span > 0) {
      for (let f of [0.25, 0.5, 0.75]) {
        let raw = c.min + f * span;
        // snap to step
        let snapped = c.min + Math.round((raw - c.min) / c.step) * c.step;
        if (snapped < c.min) snapped = c.min;
        if (snapped > c.max) snapped = c.max;
        vals.add(snapped);
      }
    }
  }
  return Array.from(vals);
}

let paramCombos = [];

if (controls.length > 0) {
  const keys = controls.map(c => c.key);
  const valueLists = controls.map(valuesForControl);

  // cartesian product size
  let totalSize = valueLists.reduce((a, l) => a * Math.max(l.length, 1), 1);

  function buildDefault() {
    const p = {};
    for (const c of controls) p[c.key] = c.value;
    return p;
  }

  const defaultParams = buildDefault();
  paramCombos.push(defaultParams);

  // Also add identity-like assignment if it looks like assignment_i controls (for invariant coverage)
  const assignKeys = keys.filter(k => /^assignment_\d+$/.test(k));
  if (assignKeys.length === controls.length && assignKeys.length > 0) {
    const n = assignKeys.length;
    const identity = {};
    for (let i = 0; i < n; i++) identity[`assignment_${i}`] = i;
    paramCombos.push(identity);

    // a swapped mary-like and cecil-like combos (best-effort, only meaningful if n>=6)
    if (n >= 6) {
      const maryConf = Object.assign({}, identity);
      maryConf.assignment_4 = 5;
      maryConf.assignment_5 = 4;
      paramCombos.push(maryConf);

      const cecilConf = Object.assign({}, identity);
      cecilConf.assignment_0 = 2;
      cecilConf.assignment_2 = 0;
      paramCombos.push(cecilConf);

      // random permutations
      for (let t = 0; t < 10; t++) {
        const arr = [0, 1, 2, 3, 4, 5];
        for (let i = arr.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        const p = {};
        for (let i = 0; i < 6; i++) p[`assignment_${i}`] = arr[i];
        paramCombos.push(p);
      }

      // random non-permutation (with repeats) combos
      for (let t = 0; t < 10; t++) {
        const p = {};
        for (let i = 0; i < 6; i++) p[`assignment_${i}`] = Math.floor(Math.random() * 6);
        paramCombos.push(p);
      }
    }
  }

  if (totalSize <= 200) {
    // full cartesian product
    function rec(idx, cur) {
      if (idx === keys.length) {
        paramCombos.push(Object.assign({}, cur));
        return;
      }
      for (const v of valueLists[idx]) {
        cur[keys[idx]] = v;
        rec(idx + 1, cur);
      }
    }
    rec(0, {});
  } else {
    // random sampling up to 200
    for (let i = 0; i < 200; i++) {
      const p = {};
      for (let j = 0; j < keys.length; j++) {
        const list = valueLists[j];
        p[keys[j]] = list[Math.floor(Math.random() * list.length)];
      }
      paramCombos.push(p);
    }
  }

  // dedupe & cap at 200
  const seen = new Set();
  const deduped = [];
  for (const p of paramCombos) {
    const s = JSON.stringify(p);
    if (!seen.has(s)) {
      seen.add(s);
      deduped.push(p);
    }
  }
  paramCombos = deduped.slice(0, 200);
} else {
  // steps-based widget: no controls sweep possible in same way
  paramCombos = [{}];
}

// ---- Contract basics ----
let derivedResults = []; // {params, derived}
let contractOk = true;

if (typeof W.derive === 'function') {
  for (const params of paramCombos) {
    let derived;
    try {
      derived = W.derive(params);
    } catch (e) {
      contractOk = false;
      record(false, `derive() threw for params=${JSON.stringify(params)}: ${e.message}`);
      continue;
    }
    const badField = checkNoBadFields(derived, `derive(${JSON.stringify(params)})`);
    if (badField) {
      contractOk = false;
      record(false, badField);
    } else {
      record(true, `derive() ok for params=${JSON.stringify(params)}`);
    }
    derivedResults.push({ params, derived });
  }
} else if (usesSteps) {
  let steps;
  try {
    steps = W.steps({});
  } catch (e) {
    record(false, `steps() threw: ${e.message}`);
    steps = [];
  }
  if (!Array.isArray(steps)) {
    record(false, 'steps() did not return an array');
  } else {
    for (const s of steps) {
      const badField = checkNoBadFields(s.state, 'steps() state');
      record(!badField, badField || 'steps() state ok');
      record(
        typeof s.caption === 'string' && s.caption.length > 0,
        'steps() caption is non-empty string'
      );
    }
  }
} else {
  record(false, 'Widget exposes neither controls+derive nor steps()');
}

// caption check (if present) for derive-based widgets
if (typeof W.caption === 'function' && derivedResults.length > 0) {
  for (const { params, derived } of derivedResults) {
    let cap;
    try {
      cap = W.caption(params, derived);
    } catch (e) {
      record(false, `caption() threw for params=${JSON.stringify(params)}: ${e.message}`);
      continue;
    }
    record(
      typeof cap === 'string' && cap.length > 0,
      `caption() non-empty string for params=${JSON.stringify(params)}`
    );
  }
}

// ---- Helper to extract assignment array from params ----
function getAssignment(params) {
  const arr = [];
  for (let i = 0; i < 6; i++) {
    arr.push(params[`assignment_${i}`]);
  }
  return arr;
}

// ---- Invariant checks (only meaningful if we have derive-based results) ----
if (derivedResults.length > 0) {
  // Invariant 1: correctCount equals count of i where assignment[i]===i
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const assignment = getAssignment(params);
      if (assignment.some(v => v === undefined)) continue;
      const expected = assignment.reduce((acc, v, i) => acc + (v === i ? 1 : 0), 0);
      if (derived.correctCount !== expected) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} expected correctCount=${expected} got=${derived.correctCount}`
        );
      }
    }
    record(
      allPass,
      'for any params.assignment, derived.correctCount equals the count of indices i in 0..5 where params.assignment[i] === i'
    );
  }

  // Invariant 2: allMatched iff correctCount === 6
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const expected = derived.correctCount === 6;
      if (Boolean(derived.allMatched) !== expected) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} correctCount=${derived.correctCount} allMatched=${derived.allMatched}`
        );
      }
    }
    record(allPass, 'derived.allMatched is true if and only if derived.correctCount === 6');
  }

  // Invariant 3: identity assignment => correctCount 6, allMatched true
  {
    const identity = {};
    for (let i = 0; i < 6; i++) identity[`assignment_${i}`] = i;
    let derived;
    let threw = false;
    try {
      derived = W.derive(identity);
    } catch (e) {
      threw = true;
    }
    const cond =
      !threw &&
      derived &&
      derived.correctCount === 6 &&
      Boolean(derived.allMatched) === true;
    record(
      cond,
      'when params.assignment is the identity [0,1,2,3,4,5], derived.correctCount === 6 and derived.allMatched === true'
    );
  }

  // Invariant 4: maryConfused iff assignment[4]===5 && assignment[5]===4
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const assignment = getAssignment(params);
      if (assignment.some(v => v === undefined)) continue;
      const expected = assignment[4] === 5 && assignment[5] === 4;
      if (Boolean(derived.maryConfused) !== expected) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} expected maryConfused=${expected} got=${derived.maryConfused}`
        );
      }
    }
    record(
      allPass,
      "derived.maryConfused is true if and only if params.assignment[4] === 5 and params.assignment[5] === 4"
    );
  }

  // Invariant 5: cecilRobertConfused iff assignment[0]===2 && assignment[2]===0
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const assignment = getAssignment(params);
      if (assignment.some(v => v === undefined)) continue;
      const expected = assignment[0] === 2 && assignment[2] === 0;
      if (Boolean(derived.cecilRobertConfused) !== expected) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} expected cecilRobertConfused=${expected} got=${derived.cecilRobertConfused}`
        );
      }
    }
    record(
      allPass,
      "derived.cecilRobertConfused is true if and only if params.assignment[0] === 2 and params.assignment[2] === 0"
    );
  }

  // Invariant 6: correctCount is integer between 0 and 6 inclusive
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const v = derived.correctCount;
      if (!(Number.isInteger(v) && v >= 0 && v <= 6)) {
        allPass = false;
        console.log(`  detail: params=${JSON.stringify(params)} correctCount=${v}`);
      }
    }
    record(allPass, 'derived.correctCount is always an integer between 0 and 6 inclusive');
  }

  // Invariant 7: isValidPermutation iff all distinct and each in 0..5
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      const assignment = getAssignment(params);
      if (assignment.some(v => v === undefined)) continue;
      const inRange = assignment.every(v => Number.isInteger(v) && v >= 0 && v <= 5);
      const distinct = new Set(assignment).size === assignment.length;
      const expected = inRange && distinct;
      if (Boolean(derived.isValidPermutation) !== expected) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} expected isValidPermutation=${expected} got=${derived.isValidPermutation}`
        );
      }
    }
    record(
      allPass,
      'derived.isValidPermutation is true if and only if the six values in params.assignment are all distinct and each lies in 0..5'
    );
  }

  // Invariant 8: if isValidPermutation is false, allMatched is false
  {
    let allPass = true;
    for (const { params, derived } of derivedResults) {
      if (derived.isValidPermutation === false && Boolean(derived.allMatched) !== false) {
        allPass = false;
        console.log(
          `  detail: params=${JSON.stringify(params)} isValidPermutation=false but allMatched=${derived.allMatched}`
        );
      }
    }
    record(
      allPass,
      'if derived.isValidPermutation is false, derived.allMatched is false regardless of correctCount'
    );
  }

  // Invariant 9: changing exactly one entry changes correctCount by at most 2
  {
    let allPass = true;
    const baseSamples = derivedResults.slice(0, Math.min(derivedResults.length, 30));
    for (const { params: baseParams } of baseSamples) {
      const baseAssignment = getAssignment(baseParams);
      if (baseAssignment.some(v => v === undefined)) continue;
      let baseDerived;
      try {
        baseDerived = W.derive(baseParams);
      } catch (e) {
        continue;
      }
      for (let idx = 0; idx < 6; idx++) {
        for (let newVal = 0; newVal <= 5; newVal++) {
          if (newVal === baseAssignment[idx]) continue;
          const newParams = Object.assign({}, baseParams);
          newParams[`assignment_${idx}`] = newVal;
          let newDerived;
          try {
            newDerived = W.derive(newParams);
          } catch (e) {
            continue;
          }
          const diff = Math.abs(newDerived.correctCount - baseDerived.correctCount);
          if (diff > 2) {
            allPass = false;
            console.log(
              `  detail: base=${JSON.stringify(baseParams)} changed idx=${idx} to ${newVal} diff=${diff}`
            );
          }
        }
      }
    }
    record(
      allPass,
      'changing exactly one entry of params.assignment (with the rest fixed) can change derived.correctCount by at most 2'
    );
  }
} else {
  console.log('SKIP: no derive-based results available to check invariants against.');
}

console.log(`RESULT ok=${ok} fail=${failCount}`);
process.exit(failCount === 0 ? 0 : 1);