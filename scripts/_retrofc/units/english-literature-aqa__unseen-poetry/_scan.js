// Automated internal-consistency scan for the unseen-poetry retro fact-check.
const fs = require('fs');
const DIR = 'scripts/_retrofc/units/english-literature-aqa__unseen-poetry';
const rows = JSON.parse(fs.readFileSync(DIR + '/_raw.json', 'utf8'));

const PLAIN = ['description'];
const ENTITY = /&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);/g;
const RIVAL = /\b(Edexcel|Pearson|OCR|WJEC|Eduqas|CIE|Cambridge International)\b/gi;
const US = /\b(analyze|analyzed|analyzing|analyzes|realize|realized|recognize|recognized|emphasize|emphasized|color|colors|favorite|behavior|neighbor|traveled|meter|theater|defense|practiced?\s+(?=as a verb)|organize|organized|summarize|summarized|criticize|criticized|memorize)\b/gi;

function walkStrings(v, path, cb) {
  if (typeof v === 'string') return cb(v, path);
  if (Array.isArray(v)) return v.forEach((x, i) => walkStrings(x, path + '[' + i + ']', cb));
  if (v && typeof v === 'object') return Object.entries(v).forEach(([k, x]) => walkStrings(x, path + '.' + k, cb));
}

// crude tag balance check for the html fields
function tagBalance(html) {
  const VOID = new Set(['br', 'hr', 'img', 'input', 'meta', 'link', 'polyline', 'path', 'circle', 'rect', 'line', 'source']);
  const stack = [];
  const issues = [];
  const re = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>/g;
  let m;
  while ((m = re.exec(html))) {
    const [, close, name, attrs] = m;
    const tag = name.toLowerCase();
    if (VOID.has(tag) || attrs.trim().endsWith('/')) continue;
    if (!close) stack.push({ tag, at: m.index });
    else {
      let found = -1;
      for (let i = stack.length - 1; i >= 0; i--) if (stack[i].tag === tag) { found = i; break; }
      if (found === -1) issues.push('stray </' + tag + '> at ' + m.index);
      else {
        for (let i = stack.length - 1; i > found; i--) issues.push('UNCLOSED <' + stack[i].tag + '> opened at ' + stack[i].at);
        stack.length = found;
      }
    }
  }
  stack.forEach(s => issues.push('UNCLOSED <' + s.tag + '> opened at ' + s.at));
  return issues;
}

