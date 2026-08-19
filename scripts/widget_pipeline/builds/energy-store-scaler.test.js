'use strict';

const path = require('path');

const target = process.argv[2];
if (!target) {
  console.error('Usage: node test.js <widget-path>');
  process.exit(1);
}

let W;
try {
  W = require(path.resolve(target));
} catch (e) {
  console.error('FAIL: could not load widget module: ' + e.message);
  console.log('RESULT ok=0 fail=1');
  process.exit(1);
}

let ok = 0;
let fail = 0;

function record(pass, msg) {
  if (pass) {
    ok++;
    console.log('PASS: ' + msg);
  } else {
    fail++;
    console.log('FAIL: ' + msg);
  }
}

function getDerived(params) {
  if (typeof W.derive === 'function') return W.derive(params);
  if (typeof W.steps === 'function') {
    const steps = W.steps(params);
    if (!Array.isArray(steps) || steps.length === 0) {
      throw new Error('steps() returned empty/non-array result');
    }
    return steps[steps.length - 1].state;
  }
  throw new Error('widget exposes neither derive() nor steps()');
}

function getCaption(params) {
  if (typeof W.caption === 'function') return W.caption(params);
  return null;
}

function buildValues(ctrl) {
  const vals = new Set();
  const min = ctrl.min;
  const max = ctrl.max;
  const step = ctrl.step;
  const value = ctrl.value;

  if (typeof value === 'boolean') {
    return [true, false];
  }

  vals.add(min);
  vals.add(max);
  if (typeof value !== 'undefined') vals.add(value);

  for (let i = 1; i <= 3; i++) {
    let v = min + ((max - min) * i) / 4;
    if (step) v = Math.round(v / step) * step;
    v = Math.min(max, Math.max(min, v));
    vals.add(v);
  }

  return Array.from(vals);
}

const controls = Array.isArray(W.controls) ? W.controls : [];
const valueLists = controls.map(buildValues);

function cartesian(lists) {
  return lists.reduce((acc, list) => {
    const res = [];
    for (const a of acc) {
      for (const v of list) {
        res.push(a.concat([v]));
      }
    }
    return res;
  }, [[]]);
}

let total = 1;
for (const l of valueLists) total *= Math.max(l.length, 1);

let combos;
if (controls.length === 0) {
  combos = [[]];
} else if (total <= 200) {
  combos = cartesian(valueLists);
} else {
  combos = [];
  combos.push(controls.map((c) => c.value));
  for (let i = 1; i < 200; i++) {
    combos.push(valueLists.map((list) => list[Math.floor(Math.random() * list.length)]));
  }
}

function toParams(combo) {
  const p = {};
  controls.forEach((c, i) => {
    p[c.key] = combo[i];
  });
  return p;
}

// --- Contract basics ---
for (const combo of combos) {
  const params = toParams(combo);
  let derived;
  try {
    derived = getDerived(params);
  } catch (e) {
    record(false, 'contract: derive/steps threw for params=' + JSON.stringify(params) + ': ' + e.message);
    continue;
  }

  if (derived === null || typeof derived !== 'object') {
    record(false, 'contract: derived result is not an object for params=' + JSON.stringify(params));
    continue;
  }

  let fieldsOk = true;
  for (const k of Object.keys(derived)) {
    const v = derived[k];
    if (v === undefined) {
      fieldsOk = false;
      record(false, 'contract: field "' + k + '" is undefined for params=' + JSON.stringify(params));
    } else if (typeof v === 'number' && !Number.isFinite(v)) {
      fieldsOk = false;
      record(false, 'contract: field "' + k + '" is NaN/Infinity (' + v + ') for params=' + JSON.stringify(params));
    }
  }
  if (fieldsOk) {
    record(true, 'contract: derived fields are all valid for params=' + JSON.stringify(params));
  }

  let caption = null;
  try {
    caption = getCaption(params);
  } catch (e) {
    record(false, 'contract: caption() threw for params=' + JSON.stringify(params) + ': ' + e.message);
  }
  if (caption !== null) {
    if (typeof caption === 'string' && caption.length > 0) {
      record(true, 'contract: caption is a non-empty string for params=' + JSON.stringify(params));
    } else {
      record(false, 'contract: caption invalid (' + JSON.stringify(caption) + ') for params=' + JSON.stringify(params));
    }
  }

  if (typeof W.steps === 'function') {
    try {
      const steps = W.steps(params);
      if (!Array.isArray(steps)) {
        record(false, 'contract: steps() did not return an array for params=' + JSON.stringify(params));
      } else {
        let stepsOk = true;
        for (const s of steps) {
          if (!s || typeof s.caption !== 'string' || s.caption.length === 0) {
            stepsOk = false;
          }
        }
        record(stepsOk, 'contract: all steps have non-empty string captions for params=' + JSON.stringify(params));
      }
    } catch (e) {
      record(false, 'contract: steps() threw for params=' + JSON.stringify(params) + ': ' + e.message);
    }
  }
}

