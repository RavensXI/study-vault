/** ADJUDICATION verification — english-literature-aqa / jane-eyre.
 *  Re-fetches live Supabase and independently re-derives every claim from
 *  Gutenberg #1260 and specs/aqa/english-literature-8702-8702.md. */
const fs = require('fs'), path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const D = __dirname;
const UNIT = '32f5bcc7-e79e-436a-9158-322c43e4941b';
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

const RAW = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/scripts/_retrofc/_texts/jane_eyre_gutenberg.txt', 'utf8');
const SPEC = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/specs/aqa/english-literature-8702-8702.md', 'utf8');
const lines = RAW.split(/\r?\n/); const ch = [];
lines.forEach((l, i) => { const m = l.trim().match(/^CHAPTER ([IVXL]+)\b/); if (m) ch.push({ r: m[1], line: i }); });
const rom = (r) => { const v = { I: 1, V: 5, X: 10, L: 50 }; let t = 0; for (let i = 0; i < r.length; i++) { const a = v[r[i]], b = v[r[i + 1]]; t += (b && a < b) ? -a : a; } return t; };
ch.forEach(c => c.n = rom(c.r));
const nrm = s => s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/[\u2014\u2013]/g, '-').replace(/\s+/g, ' ').toLowerCase();
const CH = ch.map((c, i) => ({ n: c.n, t: nrm(lines.slice(c.line, i + 1 < ch.length ? ch[i + 1].line : lines.length).join(' ')) }));
const inCh = (n, s) => CH.find(c => c.n === n).t.includes(nrm(s));
const SPECN = nrm(SPEC);

let fail = 0;
const chk = (cond, label) => { console.log(`${cond ? 'ok  ' : 'FAIL'} ${label}`); if (!cond) fail++; };

