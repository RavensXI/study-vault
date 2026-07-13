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
    '.wu-load{text-align:center;color:#7f7c75;font-size:.9rem;padding:1.4rem 0}'
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
              if (Array.isArray(kc.options) && typeof kc.correct === 'number' && kc.q)
                qs.push({ q: kc.q, opts: kc.options, correct: kc.correct,
                          from: s.name + ' · ' + (row.title || 'Lesson ' + row.lesson_number) });
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

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function open(opts) {
    opts = opts || {};
    var SUBJECTS = opts.subjects || window.SUBJECTS || [];
    var nav = opts.nav || function (u) { location.href = u; };
    var target = opts.target || null;
    var goLesson = function () { close(); if (target) nav(target); };

    if (!document.getElementById('wu-style')) {
      var st = document.createElement('style'); st.id = 'wu-style'; st.textContent = css;
      document.head.appendChild(st);
    }
    var veil = document.createElement('div'); veil.className = 'wu-veil';
    veil.innerHTML = '<div class="wu-card"><div class="wu-load">Pulling together your warm-up…</div></div>';
    document.body.appendChild(veil);
    requestAnimationFrame(function () { veil.classList.add('in'); });
    function close() { veil.classList.remove('in'); setTimeout(function () { veil.remove(); }, 260); }
    veil.addEventListener('click', function (e) { if (e.target === veil) close(); });

    fetchPool(SUBJECTS).then(function (pool) {
      if (pool.length < 4) { goLesson(); return; }   /* too thin to be worth it */
      var card = veil.querySelector('.wu-card');
      var i = 0, correct = 0, locked = false, marks = [];

      function renderQ() {
        var c = pool[i]; locked = false;
        card.innerHTML =
          '<div class="wu-kick"><span>◆ Warm-up · ' + (i + 1) + ' of ' + pool.length + '</span>'
          + '<button class="wu-skip">Skip →</button></div>'
          + '<div class="wu-from">' + esc(c.from) + '</div>'
          + '<div class="wu-q">' + esc(c.q) + '</div>'
          + c.opts.map(function (o, k) { return '<button class="wu-opt" data-i="' + k + '">' + esc(o) + '</button>'; }).join('')
          + '<div class="wu-dots">' + pool.map(function (_, k) {
              return '<i class="' + (k < i ? (marks[k] ? 'ok' : 'no') : (k === i ? 'on' : '')) + '"></i>'; }).join('') + '</div>';
        card.querySelector('.wu-skip').addEventListener('click', goLesson);
        [].forEach.call(card.querySelectorAll('.wu-opt'), function (b) {
          b.addEventListener('click', function () {
            if (locked) return; locked = true;
            var ok = +b.dataset.i === c.correct;
            marks[i] = ok; if (ok) correct++;
            b.classList.add(ok ? 'correct' : 'wrong');
            if (!ok) card.querySelector('.wu-opt[data-i="' + c.correct + '"]').classList.add('correct');
            setTimeout(function () { (++i < pool.length) ? renderQ() : renderSummary(); }, ok ? 550 : 1100);
          });
        });
      }

      function renderSummary() {
        try { localStorage.setItem(LSKEY, JSON.stringify({ date: todayStr(), correct: correct, total: pool.length })); } catch (e) {}
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
