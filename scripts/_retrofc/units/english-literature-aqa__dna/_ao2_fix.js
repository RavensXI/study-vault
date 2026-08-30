/**
 * AO2-DENIAL FIX — english-literature-aqa / dna.
 *
 * Same error class as Blood Brothers L7 before its retro fact-check fix: the
 * unit tells students that AO2 is not assessed on the AQA modern-text question.
 * It is. AQA 8702 Paper 2 Section A (modern texts) is marked out of 30 plus 4
 * for SPaG, and the 30 split AO1=12, AO2=12, AO3=6. AO2 carries exactly as many
 * marks as AO1, so "no AO2 / language analysis is not the focus" steers a
 * student away from 12 of the 30 marks.
 *
 * SCOPE: the AO2-denial claims and the KC / flashcard items that depend on them.
 * Deliberately NOT touched: practice_questions type labels and band ladders
 * (a separate mechanical sweep owns those).
 *
 * Backs up every field it changes INCREMENTALLY (written BEFORE each PATCH) to
 * _ao2_backup.json, then PATCHes id=eq. per row.
 *
 * Usage: node scripts/_retrofc/units/english-literature-aqa__dna/_ao2_fix.js --dry-run
 *        node scripts/_retrofc/units/english-literature-aqa__dna/_ao2_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_ao2_backup.json');
const REPORT = path.join(DIR, '_ao2_report.json');
const LOGF = path.join(DIR, '_ao2_fix.log');
const UNIT = 'b6e2b49c-9afe-4789-9eef-aa35d1ff822d';
const SUBJECT = 'english-literature-aqa', UNITSLUG = 'dna';

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
  // ---- L1: the flat denial in the exam tip --------------------------------
  [1, 'exam_tip_html',
    'You are assessed on AO1 (argument and evidence), AO3 (context), and AO4 (spelling, punctuation, and grammar). There is <strong>no AO2</strong> for modern texts — you do not need to analyse language techniques, but using relevant quotations to support your argument will strengthen your AO1.',
    'You are assessed on AO1 (argument and evidence, 12 marks), AO2 (Kelly’s methods and their effects, 12 marks), AO3 (context, 6 marks), and AO4 (spelling, punctuation, and grammar, 4 marks). AO2 carries exactly as many marks as AO1, so write about <strong>how</strong> Kelly builds the play — its four-act structure, its staging, its silences — as well as what it means.',
    'HIGH', 'FALSE: "There is no AO2 for modern texts — you do not need to analyse language techniques." AO2 IS assessed on AQA 8702 Paper 2 Section A and is worth 12 of the 30 marks (AO1=12, AO2=12, AO3=6, plus 4 for AO4/SPaG). This is the first exam guidance a student meets in the unit.'],

  // ---- L4: the denial repeated in the character-essay tip -----------------
  [4, 'exam_tip_html',
    'Remember: no AO2 for modern texts — focus on what the character reveals about Kelly’s ideas, not on language analysis.',
    'Remember: AO2 is worth 12 of the 30 marks, so write about how Kelly builds the character — the lines he gives them, the moments he stages — as well as what the character reveals about his ideas.',
    'HIGH', 'FALSE: "no AO2 for modern texts ... not language analysis". Same denial as L1, in the tip a student reads immediately before planning a character essay.'],

  // ---- L7: the exam-technique lesson itself -------------------------------
  [7, 'description',
    'AQA modern text essay technique: no extract, no AO2, quotation strategies, model paragraph.',
    'AQA modern text essay technique: no extract, AO1 and AO2 weighted equally, quotation strategies, model paragraph.',
    'HIGH', 'the lesson card summarised the whole lesson as "no AO2". Card text is what a student sees before opening the lesson.'],
  [7, 'content_html',
    'Check your exam board’s specimen paper for the exact mark weightings and time allowance that apply to you.',
    'On AQA Paper 2 Section A the 30 marks are split AO1 12, AO2 12 and AO3 6, with a further 4 marks for spelling, punctuation and grammar.',
    'HIGH', 'vague hedge in board-specific AQA content, sitting in the same paragraph as the closed-book claim. Replaced with the actual AQA weightings, which is what makes the AO2 correction stick — otherwise the lesson still sends the student away to find out whether AO2 counts.'],
  [7, 'content_html',
    'A strong modern text essay on <em>DNA</em> delivers three things: a sustained, personal response to the play supported by references from memory; context (Milgram, 2008 youth violence, moral philosophy, Connections programme) embedded in your analysis; and clear, fluent academic writing. Close language analysis is usually not the focus of this question.',
    'A strong modern text essay on <em>DNA</em> delivers four things: a sustained, personal response to the play supported by references from memory; analysis of Kelly’s methods — the four-act structure, the staging, the silences — and the effects they create; context (Milgram, 2008 youth violence, moral philosophy, Connections programme) embedded in your analysis; and clear, fluent academic writing.',
    'HIGH', 'the Key Fact box ended "Close language analysis is usually not the focus of this question" and listed only three things, dropping the strand worth 12 marks. Methods added as the second thing; "three" becomes "four".'],
  [7, 'content_html',
    'data-revision-tip="Cover this and recall: What three things does a strong modern text essay deliver?"',
    'data-revision-tip="Cover this and recall: What four things does a strong modern text essay deliver?"',
    'HIGH', 'the revision tip on that Key Fact box still asked for three things. Attribute-only edit, so the narrated text is unchanged.'],
  [7, 'content_html',
    'Maintain an analytical style throughout — every paragraph should develop your reading of the play.</p>',
    'Maintain an analytical style throughout — every paragraph should develop your reading of the play. Kelly’s methods are part of that argument: AO2 carries 12 marks, so say what his choices — the four-act structure, the silences, the field they keep returning to — actually do to an audience.</p>',
    'HIGH', 'the section "What Each Strand of Your Essay Needs to Do" listed exactly three strands — argument (AO1), context (AO3), writing quality (AO4) — which is the denial expressed as structure: a student who reads only this section still learns the wrong AO set. AO2 folded into the argument strand rather than inserted as a new narration block, so no manifest re-ordering is needed.'],
  [7, 'content_html',
    '<span>Why Language-Technique Spotting Is Not the Focus</span>',
    '<span>Why Device-Spotting Is Not the Same as Analysis</span>',
    'HIGH', 'the collapsible heading asserted the denial in the student\'s line of sight. Device-spotting really does earn nothing; AO2 analysis of the same choices earns up to 12 marks, and the heading now says which is which.'],
  [7, 'content_html',
    'Identifying language devices (<em>“Kelly uses a metaphor…”</em>) is usually not what earns marks on a modern text essay. You can, and should, discuss structural and dramatic choices — staging, silence, the four-act structure, the field as a recurring space — where they support your argument about Kelly’s ideas. But the focus is on <strong>what Kelly is saying</strong> (ideas, themes, context) rather than a technique checklist. Treat every structural observation as an opportunity to say more about meaning.',
    'Naming a device (<em>“Kelly uses a metaphor…”</em>) earns nothing on its own. AO2 rewards analysis of the <strong>effect</strong> a choice creates, so discuss Kelly’s structural and dramatic choices — staging, silence, the four-act structure, the field as a recurring space — and explain what each one does to an audience. Treat every observation about method as an opportunity to say more about meaning; a technique checklist with no meaning attached still earns nothing.',
    'HIGH', 'the body of that collapsible told students the focus is "what Kelly is saying ... rather than a technique checklist", i.e. that method analysis is optional. Rewritten to keep the true half (labels alone earn nothing) and drop the false half (methods are not the focus).'],
  [7, 'conclusion_html',
    'Paper 2, Section A: one essay question on DNA, 30+4 marks, no extract, no AO2. Focus on AO1 (argument + evidence) and AO3 (context).',
    'Paper 2, Section A: one essay question on DNA, 30+4 marks, no extract. AO1 (12 marks) and AO2 (12 marks — Kelly’s methods) carry equal weight, with AO3 (6 marks) for context and AO4 (4 marks) for SPaG.',
    'HIGH', 'the Key Takeaways bullet — the last thing a student reads — stated "no AO2".'],
];

// ------------------------------------------------------- KC / flashcard edits
function fixKnowledgeChecks(num, kcs) {
  if (num !== 7 || !Array.isArray(kcs)) return { out: kcs, notes: [] };
  const notes = [];
  const out = kcs.map((kc, i) => {
    const e = { ...kc };
    if (/Which assessment objective is NOT assessed for the modern text essay/i.test(e.q || '')) {
      const before = JSON.stringify({ q: e.q, correct: e.correct, options: e.options });
      e.q = 'Which assessment objectives are assessed on the modern text essay?';
      e.options = ['AO1 and AO2 only', 'AO1, AO2 and AO3 only', 'AO2, AO3 and AO4 only', 'AO1, AO2, AO3 and AO4'];
      e.correct = 3;
      notes.push({ severity: 'HIGH', where: `knowledge_checks[${i}]`,
        note: 'the keyed answer was "AO2 (language, form, structure)", i.e. the check TAUGHT that AO2 is not assessed and marked a student wrong for saying it is. Rewritten as a positive question with the true option available.',
        before, after: JSON.stringify({ q: e.q, correct: e.correct, options: e.options }) });
    }
    if (e.type === 'match' && /Match each assessment objective/i.test(e.q || '')) {
      const before = JSON.stringify({ left: e.left, right: e.right, order: e.order });
      e.left = ['AO1', 'AO2', 'AO3', 'AO4'];
      e.right = [
        'Argument, evidence, and personal response',
        'Understanding of context and how it shapes the text',
        'Spelling, punctuation, grammar, and vocabulary',
        'Analysis of the writer’s methods and the effects they create',
      ];
      e.order = [0, 3, 1, 2];   // left[i] matches right[order[i]]
      notes.push({ severity: 'HIGH', where: `knowledge_checks[${i}]`,
        note: 'the match listed only AO1, AO3 and AO4 — the exact false AO set the denial asserted — so it drilled the wrong objective list. AO2 added with its real descriptor; order rechecked as a permutation (left[i] matches right[order[i]]).',
        before, after: JSON.stringify({ left: e.left, right: e.right, order: e.order }) });
    }
    return e;
  });
  return { out, notes };
}

function fixFlashcards(num, fcs) {
  if (num !== 7 || !Array.isArray(fcs)) return { out: fcs, notes: [] };
  const notes = [];
  const out = fcs.map((fc, i) => {
    const e = { ...fc };
    if (/Which Assessment Objective is NOT formally tested on the modern text essay/i.test(e.q || '')) {
      const before = JSON.stringify({ q: e.q, a: e.a });
      e.q = 'How are the 30 marks split on the AQA modern text essay?';
      e.a = 'AO1 12, AO2 12, AO3 6 — plus 4 marks for SPaG (AO4).';
      notes.push({ severity: 'HIGH', where: `flashcard_questions[${i}]`,
        note: 'the card answered "AO2 — language analysis is not the focus". False. Replaced with the real mark split, which is what the card was reaching for.',
        before, after: JSON.stringify({ q: e.q, a: e.a }) });
    }
    if (/Which three things does a strong modern text essay deliver/i.test(e.q || '')) {
      const before = JSON.stringify({ q: e.q, a: e.a });
      e.q = 'Which four things does a strong modern text essay deliver?';
      e.a = 'Personal response with evidence, analysis of Kelly’s methods, embedded context, and fluent writing.';
      notes.push({ severity: 'HIGH', where: `flashcard_questions[${i}]`,
        note: 'moves in lockstep with the Key Fact box: the three-item list dropped the AO2 strand worth 12 marks.',
        before, after: JSON.stringify({ q: e.q, a: e.a }) });
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
    const f = fixFlashcards(num, row.flashcard_questions);
    if (JSON.stringify(k.out) !== JSON.stringify(row.knowledge_checks)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).knowledge_checks = k.out;
    }
    if (JSON.stringify(f.out) !== JSON.stringify(row.flashcard_questions)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).flashcard_questions = f.out;
    }
    [...k.notes, ...f.notes].forEach((o) => addNote(num, o));
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
