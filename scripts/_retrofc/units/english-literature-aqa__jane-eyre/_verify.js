/** Post-fix verification — english-literature-aqa / jane-eyre. Re-derives from live Supabase + Gutenberg #1260. */
const fs = require('fs'), path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const D = __dirname;
const UNIT = '32f5bcc7-e79e-436a-9158-322c43e4941b';
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }

// ---- independent re-derivation from the novel ----
const RAW = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/scripts/_retrofc/_texts/jane_eyre_gutenberg.txt', 'utf8');
const lines = RAW.split(/\r?\n/); const ch = [];
lines.forEach((l, i) => { const m = l.trim().match(/^CHAPTER ([IVXL]+)\b/); if (m) ch.push({ r: m[1], line: i }); });
const rom = (r) => { const v = { I: 1, V: 5, X: 10, L: 50 }; let t = 0; for (let i = 0; i < r.length; i++) { const a = v[r[i]], b = v[r[i + 1]]; t += (b && a < b) ? -a : a; } return t; };
ch.forEach(c => c.n = rom(c.r));
const nrm = s => s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/[\u2014\u2013]/g, '-').replace(/\s+/g, ' ').toLowerCase();
const CH = ch.map((c, i) => ({ n: c.n, t: nrm(lines.slice(c.line, i + 1 < ch.length ? ch[i + 1].line : lines.length).join(' ')) }));
const chapterOf = (s) => CH.filter(b => b.t.includes(nrm(s))).map(b => b.n);

let fail = 0;
const chk = (cond, label) => { console.log(`${cond ? 'ok  ' : 'FAIL'} ${label}`); if (!cond) fail++; };

