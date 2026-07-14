/* ============================================================
   SVDash — the ONE data layer both dashboard views share.
   dash-classic.html and dash-desk4.html are two skins over the
   same student: wizard state (sv-welcome), account state (sv-user),
   lesson completions (sv-lessons-done), the subject catalog, and
   the live unit fetch all live HERE, once.

   Pages call:  svDashInit(SUBJECTS, { view:'classic'|'desk',
                                       onUnits: fn  // after live units land
                                     })
   Globals provided: _dq, NAMEC, BOARDLBL, SUPA, ANON, SUBSLUG,
   FIRSTUNIT, PFAM, DRAMA_PLAYS, WIZ, DAYONE, SVUSER, DONE,
   doneIn(), keepUnit(), dayOneUrl().
   Staging hooks (QA): ?snap ?picked= ?boards= ?tsel= ?done=
   ============================================================ */

var _dq = new URLSearchParams(location.search);
if (_dq.has('snap')) {
  document.body.classList.add('ready');
  var _snapst = document.createElement('style');
  _snapst.textContent = '*{transition:none!important;animation:none!important}';
  document.head.appendChild(_snapst);
}

/* every free-tier subject family: name, spine colour, short tab label */
var NAMEC = { maths: ['Mathematics', '#4e5f66', 'Maths'], lang: ['English Language', '#5b7285', 'English'],
  lit: ['English Literature', '#7d5a78', 'Lit'], science: ['Combined Science', '#4e6e5d', 'Science'],
  triple: ['Triple Science', '#3d5c50', 'Triple'], history: ['History', '#8a5a44', 'History'],
  geog: ['Geography', '#6d7a4e', 'Geog'], french: ['French', '#5c72a4', 'French'],
  spanish: ['Spanish', '#a2643f', 'Spanish'], german: ['German', '#7c4a52', 'German'],
  cs: ['Computer Science', '#54606e', 'CS'], business: ['Business', '#3f5570', 'Business'],
  pe: ['Physical Education', '#a34a3a', 'PE'], psych: ['Psychology', '#9c6b74', 'Psych'],
  rs: ['Religious Studies', '#6f5b91', 'RS'], socio: ['Sociology', '#85688f', 'Sociology'],
  econ: ['Economics', '#35594e', 'Econ'], stats: ['Statistics', '#557a8a', 'Stats'],
  media: ['Media Studies', '#6b4f63', 'Media'], film: ['Film Studies', '#4a4a52', 'Film'],
  drama: ['Drama', '#8d3f4c', 'Drama'], music: ['Music', '#446272', 'Music'],
  mtech: ['Music Technology', '#4c5480', 'M-Tech'], dt: ['Design & Technology', '#8a713b', 'D&T'],
  eng: ['Engineering', '#5a6068', 'Eng'], electronics: ['Electronics', '#8f5b31', 'Electr'],
  it: ['IT', '#4f6d7d', 'IT'], astro: ['Astronomy', '#3c4a6b', 'Astro'],
  geology: ['Geology', '#6e6459', 'Geology'], classics: ['Classical Civilisation', '#9a8a5a', 'Classics'],
  citizenship: ['Citizenship', '#5d5f8d', 'Citizen'], food: ['Food & Nutrition', '#a8842f', 'Food'],
  hosp: ['Hospitality & Catering', '#67424e', 'Hosp'], hsc: ['Health & Social Care', '#4e7d78', 'H&SC'] };
var BOARDLBL = { aqa: 'AQA', edexcel: 'Edexcel', ocr: 'OCR', eduqas: 'Eduqas / WJEC', ncfe: 'NCFE' };

var SUPA = 'https://baipckgywpnwapobwtsy.supabase.co';
var ANON = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';

