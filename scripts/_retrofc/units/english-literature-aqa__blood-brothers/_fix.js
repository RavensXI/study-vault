/**
 * Retro fact-check FIX — english-literature-aqa / blood-brothers.
 *
 * Backs up every field it changes INCREMENTALLY (written BEFORE each PATCH)
 * to _backup.json, then PATCHes id=eq. per row.
 *
 * Usage:  node scripts/_retrofc/units/english-literature-aqa__blood-brothers/_fix.js --dry-run
 *         node scripts/_retrofc/units/english-literature-aqa__blood-brothers/_fix.js
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = __dirname;
const BACKUP = path.join(DIR, '_backup.json');
const REPORT = path.join(DIR, '_report.json');
const LOGF = path.join(DIR, '_fix.log');
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

// ---------------------------------------------------------------- text edits
// [lessonNumber, field, oldSubstring, newSubstring, severity, note]
const EDITS = [
  // ---- L7: AO2 denial (mark-affecting) -----------------------------------
  [7, 'content_html',
    'Modern text essay questions reward a clear argument, evidence from memory, and context woven into your analysis. Close language analysis is not the focus here — what matters is what Russell is saying and how his choices serve his political message. Most modern text exams are closed book, so you must recall quotations from memory. Check your exam board’s specimen paper for the exact mark weightings and assessment objectives that apply to you.',
    'Modern text essay questions reward a clear argument, evidence from memory, analysis of Russell’s methods, and context woven throughout. There is no printed extract — you write a whole-text essay from memory — but analysis of language, form and structure is still assessed. AO2 is worth 12 of the 30 marks, exactly as many as AO1, so writing about how Russell makes his meaning is not optional. The question is closed book, so you must recall quotations from memory.',
    'HIGH', 'AO2 IS assessed on AQA Paper 2 Section A: the mark scheme reads "Section A: Modern texts Questions 1-24 (30 marks - AO1=12, AO2=12, AO3=6)". Telling students that "close language analysis is not the focus" steers them away from 12 of the 30 marks. Also removed the vague "check your exam board" hedge from board-specific AQA content.'],
  [7, 'conclusion_html',
    'The Modern Texts essay tests AO1 (analysis with evidence), AO3 (context), and AO4 (SPaG). There is no extract and no AO2 — memorise quotations and embed context throughout.',
    'The Modern Texts essay tests AO1 (12 marks), AO2 (12 marks — Russell’s methods), AO3 (6 marks — context) and AO4 (4 marks — SPaG). There is no printed extract, but AO2 still carries as much as AO1 — memorise quotations and analyse how Russell writes.',
    'HIGH', 'FALSE: AO2 is assessed on the AQA Modern Texts question and is worth 12 of the 30 marks (mark scheme: AO1=12, AO2=12, AO3=6). The absence of a printed extract does not remove AO2.'],

  // ---- L7: rival-text debris left in a live quotation list ----------------
  [7, 'content_html',
    '“I could have been him” — Mickey’s recognition that class determined his fate. “Could it be what we, the English, have come to know as class?” — the Narrator’s thesis. “Look like the innocent flower” — wait, that’s Macbeth. Stick to <em>Blood Brothers</em> quotations in a <em>Blood Brothers</em> essay!',
    '“I could have been him” — Mickey’s recognition that class determined his fate. “Could it be what we, the English, have come to know as class?” — the Narrator’s thesis. Learn a short quotation for each major character and each major theme, and make sure every one of them is from <em>Blood Brothers</em>.',
    'HIGH', 'A Macbeth quotation ("Look like the innocent flower") plus an unedited authorial aside ("wait, that’s Macbeth") was left in the live "Key Quotations to Memorise" list. Rival-text intrusion in a memorisation list a student is told to learn.'],

  // ---- L1: context claims ------------------------------------------------
  [1, 'content_html',
    'unemployment hit 25%',
    'unemployment passed 20% city-wide and topped 30% in the worst-hit inner-city wards',
    'MEDIUM', 'no source supports a flat 25% city-wide figure. Liverpool exceeded 20% by 1985 (about double the national rate), with some inner-city wards above 30%. Replaced with the sourced framing.'],
  [1, 'content_html',
    'The government’s own advisors reportedly suggested a policy of “managed decline” for the city.',
    'After the 1981 Toxteth riots the Chancellor of the Exchequer, Sir Geoffrey Howe, privately advised Margaret Thatcher not to forget “the option of managed decline” for the city — a memo released by the National Archives in 2011.',
    'MEDIUM', 'misattribution: the "managed decline" memo was written by Sir Geoffrey Howe, then Chancellor of the Exchequer and a senior cabinet minister — not by "the government\'s own advisors". "Reportedly" also understates it: the memo is a released public record (National Archives, 30 Dec 2011).'],

  // ---- L2: fabricated / misquoted wording --------------------------------
  [2, 'content_html',
    'practical arguments (“you already have seven children”)',
    'practical arguments (“you said yourself, you had too many children already”)',
    'MEDIUM', 'the quoted wording is not in the play. Mrs Lyons\' actual line is "You said yourself, you had too many children already"; the number seven was layered onto a real quotation. (Seven children is correct as a FACT — it is only wrong inside this quotation.)'],
  [2, 'content_html',
    'Her husband courted her because she looked like Monroe, but abandoned her when “the glamour wore off.',
    'Her husband told her she was “sexier than Marilyn Monroe”, but walked out and left her to raise the children alone.',
    'MEDIUM', 'fabricated quotation: "the glamour wore off" appears in no source and is not wording from the play. Replaced with the verified line "He told me I was sexier than Marilyn Monroe".'],

  // ---- L3: misattributed insult ------------------------------------------
  [3, 'content_html',
    'She tells Eddie that Mickey is a “horrible boy” and forbids the friendship.',
    'She rounds on Eddie for behaving “like a horrible little boy” like Mickey’s crowd, and forbids the friendship.',
    'HIGH', 'the insult is pointed the wrong way. Mrs Lyons does not call Mickey a "horrible boy" — she says it TO Edward about Edward\'s own behaviour ("like a, like a horrible little boy, like them"), accusing him of becoming like Mickey and his friends.'],
  [3, 'content_html',
    'Linda joins their games as a confident, fearless girl who is better at shooting than either boy.',
    'Linda joins their games as a confident, fearless girl — in the park scene with the stolen gun she is the only one of the three to hit the target.',
    'LOW', 'overstated: sources support a single scene in which only Linda hits the target, not a running claim that she is a better shot than either boy.'],

  // ---- L4: fabricated quotation ------------------------------------------
  [4, 'content_html',
    'The childlike admiration — “you’re brilliant” — curdles into resentment.',
    'The childlike admiration — “if I was like him I’d know all the right words” — curdles into resentment.',
    'MEDIUM', 'fabricated quotation: "you\'re brilliant" appears in no source. Replaced with a verified line of Mickey\'s admiration for Eddie.'],

  // ---- L5: the ending is misdescribed ------------------------------------
  [5, 'content_html',
    'The stage direction states that the gun goes off as police marksmen shoot Mickey. There is deliberate ambiguity about whether Mickey intentionally fires at Eddie or whether the police action causes the gun to discharge. Russell leaves this unclear because the identity of the trigger-puller is less important than the',
    'Mickey shoots Eddie; the police marksmen then shoot Mickey. Two guns, two deaths, seconds apart. What Russell leaves genuinely open is not who fired but where the',
    'HIGH', 'factually wrong about the ending: sources agree Mickey shoots Eddie FIRST and the police then shoot Mickey. The "ambiguity about whether the police action causes the gun to discharge" is invented, and the appeal to a stage direction could not be verified from any citable source. The real, teachable ambiguity is about RESPONSIBILITY, which the rewrite keeps.'],
  [5, 'content_html',
    'Whether Mickey pulls the trigger or the police do, the result is the same: two working-class deaths caused by a system that separated them, denied one of them opportunity, and left him with nothing to lose.',
    'Mickey has been stripped of work, liberty and hope long before he picks up the gun, so the ending forces the question: is Mickey the cause of these two working-class deaths, or is the system that separated the twins and denied one of them every opportunity?',
    'HIGH', 'follows the correction above: the false either/or ("whether Mickey pulls the trigger or the police do") is replaced with the genuine question of agency.'],
  [5, 'content_html',
    'Both twins die in the final scene. Russell deliberately leaves ambiguity about the immediate cause (Mickey’s finger or police gunfire) because his point is that the real killer is the class system.',
    'Both twins die in the final scene: Mickey shoots Eddie, and the police marksmen then shoot Mickey. Russell’s point is not that the mechanics are unclear but that the real killer is the class system.',
    'HIGH', 'same invented mechanical ambiguity repeated in the Key Fact box.'],

  // ---- L6: Linda overstated (matches the L3 correction) ------------------
  [6, 'content_html',
    'Linda is introduced as a bold, fearless child who can outshoot both boys and speaks her mind.',
    'Linda is introduced as a bold, fearless child who plays as hard as the boys — she is the only one of the three to hit the target in the park — and speaks her mind.',
    'LOW', 'overstated in the same way as L3; corrected in lockstep so the two lessons agree.'],

  // ---- L1 / L5: play quotation over the 15-word ceiling -------------------
  [1, 'content_html',
    'The Narrator’s recurring question — “And do we blame superstition for what came to pass? Or could it be what we, the English, have come to know as class?” — directly invites',
    'The Narrator’s recurring question — “could it be what we, the English, have come to know as class?” — directly invites',
    'MEDIUM', 'copyright: 24-word verbatim quotation from an in-copyright play, over the 15-word house ceiling. Trimmed to the 13-word form already used in this lesson’s own conclusion and in L5/L7 flashcards.'],
  [5, 'content_html',
    'The Narrator’s final question — “And do we blame superstition for what came to pass? Or could it be what we, the English, have come to know as class?” — tells the audience',
    'The Narrator’s final question — “could it be what we, the English, have come to know as class?” — tells the audience',
    'MEDIUM', 'copyright: 24-word verbatim quotation trimmed to the 13-word form used elsewhere in the unit.'],
  [5, 'content_html',
    'The play ends with the Narrator addressing the audience directly: “And do we blame superstition for what came to pass? Or could it be what we, the English, have come to know as class?” This is Russell’s thesis statement.',
    'The play ends with the Narrator addressing the audience directly: does the blame lie with superstition, or with “what we, the English, have come to know as class”? This is Russell’s thesis statement.',
    'MEDIUM', 'copyright: 24-word verbatim quotation trimmed to 10 quoted words; the superstition/class dichotomy is preserved in reported speech.'],

  // ---- L1: glossary term defined as the debate, not the term --------------
  [1, 'content_html',
    'data-def="The debate about whether a person\'s character and success are determined by genetics (nature) or environment and upbringing (nurture).">nurture</dfn>',
    'data-def="The influence of environment, upbringing and social class on a person\'s character and life chances, as opposed to inherited nature.">nurture</dfn>',
    'LOW', 'the highlighted term is "nurture" but the definition defined the whole nature-versus-nurture debate, so the tooltip did not define the word the student clicked.'],

  // ---- L2: one term, two different inline definitions ---------------------
  [2, 'content_html',
    'data-def="Irrational beliefs in luck, fate, or supernatural consequences. Russell uses superstition as a metaphor for the powerlessness of the working class.">superstition</dfn>',
    'data-def="Irrational belief in luck, fate, or supernatural consequences. Russell uses it as a metaphor for the powerlessness of the working class, and Mrs Lyons invents one to control Mrs Johnstone.">superstition</dfn>',
    'LOW', 'the term "superstition" carried two different data-def values in the same lesson (the Mrs Lyons-specific one at n8 and a generic one at n12). Merged so both uses agree.'],
];

// ------------------------------------------------------- JSON-field rewrites
const CANON_LADDER = { '26-30': 'Top band', '21-25': 'Upper band', '16-20': 'Upper-mid band', '11-15': 'Mid band', '6-10': 'Lower-mid band', '1-5': 'Lower band' };
const BAD_TYPE = '30+4 marks — Shakespeare Essay';
const GOOD_TYPE = '30+4 marks — Modern Text Essay';

function fixPracticeQuestions(num, pqs) {
  if (!Array.isArray(pqs)) return { out: pqs, notes: [] };
  const notes = [];
  const out = pqs.map((pq, i) => {
    const e = { ...pq };
    if (e.type === BAD_TYPE) {
      e.type = GOOD_TYPE;
      notes.push({ severity: 'HIGH', where: `practice_questions[${i}].type`,
        note: 'Blood Brothers is a MODERN TEXT (AQA 8702 s3.2.1, Paper 2 Section A), not a Shakespeare play. Sibling AQA modern-text units already use "30+4 marks — Modern Text Essay".',
        before: BAD_TYPE, after: GOOD_TYPE });
    }
    if (typeof e.marks === 'string') {
      const before = e.marks;
      // Relabel every band by its MARK RANGE, which is unambiguous.
      const after = before.replace(
        /(Top band|Upper band|Upper-mid band|Mid band|Lower-mid band|Lower band)(\s*\(?\s*)(\d+)(\s*[–-]\s*)(\d+)/g,
        (m, label, gap, lo, dash, hi) => {
          const want = CANON_LADDER[`${lo}-${hi}`];
          return want ? `${want}${gap}${lo}${dash}${hi}` : m;
        });
      if (after !== before) {
        e.marks = after;
        notes.push({ severity: 'MEDIUM', where: `practice_questions[${i}].marks`,
          note: 'band ladder had a duplicated "Top band" label and a missing band, so it did not present six distinct labels against the six mark ranges. Relabelled from the mark ranges using the ladder independently derived from healthy AQA modern-text units.',
          before: before.replace(/\n/g, ' | ').slice(0, 260), after: after.replace(/\n/g, ' | ').slice(0, 260) });
      }
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
    if (num === 7 && /Which assessment objectives are tested in the AQA Modern Texts essay/.test(e.q || '')) {
      notes.push({ severity: 'HIGH', where: `knowledge_checks[${i}]`,
        note: 'the keyed answer was "AO1, AO3, and AO4", i.e. it taught that AO2 is NOT assessed on the Modern Texts question. AO2 is assessed. Option set rewritten so the correct answer is available.',
        before: JSON.stringify({ correct: e.correct, options: e.options }),
        after: JSON.stringify({ correct: 3, options: ['AO1 and AO2 only', 'AO1, AO2 and AO3 only', 'AO2, AO3 and AO4 only', 'AO1, AO2, AO3 and AO4'] }) });
      e.options = ['AO1 and AO2 only', 'AO1, AO2 and AO3 only', 'AO2, AO3 and AO4 only', 'AO1, AO2, AO3 and AO4'];
      e.correct = 3;
    }
    return e;
  });
  return { out, notes };
}

// Flashcards that must move in lockstep with the prose corrections above.
// [lesson, matcher on q, newQ|null, newA, severity, note]
const FC_EDITS = [
  [1, /Roughly what unemployment rate did Liverpool reach under Thatcher/, null,
    'Over 20% city-wide — above 30% in the worst-hit inner-city wards.',
    'MEDIUM', 'answer was a flat "25%", which no source supports as a city-wide figure.'],
  [1, /What alleged government policy was suggested for 1980s Liverpool/,
    'Who privately advised “managed decline” for 1980s Liverpool?',
    'Chancellor Sir Geoffrey Howe, in a 1981 memo released in 2011.',
    'MEDIUM', 'the memo is a released public record, not an "alleged" policy from unnamed advisors; Howe was Chancellor of the Exchequer.'],
  [2, /Why is Mrs Johnstone's husband absent/, null,
    'He walked out, leaving her to raise the children alone.',
    'MEDIUM', 'answer quoted "the glamour", a phrase that is not in the play.'],
  [4, /Which childlike phrase of Mickey's admiration for Eddie later curdles into resentment/,
    'Which line of Mickey’s admiration for Eddie later curdles into resentment?',
    '“If I was like him I’d know all the right words.”',
    'MEDIUM', 'answer quoted "You\'re brilliant", which is not a line from the play.'],
  [5, /Who fires the gun that kills both twins in the final scene/,
    'Who kills whom in the final scene?',
    'Mickey shoots Eddie; the police marksmen then shoot Mickey.',
    'HIGH', 'answer said the killer of BOTH twins was "ambiguous — Mickey\'s finger or police marksmen\'s fire". There are two guns and two shooters: Mickey kills Eddie, the police kill Mickey.'],
  [5, /Why does Russell deliberately leave the gun's trigger ambiguous/,
    'Where does Russell leave the real ambiguity in the ending?',
    'In who is to blame — the class system, not an individual — rather than in who fired.',
    'HIGH', 'the premise of the question was false: the trigger is not left ambiguous.'],
  [6, /What is Linda's defining childhood quality before adulthood grinds her down/, null,
    'Bold fearlessness — the only one of the three to hit the target.',
    'LOW', 'answer said "she outshoots the boys", overstating a single scene.'],
];

function fixFlashcards(num, fcs) {
  if (!Array.isArray(fcs)) return { out: fcs, notes: [] };
  const notes = [];
  const out = fcs.map((fc, i) => {
    const e = { ...fc };
    for (const [ln, re, newQ, newA, sev, note] of FC_EDITS) {
      if (ln !== num || !re.test(e.q || '')) continue;
      const b = { q: e.q, a: e.a };
      if (newQ) e.q = newQ;
      e.a = newA;
      notes.push({ severity: sev, where: `flashcard_questions[${i}]`, note,
        before: JSON.stringify(b), after: JSON.stringify({ q: e.q, a: e.a }) });
    }
    if (num === 7 && /Which AO is NOT assessed in the AQA Modern Texts essay/.test(e.q || '')) {
      const b = { q: e.q, a: e.a };
      e.q = 'Which assessment objectives does the AQA Modern Texts essay assess?';
      e.a = 'AO1 (12), AO2 (12), AO3 (6) and AO4 (4 for SPaG) — no extract, but methods still count.';
      notes.push({ severity: 'HIGH', where: `flashcard_questions[${i}]`,
        note: 'the card asserted "AO2 — there is no extract, so no language analysis marks". False: AO2 is assessed on AQA Paper 2 Section A. Card rewritten.',
        before: JSON.stringify(b), after: JSON.stringify({ q: e.q, a: e.a }) });
    }
    return e;
  });
  return { out, notes };
}

// --------------------------------------------------------------------- driver
(async () => {
  L(`\n=== RETRO FACT-CHECK: english-literature-aqa / blood-brothers ===`);
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
      L(`     looking for: ${oldS.slice(0, 120)}`);
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
    const k = fixKnowledgeChecks(num, row.knowledge_checks);
    const f = fixFlashcards(num, row.flashcard_questions);
    if (JSON.stringify(p.out) !== JSON.stringify(row.practice_questions)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).practice_questions = p.out;
    }
    if (JSON.stringify(k.out) !== JSON.stringify(row.knowledge_checks)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).knowledge_checks = k.out;
    }
    if (JSON.stringify(f.out) !== JSON.stringify(row.flashcard_questions)) {
      if (!patches.has(num)) patches.set(num, {}); patches.get(num).flashcard_questions = f.out;
    }
    [...p.notes, ...k.notes, ...f.notes].forEach((o) => addNote(num, o));
  }

  // 3. INCREMENTAL backup + patch, lesson by lesson
  const backup = {
    generated_at: new Date().toISOString(), unit_id: UNIT,
    subject: 'english-literature-aqa', unit: 'blood-brothers', lessons: [],
  };
  let report = {};
  try { report = JSON.parse(fs.readFileSync(REPORT, 'utf8')); } catch (_) { report = {}; }
  report.generated_at = new Date().toISOString();
  report.subject = 'english-literature-aqa';
  report.unit = 'blood-brothers';
  report.lessons_total = rows.length;
  report.lessons = [];
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
