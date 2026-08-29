'use strict';

const path = require('path');

let ok = 0, fail = 0, harness = 0;

function reportPass(msg) {
  ok++;
  console.log('PASS: ' + msg);
}
function reportFail(msg, detail) {
  fail++;
  console.log('FAIL: ' + msg + ' [' + detail + ']');
}
function reportHarness(msg) {
  harness++;
  console.log('HARNESS-ERROR: ' + msg);
}

function safeStringify(v) {
  try { return JSON.stringify(v); } catch (e) { return '<unstringifiable:' + e.message + '>'; }
}

function isBadNumber(v) {
  return typeof v === 'number' && (Number.isNaN(v) || !Number.isFinite(v));
}

function checkDeriveObj(obj, path_) {
  path_ = path_ || '';
  if (obj === null || typeof obj !== 'object') return null;
  for (const k in obj) {
    if (!Object.prototype.hasOwnProperty.call(obj, k)) continue;
    const v = obj[k];
    if (v === undefined) return path_ + k + ' is undefined';
    if (isBadNumber(v)) return path_ + k + ' is NaN/Infinity';
    if (typeof v === 'object' && v !== null) {
      const r = checkDeriveObj(v, path_ + k + '.');
      if (r) return r;
    }
  }
  return null;
}

function getParam(state, derived, key) {
  if (state && typeof state === 'object') {
    if (state.params && typeof state.params === 'object' && key in state.params) return state.params[key];
    if (key in state) return state[key];
  }
  if (derived && typeof derived === 'object' && key in derived) return derived[key];
  return undefined;
}

let W;
try {
  const modPath = path.resolve(process.cwd(), process.argv[2]);
  W = require(modPath);
} catch (e) {
  reportHarness('failed to require widget module: ' + e.message);
  console.log('RESULT ok=' + ok + ' fail=' + fail + ' harness=' + harness);
  process.exit(1);
}

// Basic shape sanity (harness-level assumptions)
try {
  if (typeof W.initialState !== 'function') throw new Error('W.initialState is not a function');
  if (typeof W.apply !== 'function') throw new Error('W.apply is not a function');
  if (typeof W.derive !== 'function') throw new Error('W.derive is not a function');
  if (typeof W.regions !== 'function') throw new Error('W.regions is not a function');
  if (typeof W.caption !== 'function') throw new Error('W.caption is not a function');
} catch (e) {
  reportHarness('widget missing required exports: ' + e.message);
  console.log('RESULT ok=' + ok + ' fail=' + fail + ' harness=' + harness);
  process.exit(1);
}

const checks = {
  noThrowDerive: { ok: true, detail: null },
  noThrowRegions: { ok: true, detail: null },
  noThrowApply: { ok: true, detail: null },
  deriveNoBadValues: { ok: true, detail: null },
  captionNonEmpty: { ok: true, detail: null },
  applyImmutable: { ok: true, detail: null }
};

let statesList = [];