/* verified platform slugs (queried from Supabase, 12 Jul) */
var SUBSLUG = {
  maths: { aqa: 'maths-aqa', edexcel: 'maths-edexcel', ocr: 'maths-ocr', eduqas: 'maths-eduqas' },
  lang: { aqa: 'english-language-aqa', edexcel: 'english-language-edexcel', ocr: 'english-language-ocr', eduqas: 'english-language-eduqas' },
  lit: { aqa: 'english-literature-aqa', edexcel: 'english-literature-edexcel', ocr: 'english-literature-ocr', eduqas: 'english-literature-eduqas' },
  science: { aqa: 'science-aqa', edexcel: 'science-edexcel', ocr: 'science-ocr' },
  triple: { aqa: 'separate-sciences', edexcel: 'separate-sciences-edexcel', ocr: 'separate-sciences-ocr' },
  history: { aqa: 'history-aqa', edexcel: 'history-edexcel', ocr: 'history-ocr', eduqas: 'history-eduqas' },
  geog: { aqa: 'geography-aqa', edexcel: 'geography-edexcel-a', ocr: 'geography-ocr', eduqas: 'geography-eduqas' },
  french: { aqa: 'french-aqa', edexcel: 'french-edexcel', eduqas: 'french-eduqas' },
  spanish: { aqa: 'spanish-aqa', edexcel: 'spanish-edexcel', eduqas: 'spanish-eduqas' },
  german: { aqa: 'german-aqa', edexcel: 'german-edexcel' },
  cs: { aqa: 'computer-science-aqa', edexcel: 'computer-science-edexcel', ocr: 'computer-science', eduqas: 'computer-science-eduqas' },
  business: { aqa: 'business-aqa', edexcel: 'business-edexcel', ocr: 'business-ocr' },
  pe: { aqa: 'physical-education-aqa', edexcel: 'physical-education-edexcel', ocr: 'physical-education-ocr' },
  psych: { aqa: 'psychology-aqa' },
  rs: { aqa: 'religious-studies-aqa', edexcel: 'religious-studies-edexcel', ocr: 'religious-studies-ocr', eduqas: 'religious-studies-eduqas' },
  socio: { aqa: 'sociology-aqa', eduqas: 'sociology-eduqas' },
  econ: { aqa: 'economics-aqa' }, stats: { aqa: 'statistics-aqa' }, media: { aqa: 'media-studies-aqa' },
  film: { eduqas: 'film-studies-eduqas' }, drama: { aqa: 'drama-aqa' }, music: { aqa: 'music-aqa' },
  mtech: { ncfe: 'music-technology' },
  dt: { aqa: 'design-technology', eduqas: 'design-technology-eduqas' },
  eng: { aqa: 'engineering-aqa', eduqas: 'engineering-eduqas' },
  electronics: { eduqas: 'electronics-eduqas' }, it: { ocr: 'it-ocr' }, astro: { edexcel: 'astronomy-edexcel' },
  geology: { eduqas: 'geology-eduqas' }, classics: { ocr: 'classical-civilisation-ocr' },
  citizenship: { aqa: 'citizenship-aqa' },
  food: { aqa: 'food-preparation-and-nutrition-aqa', eduqas: 'food-preparation-and-nutrition-eduqas' },
  hosp: { eduqas: 'hospitality-catering' },
  hsc: { edexcel: 'health-social-care-edexcel', ocr: 'health-social-care-ocr', eduqas: 'health-social-care-eduqas' }
};
/* first unit per platform subject (queried from Supabase, 12 Jul) */
var FIRSTUNIT = {"astronomy-edexcel":"naked-eye-astronomy","business-aqa":"business-real-world","business-edexcel":"investigating-small-business","business-ocr":"business-activity-marketing-people","cambridge-nationals-child-development":"health-and-well-being-for-child-development","cambridge-nationals-creative-imedia":"creative-imedia-in-the-media-industry","cambridge-nationals-engineering-design":"principles-of-engineering-design","cambridge-nationals-engineering-manufacture":"principles-of-engineering-manufacture","cambridge-nationals-engineering-programmable-systems":"principles-of-electronic-and-programmable-systems","cambridge-nationals-enterprise-and-marketing":"enterprise-and-marketing-concepts","cambridge-nationals-sport-science":"reducing-the-risk-of-sports-injuries","cambridge-nationals-sport-studies":"contemporary-issues-in-sport","citizenship-aqa":"politics-participation-active-citizenship","classical-civilisation-ocr":"greek-and-roman-mythology","computer-science":"computer-systems","computer-science-aqa":"algorithms","computer-science-edexcel":"computational-thinking","computer-science-eduqas":"hardware-and-systems","design-technology":"core-technical","design-technology-eduqas":"design-technology-our-world","drama-aqa":"theatre-roles-stagecraft","economics-aqa":"economic-foundations-and-resource-allocation","electronics-eduqas":"discovering-electronics","engineering-aqa":"engineering-materials","engineering-eduqas":"engineering-achievements-and-environment","english-language-aqa":"paper-1-reading","english-language-edexcel":"paper-1-reading","english-language-eduqas":"component-1-reading","english-language-ocr":"component-1-reading","english-literature-aqa":"macbeth","english-literature-edexcel":"macbeth","english-literature-eduqas":"romeo-and-juliet","english-literature-ocr":"anita-and-me","film-studies-eduqas":"film-form-and-language","food-preparation-and-nutrition-aqa":"food-nutrition-and-health","food-preparation-and-nutrition-eduqas":"food-science-and-nutrition","french-aqa":"people-and-lifestyle","french-edexcel":"my-personal-world","french-eduqas":"people-and-lifestyle","geography-aqa":"paper-1","geography-edexcel-a":"paper-1-physical-environment","geography-edexcel-b":"global-geographical-issues","geography-eduqas":"landscapes-physical-processes","geography-ocr":"living-in-the-uk-today","geology-eduqas":"rocks-and-minerals","german-aqa":"people-and-lifestyle","german-edexcel":"my-personal-world","health-social-care-edexcel":"health-and-wellbeing","health-social-care-eduqas":"growth-development-lifespan","health-social-care-ocr":"principles-of-care","history-aqa":"germany-democracy-dictatorship","history-edexcel":"medicine-in-britain","history-eduqas":"conflict-upheaval-england-1337-1381","history-ocr":"international-relations-1918-1975","hospitality-catering":"the-hospitality-and-catering-industry","it-ocr":"it-in-the-digital-world","l12-construction-built-environment":"the-construction-sector","l12-ict":"it-systems-and-services","l12-retail-business":"the-retail-business-environment","l12-sport-and-coaching-principles":"body-systems","maths-aqa":"number","maths-edexcel":"number","maths-eduqas":"number","maths-ocr":"number","media-studies-aqa":"media-language","music-aqa":"western-classical-1650-1910","music-technology":"music-business","physical-education-aqa":"human-body-and-movement","physical-education-edexcel":"fitness-and-body-systems","physical-education-ocr":"physical-factors-affecting-performance","psychology-aqa":"memory","religious-studies-aqa":"christianity-beliefs","religious-studies-edexcel":"paper-1-catholic-christianity","religious-studies-eduqas":"christianity","religious-studies-ocr":"christianity-beliefs-and-teachings","science-aqa":"biology-paper-1","science-edexcel":"biology-paper-1","science-ocr":"biology-paper-1","science-ocr-b":"biology-paper-1","separate-sciences":"biology-paper-1","separate-sciences-edexcel":"biology-paper-1","separate-sciences-ocr":"biology-paper-1","separate-sciences-ocr-b":"biology-you-and-your-genes","sociology-aqa":"studying-society-research-methods","sociology-eduqas":"cultural-transmission-research-methods","spanish-aqa":"people-and-lifestyle","spanish-edexcel":"my-personal-world","spanish-eduqas":"people-and-lifestyle","statistics-aqa":"planning-designing-enquiry"};
var PFAM = ['maths', 'lang', 'french', 'spanish', 'german'];   /* practice-first families */
var DRAMA_PLAYS = ['the-crucible', 'blood-brothers', 'noughts-and-crosses', 'around-the-world-80-days',
  'things-i-know-to-be-true', 'romeo-and-juliet', 'a-taste-of-honey', 'the-great-wave', 'the-empress'];

