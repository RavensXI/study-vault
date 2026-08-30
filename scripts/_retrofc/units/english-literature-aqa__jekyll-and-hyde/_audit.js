const fs = require('fs');
const D = __dirname;
const { lessons } = JSON.parse(fs.readFileSync(D + '/_raw.json', 'utf8'));

const ENT = /&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g;
const BOARD = /\b(Edexcel|OCR|Eduqas|WJEC|CIE|CAIE|Cambridge International)\b/g;
const US = /\b\w*(?:ize|izes|ized|izing|ization|yze|yzes|yzed|yzing|izer)\b|\bcolor\b|\bhonor\b|\bbehavior\b|\bfavor\b|\bpracticing\b|\bdefense\b|\bcenter\b/gi;
const US_OK = /\b(size|sizes|sized|sizing|prize|prizes|prized|capsize|resize|maize)\b/i;

for (const r of lessons) {
  const n = r.lesson_number;
  const html = (r.content_html || '') + '\n' + (r.exam_tip_html || '') + '\n' + (r.conclusion_html || '');
  const jsonFields = JSON.stringify([r.practice_questions, r.knowledge_checks, r.flashcard_questions, r.glossary_terms]);
  const all = html + '\n' + jsonFields + '\n' + (r.description || '') + '\n' + (r.title || '');

  const out = [];
  const ent = jsonFields.match(ENT); if (ent) out.push('ENTITY in plain-text JSON fields: ' + [...new Set(ent)].join(' '));
  const entH = (r.description || '').match(ENT); if (entH) out.push('ENTITY in description: ' + entH.join(' '));
  const bd = all.match(BOARD); if (bd) out.push('RIVAL BOARD: ' + [...new Set(bd)].join(' '));
  const us = (all.match(US) || []).filter(w => !US_OK.test(w)); if (us.length) out.push('US SPELLING: ' + [...new Set(us)].join(' '));

  // truncated attributes
  const trunc = [...html.matchAll(/data-revision-tip="([^"]*\.\.\.)"/g)].map(m => m[1]);
  if (trunc.length) out.push('TRUNCATED revision-tip: ' + trunc.map(t => '…' + t.slice(-45)).join(' | '));

  // spag claim
  const spag = (jsonFields.match(/spelling\/grammar \(4 marks\)/g) || []).length;
  if (spag) out.push(`SPaG CLAIM on 19th-c novel question x${spag}`);

  // band ladders
  (r.practice_questions || []).forEach((pq, i) => {
    const m = pq.marks || '', t = pq.type || '';
    const bands = [...m.matchAll(/([A-Z][A-Za-z\- ]*band) \((\d+)[–\-](\d+)\)/g)].map(x => [x[1], +x[2], +x[3]]);
    const labels = bands.map(b => b[0]);
    const dupes = labels.filter((l, j) => labels.indexOf(l) !== j);
    if (dupes.length) out.push(`pq[${i}] DUPLICATE band label: ${[...new Set(dupes)].join(',')}`);
    const max = Math.max(...bands.map(b => b[2]));
    const declared = (t.match(/^(\d+) marks/) || [])[1];
    if (declared && +declared !== max) out.push(`pq[${i}] type=${declared} but ladder max=${max}`);
    // contiguity
    for (let k = 0; k < bands.length - 1; k++) {
      if (bands[k][1] !== bands[k + 1][2] + 1) out.push(`pq[${i}] band gap/overlap: ${bands[k][0]}(${bands[k][1]}) vs ${bands[k+1][0]}(${bands[k+1][2]})`);
    }
    if (bands.length && bands[bands.length - 1][1] !== 1) out.push(`pq[${i}] lowest band does not start at 1`);
  });

  // KC shape
  (r.knowledge_checks || []).forEach((kc, i) => {
    if (kc.type === 'match') {
      if (!Array.isArray(kc.order) || !Array.isArray(kc.left) || !Array.isArray(kc.right)) out.push(`kc[${i}] match missing arrays`);
      else {
        if (kc.left.length !== kc.right.length || kc.order.length !== kc.left.length) out.push(`kc[${i}] match length mismatch`);
        const s = [...kc.order].sort().join(','); const exp = kc.left.map((_, j) => j).join(',');
        if (s !== exp) out.push(`kc[${i}] match order not a permutation: ${kc.order}`);
      }
    } else {
      if (!Array.isArray(kc.options)) out.push(`kc[${i}] no options`);
      else if (typeof kc.correct !== 'number' || kc.correct < 0 || kc.correct >= kc.options.length) out.push(`kc[${i}] bad correct index`);
      if ('answers' in kc) out.push(`kc[${i}] uses answers[] (non-canonical)`);
    }
  });

  // narration integrity
  const ids = [...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m => m[1]);
  const man = new Set((r.narration_manifest || []).map(e => e.id));
  const missing = ids.filter(i => !man.has(i));
  const orphan = [...man].filter(i => !ids.includes(i));
  if (missing.length) out.push('narration MISSING clips: ' + missing.join(','));
  if (orphan.length) out.push('narration ORPHAN clips: ' + orphan.join(','));
  const dupIds = ids.filter((x, j) => ids.indexOf(x) !== j);
  if (dupIds.length) out.push('narration DUP ids: ' + [...new Set(dupIds)].join(','));

  // glossary vs dfn sync
  const defs = [...html.matchAll(/<dfn class="term" data-def="([^"]*)">([^<]*)<\/dfn>/g)].map(m => [m[2], m[1]]);
  const gl = new Map((r.glossary_terms || []).map(g => [g.term, g.definition]));
  for (const [term, def] of defs) {
    if (!gl.has(term)) out.push(`dfn "${term}" not in glossary_terms`);
    else if (gl.get(term) !== def) out.push(`dfn "${term}" definition differs from glossary`);
  }
  for (const t of gl.keys()) if (!defs.find(d => d[0] === t)) out.push(`glossary "${t}" has no dfn in html`);

  console.log(`\n=== L${n} ${r.title} (${ids.length} narrated ids) ===`);
  if (!out.length) console.log('  clean');
  out.forEach(s => console.log('  - ' + s));
}
