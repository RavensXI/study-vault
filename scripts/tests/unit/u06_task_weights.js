/* The completion-weights contract (WC-3): TASK_WEIGHTS is exported as
   window.svTaskWeights so the sidebar tags read the same numbers as the
   completion maths; the full set sums to 100 so the tags read honestly as
   percentages; the reader-skin tag builder references every key it needs. */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..', '..', '..');

let fails = 0;
function t(name, cond, detail) {
  if (!cond) fails++;
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' — ' + detail : ''));
}

const main = fs.readFileSync(path.join(ROOT, 'js', 'main.js'), 'utf8');
const m = main.match(/var TASK_WEIGHTS = (\{[\s\S]*?\});/);
t('TASK_WEIGHTS found', !!m);
const W = eval('(' + m[1] + ')');
const sum = Object.values(W).reduce((a, b) => a + b, 0);
t('full weight set sums to 100 (tags show %)', sum === 100, 'sum=' + sum);
t('practice question is the anchor at 40', W['practice-question'] === 40);
t('exported as window.svTaskWeights', /window\.svTaskWeights = TASK_WEIGHTS/.test(main));

const skin = fs.readFileSync(path.join(ROOT, 'js', 'reader-skin.js'), 'utf8');
for (const key of ['knowledge-check', 'flashcards', 'practice-question', 'podcast', 'video']) {
  t("tag builder uses W['" + key + "']", skin.includes("W['" + key + "']"));
}
t('tag builder renders percent signs', /'%'/.test(skin.match(/function addWeightTags[\s\S]*?\n  \}/)[0]));

console.log('u06: ' + fails + ' failure(s)');
process.exit(fails ? 1 : 0);