/* wizard + account + progress state */
var WIZ = null;
try { WIZ = JSON.parse(localStorage.getItem('sv-welcome') || 'null'); } catch (e) {}
if (_dq.get('picked')) {                    /* staging override for renders/QA */
  WIZ = { picked: _dq.get('picked').split(',').filter(function (sl) { return NAMEC[sl]; }), boards: {}, meta: {}, topics: {} };
  (_dq.get('boards') || '').split(',').forEach(function (p) {
    var kv = p.split(':'); if (kv[1]) WIZ.boards[kv[0]] = kv[1]; });
  (_dq.get('tsel') || '').split(',').filter(Boolean).forEach(function (t) {
    var p = t.split('.');
    if (p.length >= 3) {
      var v = p.slice(2).join('.');
      (WIZ.topics[p[0]] = WIZ.topics[p[0]] || {})[p[1]] = v.indexOf('~') >= 0 ? v.split('~') : v;
    }
  });
}
var DAYONE = !!(WIZ && Array.isArray(WIZ.picked) && WIZ.picked.length);
var SVUSER = null;
try { SVUSER = JSON.parse(localStorage.getItem('sv-user') || 'null'); } catch (e) {}
if (_dq.get('user')) SVUSER = { email: _dq.get('user') };   /* staging */

