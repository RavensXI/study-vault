'use strict';

const path = require('path');

function main() {
  let ok = 0, fail = 0, harness = 0;

  function reportPass(text) {
    ok++;
    console.log('PASS: ' + text);
  }
  function reportFail(text, detail) {
    fail++;
    console.log('FAIL: ' + text + ' [' + detail + ']');
  }
  function reportHarness(what) {
    harness++;
    console.log('HARNESS-ERROR: ' + what);
  }

  let W;
  try {
    const modPath = path.resolve(process.cwd(), process.argv[2]);
    W = require(modPath);
  } catch (e) {
    console.log('HARNESS-ERROR: failed to require widget module: ' + (e && e.message ? e.message : String(e)));
    console.log('RESULT ok=0 fail=0 harness=1');
    process.exit(1);
  }

  function callWidget(fn, args) {
    try {
      if (typeof fn !== 'function') {
        return { ok: false, error: 'not a function' };
      }
      return { ok: true, value: fn.apply(null, args) };
    } catch (e) {
      return { ok: false, error: e && e.message ? e.message : String(e) };
    }
  }

  function deepClone(x) {
    return JSON.parse(JSON.stringify(x));
  }

  function safeStringify(x) {
    try {
      return JSON.stringify(x);
    } catch (e) {
      return null;
    }
  }

  function isBadNumber(v) {
    return typeof v === 'number' && (Number.isNaN(v) || !Number.isFinite(v));
  }

  function checkDerivedClean(derived) {
    if (derived === null || typeof derived !== 'object') return 'derive did not return an object';
    for (const k of Object.keys(derived)) {
      const v = derived[k];
      if (v === undefined) return 'field "' + k + '" is undefined';
      if (isBadNumber(v)) return 'field "' + k + '" is NaN/Infinity';
    }
    return null;
  }

  // ---------------------------------------------------------------
  // Part 1: BFS exploration + contract basics
  // ---------------------------------------------------------------

  let applyThrewDetail = null;
  let applyImpureDetail = null;
  let deriveThrewDetail = null;
  let deriveDirtyDetail = null;
  let captionBadDetail = null;
  let regionsBadDetail = null;

  let controls = [];
  try {
    controls = Array.isArray(W.controls) ? W.controls : [];
  } catch (e) {
    reportHarness('reading W.controls: ' + e.message);
    controls = [];
  }

  let visitedCount = 0;

  try {
    const visitedSet = new Set();
    const queue = [];

    const init = callWidget(W.initialState, []);
    if (!init.ok) {
      if (applyThrewDetail === null) { /* not relevant here */ }
      reportFail('W.initialState() must not throw', init.error);
    } else {
      queue.push(init.value);
    }

    while (queue.length > 0 && visitedCount < 300) {
      const s = queue.shift();
      let key;
      try {
        key = safeStringify(s);
        if (key === null) key = 'unstringifiable-' + Math.random();
      } catch (e) {
        key = 'unstringifiable-' + Math.random();
      }
      if (visitedSet.has(key)) continue;
      visitedSet.add(key);
      visitedCount++;

      let snapshotBefore;
      try {
        snapshotBefore = safeStringify(s);
      } catch (e) {
        snapshotBefore = null;
      }

      const dres = callWidget(W.derive, [s]);
      let derived = null;
      if (!dres.ok) {
        if (deriveThrewDetail === null) deriveThrewDetail = dres.error;
      } else {
        derived = dres.value;
        const cleanErr = checkDerivedClean(derived);
        if (cleanErr && deriveDirtyDetail === null) deriveDirtyDetail = cleanErr;
      }

      const capRes = callWidget(W.caption, [s, derived]);
      if (!capRes.ok) {
        if (captionBadDetail === null) captionBadDetail = 'threw: ' + capRes.error;
      } else if (typeof capRes.value !== 'string' || capRes.value.length === 0) {
        if (captionBadDetail === null) captionBadDetail = 'returned: ' + safeStringify(capRes.value);
      }

      const rres = callWidget(W.regions, [s, 600, 300]);
      let regions = [];
      if (!rres.ok) {
        if (regionsBadDetail === null) regionsBadDetail = 'threw: ' + rres.error;
      } else if (!Array.isArray(rres.value)) {
        if (regionsBadDetail === null) regionsBadDetail = 'not an array: ' + safeStringify(rres.value);
      } else {
        regions = rres.value;
      }

      const actions = [];
      for (const r of regions) {
        if (r && r.action !== undefined) actions.push(r.action);
      }
      for (const c of controls) {
        if (!c || c.key === undefined) continue;
        const mn = c.min, mx = c.max;
        let vals = [];
        if (typeof mn === 'number' && typeof mx === 'number') {
          vals = [mn, (mn + mx) / 2, mx];
        } else if (c.value !== undefined) {
          vals = [c.value];
        }
        for (const v of vals) {
          actions.push({ t: 'set', key: c.key, v: v });
        }
      }

      for (const a of actions) {
        let before;
        try {
          before = safeStringify(s);
        } catch (e) {
          before = null;
        }
        const ares = callWidget(W.apply, [s, a]);
        if (!ares.ok) {
          if (applyThrewDetail === null) applyThrewDetail = 'action=' + safeStringify(a) + ' error=' + ares.error;
          continue;
        }
        let after;
        try {
          after = safeStringify(s);
        } catch (e) {
          after = null;
        }
        if (before !== after) {
          if (applyImpureDetail === null) applyImpureDetail = 'action=' + safeStringify(a);
        }
        if (visitedCount + queue.length < 300) {
          queue.push(ares.value);
        }
      }
    }
  } catch (e) {
    reportHarness('exploration loop failed: ' + (e && e.message ? e.message : String(e)));
  }

  // Aggregate contract-basic results
  if (applyThrewDetail) {
    reportFail('W.apply(state, action) must not throw', applyThrewDetail);
  } else {
    reportPass('W.apply(state, action) never throws during exploration');
  }

  if (applyImpureDetail) {
    reportFail('W.apply(state, action) must not mutate its input state', applyImpureDetail);
  } else {
    reportPass('W.apply(state, action) does not mutate its input state');
  }

  if (deriveThrewDetail) {
    reportFail('W.derive(state) must not throw', deriveThrewDetail);
  } else {
    reportPass('W.derive(state) never throws during exploration');
  }

  if (deriveDirtyDetail) {
    reportFail('W.derive(state) fields must be finite numbers, not NaN/Infinity/undefined', deriveDirtyDetail);
  } else {
    reportPass('W.derive(state) fields are always finite (no NaN/Infinity/undefined)');
  }

  if (captionBadDetail) {
    reportFail('W.caption(state, derived) must return a non-empty string', captionBadDetail);
  } else {
    reportPass('W.caption(state, derived) always returns a non-empty string');
  }

  if (regionsBadDetail) {
    reportFail('W.regions(state, w, h) must not throw and must return an array', regionsBadDetail);
  } else {
    reportPass('W.regions(state, w, h) never throws and always returns an array');
  }

  // ---------------------------------------------------------------
  // Part 2: invariant checks using systematic parameter combinations
  // ---------------------------------------------------------------

  function getControlValues(keyName, fallback) {
    try {
      const c = controls.find(x => x && x.key === keyName);
      if (c && typeof c.min === 'number' && typeof c.max === 'number' && typeof c.step === 'number' && c.step > 0) {
        const vals = [];
        for (let v = c.min; v <= c.max + 1e-9; v += c.step) {
          vals.push(Math.round(v * 1e6) / 1e6);
        }
        if (vals.length > 0) return vals;
      }
    } catch (e) {
      reportHarness('reading control spec for ' + keyName + ': ' + e.message);
    }
    return fallback.slice();
  }

  const loftValues = getControlValues('loftThickness', [0, 50, 100, 150, 200, 250, 300]);
  const wallValues = getControlValues('wallChoice', [0, 1, 2]);
  const glazeValues = getControlValues('glazingChoice', [0, 1]);

  const comboCache = new Map();

  function