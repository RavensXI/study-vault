/**
 * VERIFY the adjudicated rulings — english-literature-aqa / blood-brothers.
 * Re-fetches from Supabase and re-derives every rule independently of the fix
 * log: it does not read _adjudication_report.json to decide pass/fail (only to
 * find which clips to probe on R2).
 */
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs = require('fs'), path = require('path'), https = require('https');
const D = __dirname;
const UNIT = '36556966-f4ec-436b-9ce8-736476fab761';
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

const DUET_DEF = 'A song for two voices, in which each singer’s feelings are heard against the other’s. Mickey and Edward sing “That Guy” as a duet.';
const AGENCY_DEF = 'The capacity of a character to act freely and to choose for themselves. Russell asks how much agency Mickey has left once poverty, unemployment and prison have taken his choices away.';

function ranged(url) {
  return new Promise((res) => {
    const req = https.request(url, { headers: { 'User-Agent': 'Mozilla/5.0', Range: 'bytes=0-3' } }, (r) => {
      const chunks = [];
      r.on('data', (c) => chunks.push(c));
      r.on('end', () => res({ status: r.statusCode, lm: r.headers['last-modified'], magic: Buffer.concat(chunks) }));
    });
    req.on('error', (e) => res({ status: 'ERR ' + e.message }));
    req.end();
  });
}