var DONE = {};
try { DONE = JSON.parse(localStorage.getItem('sv-lessons-done')) || {}; } catch (e) {}
if (_dq.get('done')) {                      /* staging: ?done=sub/unit:1.2,... */
  DONE = {};
  _dq.get('done').split(',').forEach(function (p) {
    var kv = p.split(':'); if (kv[1]) DONE[kv[0]] = kv[1].split('.').map(Number); });
}
function doneIn(sub, unit) { return DONE[sub + '/' + unit] || []; }

/* which units belong to THIS student (their topic choices scope the course) */
function keepUnit(su, uslug) {
  var raw = su.topicsRaw || [];
  var allRaw = (WIZ && WIZ.topics && WIZ.topics[su.slug])
    ? Object.values(WIZ.topics[su.slug]).flat() : [];
  if (su.slug === 'history' || su.slug === 'lit')
    return !raw.length || raw.indexOf(uslug) >= 0 || doneIn(su.sub, uslug).length > 0;
  if (su.slug === 'drama')                   /* core units always; plays = the chosen one */
    return DRAMA_PLAYS.indexOf(uslug) < 0 || !raw.length || raw.indexOf(uslug) >= 0 || doneIn(su.sub, uslug).length > 0;
  if (su.slug === 'rs' && allRaw.length)
    return allRaw.some(function (r) { return uslug === r || uslug.indexOf(r + '-') === 0; })
      || doneIn(su.sub, uslug).length > 0;
  return true;
}

/* where does day one actually start? A real lesson if we know the unit,
   the subject's browse page if we don't, nowhere if it isn't built yet. */
function dayOneUrl(su) {
  if (!su || !su.sub) return null;
  if (su.first) return (su.mode === 'p' ? '/practice/' : '/lesson/') + su.sub + '/' + su.first + '/1';
  return '/browse/' + su.sub;
}

/* per-subject exam papers (summer 2027, PROVISIONAL demo timetable — the
   real build reads data/exam-dates-*.json). Students never type these. */
var EXAMS = {
 maths:[[5,20,'Paper 1'],[6,3,'Paper 2'],[6,10,'Paper 3']],
 lang:[[5,24,'Paper 1'],[6,7,'Paper 2']],
 lit:[[5,12,'Paper 1'],[5,19,'Paper 2']],
 science:[[5,11,'Biology 1'],[5,21,'Physics 1'],[6,14,'Physics 2']],
 triple:[[5,11,'Biology 1'],[5,21,'Physics 1'],[6,15,'Physics 2']],
 history:[[5,18,'Paper 1'],[6,8,'Paper 2']],
 geog:[[5,14,'Paper 1'],[5,27,'Paper 2'],[6,2,'Paper 3']],
 french:[[5,25,'Listening & Reading'],[6,1,'Writing']],
 spanish:[[5,26,'Listening & Reading'],[6,2,'Writing']],
 german:[[5,27,'Listening & Reading'],[6,3,'Writing']],
 cs:[[5,13,'Paper 1'],[5,25,'Paper 2']],
 business:[[5,19,'Paper 1'],[6,7,'Paper 2']],
 pe:[[5,17,'Paper 1'],[5,28,'Paper 2']],
 psych:[[5,20,'Paper 1'],[6,11,'Paper 2']],
 rs:[[5,13,'Paper 1'],[5,24,'Paper 2']],
 socio:[[5,21,'Paper 1'],[6,9,'Paper 2']],
 econ:[[5,24,'Paper 1'],[6,8,'Paper 2']],
 stats:[[6,1,'Paper 1'],[6,10,'Paper 2']],
 media:[[5,26,'Paper 1'],[6,4,'Paper 2']],
 film:[[6,1,'Paper 1'],[6,8,'Paper 2']],
 drama:[[5,27,'Written paper']],
 music:[[6,3,'Listening exam']],
 mtech:[[6,4,'Exam']],
 dt:[[6,2,'Written paper']],
 eng:[[6,9,'Written paper']],
 electronics:[[6,11,'Paper 2']],
 it:[[5,14,'Exam']],
 astro:[[5,28,'Paper 1'],[6,10,'Paper 2']],
 geology:[[6,7,'Written paper']],
 classics:[[5,19,'Thematic study'],[6,1,'Literature & culture']],
 citizenship:[[6,4,'Paper 1'],[6,11,'Paper 2']],
 food:[[6,8,'Written paper']],
 hosp:[[6,9,'Exam']],
 hsc:[[5,13,'Exam 1'],[6,6,'Exam 2']]
};
function svExamsFor(su) {
  return (EXAMS[su.slug] || []).map(function (e) { return { d: new Date(2027, e[0] - 1, e[1]), label: e[2] }; });
}
/* first + last exam date across the student's subjects — BOTH dashboards'
   countdowns read this, so they can never disagree */
