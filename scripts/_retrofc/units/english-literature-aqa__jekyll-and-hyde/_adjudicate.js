/**
 * ADJUDICATED rulings — english-literature-aqa / jekyll-and-hyde.
 *
 * F1  L8  remove the misapplied "apophasis" label (content dfn, glossary entry,
 *         practice band descriptor, flashcard) + recast knowledge_checks[1].
 * F2  L8  Utterson "reliable narrator" -> focaliser framing (matches L6).
 * F3  L3  "ape-like fury" simile -> animalistic imagery.
 * F4  L2+L6  Enfield "cousin" -> the text's "distant kinsman".
 *
 * Backs up EVERY field it changes to _adjudication_backup.json BEFORE the first
 * write, then PATCHes id=eq. per row, then re-fetches and asserts.
 *
 * Usage: node scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_adjudicate.js --dry-run
 *        node scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_adjudicate.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_adjudication_backup.json');
const LOGF = path.join(DIR, '_adjudicate.log');
const UNIT = '10151ade-c16f-4736-9626-8166ef02a30b';

const log = [];
const L = (s) => { console.log(s); log.push(s); };
let failed = false;
const FAIL = (s) => { L('  !! ' + s); failed = true; };

async function q(p, opts) {
  const r = await fetch(`${SB}/rest/v1/${p}`, {
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
    ...opts,
  });
  if (!r.ok) throw new Error(`${p} -> ${r.status} ${await r.text()}`);
  return r.json();
}

// ---------------------------------------------------------- HTML/text edits
// [lessonNumber, field, oldSubstring, newSubstring, ruling, note]
const EDITS = [
  // ---- F4: Enfield is a "distant kinsman", not a cousin (Story of the Door)
  [2, 'content_html',
    'The novella opens with Mr Utterson and his cousin Richard Enfield on their regular Sunday walk.',
    'The novella opens with Mr Utterson and his distant kinsman Richard Enfield on their regular Sunday walk.',
    'F4', 'Stevenson writes "Mr. Richard Enfield, his distant kinsman"; the text never says cousin'],
  [6, 'content_html',
    'Enfield is Utterson’s cousin and walking companion.',
    'Enfield is Utterson’s distant kinsman and walking companion.',
    'F4', 'Stevenson writes "Mr. Richard Enfield, his distant kinsman"; the text never says cousin'],

  // ---- F1: drop the false "apophasis" label from the content dfn
  [8, 'content_html',
    'This technique of describing something by saying it <em>cannot</em> be described is called <dfn class="term" data-def="Describing something as indescribable or beyond words, often to heighten its impact on the reader.">apophasis</dfn>. It makes Hyde more terrifying because the reader must imagine the horror for themselves.',
    'This technique — describing something by insisting it <em>cannot</em> be described — leaves the horror to the reader’s imagination. It makes Hyde more terrifying than any detailed description could.',
    'F1', 'apophasis = declining to mention a thing while mentioning it; it is NOT the assertion that something is beyond description. Label removed rather than swapped for an equally obscure one.'],

  // ---- F2: Utterson is the focaliser, not a narrator (consistent with L6 n2)
  [8, 'content_html',
    'Utterson is a <dfn class="term" data-def="A narrator whose account the reader can trust because they have no reason to lie or distort.">reliable narrator</dfn> in the sense that he reports honestly what he sees. But his perspective is limited — he cannot understand what is happening because it is beyond rational explanation.',
    'Utterson is the <dfn class="term" data-def="The character through whose eyes the reader experiences the story.">focaliser</dfn> of Chapters 1–8, not a narrator: the third-person narration stays with him and reports honestly what he sees. But his perspective is limited — he cannot understand what is happening because it is beyond rational explanation.',
    'F2', 'the same lesson calls Ch 1-8 third-person; L6 already calls Utterson the focaliser. Utterson never narrates.'],
];

// ------------------------------------------------------- JSON-field rewrites
const JSON_EDITS = [];

function editFlashcard(num, idx, expectQ, newCard, ruling, note) {
  JSON_EDITS.push({ num, field: 'flashcard_questions', idx, expectQ, newCard, ruling, note });
}

// F4 — L2 flashcard 0
editFlashcard(2, 0, "Which two characters' Sunday walk opens the novella?",
  { q: "Which two characters' Sunday walk opens the novella?",
    a: 'Mr Utterson and his distant kinsman Richard Enfield.' },
  'F4', 'the text says "distant kinsman", not cousin');

// F3 — L3 flashcard 2
editFlashcard(3, 2, "Which simile describes Hyde's violence in the Carew attack?",
  { q: "What animalistic imagery describes Hyde's violence in the Carew attack?",
    a: "'Ape-like fury' — suggesting evolutionary degeneration." },
  'F3', '"ape-like" is a compound adjective, not a connective comparison; label replaced with animalistic imagery, analysis point kept');

// F4 — L6 flashcard 9
editFlashcard(6, 9, 'Who is Richard Enfield in relation to Utterson?',
  { q: 'Who is Richard Enfield in relation to Utterson?',
    a: "His distant kinsman — Stevenson's phrase — and regular Sunday walking companion." },
  'F4', 'the text says "distant kinsman", not cousin');

// F1 — L8 flashcard 2
editFlashcard(8, 2, 'What is apophasis in Jekyll and Hyde?',
  { q: 'Why does Stevenson refuse to describe Hyde clearly?',
    a: "He has characters assert what cannot be said — 'not easy to describe', 'deformity without any nameable malformation' — so Hyde is defined by an absence." },
  'F1', 'false technical label removed; card now asks what Stevenson does');

// F2 — L8 flashcard 8
editFlashcard(8, 8, 'Why is Utterson considered a reliable narrator?',
  { q: 'Utterson is the focaliser of Chapters 1–8 — what does that mean?',
    a: 'The third-person narration follows what he sees and thinks. He reports honestly, but his rational perspective cannot explain supernatural events.' },
  'F2', 'Utterson never narrates; he is the focaliser of a third-person narration');

// F1 — L8 knowledge_checks[1] full recast
const KC8_1_EXPECT_Q = 'Which language technique does Stevenson use when characters say Hyde is ‘not easy to describe’?';
const KC8_1_NEW = {
  q: 'Why does Stevenson keep Hyde’s appearance vague?',
  type: 'mcq',
  correct: 1,
  options: [
    'It makes Hyde seem harmless',
    'It forces the reader to imagine the horror',
    'It saves space in a short novella',
    'It hides a plot twist',
  ],
};

// F1 — L8 practice_questions[0].marks band descriptor
const PQ8_0_OLD = 'animalistic imagery, pathetic fallacy, apophasis.';
const PQ8_0_NEW = 'animalistic imagery, pathetic fallacy, the refusal to describe Hyde directly.';

// F1/F2 — L8 glossary_terms
const GLOSS_DROP = 'apophasis';                 // F1: delete outright
const GLOSS_SWAP_FROM = 'reliable narrator';    // F2: replace in place
const GLOSS_SWAP_TO = {
  term: 'focaliser',
  definition: 'The character through whose eyes the reader experiences the story.',
};

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== ADJUDICATED RULINGS: english-literature-aqa / jekyll-and-hyde ===`);
  L(`run: ${new Date().toISOString()}   mode: ${DRY ? 'DRY RUN' : 'LIVE'}`);

  const cols = 'id,lesson_number,title,slug,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  L(`fetched ${rows.length} lessons (live: ${rows.filter(r => r.status === 'live').length})\n`);
  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));

  const patches = new Map();   // num -> { field: newValue }
  const noteMap = new Map();   // num -> [ {ruling, where, note, before, after} ]
  const addNote = (n, o) => { if (!noteMap.has(n)) noteMap.set(n, []); noteMap.get(n).push(o); };
  const setPatch = (n, f, v) => { if (!patches.has(n)) patches.set(n, {}); patches.get(n)[f] = v; };
  const cur = (n, f) => (patches.get(n) || {})[f] ?? byNum.get(n)[f];

  // 1 — HTML/text edits
  for (const [num, field, oldS, newS, ruling, note] of EDITS) {
    const row = byNum.get(num);
    if (!row) { FAIL(`L${num} not found`); continue; }
    const c = cur(num, field);
    if (!c.includes(oldS)) {
      FAIL(`[${ruling}] L${num}.${field}: PATTERN NOT FOUND -> ${oldS.slice(0, 90)}`);
      continue;
    }
    setPatch(num, field, c.replace(oldS, newS));
    addNote(num, { ruling, where: field, note, before: oldS, after: newS });
  }

  // 2 — flashcards
  for (const e of JSON_EDITS) {
    const row = byNum.get(e.num);
    const arr = (cur(e.num, e.field) || []).map((c) => ({ ...c }));
    const card = arr[e.idx];
    if (!card || card.q !== e.expectQ) {
      FAIL(`[${e.ruling}] L${e.num}.${e.field}[${e.idx}]: expected q "${e.expectQ}", got "${card && card.q}"`);
      continue;
    }
    const before = { ...card };
    // preserve the row's own key order (this unit stores {a, q})
    const next = {};
    for (const k of Object.keys(card)) next[k] = e.newCard[k] !== undefined ? e.newCard[k] : card[k];
    arr[e.idx] = next;
    setPatch(e.num, e.field, arr);
    addNote(e.num, { ruling: e.ruling, where: `${e.field}[${e.idx}]`, note: e.note,
      before: JSON.stringify(before), after: JSON.stringify(next) });
  }

  // 3 — L8 knowledge_checks[1]
  {
    const kcs = (cur(8, 'knowledge_checks') || []).map((k) => ({ ...k }));
    if (!kcs[1] || kcs[1].q !== KC8_1_EXPECT_Q) {
      FAIL(`[F1] L8.knowledge_checks[1]: expected the apophasis stem, got "${kcs[1] && kcs[1].q}"`);
    } else {
      const before = JSON.parse(JSON.stringify(kcs[1]));
      kcs[1] = { ...KC8_1_NEW };
      setPatch(8, 'knowledge_checks', kcs);
      addNote(8, { ruling: 'F1', where: 'knowledge_checks[1]',
        note: 'the false label was the CORRECT answer; stem + all four options recast',
        before: JSON.stringify(before), after: JSON.stringify(kcs[1]) });
    }
  }

  // 4 — L8 practice_questions[0].marks
  {
    const pqs = (cur(8, 'practice_questions') || []).map((p) => ({ ...p }));
    if (!pqs[0] || !(pqs[0].marks || '').includes(PQ8_0_OLD)) {
      FAIL(`[F1] L8.practice_questions[0].marks: band descriptor not found`);
    } else {
      const before = pqs[0].marks;
      pqs[0].marks = before.replace(PQ8_0_OLD, PQ8_0_NEW);
      setPatch(8, 'practice_questions', pqs);
      addNote(8, { ruling: 'F1', where: 'practice_questions[0].marks',
        note: 'top-band descriptor told students to use the wrong term',
        before: PQ8_0_OLD, after: PQ8_0_NEW });
    }
  }

  // 5 — L8 glossary_terms: drop apophasis, swap reliable narrator -> focaliser
  {
    const gt = (cur(8, 'glossary_terms') || []).map((g) => ({ ...g }));
    const iA = gt.findIndex((g) => (g.term || '').toLowerCase() === GLOSS_DROP);
    const iR = gt.findIndex((g) => (g.term || '').toLowerCase() === GLOSS_SWAP_FROM);
    if (iA < 0) FAIL('[F1] L8.glossary_terms: "apophasis" entry not found');
    if (iR < 0) FAIL('[F2] L8.glossary_terms: "reliable narrator" entry not found');
    if (iA >= 0 && iR >= 0) {
      const beforeA = JSON.stringify(gt[iA]);
      const beforeR = JSON.stringify(gt[iR]);
      gt[iR] = { ...GLOSS_SWAP_TO };
      gt.splice(iA, 1);
      setPatch(8, 'glossary_terms', gt);
      addNote(8, { ruling: 'F1', where: `glossary_terms[${iA}]`,
        note: 'entry deleted with the label', before: beforeA, after: '(removed)' });
      addNote(8, { ruling: 'F2', where: `glossary_terms[${iR}]`,
        note: 'replaced in place; "unreliable narrator" kept for Jekyll',
        before: beforeR, after: JSON.stringify(GLOSS_SWAP_TO) });
    }
  }

  if (failed) { L('\nABORT: one or more patterns did not match. Nothing written.'); process.exit(1); }

  // 6 — BACKUP EVERY CHANGED FIELD BEFORE THE FIRST WRITE
  const backup = {
    generated_at: new Date().toISOString(),
    unit_id: UNIT, subject: 'english-literature-aqa', unit: 'jekyll-and-hyde',
    rulings: ['F1', 'F2', 'F3', 'F4'],
    lessons: [],
  };
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    const before = {};
    for (const k of Object.keys(fields)) before[k] = row[k];
    before.narration_manifest = row.narration_manifest;
    backup.lessons.push({ lesson_number: num, id: row.id, title: row.title,
      fields_changed: Object.keys(fields), findings: noteMap.get(num) || [], before });
  }
  fs.writeFileSync(BACKUP, JSON.stringify(backup, null, 1), 'utf8');
  L(`backup written BEFORE any write -> ${BACKUP}`);
  L(`  ${backup.lessons.length} lessons, ${backup.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields\n`);

  // 7 — PATCH id=eq. per row
  let fieldCount = 0;
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}   fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        [${n.ruling}] ${n.where}: ${n.note}`);
    fieldCount += Object.keys(fields).length;
    if (!DRY) {
      await q(`lessons?id=eq.${row.id}`, { method: 'PATCH', body: JSON.stringify(fields) });
      L(`      -> PATCHED`);
    }
    L('');
  }
  L(`${DRY ? 'WOULD PATCH' : 'PATCHED'}: ${patches.size} lessons, ${fieldCount} fields`);

  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
