/**
 * AO2-DENIAL FIX — english-literature-aqa / pigeon-english.
 *
 * Same error class as Blood Brothers L7 before its retro fact-check fix: the
 * unit tells students that AO2 is not assessed on the AQA modern-text question.
 * It is. AQA 8702 Paper 2 Section A (modern texts) is marked out of 30 plus 4
 * for SPaG, and the 30 split AO1=12, AO2=12, AO3=6.
 *
 * This unit's denial is narrower than DNA's: the prose already tells students
 * that close language analysis deepens the argument, so only the Key Takeaways
 * bullet, the assessment-objective knowledge check, and the weightings hedge
 * that sends a student off to check whether AO2 counts are wrong.
 *
 * SCOPE: the AO2-denial claims and the KC / flashcard items that depend on them.
 * Deliberately NOT touched: practice_questions type labels and band ladders
 * (a separate mechanical sweep owns those).
 *
 * Backs up every field it changes INCREMENTALLY (written BEFORE each PATCH) to
 * _ao2_backup.json, then PATCHes id=eq. per row.
 *
 * Usage: node scripts/_retrofc/units/english-literature-aqa__pigeon-english/_ao2_fix.js --dry-run
 *        node scripts/_retrofc/units/english-literature-aqa__pigeon-english/_ao2_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_ao2_backup.json');
const REPORT = path.join(DIR, '_ao2_report.json');
const LOGF = path.join(DIR, '_ao2_fix.log');
const UNIT = 'c6c35959-6cb5-487d-97a9-c96da6facd5d';
const SUBJECT = 'english-literature-aqa', UNITSLUG = 'pigeon-english';

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

// ---------------------------------------------------------------- text edits
// [lessonNumber, field, oldSubstring, newSubstring, severity, note]
const EDITS = [
  [7, 'conclusion_html',
    'The essay tests AO1 (analysis), AO3 (context), and AO4 (SPaG). No extract, no AO2. Memorise quotations and embed context throughout.',
    'The essay tests AO1 (12 marks), AO2 (12 marks — Kelman’s methods), AO3 (6 marks — context) and AO4 (4 marks — SPaG). There is no printed extract, but AO2 carries as much as AO1 — memorise quotations, analyse how Kelman writes, and embed context throughout.',
    'HIGH', 'FALSE: "No extract, no AO2." AO2 IS assessed on AQA 8702 Paper 2 Section A and is worth 12 of the 30 marks (AO1=12, AO2=12, AO3=6, plus 4 for AO4/SPaG). The absence of a printed extract does not remove AO2. This is the last thing a student reads in the unit, and it contradicts the lesson\'s own advice two screens earlier that close language analysis deepens the argument.'],
  [7, 'content_html',
    'Check your exam board’s specimen paper for the precise assessment weightings that apply to your question.',
    'On AQA Paper 2 Section A the weightings are fixed: 30 marks split AO1 12, AO2 12 and AO3 6, plus 4 marks for spelling, punctuation and grammar.',
    'HIGH', 'vague hedge in board-specific AQA content. It is what let the false "no AO2" bullet stand: instead of stating the weightings the lesson sent the student away to look them up. Replaced with the real AQA split so the correction holds.'],
];

// ------------------------------------------------------- KC / flashcard edits
function fixKnowledgeChecks(num, kcs) {
  if (num !== 7 || !Array.isArray(kcs)) return { out: kcs, notes: [] };
  const notes = [];
  const out = kcs.map((kc, i) => {
    const e = { ...kc };
    if (/Which assessment objectives are tested in the AQA Modern Texts essay/i.test(e.q || '')) {
      const before = JSON.stringify({ q: e.q, correct: e.correct, options: e.options });
      e.options = ['AO1 and AO2 only', 'AO1, AO2 and AO3 only', 'AO2, AO3 and AO4 only', 'AO1, AO2, AO3 and AO4'];
      e.correct = 3;
      notes.push({ severity: 'HIGH', where: `knowledge_checks[${i}]`,
        note: 'the keyed answer was "AO1, AO3, and AO4", i.e. the check TAUGHT that AO2 is not assessed, and no option stated the true set. Option set rewritten so the correct answer exists and is keyed.',
        before, after: JSON.stringify({ q: e.q, correct: e.correct, options: e.options }) });
    }
    return e;
  });
  return { out, notes };
}

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== AO2-DENIAL FIX: ${SUBJECT} / ${UNITSLUG} ===`);
  L(`run: ${new Date().toISOString()}   mode: ${DRY ? 'DRY RUN' : 'LIVE'}`);

  const cols = 'id,lesson_number,title,slug,description,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  L(`fetched ${rows.length} lessons (live: ${rows.filter((r) => r.status === 'live').length})\n`);

  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  const patches = new Map();
  const noteMap = new Map();
  const addNote = (n, o) => { if (!noteMap.has(n)) noteMap.set(n, []); noteMap.get(n).push(o); };

  for (const [num, field, oldS, newS, sev, note] of EDITS) {
    const row = byNum.get(num);
    if (!row) { L(`  !! L${num} not found`); process.exitCode = 1; continue; }
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) {
      L(`  !! L${num}.${field}: PATTERN NOT FOUND -> ${note.slice(0, 80)}`);
      L(`     looking for: ${oldS.slice(0, 140)}`);
      process.exitCode = 1;
      continue;
    }
    if (!patches.has(num)) patches.set(num, {});
    patches.get(num)[field] = cur.replace(oldS, newS);
    addNote(num, { severity: sev, where: field, note, before: oldS, after: newS });
  }

  for (const row of rows) {
    const num = row.lesson_number;
    const k = fixKnowledgeChecks(num, row.knowledge_checks);
    if (JSON.stringify(k.out) !== JSON.stringify(row.knowledge_checks)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).knowledge_checks = k.out;
    }
    k.notes.forEach((o) => addNote(num, o));
  }

  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT, subject: SUBJECT, unit: UNITSLUG,
    purpose: 'AO2-denial fix (AQA 8702 Paper 2 Section A: 30 + 4, AO1=12 AO2=12 AO3=6)', lessons: [],
  };
  const report = {
    generated_at: new Date().toISOString(), subject: SUBJECT, unit: UNITSLUG,
    purpose: 'AO2-denial fix', lessons_total: rows.length, lessons: [],
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
    writeState();   // persisted BEFORE the write

    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}   fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        [${n.severity}] ${n.where}: ${n.note.slice(0, 150)}`);
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
  report.findings_total = report.lessons.reduce((a, l) => a + l.findings.length, 0);
  L(`findings fixed: ${report.findings_total}`);
  writeState();
  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
