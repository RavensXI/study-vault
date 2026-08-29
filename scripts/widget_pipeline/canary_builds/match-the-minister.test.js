'use strict';

const path = require('path');

let ok = 0, fail = 0, harness = 0;

function jclone(x) { return JSON.parse(JSON.stringify(x)); }
function jeq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

function printPass(text) { console.log('PASS: ' + text); ok++; }
function printFail(text, detail) { console.log('FAIL: ' + text + ' [' + detail + ']'); fail++; }
function printHarness(text) { console.log('HARNESS-ERROR: ' + text); harness++; }

function runCheck(name, fn) {
  try {
    const v = fn();
    if (v === true || (v && v.pass === true)) {
      printPass(name);
    } else {
      const detail = (v && v.detail) || 'condition false';
      printFail(name, detail);
    }
  } catch (e) {
    printHarness(name + ': ' + (e && e.message ? e.message : String(e)));
  }
}

function finishAndExit() {
  console.log('RESULT ok=' + ok + ' fail=' + fail + ' harness=' + harness);
  process.exit(fail > 0 ? 1 : 0);
}

const modPath = process.argv[2];
if (!modPath) {
  printHarness('no module path provided as argv[2]');
  finishAndExit();
}

let W;
try {
  W = require(path.resolve(modPath));
} catch (e) {
  printHarness('failed to require module: ' + e.message);
  finishAndExit();
}

const requiredFns = ['initialState', 'apply', 'derive', 'regions', 'caption'];
let missing = false;
for (const fn of requiredFns) {
  if (typeof W[fn] !== 'function') {
    printHarness('W.' + fn + ' is not a function');
    missing = true;
  }
}
if (missing) finishAndExit();

let initState;
try {
  initState = W.initialState();
} catch (e) {
  printHarness('initialState() threw: ' + e.message);
  finishAndExit();
}
if (typeof initState !== 'object' || initState === null) {
  printHarness('initialState() did not return an object');
  finishAndExit();
}

// ---------- Exploration (BFS) ----------

const regionsThrew = [];
const applyThrew = [];
const deriveThrew = [];
const captionThrew = [];
const deriveInvalidField = [];
const captionInvalid = [];
const mutationViolations = [];

const allStates = [];
const transitions = [];

function getControlActions() {
  const acts = [];
  const controls = Array.isArray(W.controls) ? W.controls : [];
  for (const c of controls) {
    if (!c || typeof c.key === 'undefined') continue;
    const min = (typeof c.min === 'number') ? c.min : 0;
    const max = (typeof c.max === 'number') ? c.max : 1;
    const mid = (min + max) / 2;
    for (const v of [min, mid, max]) {
      acts.push({ t: 'set', key: c.key, v: v });
    }
  }
  return acts;
}

try {
  const visited = new Map();
  const startKey = JSON.stringify(initState);
  visited.set(startKey, initState);
  allStates.push(initState);
  const queue = [initState];

  while (queue.length && allStates.length < 300) {
    const s = queue.shift();
    let regs;
    try {
      regs = W.regions(s, 600, 300);
    } catch (e) {
      regionsThrew.push(e.message);
      regs = [];
    }
    if (!Array.isArray(regs)) regs = [];
    const actions = [];
    for (const r of regs) {
      if (r && r.action && typeof r.action.t === 'string') actions.push(r.action);
    }
    actions.push(...getControlActions());
    actions.push({ t: 'reset' });

    for (const a of actions) {
      if (allStates.length >= 300) break;
      const before = jclone(s);
      let ns;
      try {
        ns = W.apply(s, a);
      } catch (e) {
        applyThrew.push('action=' + JSON.stringify(a) + ' err=' + e.message);
        continue;
      }
      if (!jeq(before, s)) {
        mutationViolations.push('action=' + JSON.stringify(a));
      }
      if (typeof ns !== 'object' || ns === null) {
        applyThrew.push('apply returned non-object for action=' + JSON.stringify(a));
        continue;
      }
      transitions.push({ from: s, action: a, to: ns });
      const key = JSON.stringify(ns);
      if (!visited.has(key) && allStates.length < 300) {
        visited.set(key, ns);
        allStates.push(ns);
        queue.push(ns);
      }
    }
  }
} catch (e) {
  printHarness('exploration failed: ' + (e && e.message ? e.message : String(e)));
}

// ---------- Per-state basic contract checks ----------