for (const r of rows) {
  console.log('\n===== L' + r.lesson_number + '  ' + r.title + ' =====');

  // 1. HTML entities in plain-text fields
  for (const f of ['description', 'practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']) {
    walkStrings(r[f], f, (s, p) => {
      const hits = s.match(ENTITY);
      if (hits) console.log('  ENTITY  ' + p + ': ' + [...new Set(hits)].join(',') + ' :: ' + s.slice(0, 90));
    });
  }

  // 2. rival board named / US spelling, everywhere
  for (const f of ['description', 'content_html', 'exam_tip_html', 'conclusion_html', 'practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']) {
    walkStrings(r[f], f, (s, p) => {
      const rb = s.match(RIVAL); if (rb) console.log('  RIVAL-BOARD  ' + p + ': ' + [...new Set(rb)].join(',') + ' :: ' + s.slice(0, 110));
      const us = s.match(US); if (us) console.log('  US-SPELLING  ' + p + ': ' + [...new Set(us)].join(',') + ' :: ' + s.slice(0, 110));
    });
  }

  // 3. HTML well-formedness
  for (const f of ['content_html', 'exam_tip_html', 'conclusion_html']) {
    const iss = tagBalance(r[f] || '');
    iss.forEach(i => console.log('  HTML  ' + f + ': ' + i));
  }

  // 4. band ladders: arithmetic + duplicate labels + total vs question marks
  (r.practice_questions || []).forEach((q, qi) => {
    const declared = (q.type || '').match(/(\d+)\s*marks?/i);
    const max = declared ? +declared[1] : null;
    const bands = [...(q.marks || '').matchAll(/([A-Za-z][A-Za-z\- ]*band)\s*\((\d+)\s*[-–]\s*(\d+)\)/g)]
      .map(m => ({ label: m[1].trim(), lo: +m[2], hi: +m[3] }));
    if (!bands.length) {
      // bullet-style scheme: check the (1 mark) tally against declared marks
      const marks = [...(q.marks || '').matchAll(/\((\d+)\s*marks?\)/g)].map(m => +m[1]);
      if (marks.length && max && marks.reduce((a, b) => a + b, 0) !== max)
        console.log('  PQ[' + qi + '] BULLET-SUM ' + marks.reduce((a, b) => a + b, 0) + ' != declared ' + max);
      return;
    }
    const labels = bands.map(b => b.label);
    if (labels.length !== new Set(labels).size)
      console.log('  PQ[' + qi + '] DUPLICATE BAND LABEL: ' + labels.join(' | '));
    const top = Math.max(...bands.map(b => b.hi));
    if (max && top !== max) console.log('  PQ[' + qi + '] top band hi=' + top + ' but question declares ' + max + ' marks');
    const bot = Math.min(...bands.map(b => b.lo));
    if (bot !== 1) console.log('  PQ[' + qi + '] lowest band starts at ' + bot + ', expected 1');
    const sorted = [...bands].sort((a, b) => a.lo - b.lo);
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i].lo !== sorted[i - 1].hi + 1)
        console.log('  PQ[' + qi + '] GAP/OVERLAP between ' + sorted[i - 1].label + ' (' + sorted[i - 1].lo + '-' + sorted[i - 1].hi + ') and ' + sorted[i].label + ' (' + sorted[i].lo + '-' + sorted[i].hi + ')');
    }
    console.log('  PQ[' + qi + '] (' + (q.type || '') + ') ladder: ' + bands.map(b => b.label + ' ' + b.lo + '-' + b.hi).join(' | '));
  });

  // 5. KC shape + answer index sanity
  (r.knowledge_checks || []).forEach((k, ki) => {
    if (k.type === 'match') {
      if (!Array.isArray(k.left) || !Array.isArray(k.right) || !Array.isArray(k.order))
        console.log('  KC[' + ki + '] match missing left/right/order');
      else if (k.left.length !== k.right.length || k.order.length !== k.left.length)
        console.log('  KC[' + ki + '] match length mismatch');
    } else {
      if (!Array.isArray(k.options)) console.log('  KC[' + ki + '] no options array');
      else if (typeof k.correct !== 'number' || k.correct < 0 || k.correct >= k.options.length)
        console.log('  KC[' + ki + '] correct index out of range: ' + k.correct);
      if ('answers' in k) console.log('  KC[' + ki + '] uses non-canonical answers[] field');
    }
  });

  // 6. glossary <-> dfn cross-check
  const dfns = [...(r.content_html || '').matchAll(/<dfn[^>]*class="term"[^>]*>(.*?)<\/dfn>/gs)]
    .map(m => m[1].replace(/<[^>]+>/g, '').trim().toLowerCase());
  const gterms = (r.glossary_terms || []).map(g => (g.term || '').toLowerCase());
  gterms.filter(t => !dfns.includes(t)).forEach(t => console.log('  GLOSSARY orphan (no matching <dfn>): "' + t + '"'));
  dfns.filter(t => !gterms.includes(t)).forEach(t => console.log('  DFN with no glossary entry: "' + t + '"'));

  // 7. question-number references
  const allText = JSON.stringify(r);
  const qrefs = [...allText.matchAll(/\bQ(?:uestion)?\s?(2[0-9](?:\.\d)?)\b/g)].map(m => m[1]);
  if (qrefs.length) {
    const tally = {}; qrefs.forEach(q => tally[q] = (tally[q] || 0) + 1);
    console.log('  QREFS: ' + Object.entries(tally).map(([k, v]) => 'Q' + k + '×' + v).join(', '));
  }
}
