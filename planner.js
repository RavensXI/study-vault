/* svPlanner — the revision-plan engine + modal, shared by both dashboards.
   One module so the classic view and the cosy desk show the SAME plan
   (shared-truth rule: anything both views show comes from one place).

   11 Sep 2026 rebuild (Tom): the plan is CONCRETE. Each session is a real
   lesson — the student's next unread lesson in that subject — walked forward
   from where they actually are, with its quick quiz scheduled a few days
   later as spaced retrieval. Finishing a lesson early or skipping a day
   re-flows everything after it. The dashboards' "Here's your plan" card is
   fed from the same engine (svPlanPrimary), so the card, the calendar tip,
   the desk notebook and this sheet can never disagree.

   Engine: a schedule from today to the LAST exam. Rest days and holidays
   push work along rather than deleting it. A subject's urgency rises as its
   next paper approaches, and it drops out once its final paper is sat.

   Exam dates: data/exam-dates-2027.json (the boards' own timetables) where
   the board+subject is in it; dash-data's provisional table otherwise. Only
   real dates are offered for export.

   Depends on dash-data.js globals: svExamsFor, svFirstLast, SUPA, ANON,
   DONE, svIsPracticeUnit.
   Page contract:
     svPlannerBoot(SUBJECTS, {onChange})   // after SUBJECTS are final
     svPlannerRefresh()                    // after live units land / progress changes
     svPlannerOpen(monthDate?)             // the calendar door
     planFor(date) -> {exams,off,sessions,done,total} | null
     svPlanToday() -> [sessions] | null;  svPlanPrimary() -> today's lesson (continue-target shape)
     showDayTip(anchorEl, date)            // hover/click day tooltip
   Prefs in localStorage sv-plan-prefs {rest:[dow], hols:[iso]} — account-synced. */

var PLANK = 'sv-plan-prefs';
var PLANP = { rest: [], hols: [] };
try { Object.assign(PLANP, JSON.parse(localStorage.getItem(PLANK) || '{}')); } catch (e) {}
function planSave() {
  try { localStorage.setItem(PLANK, JSON.stringify(PLANP)); } catch (e) {}
  if (window.svProgressPushSoon) svProgressPushSoon();
}
function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
var PLNOW = new Date();
var T0 = new Date(PLNOW.getFullYear(), PLNOW.getMonth(), PLNOW.getDate());
function offKind(d) {
  if (PLANP.rest.includes(d.getDay())) return 'rest';
  if (PLANP.hols.includes(iso(d))) return 'holiday';
  return null;
}
function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

/* ---- real exam dates: the boards' timetables where we have them ---- */
var PL_REAL = null;          // data/exam-dates-2027.json once loaded
var PL_BASE = { maths: 'maths', lang: 'english-language', lit: 'english-literature', science: 'science', triple: 'separate-sciences',
  history: 'history', geog: 'geography', french: 'french', spanish: 'spanish', german: 'german', cs: 'computer-science',
  business: 'business', rs: 'religious-education', drama: 'drama', music: 'music', mtech: 'music-technology',
  dt: 'design-technology', food: 'food-technology', pe: 'sport-science', it: 'creative-imedia' };
function plBoardOf(su) {
  var m = /-(aqa|edexcel|ocr|eduqas|wjec|ncfe)(-b)?$/.exec(su.sub || '');
  return m ? (m[1] === 'wjec' ? 'eduqas' : m[1]) : null;
}
/* exams for a subject: real if the timetable has the board+subject, else the provisional table */
function plExams(su) {
  var board = plBoardOf(su), base = PL_BASE[su.slug];
  if (PL_REAL && board && base && PL_REAL[board] && PL_REAL[board][base]) {
    return PL_REAL[board][base].map(function (p) {
      var y = +p.date.slice(0, 4), mo = +p.date.slice(5, 7), da = +p.date.slice(8, 10);
      return { d: new Date(y, mo - 1, da), label: p.paper + (p.session ? ' (' + p.session.toUpperCase() + ')' : ''), real: true };
    });
  }
  return (svExamsFor(su) || []).map(function (e) { return { d: e.d, label: e.label, real: false }; });
}
function plLast(subjects) {
  var last = null;
  subjects.forEach(function (su) { plExams(su).forEach(function (e) { if (!last || e.d > last) last = e.d; }); });
  return last || svFirstLast(subjects).last;
}

/* ---- lesson titles: one fetch for the student's subjects, cached for the session ---- */
var PL_TITLES = {};          // sub -> unitSlug -> { num: title }
function plLoadTitles(subjects, cb) {
  var subs = subjects.map(function (s) { return s.sub; }).filter(Boolean);
  if (!subs.length || typeof SUPA === 'undefined') { cb && cb(); return; }
  var key = 'sv-plan-titles:' + subs.join(',');
  try { var c = sessionStorage.getItem(key); if (c) { PL_TITLES = JSON.parse(c); cb && cb(); return; } } catch (e) {}
  var url = SUPA + '/rest/v1/lessons?select=title,lesson_number,units!inner(slug,subjects!inner(slug,school_id))'
    + '&status=eq.live&units.subjects.school_id=is.null&units.subjects.slug=in.(' + subs.map(function (s) { return '"' + s + '"'; }).join(',') + ')';
  fetch(url, { headers: { apikey: ANON } }).then(function (r) { return r.json(); }).then(function (rows) {
    var t = {};
    (Array.isArray(rows) ? rows : []).forEach(function (l) {
      var s = l.units && l.units.subjects && l.units.subjects.slug, u = l.units && l.units.slug;
      if (!s || !u) return;
      (t[s] = t[s] || {}); (t[s][u] = t[s][u] || {}); t[s][u][l.lesson_number] = l.title;
    });
    PL_TITLES = t;
    try { sessionStorage.setItem(key, JSON.stringify(t)); } catch (e) {}
    cb && cb();
  }).catch(function () { cb && cb(); });
}
function plTitle(su, unit, num) {
  return (PL_TITLES[su.sub] && PL_TITLES[su.sub][unit] && PL_TITLES[su.sub][unit][num]) || null;
}