function svFirstLast(SUBJECTS) {
  var all = [];
  SUBJECTS.forEach(function (su) { all = all.concat(svExamsFor(su)); });
  all.sort(function (a, b) { return a.d - b.d; });
  return { first: all.length ? all[0].d : new Date(2027, 4, 17),
           last: all.length ? all[all.length - 1].d : new Date(2027, 5, 18),
           all: all };
}

/* where should "Start" take this student? The first unfinished lesson of the
   first subject with any progress; null while nothing's started (day-one plan
   stands) or before units load. Single source for both dashboards' plans. */
function svContinueTarget(SUBJECTS) {
  for (var si = 0; si < SUBJECTS.length; si++) {
    var su = SUBJECTS[si];
    if (!su.units || !su.units.length) continue;
    for (var ui = 0; ui < su.units.length; ui++) {
      var u = su.units[ui], set = u[4] || [];
      if (!set.length) continue;
      var k = 1; while (k <= u[1] && set.indexOf(k) >= 0) k++;
      if (k <= u[1])
        return { su: su, unitName: u[0], unitSlug: u[3], total: u[1], num: k,
                 url: '/' + (su.mode === 'p' ? 'practice' : 'lesson') + '/' + su.sub + '/' + u[3] + '/' + k };
    }
  }
  return null;
}

/* lifetime + this-week completion counts. Lesson pages stamp completion dates
   into sv-lessons-when (js/main.js) — lessons finished before stamping existed
   count in the total but not the weekly figure. */
function svDoneStats() {
  var total = 0, k;
  for (k in DONE) total += DONE[k].length;
  var when = {};
  try { when = JSON.parse(localStorage.getItem('sv-lessons-when')) || {}; } catch (e) {}
  var week = 0, cutoff = Date.now() - 7 * 864e5;
  for (k in when) { var d = new Date(when[k]); if (d.getTime() >= cutoff) week++; }
  return { total: total, week: Math.min(week, total) };
}

/* which of today's plan steps are already done — warm-up (sv-warmup), a
   lesson (sv-lessons-when stamped today), flashcards (sv-flash-day). Both
   views cross rows off and relabel Start from this. */
function svPlanState() {
  var today = new Date().toISOString().slice(0, 10);
  var warm = false, cards = false, lesson = false;
  var sim = _dq.get('psim');          /* staging: ?psim=warm.lesson to fake done steps */
  if (sim !== null) {
    var ss = sim.split('.');
    warm = ss.indexOf('warm') >= 0; lesson = ss.indexOf('lesson') >= 0; cards = ss.indexOf('cards') >= 0;
    var m0 = (warm ? 0 : 2) + (lesson ? 0 : 15) + (cards ? 0 : 2);
    return { warm: warm, lesson: lesson, cards: cards, any: warm || lesson || cards, mins: m0 };
  }
  try { var w = JSON.parse(localStorage.getItem('sv-warmup')); warm = !!(w && w.date === today); } catch (e) {}
  try { cards = localStorage.getItem('sv-flash-day') === today; } catch (e) {}
  try {
    var when = JSON.parse(localStorage.getItem('sv-lessons-when')) || {};
    for (var k in when) if (when[k] === today) { lesson = true; break; }
  } catch (e) {}
  var mins = (warm ? 0 : 2) + (lesson ? 0 : 15) + (cards ? 0 : 2);
  return { warm: warm, lesson: lesson, cards: cards,
           any: warm || lesson || cards, mins: mins };
}

