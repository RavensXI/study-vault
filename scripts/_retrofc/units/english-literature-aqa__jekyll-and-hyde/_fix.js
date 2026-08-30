/**
 * Retro fact-check FIX — english-literature-aqa / jekyll-and-hyde.
 *
 * Backs up every field it changes INCREMENTALLY (written after each lesson)
 * to _backup.json, then PATCHes id=eq. per row.
 *
 * Usage:  node scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_fix.js --dry-run
 *         node scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_backup.json');
const REPORT = path.join(DIR, '_report.json');
const LOGF = path.join(DIR, '_fix.log');
const UNIT = '10151ade-c16f-4736-9626-8166ef02a30b';

const log = [];
const L = (s) => { console.log(s); log.push(s); };

async function q(p, opts) {
  const r = await fetch(`${SB}/rest/v1/${p}`, {
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
    ...opts,
  });
  if (!r.ok) throw new Error(`${p} -> ${r.status} ${await r.text()}`);
  return r.json();
}

const SPAG = 'spelling/grammar (4 marks).\n';

// ---------------------------------------------------------------- text edits
// [lessonNumber, field, oldSubstring, newSubstring, severity, note]
const EDITS = [
  // ---- L2 -----------------------------------------------------------------
  [2, 'content_html',
    'blistered, neglected, with “no bell nor knocker”',
    'blistered, neglected, with “neither bell nor knocker”',
    'MEDIUM', 'misquotation: the text reads "equipped with neither bell nor knocker" (Story of the Door)'],
  [2, 'content_html',
    "emphasize his lack of moral boundaries",
    "emphasise his lack of moral boundaries",
    'LOW', 'US spelling in revision tip (house rule: British English); body text already uses "emphasise"'],

  // ---- L3 -----------------------------------------------------------------
  [3, 'title',
    'Chapters 4–6: The Carew Murder and Incident at the Window',
    'Chapters 4–6: The Carew Murder and Dr Lanyon',
    'HIGH', 'chapter misattribution: "Incident at the Window" is Chapter 7 and is taught in L4. This lesson covers Ch 4-6, ending with the Incident of Dr Lanyon.'],

  // ---- L4 -----------------------------------------------------------------
  [4, 'content_html',
    'his evil side had less “exercise” than his good side.',
    'his evil side had been “much less exercised” than his good side.',
    'MEDIUM', 'misquotation: the text reads "it had been much less exercised and much less exhausted" (Full Statement)'],
  [4, 'content_html',
    'make the supernatural transformation feel more imme..."',
    'make the supernatural transformation feel more immediate."',
    'MEDIUM', 'revision tip truncated mid-word ("more imme...") and shown to students'],
  [4, 'content_html',
    'data-def="The person whose perspective shapes the telling of the story.">narrators</dfn>',
    'data-def="The people whose perspectives shape the telling of a story.">narrators</dfn>',
    'LOW', 'glossary term is plural ("narrators") but the definition was singular'],

  // ---- L5 -----------------------------------------------------------------
  [5, 'content_html',
    'his evil side had “less exercise” — it had been suppressed for years.',
    'his evil side had been “much less exercised” — suppressed for years.',
    'MEDIUM', 'misquotation: the text reads "much less exercised"'],
  [5, 'content_html',
    'what does this size difference symbolize about repression?',
    'what does this size difference symbolise about repression?',
    'LOW', 'US spelling in revision tip'],

  // ---- L6 -----------------------------------------------------------------
  [6, 'content_html',
    'Cover this box and analyze why',
    'Cover this box and analyse why',
    'LOW', 'US spelling in revision tip'],

  // ---- L7 -----------------------------------------------------------------
  [7, 'content_html',
    'Lanyon calls it “unscientific balderdash,” not because the chemistry is wrong, but because it violates the natural order.',
    'Lanyon calls it “unscientific balderdash” because he believes Jekyll has gone “wrong in mind” and abandoned proper scientific method. Stevenson’s own point is different: the chemistry works, and it is the moral cost that destroys Jekyll.',
    'MEDIUM', 'contradicted by the text — Lanyon objects on scientific grounds ("too fanciful", "wrong in mind", "unscientific"), not because the experiment "violates the natural order"'],

  // ---- L8 -----------------------------------------------------------------
  [8, 'content_html',
    'and hisses “like a cornered snake.”',
    'and shrinks back “with a hissing intake of the breath.”',
    'HIGH', 'FABRICATED QUOTATION — "like a cornered snake" appears nowhere in Stevenson. The text reads "Mr. Hyde shrank back with a hissing intake of the breath" (Search for Mr Hyde)'],
  [8, 'content_html',
    'what three specific weather/lighting elements mirror moral confusion..."',
    'and the three weather and lighting elements that mirror moral confusion."',
    'MEDIUM', 'revision tip truncated and shown to students'],
  [8, 'content_html',
    'what type of ending forces readers to draw their own c..."',
    'what type of ending forces readers to draw their own conclusions."',
    'MEDIUM', 'revision tip truncated mid-word ("their own c...")'],
];

// ------------------------------------------------------- JSON-field rewriters
function fixPracticeQuestions(num, qs) {
  if (!Array.isArray(qs)) return { out: qs, notes: [] };
  const notes = [];
  const out = qs.map((pq, i) => {
    const e = { ...pq };
    if ((e.marks || '').includes(SPAG)) {
      e.marks = e.marks.replace(SPAG, '');
      notes.push({ severity: 'HIGH', where: `practice_questions[${i}].marks`,
        note: 'exam claim unsupported by the spec: AQA 8702 Paper 1 is 64 raw marks = Section A Shakespeare (30 + 4 AO4) + Section B 19th-century novel (30). AO4 is 2.5% of the qualification = 4 marks in total, awarded in Section A only. A 19th-century novel answer carries NO SPaG marks.' });
    }
    return e;
  });
  return { out, notes };
}

function fixFlashcards(num, cards) {
  if (!Array.isArray(cards)) return { out: cards, notes: [] };
  const notes = [];
  const out = cards.map((c, i) => {
    const e = { ...c };
    if (num === 2 && /no bell nor knocker/.test(e.q || '')) {
      e.q = e.q.replace("'no bell nor knocker'", "'neither bell nor knocker'");
      notes.push({ severity: 'MEDIUM', where: `flashcard_questions[${i}].q`, note: 'misquotation: text reads "neither bell nor knocker"' });
    }
    if (num === 4 && /less 'exercise' than his good side/.test(e.a || '')) {
      e.a = e.a.replace("it had less 'exercise' than his good side", "it had been 'much less exercised' than his good side");
      notes.push({ severity: 'MEDIUM', where: `flashcard_questions[${i}].a`, note: 'misquotation: text reads "much less exercised"' });
    }
    if (num === 5 && /His evil side had 'less exercise'/.test(e.a || '')) {
      e.a = "His evil side had been 'much less exercised' — suppressed for years.";
      notes.push({ severity: 'MEDIUM', where: `flashcard_questions[${i}].a`, note: 'misquotation: text reads "much less exercised"' });
    }
    if (num === 7 && /a violation of natural order/.test(e.a || '')) {
      e.a = "'Unscientific balderdash' — he rejects it as bad science, not as immoral.";
      notes.push({ severity: 'MEDIUM', where: `flashcard_questions[${i}].a`, note: 'contradicted by the text — Lanyon\'s objection is scientific, not moral' });
    }
    if (num === 8 && /like a cornered snake/.test(e.a || '')) {
      e.a = "'Ape-like fury', 'troglodytic', and a 'hissing intake of the breath' — linking him to degeneration theory.";
      notes.push({ severity: 'HIGH', where: `flashcard_questions[${i}].a`, note: 'FABRICATED QUOTATION — "like a cornered snake" is not in Stevenson' });
    }
    return e;
  });
  return { out, notes };
}

function fixKnowledgeChecks(num, kcs) {
  if (!Array.isArray(kcs)) return { out: kcs, notes: [] };
  const notes = [];
  const out = kcs.map((kc, i) => {
    const e = { ...kc };
    if (num === 5 && Array.isArray(e.options)) {
      const j = e.options.findIndex((o) => /Jekyll’s evil side had ‘less exercise’/.test(o));
      if (j >= 0) {
        e.options = e.options.slice();
        e.options[j] = 'Jekyll’s evil side had been ‘much less exercised’';
        notes.push({ severity: 'MEDIUM', where: `knowledge_checks[${i}].options[${j}]`, note: 'misquotation in the correct answer: text reads "much less exercised"' });
      }
    }
    if (num === 5 && Array.isArray(e.left)) {
      const j = e.left.findIndex((o) => /‘less exercise’/.test(o));
      if (j >= 0) {
        e.left = e.left.slice();
        e.left[j] = '‘much less exercised’';
        notes.push({ severity: 'MEDIUM', where: `knowledge_checks[${i}].left[${j}]`, note: 'misquotation in a match key: text reads "much less exercised"' });
      }
    }
    return e;
  });
  return { out, notes };
}

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== RETRO FACT-CHECK: english-literature-aqa / jekyll-and-hyde ===`);
  L(`run: ${new Date().toISOString()}   mode: ${DRY ? 'DRY RUN' : 'LIVE'}`);

  const cols = 'id,lesson_number,title,slug,description,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  L(`fetched ${rows.length} lessons (live: ${rows.filter(r => r.status === 'live').length})\n`);

  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  const patches = new Map();
  const noteMap = new Map();
  const addNote = (n, o) => { if (!noteMap.has(n)) noteMap.set(n, []); noteMap.get(n).push(o); };

  // 1. text edits
  for (const [num, field, oldS, newS, sev, note] of EDITS) {
    const row = byNum.get(num);
    if (!row) { L(`  !! L${num} not found`); process.exitCode = 1; continue; }
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) {
      L(`  !! L${num}.${field}: PATTERN NOT FOUND -> ${note}`);
      L(`     looking for: ${oldS.slice(0, 100)}`);
      process.exitCode = 1;
      continue;
    }
    if (!patches.has(num)) patches.set(num, {});
    patches.get(num)[field] = cur.replace(oldS, newS);
    addNote(num, { severity: sev, where: field, note, before: oldS, after: newS });
  }

  // 2. JSON-field edits
  for (const row of rows) {
    const num = row.lesson_number;
    const p = fixPracticeQuestions(num, row.practice_questions);
    const f = fixFlashcards(num, row.flashcard_questions);
    const k = fixKnowledgeChecks(num, row.knowledge_checks);
    if (JSON.stringify(p.out) !== JSON.stringify(row.practice_questions)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).practice_questions = p.out;
    }
    if (JSON.stringify(f.out) !== JSON.stringify(row.flashcard_questions)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).flashcard_questions = f.out;
    }
    if (JSON.stringify(k.out) !== JSON.stringify(row.knowledge_checks)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).knowledge_checks = k.out;
    }
    [...p.notes, ...f.notes, ...k.notes].forEach((o) => addNote(num, o));
  }

  // 3. INCREMENTAL backup + patch, lesson by lesson
  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT,
    subject: 'english-literature-aqa', unit: 'jekyll-and-hyde', lessons: [],
  };
  const report = {
    generated_at: new Date().toISOString(),
    subject: 'english-literature-aqa', unit: 'jekyll-and-hyde',
    lessons_total: rows.length, lessons: [],
  };
  const writeState = () => {
    fs.writeFileSync(BACKUP, JSON.stringify(backup, null, 1), 'utf8');
    fs.writeFileSync(REPORT, JSON.stringify(report, null, 1), 'utf8');
  };

  let fieldCount = 0;
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    const before = {};
    for (const k of Object.keys(fields)) before[k] = row[k];
    before.narration_manifest = row.narration_manifest;
    backup.lessons.push({ lesson_number: num, id: row.id, title: row.title, fields_changed: Object.keys(fields), before });
    report.lessons.push({ lesson_number: num, id: row.id, title: row.title,
      fields_changed: Object.keys(fields), findings: noteMap.get(num) || [] });
    writeState();   // <- persisted BEFORE the write; a killed run loses nothing

    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}   fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        [${n.severity}] ${n.where}: ${n.note}`);
    fieldCount += Object.keys(fields).length;
    if (!DRY) {
      await q(`lessons?id=eq.${row.id}`, { method: 'PATCH', body: JSON.stringify(fields) });
      L(`      -> PATCHED`);
      report.lessons[report.lessons.length - 1].patched_at = new Date().toISOString();
      writeState();
    }
    L('');
  }
  L(`${DRY ? 'WOULD PATCH' : 'PATCHED'}: ${patches.size} lessons, ${fieldCount} fields`);
  const counts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
  for (const l of report.lessons) for (const f of l.findings) counts[f.severity]++;
  report.fixed_counts = counts;
  L(`fixed findings: HIGH=${counts.HIGH} MEDIUM=${counts.MEDIUM} LOW=${counts.LOW}`);
  writeState();
  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