/* ---- the queue of what each subject still has to do, in order ---- */
/* the subject's remaining lessons, red-rated units first (the student's own
   RAG, unit level over subject level), otherwise in unit order. Each item
   carries its entry point: a lesson the student rated amber/green (or that
   has strength from before) is quiz-first - pass and it is covered. */
function plRagOf(su, unit) {
  if (!window.svStrength) return 'a';
  var r = svStrength.rag(); return r[su.sub + '/' + unit] || r[su.slug] || 'a';
}
function plQueue(su) {
  var q = [], order = { r: 0, a: 1, g: 1 };   // red units first; the rest keep the unit order (green ones become quiz-first, not last)
  var units = (su.units || []).map(function (u, i) { return { u: u, i: i, r: order[plRagOf(su, u[3])] }; });
  units.sort(function (a, b) { return (a.r - b.r) || (a.i - b.i); });
  units.forEach(function (w) {
    var u = w.u, done = u[4] || [];
    for (var n = 1; n <= (u[1] || 0); n++) {
      if (done.indexOf(n) >= 0) continue;
      var st = window.svStrength ? svStrength.lesson(su, u[3], n) : null;
      q.push({ unit: u[3], unitName: u[0], num: n, total: u[1], quizFirst: !!(st && st.s >= 35) });
    }
  });
  return q;
}
/* the daily budget -> how many subject sessions a day, and their minutes */
function plBudget() { return (window.svStrength && svStrength.budget()) || 45; }
function plShape() {
  var b = plBudget();
  return b <= 20 ? { n: 1, mins: [15] } : b <= 45 ? { n: 2, mins: [25, 15] } : { n: 3, mins: [25, 15, 15] };
}
function plUrl(su, unit, num) {
  return '/' + ((window.svIsPracticeUnit && svIsPracticeUnit(su, unit)) ? 'practice' : 'lesson') + '/' + su.sub + '/' + unit + '/' + num;
}
function plKcDone(su, unit, num) {
  try { var kc = JSON.parse(localStorage.getItem('sv-kc-log') || '{}'); return !!kc[su.sub + '/' + unit + '/' + num]; } catch (e) { return false; }
}
function plLessonDone(su, unit, num) {
  var set = (typeof DONE !== 'undefined' && DONE[su.sub + '/' + unit]) || [];
  return set.indexOf(num) >= 0;
}

