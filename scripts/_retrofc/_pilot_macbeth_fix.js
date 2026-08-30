/**
 * Retro fact-check PILOT — english-literature-aqa / macbeth.
 *
 * Backs up every field it will change to _pilot_macbeth_backup.json BEFORE the
 * first write, then applies surgical PATCHes (id=eq.) to Supabase.
 *
 * Usage:  node scripts/_retrofc/_pilot_macbeth_fix.js --dry-run
 *         node scripts/_retrofc/_pilot_macbeth_fix.js
 */
const fs = require('fs');
const path = require('path');
const URL = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = path.join(__dirname);
const BACKUP = path.join(DIR, '_pilot_macbeth_backup.json');
const UNIT = 'ce6cd0d6-72b3-47fe-aafd-57d396898470';

const log = [];
function L(s) { console.log(s); log.push(s); }

async function q(p, opts) {
  const r = await fetch(`${URL}/rest/v1/${p}`, {
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
    ...opts,
  });
  if (!r.ok) throw new Error(`${p} -> ${r.status} ${await r.text()}`);
  return r.json();
}

// ---------------------------------------------------------------- text edits
// [lessonNumber, field, oldSubstring, newSubstring, note]
const EDITS = [
  // ---- L1 -----------------------------------------------------------------
  [1, 'content_html',
    'Understanding this context is essential For the exam . The play was written',
    'Understanding this context is essential for the exam. The play was written',
    'LOW n3: stray capital + space before full stop'],

  // ---- L2 -----------------------------------------------------------------
  [2, 'content_html',
    'This connects to the Aristotelian structure of tragedy that Shakespeare’s audience would have recognised.',
    'This connects to the classical tradition of tragedy — the fall of a great man from high status — which reached English drama through Roman playwrights such as Seneca, and which later critics describe using Aristotle’s term <em>hamartia</em>.',
    'MEDIUM n12: Aristotelian structure was not what a Jacobean playhouse audience would have recognised'],

  // ---- L3 -----------------------------------------------------------------
  [3, 'content_html',
    'data-def="A direct address to an absent person, a dead person, or an abstract concept, used in drama and poetry to heighten emotion."',
    'data-def="A calling upon a god, spirit, or supernatural power for help, inspiration, or protection."',
    'MEDIUM: "invocation" was given the definition of apostrophe'],

  // ---- L4 -----------------------------------------------------------------
  [4, 'content_html',
    'analyze what sleep symbolizes',
    'analyse what sleep symbolises',
    'LOW: US spelling in revision tip (house rule: British English)'],

  // ---- L5 -----------------------------------------------------------------
  [5, 'content_html',
    'The irony is clear: she who said “a little water clears us” now believes “all great Neptune’s ocean” cannot wash away the bloodstains.',
    'The irony is clear: she who said “a little water clears us” now finds that “all the perfumes of Arabia will not sweeten this little hand.”',
    'HIGH n14: "all great Neptune’s ocean" is MACBETH’s line (2.2), not Lady Macbeth’s — contradicted L4'],
  [5, 'content_html',
    'data-def="Relating to the religious beliefs and practices of the early 1600s."',
    'data-def="Relating to the reign of King James I of England (1603–1625)."',
    'MEDIUM: "Jacobean" misdefined; contradicted L1'],

  // ---- L6 -----------------------------------------------------------------
  [6, 'content_html',
    'This <dfn class="term" data-def="A comparison between two unlike things using connecting words such as ‘like’ or ‘as.’">simile</dfn> of wading through a river of blood',
    'This <dfn class="term" data-def="A figure of speech in which one thing is described as being another, without using ‘like’ or ‘as.’">metaphor</dfn> of wading through a river of blood',
    'HIGH n18: "I am in blood / Stepped in so far" is a metaphor, not a simile (AO2 terminology)'],
  [6, 'content_html',
    'barren sceptre in my grip” (Act 3, Scene 1)',
    'barren sceptre in my gripe” (Act 3, Scene 1)',
    'LOW n20: key quotation misquoted — the word is "gripe"'],
  [6, 'content_html',
    "describe where Banquo's ghost sits and what it symbolizes",
    "describe where Banquo's ghost sits and what it symbolises",
    'LOW: US spelling in revision tip'],

  // ---- L7 -----------------------------------------------------------------
  [7, 'content_html',
    'Shakespeare stages the murder of Lady Macduff and her young son to maximise the audience’s horror.',
    'Shakespeare stages the murder of Lady Macduff’s young son, then has her hunted down offstage moments later, to maximise the audience’s horror.',
    'LOW n14: only the son is killed on stage; Lady Macduff flees and is killed offstage'],
  [7, 'content_html',
    'and that people are “float upon a wild and violent sea.”',
    'and that people “float upon a wild and violent sea.”',
    'LOW n17: broken quote splice ("people are float upon")'],

  // ---- L8 -----------------------------------------------------------------
  [8, 'content_html',
    'Malcolm describes Scotland as a place where “Each new morn / New widows howl, new orphans cry.” Macduff calls Scotland their “down-fallen birthright.”',
    'Macduff calls the country their “down-fall’n birthdom,” a place where “each new morn / New widows howl, new orphans cry.”',
    'HIGH n17: "Each new morn..." is MACDUFF’s line (4.3), not Malcolm’s; and the word is "birthdom", not "birthright"'],

  // ---- L9 -----------------------------------------------------------------
  [9, 'content_html',
    'data-def="The act of killing oneself, considered a mortal sin in Christian teaching, meaning the person would be denied a Christian burial and condemned to Hell."',
    'data-def="In Christian teaching, a grave sin committed knowingly and willingly, believed to cut the soul off from God’s grace. Suicide was counted among them, so the person was denied Christian burial."',
    'MEDIUM: "mortal sin" was defined as "the act of killing oneself" — conflated with suicide'],
];

