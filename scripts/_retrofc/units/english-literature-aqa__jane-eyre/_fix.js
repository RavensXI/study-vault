/**
 * Retro fact-check FIX — english-literature-aqa / jane-eyre.
 *
 * Every claim below was verified against Project Gutenberg #1260 (Jane Eyre)
 * and against specs/aqa/english-literature-8702-8702.md.
 *
 * Backs up every field it changes INCREMENTALLY (written BEFORE each lesson's
 * PATCH) to _backup.json, then PATCHes id=eq. per row.
 *
 * Usage:  node scripts/_retrofc/units/english-literature-aqa__jane-eyre/_fix.js --dry-run
 *         node scripts/_retrofc/units/english-literature-aqa__jane-eyre/_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_backup.json');
const REPORT = path.join(DIR, '_report.json');
const LOGF = path.join(DIR, '_fix.log');
const UNIT = '32f5bcc7-e79e-436a-9158-322c43e4941b';

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

// ------------------------------------------------------------------ HTML edits
// [lessonNumber, field, oldSubstring, newSubstring, severity, note]
const EDITS = [
  // ---- L2: "You are like a murderer" is Ch 1, spoken to JOHN Reed ----------
  [2, 'content_html',
    'He tells Jane: “You have no business to take our books; you are a <dfn class="term" data-def="A person who relies on another for financial support; in Victorian society, being a dependant (especially a poor relation) carried deep social stigma.">dependant</dfn>.” He physically assaults her',
    'He tells Jane: “You have no business to take our books; you are a dependent, mama says; you have no money; your father left you none.” The label of <dfn class="term" data-def="A person who relies on another for financial support; in Victorian society, being a dependant (especially a poor relation) carried deep social stigma.">dependant</dfn> defines Jane entirely by what she lacks. He physically assaults her',
    'MEDIUM', 'Misquotation. Brontë writes "you are a dependent, mama says" (Ch 1) — spelt "dependent", not "dependant". Quotation restored verbatim; the glossary term "dependant" kept as a separate gloss.'],

  [2, 'content_html',
    'When Mrs Reed sends her to the red-room, Jane screams: “You are like a murderer — you are like a slave-driver — you are like the Roman emperors!” These <dfn class="term" data-def="A direct comparison using ‘like’ or ‘as’ that draws a parallel between two things.">similes</dfn> are remarkable because Jane compares her aunt to figures of absolute power and cruelty. She does not accept her suffering passively — she names it and condemns it.',
    'In Chapter 1, John hurls a book at her and cuts her head, and Jane rounds on him: “Wicked and cruel boy! You are like a murderer — you are like a slave-driver — you are like the Roman emperors!” These <dfn class="term" data-def="A direct comparison using ‘like’ or ‘as’ that draws a parallel between two things.">similes</dfn> are remarkable because Jane compares her cousin to figures of absolute power and cruelty. She does not accept her suffering passively — she names it and condemns it. It is this outburst, and the fight that follows, that gets her locked in the red-room.',
    'HIGH', 'Wrong speaker and wrong moment. Gutenberg #1260 Ch 1: Jane says this to JOHN Reed immediately after he throws the book and cuts her head — NOT to Mrs Reed, and not on the way to the red-room. (Her defiant speech to Mrs Reed is the separate Ch 4 line, correctly taught in the next paragraph.)'],

  [2, 'conclusion_html',
    'Jane’s rebellion against Mrs Reed — “You are like a murderer”',
    'Jane’s rebellion against John Reed — “You are like a murderer”',
    'HIGH', 'Same misattribution in the takeaway: the "murderer" similes are addressed to John Reed (Ch 1).'],

  // ---- L4: Rochester's bird imagery ---------------------------------------
  [4, 'content_html',
    'Rochester frequently calls Jane his “bird” — his “lark,” his “eager bird.” These <dfn class="term" data-def="Pet names or intimate forms of address that can reveal power dynamics in a relationship.">terms of endearment</dfn> are also terms of possession: a bird in a cage is beautiful but trapped. Jane resists this language: “I am no bird; and no net ensnares me.” After the engagement, Rochester tries to dress Jane in jewels and silks — essentially decorating her like a caged bird. Jane resists every attempt, insisting on her plain Quaker-like dress.',
    'Rochester repeatedly likens Jane to a caged bird. In Chapter 14 he tells her he catches “the glance of a curious sort of bird through the close-set bars of a cage,” and moments before her great speech he urges her not to “struggle so, like a wild frantic bird that is rending its own plumage.” A bird in a cage is beautiful but trapped, and Jane rejects the image outright: “I am no bird; and no net ensnares me.” Only much later, blind and dependent on her, does he call her “my skylark” — and by then such <dfn class="term" data-def="Pet names or intimate forms of address that can reveal power dynamics in a relationship.">terms of endearment</dfn> no longer carry the threat of possession. After the engagement, Rochester tries to dress Jane in jewels and silks — essentially decorating her like a caged bird. Jane resists every attempt, calling herself his “plain, Quakerish governess.”',
    'MEDIUM', 'Unsupported textual claim + misquotation. Rochester never habitually calls Jane his "bird"; "lark" is actually "my skylark" and occurs only at Ferndean (Ch 37), and "eager bird" is a simile in Ch 27 — both AFTER the Ch 23 speech they were said to provoke. Replaced with the verbatim caged-bird imagery that does precede it (Ch 14; Ch 23) plus Jane\'s own "plain, Quakerish governess" (Ch 24).'],

  [4, 'content_html',
    'data-def="A person of mixed European and Caribbean descent; Bertha’s Creole heritage connects her to Britain’s colonial exploitation of the Caribbean."',
    'data-def="In the 19th-century Caribbean, a person born and raised in the West Indies — for a planter family such as the Masons, of European settler descent. Bertha’s Creole background ties the novel to Britain’s colonial exploitation of the Caribbean."',
    'MEDIUM', 'Factual error. "Creole" in this period means born and raised in the West Indies, not "of mixed European and Caribbean descent". Bertha is the daughter of "Jonas Mason, merchant, and of Antoinetta his wife, a Creole" (Ch 26) in a West India planter family, and is standardly read as a white Creole. (Attribute-only edit — no narrated text changes.)'],

  // ---- L7: quotation bank -------------------------------------------------
  [7, 'content_html',
    '<strong>"You have no business to take our books; you are a dependant."</strong> (John Reed, Ch. 1) — The possessive "our" and the label "dependant" show how class defines identity in Victorian society.',
    '<strong>"You have no business to take our books; you are a dependent, mama says."</strong> (John Reed, Ch. 1) — The possessive "our" and the label "dependent" show how class defines identity in Victorian society.',
    'MEDIUM', 'Misquotation in the memorisation bank. Brontë writes "dependent" (Ch 1). Students memorise this verbatim, so the spelling matters.'],

  [7, 'content_html',
    '(Jane, Ch. 4) — Triple <dfn class="term" data-def="A direct comparison using \'like\' or \'as.\'">simile</dfn> escalates',
    '(Jane to John Reed, Ch. 1) — Triple <dfn class="term" data-def="A direct comparison using \'like\' or \'as.\'">simile</dfn> escalates',
    'HIGH', 'Wrong chapter in the memorisation bank: the triple simile is Ch 1, addressed to John Reed. Addressee added because L2 taught it as spoken to Mrs Reed.'],

  [7, 'content_html',
    'data-def="A structure where successive clauses build in intensity, creating a sense of accumulation and emphasis."',
    'data-def="A structure where successive clauses begin with the same word or phrase, building intensity; e.g. ‘the more… the more.’"',
    'MEDIUM', 'The inline definition of anaphora described climax/auxesis, not anaphora, and contradicted this lesson’s own glossary entry. Aligned to the (correct) glossary text. (Attribute-only edit — no narrated text changes.)'],

  [7, 'content_html',
    'of the bird and net draws on Rochester\'s habit of calling Jane his "bird" and "lark" — terms of endearment that are also terms of ownership.',
    'of the bird and net answers Rochester directly: seconds earlier he has told her not to "struggle so, like a wild frantic bird that is rending its own plumage," and in Chapter 14 he described her as "a curious sort of bird through the close-set bars of a cage."',
    'MEDIUM', 'Same unsupported claim as L4 n7, inside the model exam paragraph — the version a student is most likely to copy. Replaced with verbatim, correctly-placed textual evidence.'],
];

// ------------------------------------------------- JSON field edits (by path)
// [lessonNumber, field, index, key, oldValue, newValue, severity, note]
const JSON_EDITS = [
  // ---- L1 -----------------------------------------------------------------
  [1, 'flashcard_questions', 12, 'q',
    'Which three religious figures show hypocritical Christianity in the novel?',
    'Which three characters represent contrasting versions of Christianity in the novel?',
    'HIGH', 'Self-contradicting card. The answer names Brocklehurst, Helen Burns and St John Rivers, but this lesson’s own body text says Helen "practises patient, accepting faith" and St John represents "cold, duty-driven religion". Only Brocklehurst is hypocritical. Stem corrected to "contrasting versions", which the answer does satisfy.'],

  // ---- L2 -----------------------------------------------------------------
  [2, 'knowledge_checks', 1, 'q',
    'What disease kills many students at Lowood, including Helen Burns?',
    'What disease sweeps through Lowood in spring, killing many students?',
    'HIGH', 'Factually wrong and contradicts this lesson’s own content_html and glossary. Ch 9: the epidemic is typhus, but "her complaint was consumption, not typhus" — Helen Burns is NOT one of the typhus victims. Stem corrected; answer stays Typhus (index 1), which is right for the epidemic.'],
  [2, 'knowledge_checks', 2, 'q',
    'Jane compares Mrs Reed to a murderer, a slave-driver, and the _____ emperors.',
    'Jane compares John Reed to a murderer, a slave-driver, and the _____ emperors.',
    'HIGH', 'Wrong addressee — Ch 1, spoken to John Reed.'],
  [2, 'flashcard_questions', 1, 'a',
    "'You have no business to take our books; you are a dependant.'",
    "'You have no business to take our books; you are a dependent, mama says.'",
    'MEDIUM', 'Misquotation — Brontë writes "dependent" (Ch 1).'],
  [2, 'flashcard_questions', 4, 'q',
    'Which similes does Jane use to condemn Mrs Reed?',
    'Which similes does Jane use to condemn John Reed?',
    'HIGH', 'Wrong addressee — Ch 1, spoken to John Reed.'],
  [2, 'flashcard_questions', 8, 'a',
    'A consumption (TB) epidemic kills many Lowood students, but Helen Burns dies separately of consumption (TB) in Chapter 9 — Jane holds her in her arms.',
    "A typhus epidemic kills many Lowood students, but Helen Burns dies separately of consumption (TB) in Chapter 9 — Jane is found asleep with her arms round Helen's neck.",
    'HIGH', 'Botched earlier edit: the answer named the epidemic as consumption, contradicting the question ("what epidemic"), the lesson body and the glossary. Ch 9: Lowood "breathed typhus"; Helen’s "complaint was consumption, not typhus".'],

  // ---- L3 -----------------------------------------------------------------
  [3, 'flashcard_questions', 6, 'q',
    'How does Rochester test Jane in Chapter 18?',
    'How does Rochester test Jane in Chapters 18–19?',
    'LOW', 'The gipsy disguise arrives in Ch 18, but Jane’s own interview — the test of HER — is Ch 19. Span given instead of the single wrong chapter.'],

  // ---- L4 -----------------------------------------------------------------
  [4, 'flashcard_questions', 13, 'a',
    'As mirroring British imperial attitudes toward colonised Caribbean peoples.',
    'As mirroring British imperial attitudes towards colonised Caribbean peoples.',
    'LOW', 'US "toward" — house style is British English ("towards"). Only instance in the unit.'],
  [4, 'flashcard_questions', 14, 'a',
    "Of mixed European and Caribbean descent — Bertha's Jamaican heritage.",
    "Born and raised in the West Indies — for a planter family such as the Masons, of European settler descent. Bertha's Jamaican background.",
    'MEDIUM', 'Same "Creole" error as the body gloss — see L4 content note.'],
];

// glossary rewrites: [lessonNumber, term, oldDefinition, newDefinition, severity, note]
const GLOSSARY_EDITS = [
  [4, 'Creole',
    'A person of mixed European and Caribbean descent; Bertha’s Creole heritage connects her to Britain’s colonial exploitation of the Caribbean.',
    'In the 19th-century Caribbean, a person born and raised in the West Indies — for a planter family such as the Masons, of European settler descent. Bertha’s Creole background ties the novel to Britain’s colonial exploitation of the Caribbean.',
    'MEDIUM', 'Same "Creole" error as the body gloss — see L4 content note.'],
];

const noteMap = new Map();
const addNote = (num, o) => { if (!noteMap.has(num)) noteMap.set(num, []); noteMap.get(num).push(o); };

(async () => {
  const cols = 'id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  L(`\n=== JANE EYRE FIX ${DRY ? '(DRY RUN)' : '(LIVE)'} — ${new Date().toISOString()} ===`);
  L(`${rows.length} lessons; all status=${[...new Set(rows.map((r) => r.status))].join(',')}\n`);

  const patches = new Map();
  const stage = (num, field, val) => {
    if (!patches.has(num)) patches.set(num, {});
    patches.get(num)[field] = val;
  };

  // 1. plain string edits on HTML fields
  for (const [num, field, oldS, newS, sev, note] of EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) throw new Error(`L${num}.${field}: OLD STRING NOT FOUND\n  ${oldS.slice(0, 160)}`);
    const occurrences = cur.split(oldS).length - 1;
    if (occurrences !== 1) throw new Error(`L${num}.${field}: expected 1 occurrence, found ${occurrences}`);
    stage(num, field, cur.replace(oldS, newS));
    addNote(num, { severity: sev, where: `${field}`, note, was: oldS.slice(0, 200), now: newS.slice(0, 200) });
  }

  // 2. JSON array item edits
  for (const [num, field, idx, key, oldV, newV, sev, note] of JSON_EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {})[field] ?? row[field];
    const arr = JSON.parse(JSON.stringify(cur));
    if (arr[idx][key] !== oldV) throw new Error(`L${num}.${field}[${idx}].${key}: MISMATCH\n  expected: ${oldV}\n  actual:   ${arr[idx][key]}`);
    arr[idx][key] = newV;
    stage(num, field, arr);
    addNote(num, { severity: sev, where: `${field}[${idx}].${key}`, note, was: oldV, now: newV });
  }

  // 3. glossary rewrites (matched by term, not index)
  for (const [num, term, oldD, newD, sev, note] of GLOSSARY_EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {}).glossary_terms ?? row.glossary_terms;
    const arr = JSON.parse(JSON.stringify(cur));
    const i = arr.findIndex((g) => g.term === term);
    if (i < 0) throw new Error(`L${num} glossary term "${term}" not found`);
    if (arr[i].definition !== oldD) throw new Error(`L${num} glossary "${term}": MISMATCH\n  expected: ${oldD}\n  actual:   ${arr[i].definition}`);
    arr[i].definition = newD;
    stage(num, 'glossary_terms', arr);
    addNote(num, { severity: sev, where: `glossary_terms["${term}"]`, note, was: oldD, now: newD });
  }

  // 4. practice question chapter attributions
  {
    const row = byNum.get(2);
    const pq = JSON.parse(JSON.stringify((patches.get(2) || {}).practice_questions ?? row.practice_questions));
    const oldT = pq[0].text;
    if (!oldT.startsWith('Read the following extract from Chapter 4:')) throw new Error('L2 pq[0] unexpected opening');
    pq[0].text = oldT.replace('Read the following extract from Chapter 4:', 'Read the following extract from Chapter 1:');
    stage(2, 'practice_questions', pq);
    addNote(2, {
      severity: 'HIGH', where: 'practice_questions[0].text',
      note: 'Wrong chapter on the printed extract: the "murderer / slave-driver / Roman emperors" speech is Ch 1 (to John Reed), not Ch 4.',
      was: 'Read the following extract from Chapter 4:', now: 'Read the following extract from Chapter 1:',
    });
  }

  // ---------------------------------------- incremental backup + patch, per lesson
  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT,
    subject: 'english-literature-aqa', unit: 'jane-eyre', lessons: [],
  };
  const report = {
    generated_at: new Date().toISOString(),
    subject: 'english-literature-aqa', unit: 'jane-eyre',
    source_text: 'Project Gutenberg #1260 (Jane Eyre: An Autobiography)',
    spec: 'specs/aqa/english-literature-8702-8702.md',
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
    report.lessons.push({
      lesson_number: num, id: row.id, title: row.title,
      fields_changed: Object.keys(fields), findings: noteMap.get(num) || [],
    });
    writeState();   // persisted BEFORE the write; a killed run loses nothing

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
  const counts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
  for (const l of report.lessons) for (const f of l.findings) counts[f.severity]++;
  report.fixed_counts = counts;
  L(`fixed findings: HIGH=${counts.HIGH} MEDIUM=${counts.MEDIUM} LOW=${counts.LOW}`);
  writeState();
  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