(async () => {
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status&order=lesson_number`);
  const by = new Map(rows.map(r => [r.lesson_number, r]));
  const txt = (n) => (by.get(n).content_html || '') + (by.get(n).exam_tip_html || '') + (by.get(n).conclusion_html || '') + JSON.stringify([by.get(n).practice_questions, by.get(n).knowledge_checks, by.get(n).flashcard_questions, by.get(n).glossary_terms]);

  console.log('=== A. source-of-truth re-derivation (Gutenberg #1260) ===');
  chk(JSON.stringify(chapterOf('you are like a murderer')) === '[1]', '"you are like a murderer" is Chapter 1 (not 4)');
  chk(CH.find(c => c.n === 1).t.includes(nrm('"wicked and cruel boy!" i said. "you are like a murderer')), 'Ch 1: addressed to John Reed right after he throws the book');
  chk(CH.find(c => c.n === 1).t.includes(nrm('you are a dependent, mama says')), 'Ch 1 spells it "dependent"');
  chk(CH.find(c => c.n === 9).t.includes(nrm('her complaint was consumption, not typhus')), 'Ch 9: Helen dies of consumption, NOT typhus');
  chk(CH.find(c => c.n === 9).t.includes(nrm('breathed typhus through its crowded schoolroom')), 'Ch 9: the epidemic IS typhus');
  chk(CH.find(c => c.n === 14).t.includes(nrm('a curious sort of bird through the close-set bars of a cage')), 'Ch 14 caged-bird line exists (pre-dates Ch 23)');
  chk(CH.find(c => c.n === 23).t.includes(nrm("struggle so, like a wild frantic bird that is rending its own plumage")), 'Ch 23 "wild frantic bird" precedes "I am no bird"');
  chk(CH.find(c => c.n === 37).t.includes(nrm('my skylark')), 'Ch 37 has "my skylark" (not "lark")');
  chk(CH.find(c => c.n === 24).t.includes(nrm('i am your plain, quakerish governess')), 'Ch 24 "plain, Quakerish governess"');
  chk(CH.find(c => c.n === 26).t.includes(nrm('antoinetta his wife, a creole')), 'Ch 26 register: Bertha\'s mother named "a Creole" in a planter family');

  console.log('\n=== B. corrections landed ===');
  const MUST_GONE = [
    [2, 'When Mrs Reed sends her to the red-room, Jane screams'],
    [2, 'Jane compares her aunt to figures'],
    [2, 'rebellion against Mrs Reed'],
    [2, 'Chapter 4:\n\n\u2018You are like a murderer'],
    [2, 'Mrs Reed to a murderer'],
    [2, 'condemn Mrs Reed'],
    [2, 'A consumption (TB) epidemic kills many Lowood students'],
    [2, 'including Helen Burns?'],
    [2, 'you are a dependant.'],
    [1, 'Which three religious figures show hypocritical Christianity'],
    [4, 'frequently calls Jane his'],
    [4, 'A person of mixed European and Caribbean descent'],
    [4, 'attitudes toward colonised'],
    [7, 'you are a dependant."'],
    [7, '(Jane, Ch. 4)'],
    [7, 'successive clauses build in intensity'],
    [7, "habit of calling Jane his"],
  ];
  for (const [n, s] of MUST_GONE) chk(!txt(n).includes(s), `L${n} removed: "${s.slice(0, 52)}"`);

  const MUST_PRESENT = [
    [2, 'you are a dependent, mama says'],
    [2, 'In Chapter 1, John hurls a book at her'],
    [2, 'Jane compares her cousin to figures'],
    [2, 'rebellion against John Reed'],
    [2, 'Read the following extract from Chapter 1'],
    [2, 'Jane compares John Reed to a murderer'],
    [2, 'condemn John Reed'],
    [2, 'A typhus epidemic kills many Lowood students'],
    [1, 'Which three characters represent contrasting versions of Christianity'],
    [3, 'Chapters 18\u201319'],
    [4, 'the close-set bars of a cage'],
    [4, 'my skylark'],
    [4, 'plain, Quakerish governess'],
    [4, 'born and raised in the West Indies'],
    [4, 'attitudes towards colonised'],
    [7, 'you are a dependent, mama says.'],
    [7, '(Jane to John Reed, Ch. 1)'],
    [7, 'successive clauses begin with the same word or phrase'],
    [7, 'close-set bars of a cage'],
  ];
  for (const [n, s] of MUST_PRESENT) chk(txt(n).includes(s), `L${n} present: "${s.slice(0, 52)}"`);

  console.log('\n=== C. no residual cross-lesson contradiction ===');
  for (const r of rows) {
    const t = txt(r.lesson_number);
    const bad = /(?:Mrs Reed|her aunt)[^.]{0,60}(?:murderer|slave-driver|Roman emperor)/i.test(t) || /(?:murderer|slave-driver|Roman emperor)[^.]{0,60}(?:Mrs Reed|her aunt)/i.test(t);
    chk(!bad, `L${r.lesson_number} no "murderer" line attached to Mrs Reed`);
    // every sentence naming BOTH Helen and typhus must also disown the link
    const sents = t.split(/(?<=[.!?])\s+|\\n/).filter(s => /helen/i.test(s) && /typhus/i.test(s));
    const badTy = sents.filter(s => !/consumption|not typhus|separately/i.test(s));
    chk(badTy.length === 0, `L${r.lesson_number} no "Helen dies of typhus" claim (${sents.length} Helen+typhus sentences, all disown the link)`);
    if (badTy.length) badTy.forEach(s => console.log('      >> ' + s.slice(0, 160)));
    chk(!/Ch(?:apter|\.)?\s*4\b[^.]{0,40}murderer|murderer[^.]{0,60}Ch(?:apter|\.)?\s*4\b/i.test(t), `L${r.lesson_number} no Ch 4 attribution for the murderer line`);
  }

  console.log('\n=== D. exam claims vs AQA 8702 (Paper 1 Sec B = 30 marks, AO1 12 / AO2 12 / AO3 6, NO AO4/SPaG) ===');
  let pq = 0, spag = 0, arith = 0;
  for (const r of rows) for (const [i, p] of (r.practice_questions || []).entries()) {
    pq++;
    if (/spag|spelling,? punctuation|AO4/i.test((p.marks || '') + (p.type || '') + (p.text || ''))) { console.log(`  SPaG L${r.lesson_number}[${i}]`); spag++; }
    const aos = [...(p.marks || '').matchAll(/AO(\d)\s*\((\d+)/g)].map(x => [+x[1], +x[2]]);
    if (JSON.stringify(aos) !== '[[1,12],[2,12],[3,6]]' || !/\[30 marks\]/.test(p.text || '')) { console.log(`  ARITH L${r.lesson_number}[${i}] ${JSON.stringify(aos)}`); arith++; }
  }
  chk(spag === 0, `no SPaG/AO4 claim on any of ${pq} questions`);
  chk(arith === 0, `all ${pq} questions are 30 marks with AO1 12 / AO2 12 / AO3 6`);
  chk(by.get(7).knowledge_checks[0].options[by.get(7).knowledge_checks[0].correct] === '30 marks', 'L7 KC: Section B question worth 30 marks');

  console.log('\n=== E. hygiene ===');
  const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
  const BD = /\b(Edexcel|OCR|Eduqas|WJEC|CCEA)\b/g;
  const US = /\b(?:analyz\w*|symboliz\w*|emphasiz\w*|organiz\w*|recogniz\w*|criticiz\w*|realiz\w*|color(?:s|ed|ing)?|honor(?:s|ed)?|behavior\w*|favor(?:s|ed|ite)?|defense|center(?:s|ed)?|toward(?!s)|traveled|labeled)\b/gi;
  for (const r of rows) {
    const plain = JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms, r.description]);
    const all = plain + (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    chk(!ENT.test(plain), `L${r.lesson_number} no HTML entities in plain-text fields`); ENT.lastIndex = 0;
    chk(!BD.test(all), `L${r.lesson_number} no rival board`); BD.lastIndex = 0;
    chk(!US.test(all), `L${r.lesson_number} British English`); US.lastIndex = 0;
  }

  console.log('\n=== F. narration manifest integrity + freshness of the 7 regenerated clips ===');
  for (const r of rows) {
    const html = (r.content_html || '') + (r.exam_tip_html || '') + (r.conclusion_html || '');
    const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]);
    const man = r.narration_manifest || [], mid = man.map(e => e.id);
    const ok = ids.every(i => mid.includes(i)) && mid.every(i => ids.includes(i)) && man.every(e => /^https:\/\/pub-\S+\.mp3$/.test(e.src));
    chk(ok, `L${r.lesson_number} manifest ${man.length} entries, ids aligned, all src valid`);
  }
  const rep = JSON.parse(fs.readFileSync(path.join(D, '_report.json'), 'utf8'));
  const rn = rep.renarration || {};
  chk(rn.verified_ok === rn.total && rn.total === 7, `re-narration ${rn.verified_ok}/${rn.total} clips verified 206 + fresh Last-Modified`);
  for (const c of rn.clips || []) chk(String(c.verify_status) === '206' && /2026/.test(c.last_modified || ''), `  L${c.lesson} ${c.id} ${c.verify_status} ${c.last_modified}`);

  const bk = JSON.parse(fs.readFileSync(path.join(D, '_backup.json'), 'utf8'));
  console.log(`\nbackup: ${bk.lessons.length} lessons, ${bk.lessons.reduce((a, l) => a + l.fields_changed.length, 0)} fields, ${fs.statSync(path.join(D, '_backup.json')).size} bytes`);
  console.log(`report: ${rep.lessons.length} lessons, fixed=${JSON.stringify(rep.fixed_counts)}`);
  console.log(`\n=== VERIFY ${fail === 0 ? 'PASS' : 'FAIL (' + fail + ')'} ===`);
  process.exit(fail ? 1 : 0);
})();
