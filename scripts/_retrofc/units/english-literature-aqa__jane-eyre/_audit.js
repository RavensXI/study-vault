const fs = require('fs'), path = require('path');
const D = __dirname;
const { lessons } = JSON.parse(fs.readFileSync(path.join(D, '_raw.json'), 'utf8'));

const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
const BOARD = /\b(Edexcel|OCR|Eduqas|WJEC|CCEA)\b/g;
const USBAD = /\b(?:analyze[sd]?|analyzing|symboliz\w*|emphasiz\w*|organiz\w*|recogniz\w*|criticiz\w*|realiz\w*|dramatiz\w*|characteriz\w*|apologiz\w*|color(?:s|ed|ing)?|honor(?:s|ed|ing)?|behavior\w*|favor(?:s|ed|ing|ite)?|defense|offense|center(?:s|ed|ing)?|traveled|labeled|marvelous|practiced\b)\b/gi;

console.log('=== SPaG / AO / marks arithmetic on every practice question ===');
let pqTotal = 0, spag = 0, arith = 0;
for (const L of lessons) {
  for (const [i, pq] of (L.practice_questions || []).entries()) {
    pqTotal++;
    const m = pq.marks || '', t = pq.type || '', txt = pq.text || '';
    if (/spag|spelling,? punctuation|AO4|accurate spelling/i.test(m + t + txt)) { console.log(`  SPaG/AO4 L${L.lesson_number} pq[${i}]`); spag++; }
    const aos = [...m.matchAll(/AO(\d)\s*\((\d+)(?:\s*marks?)?\)/g)].map(x => [+x[1], +x[2]]);
    const sum = aos.reduce((a, b) => a + b[1], 0);
    const declared = +((t.match(/(\d+)\s*marks/) || [])[1] || (txt.match(/\[(\d+)\s*marks\]/) || [])[1] || 0);
    const ok = aos.length === 3 && sum === declared && declared === 30 &&
      aos[0][0] === 1 && aos[0][1] === 12 && aos[1][0] === 2 && aos[1][1] === 12 && aos[2][0] === 3 && aos[2][1] === 6;
    if (!ok) { console.log(`  ARITH L${L.lesson_number} pq[${i}] declared=${declared} aos=${JSON.stringify(aos)} sum=${sum}`); arith++; }
    if (!/\[30 marks\]/.test(txt)) console.log(`  NOTE L${L.lesson_number} pq[${i}] text has no [30 marks] tag`);
  }
}
console.log(`  questions=${pqTotal} spagClaims=${spag} arithProblems=${arith}`);

console.log('\n=== extract-format check (AQA Section B is extract-based) ===');
for (const L of lessons) for (const [i, pq] of (L.practice_questions || []).entries()) {
  const txt = pq.text || '';
  const hasExtract = /Read the following extract/i.test(txt);
  const startingWith = /Starting with/i.test(txt);
  if (!hasExtract && !startingWith) console.log(`  NO-EXTRACT/NO-ANCHOR L${L.lesson_number} pq[${i}]: ${txt.slice(0, 78).replace(/\n/g, ' ')}`);
}

console.log('\n=== entities in plain-text fields / rival board / US spelling ===');
for (const L of lessons) {
  const plain = JSON.stringify([L.practice_questions, L.knowledge_checks, L.flashcard_questions, L.glossary_terms, L.description]);
  const all = plain + (L.content_html || '') + (L.exam_tip_html || '') + (L.conclusion_html || '') + L.title;
  const e = plain.match(ENT), b = all.match(BOARD), u = all.match(USBAD);
  if (e) console.log(`  ENTITY L${L.lesson_number}`, [...new Set(e)]);
  if (b) console.log(`  BOARD  L${L.lesson_number}`, [...new Set(b)]);
  if (u) console.log(`  US-SP  L${L.lesson_number}`, [...new Set(u.map(x => x.toLowerCase()))]);
}
console.log('  (blank above = clean)');

console.log('\n=== knowledge_checks canonical shape ===');
for (const L of lessons) for (const [i, kc] of (L.knowledge_checks || []).entries()) {
  const p = [];
  if (kc.answers) p.push('has answers[] (non-canonical)');
  if (kc.type === 'mcq' || kc.type === 'fill') {
    if (!Array.isArray(kc.options)) p.push('no options[]');
    else if (typeof kc.correct !== 'number' || kc.correct < 0 || kc.correct >= kc.options.length) p.push('bad correct idx');
  } else if (kc.type === 'match') {
    if (!Array.isArray(kc.left) || !Array.isArray(kc.right)) p.push('match missing left/right');
    else if (kc.left.length !== kc.right.length) p.push('match len mismatch');
    if (!Array.isArray(kc.order) || kc.order.length !== (kc.left || []).length) p.push('bad order');
  } else p.push('unknown type ' + kc.type);
  if (p.length) console.log(`  KC L${L.lesson_number}[${i}] ${p.join('; ')}`);
}
console.log('  (blank above = clean)');

console.log('\n=== narration manifest integrity ===');
for (const L of lessons) {
  const html = (L.content_html || '') + (L.exam_tip_html || '') + (L.conclusion_html || '');
  const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]);
  const man = L.narration_manifest || [];
  const manIds = man.map(e => e.id);
  const missing = ids.filter(i => !manIds.includes(i));
  const orphan = manIds.filter(i => !ids.includes(i));
  const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
  const bad = man.filter(e => !e.src || !/^https?:\/\/\S+\.mp3$/.test(e.src));
  const prefixes = [...new Set(man.map(e => (e.src || '').replace(/^https?:\/\/[^/]+\//, '').split('/')[0]))];
  const ok = !missing.length && !orphan.length && !bad.length && !dup.length;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} L${L.lesson_number} ids=${ids.length} man=${man.length} missing=${missing} orphan=${orphan} dup=${dup} badsrc=${bad.length} r2prefix=${JSON.stringify(prefixes)}`);
}

console.log('\n=== data-revision-tip truncation ===');
for (const L of lessons) {
  const t = [...((L.content_html || '').matchAll(/data-revision-tip="([^"]*)"/g))].map(m => m[1]);
  const badT = t.filter(x => /\.\.\.$|…$/.test(x));
  console.log(`  L${L.lesson_number} tips=${t.length} truncated=${badT.length}`);
}

console.log('\n=== glossary <-> dfn data-def consistency ===');
for (const L of lessons) {
  const dfns = [...((L.content_html || '').matchAll(/<dfn class="term" data-def="([^"]*)">([^<]*)<\/dfn>/g))].map(m => ({ def: m[1], term: m[2] }));
  const gl = (L.glossary_terms || []);
  for (const d of dfns) {
    const g = gl.find(g => g.term.toLowerCase() === d.term.toLowerCase().replace(/[’']s$/, ''));
    if (!g) { console.log(`  L${L.lesson_number} dfn "${d.term}" has NO glossary entry`); continue; }
  }
  // report term-name mismatches both ways
  const dTerms = dfns.map(d => d.term.toLowerCase());
  for (const g of gl) if (!dTerms.includes(g.term.toLowerCase())) console.log(`  L${L.lesson_number} glossary "${g.term}" has no matching dfn in body`);
}
