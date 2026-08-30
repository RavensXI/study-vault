/**
 * Retro fact-check VERIFY — english-literature-aqa / blood-brothers.
 * Independently re-derives every rule rather than trusting the fix log.
 */
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs = require('fs'), path = require('path');
const D = __dirname;
const UNIT = '36556966-f4ec-436b-9ce8-736476fab761';
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

const MUST_GONE = [
  [7, 'content_html', 'Look like the innocent flower'],
  [7, 'content_html', 'wait, that’s Macbeth'],
  [7, 'content_html', 'Close language analysis is not the focus here'],
  [7, 'content_html', 'Check your exam board’s specimen paper'],
  [7, 'conclusion_html', 'no extract and no AO2'],
  [1, 'content_html', 'And do we blame superstition for what came to pass'],
  [5, 'content_html', 'And do we blame superstition for what came to pass'],
];
const MUST_PRESENT = [
  [7, 'content_html', 'AO2 is worth 12 of the 30 marks'],
  [7, 'conclusion_html', 'AO2 (12 marks'],
  [1, 'content_html', '“could it be what we, the English, have come to know as class?” — directly invites'],
  [5, 'content_html', '“could it be what we, the English, have come to know as class?” — tells the audience'],
  [5, 'content_html', 'does the blame lie with superstition'],
];