var PL_SUBJECTS = [], PL_LAST = null, PL_ONCHANGE = null, PL_FIT = {};
var SCHED = {};
function buildSchedule() {
  SCHED = {};
  if (!PL_SUBJECTS.length || !PL_LAST) return;
  var lastSeen = {}, queues = {}, retrieval = [];      // retrieval: quizzes due on a date
  var shape = plShape();
  PL_FIT = {};                                          // per subject: lessons that fit before its first exam
  PL_SUBJECTS.forEach(function (su) { lastSeen[su.slug] = -999; queues[su.slug] = plQueue(su); PL_FIT[su.slug] = { left: queues[su.slug].length, fit: 0, first: (plExams(su)[0] || {}).d || null }; });
  /* today only: lessons whose real strength has faded come back as a quick quiz first */
  var dueNow = [];
  if (window.svStrength) PL_SUBJECTS.forEach(function (su) { svStrength.due(su, 2).forEach(function (r) { dueNow.push({ on: T0, s: su, unit: r.unit, unitName: r.unitName, num: r.num, total: r.total }); }); });
  retrieval = retrieval.concat(dueNow.slice(0, 2));
  for (var d = new Date(T0), di = 0; d <= PL_LAST; d = new Date(d.getTime() + 864e5), di++) {
    if (offKind(d)) continue;
    var active = PL_SUBJECTS.filter(function (su) {
      var ex = plExams(su); return ex.length && ex[ex.length - 1].d >= d;
    });
    if (!active.length) continue;
    var scored = active.map(function (su) {
      var nxt = plExams(su).find(function (e) { return e.d >= d; });
      var urg = 1 + 8 / ((nxt ? Math.round((nxt.d - d) / 864e5) : 400) + 3);
      /* the student's own rating of the SUBJECT: red comes round more often, green less */
      var rw = { r: 1.4, a: 1, g: 0.7 }[(window.svStrength && svStrength.rag()[su.slug]) || 'a'] || 1;
      return { su: su, score: (di - lastSeen[su.slug]) * urg * rw };
    }).sort(function (a, b) { return b.score - a.score || a.su.slug.localeCompare(b.su.slug); });
    var picks = [], k = iso(d);
    scored.slice(0, shape.n).forEach(function (p, pi) {
      var su = p.su; lastSeen[su.slug] = di;
      var q = queues[su.slug], item = q.length ? q.shift() : null;
      var practice = item && window.svIsPracticeUnit && svIsPracticeUnit(su, item.unit);
      if (item) {
        var qf = item.quizFirst && !practice;
        if (PL_FIT[su.slug].first && d <= PL_FIT[su.slug].first) PL_FIT[su.slug].fit++;
        picks.push({ s: su, act: practice ? 'practice' : (qf ? 'quiz-first' : 'lesson'), unit: item.unit, unitName: item.unitName, num: item.num, total: item.total,
                     title: plTitle(su, item.unit, item.num), url: plUrl(su, item.unit, item.num) + (qf ? '?quiz=1' : ''), min: qf ? 10 : shape.mins[pi] });
        /* the quick quiz on it three days on: retrieval, not re-reading */
        if (!practice) retrieval.push({ on: new Date(d.getTime() + 3 * 864e5), s: su, unit: item.unit, unitName: item.unitName, num: item.num, total: item.total });
      } else {
        /* everything read: a practice review of the subject instead */
        picks.push({ s: su, act: 'review', title: 'Practice questions — pick a weak unit', url: '/browse/' + su.sub, min: pi ? 15 : 20 });
      }
    });
    /* quizzes that fell due today (or slid off a rest day onto it) */
    var due = retrieval.filter(function (r) { return r.on <= d; });
    retrieval = retrieval.filter(function (r) { return r.on > d; });
    due.slice(0, 2).forEach(function (r) {
      picks.push({ s: r.s, act: 'knowledge check', unit: r.unit, unitName: r.unitName, num: r.num, total: r.total,
                   title: plTitle(r.s, r.unit, r.num), url: plUrl(r.s, r.unit, r.num) + '#kc', min: 5, quiz: true });
    });
    /* the mixed deck: today it is sized by what is actually due; later days a short sitting */
    var dueCards = (di === 0 && window.svStrength) ? svStrength.flashDue() : 0;
    picks.push({ s: null, act: 'flashcards', title: di === 0 && dueCards ? dueCards + ' cards due' : 'Flashcards — mixed deck',
                 url: '/classic?fc=1', min: di === 0 && dueCards ? Math.min(12, Math.ceil(dueCards / 4) + 1) : 5, mixed: true });
    SCHED[k] = picks;
  }
}
function examsOn(d) {
  var k = iso(d), out = [];
  PL_SUBJECTS.forEach(function (su) { plExams(su).forEach(function (e) { if (iso(e.d) === k) out.push({ s: su, label: e.label, real: e.real }); }); });
  return out;
}
function sessDone(x) {
  if (!x || !x.s) return x && x.mixed ? plFlashToday() : false;
  if (x.act === 'quiz-first') return plLessonDone(x.s, x.unit, x.num) || plKcDone(x.s, x.unit, x.num);
  if (x.quiz) return plKcDone(x.s, x.unit, x.num);
  if (x.act === 'review') return false;
  return plLessonDone(x.s, x.unit, x.num);
}
function plFlashToday() { try { return localStorage.getItem('sv-flash-day') === iso(PLNOW); } catch (e) { return false; } }
function planFor(d) {
  if (!PL_LAST || d < T0 - 32 * 864e5 || d > PL_LAST || !PL_SUBJECTS.length) return null;
  var off = offKind(d), s = off ? null : (SCHED[iso(d)] || null), done = 0;
  (s || []).forEach(function (x) { if (sessDone(x)) done++; });
  return { exams: examsOn(d), off: off, sessions: s, done: done, total: s ? s.length : 0 };
}
function svPlanToday() { var p = planFor(T0); return p ? p.sessions : null; }
/* the dashboards' row 2: today's first real lesson, in svContinueTarget's shape */
function svPlanPrimary() {
  var s = svPlanToday(); if (!s) return null;
  var x = s.find(function (y) { return y.s && (y.act === 'lesson' || y.act === 'practice' || y.act === 'quiz-first'); });
  if (!x) return null;
  return { su: x.s, unitName: x.unitName, unitSlug: x.unit, total: x.total, num: x.num, url: x.url, title: x.title, act: x.act, min: x.min };
}
function sessLabel(x) { return x.title || (x.s ? (x.unitName + ' · ' + (x.act === 'practice' ? 'set' : 'lesson') + ' ' + x.num) : x.act); }
function actWord(x) { return x.quiz ? 'quick quiz' : x.act === 'quiz-first' ? 'quiz first - pass and it is covered' : x.act === 'review' ? 'review' : x.mixed ? '' : x.act; }

/* ---- day tooltip (shared by both views' mini calendars) ---- */
var DOWNAME = ['Sundays', 'Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays'];
function showDayTip(anchor, d) {
  var daytip = document.getElementById('daytip');
  var p = planFor(d);
  var html = '<b>' + d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) + '</b><br>';
  if (!p) { html += d > PL_LAST ? 'Exams over. Freedom.' : 'Outside your plan.'; }
  else {
    if (p.exams.length) html += p.exams.map(function (e) {
      return '<span class="row"><span class="sw" style="background:' + e.s.c + '"></span><b>Exam · ' + esc(e.s.name) + ' — ' + esc(e.label) + '</b></span>'; }).join('');
    if (p.off === 'rest') html += 'Rest day — you don’t revise on ' + DOWNAME[d.getDay()] + '.';
    else if (p.off === 'holiday') html += 'Holiday — enjoy it. The work moved along, it didn’t vanish.';
    else if (p.sessions) html += p.sessions.map(function (x) {
      var sw = '<span class="sw" style="background:' + (x.s ? x.s.c : '#9a8f7a') + '"></span>';
      var who = x.s ? esc(x.s.tab || x.s.name) + ' · ' : '';
      return '<span class="row' + (sessDone(x) ? ' dn' : '') + '">' + sw + who + esc(sessLabel(x)) + ' · ' + x.min + ' min</span>'; }).join('');
    else if (!p.exams.length) html += 'Nothing scheduled.';
    html += '<span class="tipmore">tap for the full day</span>';
  }
  daytip.innerHTML = html;
  var r = anchor.getBoundingClientRect();
  daytip.style.left = Math.min(innerWidth - 290, Math.max(8, r.left - 40)) + 'px';
  daytip.style.top = (r.bottom + 6 + scrollY) + 'px';
  daytip.classList.add('on');
}

