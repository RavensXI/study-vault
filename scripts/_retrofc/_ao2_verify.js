/**
 * VERIFY the AO2-denial fix for an AQA English Literature modern-text unit.
 * Re-fetches from Supabase and re-derives every rule; the report is read only
 * to learn which audio objects to probe, never to decide pass/fail.
 *
 * AQA 8702 Paper 2 Section A (modern texts): 30 marks + 4 SPaG,
 * AO1 = 12, AO2 = 12, AO3 = 6.
 *
 * Usage: node scripts/_retrofc/_ao2_verify.js dna
 *        node scripts/_retrofc/_ao2_verify.js pigeon-english
 */
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs = require('fs'), path = require('path'), https = require('https');

const UNITS = {
  dna: {
    id: 'b6e2b49c-9afe-4789-9eef-aa35d1ff822d',
    dir: path.join(__dirname, 'units', 'english-literature-aqa__dna'),
    present: [
      [1, 'exam_tip_html', 'AO2 (Kelly’s methods and their effects, 12 marks)'],
      [4, 'exam_tip_html', 'AO2 is worth 12 of the 30 marks'],
      [7, 'description', 'AO1 and AO2 weighted equally'],
      [7, 'content_html', 'the 30 marks are split AO1 12, AO2 12 and AO3 6'],
      [7, 'content_html', 'delivers four things'],
      [7, 'content_html', 'AO2 carries 12 marks'],
      [7, 'content_html', 'AO2 rewards analysis of the <strong>effect</strong>'],
      [7, 'content_html', 'What four things does a strong modern text essay deliver?'],
      [7, 'conclusion_html', 'AO1 (12 marks) and AO2 (12 marks'],
    ],
    gone: [
      [1, 'exam_tip_html', 'no AO2'],
      [4, 'exam_tip_html', 'no AO2'],
      [7, 'description', 'no AO2'],
      [7, 'conclusion_html', 'no AO2'],
      [7, 'content_html', 'Close language analysis is usually not the focus'],
      [7, 'content_html', 'Why Language-Technique Spotting Is Not the Focus'],
      [7, 'content_html', 'Check your exam board’s specimen paper'],
      [7, 'content_html', 'three things'],
    ],
  },
  'pigeon-english': {
    id: 'c6c35959-6cb5-487d-97a9-c96da6facd5d',
    dir: path.join(__dirname, 'units', 'english-literature-aqa__pigeon-english'),
    present: [
      [7, 'conclusion_html', 'AO2 (12 marks — Kelman’s methods)'],
      [7, 'conclusion_html', 'AO2 carries as much as AO1'],
      [7, 'content_html', '30 marks split AO1 12, AO2 12 and AO3 6'],
    ],
    gone: [
      [7, 'conclusion_html', 'no AO2'],
      [7, 'content_html', 'Check your exam board’s specimen paper'],
    ],
  },
};

const SLUG = process.argv[2];
const CFG = UNITS[SLUG];
if (!CFG) { console.error(`unknown unit "${SLUG}"; known: ${Object.keys(UNITS).join(', ')}`); process.exit(1); }

async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

function ranged(url) {
  return new Promise((res) => {
    const req = https.request(url, { headers: { 'User-Agent': 'Mozilla/5.0', Range: 'bytes=0-3' } }, (r) => {
      const chunks = [];
      r.on('data', (c) => chunks.push(c));
      r.on('end', () => res({ status: r.statusCode, lm: r.headers['last-modified'], magic: Buffer.concat(chunks) }));
    });
    req.on('error', (e) => res({ status: 'ERR ' + e.message }));
    req.end();
  });
}

// Every way this corpus has been caught denying AO2.
const DENIAL = [
  /no AO2/i,
  /without AO2/i,
  /AO2 is not assessed/i,
  /AO2 (is )?NOT (formally )?tested/i,
  /Which (assessment objective|Assessment Objective) is NOT/i,
  /AO2 — (language|there is no extract)/i,
  /language analysis is not the focus/i,
  /close language analysis is (usually )?not/i,
  /you do not need to analyse language/i,
  /not what earns marks on a modern text essay/i,
];