(async () => {
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status&order=lesson_number`);
  const by = new Map(rows.map(r => [r.lesson_number, r]));
  const txt = (n) => (by.get(n).content_html || '') + (by.get(n).exam_tip_html || '') + (by.get(n).conclusion_html || '') + JSON.stringify([by.get(n).practice_questions, by.get(n).knowledge_checks, by.get(n).flashcard_questions, by.get(n).glossary_terms]);

  console.log('=== A. source-of-truth re-derivation (Gutenberg #1260 + AQA 8702 spec) ===');
  // G3
  chk(SPECN.includes(nrm('written exam: 1 hour 45 minutes')) && SPECN.includes(nrm('64 marks')) && SPECN.includes(nrm('40% of gcse')), 'AQA spec: Paper 1 = 1 h 45 min, 64 marks, 40% of GCSE');
  chk(SPECN.includes(nrm('Section B The 19th-century novel: students will answer one question on their novel of choice. They will be required to write in detail about an extract from the novel and then to write about the novel as a whole.')), 'AQA spec: Section B = extract + whole novel, one question');
  chk(SPECN.includes(nrm('All assessments are closed book: any stimulus materials required will be provided')), 'AQA spec: closed book, stimulus provided (so the extract is printed)');
  chk(!/roughly 400 words/i.test(SPEC), 'AQA spec contains no 400-word figure (the old claim was unsourced)');
  // G4
  chk(inCh(9, 'the nurse held me; she was carrying me through the passage back to the dormitory'), 'Ch 9: Jane is carried back to the dormitory, asleep');
  chk(inCh(9, 'a day or two afterwards'), 'Ch 9: "a day or two afterwards" she learns of it');
  chk(inCh(9, 'my face against Helen Burns\u2019s shoulder, my arms round her neck. I was asleep, and Helen was\u2014dead.'), 'Ch 9: "I was asleep, and Helen was—dead." verbatim');
  // G5
  chk(inCh(37, 'The caged eagle, whose gold-ringed eyes cruelty has extinguished, might look as looked that sightless Samson.'), 'Ch 37: full caged-eagle sentence verbatim (carries the comparator "as")');
  chk(inCh(37, 'some wronged and fettered wild beast or bird'), 'Ch 37: "some wronged and fettered wild beast or bird" verbatim');
  // G6
  chk(inCh(37, 'I began sometimes to pray: very brief prayers they were, but very sincere.'), 'Ch 37: "I began sometimes to pray..." verbatim');
  chk(inCh(37, 'only of late\u2014I began to see and acknowledge the hand of God in my doom'), 'Ch 37: "of late" + "the hand of God in my doom" verbatim');
  chk(!nrm(RAW).includes(nrm('for the first time')) || !inCh(37, 'prayed to God for the first time'), 'Ch 37: Rochester never says he prayed "for the first time"');
  // G7
  chk(inCh(30, 'I established one for boys: I mean now to open a second school for girls'), 'Ch 30: St John establishes the Morton schools');
  chk(inCh(30, 'a cottage of two rooms attached to it for the mistress\u2019s house'), 'Ch 30: Jane is offered the mistress post, not the founding');
  // G8
  chk(inCh(35, 'it did not seem in the room\u2014nor in the house\u2014nor in the garden'), 'Ch 35: the voice is not in the room, house or garden');
  chk(inCh(35, 'all was moorland loneliness and midnight hush'), 'Ch 35: "moorland loneliness and midnight hush" verbatim');
  chk(inCh(35, 'All the house was still') && inCh(35, 'the room was full of moonlight'), 'Ch 35: Jane is INDOORS at Moor House when the voice comes');

  console.log('\n=== B. adjudicated errors removed ===');
  const MUST_GONE = [
    [7, 'In most boards'],
    [7, 'roughly 400 words'],
    [7, "Check your exam board's specimen paper"],
    [2, 'wakes to find she has died'],
    [6, 'Jane describes him as a \u201Ccaged eagle, whose gold-ringed eyes cruelty has extinguished.\u201D'],
    [6, "A 'caged eagle, whose gold-ringed eyes cruelty has extinguished.'"],
    [6, 'Jane compares Rochester to a \u2018caged eagle\u2019 to show his diminished power.'],
    [6, 'he prayed to God for the first time'],
    [6, 'for the first time during his suffering'],
    [6, 'He prayed to God \u2014 a genuine spiritual transformation.'],
    [5, 'she opens a village school for poor girls'],
    [5, 'meaningful work (the village school)'],
    [5, 'meaningful work (a village school)'],
    [5, 'across the moors'],
  ];
  for (const [n, s] of MUST_GONE) chk(!txt(n).includes(s), `L${n} removed: "${s.slice(0, 56)}"`);
  for (const r of rows) chk(!txt(r.lesson_number).includes('across the moors'), `L${r.lesson_number} unit-wide: no "across the moors"`);

  console.log('\n=== C. adjudicated corrections present ===');
  const MUST_PRESENT = [
    [7, 'AQA Paper 1 is 1 hour 45 minutes long and worth 64 marks'],
    [7, 'Section B is the 19th-century novel'],
    [7, 'worth 30 marks'],
    [7, 'closed book, so AQA prints an extract'],
    [7, 'AQA sets no word count'],
    [2, 'falls asleep beside her'],
    [2, 'a day or two afterwards'],
    [2, 'I was asleep, and Helen was\u2014dead.'],
    [6, 'The caged eagle, whose gold-ringed eyes cruelty has extinguished, might look as looked that sightless Samson.'],
    [6, 'some wronged and fettered wild beast or bird'],
    [6, 'might look as looked that sightless Samson\u2019 \u2014 Jane\u2019s image for the blinded Rochester'],
    [6, 'I began sometimes to pray: very brief prayers they were, but very sincere.'],
    [6, 'the hand of God in my doom'],
    [6, "What does Rochester say he began to do 'of late'"],
    [5, 'St John Rivers has established at Morton'],
    [5, 'mistress of the Morton girls\u2019 school St John set up'],
    [5, 'mistress of the village school St John founded at Morton'],
    [5, 'She is indoors at Moor House'],
    [5, 'it did not seem in the room\u2014nor in the house\u2014nor in the garden'],
    [5, 'moorland loneliness and midnight hush'],
    [5, 'Indoors at Moor House, Jane hears Rochester\u2019s voice cry her name'],
    [5, 'Indoors at Moor House, Jane hears Rochester\u2019s voice cry \u2018_____'],
    [5, "Indoors at Moor House she hears Rochester's voice cry 'Jane! Jane! Jane!'"],
  ];
  for (const [n, s] of MUST_PRESENT) chk(txt(n).includes(s), `L${n} present: "${s.slice(0, 56)}"`);

  console.log('\n=== D. no new contradiction introduced ===');
  chk(by.get(5).knowledge_checks[3].options[by.get(5).knowledge_checks[3].correct] === 'Jane', 'L5 KC[3] answer key still "Jane" after the stem rewrite');
  chk(/simile/.test(by.get(6).content_html) && /might look as looked/.test(by.get(6).content_html), 'L6 the word "simile" now sits beside a quotation containing "as"');
  chk(!/(?:Jane|she)[^.]{0,40}(?:opens|founded|founds|established)[^.]{0,30}(?:village |Morton )?school/i.test(txt(5)), 'L5 no claim that Jane founds the school');
  chk(!/prayed[^.]{0,30}first time|first time[^.]{0,30}pray/i.test(txt(6)), 'L6 no "first prayer" claim left');
  for (const r of rows) {
    const t = txt(r.lesson_number);
    chk(!/In most boards|other exam boards|whichever board/i.test(t), `L${r.lesson_number} no board-agnostic hedge`);
    chk(!/\b(Edexcel|OCR|Eduqas|WJEC|CCEA)\b/.test(t), `L${r.lesson_number} no rival board named`);
  }

  console.log('\n=== E. hygiene (entities / British English) ===');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  const US = /\b(?:analyz\w*|symboliz\w*|emphasiz\w*|organiz\w*|recogniz\w*|criticiz\w*|realiz\w*|color(?:s|ed|ing)?|honor(?:s|ed)?|behavior\w*|favor(?:s|ed|ite)?|defense|center(?:s|ed)?|toward(?!s)|traveled|labeled)\b/gi;
  for (const r of rows) {
    const plain = JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms, r.description]);
    const all = plain + (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    chk(!ENT.test(plain), `L${r.lesson_number} ZERO HTML entities in plain-text fields`); ENT.lastIndex = 0;
    chk(!US.test(all), `L${r.lesson_number} British English`); US.lastIndex = 0;
  }

  console.log('\n=== F. narration integrity + freshness of the 8 adjudication clips ===');
  for (const r of rows) {
    const html = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]);
    const man = r.narration_manifest || [], mid = man.map(e => e.id);
    const ok = ids.every(i => mid.includes(i)) && mid.every(i => ids.includes(i)) && man.every(e => /^https:\/\/pub-\S+\.mp3$/.test(e.src));
    chk(ok, `L${r.lesson_number} manifest ${man.length} entries, ids aligned, all src valid`);
  }
  // ids preserved exactly as they were before the adjudication
  const bk = JSON.parse(fs.readFileSync(path.join(D, '_adjudication_backup.json'), 'utf8'));
  for (const l of bk.lessons) {
    const oldIds = ['content_html', 'exam_tip_html', 'conclusion_html'].map(f => [...String(l.before[f] || '').matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]).join(',')).join('|');
    const row = by.get(l.lesson_number);
    const newIds = ['content_html', 'exam_tip_html', 'conclusion_html'].map(f => (f in l.before ? [...String(row[f] || '').matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]).join(',') : [...String(l.before[f] || '').matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]).join(','))).join('|');
    chk(oldIds === newIds, `L${l.lesson_number} narration ids preserved exactly`);
  }
  const rep = JSON.parse(fs.readFileSync(path.join(D, '_report.json'), 'utf8'));
  const rn = (rep.adjudication || {}).renarration || {};
  chk(rn.verified_ok === rn.total && rn.total === 8, `re-narration ${rn.verified_ok}/${rn.total} clips verified 206 + fresh Last-Modified`);
  for (const c of rn.clips || []) chk(String(c.verify_status) === '206' && /30 Aug 2026/.test(c.last_modified || ''), `  L${c.lesson} ${c.id} ${c.verify_status} ${c.last_modified}`);
  // every regenerated clip's URL is the one the manifest now points at
  for (const c of rn.clips || []) {
    const e = (by.get(c.lesson).narration_manifest || []).find(x => x.id === c.id);
    chk(!!e && e.src === c.url && Math.abs(e.duration - c.duration) < 0.01, `  L${c.lesson} ${c.id} manifest src+duration match the new upload`);
  }

  console.log(`\nbackup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(D, '_adjudication_backup.json')).size} bytes`);
  console.log(`\n=== ADJUDICATION VERIFY ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  process.exit(fail ? 1 : 0);
})();