/* ---- the modal: injected on boot so both views get the identical sheet ---- */
var PL_CSS = [
  '.daytip{position:absolute;z-index:70;background:#26231e;color:#f2ead9;border-radius:6px;padding:.6rem .8rem;font-size:.78rem;line-height:1.6;max-width:280px;box-shadow:0 10px 30px rgba(0,0,0,.3);display:none;pointer-events:none}',
  '.daytip.on{display:block}',
  '.daytip b{color:#fff}',
  '.daytip .row{display:flex;gap:7px;align-items:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
  '.daytip .row.dn{opacity:.55;text-decoration:line-through}',
  '.daytip .tipmore{display:block;margin-top:.2rem;font-size:.7rem;color:#b8ad98}',
  '.daytip .sw,.plday .sw,.plsess .sw,.plagenda .sw{width:8px;height:8px;border-radius:2px;flex:none;display:inline-block}',
  '.plmodal{position:fixed;inset:0;background:rgba(38,30,18,.55);display:none;place-items:center;z-index:60;padding:20px;font-family:"Schibsted Grotesk",system-ui,sans-serif;color:#2d2a26}',
  '.plmodal.open{display:grid}',
  '.plsheet{background:#f6f1e7;border-radius:10px;max-width:1040px;width:100%;max-height:92vh;overflow:auto;padding:26px 30px 30px;position:relative;box-shadow:0 30px 80px rgba(0,0,0,.35)}',
  '.plsheet .x{position:absolute;top:16px;right:18px;width:36px;height:36px;border-radius:50%;border:1px solid #e4dfd2;background:#fffdf8;cursor:pointer;font-size:1rem;color:#57534a}',
  '.plsheet h2{font-family:"Literata",Georgia,serif;margin:0 0 .2rem;font-size:1.6rem}',
  '.plsub{color:#57534a;font-size:.92rem;margin:0 0 1rem;max-width:680px;line-height:1.5}',
  '.plctl{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;margin-bottom:1rem;padding:.8rem 1rem;background:#fffdf8;border:1px solid #e4dfd2;border-radius:6px}',
  '.plctl .lbl2{font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#84806f}',
  '.wkday{display:flex;gap:5px}',
  '.wkday button{border:1px solid #e4dfd2;background:#fffdf8;border-radius:4px;padding:.35rem .55rem;font-weight:600;font-size:.78rem;cursor:pointer;color:#57534a;font-family:inherit}',
  '.wkday button[aria-pressed="true"]{background:#5b4632;border-color:#5b4632;color:#fff}',
  '.plctl .sp{flex:1}',
  '.plbtn{border:1px solid #cfc6b4;background:#fffdf8;border-radius:4px;padding:.4rem .75rem;font-weight:600;font-size:.78rem;cursor:pointer;color:#3f3222;font-family:inherit;white-space:nowrap}',
  '.plbtn:hover{border-color:#5b4632}',
  '.plbtn.dark{background:#5b4632;border-color:#5b4632;color:#fff}',
  '.replan{opacity:0;transition:opacity .3s;font-size:.78rem;font-weight:700;color:#4e6e5d}',
  '.replan.on{opacity:1}',
  '.plnav{display:flex;align-items:center;gap:10px;margin:.3rem 0 .5rem}',
  '.plnav b{font-family:"Literata",Georgia,serif;font-size:1.05rem;min-width:160px;text-align:center}',
  '.plnav button{width:30px;height:30px;border:1px solid #e4dfd2;background:#fffdf8;border-radius:4px;cursor:pointer}',
  '.plgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px}',
  '.plgrid .hd{font-size:.68rem;font-weight:700;letter-spacing:.1em;color:#84806f;text-transform:uppercase;text-align:center;padding:.2rem 0}',
  '.plday{min-height:76px;min-width:0;overflow:hidden;border:1px solid #efeadf;border-radius:5px;background:#fffdf8;padding:.3rem .4rem .35rem;font-size:.72rem;position:relative;text-align:left;cursor:pointer;font-family:inherit;color:#2d2a26;display:flex;flex-direction:column;gap:.22rem}',
  '.plday:hover{border-color:#cfc6b4}',
  '.plday.sel{border-color:#5b4632;box-shadow:inset 0 0 0 1px #5b4632}',
  '.plday .dn{font-weight:700;color:#57534a;font-variant-numeric:tabular-nums;display:flex;align-items:center;gap:.3rem}',
  '.plday .dn .tick{margin-left:auto;font-size:.7rem;color:#4e6e5d;font-weight:700}',
  '.plday .dn .miss{margin-left:auto;font-size:.66rem;color:#b3a48a}',
  '.plday.off{background:transparent;border-style:dashed}',
  '.plday.off .dn{color:#84806f}',
  '.plday.past{opacity:.55}',
  '.plday.hol{background:#f6ecd2;border-color:#e6d5a9}',
  '.plday.hol .dn::after{content:"holiday";font-weight:600;color:#a3873a;margin-left:auto;font-size:.62rem}',
  '.plday.examday{outline:2px solid #a3542f;outline-offset:-2px}',
  '.plday .chip{display:inline-flex;align-items:center;gap:.3rem;max-width:100%;padding:.12rem .4rem;border-radius:3px;font-weight:600;font-size:.68rem;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
  '.plday .chip.done{opacity:.5;text-decoration:line-through}',
  '.plday .chip.ex{background:#a3542f}',
  '.plday .more{font-size:.62rem;color:#84806f}',
  '.plday.today .dn{color:#fff;background:#5b4632;border-radius:3px;padding:0 4px;align-self:flex-start}',
  '.pldaysheet{margin-top:.9rem;background:#fffdf8;border:1px solid #e4dfd2;border-radius:8px;padding:1rem 1.1rem 1rem;display:none}',
  '.pldaysheet.on{display:block}',
  '.pldaysheet h3{font-family:"Literata",Georgia,serif;margin:0 0 .5rem;font-size:1.15rem;display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}',
  '.pldaysheet h3 small{font-family:inherit;font-weight:400;font-size:.8rem;color:#84806f}',
  '.plsess{list-style:none;margin:0 0 .8rem;padding:0}',
  '.plsess li{display:flex;align-items:center;gap:.7rem;padding:.5rem .2rem;border-top:1px solid #efeadf}',
  '.plsess li:first-child{border-top:0}',
  '.plsess li a{color:inherit;text-decoration:none;flex:1;min-width:0;display:flex;flex-direction:column}',
  '.plsess li a:hover b{text-decoration:underline}',
  '.plsess li b{font-weight:600;font-size:.92rem;line-height:1.3}',
  '.plsess li small{color:#84806f;font-size:.76rem}',
  '.plsess li .mins{font-size:.74rem;color:#84806f;white-space:nowrap}',
  '.plsess li.dn b{text-decoration:line-through;color:#84806f}',
  '.plsess li .ok{color:#4e6e5d;font-weight:700;font-size:.8rem}',
  '.plsess li.ex b{color:#7a3f24}',
  '.plsess li.ex .mins{color:#a3542f;font-weight:600}',
  '.plsheet .acts{display:flex;gap:8px;flex-wrap:wrap}',
  '.plfoot{margin-top:.9rem;font-size:.8rem;color:#57534a}',
  '.plagenda{display:none;list-style:none;margin:0;padding:0}',
  '.plagenda li.day{margin:.9rem 0 .3rem;font-weight:700;font-size:.8rem;color:#57534a;display:flex;align-items:center;gap:.5rem}',
  '.plagenda li.day .tag{font-weight:600;font-size:.68rem;color:#a3873a}',
  '.plagenda li.s{display:flex;align-items:center;gap:.6rem;padding:.45rem .2rem;border-top:1px solid #efeadf;font-size:.9rem}',
  '.plagenda li.s a{color:inherit;text-decoration:none;flex:1;min-width:0}',
  '.plagenda li.s small{color:#84806f;font-size:.74rem;white-space:nowrap}',
  '.plagenda li.s.dn a{text-decoration:line-through;color:#84806f}',
  '.plagenda li.ex{border-top:1px solid #efeadf;padding:.45rem .2rem;font-size:.9rem;color:#7a3f24;font-weight:600}',
  '.plagenda .plbtn{margin-left:auto}',
  '@media (max-width:700px){.plsheet{padding:18px 14px 22px;max-height:96vh}.plnav,.plgrid,.pldaysheet,.pldaysheet.on{display:none}.plagenda{display:block}.plctl .sp{display:none}.plsub{font-size:.86rem}.wkday{flex-wrap:wrap}}'
].join('\n');