(async () => {
  const rows = await q(`lessons?unit_id=eq.${CFG.id}&select=id,lesson_number,title,status,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest&order=lesson_number`);
  const by = new Map(rows.map((r) => [r.lesson_number, r]));
  let fail = 0;
  const ok = (cond, msg) => { console.log(`${cond ? 'ok  ' : 'FAIL'} ${msg}`); if (!cond) fail++; };

  console.log(`=== AO2 VERIFY: english-literature-aqa / ${SLUG} (${rows.length} lessons) ===`);

  console.log('--- no AO2 denial survives anywhere in the unit ---');
  for (const r of rows) {
    const all = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + (r.description || '') +
      JSON.stringify([r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
    const hits = DENIAL.filter((re) => re.test(all)).map((re) => re.source);
    ok(hits.length === 0, `L${String(r.lesson_number).padStart(2, '0')}${hits.length ? '  ' + hits.join(' | ') : ''}`);
  }

  console.log('--- removed strings ---');
  for (const [n, f, s] of CFG.gone) {
    const hit = (by.get(n)[f] || '').includes(s);
    ok(!hit, `L${n}.${f}: "${s.slice(0, 56)}"`);
  }
  console.log('--- required strings ---');
  for (const [n, f, s] of CFG.present) {
    const hit = (by.get(n)[f] || '').includes(s);
    ok(hit, `L${n}.${f}: "${s.slice(0, 56)}"`);
  }

  console.log('--- knowledge checks that name the AOs must teach all four ---');
  for (const r of rows) {
    for (const [i, kc] of (r.knowledge_checks || []).entries()) {
      if (!/assessment objective/i.test(kc.q || '')) continue;
      if (kc.type === 'match') {
        const has = (kc.left || []).includes('AO2');
        ok(has, `L${r.lesson_number} KC${i + 1} match includes AO2 (left=${JSON.stringify(kc.left)})`);
        const n = (kc.left || []).length;
        const perm = (kc.right || []).length === n && (kc.order || []).length === n &&
          [...(kc.order || [])].sort((a, b) => a - b).join(',') === [...Array(n).keys()].join(',');
        ok(perm, `L${r.lesson_number} KC${i + 1} match shape valid (${n} rows, order is a permutation)`);
        const ao2Right = (kc.right || [])[(kc.order || [])[(kc.left || []).indexOf('AO2')]] || '';
        ok(/method/i.test(ao2Right), `L${r.lesson_number} KC${i + 1} AO2 maps to a methods descriptor: "${ao2Right}"`);
      } else {
        const chosen = (kc.options || [])[kc.correct] || '';
        ok(/AO1.*AO2.*AO3.*AO4/.test(chosen), `L${r.lesson_number} KC${i + 1} keyed answer = "${chosen}"`);
      }
    }
  }

  console.log('--- KC / flashcard shape ---');
  for (const r of rows) {
    for (const [i, kc] of (r.knowledge_checks || []).entries()) {
      if (kc.type === 'match') {
        const l = (kc.left || []).length, rr = (kc.right || []).length, o = (kc.order || []).length;
        const perm = [...(kc.order || [])].sort((a, b) => a - b).join(',') === [...Array(o).keys()].join(',');
        if (!(l === rr && rr === o && perm)) { console.log(`FAIL L${r.lesson_number} KC${i + 1} match shape`); fail++; }
      } else {
        if (kc.answers) { console.log(`FAIL L${r.lesson_number} KC${i + 1} non-canonical answers[]`); fail++; }
        if (!Array.isArray(kc.options) || typeof kc.correct !== 'number' || kc.correct < 0 || kc.correct >= kc.options.length) { console.log(`FAIL L${r.lesson_number} KC${i + 1} correct/options`); fail++; }
      }
    }
    for (const [i, fc] of (r.flashcard_questions || []).entries()) {
      if (!fc.q || !fc.a) { console.log(`FAIL L${r.lesson_number} FC${i + 1} empty side`); fail++; }
    }
  }
  console.log('  (no FAIL above = ok)');

  console.log('--- entity sweep on plain-text fields ---');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  for (const r of rows) {
    const j = JSON.stringify([r.knowledge_checks, r.flashcard_questions, r.glossary_terms]) + (r.description || '');
    const e = j.match(ENT);
    if (e) { console.log(`FAIL entity L${r.lesson_number}`, [...new Set(e)]); fail++; }
  }
  console.log('  (no FAIL above = ok)');

  console.log('--- narration manifest integrity ---');
  for (const r of rows) {
    const html = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map((m) => m[1]);
    const man = new Set((r.narration_manifest || []).map((e) => e.id));
    const missing = ids.filter((i) => !man.has(i));
    const orphan = [...man].filter((i) => !ids.includes(i));
    const bad = (r.narration_manifest || []).filter((e) => !e.src || !/^https:\/\/pub-.*\.mp3$/.test(e.src));
    ok(!missing.length && !orphan.length && !bad.length,
      `L${String(r.lesson_number).padStart(2, '0')} ids=${ids.length} manifest=${man.size} missing=${missing.length} orphan=${orphan.length} badsrc=${bad.length}`);
  }

  console.log('--- truncated revision tips ---');
  let tips = 0;
  for (const r of rows) {
    const t = [...((r.content_html || '').matchAll(/data-revision-tip="([^"]*)"/g))].map((m) => m[1]).filter((x) => /\.\.\.$|…$/.test(x) || x.length < 25);
    if (t.length) { console.log(`FAIL L${r.lesson_number}`, t); tips += t.length; }
  }
  console.log(tips ? '' : '  (none = ok)');
  fail += tips;

  console.log('--- regenerated audio: live ranged GET + freshness ---');
  const rep = JSON.parse(fs.readFileSync(path.join(CFG.dir, '_ao2_report.json'), 'utf8'));
  const clips = (rep.renarration || {}).clips || [];
  ok(clips.length > 0, `report lists ${clips.length} regenerated clip(s)`);
  for (const c of clips) {
    const manEntry = (by.get(c.lesson).narration_manifest || []).find((e) => e.id === c.id);
    ok(!!manEntry && manEntry.src === c.url, `L${c.lesson} ${c.id} manifest src matches the uploaded object`);
    const r = await ranged(c.url);
    const fresh = r.lm && (Date.now() - new Date(r.lm).getTime()) < 6 * 3600 * 1000;
    const sync = r.magic && r.magic[0] === 0xff;
    ok((r.status === 200 || r.status === 206) && fresh && sync,
      `L${c.lesson} ${c.id} -> ${r.status}, Last-Modified ${r.lm}, mp3-sync=${sync}`);
  }

  console.log(`\n=== AO2 VERIFY (${SLUG}) ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  const bk = JSON.parse(fs.readFileSync(path.join(CFG.dir, '_ao2_backup.json'), 'utf8'));
  console.log(`backup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(CFG.dir, '_ao2_backup.json')).size} bytes`);
  process.exit(fail === 0 ? 0 : 1);
})();