try {
  let initial;
  try {
    initial = W.initialState();
  } catch (e) {
    reportHarness('W.initialState() threw: ' + e.message);
    initial = null;
  }

  if (initial !== null) {
    let queue = [initial];
    let visited = new Set();

    while (queue.length && visited.size < 300) {
      const s = queue.shift();
      let keyStr;
      try {
        keyStr = safeStringify(s);
      } catch (e) {
        continue;
      }
      if (visited.has(keyStr)) continue;
      visited.add(keyStr);

      let derived;
      try {
        derived = W.derive(s);
      } catch (e) {
        checks.noThrowDerive.ok = false;
        checks.noThrowDerive.detail = 'derive threw on state ' + keyStr + ': ' + e.message;
        continue;
      }

      const badField = checkDeriveObj(derived);
      if (badField && checks.deriveNoBadValues.ok) {
        checks.deriveNoBadValues.ok = false;
        checks.deriveNoBadValues.detail = badField + ' (state ' + keyStr + ')';
      }

      try {
        const cap = W.caption(s, derived);
        if (typeof cap !== 'string' || cap.length === 0) {
          if (checks.captionNonEmpty.ok) {
            checks.captionNonEmpty.ok = false;
            checks.captionNonEmpty.detail = 'caption returned: ' + safeStringify(cap) + ' (state ' + keyStr + ')';
          }
        }
      } catch (e) {
        if (checks.captionNonEmpty.ok) {
          checks.captionNonEmpty.ok = false;
          checks.captionNonEmpty.detail = 'caption threw: ' + e.message + ' (state ' + keyStr + ')';
        }
      }

      let regionsArr;
      try {
        regionsArr = W.regions(s, 600, 300);
        if (!Array.isArray(regionsArr)) throw new Error('regions() did not return an array');
      } catch (e) {
        if (checks.noThrowRegions.ok) {
          checks.noThrowRegions.ok = false;
          checks.noThrowRegions.detail = 'regions threw/invalid: ' + e.message + ' (state ' + keyStr + ')';
        }
        regionsArr = [];
      }

      statesList.push({ state: s, derived: derived });

      let actions = [];
      for (const r of regionsArr) {
        if (r && r.action !== undefined) actions.push(r.action);
      }
      if (Array.isArray(W.controls)) {
        for (const c of W.controls) {
          if (c && typeof c.key === 'string' && typeof c.min === 'number' && typeof c.max === 'number') {
            const midRaw = (c.min + c.max) / 2;
            const vals = new Set([c.min, c.max, midRaw]);
            for (const v of vals) {
              actions.push({ t: 'set', key: c.key, v: v });
            }
          }
        }
      }

      for (const a of actions) {
        const snapshotBefore = safeStringify(s);
        let s2;
        try {
          s2 = W.apply(s, a);
        } catch (e) {
          if (checks.noThrowApply.ok) {
            checks.noThrowApply.ok = false;
            checks.noThrowApply.detail = 'apply threw on action ' + safeStringify(a) + ': ' + e.message;
          }
          continue;
        }
        const snapshotAfter = safeStringify(s);
        if (snapshotAfter !== snapshotBefore) {
          if (checks.applyImmutable.ok) {
            checks.applyImmutable.ok = false;
            checks.applyImmutable.detail = 'state mutated by action ' + safeStringify(a);
          }
        }
        if (s2 !== undefined && s2 !== null) {
          let k2;
          try {
            k2 = safeStringify(s2);
          } catch (e) {
            continue;
          }
          if (!visited.has(k2)) queue.push(s2);
        }
      }
    }
  }
} catch (e) {
  reportHarness('unexpected harness exception during exploration: ' + e.message);
}

// Report contract-basic check results
const basicLabels = {
  noThrowDerive: 'contract: derive() never throws',
  noThrowRegions: 'contract: regions() never throws and returns array',
  noThrowApply: 'contract: apply() never throws',
  deriveNoBadValues: 'contract: derive() has no NaN/Infinity/undefined fields',
  captionNonEmpty: 'contract: caption(s, derive(s)) is a non-empty string',
  applyImmutable: 'contract: apply(s,a) does not mutate s'
};
for (const key of Object.keys(checks)) {
  const c = checks[key];
  const label = basicLabels[key];
  if (c.ok) {
    reportPass(label);
  } else {
    reportFail(label, c.detail || 'unknown');
  }
}

// Invariant definitions
function findFirstFail(states, predicate, filter) {
  for (const item of states) {
    const s = item.state, d = item.derived;
    if (filter && !filter(s, d)) continue;
    const res = predicate(s, d);
    if (res !== null && res !== undefined && res !== true) {
      return res === false ? ('state ' + safeStringify(s) + ' derived ' + safeStringify(d)) : res;
    }
  }
  return null;
}

