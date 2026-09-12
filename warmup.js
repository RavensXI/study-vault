/* svWarmup — the "Warm up · 10 quick questions" step both dashboards promise
   in the day-one plan. An overlay quiz built from the student's own lessons:
   knowledge checks drawn from the unit each subject is currently in, up to the
   lesson they're about to do — so it's retrieval for studied material and a
   level-finder for untouched subjects.

   Depends on dash-data.js globals: SUPA, ANON, DONE, doneIn.
   API:  svWarmup.open({subjects, target, nav})   // target = today's lesson URL
         svWarmup.doneToday() -> {correct,total} | null
   Never traps the student: fetch failure or a thin question pool (<4) just
   navigates straight to the lesson, same as before the warm-up existed. */

(function () {
  var LSKEY = 'sv-warmup';
  var N_QUESTIONS = 10;
  var css = [
    '.wu-veil{position:fixed;inset:0;z-index:900;background:rgba(29,28,26,.45);display:grid;place-items:center;opacity:0;transition:opacity .25s ease}',
    '.wu-veil.in{opacity:1}',
    '.wu-card{width:min(92vw,480px);max-height:88vh;overflow:auto;background:#fff;color:#1d1c1a;border:1px solid #e6e4e0;border-radius:16px;box-shadow:0 18px 60px rgba(29,28,26,.28);padding:1.6rem 1.5rem;font-family:inherit;transform:translateY(10px);transition:transform .25s ease}',
    '.wu-veil.in .wu-card{transform:none}',
    '.wu-kick{display:flex;justify-content:space-between;align-items:baseline;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:#8a5a44}',
    '.wu-kick .wu-skip{font-weight:600;letter-spacing:0;text-transform:none;font-size:.8rem;color:#7f7c75;background:none;border:none;cursor:pointer;padding:0}',
    '.wu-kick .wu-skip:hover{color:#1d1c1a}',
    '.wu-from{font-size:.82rem;color:#7f7c75;margin:.35rem 0 1rem}',
    '.wu-q{font-size:1.12rem;line-height:1.35;margin-bottom:1.05rem}',
    '.wu-opt{display:block;width:100%;text-align:left;font-size:.95rem;background:#faf9f7;border:1px solid #e6e4e0;border-radius:11px;padding:.8rem .95rem;margin-bottom:.6rem;cursor:pointer;color:#1d1c1a;transition:border-color .15s,background .15s}',
    '.wu-opt:hover{border-color:#c9b8a4}',
    '.wu-opt.correct{border-color:#2f7d57;background:#edf6f0;color:#1e5b3e;font-weight:600}',
    '.wu-opt.wrong{border-color:#c0533a;background:#fbeee9;color:#9a3a25}',
    '.wu-dots{display:flex;gap:.35rem;margin-top:1.05rem}',
    '.wu-dots i{width:8px;height:8px;border-radius:50%;background:#e6e4e0}',
    '.wu-dots i.on{background:#8a5a44}',
    '.wu-dots i.ok{background:#2f7d57}',
    '.wu-dots i.no{background:#c0533a}',
    '.wu-sum{text-align:center;padding:.6rem 0 .2rem}',
    '.wu-sum .wu-big{font-size:2.1rem;font-weight:800}',
    '.wu-sum p{color:#54524d;font-size:.95rem;line-height:1.45;margin:.5rem auto 1.2rem;max-width:30ch}',
    '.wu-go{display:inline-block;font-weight:700;font-size:.98rem;background:#221E19;color:#faf8f5;border:none;border-radius:12px;padding:.85rem 1.5rem;cursor:pointer}',
    '.wu-go:hover{background:#3a342c}',
    '.wu-load{text-align:center;color:#7f7c75;font-size:.9rem;padding:1.4rem 0}',
    '.wu-line{display:flex;justify-content:space-between;gap:1rem;font-size:.92rem;padding:.4rem 0;border-top:1px solid #efece6}',
    '.wu-line b{color:#9a3a25;font-weight:600;white-space:nowrap}.wu-line.ok b{color:#1e5b3e}'
  ].join('\n');

  function todayStr() { return new Date().toISOString().slice(0, 10); }

  function doneToday() {
    try {
      var w = JSON.parse(localStorage.getItem(LSKEY));
      return (w && w.date === todayStr()) ? w : null;
    } catch (e) { return null; }
  }

  /* which unit is each subject "in", and up to which lesson has it been seen?
     Mirrors svContinueTarget but per-subject: first unit with an unfinished
     lesson (or the first unit), questions drawn from lessons 1..next. */
  function sources(SUBJECTS) {
    var out = [];
    (SUBJECTS || []).forEach(function (su) {
      if (!su.sub || su.mode === 'p') return;
      var unit = null, next = 1;
      if (su.units && su.units.length) {
        for (var i = 0; i < su.units.length; i++) {
          var u = su.units[i], set = u[4] || [];
          var k = 1; while (k <= u[1] && set.indexOf(k) >= 0) k++;
          if (k <= u[1]) { unit = u[3]; next = k; break; }
        }
        if (!unit) { unit = su.units[0][3]; next = 1; }
      } else if (su.first) { unit = su.first; }
      if (unit) out.push({ sub: su.sub, name: su.name, unit: unit, lte: next });
    });
    return out;
  }

  function fetchPool(SUBJECTS) {
    var srcs = sources(SUBJECTS);
    if (!srcs.length) return Promise.resolve([]);
    return Promise.all(srcs.map(function (s) {
      var url = SUPA + '/rest/v1/lessons?select=lesson_number,title,knowledge_checks,units!inner(slug,subjects!inner(slug,school_id))'
        + '&units.slug=eq.' + encodeURIComponent(s.unit)
        + '&units.subjects.slug=eq.' + encodeURIComponent(s.sub)
        + '&units.subjects.school_id=is.null'
        + '&lesson_number=lte.' + s.lte;
      return fetch(url, { headers: { apikey: ANON } })
        .then(function (r) { return r.json(); })
        .then(function (rows) {
          var qs = [];
          (rows || []).forEach(function (row) {
            (row.knowledge_checks || []).forEach(function (kc) {
              if (Array.isArray(kc.options) && typeof kc.correct === 'number' && kc.q) {
                /* authors often leave the right answer in the same slot (it was
                   very often option 2) — shuffle so position carries no signal */
                var mixed = shuffleOpts(kc.options, kc.correct);
                qs.push({ q: kc.q, opts: mixed.opts, correct: mixed.correct,
                          sub: s.sub, unit: s.unit, n: row.lesson_number,
                          title: row.title || ('Lesson ' + row.lesson_number),
                          from: s.name + ' · ' + (row.title || 'Lesson ' + row.lesson_number) });
              }
            });
          });
          return qs;
        })
        .catch(function () { return []; });
    })).then(function (per) {
      /* interleave subjects so the deck feels mixed, then cap */
      var pool = [];
      per.forEach(function (qs) { shuffle(qs); });
      for (var round = 0; pool.length < N_QUESTIONS * 2 && per.some(function (q) { return q.length; }); round++)
        per.forEach(function (qs) { if (qs.length) pool.push(qs.shift()); });
      return pool.slice(0, N_QUESTIONS);
    });
  }

  /* the revisit: every knowledge check of the given lessons, lesson by lesson (worst first, as given) */
  function fetchLessons(list) {
    var groups = {};
    (list || []).forEach(function (l) { var k = l.sub + '/' + l.unit; (groups[k] = groups[k] || { sub: l.sub, unit: l.unit, name: (l.su && l.su.name) || l.sub, ns: [] }).ns.push(l.n || l.num); });
    return Promise.all(Object.keys(groups).map(function (k) {
      var gp = groups[k];
      var url = SUPA + '/rest/v1/lessons?select=lesson_number,title,knowledge_checks,units!inner(slug,subjects!inner(slug,school_id))'
        + '&units.slug=eq.' + encodeURIComponent(gp.unit) + '&units.subjects.slug=eq.' + encodeURIComponent(gp.sub)
        + '&units.subjects.school_id=is.null&lesson_number=in.(' + gp.ns.join(',') + ')';
      return fetch(url, { headers: { apikey: ANON } }).then(function (r) { return r.json(); }).then(function (rows) {
        var by = {};
        (rows || []).forEach(function (row) {
          var qs = [];
          (row.knowledge_checks || []).forEach(function (kc) {
            if (Array.isArray(kc.options) && typeof kc.correct === 'number' && kc.q) {
              var mixed = shuffleOpts(kc.options, kc.correct);
              qs.push({ q: kc.q, opts: mixed.opts, correct: mixed.correct, sub: gp.sub, unit: gp.unit, n: row.lesson_number,
                        title: row.title || ('Lesson ' + row.lesson_number), from: gp.name + ' · ' + (row.title || 'Lesson ' + row.lesson_number) });
            }
          });
          by[row.lesson_number] = qs;
        });
        return { key: k, by: by };
      }).catch(function () { return { key: k, by: {} }; });
    })).then(function (per) {
      var lookup = {}; per.forEach(function (x) { lookup[x.key] = x.by; });
      var pool = [];
      (list || []).forEach(function (l) { var qs = (lookup[l.sub + '/' + l.unit] || {})[l.n || l.num] || []; pool = pool.concat(qs); });
      return pool;
    });
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* shuffle a question's options and report where the correct one landed.
     Options that only make sense in place ("all of the above", "both A and B",
     "none of these") are left untouched — reordering them would be wrong. */
  var POSITIONAL = /\b(all|none|both|neither)\b.*\b(above|these|apply|correct)\b|\b(a and b|b and c|a and c)\b/i;
  function shuffleOpts(opts, correct) {
    if (opts.some(function (o) { return POSITIONAL.test(String(o)); }))
      return { opts: opts, correct: correct };
    var arr = opts.map(function (o, i) { return { o: o, c: i === correct }; });
    shuffle(arr);
    var ci = 0; for (var i = 0; i < arr.length; i++) if (arr[i].c) { ci = i; break; }
    return { opts: arr.map(function (x) { return x.o; }), correct: ci };
  }

  function open(opts) {
    opts = opts || {};
    var SUBJECTS = opts.subjects || window.SUBJECTS || [];
    var nav = opts.nav || function (u) { location.href = u; };
    var target = opts.target || null;
    var REV = Array.isArray(opts.lessons);           /* the revisit slot, not the day-one warm-up */
    var LABEL = REV ? 'Revisit' : 'Warm-up';
    var goLesson = function () { close(); if (target) nav(target); };

    if (!document.getElementById('wu-style')) {
      var st = document.createElement('style'); st.id = 'wu-style'; st.textContent = css;
      document.head.appendChild(st);
    }
    var veil = document.createElement('div'); veil.className = 'wu-veil';
    veil.innerHTML = '<div class="wu-card"><div class="wu-load">' + (REV ? 'Pulling together your revisit…' : 'Pulling together your warm-up…') + '</div></div>';
    document.body.appendChild(veil);
    requestAnimationFrame(function () { veil.classList.add('in'); });
    function close() { veil.classList.remove('in'); setTimeout(function () { veil.remove(); }, 260); }
    veil.addEventListener('click', function (e) { if (e.target === veil) close(); });

    (REV ? fetchLessons(opts.lessons) : fetchPool(SUBJECTS)).then(function (pool) {
      if (pool.length < (REV ? 1 : 4)) { goLesson(); return; }   /* too thin to be worth it */
      window.__svWarmPool = pool;
      var card = veil.querySelector('.wu-card');
      var i = 0, correct = 0, locked = false, marks = [], misses = [], unitAtt = {};

      /* the revisit counts in LESSONS, like the plan row does: "Revisit · lesson 1 of 3",
         the lesson named underneath with its own question count, dots for that lesson only */
      var lkey = function (c) { return c.sub + '/' + c.unit + '/' + c.n; };
      var lessonKeys = []; pool.forEach(function (c) { var k = lkey(c); if (lessonKeys.indexOf(k) < 0) lessonKeys.push(k); });
      function renderQ() {
        var c = pool[i]; locked = false;
        var kick, from, dots;
        if (REV) {
          var k0 = lkey(c), li = lessonKeys.indexOf(k0);
          var idx = pool.map(function (x, k) { return lkey(x) === k0 ? k : -1; }).filter(function (k) { return k >= 0; });
          kick = '◆ ' + LABEL + ' · lesson ' + (li + 1) + ' of ' + lessonKeys.length;
          from = esc(c.from) + ' · ' + (idx.indexOf(i) + 1) + ' of ' + idx.length;
          dots = idx.map(function (k) { return '<i class="' + (k < i ? (marks[k] ? 'ok' : 'no') : (k === i ? 'on' : '')) + '"></i>'; }).join('');
        } else {
          kick = '◆ ' + LABEL + ' · ' + (i + 1) + ' of ' + pool.length;
          from = esc(c.from);
          dots = pool.map(function (_, k) { return '<i class="' + (k < i ? (marks[k] ? 'ok' : 'no') : (k === i ? 'on' : '')) + '"></i>'; }).join('');
        }
        card.innerHTML =
          '<div class="wu-kick"><span>' + kick + '</span>'
          + '<button class="wu-skip">Skip →</button></div>'
          + '<div class="wu-from">' + from + '</div>'
          + '<div class="wu-q">' + esc(c.q) + '</div>'
          + c.opts.map(function (o, k) { return '<button class="wu-opt" data-i="' + k + '">' + esc(o) + '</button>'; }).join('')
          + '<div class="wu-dots">' + dots + '</div>';
        card.querySelector('.wu-skip').addEventListener('click', goLesson);
        [].forEach.call(card.querySelectorAll('.wu-opt'), function (b) {
          b.addEventListener('click', function () {
            if (locked) return; locked = true;
            var ok = +b.dataset.i === c.correct;
            marks[i] = ok; if (ok) correct++;
            else misses.push({ sub: c.sub, unit: c.unit, n: c.n, title: c.title, q: (c.q || '').slice(0, 160),
              /* the CHOSEN distractor is the teacher's misconception signal —
                 "18 of 24 wrong answers picked X" beats "they got it wrong" */
              chose: String(c.opts[+b.dataset.i] || '').slice(0, 90),
              right: String(c.opts[c.correct] || '').slice(0, 90) });
            /* per-unit attempt counts — without these, unit accuracy would be
               computed from misses alone and every topic would look dire */
            var uk = (c.sub || '') + '/' + (c.unit || '');
            unitAtt[uk] = unitAtt[uk] || { a: 0, m: 0 };
            unitAtt[uk].a++; if (!ok) unitAtt[uk].m++;
            b.classList.add(ok ? 'correct' : 'wrong');
            if (!ok) card.querySelector('.wu-opt[data-i="' + c.correct + '"]').classList.add('correct');
            setTimeout(function () { (++i < pool.length) ? renderQ() : renderSummary(); }, ok ? 550 : 1100);
          });
        });
      }

      function renderSummary() {
        if (REV) { renderRevisitSummary(); return; }
        try { localStorage.setItem(LSKEY, JSON.stringify({ date: todayStr(), correct: correct, total: pool.length })); } catch (e) {}
        /* the running log is the teacher-facing record (one entry per day,
           misses carry their lesson so weaknesses aggregate by topic) */
        try {
          var lg = JSON.parse(localStorage.getItem('sv-warmup-log')) || {};
          lg[todayStr()] = { correct: correct, total: pool.length, misses: misses, units: unitAtt };
          localStorage.setItem('sv-warmup-log', JSON.stringify(lg));
        } catch (e) {}
        if (window.svProgressPushSoon) svProgressPushSoon();
        var line = correct >= pool.length * 0.8 ? 'Sharp. Today’s lesson will build on that.'
                 : correct >= pool.length * 0.5 ? 'Solid — a couple to revisit, and today’s lesson is next.'
                 : 'Good — now you know where the gaps are. The lesson fills them in.';
        card.innerHTML = '<div class="wu-kick"><span>◆ Warm-up done</span></div>'
          + '<div class="wu-sum"><div class="wu-big">' + correct + ' / ' + pool.length + '</div>'
          + '<p>' + line + '</p>'
          + (target ? '<button class="wu-go">Start today’s lesson →</button>' : '') + '</div>';
        var go = card.querySelector('.wu-go');
        if (go) go.addEventListener('click', goLesson);
        if (typeof window.svWarmupDone === 'function') try { window.svWarmupDone(); } catch (e) {}
      }

      /* the revisit writes a real quiz result per lesson (sv-kc-log), so the
         strength model resets each lesson's clock; 4/5 keeps the word it had */
      function renderRevisitSummary() {
        var per = {}, order = [];
        pool.forEach(function (c, k) {
          var key = c.sub + '/' + c.unit + '/' + c.n;
          if (!per[key]) { per[key] = { s: 0, t: 0, title: c.title, miss: [] }; order.push(key); }
          per[key].t++; if (marks[k]) per[key].s++;
        });
        misses.forEach(function (m) { var key = m.sub + '/' + m.unit + '/' + m.n; if (per[key]) per[key].miss.push({ q: m.q, chose: m.chose, right: m.right }); });
        try {
          var kclg = JSON.parse(localStorage.getItem('sv-kc-log')) || {};
          order.forEach(function (key) { kclg[key] = { s: per[key].s, t: per[key].t, d: todayStr(), miss: per[key].miss.slice(0, 5) }; });
          localStorage.setItem('sv-kc-log', JSON.stringify(kclg));
          localStorage.setItem('sv-revisit', JSON.stringify({ date: todayStr(), correct: order.filter(function (key) { return per[key].t && per[key].s / per[key].t >= 0.8; }).length, total: order.length, questions: correct, ofQuestions: pool.length,
            lessons: order.map(function (key) { return { key: key, s: per[key].s, t: per[key].t, title: per[key].title }; }) }));
        } catch (e) {}
        if (window.svProgressPushSoon) svProgressPushSoon();
        var rows = order.map(function (key) { var r = per[key], ok = r.t && r.s / r.t >= 0.8;
          return '<div class="wu-line' + (ok ? ' ok' : '') + '"><span>' + esc(r.title) + '</span><b>' + (ok ? 'still secure' : 'back in your plan') + '</b></div>'; }).join('');
        var kept = order.filter(function (key) { return per[key].t && per[key].s / per[key].t >= 0.8; }).length;
        card.innerHTML = '<div class="wu-kick"><span>◆ Revisit done</span></div>'
          + '<div class="wu-sum"><div class="wu-big">' + kept + ' / ' + order.length + '</div>' + rows
          + (target ? '<button class="wu-go">Start today’s lesson →</button>' : '<button class="wu-go">Back to my plan →</button>') + '</div>';
        var go = card.querySelector('.wu-go');
        if (go) go.addEventListener('click', target ? goLesson : close);
        if (typeof window.svWarmupDone === 'function') try { window.svWarmupDone(); } catch (e) {}
      }

      renderQ();
    }).catch(goLesson);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  window.svWarmup = { open: open, doneToday: doneToday };
})();