// --- Invariants ---
const EPS = 1e-9;

for (const combo of combos) {
  const params = toParams(combo);
  let derived;
  try {
    derived = getDerived(params);
  } catch (e) {
    continue;
  }

  const mass = params.mass;
  const height = params.height;
  const speed = params.speed;

  record(
    Math.abs(derived.gpe - mass * 10 * height) <= EPS,
    'for any params, derived.gpe equals params.mass * 10 * params.height within 1e-9 [params=' + JSON.stringify(params) + ']'
  );

  record(
    Math.abs(derived.ke - 0.5 * mass * speed * speed) <= EPS,
    'for any params, derived.ke equals 0.5 * params.mass * params.speed^2 within 1e-9 [params=' + JSON.stringify(params) + ']'
  );

  record(
    Math.abs(derived.total - (derived.ke + derived.gpe)) <= EPS,
    'for any params, derived.total equals derived.ke + derived.gpe within 1e-9 [params=' + JSON.stringify(params) + ']'
  );

  record(
    Math.abs(derived.keDoubledSpeed - 4 * derived.ke) <= EPS,
    'doubling params.speed (others fixed) makes derived.keDoubledSpeed equal 4 times the original derived.ke within 1e-9 [params=' + JSON.stringify(params) + ']'
  );

  try {
    const doubledMassParams = Object.assign({}, params, { mass: mass * 2 });
    const dm = getDerived(doubledMassParams);
    const pass = Math.abs(dm.ke - 2 * derived.ke) <= EPS && Math.abs(dm.gpe - 2 * derived.gpe) <= EPS;
    record(
      pass,
      'doubling params.mass (others fixed) exactly doubles both derived.ke and derived.gpe within 1e-9 [params=' + JSON.stringify(params) + ']'
    );
  } catch (e) {
    record(false, 'doubling params.mass invariant threw: ' + e.message);
  }

  try {
    const doubledHeightParams = Object.assign({}, params, { height: height * 2 });
    const dh = getDerived(doubledHeightParams);
    const pass = Math.abs(dh.gpe - 2 * derived.gpe) <= EPS && Math.abs(dh.ke - derived.ke) <= EPS;
    record(
      pass,
      'doubling params.height (others fixed) exactly doubles derived.gpe and leaves derived.ke unchanged within 1e-9 [params=' + JSON.stringify(params) + ']'
    );
  } catch (e) {
    record(false, 'doubling params.height invariant threw: ' + e.message);
  }

  record(
    derived.ke >= -EPS,
    'derived.ke is never negative for any non-negative params.mass and params.speed [params=' + JSON.stringify(params) + ']'
  );

  record(
    derived.gpe >= -EPS,
    'derived.gpe is never negative for any non-negative params.mass and params.height [params=' + JSON.stringify(params) + ']'
  );

  if (speed === 0) {
    record(
      derived.ke === 0,
      'if params.speed is 0 then derived.ke equals 0 exactly [params=' + JSON.stringify(params) + ']'
    );
  }

  if (height === 0) {
    record(
      derived.gpe === 0,
      'if params.height is 0 then derived.gpe equals 0 exactly [params=' + JSON.stringify(params) + ']'
    );
  }
}

console.log('RESULT ok=' + ok + ' fail=' + fail);
process.exit(fail > 0 ? 1 : 0);