/* the student's OWN flashcards + podcasts, drawn from each subject's current
   unit (flashcard_questions come from lessons they've reached; podcasts from
   the whole unit — listening ahead is what the bus is for). Called by both
   dashboards after live units land; cb({deck, pods}). */
function svUnitMedia(SUBJECTS, cb) {
  var srcs = [];
  SUBJECTS.forEach(function (su) {
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
    if (unit) srcs.push({ su: su, unit: unit, next: next });
  });
  if (!srcs.length) { cb({ deck: [], pods: [] }); return; }
  Promise.all(srcs.map(function (s) {
    var url = SUPA + '/rest/v1/lessons?select=lesson_number,title,flashcard_questions,related_media,units!inner(slug,subjects!inner(slug,school_id))'
      + '&units.slug=eq.' + encodeURIComponent(s.unit)
      + '&units.subjects.slug=eq.' + encodeURIComponent(s.su.sub)
      + '&units.subjects.school_id=is.null&order=lesson_number';
    return fetch(url, { headers: { apikey: ANON } })
      .then(function (r) { return r.json(); })
      .then(function (rows) {
        var deck = [], pods = [];
        (rows || []).forEach(function (row) {
          if (row.lesson_number <= s.next) (row.flashcard_questions || []).forEach(function (f) {
            if (f && f.q && f.a) deck.push({ slug: s.su.slug, name: s.su.name, q: f.q, a: f.a,
              sub: s.su.sub, unit: s.unit, n: row.lesson_number });
          });
          var pc = (row.related_media || []).find(function (m) { return m.category === 'Podcasts'; });
          var ep = pc && (pc.items || []).find(function (it) { return it.url && it.url.indexOf('.r2.dev/') >= 0; });
          if (ep) pods.push({ t: row.title || ('Lesson ' + row.lesson_number), s: s.su.name, u: ep.url });
        });
        return { deck: deck, pods: pods };
      })
      .catch(function () { return { deck: [], pods: [] }; });
  })).then(function (per) {
    /* interleave decks across subjects so the mixed deck is genuinely mixed */
    var decks = per.map(function (p) { return p.deck; });
    decks.forEach(function (d) {
      for (var i = d.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = d[i]; d[i] = d[j]; d[j] = t; }
    });
    var deck = [];
    while (decks.some(function (d) { return d.length; }))
      decks.forEach(function (d) { if (d.length) deck.push(d.shift()); });
    cb({ deck: deck, pods: per.reduce(function (a, p) { return a.concat(p.pods); }, []) });
  });
}

/* signed-in avatar menu: who you are, edit subjects, sign out. Signing out
   removes the signed-in marker and the Supabase session token; the device
   keeps its setup and progress (those live locally, not on the account). */
function svAvatarMenu(av) {
  if (!av || !SVUSER || !SVUSER.email) return;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  av.style.cursor = 'pointer';
  av.setAttribute('role', 'button'); av.setAttribute('aria-haspopup', 'true');
  var menu = null;
  function close() { if (menu) { menu.remove(); menu = null; document.removeEventListener('click', onDoc, true); } }
  function onDoc(e) { if (menu && !menu.contains(e.target) && e.target !== av) close(); }
  av.addEventListener('click', function (e) {
    e.stopPropagation();
    if (menu) { close(); return; }
    if (!document.getElementById('sv-avmenu-style')) {
      var st = document.createElement('style'); st.id = 'sv-avmenu-style';
      st.textContent = '.sv-avmenu{position:fixed;z-index:950;min-width:232px;background:#fffdf8;color:#26231e;'
        + 'border:1px solid #e4dfd2;border-radius:10px;box-shadow:0 14px 40px rgba(20,14,6,.22);'
        + 'padding:.45rem;font-family:"Schibsted Grotesk",system-ui,sans-serif;font-size:.9rem}'
        + '.sv-avmenu .who{padding:.5rem .65rem;color:#84806f;font-size:.8rem;border-bottom:1px solid #efeadf;'
        + 'margin-bottom:.35rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
        + '.sv-avmenu button,.sv-avmenu a{display:block;width:100%;text-align:left;background:none;border:none;'
        + 'font:inherit;color:#26231e;padding:.5rem .65rem;border-radius:7px;cursor:pointer;text-decoration:none}'
        + '.sv-avmenu button:hover,.sv-avmenu a:hover{background:#f4efe4}';
      document.head.appendChild(st);
    }
    menu = document.createElement('div'); menu.className = 'sv-avmenu';
    menu.innerHTML = '<div class="who">Signed in as ' + esc(SVUSER.email) + '</div>'
      + '<a href="home-study.html">Edit subjects &amp; boards</a>'
      + '<button type="button" class="out">Sign out</button>';
    document.body.appendChild(menu);
    var r = av.getBoundingClientRect();
    menu.style.top = (r.bottom + 8) + 'px';
    menu.style.left = Math.max(8, Math.min(window.innerWidth - menu.offsetWidth - 8, r.right - menu.offsetWidth)) + 'px';
    menu.querySelector('.out').addEventListener('click', function () {
      if (window.svSignOut) { svSignOut(); return; }   /* push progress, then clean the device */
      try { localStorage.removeItem('sv-user'); } catch (e2) {}
      try { Object.keys(localStorage).forEach(function (k) {
        if (/^sb-.*-auth-token/.test(k)) localStorage.removeItem(k); }); } catch (e2) {}
      location.reload();
    });
    setTimeout(function () { document.addEventListener('click', onDoc, true); }, 0);
  });
  if (_dq.get('menu')) setTimeout(function () { av.click(); }, 80);   /* staging: render it open */
}

