/**
 * ADJUDICATION pass — english-literature-aqa / jane-eyre.
 *
 * Applies the six ADJUDICATED rulings on flags G3–G8 from _report.json.
 * G1 and G2 were adjudicated KEEP and are not touched.
 *
 * Every textual claim below is verified against Project Gutenberg #1260 and
 * against specs/aqa/english-literature-8702-8702.md.
 *
 * Backs up every changed field INCREMENTALLY (written BEFORE each PATCH) to
 * _adjudication_backup.json, then PATCHes id=eq. per row.
 *
 * Usage:  node scripts/_retrofc/units/english-literature-aqa__jane-eyre/_adjudicate.js --dry-run
 *         node scripts/_retrofc/units/english-literature-aqa__jane-eyre/_adjudicate.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_adjudication_backup.json');
const REPORT = path.join(DIR, '_report.json');
const LOGF = path.join(DIR, '_adjudicate.log');
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
// [ruling, lessonNumber, field, oldSubstring, newSubstring, note]
const EDITS = [
  // ---- RULING 1 / G3 (L7 n16): board-agnostic hedge -> AQA 8702 reality ------
  ['G3', 7, 'content_html',
    "In most boards, the 19th-century novel question gives you a printed extract (roughly 400 words) from <em>Jane Eyre</em> and asks you to write about the extract and the novel as a whole. Your response is assessed on three strands: your critical response to the text with well-chosen references (AO1), your analysis of the writer's methods — language, form and structure (AO2), and your understanding of context (AO3). Check your exam board's specimen paper and mark scheme for the exact weightings and timings that apply to your exam.",
    "AQA Paper 1 is 1 hour 45 minutes long and worth 64 marks — 40% of your GCSE. Section B is the 19th-century novel: one question on <em>Jane Eyre</em>, worth 30 marks. The paper is closed book, so AQA prints an extract from the novel for you; you write in detail about that extract and then about the novel as a whole. Three assessment objectives carry the marks: your critical response with well-chosen references (AO1, 12 marks), your analysis of the writer's methods — language, form and structure (AO2, 12 marks), and your understanding of context (AO3, 6 marks). AQA sets no word count, so judge length by time: Section B is 30 of the paper's 64 marks, which makes about 50 minutes of the 105 a fair share — five to read and plan, the rest to write.",
    'Board-agnostic hedge removed. AQA 8702 spec, Specification at a glance: Paper 1 = 1 h 45 min, 64 marks, 40% of GCSE; Section B the 19th-century novel = one question, students "write in detail about an extract from the novel and then about the novel as a whole"; all assessments closed book with stimulus provided. Section B AO split (12/12/6 = 30) already carried by this unit. The unsourced "roughly 400 words" is replaced by mark-proportional timing.'],

  // ---- RULING 2 / G4 (L2 n11): Helen Burns's death -------------------------
  ['G4', 2, 'content_html',
    'In Chapter 9, Jane steals away to Miss Temple’s room to be with Helen and wakes to find she has died with Jane’s arms around her neck.',
    'In Chapter 9, Jane steals away to Miss Temple’s room to be with Helen and falls asleep beside her. A nurse carries Jane back to the dormitory before dawn, so she does not wake to the discovery: only “a day or two afterwards” does she learn what Miss Temple found at daybreak — “my face against Helen Burns’s shoulder, my arms round her neck. I was asleep, and Helen was—dead.”',
    'Ch 9 sequence corrected. Jane falls asleep beside Helen; "When I awoke it was day... the nurse held me; she was carrying me through the passage back to the dormitory"; "a day or two afterwards I learned that Miss Temple... had found me laid in the little crib; my face against Helen Burns\'s shoulder, my arms round her neck. I was asleep, and Helen was—dead."'],

  // ---- RULING 3 / G5 (L6 n6): caged eagle must carry its comparator ---------
  ['G5', 6, 'content_html',
    'Jane describes him as a “caged eagle, whose gold-ringed eyes cruelty has extinguished.” The <dfn class="term" data-def="A direct comparison using ‘like’ or ‘as’; here Jane compares Rochester to a caged eagle to show his diminished power and noble suffering.">simile</dfn> of the caged eagle is significant: Rochester, once the powerful master, is now confined and powerless',
    'Jane sees in him “some wronged and fettered wild beast or bird,” then makes the comparison explicit: “The caged eagle, whose gold-ringed eyes cruelty has extinguished, might look as looked that sightless Samson.” The <dfn class="term" data-def="A direct comparison using ‘like’ or ‘as’; here the caged eagle ‘might look as looked that sightless Samson’ — the blinded Rochester.">simile</dfn> turns on that “as”: Rochester is the sightless Samson, and the caged eagle is what he now resembles. Once the powerful master, he is now confined and powerless',
    'Quotation extended so the simile label is true. Gutenberg #1260 Ch 37, verbatim: "reminded me of some wronged and fettered wild beast or bird... The caged eagle, whose gold-ringed eyes cruelty has extinguished, might look as looked that sightless Samson." The comparator is "as looked", so the full sentence is 16 words — one over the 15-word target, kept whole because trimming would break verbatim quotation.'],

  // ---- RULING 4 / G6 (L6 n14): Rochester's prayer --------------------------
  ['G6', 6, 'content_html',
    'He tells Jane that during his suffering he prayed to God for the first time, suggesting a genuine spiritual transformation rather than mere physical punishment.',
    'He tells Jane that only “of late” has he begun to acknowledge “the hand of God in my doom”: “I began sometimes to pray: very brief prayers they were, but very sincere.” This is recent, humbled prayer rather than a first prayer, and it suggests a genuine spiritual transformation rather than mere physical punishment.',
    'Ch 37 verbatim: "Of late, Jane—only—only of late—I began to see and acknowledge the hand of God in my doom... I began sometimes to pray: very brief prayers they were, but very sincere." Rochester never says "for the first time".'],

  // ---- RULING 5 / G7 (L5 n4 key-fact): who founds the Morton school ---------
  ['G7', 5, 'content_html',
    'she opens a village school for poor girls. These gains mean she can return to Rochester as an equal, not a dependant.',
    'she takes charge of the village girls’ school that St John Rivers has established at Morton. These gains mean she can return to Rochester as an equal, not a dependant.',
    'Ch 30 verbatim, St John speaking: "Morton, when I came to it two years ago, had no school: the children of the poor were excluded from every hope of progress. I established one for boys: I mean now to open a second school for girls. I have hired a building for the purpose, with a cottage of two rooms attached to it for the mistress\'s house." Jane is the mistress, not the founder.'],

  // ---- RULING 6 / G8 (L5 n15): where Jane is when she hears the voice -------
  ['G8', 5, 'content_html',
    'At the moment Jane is about to yield to St John, she hears Rochester’s voice calling her name across the moors: “Jane! Jane! Jane!” This could be supernatural (a telepathic connection) or psychological (Jane’s subconscious reasserting her true desires). Either way, it is the catalyst that frees her from St John’s control and sends her back to Thornfield.',
    'At the moment Jane is about to yield to St John, a voice cries “Jane! Jane! Jane!” She is indoors at Moor House, in a room filling with moonlight, and the cry seems to belong nowhere: “it did not seem in the room—nor in the house—nor in the garden.” She knows the voice for Rochester’s, and he is miles away at Ferndean with the moors lying between them; she runs out and finds an empty garden and “moorland loneliness and midnight hush.” This could be supernatural (a telepathic connection) or psychological (Jane’s subconscious reasserting her true desires). Either way, it is the catalyst that frees her from St John’s control and sends her back to Thornfield.',
    'Ch 35: Jane is inside Moor House with St John ("All the house was still... the room was full of moonlight"). The cry "did not seem in the room—nor in the house—nor in the garden"; she runs out afterwards and finds "all was moorland loneliness and midnight hush". The moors lie between her and Ferndean; she is not on them.'],

  ['G7', 5, 'conclusion_html',
    'and meaningful work (the village school).',
    'and meaningful work (mistress of the Morton girls’ school St John set up).',
    'Same Morton-school correction in the takeaway (see G7 above).'],

  ['G8', 5, 'conclusion_html',
    'Jane hears Rochester’s voice calling across the moors, breaking St John’s hold and proving that genuine feeling is a more reliable guide than cold religious duty.',
    'Indoors at Moor House, Jane hears Rochester’s voice cry her name from nowhere she can place, breaking St John’s hold and proving that genuine feeling is a more reliable guide than cold religious duty.',
    'Same location correction in the takeaway (see G8 above).'],
];

// ------------------------------------------------- JSON field edits (by path)
// [ruling, lessonNumber, field, index, key, oldValue, newValue, note]
const JSON_EDITS = [
  ['G5', 6, 'flashcard_questions', 4, 'a',
    "A 'caged eagle, whose gold-ringed eyes cruelty has extinguished.'",
    "'The caged eagle, whose gold-ringed eyes cruelty has extinguished, might look as looked that sightless Samson.'",
    'Fragment extended so the card teaches a real simile (comparator "as looked"). Ch 37, verbatim.'],

  ['G6', 6, 'flashcard_questions', 9, 'q',
    'What does Rochester say he did for the first time during his suffering?',
    "What does Rochester say he began to do 'of late', during his suffering?",
    'Rochester never claims a first prayer; Ch 37 says "of late... I began sometimes to pray".'],
  ['G6', 6, 'flashcard_questions', 9, 'a',
    'He prayed to God — a genuine spiritual transformation.',
    "He began sometimes to pray — 'very brief prayers they were, but very sincere' — a genuine spiritual change.",
    'Answer aligned to the corrected stem and to the Ch 37 wording.'],

  ['G7', 5, 'flashcard_questions', 1, 'a',
    'A family (the Rivers cousins), financial independence (£20,000 inheritance), and meaningful work (a village school).',
    'A family (the Rivers cousins), financial independence (£20,000 inheritance), and meaningful work — mistress of the village school St John founded at Morton.',
    'Same Morton-school correction on the card (see G7 above).'],

  ['G8', 5, 'flashcard_questions', 11, 'a',
    "She hears Rochester's voice calling 'Jane! Jane! Jane!' across the moors — supernatural or psychological.",
    "Indoors at Moor House she hears Rochester's voice cry 'Jane! Jane! Jane!' from nowhere she can place — supernatural or psychological.",
    'Same location correction on the card (see G8 above).'],

  ['G8', 5, 'knowledge_checks', 3, 'q',
    'Jane hears Rochester’s voice calling ‘_____! _____! _____!’ across the moors, which breaks St John’s hold over her.',
    'Indoors at Moor House, Jane hears Rochester’s voice cry ‘_____! _____! _____!’, which breaks St John’s hold over her.',
    'Same location correction in the knowledge check; answer key (index 0 = "Jane") unchanged.'],
];

// glossary rewrites: [ruling, lessonNumber, term, oldDefinition, newDefinition, note]
const GLOSSARY_EDITS = [
  ['G5', 6, 'simile',
    'A direct comparison using ‘like’ or ‘as’; Jane compares Rochester to a ‘caged eagle’ to show his diminished power.',
    'A direct comparison using ‘like’ or ‘as’; the caged eagle ‘might look as looked that sightless Samson’ — Jane’s image for the blinded Rochester.',
    'Glossary example now carries the comparator, so the definition and the example agree.'],
];

const noteMap = new Map();
const addNote = (num, o) => { if (!noteMap.has(num)) noteMap.set(num, []); noteMap.get(num).push(o); };

(async () => {
  const cols = 'id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  L(`\n=== JANE EYRE ADJUDICATION ${DRY ? '(DRY RUN)' : '(LIVE)'} — ${new Date().toISOString()} ===`);
  L(`${rows.length} lessons; all status=${[...new Set(rows.map((r) => r.status))].join(',')}\n`);

  const patches = new Map();
  const stage = (num, field, val) => {
    if (!patches.has(num)) patches.set(num, {});
    patches.get(num)[field] = val;
  };

  for (const [rule, num, field, oldS, newS, note] of EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) throw new Error(`${rule} L${num}.${field}: OLD STRING NOT FOUND\n  ${oldS.slice(0, 200)}`);
    const occ = cur.split(oldS).length - 1;
    if (occ !== 1) throw new Error(`${rule} L${num}.${field}: expected 1 occurrence, found ${occ}`);
    stage(num, field, cur.replace(oldS, newS));
    addNote(num, { ruling: rule, where: field, note, was: oldS, now: newS });
  }

  for (const [rule, num, field, idx, key, oldV, newV, note] of JSON_EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {})[field] ?? row[field];
    const arr = JSON.parse(JSON.stringify(cur));
    if (arr[idx][key] !== oldV) throw new Error(`${rule} L${num}.${field}[${idx}].${key}: MISMATCH\n  expected: ${oldV}\n  actual:   ${arr[idx][key]}`);
    arr[idx][key] = newV;
    stage(num, field, arr);
    addNote(num, { ruling: rule, where: `${field}[${idx}].${key}`, note, was: oldV, now: newV });
  }

  for (const [rule, num, term, oldD, newD, note] of GLOSSARY_EDITS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {}).glossary_terms ?? row.glossary_terms;
    const arr = JSON.parse(JSON.stringify(cur));
    const i = arr.findIndex((g) => g.term === term);
    if (i < 0) throw new Error(`${rule} L${num} glossary term "${term}" not found`);
    if (arr[i].definition !== oldD) throw new Error(`${rule} L${num} glossary "${term}": MISMATCH\n  expected: ${oldD}\n  actual:   ${arr[i].definition}`);
    arr[i].definition = newD;
    stage(num, 'glossary_terms', arr);
    addNote(num, { ruling: rule, where: `glossary_terms["${term}"]`, note, was: oldD, now: newD });
  }

  // narration-id integrity guard: no id may be added, removed or renamed
  for (const [num, fields] of patches.entries()) {
    const row = byNum.get(num);
    for (const f of ['content_html', 'exam_tip_html', 'conclusion_html']) {
      if (!(f in fields)) continue;
      const ids = (s) => [...String(s || '').matchAll(/data-narration-id="([^"]+)"/g)].map((m) => m[1]).join(',');
      if (ids(row[f]) !== ids(fields[f])) throw new Error(`L${num}.${f}: narration ids changed`);
    }
  }

  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT,
    subject: 'english-literature-aqa', unit: 'jane-eyre',
    pass: 'adjudication (rulings on G3-G8; G1 and G2 KEPT untouched)',
    lessons: [],
  };
  const findings = [];
  const writeState = () => fs.writeFileSync(BACKUP, JSON.stringify(backup, null, 1), 'utf8');

  let fieldCount = 0;
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    const before = {};
    for (const k of Object.keys(fields)) before[k] = row[k];
    before.narration_manifest = row.narration_manifest;
    backup.lessons.push({ lesson_number: num, id: row.id, title: row.title, fields_changed: Object.keys(fields), before });
    writeState();

    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}   fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        [${n.ruling}] ${n.where}`);
    fieldCount += Object.keys(fields).length;
    if (!DRY) {
      await q(`lessons?id=eq.${row.id}`, { method: 'PATCH', body: JSON.stringify(fields) });
      L(`      -> PATCHED`);
      backup.lessons[backup.lessons.length - 1].patched_at = new Date().toISOString();
      writeState();
    }
    for (const n of noteMap.get(num) || []) findings.push({ lesson_number: num, lesson_id: row.id, ...n });
    L('');
  }
  L(`${DRY ? 'WOULD PATCH' : 'PATCHED'}: ${patches.size} lessons, ${fieldCount} fields, ${findings.length} edits`);

  if (!DRY) {
    const report = JSON.parse(fs.readFileSync(REPORT, 'utf8'));
    report.adjudication = {
      run_at: new Date().toISOString(),
      rulings: 'G3, G4, G5, G6, G7, G8 applied; G1 and G2 adjudicated KEEP',
      backup: '_adjudication_backup.json',
      lessons_patched: [...patches.keys()].sort((a, b) => a - b),
      fields_patched: fieldCount,
      edits: findings,
    };
    for (const f of report.flagged || []) {
      if (['G3', 'G4', 'G5', 'G6', 'G7', 'G8'].includes(f.id)) f.action = 'EDITED (adjudicated ' + new Date().toISOString().slice(0, 10) + ')';
      if (['G1', 'G2'].includes(f.id)) f.action = 'NOT EDITED (adjudicated KEEP)';
    }
    fs.writeFileSync(REPORT, JSON.stringify(report, null, 1), 'utf8');
  }
  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
