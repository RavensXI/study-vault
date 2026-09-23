/* Run the safeguarding check over the labelled cases (all hand-written, no real
   pupil text). c = concerning, a = ambiguous/venting, b = benign.
   Local runs have no AWS keys, so they need ALLOW_US_FALLBACK=1; production runs
   the same check on Bedrock in London.
     ALLOW_US_FALLBACK=1 node scripts/safeguarding/test_check.js */
const { check } = require('../../api/_lib/safeguard');
const cases = require('./cases.json');
(async () => {
  const out = []; let i = 0;
  async function worker() { while (i < cases.length) { const k = i++; const c = cases[k];
    const r = await check({ text: c.text, context: c.context, source: 'exam_answer' }).catch(e => ({ decision: 'error', reason: e.message }));
    out[k] = Object.assign({}, c, { decision: r && r.decision, category: r && r.category, reason: r && r.reason }); } }
  await Promise.all([worker(), worker(), worker(), worker(), worker()]);
  const flagged = r => r.decision === 'concern' || r.decision === 'unsure';
  for (const L of ['c', 'a', 'b']) { const g = out.filter(r => r.label === L); console.log(L, 'flagged', g.filter(flagged).length + '/' + g.length); }
  console.log('\nMISSED CONCERNS:'); out.filter(r => r.label === 'c' && !flagged(r)).forEach(r => console.log(' -', r.decision, '|', r.text.slice(0, 100)));
  console.log('\nBENIGN FLAGGED:'); out.filter(r => r.label === 'b' && flagged(r)).forEach(r => console.log(' -', r.decision, '|', r.text.slice(0, 100), '|', r.reason));
  console.log('\nAMBIGUOUS:'); out.filter(r => r.label === 'a').forEach(r => console.log(' -', r.decision.padEnd(7), '|', r.text.slice(0, 90)));
  require('fs').writeFileSync(__dirname + '/last_run.json', JSON.stringify(out, null, 1));
})();
