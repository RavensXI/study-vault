/**
 * Independent re-derivation that the four adjudicated rulings landed:
 * re-FETCHES the unit from Supabase and asserts old strings gone / new present.
 * Does not trust the patch script's own return=representation.
 */
const fs = require('fs');
const path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const UNIT = '10151ade-c16f-4736-9626-8166ef02a30b';
const BACKUP = path.join(__dirname, '_adjudication_backup.json');

let pass = 0, fail = 0;
const ok = (m) => { pass++; console.log(`  PASS  ${m}`); };
const no = (m) => { fail++; console.log(`  FAIL  ${m}`); };
const assert = (c, m) => (c ? ok(m) : no(m));

(async () => {
  const cols = 'id,lesson_number,title,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status';
  const r = await fetch(`${SB}/rest/v1/lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`, {
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
  if (!r.ok) throw new Error(r.status + await r.text());
  const rows = await r.json();
  const by = new Map(rows.map((x) => [x.lesson_number, x]));
  const backup = JSON.parse(fs.readFileSync(BACKUP, 'utf8'));

  const whole = (n) => JSON.stringify(by.get(n));
  const unitJson = JSON.stringify(rows);

  console.log('\n--- F1: the "apophasis" label is gone from every touchpoint ---');
  assert(!/apophasis/i.test(unitJson), 'no "apophasis" anywhere in the unit (all 8 lessons, all fields)');
  const L8 = by.get(8);
  assert(L8.content_html.includes('This technique — describing something by insisting it <em>cannot</em> be described — leaves the horror to the reader’s imagination.'),
    'L8 content_html: device described without the false label');
  assert(!/<dfn[^>]*>apophasis<\/dfn>/i.test(L8.content_html), 'L8 content_html: <dfn> wrapper removed');
  assert(L8.glossary_terms.length === 6 && !L8.glossary_terms.some((g) => /apophasis/i.test(g.term)),
    `L8 glossary_terms: apophasis entry deleted (7 -> ${L8.glossary_terms.length})`);
  const kc = L8.knowledge_checks[1];
  assert(kc.q === 'Why does Stevenson keep Hyde’s appearance vague?', 'L8 knowledge_checks[1]: stem recast');
  assert(kc.correct === 1 && kc.options[kc.correct] === 'It forces the reader to imagine the horror',
    'L8 knowledge_checks[1]: correct index points at the right option');
  assert(kc.options.length === 4 && !kc.options.some((o) => /apophasis|metaphor|hyperbole|simile/i.test(o)),
    'L8 knowledge_checks[1]: all four distractors replaced, no device labels left');
  assert(kc.type === 'mcq' && 'correct' in kc && 'options' in kc && !('answers' in kc),
    'L8 knowledge_checks[1]: canonical shape (correct + options, no answers[])');
  assert(L8.practice_questions[0].marks.includes('animalistic imagery, pathetic fallacy, the refusal to describe Hyde directly.'),
    'L8 practice_questions[0].marks: top band descriptor fixed');
  assert(L8.flashcard_questions[2].q === 'Why does Stevenson refuse to describe Hyde clearly?',
    'L8 flashcard_questions[2]: recast');
  assert(!/apophasis/i.test(L8.exam_tip_html), 'L8 exam_tip_html: clean (already listed only correct terminology)');

  console.log('\n--- F2: Utterson is the focaliser, not a "reliable narrator" ---');
  const bare = (s) => (s.match(/(^|[^n])reliable narrator/gi) || []).filter((m) => !/unreliable/i.test(m));
  assert(bare(whole(8)).length === 0, 'L8: no bare "reliable narrator" left in any field');
  assert(L8.content_html.includes('Utterson is the <dfn class="term" data-def="The character through whose eyes the reader experiences the story.">focaliser</dfn> of Chapters 1–8, not a narrator'),
    'L8 content_html n16: focaliser framing, dfn definition identical to L6');
  const l6def = (by.get(6).content_html.match(/data-def="([^"]*)">focaliser</) || [])[1];
  const l8def = (L8.content_html.match(/data-def="([^"]*)">focaliser</) || [])[1];
  assert(l6def && l6def === l8def, `L6 and L8 use the SAME focaliser definition ("${l8def}")`);
  assert(L8.glossary_terms.some((g) => g.term === 'focaliser' && g.definition === l6def),
    'L8 glossary_terms: focaliser entry replaces "reliable narrator" in place');
  assert(L8.glossary_terms.some((g) => g.term === 'unreliable narrator'),
    'L8 glossary_terms: "unreliable narrator" KEPT for Jekyll');
  assert(/unreliable narrator/i.test(L8.content_html) && /unreliable narrator/i.test(L8.conclusion_html) && /unreliable narrator/i.test(L8.exam_tip_html),
    'L8: the Jekyll unreliable-narrator contrast is intact (content, conclusion, exam tip)');
  assert(L8.flashcard_questions[8].q === 'Utterson is the focaliser of Chapters 1–8 — what does that mean?',
    'L8 flashcard_questions[8]: recast to focaliser');

  console.log('\n--- F3: "ape-like fury" is animalistic imagery, not a simile ---');
  const fc3 = by.get(3).flashcard_questions[2];
  assert(!/simile/i.test(fc3.q), 'L3 flashcard_questions[2]: "simile" label gone');
  assert(fc3.q === "What animalistic imagery describes Hyde's violence in the Carew attack?",
    'L3 flashcard_questions[2]: relabelled "animalistic imagery"');
  assert(fc3.a === "'Ape-like fury' — suggesting evolutionary degeneration.",
    'L3 flashcard_questions[2]: analysis point kept EXACTLY intact');
  const juggernaut = by.get(2).flashcard_questions.find((c) => /Juggernaut/.test(c.a));
  assert(juggernaut && /simile/i.test(juggernaut.q),
    'L2 "like some damned Juggernaut" still called a simile (a real simile — correctly untouched)');

  console.log('\n--- F4: Enfield is a "distant kinsman", not a cousin ---');
  assert(!/cousin/i.test(unitJson), 'no "cousin" anywhere in the unit');
  assert(by.get(2).content_html.includes('his distant kinsman Richard Enfield'), 'L2 content_html n2 corrected');
  assert(by.get(2).flashcard_questions[0].a === 'Mr Utterson and his distant kinsman Richard Enfield.', 'L2 flashcard_questions[0] corrected');
  assert(by.get(6).content_html.includes('Enfield is Utterson’s distant kinsman and walking companion.'), 'L6 content_html n14 corrected');
  assert(by.get(6).flashcard_questions[9].a === "His distant kinsman — Stevenson's phrase — and regular Sunday walking companion.", 'L6 flashcard_questions[9] corrected');
  assert((unitJson.match(/distant kinsman/g) || []).length === 4, 'exactly 4 "distant kinsman" occurrences — every former "cousin" replaced');

  console.log('\n--- integrity: narration ids, manifest shape, entity conventions ---');
  const RENARRATED = { 2: ['n2'], 6: ['n14'], 8: ['n4', 'n16'] };
  for (const b of backup.lessons) {
    const live = by.get(b.lesson_number);
    const oldM = b.before.narration_manifest || [];
    const newM = live.narration_manifest || [];
    const oldIds = oldM.map((e) => e.id).join(',');
    const newIds = newM.map((e) => e.id).join(',');
    assert(oldIds === newIds, `L${b.lesson_number}: narration ids preserved (${newM.length} entries, same order)`);
    const changed = newM.filter((e, i) => JSON.stringify(e) !== JSON.stringify(oldM[i])).map((e) => e.id);
    const expect = RENARRATED[b.lesson_number] || [];
    assert(JSON.stringify(changed.sort()) === JSON.stringify([...expect].sort()),
      `L${b.lesson_number}: only ${expect.length ? expect.join(', ') : 'no clip'} changed in the manifest (got ${changed.join(', ') || 'none'})`);
    // every content narration id still has a manifest clip
    const inHtml = [...((live.content_html || '') + (live.exam_tip_html || '') + (live.conclusion_html || ''))
      .matchAll(/data-narration-id="([^"]+)"/g)].map((m) => m[1]);
    const missing = inHtml.filter((id) => !newM.some((e) => e.id === id));
    assert(missing.length === 0, `L${b.lesson_number}: every data-narration-id has a clip (${inHtml.length} ids, ${missing.length} orphaned)`);
  }
  // plain-text fields must carry unicode, not HTML entities (validator rule)
  for (const row of rows) {
    for (const f of ['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']) {
      const s = JSON.stringify(row[f] || null);
      if (/&(rsquo|lsquo|amp|quot|ldquo|rdquo|nbsp|mdash|#\d+);/.test(s)) no(`L${row.lesson_number}.${f}: HTML entity in a plain-text field`);
    }
  }
  ok('no HTML entities in any plain-text field across the unit');
  assert(!/\b(analyze|emphasize|symbolize|recognize|behavior|color)\b/i.test(unitJson), 'no US spellings introduced');
  assert(rows.every((x) => x.status === 'live'), 'all 8 lessons still live');

  console.log(`\n=== ${pass} passed, ${fail} failed ===`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
