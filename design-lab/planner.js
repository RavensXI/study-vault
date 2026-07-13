/* svPlanner — the revision-plan engine + modal, shared by both dashboards.
   Moved out of dash-classic so the cosy desk's calendar opens the SAME
   planner and shows the SAME per-day sessions (shared-truth rule: anything
   both views show comes from one module).

   Engine: a real schedule from today to the LAST exam. Sessions are laid
   over the days the student actually has — rest days and holidays push work
   along rather than deleting it. A subject's urgency rises as its next paper
   approaches, and it drops out of the rotation once its final paper is sat.

   Depends on dash-data.js globals: svExamsFor, svFirstLast.
   Page contract:
     svPlannerBoot(SUBJECTS, {onChange})   // after SUBJECTS are final
     svPlannerOpen(monthDate?)             // the calendar door
     planFor(date) -> {exams,off,sessions} | null
     showDayTip(anchorEl, date)            // hover/click day tooltip
   Prefs in localStorage sv-plan-prefs {rest:[dow], hols:[iso]} — shared. */

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

var PL_SUBJECTS = [], PL_LAST = null, PL_ONCHANGE = null;
var SCHED = {};
function buildSchedule() {
  SCHED = {};
  if (!PL_SUBJECTS.length) return;
  var lastSeen = {}; PL_SUBJECTS.forEach(function (su) { lastSeen[su.slug] = -999; });
  var ACT = ['lesson', 'practice', 'flashcards', 'knowledge check'];
  for (var d = new Date(T0), di = 0; d <= PL_LAST; d = new Date(d.getTime() + 864e5), di++) {
    if (offKind(d)) continue;
    var active = PL_SUBJECTS.filter(function (su) {
      var ex = svExamsFor(su); return ex.length && ex[ex.length - 1].d >= d;
    });
    if (!active.length) continue;
    var scored = active.map(function (su) {
      var nxt = svExamsFor(su).find(function (e) { return e.d >= d; });
      var urg = 1 + 8 / ((nxt ? Math.round((nxt.d - d) / 864e5) : 400) + 3);
      return { su: su, score: (di - lastSeen[su.slug]) * urg };
    }).sort(function (a, b) { return b.score - a.score || a.su.slug.localeCompare(b.su.slug); });
    SCHED[iso(d)] = scored.slice(0, Math.min(2, scored.length)).map(function (p, pi) {
      lastSeen[p.su.slug] = di;
      return { s: p.su, act: ACT[(di + pi * 2) % 4], min: pi ? 15 : 25 };
    });
  }
}
function examsOn(d) {
  var k = iso(d), out = [];
  PL_SUBJECTS.forEach(function (su) { svExamsFor(su).forEach(function (e) { if (iso(e.d) === k) out.push({ s: su, label: e.label }); }); });
  return out;
}
function planFor(d) {
  if (!PL_LAST || d < T0 || d > PL_LAST || !PL_SUBJECTS.length) return null;
  var off = offKind(d);
  return { exams: examsOn(d), off: off, sessions: off ? null : (SCHED[iso(d)] || null) };
}

/* ---- day tooltip (shared by both views' mini calendars) ---- */
var DOWNAME = ['Sundays', 'Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays'];
function showDayTip(anchor, d) {
  var daytip = document.getElementById('daytip');
  var p = planFor(d);
  var html = '<b>' + d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) + '</b><br>';
  if (!p) { html += d > PL_LAST ? 'Exams over. Freedom.' : 'Outside your plan.'; }
  else {
    if (p.exams.length) html += p.exams.map(function (e) {
      return '<span class="row"><span class="sw" style="background:' + e.s.c + '"></span><b>Exam · ' + e.s.name + ' — ' + e.label + '</b></span>'; }).join('');
    if (p.off === 'rest') html += 'Rest day — you don’t revise on ' + DOWNAME[d.getDay()] + '.';
    else if (p.off === 'holiday') html += 'Holiday — enjoy it. The work moved along, it didn’t vanish.';
    else if (p.sessions) html += p.sessions.map(function (x) {
      return '<span class="row"><span class="sw" style="background:' + x.s.c + '"></span>' + x.s.name + ' · ' + x.act + ' · ' + x.min + ' min</span>'; }).join('');
    else if (!p.exams.length) html += 'Nothing scheduled.';
  }
  daytip.innerHTML = html;
  var r = anchor.getBoundingClientRect();
  daytip.style.left = Math.min(innerWidth - 270, Math.max(8, r.left - 40)) + 'px';
  daytip.style.top = (r.bottom + 6 + scrollY) + 'px';
  daytip.classList.add('on');
}