(async () => {
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,status,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest&order=lesson_number`);
  const by = new Map(rows.map((r) => [r.lesson_number, r]));
  const blob = (r) => (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '') + (r.description || '') +
    JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
  let fail = 0;
  const ok = (cond, msg) => { console.log(`${cond ? 'ok  ' : 'FAIL'} ${msg}`); if (!cond) fail++; };

  console.log('--- RULING 1: "That Guy" is a sung duet, not a soliloquy ---');
  const soli = rows.filter((r) => /soliloqu/i.test(blob(r))).map((r) => `L${r.lesson_number}`);
  ok(soli.length === 0, `"soliloquy" gone from the whole unit (found in: ${soli.join(',') || 'none'})`);
  const l6 = by.get(6);
  ok(/<dfn class="term" data-def="[^"]*">duet<\/dfn> with Edward, “That Guy”/.test(l6.content_html), 'L6 prose highlights "duet" with Edward, "That Guy"');
  ok((l6.glossary_terms || []).some((g) => g.term === 'duet' && g.definition === DUET_DEF), 'L6 glossary carries the "duet" entry');
  ok(l6.content_html.includes(`data-def="${DUET_DEF}"`), 'L6 dfn data-def is IDENTICAL to the glossary definition');
  ok((l6.flashcard_questions || []).some((f) => /duet with Edward/.test(f.q) && /Class-bred insecurity/.test(f.a)), 'L6 flashcard relabelled, answer untouched');
  ok(/Mickey's song about 'that guy'/.test(JSON.stringify(l6.knowledge_checks)), 'L6 KC1 (already correct: "song") still intact');

  console.log('--- RULING 2: "agency" restored to its real meaning ---');
  const l5 = by.get(5);
  const ag = (l5.glossary_terms || []).find((g) => g.term === 'agency');
  ok(!!ag && ag.definition === AGENCY_DEF, 'L5 glossary "agency" = capacity to act and choose');
  ok(l5.content_html.includes(`data-def="${AGENCY_DEF}"`), 'L5 inline dfn carries the same definition');
  ok(!/forces or factors that ultimately bring about the tragic outcome/.test(blob(l5)), 'the bent definition is gone from every field');

  console.log('--- RULING 3: invented term "convenient narrative" retired ---');
  ok(!(l5.glossary_terms || []).some((g) => g.term === 'convenient narrative'), 'L5 glossary entry removed');
  ok(!/data-def="[^"]*">convenient narrative<\/dfn>/.test(l5.content_html), 'no dfn wraps the phrase any more');
  ok(l5.content_html.includes('it is a convenient narrative that distracts'), 'the phrase survives as the lesson’s own plain words');
  ok(!/A simplified, often misleading explanation/.test(blob(l5)), 'the invented definition is gone from every field');

  console.log('--- RULINGS 4 + 5: flashcard grammar ---');
  const l2 = by.get(2);
  ok((l2.flashcard_questions || []).some((f) => f.q === 'Where do Russell’s sympathies lie between the two mothers?' && /Clearly with Mrs Johnstone/.test(f.a)), 'L2 stem reworded, answer untouched');
  ok(!/sympathy between the two mothers land/.test(JSON.stringify(l2.flashcard_questions)), 'L2 ungrammatical stem gone');
  ok((l5.flashcard_questions || []).some((f) => f.a === 'The myth of meritocracy — that poverty is caused by laziness, not by the system.'), 'L5 answer now grammatical');
  ok(!/laziness, not system/.test(JSON.stringify(l5.flashcard_questions)), 'L5 ungrammatical answer gone');

  console.log('--- KEPT flags must be UNTOUCHED ---');
  ok(/I could have been him/.test(blob(by.get(4))), 'L4 keeps the "I could have been him" fragment');
  ok(/thesis in five words/.test(by.get(4).content_html), 'L4 keeps the "five words" framing');
  ok(/first performed in 1983/.test(by.get(1).content_html), 'L1 keeps the verified 1983 premiere claim');

  console.log('--- glossary <-> dfn 1:1 mirror (the unit’s own convention) ---');
  for (const r of rows) {
    const dfns = [...(r.content_html || '').matchAll(/<dfn[^>]*>([^<]+)<\/dfn>/g)].map((m) => m[1]);
    const terms = (r.glossary_terms || []).map((g) => g.term);
    const missing = dfns.filter((d) => !terms.includes(d));
    const extra = terms.filter((t) => !dfns.includes(t));
    ok(missing.length === 0 && extra.length === 0,
      `L${r.lesson_number} dfn=${dfns.length} glossary=${terms.length}` +
      (missing.length ? ` missing:${missing}` : '') + (extra.length ? ` extra:${extra}` : ''));
  }

  console.log('--- narration manifest integrity ---');
  for (const r of rows) {
    const html = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map((m) => m[1]);
    const man = new Set((r.narration_manifest || []).map((e) => e.id));
    const missing = ids.filter((i) => !man.has(i));
    const orphan = [...man].filter((i) => !ids.includes(i));
    const bad = (r.narration_manifest || []).filter((e) => !e.src || !/^https:\/\/pub-.*\.mp3$/.test(e.src));
    ok(!missing.length && !orphan.length && !bad.length,
      `L${String(r.lesson_number).padStart(2, '0')} ids=${ids.length} manifest=${man.size} missing=${missing.length} orphan=${orphan.length} badsrc=${bad.length}`);
  }

  console.log('--- entity sweep on the fields we rewrote ---');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  for (const r of rows) {
    const j = JSON.stringify([r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
    const e = j.match(ENT);
    if (e) { console.log(`FAIL entity L${r.lesson_number}`, [...new Set(e)]); fail++; }
  }
  console.log('  (no FAIL above = ok)');

  console.log('--- regenerated audio: live ranged GET + freshness ---');
  const rep = JSON.parse(fs.readFileSync(path.join(D, '_adjudication_report.json'), 'utf8'));
  const clips = (rep.renarration || {}).clips || [];
  ok(clips.length > 0, `report lists ${clips.length} regenerated clip(s)`);
  for (const c of clips) {
    const manEntry = (by.get(c.lesson).narration_manifest || []).find((e) => e.id === c.id);
    ok(!!manEntry && manEntry.src === c.url, `L${c.lesson} ${c.id} manifest src matches the uploaded object`);
    const r = await ranged(c.url);
    const fresh = r.lm && (Date.now() - new Date(r.lm).getTime()) < 6 * 3600 * 1000;
    const sync = r.magic && [0xff].includes(r.magic[0]);
    ok((r.status === 200 || r.status === 206) && fresh && sync,
      `L${c.lesson} ${c.id} -> ${r.status}, Last-Modified ${r.lm}, mp3-sync=${sync}`);
  }

  console.log(`\n=== ADJUDICATION VERIFY ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  const bk = JSON.parse(fs.readFileSync(path.join(D, '_adjudication_backup.json'), 'utf8'));
  console.log(`backup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(D, '_adjudication_backup.json')).size} bytes`);
  process.exit(fail === 0 ? 0 : 1);
})();
