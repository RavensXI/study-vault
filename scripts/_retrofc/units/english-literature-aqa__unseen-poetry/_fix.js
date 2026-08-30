/**
 * Retro fact-check FIX — english-literature-aqa / unseen-poetry.
 *
 * Applies only CERTAIN corrections, verified against official AQA sources:
 *   - AQA-87022-SQP.PDF   (specimen question paper: Section C = Q27.1 / Q27.2)
 *   - AQA-87022-SMS.PDF   (specimen mark scheme: 24-mark band ladder, AO splits)
 *   - AQA-87022-MS-JUN23.PDF / JUN24 (live series confirm 27.1 / 27.2)
 *   - specs/aqa/english-literature-8702-8702.md (verbatim AO2 wording)
 *
 * Backs up every changed field INCREMENTALLY (written after each lesson) to
 * _backup.json, then PATCHes id=eq. per row.
 *
 * Usage:  node .../_fix.js --dry-run
 *         node .../_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_backup.json');
const RAW = path.join(DIR, '_raw.json');
const UNIT = '00e90d53-67ee-4074-be96-2f4f7fb9ea0f';

const log = [];
function L(s) { console.log(s); log.push(s); }

const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'return=representation' };

const JSON_FIELDS = new Set(['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']);

// ---- correct AQA 24-mark ladders (Level 6→1: 21-24/17-20/13-16/9-12/5-8/1-4)
// Only the BOUNDARIES and the duplicate label are corrected; descriptor prose
// is left exactly as authored.
const L1_LADDER_OLD =
  "Top band (22-24) Convincing, critical analysis. Exploratory response with perceptive understanding. Well-chosen, precisely embedded quotations. Sophisticated analysis of language, form, and structure.\nUpper band (18-21) Thoughtful, developed response. Clear analysis of methods.\nTop band (13-17): Clear understanding with explained analysis.\nUpper-mid band (9-12): Some understanding with some analysis.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";
const L1_LADDER_NEW =
  "Top band (21-24) Convincing, critical analysis. Exploratory response with perceptive understanding. Well-chosen, precisely embedded quotations. Sophisticated analysis of language, form, and structure.\nUpper band (17-20) Thoughtful, developed response. Clear analysis of methods.\nUpper-mid band (13-16): Clear understanding with explained analysis.\nMid band (9-12): Some understanding with some analysis.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";

const L2_LADDER_OLD =
  "Top band (22-24) Convincing, critical analysis. Exploratory response with perceptive exploration of language. Well-chosen, precisely embedded quotations. Sophisticated analysis of word choice, imagery, and sound.\nUpper band (18-21) Thoughtful, developed response.\nTop band (13-17): Clear, explained analysis.\nUpper-mid band (9-12): Some understanding with some analysis.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";
const L2_LADDER_NEW =
  "Top band (21-24) Convincing, critical analysis. Exploratory response with perceptive exploration of language. Well-chosen, precisely embedded quotations. Sophisticated analysis of word choice, imagery, and sound.\nUpper band (17-20) Thoughtful, developed response.\nUpper-mid band (13-16): Clear, explained analysis.\nMid band (9-12): Some understanding with some analysis.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";

const L3_LADDER_OLD =
  "Top band (22-24) Convincing, critical analysis of how structural and formal choices contribute to meaning. Explores the relationship between form and content. Precise terminology.\nUpper band (18-21) Thoughtful response with clear structural analysis.\nTop band (13-17): Clear understanding of structural effects.\nUpper-mid band (9-12): Some structural comments.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";
const L3_LADDER_NEW =
  "Top band (21-24) Convincing, critical analysis of how structural and formal choices contribute to meaning. Explores the relationship between form and content. Precise terminology.\nUpper band (17-20) Thoughtful response with clear structural analysis.\nUpper-mid band (13-16): Clear understanding of structural effects.\nMid band (9-12): Some structural comments.\nLower-mid band (5-8): Supported comments.\nLower band (1-4): Simple, limited comments.";

// [lessonNumber, field, old, new, severity, note]
const EDITS = [
  // ================= HIGH-1: Q28 does not exist on AQA 8702 =================
  // Section C is Question 27.1 (24 marks) + Question 27.2 (8 marks).
  [1, 'content_html',
    'Question 27 asks you to analyse a single unseen poem',
    'Question 27.1 asks you to analyse a single unseen poem',
    'HIGH', 'n3 key fact: AQA numbers the 24-mark task 27.1, not 27'],
  [1, 'content_html',
    'Question 28 asks you to compare the first poem',
    'Question 27.2 asks you to compare the first poem',
    'HIGH', 'n3 key fact: there is no Q28 on AQA 8702/2'],
  [1, 'content_html',
    '<strong>25 minutes</strong> on Q27 and <strong>20 minutes</strong> on Q28.',
    '<strong>25 minutes</strong> on Q27.1 and <strong>20 minutes</strong> on Q27.2.',
    'HIGH', 'n3 key fact: timing line'],
  [1, 'exam_tip_html', 'For Q27 (24 marks)', 'For Q27.1 (24 marks)', 'HIGH', 'n26 exam tip'],
  [1, 'knowledge_checks',
    'How many marks is Q27 (single poem analysis) worth?',
    'How many marks is Q27.1 (single poem analysis) worth?',
    'HIGH', 'KC0 stem'],
  [1, 'knowledge_checks', 'Only for Q28', 'Only for Q27.2', 'HIGH', 'KC1 distractor'],
  [1, 'flashcard_questions',
    'Question 27, the single unseen poem question',
    'Question 27.1, the single unseen poem question',
    'HIGH', 'flashcard'],
  [1, 'flashcard_questions',
    'Question 28, the unseen poetry comparison',
    'Question 27.2, the unseen poetry comparison',
    'HIGH', 'flashcard'],
  [1, 'flashcard_questions',
    'spend on Question 27 in AQA unseen poetry?',
    'spend on Question 27.1 in AQA unseen poetry?',
    'HIGH', 'flashcard'],
  [1, 'flashcard_questions',
    'aim for on Question 27?', 'aim for on Question 27.1?', 'HIGH', 'flashcard'],

  [4, 'conclusion_html', 'Q28 is worth 8 marks', 'Q27.2 is worth 8 marks', 'HIGH', 'n27 takeaway'],
  [4, 'exam_tip_html',
    'Q28 is the last question on the entire paper.',
    'Q27.2 is the last question on the entire paper.',
    'HIGH', 'n25 exam tip'],
  [4, 'exam_tip_html',
    '25 minutes for Q27, then 20 minutes for Q28.',
    '25 minutes for Q27.1, then 20 minutes for Q27.2.',
    'HIGH', 'n25 exam tip'],
  [4, 'practice_questions',
    'between Q27 and Q28 in terms of what is assessed?',
    'between Q27.1 and Q27.2 in terms of what is assessed?',
    'HIGH', 'PQ2 stem'],
  [4, 'practice_questions',
    '• Q27 assesses AO1 (personal response, 12 marks) AND AO2 (methods, 12 marks) (1 mark)',
    '• Q27.1 assesses AO1 (personal response, 12 marks) AND AO2 (methods, 12 marks) (1 mark)',
    'HIGH', 'PQ2 scheme'],
  [4, 'practice_questions',
    '• Q28 assesses AO2 ONLY (methods, 8 marks) (1 mark)',
    '• Q27.2 assesses AO2 ONLY (methods, 8 marks) (1 mark)',
    'HIGH', 'PQ2 scheme'],
  [4, 'practice_questions',
    'This means Q28 must focus entirely', 'This means Q27.2 must focus entirely',
    'HIGH', 'PQ2 scheme'],
  [4, 'practice_questions',
    'the other is a common mistake in Q28.', 'the other is a common mistake in Q27.2.',
    'HIGH', 'PQ3 stem'],
  [4, 'practice_questions',
    'Write a model comparative paragraph for Q28, comparing',
    'Write a model comparative paragraph for Q27.2, comparing',
    'HIGH', 'PQ4 stem'],
  [4, 'practice_questions',
    'How many paragraphs should you write for Q28 and why?',
    'How many paragraphs should you write for Q27.2 and why?',
    'HIGH', 'PQ5 stem'],
  [4, 'knowledge_checks',
    'The biggest mistake in Q28 is writing about one poem',
    'The biggest mistake in Q27.2 is writing about one poem',
    'HIGH', 'KC3 stem'],
  [4, 'knowledge_checks',
    'How many marks is Q28 (unseen poetry comparison) worth?',
    'How many marks is Q27.2 (unseen poetry comparison) worth?',
    'HIGH', 'KC0 stem'],
  [4, 'knowledge_checks',
    'Which Assessment Objective does Q28 assess?',
    'Which Assessment Objective does Q27.2 assess?',
    'HIGH', 'KC1 stem'],
  [4, 'knowledge_checks',
    'You should spend approximately _____ minutes on Q28.',
    'You should spend approximately _____ minutes on Q27.2.',
    'HIGH', 'KC2 stem'],
  [4, 'knowledge_checks',
    'Match each Q28 mistake to why it loses marks:',
    'Match each Q27.2 mistake to why it loses marks:',
    'HIGH', 'KC4 stem'],
  [4, 'knowledge_checks',
    'Takes time from Q27 (worth 3x more)', 'Takes time from Q27.1 (worth 3x more)',
    'HIGH', 'KC4 match target'],
  [4, 'glossary_terms',
    'The marks available for Q28 (unseen poetry comparison)',
    'The marks available for Q27.2 (unseen poetry comparison)',
    'HIGH', 'glossary definition'],

  // ============ HIGH-2: 24-mark band ladder boundaries + duplicate ==========
  [1, 'practice_questions', L1_LADDER_OLD, L1_LADDER_NEW, 'HIGH',
    'PQ0: AQA 24-mark ladder is 21-24/17-20/13-16/9-12/5-8/1-4; "Top band" appeared twice'],
  [2, 'practice_questions', L2_LADDER_OLD, L2_LADDER_NEW, 'HIGH',
    'PQ0: same broken ladder'],
  [3, 'practice_questions', L3_LADDER_OLD, L3_LADDER_NEW, 'HIGH',
    'PQ0: same broken ladder'],

  // ==================== MEDIUM-1: AO2 misquoted in L3 ======================
  [3, 'content_html',
    'AO2 explicitly assesses your ability to analyse “the effects of the writer’s methods, using relevant subject terminology: language, <strong>form</strong> and <strong>structure</strong>.”',
    'AO2 explicitly assesses your ability to “analyse the language, <strong>form</strong> and <strong>structure</strong> used by a writer to create meanings and effects, using relevant subject terminology where appropriate.”',
    'MEDIUM', 'n2: quoted text was not the AO2 wording; replaced with the spec verbatim'],

  // ==================== MEDIUM-2: L4 unclosed <p> =========================
  [4, 'content_html',
    '“Where Poet 1 [approach], Poet 2 [contrasting approach].”',
    '“Where Poet 1 [approach], Poet 2 [contrasting approach].”</p>',
    'MEDIUM', 'content_html ended with an unclosed <p data-narration-id="n24">'],
];

function replaceInStrings(v, oldS, newS, counter) {
  if (typeof v === 'string') {
    if (v.includes(oldS)) { counter.n += v.split(oldS).length - 1; return v.split(oldS).join(newS); }
    return v;
  }
  if (Array.isArray(v)) return v.map(x => replaceInStrings(x, oldS, newS, counter));
  if (v && typeof v === 'object') {
    const o = {};
    for (const [k, x] of Object.entries(v)) o[k] = replaceInStrings(x, oldS, newS, counter);
    return o;
  }
  return v;
}

(async () => {
  const rows = JSON.parse(fs.readFileSync(RAW, 'utf8'));
  const byNum = new Map(rows.map(r => [r.lesson_number, r]));

  const backup = {
    generated_at: new Date().toISOString(),
    unit_id: UNIT, subject: 'english-literature-aqa', unit: 'unseen-poetry',
    sources: [
      'https://filestore.aqa.org.uk/resources/english/AQA-87022-SQP.PDF',
      'https://filestore.aqa.org.uk/resources/english/AQA-87022-SMS.PDF',
      'https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-87022-MS-JUN23.PDF',
      'specs/aqa/english-literature-8702-8702.md',
    ],
    lessons: [],
  };
  if (!DRY && fs.existsSync(BACKUP)) {
    L(`!! ${BACKUP} already exists — refusing to overwrite. Move it aside first.`);
    process.exit(1);
  }

  const byLesson = new Map();
  for (const e of EDITS) {
    if (!byLesson.has(e[0])) byLesson.set(e[0], []);
    byLesson.get(e[0]).push(e);
  }

  let applied = 0;
  for (const num of [...byLesson.keys()].sort((a, b) => a - b)) {
    const row = byNum.get(num);
    if (!row) { L(`!! no lesson ${num}`); continue; }
    L(`\n--- L${num} ${row.title} (${row.id}) ---`);

    const before = {};
    const after = {};
    for (const [, field, oldS, newS, sev, note] of byLesson.get(num)) {
      const cur = field in after ? after[field] : row[field];
      const counter = { n: 0 };
      const next = JSON_FIELDS.has(field)
        ? replaceInStrings(cur, oldS, newS, counter)
        : (typeof cur === 'string' && cur.includes(oldS)
            ? (counter.n = cur.split(oldS).length - 1, cur.split(oldS).join(newS))
            : cur);
      if (!counter.n) {
        L(`  !! NO MATCH  [${sev}] ${field}: ${JSON.stringify(oldS.slice(0, 70))}`);
        process.exitCode = 1;
        continue;
      }
      if (!(field in before)) before[field] = row[field];
      after[field] = next;
      applied += counter.n;
      L(`  [${sev}] ${field} ×${counter.n} — ${note}`);
    }

    const changed = Object.keys(after);
    if (!changed.length) continue;

    // ---- residual check: no Q28 / bare Q27 must survive in this lesson ----
    const merged = JSON.stringify({ ...row, ...after });
    const bad = [...merged.matchAll(/Q(?:uestion)?\s?(2[0-9])(?!\.\d)(?![0-9])/g)].map(m => m[0]);
    if (bad.length) L(`  ?? residual bare question refs: ${[...new Set(bad)].join(', ')}`);

    backup.lessons.push({
      lesson_number: num, id: row.id, title: row.title,
      fields_changed: changed, before,
    });
    // INCREMENTAL: write the backup BEFORE the PATCH, after every lesson.
    if (!DRY) fs.writeFileSync(BACKUP, JSON.stringify(backup, null, 1));

    if (DRY) { L('  (dry run — not written)'); continue; }

    const r = await fetch(`${SB}/rest/v1/lessons?id=eq.${row.id}`, {
      method: 'PATCH', headers: H, body: JSON.stringify(after),
    });
    if (!r.ok) { L(`  !! PATCH FAILED ${r.status} ${await r.text()}`); process.exitCode = 1; continue; }
    L(`  PATCHed ${changed.join(', ')}`);
  }

  L(`\n${applied} string replacements across ${backup.lessons.length} lessons.`);
  fs.appendFileSync(path.join(DIR, '_fix.log'), log.join('\n') + '\n');
})();
