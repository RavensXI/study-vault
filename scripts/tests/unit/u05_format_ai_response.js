/* Museum exhibit 10 (fixed as WC-5): AI-marker markdown never renders raw.
   The marker drifts between #, ## and ### headings and **bold** — the
   extracted LIVE formatAiResponse from main.js must convert all of them and
   escape any HTML the model emits. */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..', '..', '..');

let fails = 0;
function t(name, cond, detail) {
  if (!cond) fails++;
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' — ' + detail : ''));
}

const src = fs.readFileSync(path.join(ROOT, 'js', 'main.js'), 'utf8');
const escFn = src.match(/function escapeHtml\(s\) \{[\s\S]*?\n  \}/);
const fmtFn = src.match(/function formatAiResponse\(text\) \{[\s\S]*?\n  \}/);
t('escapeHtml found in source', !!escFn);
t('formatAiResponse found in source', !!fmtFn);
if (!escFn || !fmtFn) { console.log('u05: ' + fails + ' failure(s)'); process.exit(1); }
eval(escFn[0] + '\n' + fmtFn[0]);

const out = formatAiResponse(
  '# Mark: 2/2\n\n## What worked\nYou named the **sequence**.\n\n### Suggestion\nAnchor it to a bar.');
const textOnly = out.replace(/<[^>]+>/g, '');
t('single-hash heading converts', out.includes('<h3>Mark: 2/2</h3>'));
t('double-hash heading converts', out.includes('<h3>What worked</h3>'));
t('triple-hash heading converts', out.includes('<h3>Suggestion</h3>'));
t('bold converts', out.includes('<strong>sequence</strong>'));
t('no raw hash marks leak', !/^#/m.test(textOnly), JSON.stringify(textOnly.slice(0, 40)));

const hostile = formatAiResponse('Mark: 1/2 <script>alert(1)</script> **ok**');
t('model-emitted HTML is escaped', !hostile.includes('<script>') && hostile.includes('&lt;script&gt;'));

console.log('u05: ' + fails + ' failure(s)');
process.exit(fails ? 1 : 0);
