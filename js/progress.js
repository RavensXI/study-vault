/* Progress, in words — retrieval-strength branch (Tom, 12 Sep 2026).
   Students should see themselves getting better, not how busy they have been.
   Four things, all read from the strength model (js/strength.js) and the
   planner's fit (planner.js):
     counts(su)   -> {secure, developing, due, notyet, total, done}   the subject headline
                     bands are the school words (emerging / developing / secure); decay is not a band
                     but a prompt — a lesson with evidence below the revisit line counts as "due a revisit"
     track(su)    -> 'on track for 11 May' | '≈ 6 lessons behind schedule' | null
     saidNow(...) -> "Good progress on Cells — developing now."   said only when the evidence beats their own rating
     week()       -> the last seven days, and lastWeek() for the first visit of a new week
   Tone: say what happened, name the topic, use their words. Never speak when
   nothing changed, never negative, no streaks, no badges. */
(function () {
  'use strict';
  function g(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function today() { return new Date().toISOString().slice(0, 10); }
  var SAID = { n: 'not started', r: 'struggling', a: 'getting there', g: 'confident' };
  var NOW = { r: 'emerging', a: 'developing', g: 'secure' };
  var REVISIT = 55;   /* the planner's due line (js/strength.js due()) */
  var RANK_SAID = { n: 0, r: 0, a: 1, g: 2 }, RANK_NOW = { r: 0, a: 1, g: 2 };

  /* one lesson: {s, prior, reps} from the strength model */
  function L(su, unit, n) { return window.svStrength ? svStrength.lesson(su, unit, n) : { s: 0, prior: true, reps: 0 }; }

  function counts(su) {
    var c = { secure: 0, developing: 0, due: 0, notyet: 0, total: 0, done: 0 };
    (su.units || []).forEach(function (u) {
      c.total += u[1] || 0; c.done += u[2] || 0;
      for (var n = 1; n <= (u[1] || 0); n++) {
        var r = L(su, u[3], n);
        if (r.prior || !r.reps) { c.notyet++; continue; }
        if (r.s < REVISIT) c.due++; else if (r.s >= 70) c.secure++; else c.developing++;
      }
    });
    return c;
  }
  /* lessons in one unit that are due a revisit */
  function dueIn(su, u) { var d = 0; for (var n = 1; n <= (u[1] || 0); n++) { var r = L(su, u[3], n); if (!r.prior && r.reps && r.s < REVISIT) d++; } return d; }
  /* the headline: only the groups that exist, "not yet" always last */
  function headline(su) {
    var c = counts(su), parts = [];
    if (c.secure) parts.push(c.secure + ' secure');
    if (c.developing) parts.push(c.developing + ' developing');
    if (c.due) parts.push('<span class="pg-due">' + c.due + ' due a revisit</span>');
    parts.push(c.notyet + ' not yet');
    return parts.join(' · ');
  }
  function shortDate(iso) {
    if (!iso) return '';
    var d = new Date(iso + (iso.length === 10 ? 'T12:00:00' : ''));
    return isNaN(d) ? '' : d.getDate() + ' ' + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()];
  }
  /* on track, quietly: from the planner's fit (lessons that fit before the first paper at the budget) */
  function track(su) {
    if (!window.svPlanFit) return null;
    var f = svPlanFit(su.slug); if (!f || !f.first) return null;
    if (!f.left) return 'nothing left before ' + shortDate(f.first);
    if (f.fit >= f.left) return 'on track for ' + shortDate(f.first);
    var behind = f.left - f.fit;
    return '≈ ' + behind + ' lesson' + (behind === 1 ? '' : 's') + ' behind schedule';
  }

  /* "you said / now": a unit whose evidence has climbed above the student's own rating.
     Needs real evidence on at least two lessons (or a quarter of the unit). Told once per
     band, kept in sv-said-now so the line stays until something newer is true. */
  /* where a unit is NOW: the evidence band once any lesson has real evidence, else null */
  function band(su, u) {
    var ev = [], n = u[1] || 0;
    for (var i = 1; i <= n; i++) { var r = L(su, u[3], i); if (!r.prior && r.reps) ev.push(r.s); }
    if (!ev.length) return null;
    var avg = ev.reduce(function (a, b) { return a + b; }, 0) / ev.length;
    return avg >= 70 ? 'g' : avg >= 40 ? 'a' : 'r';
  }
  function nowBand(su, u) {
    var ev = [], n = u[1] || 0;
    for (var i = 1; i <= n; i++) { var r = L(su, u[3], i); if (!r.prior && r.reps) ev.push(r.s); }
    if (ev.length < Math.max(2, Math.ceil(n * 0.25))) return null;
    var avg = ev.reduce(function (a, b) { return a + b; }, 0) / ev.length;
    return avg >= 70 ? 'g' : avg >= 40 ? 'a' : 'r';
  }
  function saidNowScan(subjects) {
    var told = g('sv-said-now', {}), rag = window.svStrength ? svStrength.rag() : {}, changed = false;
    (subjects || []).forEach(function (su) {
      (su.units || []).forEach(function (u) {
        var key = su.sub + '/' + u[3], said = rag[key]; if (!said) return;
        var now = nowBand(su, u); if (!now) return;
        if (RANK_NOW[now] <= RANK_SAID[said]) return;
        var prev = told[key];
        if (prev && RANK_NOW[prev.band] >= RANK_NOW[now]) return;
        var text = now === 'g'
          ? u[0] + ' is secure now — good work.'
          : 'Good progress on ' + u[0] + ' — developing now.';
        told[key] = { band: now, d: today(), t: Date.now(), text: text, sub: su.slug };
        changed = true;
      });
    });
    if (changed) { try { localStorage.setItem('sv-said-now', JSON.stringify(told)); } catch (e) {} if (window.svProgressPushSoon) svProgressPushSoon(); }
    return told;
  }
  /* the line to show: the newest thing that became true (optionally for one subject) */
  function saidNow(subjects, slug) {
    var told = saidNowScan(subjects), best = null;
    for (var k in told) { var e = told[k]; if (slug && e.sub !== slug) continue; if (!best || (e.t || 0) > (best.t || 0)) best = e; }
    return best ? best.text : null;
  }

  /* the last seven days (or any window), from the logs every page already writes */
  function window7(from, to) {
    var s = { days: {}, lessons: 0, quizzes: 0, quizPass: 0, cards: 0, cardsRight: 0, answers: 0, active: 0 };
    var inWin = function (d) { return d && d >= from && d <= to; };
    var when = g('sv-lessons-when', {}); for (var k in when) if (inWin(when[k])) { s.lessons++; s.days[when[k]] = 1; }
    var kc = g('sv-kc-log', {}); for (var k2 in kc) { var e = kc[k2]; if (inWin(e.d)) { s.quizzes++; if (e.t && e.s / e.t >= 0.8) s.quizPass++; s.days[e.d] = 1; } }
    (g('sv-flash-log', []) || []).forEach(function (e) { if (inWin(e.d)) { s.cards++; if (e.ok) s.cardsRight++; s.days[e.d] = 1; } });
    (g('sv-practice-log', []) || []).forEach(function (e) { if (inWin(e.d)) { s.answers++; s.days[e.d] = 1; } });
    s.active = Object.keys(s.days).length;
    s.any = !!(s.lessons || s.quizzes || s.cards || s.answers);
    return s;
  }
  function iso(d) { return d.toISOString().slice(0, 10); }
  function week() { var t = new Date(); var f = new Date(t); f.setDate(f.getDate() - 6); return window7(iso(f), iso(t)); }
  function lastWeek() { var t = new Date(); t.setDate(t.getDate() - 7); var f = new Date(t); f.setDate(f.getDate() - 6); return window7(iso(f), iso(t)); }
  /* ISO week id, so the review shows once per week */
  function weekId() { var d = new Date(); var day = (d.getDay() + 6) % 7; d.setDate(d.getDate() - day); return iso(d); }
  /* first visit of a new week with something to say -> last week's picture, once */
  function review() {
    var seen = null; try { seen = localStorage.getItem('sv-week-seen'); } catch (e) {}
    var id = weekId(); if (seen === id) return null;
    var lw = lastWeek();
    try { localStorage.setItem('sv-week-seen', id); } catch (e2) {}
    return lw.any ? lw : null;
  }
  function lines(s) {
    var out = [];
    out.push(['Days revised', String(s.active)]);
    if (s.lessons) out.push(['Lessons covered', String(s.lessons)]);
    if (s.quizzes) out.push(['Quizzes passed', s.quizPass + ' of ' + s.quizzes]);
    if (s.cards) out.push(['Cards right', s.cardsRight + ' of ' + s.cards]);
    if (s.answers) out.push(['Exam answers marked', String(s.answers)]);
    return out;
  }

  window.svProgress = { counts: counts, headline: headline, track: track, band: band, dueIn: dueIn, words: NOW, saidNow: saidNow, week: week, lastWeek: lastWeek, review: review, lines: lines, shortDate: shortDate };
})();