/* ---- the modal: injected on boot so both views get the identical sheet ---- */
var PL_CSS = [
  '.daytip{position:absolute;z-index:70;background:#26231e;color:#f2ead9;border-radius:6px;padding:.6rem .8rem;font-size:.78rem;line-height:1.6;max-width:250px;box-shadow:0 10px 24px rgba(20,14,6,.35);display:none;font-family:"Schibsted Grotesk",system-ui,sans-serif}',
  '.daytip.on{display:block}',
  '.daytip b{color:#fff}',
  '.daytip .row{display:flex;gap:7px;align-items:center;white-space:nowrap}',
  '.daytip .sw,.plday .sw{width:8px;height:8px;border-radius:2px;flex:none}',
  '.plmodal{position:fixed;inset:0;background:rgba(38,30,18,.55);display:none;place-items:center;z-index:60;padding:20px;font-family:"Schibsted Grotesk",system-ui,sans-serif;color:#26231e}',
  '.plmodal.open{display:grid}',
  '.plsheet{background:#f6f1e7;border-radius:10px;max-width:1000px;width:100%;max-height:92vh;overflow:auto;padding:26px 30px 30px;position:relative;box-shadow:0 30px 80px rgba(20,14,6,.45)}',
  '.plsheet .x{position:absolute;top:16px;right:18px;width:36px;height:36px;border-radius:50%;border:1px solid #e4dfd2;background:#fffdf8;cursor:pointer;font-size:1rem;color:#57534a}',
  '.plsheet h2{font-family:"Literata",Georgia,serif;margin:0 0 .2rem;font-size:1.6rem}',
  '.plsub{color:#57534a;font-size:.92rem;margin:0 0 1rem;max-width:640px;line-height:1.5}',
  '.plctl{display:flex;flex-wrap:wrap;gap:14px 22px;align-items:center;margin-bottom:1rem;padding:.8rem 1rem;background:#fffdf8;border:1px solid #e4dfd2;border-radius:6px}',
  '.plctl .lbl2{font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#84806f}',
  '.wkday{display:flex;gap:5px}',
  '.wkday button{border:1px solid #e4dfd2;background:#fffdf8;border-radius:4px;padding:.35rem .55rem;font-weight:600;font-size:.78rem;cursor:pointer;color:#57534a;font-family:inherit}',
  '.wkday button[aria-pressed="true"]{background:#5b4632;border-color:#5b4632;color:#fff}',
  '.holhint{font-size:.8rem;color:#57534a}',
  '.plnav{display:flex;align-items:center;gap:10px;margin:.3rem 0 .5rem}',
  '.plnav b{font-family:"Literata",Georgia,serif;font-size:1.05rem;min-width:160px;text-align:center}',
  '.plnav button{width:30px;height:30px;border:1px solid #e4dfd2;background:#fffdf8;border-radius:4px;cursor:pointer}',
  '.plgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px}',
  '.plgrid .hd{font-size:.68rem;font-weight:700;letter-spacing:.1em;color:#84806f;text-transform:uppercase;text-align:center;padding:.2rem 0}',
  '.plday{min-height:88px;min-width:0;overflow:hidden;border:1px solid #efeadf;border-radius:5px;background:#fffdf8;padding:.32rem .45rem;font-size:.72rem;position:relative;cursor:pointer;text-align:left;font-family:inherit}',
  '.plday .dn{font-weight:700;color:#57534a;font-variant-numeric:tabular-nums}',
  '.plday.off{background:transparent;border-style:dashed}',
  '.plday.off .dn{color:#84806f}',
  '.plday.past{opacity:.4;cursor:default}',
  '.plday.hol{background:#f6ecd2;border-color:#e6d5a9}',
  '.plday.hol .dn::after{content:" · holiday";font-weight:600;color:#a3873a}',
  '.plday.examday{outline:2px solid #a3542f;outline-offset:-2px}',
  '.plday .sess{display:flex;gap:5px;align-items:center;margin-top:.24rem;white-space:nowrap;overflow:hidden;color:#57534a}',
  '.plday.today .dn{color:#fff;background:#5b4632;border-radius:3px;padding:0 4px}',
  '.plfoot{margin-top:.9rem;font-size:.8rem;color:#57534a}',
  '.plday .sess b{color:#7a3f24}',
  '.replan{opacity:0;transition:opacity .3s;font-size:.78rem;font-weight:700;color:#4e6e5d}',
  '.replan.on{opacity:1}'
].join('\n');