var PL_HTML =
  '<div class="plsheet">' +
  '<button class="x" id="closepl" aria-label="Close">✕</button>' +
  '<h2>Your revision plan.</h2>' +
  '<p class="plsub" id="plsub"></p>' +
  '<div class="plctl">' +
  '<span class="lbl2">Revise on</span><span class="wkday" id="wkday"></span>' +
  '<span class="lbl2">Most days</span><span class="wkday" id="plbudget"></span>' +
  '<span class="replan" id="replan">replanned ✓</span><span class="sp"></span>' +
  '<button type="button" class="plbtn" id="plics">Next 2 weeks to my calendar</button>' +
  '<button type="button" class="plbtn" id="plicsex" hidden>Exam dates to my calendar</button></div>' +
  '<div class="plnav"><button id="plprev" aria-label="Previous month">‹</button><b id="plmon"></b><button id="plnext" aria-label="Next month">›</button></div>' +
  '<div class="plgrid" id="plgrid"></div>' +
  '<div class="pldaysheet" id="pldaysheet"></div>' +
  '<ul class="plagenda" id="plagenda"></ul>' +
  '<p class="plfoot" id="plfit"></p>' +
  '<p class="plfoot" id="plfoot">Built from your subjects, where you are in each one, and the exam boards&rsquo; timetables. ' +
  'Finish a lesson early or take a day off and everything after it moves along &mdash; nothing is lost.</p></div>';

