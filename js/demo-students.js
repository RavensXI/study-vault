/* Demo students — a dashboard at a snapshot in time (Tom, 12 Sep 2026).
   /classic?demo=amira  (or /desk?demo=…) wipes this browser's student state and
   seeds a believable one: subjects, ratings, lessons done on real dates, quiz
   scores, flashcard boxes, the week's logs. Then reloads without the param.
   Real unit slugs and lesson ids come from Supabase, so the picture is the
   live catalogue. Personas:
     priya  — day one: rated everything, done nothing
     josh   — three weeks in, 20 min a day, confident on paper, thin evidence
     amira  — six weeks in, 45 min a day, honest ratings, some units outgrown */
(function () {
  'use strict';
  var q = new URLSearchParams(location.search), who = q.get('demo'); if (!who) return;
  var SUPA = 'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/', KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';

  /* unit rule: rag + how many lessons done + how well (strong 4-5/5, mixed 3-5, weak 2-3) + when the run started (days ago) */
  var P = {
    priya: { weeks: 0, budget: 45,
      picked: ['maths', 'lang', 'lit', 'science', 'history', 'geog'],
      boards: { maths: 'edexcel', lang: 'aqa', lit: 'aqa', science: 'aqa', history: 'aqa', geog: 'aqa' },
      topics: { history: { 0: 'america-opportunity-inequality', 1: 'conflict-tension-inter-war', 2: 'britain-health-people', 3: 'elizabethan-england' },
                lit: { 0: 'macbeth', 1: 'a-christmas-carol', 2: 'an-inspector-calls', 3: 'power-and-conflict' } },
      units: { 'maths-edexcel': { number: 'a', algebra: 'a', graphs: 'r', 'ratio-proportion': 'n', geometry: 'r', 'probability-statistics': 'n' },
               'english-language-aqa': { 'paper-1-reading': 'a', 'paper-1-writing': 'a', 'paper-2-reading': 'n', 'paper-2-writing': 'n' },
               'english-literature-aqa': { macbeth: 'r', 'a-christmas-carol': 'a', 'an-inspector-calls': 'n', 'power-and-conflict': 'r' },
               'science-aqa': { 'biology-paper-1': 'a', 'biology-paper-2': 'n', 'chemistry-paper-1': 'r', 'chemistry-paper-2': 'n', 'physics-paper-1': 'r', 'physics-paper-2': 'n', 'physics-calculations': 'r', 'chemistry-calculations': 'n', 'biology-data-skills': 'a' },
               'history-aqa': { 'america-opportunity-inequality': 'a', 'conflict-tension-inter-war': 'n', 'britain-health-people': 'n', 'elizabethan-england': 'n' },
               'geography-aqa': { 'paper-1': 'a', 'paper-2': 'n', 'geographical-skills': 'a' } } },
    josh: { weeks: 3, budget: 20,
      picked: ['maths', 'lang', 'lit', 'science', 'history'],
      boards: { maths: 'edexcel', lang: 'aqa', lit: 'aqa', science: 'aqa', history: 'aqa' },
      topics: { history: { 0: 'germany-democracy-dictatorship', 1: 'conflict-tension-east-west', 2: 'britain-power-people', 3: 'norman-england' },
                lit: { 0: 'romeo-and-juliet', 1: 'jekyll-and-hyde', 2: 'animal-farm', 3: 'power-and-conflict' } },
      units: { 'maths-edexcel': { number: ['g', 3, 'weak', 20], algebra: 'g', graphs: 'a', 'ratio-proportion': 'a', geometry: 'r', 'probability-statistics': 'n' },
               'english-language-aqa': { 'paper-1-reading': ['a', 2, 'mixed', 12], 'paper-1-writing': 'a', 'paper-2-reading': 'n', 'paper-2-writing': 'n' },
               'english-literature-aqa': { 'romeo-and-juliet': ['a', 2, 'mixed', 18], 'jekyll-and-hyde': 'n', 'animal-farm': 'a', 'power-and-conflict': 'n' },
               'science-aqa': { 'biology-paper-1': ['g', 2, 'weak', 19], 'biology-paper-2': 'n', 'chemistry-paper-1': 'a', 'chemistry-paper-2': 'n', 'physics-paper-1': 'r', 'physics-paper-2': 'n', 'physics-calculations': 'r', 'chemistry-calculations': 'n', 'biology-data-skills': 'n' },
               'history-aqa': { 'germany-democracy-dictatorship': ['a', 1, 'mixed', 15], 'conflict-tension-east-west': 'n', 'britain-power-people': 'n', 'norman-england': 'n' } } },
    amira: { weeks: 6, budget: 45,
      picked: ['maths', 'lang', 'lit', 'science', 'history', 'geog'],
      boards: { maths: 'edexcel', lang: 'aqa', lit: 'aqa', science: 'aqa', history: 'aqa', geog: 'aqa' },
      topics: { history: { 0: 'america-opportunity-inequality', 1: 'conflict-tension-inter-war', 2: 'britain-health-people', 3: 'elizabethan-england' },
                lit: { 0: 'macbeth', 1: 'a-christmas-carol', 2: 'an-inspector-calls', 3: 'power-and-conflict' } },
      units: { 'maths-edexcel': { number: ['g', 7, 'strong', 42], algebra: ['a', 6, 'mixed', 30], graphs: 'r', 'ratio-proportion': ['n', 2, 'strong', 6], geometry: 'r', 'probability-statistics': 'n' },
               'english-language-aqa': { 'paper-1-reading': ['a', 5, 'mixed', 38], 'paper-1-writing': ['a', 2, 'mixed', 9], 'paper-2-reading': 'n', 'paper-2-writing': 'n' },
               'english-literature-aqa': { macbeth: ['r', 7, 'strong', 40], 'a-christmas-carol': ['a', 3, 'mixed', 16], 'an-inspector-calls': 'a', 'power-and-conflict': ['r', 2, 'mixed', 5] },
               'science-aqa': { 'biology-paper-1': ['a', 8, 'strong', 41], 'biology-paper-2': 'n', 'chemistry-paper-1': ['r', 4, 'mixed', 24], 'chemistry-paper-2': 'n', 'physics-paper-1': ['r', 3, 'weak', 39], 'physics-paper-2': 'n', 'physics-calculations': ['r', 2, 'mixed', 20], 'chemistry-calculations': 'n', 'biology-data-skills': 'a' },
               'history-aqa': { 'america-opportunity-inequality': ['n', 6, 'strong', 36], 'conflict-tension-inter-war': ['a', 3, 'mixed', 14], 'britain-health-people': 'n', 'elizabethan-england': 'n' },
               'geography-aqa': { 'paper-1': ['a', 5, 'mixed', 33], 'paper-2': 'n', 'geographical-skills': ['a', 2, 'strong', 8] } } }
  };
  var spec = P[who]; if (!spec) { console.warn('demo: no persona ' + who); return; }

  /* deterministic pseudo-random so the same persona always looks the same */
  var seed = 7; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
  function pick(arr) { return arr[Math.floor(rnd() * arr.length)]; }
  function dayISO(ago) { var d = new Date(); d.setDate(d.getDate() - ago); return d.toISOString().slice(0, 10); }
  var SCORES = { strong: [4, 5, 5, 5, 4], mixed: [3, 4, 5, 3, 4], weak: [2, 3, 2, 3, 2] };
  var BOXES = { strong: [4, 5, 5, 4, 5], mixed: [2, 3, 4, 3, 2], weak: [1, 2, 1, 2, 1] };
  var IV = [0, 1, 2, 4, 7, 14];
  /* practice-format units carry no quiz and no flashcards: only the done stamp and marked answers */
  var PRACTICE = { 'maths-edexcel': true, 'english-language-aqa': true, 'science-aqa/physics-calculations': true, 'science-aqa/chemistry-calculations': true, 'science-aqa/biology-data-skills': true, 'geography-aqa/geographical-skills': true };
  function isPractice(sub, u) { return !!(PRACTICE[sub] || PRACTICE[sub + '/' + u]); }

  function fetchSub(sub) {
    return fetch(SUPA + 'subjects?select=slug,units(slug,name,sort_order,lessons(id,lesson_number,status))&school_id=is.null&slug=eq.' + sub + '&units.lessons.status=eq.live', { headers: { apikey: KEY } })
      .then(function (r) { return r.json(); }).then(function (rows) { return (rows[0] || {}).units || []; });
  }

  Promise.all(Object.keys(spec.units).map(fetchSub)).then(function (all) {
    var subs = Object.keys(spec.units);
    var rag = {}, done = {}, when = {}, kc = {}, keys = {}, cards = {}, flog = [], plog = [];
    subs.forEach(function (sub, si) {
      var rules = spec.units[sub], units = all[si];
      Object.keys(rules).forEach(function (uslug) {
        var rule = rules[uslug], rr = Array.isArray(rule) ? rule : [rule, 0, 'mixed', 0];
        var ragv = rr[0], n = rr[1], quality = rr[2], start = rr[3];
        rag[sub + '/' + uslug] = ragv;
        var unit = units.filter(function (u) { return u.slug === uslug; })[0]; if (!unit || !n) return;
        var lessons = (unit.lessons || []).sort(function (a, b) { return a.lesson_number - b.lesson_number; }).slice(0, n);
        done[sub + '/' + uslug] = lessons.map(function (l) { return l.lesson_number; });
        lessons.forEach(function (l, i) {
          var ago = Math.max(1, Math.round(start - (start - 1) * (i / Math.max(1, n - 1))));   /* spread from `start` days ago to yesterday */
          var key = sub + '/' + uslug + '/' + l.lesson_number, d = dayISO(ago);
          when[key] = d;
          keys[l.id] = key;
          if (isPractice(sub, uslug)) { plog.push({ d: d, k: key, q: '', m: 4, a: '', r: 'Mark: ' + ({ strong: 4, mixed: 3, weak: 1 })[quality] + '/4' }); return; }
          var s = SCORES[quality][i % 5]; kc[key] = { s: s, t: 5, d: d, miss: [] };
          for (var c = 0; c < 5; c++) {
            var box = BOXES[quality][(i + c) % 5], last = Math.max(0, ago - Math.floor(rnd() * 3));
            var nr = new Date(); nr.setDate(nr.getDate() - last + IV[box]);
            cards[l.id + ':' + c] = { box: box, nextReview: nr.toISOString().slice(0, 10), attempts: box + 1, correct: box };
          }
          if (ago <= 6) {
            for (var f = 0; f < 4; f++) flog.push({ t: Date.now() - ago * 864e5, d: d, sub: sub, unit: uslug, n: l.lesson_number, ok: quality === 'weak' ? f % 2 === 0 : f !== 3, q: '' });
            if (i % 2 === 0) plog.push({ d: d, k: key, q: '', m: 4, a: '', r: 'Mark: ' + (quality === 'weak' ? 1 : 3) + '/4' });
          }
        });
      });
    });
    /* the subject's own colour is the average of its topics, as the picker does it */
    var v = { n: 0, r: 0, a: 1, g: 2 };
    spec.picked.forEach(function (sl) {
      var sub = ({ maths: 'maths-edexcel', lang: 'english-language-aqa', lit: 'english-literature-aqa', science: 'science-aqa', history: 'history-aqa', geog: 'geography-aqa' })[sl];
      var t = 0, c = 0; for (var k in rag) if (k.indexOf(sub + '/') === 0) { t += v[rag[k]]; c++; }
      if (c) { var m = t / c; rag[sl] = m < 0.67 ? 'r' : m < 1.34 ? 'a' : 'g'; }
    });
    /* wipe this browser's student state, then seed */
    var drop = ['sv-welcome', 'sv-welcome-decision', 'sv-lessons-done', 'sv-lessons-when', 'sv-kc-log', 'sv-lesson-keys', 'sv-flashcard-progress', 'sv-flash-log', 'sv-flash-day', 'sv-practice-log', 'sv-warmup', 'sv-warmup-log', 'sv-cards-nudge', 'sv-said-now', 'sv-week-seen', 'sv-plan-skip', 'sv-plan-holidays', 'studyvault-visited'];
    drop.forEach(function (k) { localStorage.removeItem(k); });
    Object.keys(localStorage).filter(function (k) { return k.indexOf('sv_progress_') === 0 || k.indexOf('studyvault-kc-') === 0; }).forEach(function (k) { localStorage.removeItem(k); });
    localStorage.setItem('sv-welcome', JSON.stringify({ picked: spec.picked, boards: spec.boards, topics: spec.topics, meta: {}, tiers: {}, guess: {}, rag: rag, budget: spec.budget }));
    localStorage.setItem('sv-welcome-decision', '1');
    localStorage.setItem('studyvault-exam-year', '2027');
    localStorage.setItem('sv-reader-tour-v1', '1');
    localStorage.setItem('sv-lessons-done', JSON.stringify(done));
    localStorage.setItem('sv-lessons-when', JSON.stringify(when));
    localStorage.setItem('sv-kc-log', JSON.stringify(kc));
    localStorage.setItem('sv-lesson-keys', JSON.stringify(keys));
    localStorage.setItem('sv-flashcard-progress', JSON.stringify({ cards: cards, streak: { current: 0, lastStudy: null } }));
    localStorage.setItem('sv-flash-log', JSON.stringify(flog));
    localStorage.setItem('sv-practice-log', JSON.stringify(plog));
    localStorage.setItem('sv-demo-student', who);
    q.delete('demo'); var rest = q.toString();
    location.replace(location.pathname + (rest ? '?' + rest : ''));
  }).catch(function (e) { console.error('demo seed failed', e); });
})();