for (const s of allStates) {
  let d;
  try {
    d = W.derive(s);
  } catch (e) {
    deriveThrew.push(e.message);
    continue;
  }
  if (typeof d !== 'object' || d === null) {
    deriveInvalidField.push('derive did not return an object');
    continue;
  }
  for (const k in d) {
    const v = d[k];
    if (v === undefined) {
      deriveInvalidField.push('field ' + k + ' is undefined');
    } else if (typeof v === 'number' && (Number.isNaN(v) || !Number.isFinite(v))) {
      deriveInvalidField.push('field ' + k + ' is NaN/Infinity');
    }
  }
  let cap;
  try {
    cap = W.caption(s, d);
  } catch (e) {
    captionThrew.push(e.message);
    continue;
  }
  if (typeof cap !== 'string' || cap.length === 0) {
    captionInvalid.push('caption returned: ' + JSON.stringify(cap));
  }
}

// ---------- Generic contract-basics reports ----------

runCheck('apply/derive/regions never throw on visited states', () => {
  const all = regionsThrew.concat(applyThrew, deriveThrew);
  if (all.length === 0) return { pass: true };
  return { pass: false, detail: all.length + ' throws, e.g. ' + all[0] };
});

runCheck('derive(s) never returns NaN/Infinity/undefined fields', () => {
  if (deriveInvalidField.length === 0) return { pass: true };
  return { pass: false, detail: deriveInvalidField.length + ' issues, e.g. ' + deriveInvalidField[0] };
});

runCheck('caption(s, derive(s)) is always a non-empty string', () => {
  const all = captionThrew.concat(captionInvalid);
  if (all.length === 0) return { pass: true };
  return { pass: false, detail: all.length + ' issues, e.g. ' + all[0] };
});

// ---------- INVARIANTS ----------

const INV = [
  "apply(s,a) does not mutate s; it returns a new state object",
  "for every key k in s.matched, s.matched[k] equals the correctEntity of the descriptor with id k (no wrong entity is ever recorded as matched)",
  "derive(s).matchedCount equals the number of keys in s.matched, for any reachable state",
  "applying attemptMatch with a descriptor whose id is already a key in s.matched leaves state unchanged",
  "applying attemptMatch when s.selectedEntity is null leaves state unchanged",
  "a correct attemptMatch removes exactly one id from s.pool and adds exactly one entry to s.matched; an incorrect attemptMatch leaves s.pool and s.matched unchanged",
  "s.mistakes never decreases except via reset, and only increases by 1 per incorrect attemptMatch",
  "derive(s).complete is true if and only if derive(s).matchedCount equals 8",
  "selectEntity never sets s.selectedEntity to an entity whose derive(s).entityProgress value is already 2",
  "after reset, s equals initialState except possibly for the shuffled order of s.pool and s.descriptors"
];

runCheck(INV[0], () => {
  if (mutationViolations.length === 0) return { pass: true };
  return { pass: false, detail: mutationViolations.length + ' mutations detected, e.g. ' + mutationViolations[0] };
});

runCheck(INV[1], () => {
  for (const s of allStates) {
    if (!s || !s.matched) continue;
    const descs = Array.isArray(s.descriptors) ? s.descriptors : [];
    for (const k of Object.keys(s.matched)) {
      const desc = descs.find(dd => dd && dd.id === k);
      if (!desc) return { pass: false, detail: 'descriptor ' + k + ' not found in s.descriptors' };
      if (s.matched[k] !== desc.correctEntity) {
        return { pass: false, detail: 'matched[' + k + ']=' + s.matched[k] + ' but correctEntity=' + desc.correctEntity };
      }
    }
  }
  return { pass: true };
});

runCheck(INV[2], () => {
  for (const s of allStates) {
    let d;
    try { d = W.derive(s); } catch (e) { continue; }
    const cnt = s.matched ? Object.keys(s.matched).length : 0;
    if (d.matchedCount !== cnt) {
      return { pass: false, detail: 'state has ' + cnt + ' matched keys but derive.matchedCount=' + d.matchedCount };
    }
  }
  return { pass: true };
});

runCheck(INV[3], () => {
  for (const s of allStates) {
    if (!s.matched) continue;
    const keys = Object.keys(s.matched);
    if (keys.length === 0) continue;
    const descId = keys[0];
    const before = jclone(s);
    let ns;
    try {
      ns = W.apply(s, { t: 'attemptMatch', descriptor: descId });
    } catch (e) {
      return { pass: false, detail: 'apply threw: ' + e.message };
    }
    if (!jeq(before, ns)) {
      return { pass: false, detail: 'state changed when re-matching already-matched descriptor ' + descId };
    }
  }
  return { pass: true };
});

runCheck(INV[4], () => {
  for (const s of allStates) {
    if (s.selectedEntity !== null && s.selectedEntity !== undefined) continue;
    const pool = Array.isArray(s.pool) ? s.pool : [];
    if (pool.length === 0) continue;
    const descId = pool[0];
    const before = jclone(s);
    let ns;
    try {
      ns = W.apply(s, { t: 'attemptMatch', descriptor: descId });
    } catch (e) {
      return { pass: false, detail: 'apply threw: ' + e.message };
    }
    if (!jeq(before, ns)) {
      return { pass: false, detail: 'state changed despite null selectedEntity' };
    }
  }
  return { pass: true };
});