var plview = new Date(PLNOW.getFullYear(), PLNOW.getMonth(), 1);
var plsel = null;            // the day open in the sheet
function flashReplan() {
  var el = document.getElementById('replan'); if (!el) return;
  el.classList.add('on'); clearTimeout(flashReplan._t);
  flashReplan._t = setTimeout(function () { el.classList.remove('on'); }, 1500);
}
function plSubtitle() {
  var el = document.getElementById('plsub'); if (!el || !PL_LAST) return;
  el.textContent = 'Runs to your last exam on '
    + PL_LAST.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
    + '. Each session is a real lesson, picked up from where you are. Tap a day to see it in full, or to make it a holiday.';
}
function replan(quiet) {
  buildSchedule(); plSubtitle(); buildFit(); buildPlan(); buildAgenda(); if (plsel) buildDaySheet(plsel);
  if (!quiet) flashReplan();
  if (PL_ONCHANGE) try { PL_ONCHANGE(); } catch (e) {}
}
function buildBudget() {
  var w = document.getElementById('plbudget'); if (!w) return; w.innerHTML = '';
  [[20, '20 min'], [45, '45 min'], [60, '1 hour']].forEach(function (o) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = o[1];
    b.setAttribute('aria-pressed', String(plBudget() === o[0]));
    b.onclick = function () { if (window.svStrength) svStrength.setBudget(o[0]); buildBudget(); replan(); };
    w.appendChild(b);
  });
}
/* the honest line: which subjects will not be covered before their first paper at this budget */
function buildFit() {
  var el = document.getElementById('plfit'); if (!el) return;
  var short = [];
  PL_SUBJECTS.forEach(function (su) {
    var f = PL_FIT[su.slug]; if (!f || !f.first || !f.left) return;
    if (f.fit < f.left) short.push(su.name + ': ' + f.fit + ' of ' + f.left + ' lessons fit before ' + f.first.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }));
  });
  el.textContent = short.length ? 'At ' + plBudget() + ' minutes a day: ' + short.join(' · ') + '. Rate the topics you already know and the quiz-first sessions clear them in minutes.'
                                : 'At ' + plBudget() + ' minutes a day everything fits before its paper.';
}
function buildWk() {
  var w = document.getElementById('wkday'); w.innerHTML = '';
  ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (nm, i) {
    var dow = (i + 1) % 7;
    var b = document.createElement('button'); b.type = 'button'; b.textContent = nm;
    b.setAttribute('aria-pressed', String(!PLANP.rest.includes(dow)));
    b.onclick = function () {
      var ix = PLANP.rest.indexOf(dow);
      if (ix >= 0) PLANP.rest.splice(ix, 1); else PLANP.rest.push(dow);
      planSave(); buildWk(); replan();
    };
    w.appendChild(b);
  });
}
function toggleHoliday(d) {
  var id = iso(d), ix = PLANP.hols.indexOf(id);
  if (ix >= 0) PLANP.hols.splice(ix, 1); else PLANP.hols.push(id);
  planSave(); replan();
}
function buildPlan() {
  var plgrid = document.getElementById('plgrid'), plmon = document.getElementById('plmon');
  if (!plgrid) return;
  plmon.textContent = plview.toLocaleDateString('en-GB', { month: 'long', year: 'numeric' });
  plgrid.innerHTML = '';
  ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (h) {
    var sp = document.createElement('span'); sp.className = 'hd'; sp.textContent = h; plgrid.appendChild(sp);
  });
  var days = new Date(plview.getFullYear(), plview.getMonth() + 1, 0).getDate();
  var lead = (plview.getDay() + 6) % 7;
  for (var i = 0; i < lead; i++) plgrid.appendChild(document.createElement('span'));
  for (var dd = 1; dd <= days; dd++) {
    (function (dd) {
      var d = new Date(plview.getFullYear(), plview.getMonth(), dd);
      var cell = document.createElement('button'); cell.className = 'plday'; cell.type = 'button';
      var p = planFor(d), past = d < T0;
      var dn = '<span class="dn">' + dd;
      if (past && p && p.total) dn += p.done >= p.total ? '<span class="tick">✓</span>' : p.done ? '<span class="tick">' + p.done + '/' + p.total + '</span>' : '<span class="miss">missed</span>';
      dn += '</span>';
      cell.innerHTML = dn;
      if (past) cell.classList.add('past');
      if (iso(d) === iso(PLNOW)) cell.classList.add('today');
      if (plsel && iso(d) === iso(plsel)) cell.classList.add('sel');
      if (p && p.exams.length) {
        cell.classList.add('examday');
        p.exams.forEach(function (e) { cell.innerHTML += '<span class="chip ex">EXAM · ' + esc(e.s.tab || e.s.name) + '</span>'; });
      }
      if (p && p.off === 'rest') cell.classList.add('off');
      else if (p && p.off === 'holiday') cell.classList.add('hol');
      else if (p && p.sessions) {
        var shown = p.sessions.filter(function (x) { return x.s && !x.quiz; }).slice(0, 2);
        shown.forEach(function (x) {
          cell.innerHTML += '<span class="chip' + (sessDone(x) ? ' done' : '') + '" style="background:' + x.s.c + '">' + esc(x.s.tab || x.s.name) + '</span>';
        });
        var extra = p.sessions.length - shown.length;
        if (extra > 0) cell.innerHTML += '<span class="more">+ ' + extra + ' more</span>';
      }
      if (p) cell.onclick = function () { plsel = d; buildPlan(); buildDaySheet(d); };
      plgrid.appendChild(cell);
    })(dd);
  }
}
function sessRow(x, dayIso) {
  var done = sessDone(x);
  var who = x.s ? esc(x.s.name) : 'All subjects';
  var sub = who + (x.unitName ? ' · ' + esc(x.unitName) + (x.num ? ' · ' + (x.act === 'practice' ? 'set' : 'lesson') + ' ' + x.num + ' of ' + x.total : '') : '');
  var kick = actWord(x); if (kick) sub = '<span style="text-transform:capitalize">' + esc(kick) + '</span> · ' + sub;
  return '<li class="' + (done ? 'dn' : '') + '"><span class="sw" style="background:' + (x.s ? x.s.c : '#9a8f7a') + '"></span>' +
    '<a href="' + esc(x.url) + '"><b>' + esc(sessLabel(x)) + '</b><small>' + sub + '</small></a>' +
    (done ? '<span class="ok">done ✓</span>' : '<span class="mins">' + x.min + ' min</span>') + '</li>';
}
function buildDaySheet(d) {
  var sh = document.getElementById('pldaysheet'); if (!sh) return;
  var p = planFor(d);
  var title = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  var html = '<h3>' + title + (iso(d) === iso(PLNOW) ? '<small>today</small>' : '') + '</h3>';
  if (!p) html += '<p class="plsub">' + (d > PL_LAST ? 'After your last exam. Freedom.' : 'Before today.') + '</p>';
  else {
    var rows = '';
    p.exams.forEach(function (e) {
      rows += '<li class="ex"><span class="sw" style="background:' + e.s.c + '"></span><a><b>Exam · ' + esc(e.s.name) + '</b><small>' + esc(e.label) + (e.real ? '' : ' · provisional date') + '</small></a><span class="mins">exam</span></li>'; });
    if (p.off === 'rest') rows += '<li><a><b>Rest day</b><small>You don’t revise on ' + DOWNAME[d.getDay()] + '. Change that under “Revise on”.</small></a></li>';
    else if (p.off === 'holiday') rows += '<li><a><b>Holiday</b><small>The work moved along — nothing vanished.</small></a></li>';
    else if (p.sessions) p.sessions.forEach(function (x) { rows += sessRow(x, iso(d)); });
    else if (!p.exams.length) rows += '<li><a><b>Nothing scheduled</b></a></li>';
    html += '<ul class="plsess">' + rows + '</ul>';
    var total = (p.sessions || []).reduce(function (a, x) { return a + x.min; }, 0);
    html += '<div class="acts">';
    if (d >= T0 && p.off !== 'rest') html += '<button type="button" class="plbtn" id="plhol">' + (p.off === 'holiday' ? 'Put this day back' : 'Make this a holiday') + '</button>';
    if (d >= T0 && p.sessions) html += '<button type="button" class="plbtn" id="plpush">Push today’s work along</button>';
    if (p.sessions && total) html += '<span class="plsub" style="margin:0;align-self:center">' + total + ' min in all</span>';
    html += '</div>';
  }
  sh.innerHTML = html; sh.classList.add('on');
  var hb = document.getElementById('plhol'); if (hb) hb.onclick = function () { toggleHoliday(d); };
  var pb = document.getElementById('plpush'); if (pb) pb.onclick = function () { toggleHoliday(d); };
  if (window.innerWidth > 700) sh.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}