// ------------------------------------------------------- JSON-field rewriters
function fixGlossary(lessonNumber, terms) {
  if (!Array.isArray(terms)) return { out: terms, notes: [] };
  const notes = [];
  const out = terms.map((t) => {
    const e = { ...t };
    if (lessonNumber === 3 && e.term === 'invocation') {
      e.definition = 'A calling upon a god, spirit, or supernatural power for help, inspiration, or protection.';
      notes.push('MEDIUM glossary: "invocation" was defined as apostrophe');
    }
    if (lessonNumber === 5 && e.term === 'equivocation') {
      e.definition = 'The use of ambiguous language to deceive without technically lying — a practice Jacobeans associated with the Gunpowder Plot conspirators.';
      notes.push('MEDIUM glossary: "equivocation" was given the definition of dramatic irony');
    }
    if (lessonNumber === 6 && e.term === 'simile') {
      e.term = 'metaphor';
      e.definition = 'A figure of speech in which one thing is described as being another, without using ‘like’ or ‘as.’';
      notes.push('HIGH glossary: "simile" replaced by "metaphor" to match the corrected n18');
    }
    if (lessonNumber === 6 && e.term === 'projection') {
      e.definition = 'The unconscious transfer of inner guilt, fear, or desire onto an external image or event.';
      notes.push('LOW glossary: "projection" was defined circularly');
    }
    if (lessonNumber === 8 && e.term === 'king-becoming graces') {
      e.definition = 'The twelve virtues Malcolm names as the marks of a good king: justice, verity, temperance, stableness, bounty, perseverance, mercy, lowliness, devotion, patience, courage, fortitude.';
      notes.push('LOW glossary: listed only 8 of the 12 graces the lesson says Malcolm names');
    }
    if (lessonNumber === 9 && e.term === 'mortal sin') {
      e.definition = 'In Christian teaching, a grave sin committed knowingly and willingly, believed to cut the soul off from God’s grace. Suicide was counted among them, so the person was denied Christian burial.';
      notes.push('MEDIUM glossary: "mortal sin" was defined as "the act of killing oneself"');
    }
    return e;
  });
  return { out, notes };
}

function fixFlashcards(lessonNumber, cards) {
  if (!Array.isArray(cards)) return { out: cards, notes: [] };
  const notes = [];
  const out = cards.map((c) => {
    const e = { ...c };
    if (lessonNumber === 5 && /Whose families does Macbeth order murdered/.test(e.q || '')) {
      e.a = "Banquo's — though his son Fleance escapes — and Macduff's, whose wife and children are massacred.";
      notes.push('MEDIUM flashcard: answer said Banquo’s family was "successfully killed"; Fleance escapes (contradicted L6)');
    }
    if (lessonNumber === 9 && /bathetic dismissal/.test(e.q || '')) {
      e.q = 'Whose earlier dismissal of guilt is bitterly ironic by Act 5?';
      notes.push('LOW flashcard: "bathetic" misused and above GCSE register');
    }
    return e;
  });
  return { out, notes };
}