(async () => {
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,slug,status,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest&order=lesson_number`);
  const by = new Map(rows.map(r => [r.lesson_number, r]));
  let fail = 0;

  console.log('--- removed strings ---');
  for (const [n, f, s] of MUST_GONE) { const hit = (by.get(n)[f] || '').includes(s); console.log(`${hit ? 'FAIL' : 'ok  '} L${n}.${f}: "${s.slice(0, 52)}"`); if (hit) fail++; }
  console.log('--- required strings ---');
  for (const [n, f, s] of MUST_PRESENT) { const hit = (by.get(n)[f] || '').includes(s); console.log(`${hit ? 'ok  ' : 'FAIL'} L${n}.${f}: "${s.slice(0, 52)}"`); if (!hit) fail++; }

  console.log('--- exam claim: modern text = 30+4, six distinct bands, no Shakespeare label ---');
  const LADDER = { '26-30': 'Top band', '21-25': 'Upper band', '16-20': 'Upper-mid band', '11-15': 'Mid band', '6-10': 'Lower-mid band', '1-5': 'Lower band' };
  let typeFail = 0, bandFail = 0, spagFail = 0;
  for (const r of rows) for (const [i, pq] of (r.practice_questions || []).entries()) {
    const m = pq.marks || '', t = pq.type || '';
    if (/Shakespeare/i.test(t)) { console.log(`FAIL Shakespeare label L${r.lesson_number} pq[${i}]: ${t}`); typeFail++; }
    if (t !== '30+4 marks — Modern Text Essay') { console.log(`FAIL type L${r.lesson_number} pq[${i}]: ${t}`); typeFail++; }
    // the modern text question DOES carry SPaG, so its presence is required here
    if (!/spelling\/grammar/i.test(m)) { console.log(`FAIL missing SPaG ladder L${r.lesson_number} pq[${i}]`); spagFail++; }
    const bands = [...m.matchAll(/([A-Z][A-Za-z\- ]*band)\s*\(?\s*(\d+)\s*[–\-]\s*(\d+)/g)].map(x => [x[1], +x[2], +x[3]]);
    const labels = bands.map(b => b[0]);
    if (labels.length !== 6) { console.log(`FAIL band count ${labels.length} L${r.lesson_number} pq[${i}]`); bandFail++; }
    if (new Set(labels).size !== labels.length) { console.log(`FAIL dup band label L${r.lesson_number} pq[${i}]: ${labels}`); bandFail++; }
    for (const [lbl, lo, hi] of bands) {
      const want = LADDER[`${lo}-${hi}`];
      if (want && want !== lbl) { console.log(`FAIL band label L${r.lesson_number} pq[${i}]: ${lo}-${hi} labelled "${lbl}", expected "${want}"`); bandFail++; }
    }
    if (bands.length && Math.max(...bands.map(b => b[2])) !== 30) { console.log(`FAIL band max != 30 L${r.lesson_number} pq[${i}]`); bandFail++; }
    for (let k = 0; k < bands.length - 1; k++) if (bands[k][1] !== bands[k + 1][2] + 1) { console.log(`FAIL band gap L${r.lesson_number} pq[${i}]`); bandFail++; }
  }
  console.log(`typeProblems=${typeFail}  bandProblems=${bandFail}  spagProblems=${spagFail}`);
  fail += typeFail + bandFail + spagFail;

  console.log('--- AO claims consistent with AQA mark scheme (AO1=12, AO2=12, AO3=6, AO4=4) ---');
  let aoFail = 0;
  for (const r of rows) {
    const all = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + JSON.stringify([r.knowledge_checks, r.flashcard_questions]);
    if (/no AO2|without AO2|AO2 is not assessed|AO2 — there is no extract/i.test(all)) { console.log(`FAIL L${r.lesson_number} still denies AO2`); aoFail++; }
    for (const kc of r.knowledge_checks || []) {
      if (/assessment objectives/i.test(kc.q || '') && Array.isArray(kc.options)) {
        const chosen = kc.options[kc.correct] || '';
        if (!/AO1.*AO2.*AO3.*AO4/.test(chosen)) { console.log(`FAIL L${r.lesson_number} KC AO answer = "${chosen}"`); aoFail++; }
        else console.log(`ok   L${r.lesson_number} KC AO answer = "${chosen}"`);
      }
    }
  }
  fail += aoFail;

  console.log('--- quotation ceiling: no play quotation over 15 words ---');
  let qFail = 0;
  for (const r of rows) {
    const txt = ((r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '')).replace(/<[^>]+>/g, ' ');
    for (const m of txt.matchAll(/[“]([^”]{1,400})[”]/g)) {
      const body = m[1].trim();
      const w = body.split(/\s+/).filter(Boolean).length;
      // our own model-answer exemplars start "Russell " and are not play quotations
      if (w > 15 && !/^Russell\b/.test(body)) { console.log(`FAIL L${r.lesson_number} quote ${w} words: "${body.slice(0, 70)}"`); qFail++; }
    }
  }
  console.log(qFail ? `  ${qFail} over-length` : '  none over 15 words');
  fail += qFail;

  console.log('--- entity / rival-board / US-spelling sweep ---');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  const BD = /\b(Edexcel|OCR|Eduqas|WJEC)\b/g;
  const USBAD = /\b(?:analyze|symbolize|emphasize|organize|recognize|criticize|realize|color|honor|behavior|favor|defense|center|theater)\b/gi;
  for (const r of rows) {
    const j = JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
    const all = j + (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + (r.description || '') + r.title;
    const e = j.match(ENT), b = all.match(BD), u = all.match(USBAD);
    if (e) { console.log(`FAIL entity L${r.lesson_number}`, [...new Set(e)]); fail++; }
    if (b) { console.log(`FAIL board L${r.lesson_number}`, [...new Set(b)]); fail++; }
    if (u) { console.log(`FAIL US spelling L${r.lesson_number}`, [...new Set(u)]); fail++; }
  }
  console.log('  (no FAIL above = ok)');

  console.log('--- KC / flashcard shape ---');
  for (const r of rows) {
    for (const [i, kc] of (r.knowledge_checks || []).entries()) {
      if (kc.type === 'match') {
        const L = (kc.left || []).length, R = (kc.right || []).length, O = (kc.order || []).length;
        const perm = [...(kc.order || [])].sort((a, b) => a - b).join(',') === [...Array(O).keys()].join(',');
        if (!(L === R && R === O && perm)) { console.log(`FAIL L${r.lesson_number} KC${i + 1} match shape`); fail++; }
      } else {
        if (kc.answers) { console.log(`FAIL L${r.lesson_number} KC${i + 1} non-canonical answers[]`); fail++; }
        if (!Array.isArray(kc.options) || typeof kc.correct !== 'number' || kc.correct < 0 || kc.correct >= kc.options.length) { console.log(`FAIL L${r.lesson_number} KC${i + 1} correct/options`); fail++; }
      }
    }
  }
  console.log('  (no FAIL above = ok)');

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
  let tips = 0;
  for (const r of rows) {
    const t = [...((r.content_html || '').matchAll(/data-revision-tip="([^"]*)"/g))].map(m => m[1]).filter(x => /\.\.\.$|…$/.test(x) || x.length < 25);
    if (t.length) { console.log(`FAIL L${r.lesson_number}`, t); tips += t.length; }
  }
  console.log(tips ? '' : '  (none = ok)');
  fail += tips;

  console.log(`\n=== VERIFY ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  const bk = JSON.parse(fs.readFileSync(path.join(D, '_backup.json'), 'utf8'));
  console.log(`backup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(D, '_backup.json')).size} bytes`);
  const rep = JSON.parse(fs.readFileSync(path.join(D, '_report.json'), 'utf8'));
  console.log(`report: ${rep.lessons.length} lessons, fixed=${JSON.stringify(rep.fixed_counts)}, renarrated=${rep.renarration ? rep.renarration.verified_ok + '/' + rep.renarration.total : 'none'}`);
  process.exit(fail === 0 ? 0 : 1);
})();