function buildAgenda() {
  var ag = document.getElementById('plagenda'); if (!ag) return;
  var html = '';
  for (var i = 0; i < 14; i++) {
    var d = new Date(T0.getTime() + i * 864e5); if (d > PL_LAST) break;
    var p = planFor(d); if (!p) continue;
    var label = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'short' });
    html += '<li class="day"><span>' + label + '</span>' + (p.off ? '<span class="tag">' + p.off + '</span>' : '') +
      (p.off !== 'rest' ? '<button type="button" class="plbtn" data-hol="' + iso(d) + '">' + (p.off === 'holiday' ? 'put back' : 'holiday') + '</button>' : '') + '</li>';
    p.exams.forEach(function (e) { html += '<li class="ex">Exam · ' + esc(e.s.name) + ' — ' + esc(e.label) + '</li>'; });
    (p.sessions || []).forEach(function (x) {
      html += '<li class="s' + (sessDone(x) ? ' dn' : '') + '"><span class="sw" style="background:' + (x.s ? x.s.c : '#9a8f7a') + '"></span>' +
        '<a href="' + esc(x.url) + '">' + (x.s ? esc(x.s.tab || x.s.name) + ' · ' : '') + esc(sessLabel(x)) + '</a><small>' + (sessDone(x) ? 'done ✓' : x.min + ' min') + '</small></li>';
    });
  }
  ag.innerHTML = html;
  ag.querySelectorAll('[data-hol]').forEach(function (b) {
    b.onclick = function () { var s = b.getAttribute('data-hol'); toggleHoliday(new Date(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10))); };
  });
}