runCheck(INV[5], () => {
  for (const s of allStates) {
    if (s.selectedEntity === null || s.selectedEntity === undefined) continue;
    const pool = Array.isArray(s.pool) ? s.pool : [];
    const descs = Array.isArray(s.descriptors) ? s.descriptors : [];
    for (const descId of pool) {
      const desc = descs.find(dd => dd && dd.id === descId);
      if (!desc) continue;
      const correct = desc.correctEntity === s.selectedEntity;
      let ns;
      try {
        ns = W.apply(s, { t: 'attemptMatch', descriptor: descId });
      } catch (e) {
        return { pass: false, detail: 'apply threw: ' + e.message };
      }
      const poolBefore = pool.length;
      const poolAfter = Array.isArray(ns.pool) ? ns.pool.length : -1;
      const matchedBefore = s.matched ? Object.keys(s.matched).length : 0;
      const matchedAfter = ns.matched ? Object.keys(ns.matched).length : 0;
      if (correct) {
        if (!(poolAfter === poolBefore - 1 && matchedAfter === matchedBefore + 1 && ns.matched && ns.matched[descId] === s.selectedEntity)) {
          return { pass: false, detail: 'correct match for ' + descId + ' did not update pool/matched as expected' };
        }
      } else {
        if (!(poolAfter === poolBefore && matchedAfter === matchedBefore)) {
          return { pass: false, detail: 'incorrect match for ' + descId + ' changed pool/matched' };
        }
      }
    }
  }
  return { pass: true };
});

runCheck(INV[6], () => {
  for (const tr of transitions) {
    const before = tr.from.mistakes;
    const after = tr.to.mistakes;
    if (typeof before !== 'number' || typeof after !== 'number') continue;
    if (tr.action.t === 'reset') continue;
    if (after < before) {
      return { pass: false, detail: 'mistakes decreased from ' + before + ' to ' + after + ' via action ' + JSON.stringify(tr.action) };
    }
    if (after > before && after !== before + 1) {
      return { pass: false, detail: 'mistakes jumped from ' + before + ' to ' + after + ' via action ' + JSON.stringify(tr.action) };
    }
  }
  return { pass: true };
});

runCheck(INV[7], () => {
  for (const s of allStates) {
    let d;
    try { d = W.derive(s); } catch (e) { continue; }
    const shouldBeComplete = d.matchedCount === 8;
    if (Boolean(d.complete) !== shouldBeComplete) {
      return { pass: false, detail: 'complete=' + d.complete + ' but matchedCount=' + d.matchedCount };
    }
  }
  return { pass: true };
});

runCheck(INV[8], () => {
  for (const s of allStates) {
    let d;
    try { d = W.derive(s); } catch (e) { continue; }
    const entities = Array.isArray(s.entities) ? s.entities : [];
    for (const ent of entities) {
      const progress = d.entityProgress ? d.entityProgress[ent] : undefined;
      if (progress === 2) {
        let ns;
        try {
          ns = W.apply(s, { t: 'selectEntity', entity: ent });
        } catch (e) {
          return { pass: false, detail: 'apply threw: ' + e.message };
        }
        if (ns.selectedEntity === ent) {
          return { pass: false, detail: 'selectedEntity was set to full entity ' + ent };
        }
      }
    }
  }
  return { pass: true };
});

runCheck(INV[9], () => {
  let init0;
  try {
    init0 = W.initialState();
  } catch (e) {
    return { pass: false, detail: 'initialState() threw: ' + e.message };
  }
  const normalize = (obj) => {
    const copy = Object.assign({}, obj);
    if (Array.isArray(copy.pool)) copy.pool = copy.pool.slice().sort();
    if (Array.isArray(copy.descriptors)) {
      copy.descriptors = copy.descriptors.slice().sort((x, y) => {
        if (x.id < y.id) return -1;
        if (x.id > y.id) return 1;
        return 0;
      });
    }
    return copy;
  };
  const bn = normalize(jclone(init0));
  for (const s of allStates) {
    let ns;
    try {
      ns = W.apply(s, { t: 'reset' });
    } catch (e) {
      return { pass: false, detail: 'apply reset threw: ' + e.message };
    }
    const an = normalize(jclone(ns));
    if (!jeq(an, bn)) {
      return { pass: false, detail: 'reset() result differs from initialState() beyond pool/descriptors ordering' };
    }
  }
  return { pass: true };
});

finishAndExit();