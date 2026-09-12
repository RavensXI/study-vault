/* svStrength — one number per lesson, 0–100, from the retrieval the student
   has actually done, decaying with time. Everything else is a view of it:
   the RAG map is this coloured, the planner's "come back to this" is this
   dropping below a line, the flashcard strip is this per subject.

   Evidence per lesson (key "subjectSlug/unitSlug/n"):
     quiz     sv-kc-log            {s,t,d}          -> 25 + 75·(s/t), dated d
     read     sv-lessons-done/when                  -> 45, dated when it was read
     cards    sv-flashcard-progress cards lessonId:qN {box,nextReview}
              via sv-lesson-keys {lessonId: key}    -> 20 + 80·(avg box/5)
   Each piece decays by half over a half-life that grows with the number of
   retrieval events (3, 6, 12, 24, 48 days). Strength is the strongest piece
   after decay. No evidence => the RAG prior, if the student gave one.

   RAG prior (sv-welcome.rag): subject slug or "subjectSlug/unitSlug" -> 'r'|'a'|'g'
     red 10 · amber 35 · green 60. It orders the plan and picks the entry
     point (green/amber: quiz first); real retrieval overwrites it. */
(function () {
  var HALF = [3, 6, 12, 24, 48];
  var CARD_IV = [0, 1, 2, 4, 7, 14];
  function g(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function daysSince(iso) { if (!iso) return 999; var t = new Date(iso + 'T00:00:00'); return Math.max(0, (Date.now() - t) / 864e5); }
  function decay(v, d, reps) { var h = HALF[Math.min(HALF.length - 1, Math.max(0, reps - 1))]; return v * Math.pow(0.5, d / h); }
  function rag() { var w = g('sv-welcome', {}); return (w && w.rag) || {}; }
  function priorFor(slug, sub, unit) {
    var r = rag(), v = r[sub + '/' + unit] || r[slug];
    return v === 'r' || v === 'n' ? 10 : v === 'g' ? 60 : v === 'a' ? 35 : null;
  }
  function idFor(key) { var ids = g('sv-lesson-keys', {}); for (var k in ids) if (ids[k] === key) return k; return null; }
  function evidence(sub, unit, num) {
    var key = sub + '/' + unit + '/' + num, out = [];
    var kc = g('sv-kc-log', {})[key];
    if (kc && kc.t) out.push({ v: 25 + 75 * (kc.s / kc.t), d: daysSince(kc.d), kind: 'quiz' });
    var done = (g('sv-lessons-done', {})[sub + '/' + unit] || []).indexOf(num) >= 0;
    if (done) { var when = g('sv-lessons-when', {})[key]; out.push({ v: 45, d: when ? daysSince(when) : 30, kind: 'read' }); }
    /* marked exam answers (sv-practice-log): the AI's mark out of the question's marks.
       For practice-format lessons this is the only real evidence there is. */
    (g('sv-practice-log', []) || []).forEach(function (e) {
      if (!e || e.k !== key) return;
      var mm = String(e.r || '').match(/(\d+)\s*(?:\/|out of)\s*(\d+)/i); if (!mm || !+mm[2]) return;
      out.push({ v: 25 + 75 * Math.min(1, +mm[1] / +mm[2]), d: daysSince(e.d), kind: 'answer' });
    });
    var id = idFor(key);
    if (id) {
      var cards = (g('sv-flashcard-progress', { cards: {} }) || {}).cards || {}, boxes = [], last = null;
      for (var ck in cards) {
        if (ck.indexOf(id + ':') !== 0) continue;
        var c = cards[ck], box = c.box || 1; boxes.push(box);
        var lr = new Date((c.nextReview || '2000-01-01') + 'T00:00:00'); lr.setDate(lr.getDate() - CARD_IV[box]);
        var ds = Math.max(0, (Date.now() - lr) / 864e5); if (last === null || ds < last) last = ds;
      }
      if (boxes.length) { var avg = boxes.reduce(function (a, b) { return a + b; }, 0) / boxes.length; out.push({ v: 20 + 80 * (avg / 5), d: last || 0, kind: 'cards', reps: Math.max(1, Math.round(avg)) }); }
    }
    return out;
  }
  /* -> {s, prior, reps, last} */
  /* ahead: project the score N days into the future (the revisit slot looks three days out) */
  function lesson(su, unit, num, ahead) {
    var ev = evidence(su.sub, unit, num);
    if (!ev.length) { var p = priorFor(su.slug, su.sub, unit); return { s: p == null ? 0 : p, prior: p != null, reps: 0, last: null }; }
    var best = 0, reps = ev.length;
    ev.forEach(function (e) { best = Math.max(best, decay(e.v, e.d + (ahead || 0), e.reps || reps)); });
    return { s: Math.round(best), prior: false, reps: reps, last: Math.min.apply(null, ev.map(function (e) { return e.d; })) };
  }
  function band(s) { return s >= 70 ? 'g' : s >= 40 ? 'a' : 'r'; }
  function unit(su, u) { var n = u[1] || 0; if (!n) return null; var t = 0; for (var i = 1; i <= n; i++) t += lesson(su, u[3], i).s; return Math.round(t / n); }
  function subject(su) { var t = 0, c = 0; (su.units || []).forEach(function (u) { var v = unit(su, u); if (v != null) { t += v; c++; } }); return c ? Math.round(t / c) : 0; }
  /* lessons with REAL evidence whose strength has faded: due for a quick quiz */
  var REVISIT_LINE = 55;
  function due(su, limit, ahead) {
    var out = [];
    (su.units || []).forEach(function (u) {
      for (var i = 1; i <= (u[1] || 0); i++) { var r = lesson(su, u[3], i, ahead); if (!r.prior && r.reps && r.s < REVISIT_LINE) out.push({ unit: u[3], unitName: u[0], num: i, total: u[1], s: lesson(su, u[3], i).s }); }
    });
    out.sort(function (a, b) { return a.s - b.s; });
    return limit ? out.slice(0, limit) : out;
  }
  /* the revisit slot: lessons that have slipped below the line, or will within
     three days, worst first — capped per day by the budget so a month away does
     not become a wall of quizzes (20 min -> 2, 45 -> 3, 60 -> 4). Article
     lessons only: practice sets and set works have no quick quiz to come back to. */
  function revisitCap() { return Math.max(2, Math.round(budget() / 15)); }
  /* a quiz is passed with at most one wrong (4/5, 3/4), or 80% on longer sets */
  function passed(sc, t) { return t > 0 && (t <= 5 ? sc >= t - 1 : sc / t >= 0.8); }
  /* a lesson whose latest quiz was failed in the last fortnight is not re-quizzed:
     it goes back into the plan as a lesson to redo (planner.js plQueue) */
  function failedRecently(sub, unit, num) {
    var e = g('sv-kc-log', {})[sub + '/' + unit + '/' + num];
    return !!(e && e.t && daysSince(e.d) <= 14 && !passed(e.s, e.t));
  }
  function redo(su) {
    var out = [];
    (su.units || []).forEach(function (u) { (u[4] || []).forEach(function (n) { if (failedRecently(su.sub, u[3], n)) out.push({ unit: u[3], unitName: u[0], num: n, total: u[1] }); }); });
    return out;
  }
  /* days until a lesson's projected strength crosses the revisit line (null if it is already under) */
  function nextCheck(su, unit, num) {
    if (lesson(su, unit, num).s < REVISIT_LINE) return null;
    for (var d = 1; d <= 120; d++) if (lesson(su, unit, num, d).s < REVISIT_LINE) return d;
    return 120;
  }
  function revisit(subjects) {
    var all = [];
    (subjects || []).forEach(function (su) {
      if (!su.sub || su.slug === 'music') return;
      due(su, 0, 3).forEach(function (r) {
        if (window.svIsPracticeUnit && svIsPracticeUnit(su, r.unit)) return;
        if (failedRecently(su.sub, r.unit, r.num)) return;
        all.push({ su: su, sub: su.sub, unit: r.unit, unitName: r.unitName, n: r.num, num: r.num, total: r.total, s: r.s });
      });
    });
    all.sort(function (a, b) { return a.s - b.s; });
    var cap = revisitCap(), today = all.slice(0, cap);
    return { today: today, total: all.length, cap: cap, mins: today.length * 2 };
  }
  function revisitDone() { var r = g('sv-revisit', null); return (r && r.date === new Date().toISOString().slice(0, 10)) ? r : null; }
  function flashDue() {
    var cards = (g('sv-flashcard-progress', { cards: {} }) || {}).cards || {}, today = new Date().toISOString().slice(0, 10), n = 0;
    for (var k in cards) if ((cards[k].nextReview || '9999') <= today) n++;
    return n;
  }
  function setRag(key, val) {
    var w = g('sv-welcome', {}); w.rag = w.rag || {};
    if (val) w.rag[key] = val; else delete w.rag[key];
    try { localStorage.setItem('sv-welcome', JSON.stringify(w)); } catch (e) {}
    if (window.svProgressPushSoon) svProgressPushSoon();
  }
  function budget() { var w = g('sv-welcome', {}); return (w && +w.budget) || 45; }
  function setBudget(m) { var w = g('sv-welcome', {}); w.budget = m; try { localStorage.setItem('sv-welcome', JSON.stringify(w)); } catch (e) {} if (window.svProgressPushSoon) svProgressPushSoon(); }
  window.svStrength = { lesson: lesson, unit: unit, subject: subject, band: band, due: due, flashDue: flashDue, revisit: revisit, revisitDone: revisitDone, revisitCap: revisitCap, passed: passed, failedRecently: failedRecently, redo: redo, nextCheck: nextCheck,
                        rag: rag, setRag: setRag, prior: priorFor, budget: budget, setBudget: setBudget };
})();