/* entry point: swap demo subjects for the student's own, then fetch their
   real course structure and lay their completions over it */
function svDashInit(SUBJECTS, opts) {
  opts = opts || {};
  try { localStorage.setItem('sv-dash-view', opts.view || 'classic'); } catch (e) {}
  if (!DAYONE) return;

  var rawT = WIZ.topics || {};
  SUBJECTS.splice(0, SUBJECTS.length, ...WIZ.picked.filter(function (sl) { return NAMEC[sl]; }).map(function (sl) {
    var board = (WIZ.boards || {})[sl] || '';
    var sub = (SUBSLUG[sl] || {})[board] || null;
    var raw = [];
    var tsl = rawT[sl] || {};
    Object.keys(tsl).sort(function (a, b) { return a - b; }).forEach(function (k) {
      var v = tsl[k];
      (Array.isArray(v) ? v : [v]).forEach(function (x) { raw.push(x); });
    });
    var first = null;
    if (sub) {
      if ((sl === 'history' || sl === 'lit' || sl === 'drama') && raw.length) first = raw[0];
      else if (sl === 'rs' && board === 'aqa' && raw.length) first = raw[0] + '-beliefs';
      else first = FIRSTUNIT[sub] || null;
    }
    return { tab: NAMEC[sl][2], slug: sl, sub: sub, mode: PFAM.indexOf(sl) >= 0 ? 'p' : 'l',
      name: NAMEC[sl][0], c: NAMEC[sl][1], units: [],
      board: (WIZ.meta && WIZ.meta[sl] && WIZ.meta[sl].board) || BOARDLBL[board] || '',
      topics: (WIZ.meta && WIZ.meta[sl] && WIZ.meta[sl].topics) || [],
      topicsRaw: (sl === 'history' || sl === 'lit' || sl === 'drama') ? raw : [], first: first };
  }));

  var subs = SUBJECTS.filter(function (su) { return su.sub && su.mode !== 'p'; })
    .map(function (su) { return su.sub; });
  if (!subs.length) return;
  fetch(SUPA + '/rest/v1/subjects?select=slug,units(slug,name,lesson_count,sort_order)'
      + '&school_id=is.null&slug=in.(' + subs.map(function (x) { return '"' + x + '"'; }).join(',') + ')',
      { headers: { apikey: ANON } })
    .then(function (r) { return r.json(); })
    .then(function (rows) {
      rows.forEach(function (row) {
        var su = SUBJECTS.find(function (x) { return x.sub === row.slug; });
        if (!su) return;
        var us = (row.units || []).sort(function (a, b) { return (a.sort_order || 0) - (b.sort_order || 0); })
          .filter(function (u) { return keepUnit(su, u.slug); });
        if (!us.length) return;
        su.units = us.map(function (u) {
          var dn = doneIn(su.sub, u.slug).filter(function (k) { return k >= 1 && k <= (u.lesson_count || 0); });
          return [u.name, u.lesson_count || 0, dn.length, u.slug, dn];
        });
      });
      if (opts.onUnits) opts.onUnits();
    })
    .catch(function () {});
}
