const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs = require('fs'), path = require('path');
const D = __dirname;
const UNIT = '10151ade-c16f-4736-9626-8166ef02a30b';
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

const MUST_GONE = [
  [2, 'content_html', 'no bell nor knocker'],
  [2, 'content_html', 'emphasize'],
  [4, 'content_html', 'less “exercise”'],
  [4, 'content_html', 'more imme..."'],
  [5, 'content_html', '“less exercise”'],
  [5, 'content_html', 'symbolize'],
  [6, 'content_html', 'analyze'],
  [7, 'content_html', 'not because the chemistry is wrong'],
  [8, 'content_html', 'cornered snake'],
  [8, 'content_html', 'moral confusion..."'],
  [8, 'content_html', 'their own c..."'],
  [3, 'title', 'Incident at the Window'],
];
const MUST_PRESENT = [
  [2, 'content_html', '“neither bell nor knocker”'],
  [4, 'content_html', '“much less exercised” than his good side'],
  [4, 'content_html', 'feel more immediate."'],
  [5, 'content_html', 'had been “much less exercised”'],
  [7, 'content_html', 'the chemistry works, and it is the moral cost'],
  [8, 'content_html', 'with a hissing intake of the breath'],
  [3, 'title', 'The Carew Murder and Dr Lanyon'],
];

(async () => {
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,slug,status,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest&order=lesson_number`);
  const by = new Map(rows.map(r => [r.lesson_number, r]));
  let fail = 0;

  console.log('--- removed strings ---');
  for (const [n, f, s] of MUST_GONE) { const hit = (by.get(n)[f] || '').includes(s); console.log(`${hit ? 'FAIL' : 'ok  '} L${n}.${f}: "${s.slice(0, 48)}"`); if (hit) fail++; }
  console.log('--- required strings ---');
  for (const [n, f, s] of MUST_PRESENT) { const hit = (by.get(n)[f] || '').includes(s); console.log(`${hit ? 'ok  ' : 'FAIL'} L${n}.${f}: "${s.slice(0, 48)}"`); if (!hit) fail++; }

  console.log('--- exam claim: no SPaG on any 19th-century novel question ---');
  let spag = 0, bandFail = 0;
  for (const r of rows) for (const [i, pq] of (r.practice_questions || []).entries()) {
    const m = pq.marks || '', t = pq.type || '';
    if (/spelling\/grammar/i.test(m)) { console.log(`FAIL SPaG L${r.lesson_number} pq[${i}]`); spag++; }
    const bands = [...m.matchAll(/([A-Z][A-Za-z\- ]*band) \((\d+)[–\-](\d+)\)/g)].map(x => [x[1], +x[2], +x[3]]);
    const labels = bands.map(b => b[0]);
    if (labels.some((l, j) => labels.indexOf(l) !== j)) { console.log(`FAIL dup band label L${r.lesson_number} pq[${i}]`); bandFail++; }
    const declared = +(t.match(/^(\d+) marks/) || [])[1];
    if (declared && Math.max(...bands.map(b => b[2])) !== declared) { console.log(`FAIL band max != ${declared} L${r.lesson_number} pq[${i}]`); bandFail++; }
    for (let k = 0; k < bands.length - 1; k++) if (bands[k][1] !== bands[k + 1][2] + 1) { console.log(`FAIL band gap L${r.lesson_number} pq[${i}]`); bandFail++; }
  }
  console.log(`spagClaims=${spag}  bandProblems=${bandFail}`); fail += spag + bandFail;

  console.log('--- entity / rival-board / US-spelling sweep ---');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  const BD = /\b(Edexcel|OCR|Eduqas|WJEC)\b/g;
  const USSP = /\b(?:analyze|analyse[sd]?|symbolize|emphasize|organize|recognize|criticize|realize|color|honor|behavior|favor|defense|center)\b/g;
  const USBAD = /\b(?:analyze|symbolize|emphasize|organize|recognize|criticize|realize|color|honor|behavior|favor|defense|center)\b/g;
  for (const r of rows) {
    const j = JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
    const all = j + (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + (r.description || '') + r.title;
    const e = j.match(ENT), b = all.match(BD), u = all.match(USBAD);
    if (e) { console.log(`FAIL entity L${r.lesson_number}`, [...new Set(e)]); fail++; }
    if (b) { console.log(`FAIL board L${r.lesson_number}`, [...new Set(b)]); fail++; }
    if (u) { console.log(`FAIL US spelling L${r.lesson_number}`, [...new Set(u)]); fail++; }
  }

  console.log('--- narration manifest integrity ---');
  for (const r of rows) {
    const html = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]);
    const man = new Set((r.narration_manifest || []).map(e => e.id));
    const missing = ids.filter(i => !man.has(i));
    const orphan = [...man].filter(i => !ids.includes(i));
    const bad = (r.narration_manifest || []).filter(e => !e.src || !/^https:\/\/pub-.*\.mp3$/.test(e.src));
    const ok = !missing.length && !orphan.length && !bad.length;
    console.log(`${ok ? 'ok  ' : 'FAIL'} L${String(r.lesson_number).padStart(2, '0')}  ids=${ids.length} manifest=${man.size} missing=${missing.length} orphan=${orphan.length} badsrc=${bad.length}`);
    fail += missing.length + orphan.length + bad.length;
  }

  console.log('--- truncated revision tips ---');
  for (const r of rows) {
    const t = [...((r.content_html || '').matchAll(/data-revision-tip="([^"]*\.\.\.)"/g))].map(m => m[1]);
    if (t.length) { console.log(`FAIL L${r.lesson_number}`, t.map(x => '…' + x.slice(-40))); fail += t.length; }
  }
  console.log('  (none = ok)');

  console.log(`\n=== VERIFY ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  const bk = JSON.parse(fs.readFileSync(path.join(D, '_backup.json'), 'utf8'));
  console.log(`backup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(D, '_backup.json')).size} bytes`);
  const rep = JSON.parse(fs.readFileSync(path.join(D, '_report.json'), 'utf8'));
  console.log(`report: ${rep.lessons.length} lessons, fixed=${JSON.stringify(rep.fixed_counts)}, renarrated=${rep.renarration ? rep.renarration.verified_ok + '/' + rep.renarration.total : 'none'}`);
})();