function fixPracticeQuestions(lessonNumber, qs) {
  if (!Array.isArray(qs)) return { out: qs, notes: [] };
  const notes = [];
  const out = qs.map((pq, i) => {
    const e = { ...pq };
    let m = e.marks || '';
    const type = e.type || '';

    // (A) two different bands both labelled "Top band" -> monotone ladder
    if ((m.match(/Top band/g) || []).length > 1 && /Top band \(19-24\)/.test(m)) {
      m = m.replace('Upper-mid band (13-18)', 'Mid band (13-18)')
           .replace('Top band (19-24)', 'Upper-mid band (19-24)');
      notes.push(`MEDIUM pq[${i}]: two bands both labelled "Top band"; ladder relabelled`);
    }

    // (B) type says 30 marks but the ladder tops out at 12 -> rescale x2.5
    if (/^30 marks/.test(type) && /Top band \(10-12\)/.test(m)) {
      m = m.replace('Top band (10-12)', 'Top band (25-30)')
           .replace('Upper-mid band (7-9)', 'Upper-mid band (18-24)')
           .replace('Lower-mid band (4-6)', 'Lower-mid band (10-17)')
           .replace('Lower band (1-3)', 'Lower band (1-9)');
      notes.push(`MEDIUM pq[${i}]: type "${type}" carried a 12-mark band ladder; rescaled to 30`);
    }

    // (C) type says 4 marks but the ladder is a 6-mark scheme
    if (/^4 marks/.test(type) && /^6 marks:/m.test(m)) {
      m = m.replace(/^6 marks:/m, '4 marks:')
           .replace(/^4-5 marks:/m, '3 marks:')
           .replace(/^2-3 marks:/m, '2 marks:');
      notes.push(`MEDIUM pq[${i}]: type "${type}" carried a 6-mark band ladder; rescaled to 4`);
    }

    // (D) L6 simile -> metaphor in the question text and its band descriptor
    if (lessonNumber === 6) {
      if (/the simile “I am in blood/.test(e.text || '')) {
        e.text = e.text.replace('the simile “I am in blood', 'the metaphor “I am in blood');
        notes.push(`HIGH pq[${i}]: question called the "I am in blood" image a simile`);
      }
      if (/river of blood simile/.test(m)) m = m.replace('river of blood simile', 'river of blood metaphor');
    }

    e.marks = m;
    return e;
  });
  return { out, notes };
}

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== RETRO FACT-CHECK PILOT: english-literature-aqa / macbeth ===`);
  L(`run: ${new Date().toISOString()}   mode: ${DRY ? 'DRY RUN' : 'LIVE'}`);

  const cols = 'id,lesson_number,title,content_html,conclusion_html,exam_tip_html,description,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  L(`fetched ${rows.length} lessons\n`);

  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  const patches = new Map();   // lesson_number -> {field: newValue}
  const noteMap = new Map();   // lesson_number -> [notes]
  const addNote = (n, s) => { if (!noteMap.has(n)) noteMap.set(n, []); noteMap.get(n).push(s); };

  // 1. text edits
  for (const [num, field, oldS, newS, note] of EDITS) {
    const row = byNum.get(num);
    if (!row) { L(`  !! L${num} not found`); continue; }
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) {
      L(`  !! L${num}.${field}: PATTERN NOT FOUND -> ${note}`);
      L(`     looking for: ${oldS.slice(0, 90)}`);
      process.exitCode = 1;
      continue;
    }
    const next = cur.replace(oldS, newS);
    if (!patches.has(num)) patches.set(num, {});
    patches.get(num)[field] = next;
    addNote(num, note);
  }

  // 2. JSON-field edits
  for (const row of rows) {
    const num = row.lesson_number;
    const g = fixGlossary(num, row.glossary_terms);
    const f = fixFlashcards(num, row.flashcard_questions);
    const p = fixPracticeQuestions(num, row.practice_questions);
    if (JSON.stringify(g.out) !== JSON.stringify(row.glossary_terms)) {
      if (!patches.has(num)) patches.set(num, {});
      patches.get(num).glossary_terms = g.out;
    }
    if (JSON.stringify(f.out) !== JSON.stringify(row.flashcard_questions)) {
      if (!patches.has(num)) patches.set(num, {});
      patches.get(num).flashcard_questions = f.out;
    }
    if (JSON.stringify(p.out) !== JSON.stringify(row.practice_questions)) {
      if (!patches.has(num)) patches.set(num, {});
      patches.get(num).practice_questions = p.out;
    }
    [...g.notes, ...f.notes, ...p.notes].forEach((s) => addNote(num, s));
  }

  // 3. BACKUP every field about to change, BEFORE any write
  const backup = { generated_at: new Date().toISOString(), unit_id: UNIT, subject: 'english-literature-aqa', unit: 'macbeth', lessons: [] };
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    const before = {};
    for (const k of Object.keys(fields)) before[k] = row[k];
    before.narration_manifest = row.narration_manifest;   // so clips are restorable too
    backup.lessons.push({ lesson_number: num, id: row.id, title: row.title, fields_changed: Object.keys(fields), before });
  }
  fs.writeFileSync(BACKUP, JSON.stringify(backup, null, 1), 'utf8');
  L(`BACKUP written: ${BACKUP}  (${backup.lessons.length} lessons)\n`);

  // 4. report + write
  let fieldCount = 0;
  for (const [num, fields] of [...patches.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}`);
    L(`      fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        - ${n}`);
    fieldCount += Object.keys(fields).length;
    if (!DRY) {
      await q(`lessons?id=eq.${row.id}`, { method: 'PATCH', body: JSON.stringify(fields) });
      L(`      -> PATCHED`);
    }
    L('');
  }
  L(`${DRY ? 'WOULD PATCH' : 'PATCHED'}: ${patches.size} lessons, ${fieldCount} fields`);

  fs.appendFileSync(path.join(DIR, '_pilot_macbeth.log'), log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