var PL_HTML =
  '<div class="plsheet">' +
  '<button class="x" id="closepl" aria-label="Close">✕</button>' +
  '<h2>Your revision plan.</h2>' +
  '<p class="plsub" id="plsub"></p>' +
  '<div class="plctl">' +
  '<span class="lbl2">Revise on</span><span class="wkday" id="wkday"></span>' +
  '<span class="lbl2">Holidays</span>' +
  '<span class="holhint">tap any day to mark it as a holiday — sessions move around it</span>' +
  '<span class="replan" id="replan">replanned ✓</span></div>' +
  '<div class="plnav"><button id="plprev" aria-label="Previous month">‹</button><b id="plmon"></b><button id="plnext" aria-label="Next month">›</button></div>' +
  '<div class="plgrid" id="plgrid"></div>' +
  '<p class="plfoot">Built from your subjects and the exam boards&rsquo; own timetables &mdash; no dates to type in. ' +
  'Runs to your last paper; each subject drops out of the rotation once it&rsquo;s been sat. ' +
  '<em>(Prototype uses a provisional summer-2027 timetable.)</em></p></div>';

var plview = new Date(PLNOW.getFullYear(), PLNOW.getMonth(), 1);
function flashReplan() {
  var el = document.getElementById('replan'); if (!el) return;
  el.classList.add('on'); clearTimeout(flashReplan._t);
  flashReplan._t = setTimeout(function () { el.classList.remove('on'); }, 1500);
}
function replan() {
  buildSchedule(); buildPlan(); flashReplan();
  if (PL_ONCHANGE) try { PL_ONCHANGE(); } catch (e) {}
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
      cell.innerHTML = '<span class="dn">' + dd + '</span>';
      var p = planFor(d);
      if (d < T0) cell.classList.add('past');
      if (iso(d) === iso(PLNOW)) cell.classList.add('today');
      if (p && p.exams.length) {
        cell.classList.add('examday');
        p.exams.forEach(function (e) {
          cell.innerHTML += '<span class="sess"><span class="sw" style="background:' + e.s.c + '"></span><b>EXAM · ' + e.s.tab + '</b></span>'; });
      }
      if (p && p.off === 'rest') cell.classList.add('off');
      else if (p && p.off === 'holiday') cell.classList.add('hol');
      else if (p && p.sessions) p.sessions.forEach(function (x) {
        cell.innerHTML += '<span class="sess"><span class="sw" style="background:' + x.s.c + '"></span>' + x.s.tab + ' · ' + x.act + '</span>'; });
      if (d >= T0 && d <= PL_LAST && !(p && p.off === 'rest')) {
        cell.title = (p && p.off === 'holiday') ? 'Tap to unmark this holiday' : 'Tap to mark as a holiday';
        cell.onclick = function () {
          var id = iso(d), ix = PLANP.hols.indexOf(id);
          if (ix >= 0) PLANP.hols.splice(ix, 1); else PLANP.hols.push(id);
          planSave(); replan();
        };
      }
      plgrid.appendChild(cell);
    })(dd);
  }
}

function svPlannerBoot(SUBJECTS, opts) {
  opts = opts || {};
  PL_SUBJECTS = SUBJECTS;
  PL_LAST = svFirstLast(SUBJECTS).last;
  PL_ONCHANGE = opts.onChange || null;
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
    m.addEventListener('click', function (e) { if (e.target === m) m.classList.remove('open'); });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.cal .d') && !e.target.closest('.calgrid .d') && !e.target.closest('.daytip')) tip.classList.remove('on');
    });
  }
  buildSchedule();
  /* staging: ?plan=YYYY-MM opens the planner at that month */
  var q = new URLSearchParams(location.search).get('plan');
  if (q !== null) {
    if (/^\d{4}-\d{2}$/.test(q)) plview = new Date(+q.slice(0, 4), +q.slice(5, 7) - 1, 1);
    svPlannerOpen();
  }
}

function svPlannerOpen(month) {
  if (month instanceof Date) plview = new Date(month.getFullYear(), month.getMonth(), 1);
  document.getElementById('plsub').textContent = 'Runs to your last exam on '
    + PL_LAST.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
    + '. Each subject drops out once its final paper is sat. Switch off the days you keep free, tap any date to mark a holiday — it replans itself, nothing is lost.';
  buildWk(); buildPlan();
  document.getElementById('plmodal').classList.add('open');
}
