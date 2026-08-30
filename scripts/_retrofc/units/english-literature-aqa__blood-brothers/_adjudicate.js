/**
 * ADJUDICATED RULINGS — english-literature-aqa / blood-brothers.
 *
 * Applies the five rulings Tom adjudicated on the flags left OPEN by the retro
 * fact-check (_report.json .flags). The two KEPT flags ("I could have been him"
 * fragment, premiere date) are deliberately untouched.
 *
 *  1. "That Guy" is a sung DUET (Mickey + Edward), not a soliloquy  -> L6
 *     relabelled in content_html, flashcard_questions and glossary_terms.
 *     "soliloquy" occurs NOWHERE ELSE in the unit (checked), so the glossary
 *     entry would be orphaned; it is replaced by "duet" in lockstep.
 *  2. glossary "agency" restored to its real meaning                -> L5
 *     (both the glossary entry and the inline dfn data-def, which carried the
 *     identical bent definition).
 *  3. invented term "convenient narrative" retired                  -> L5
 *     glossary entry removed; the dfn wrapper unwrapped so the phrase survives
 *     as the lesson's own words. Narrated text is unchanged by an unwrap.
 *  4. ungrammatical flashcard stem                                  -> L2
 *  5. ungrammatical flashcard answer                                -> L5
 *
 * Backs up every field it changes INCREMENTALLY (written BEFORE each PATCH) to
 * _adjudication_backup.json, then PATCHes id=eq. per row.
 *
 * Usage: node scripts/_retrofc/units/english-literature-aqa__blood-brothers/_adjudicate.js --dry-run
 *        node scripts/_retrofc/units/english-literature-aqa__blood-brothers/_adjudicate.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_adjudication_backup.json');
const REPORT = path.join(DIR, '_adjudication_report.json');
const LOGF = path.join(DIR, '_adjudicate.log');
const UNIT = '36556966-f4ec-436b-9ce8-736476fab761';

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

// The duet definition is used verbatim in BOTH the inline dfn and the glossary,
// so the tooltip and the glossary can never drift apart (the failure mode the
// retro fact-check already had to repair for "superstition").
const DUET_DEF = 'A song for two voices, in which each singer’s feelings are heard against the other’s. Mickey and Edward sing “That Guy” as a duet.';
const AGENCY_DEF = 'The capacity of a character to act freely and to choose for themselves. Russell asks how much agency Mickey has left once poverty, unemployment and prison have taken his choices away.';

// ---------------------------------------------------------------- text edits
// [lessonNumber, field, oldSubstring, newSubstring, ruling, note]
const EDITS = [
  // ---- RULING 1: "That Guy" is a sung duet, not a soliloquy ---------------
  [6, 'content_html',
    'His <dfn class="term" data-def="A single character\'s inner thoughts or feelings spoken aloud on stage, allowing the audience direct access to their emotions.">soliloquy</dfn> about wanting to be like “that guy” — confident, smooth, able to talk to Linda — reveals his growing insecurity.',
    `His <dfn class="term" data-def="${DUET_DEF}">duet</dfn> with Edward, “That Guy” — a sung wish to be confident, smooth, able to talk to Linda — reveals his growing insecurity.`,
    'RULING 1',
    '"That Guy" is a sung duet between Mickey and Edward, not a solo spoken speech, so "soliloquy" was wrong on both counts. The lesson also contradicted itself: KC1 already called it "Mickey’s song about ‘that guy’". The substance (an idealised masculinity, not Eddie) is unchanged.'],

  // ---- RULING 2: "agency" restored to its real meaning --------------------
  [5, 'content_html',
    'data-def="In literary analysis, the forces or factors that ultimately bring about the tragic outcome. Russell argues that the real agent of the tragedy is the class system, not any individual character.">agency</dfn>',
    `data-def="${AGENCY_DEF}">agency</dfn>`,
    'RULING 2',
    'the inline definition carried the same bent meaning as the glossary entry: "agency" was defined as the forces that bring about the outcome, which is not what the word means. Restored to the standard sense — the capacity to act and choose — applied to Mickey. Attribute-only edit, so the narrated text is unchanged.'],

  // ---- RULING 3: retire the invented term "convenient narrative" ----------
  [5, 'content_html',
    'it is a <dfn class="term" data-def="A simplified, often misleading explanation that distracts from the real, more complex cause. Russell suggests that blaming superstition for the tragedy distracts from the real cause: class inequality.">convenient narrative</dfn> that distracts',
    'it is a convenient narrative that distracts',
    'RULING 3',
    '"convenient narrative" is not an established critical term but sat in the glossary beside real terminology (cyclical structure, rhetorical question), so a student could carry it into an exam believing it was subject terminology. The dfn wrapper is removed and the phrase survives as the lesson’s own plain words. Tag-only edit, so the narrated text is unchanged.'],
];

// ----------------------------------------------------------- glossary edits
// [lessonNumber, existingTerm, replacementObject|null]   (null = remove entry)
const GLOSSARY_OPS = [
  [6, 'soliloquy', { term: 'duet', definition: DUET_DEF },
    'RULING 1', 'the term is orphaned once "That Guy" is correctly labelled: "soliloquy" appears nowhere else in this unit (verified across all 7 lessons, every field). Replaced by "duet", which is what the prose now highlights, so glossary and dfn stay 1:1.'],
  [5, 'agency', { term: 'agency', definition: AGENCY_DEF },
    'RULING 2', 'restored to the standard meaning of "agency"; identical to the inline dfn so tooltip and glossary agree.'],
  [5, 'convenient narrative', null,
    'RULING 3', 'invented term removed from the glossary; the phrase stays in the prose as the lesson’s own wording.'],
];

// --------------------------------------------------------- flashcard edits
// [lessonNumber, matcherOnQ, newQ|null, newA|null, ruling, note]
const FC_OPS = [
  [6, /adolescent soliloquy about 'that guy'/,
    'What does Mickey’s adolescent duet with Edward, ‘That Guy’, expose?', null,
    'RULING 1', 'card called the sung duet a soliloquy. Answer unchanged — only the label was wrong.'],
  [2, /How does Russell's sympathy between the two mothers land\?/,
    'Where do Russell’s sympathies lie between the two mothers?', null,
    'RULING 4', 'ungrammatical stem ("how does sympathy ... land?"). Meaning unchanged; answer untouched.'],
  [5, /What is the 'convenient narrative' Russell argues society tells itself\?/,
    null, 'The myth of meritocracy — that poverty is caused by laziness, not by the system.',
    'RULING 5', 'ungrammatical answer: "not system" needed an article. Meaning unchanged.'],
];

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== ADJUDICATED RULINGS: english-literature-aqa / blood-brothers ===`);
  L(`run: ${new Date().toISOString()}   mode: ${DRY ? 'DRY RUN' : 'LIVE'}`);

  const cols = 'id,lesson_number,title,slug,description,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  L(`fetched ${rows.length} lessons (live: ${rows.filter((r) => r.status === 'live').length})`);

  // Independent re-check of the ruling-1 precondition, in this run, before writing.
  const soliloquyHits = [];
  for (const r of rows) {
    const blob = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + (r.description || '') +
      JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
    const n = (blob.match(/soliloqu/gi) || []).length;
    if (n) soliloquyHits.push(`L${r.lesson_number}×${n}`);
  }
  L(`"soliloquy" occurrences before the fix: ${soliloquyHits.join(', ') || 'none'}`);
  if (soliloquyHits.some((h) => !h.startsWith('L6'))) {
    L('  !! soliloquy is used outside L6 — the glossary entry must be KEPT, not replaced. ABORTING.');
    process.exit(1);
  }
  L('');

  const byNum = new Map(rows.map((r) => [r.lesson_number, r]));
  const patches = new Map();
  const noteMap = new Map();
  const addNote = (n, o) => { if (!noteMap.has(n)) noteMap.set(n, []); noteMap.get(n).push(o); };
  const stage = (num, field, val) => { if (!patches.has(num)) patches.set(num, {}); patches.get(num)[field] = val; };

  // 1. exact-string edits
  for (const [num, field, oldS, newS, ruling, note] of EDITS) {
    const row = byNum.get(num);
    if (!row) { L(`  !! L${num} not found`); process.exitCode = 1; continue; }
    const cur = (patches.get(num) || {})[field] ?? row[field];
    if (!cur.includes(oldS)) {
      L(`  !! L${num}.${field}: PATTERN NOT FOUND -> ${ruling}`);
      L(`     looking for: ${oldS.slice(0, 140)}`);
      process.exitCode = 1;
      continue;
    }
    stage(num, field, cur.replace(oldS, newS));
    addNote(num, { ruling, where: field, note, before: oldS, after: newS });
  }

  // 2. glossary edits
  for (const [num, term, repl, ruling, note] of GLOSSARY_OPS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {}).glossary_terms ?? row.glossary_terms;
    if (!Array.isArray(cur)) { L(`  !! L${num} glossary_terms not an array`); process.exitCode = 1; continue; }
    const i = cur.findIndex((g) => g.term === term);
    if (i < 0) { L(`  !! L${num} glossary term "${term}" NOT FOUND`); process.exitCode = 1; continue; }
    const before = cur[i];
    const out = cur.slice();
    if (repl) out[i] = repl; else out.splice(i, 1);
    stage(num, 'glossary_terms', out);
    addNote(num, { ruling, where: `glossary_terms[${i}]`, note,
      before: JSON.stringify(before), after: repl ? JSON.stringify(repl) : '(entry removed)' });
  }

  // 3. flashcard edits
  for (const [num, re, newQ, newA, ruling, note] of FC_OPS) {
    const row = byNum.get(num);
    const cur = (patches.get(num) || {}).flashcard_questions ?? row.flashcard_questions;
    if (!Array.isArray(cur)) { L(`  !! L${num} flashcard_questions not an array`); process.exitCode = 1; continue; }
    const i = cur.findIndex((f) => re.test(f.q || ''));
    if (i < 0) { L(`  !! L${num} flashcard ${re} NOT FOUND`); process.exitCode = 1; continue; }
    const before = { q: cur[i].q, a: cur[i].a };
    const out = cur.slice();
    out[i] = { ...cur[i] };
    if (newQ) out[i].q = newQ;
    if (newA) out[i].a = newA;
    stage(num, 'flashcard_questions', out);
    addNote(num, { ruling, where: `flashcard_questions[${i}]`, note,
      before: JSON.stringify(before), after: JSON.stringify({ q: out[i].q, a: out[i].a }) });
  }

  // 4. INCREMENTAL backup + patch, lesson by lesson
  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT,
    subject: 'english-literature-aqa', unit: 'blood-brothers',
    purpose: 'adjudicated rulings on the OPEN flags of the retro fact-check', lessons: [],
  };
  const report = {
    generated_at: new Date().toISOString(), subject: 'english-literature-aqa', unit: 'blood-brothers',
    purpose: 'adjudicated rulings', lessons_total: rows.length, lessons: [],
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
    writeState();   // persisted BEFORE the write; a killed run loses nothing

    L(`L${String(num).padStart(2, '0')}  ${row.title}`);
    L(`      id=${row.id}   fields: ${Object.keys(fields).join(', ')}`);
    for (const n of noteMap.get(num) || []) L(`        [${n.ruling}] ${n.where}: ${n.note.slice(0, 160)}`);
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
  report.rulings_applied = report.lessons.reduce((a, l) => a + l.findings.length, 0);
  L(`ruling edits: ${report.rulings_applied}`);
  writeState();
  fs.appendFileSync(LOGF, log.join('\n') + '\n', 'utf8');
})().catch((e) => { console.error(e); process.exit(1); });