/* ---- calendar export (.ics): the next fortnight of sessions; exam dates when they are real ---- */
function icsStamp(d, h, m) { return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0') + (h == null ? '' : 'T' + String(h).padStart(2, '0') + String(m).padStart(2, '0') + '00'); }
function icsText(s) { return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n'); }
function icsFile(name, events) {
  var out = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//StudyVault//Revision plan//EN', 'CALSCALE:GREGORIAN', 'X-WR-CALNAME:' + icsText(name)];
  events.forEach(function (e, i) {
    out.push('BEGIN:VEVENT', 'UID:sv-' + Date.now() + '-' + i + '@studyvault.co.uk', 'DTSTAMP:' + icsStamp(new Date(), 0, 0) + 'Z');
    if (e.allDay) { out.push('DTSTART;VALUE=DATE:' + icsStamp(e.d), 'DTEND;VALUE=DATE:' + icsStamp(new Date(e.d.getTime() + 864e5))); }
    else { out.push('DTSTART:' + icsStamp(e.d, e.h, e.m), 'DTEND:' + icsStamp(e.d, e.h2, e.m2)); }
    out.push('SUMMARY:' + icsText(e.summary));
    if (e.desc) out.push('DESCRIPTION:' + icsText(e.desc));
    if (e.url) out.push('URL:' + e.url);
    out.push('END:VEVENT');
  });
  out.push('END:VCALENDAR');
  return out.join('\r\n');
}
function plDownload(name, text) {
  var blob = new Blob([text], { type: 'text/calendar;charset=utf-8' }), a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
}
function exportSessions() {
  var ev = [];
  for (var i = 0; i < 14; i++) {
    var d = new Date(T0.getTime() + i * 864e5); if (d > PL_LAST) break;
    var p = planFor(d); if (!p || !p.sessions) continue;
    var h = 16, m = 30;                            // one block from 4:30pm, sessions back to back
    p.sessions.forEach(function (x) {
      var mins = x.min, m2 = m + mins, h2 = h + Math.floor(m2 / 60); m2 = m2 % 60;
      ev.push({ d: d, h: h, m: m, h2: h2, m2: m2, summary: (x.s ? (x.s.tab || x.s.name) + ': ' : '') + sessLabel(x),
                desc: 'StudyVault revision plan (a snapshot — the live plan on the site re-flows as you go).', url: location.origin + x.url });
      h = h2; m = m2;
    });
  }
  if (!ev.length) return;
  plDownload('studyvault-revision-plan.ics', icsFile('StudyVault revision plan', ev));
}
function exportExams() {
  var ev = [];
  PL_SUBJECTS.forEach(function (su) { plExams(su).forEach(function (e) { if (e.real) ev.push({ d: e.d, allDay: true, summary: 'EXAM · ' + su.name + ' — ' + e.label, desc: 'From the exam board’s published timetable.' }); }); });
  if (!ev.length) return;
  plDownload('studyvault-exam-dates.ics', icsFile('StudyVault exam dates', ev));
}
function anyRealExams() {
  return PL_SUBJECTS.some(function (su) { return plExams(su).some(function (e) { return e.real; }); });
}

function svPlannerBoot(SUBJECTS, opts) {
  opts = opts || {};
  PL_SUBJECTS = SUBJECTS;
  PL_ONCHANGE = opts.onChange || null;
  PL_LAST = plLast(SUBJECTS);
  if (!document.getElementById('plmodal')) {
    var st = document.createElement('style'); st.textContent = PL_CSS; document.head.appendChild(st);
    var m = document.createElement('div'); m.className = 'plmodal'; m.id = 'plmodal';
    m.setAttribute('aria-modal', 'true'); m.setAttribute('role', 'dialog'); m.setAttribute('aria-label', 'Your revision plan');
    m.innerHTML = PL_HTML;
    document.body.appendChild(m);
    var tip = document.createElement('div'); tip.className = 'daytip'; tip.id = 'daytip';
    document.body.appendChild(tip);
    document.getElementById('plprev').onclick = function () { plview = new Date(plview.getFullYear(), plview.getMonth() - 1, 1); buildPlan(); };
    document.getElementById('plnext').onclick = function () { plview = new Date(plview.getFullYear(), plview.getMonth() + 1, 1); buildPlan(); };
    document.getElementById('closepl').onclick = function () { m.classList.remove('open'); };
    document.getElementById('plics').onclick = exportSessions;
    document.getElementById('plicsex').onclick = exportExams;
    m.addEventListener('click', function (e) { if (e.target === m) m.classList.remove('open'); });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.cal .d') && !e.target.closest('.calgrid .d') && !e.target.closest('.daytip')) tip.classList.remove('on');
    });
  }
  buildSchedule();
  /* the real timetable and the lesson titles arrive async; each re-plans quietly */
  if (!PL_REAL) fetch('/data/exam-dates-2027.json').then(function (r) { return r.json(); }).then(function (j) {
    PL_REAL = j || null; PL_LAST = plLast(PL_SUBJECTS); replan(true);
    var b = document.getElementById('plicsex'); if (b) b.hidden = !anyRealExams();
  }).catch(function () {});
  plLoadTitles(SUBJECTS, function () { replan(true); });
  /* staging: ?plan=YYYY-MM opens the planner at that month */
  var q = new URLSearchParams(location.search).get('plan');
  if (q !== null) {
    if (/^\d{4}-\d{2}$/.test(q)) plview = new Date(+q.slice(0, 4), +q.slice(5, 7) - 1, 1);
    svPlannerOpen();
  }
}
/* after live units land (progress-aware queues), or progress changes */
function svPlannerRefresh() { PL_LAST = plLast(PL_SUBJECTS); replan(true); }

function svPlannerOpen(month) {
  if (month instanceof Date) plview = new Date(month.getFullYear(), month.getMonth(), 1);
  plSubtitle();
  var b = document.getElementById('plicsex'); if (b) b.hidden = !anyRealExams();
  if (!plsel) plsel = new Date(T0);
  buildWk(); buildBudget(); buildFit(); buildPlan(); buildAgenda(); buildDaySheet(plsel);
  document.getElementById('plmodal').classList.add('open');
}