const invariants = [
  {
    text: "when params.marriage == 0, derived.religiousRisk == 1 and derived.warRisk == 1 and derived.civilWarRiskFaction == 0 and derived.diplomaticLeverage == 0",
    fn: (states) => findFirstFail(states, (s, d) => {
      if (!(d.religiousRisk === 1 && d.warRisk === 1 && d.civilWarRiskFaction === 0 && d.diplomaticLeverage === 0)) {
        return 'state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    }, (s, d) => getParam(s, d, 'marriage') === 0)
  },
  {
    text: "when params.marriage == 1, derived.civilWarRiskFaction == 1 and derived.religiousRisk == 0 and derived.warRisk == 0 and derived.diplomaticLeverage == 0",
    fn: (states) => findFirstFail(states, (s, d) => {
      if (!(d.civilWarRiskFaction === 1 && d.religiousRisk === 0 && d.warRisk === 0 && d.diplomaticLeverage === 0)) {
        return 'state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    }, (s, d) => getParam(s, d, 'marriage') === 1)
  },
  {
    text: "when params.marriage == 2, derived.diplomaticLeverage == 1 and derived.religiousRisk == 0 and derived.warRisk == 0 and derived.civilWarRiskFaction == 0",
    fn: (states) => findFirstFail(states, (s, d) => {
      if (!(d.diplomaticLeverage === 1 && d.religiousRisk === 0 && d.warRisk === 0 && d.civilWarRiskFaction === 0)) {
        return 'state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    }, (s, d) => getParam(s, d, 'marriage') === 2)
  },
  {
    text: "when params.succession == 0, derived.plotRisk == 1 and derived.civilWarRiskSuccession == 0",
    fn: (states) => findFirstFail(states, (s, d) => {
      if (!(d.plotRisk === 1 && d.civilWarRiskSuccession === 0)) {
        return 'state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    }, (s, d) => getParam(s, d, 'succession') === 0)
  },
  {
    text: "when params.succession == 1, derived.civilWarRiskSuccession == 1 and derived.plotRisk == 0",
    fn: (states) => findFirstFail(states, (s, d) => {
      if (!(d.civilWarRiskSuccession === 1 && d.plotRisk === 0)) {
        return 'state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    }, (s, d) => getParam(s, d, 'succession') === 1)
  },
  {
    text: "for every valid params.succession value, derived.plotRisk + derived.civilWarRiskSuccession equals exactly 1, showing the succession dilemma always carries at least one risk",
    fn: (states) => findFirstFail(states, (s, d) => {
      const sum = (d.plotRisk || 0) + (d.civilWarRiskSuccession || 0);
      if (sum !== 1) {
        return 'plotRisk+civilWarRiskSuccession=' + sum + ' for state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    })
  },
  {
    text: "derived.totalRiskFlags equals derived.religiousRisk + derived.warRisk + derived.civilWarRiskFaction + derived.plotRisk + derived.civilWarRiskSuccession for every params combination",
    fn: (states) => findFirstFail(states, (s, d) => {
      const sum = (d.religiousRisk || 0) + (d.warRisk || 0) + (d.civilWarRiskFaction || 0) + (d.plotRisk || 0) + (d.civilWarRiskSuccession || 0);
      if (d.totalRiskFlags !== sum) {
        return 'totalRiskFlags=' + d.totalRiskFlags + ' but sum=' + sum + ' for state ' + safeStringify(s) + ' derived ' + safeStringify(d);
      }
      return null;
    })
  },
  {
    text: "for any fixed params.succession, derived.totalRiskFlags at params.marriage == 2 is strictly less than derived.totalRiskFlags at params.marriage == 0 and strictly less than at params.marriage == 1",
    fn: (states) => {
      const map = {};
      for (const item of states) {
        const s = item.state, d = item.derived;
        const succ = getParam(s, d, 'succession');
        const marr = getParam(s, d, 'marriage');
        if (succ === undefined || marr === undefined) continue;
        const key = String(succ) + '|' + String(marr);
        if (!(key in map)) map[key] = d.totalRiskFlags;
      }
      const succVals = new Set();
      for (const k of Object.keys(map)) {
        succVals.add(k.split('|')[0]);
      }
      for (const sv of succVals) {
        const t0 = map[sv + '|0'];
        const t1 = map[sv + '|1'];
        const t2 = map[sv + '|2'];
        if (t2 === undefined) continue;
        if (t0 !== undefined && !(t2 < t0)) {
          return 'succession=' + sv + ': totalRiskFlags(marriage=2)=' + t2 + ' not < totalRiskFlags(marriage=0)=' + t0;
        }
        if (t1 !== undefined && !(t2 < t1)) {
          return 'succession=' + sv + ': totalRiskFlags(marriage=2)=' + t2 + ' not < totalRiskFlags(marriage=1)=' + t1;
        }
      }
      return null;
    }
  },
  {
    text: "derived.diplomaticLeverage equals 1 if and only if params.marriage == 2",
    fn: (states) => findFirstFail(states, (s, d) => {
      const marr = getParam(s, d, 'marriage');
      if (marr === undefined) return null;
      const expected = (marr === 2) ? 1 : 0;
      if (d.diplomaticLeverage !== expected) {
        return 'marriage=' + marr + ' diplomaticLeverage=' + d.diplomaticLeverage + ' expected=' + expected + ' state ' + safeStringify(s);
      }
      return null;
    })
  }
];

for (const inv of invariants) {
  try {
    const detail = inv.fn(statesList);
    if (detail === null || detail === undefined) {
      reportPass(inv.text);
    } else {
      reportFail(inv.text, detail);
    }
  } catch (e) {
    reportHarness('invariant check threw for "' + inv.text + '": ' + e.message);
  }
}

console.log('RESULT ok=' + ok + ' fail=' + fail + ' harness=' + harness);
process.exit(fail === 0 ? 0 : 1);