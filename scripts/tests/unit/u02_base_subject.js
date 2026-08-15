/* Museum exhibit 6: the board-suffix reducer.
   Three copies of this regex live in the codebase (exam-countdown.js,
   main.js, practice-loader.js). They drifted: two of them missed wjec/ncfe
   and -a/-b board variants, so a Foundation student's tier lookup missed on
   e.g. geography-edexcel-a. This test extracts all three FROM SOURCE and
   pins (a) that each one reduces the exhibit cases correctly, (b) that no
   copy drifts from the others again. */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..', '..', '..');

let fails = 0;
function t(name, cond, detail) {
  if (!cond) fails++;
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' — ' + detail : ''));
}

const SOURCES = [
  ['js/exam-countdown.js', /slug\.replace\((\/[^/]+\/)/],
  ['js/main.js', /baseSlug = subject\.replace\((\/[^/]+\/)/],
  ['js/practice-loader.js', /subjectBase = params\.subjectSlug\.replace\((\/[^/]+\/)/],
];

const CASES = [
  ['geography-edexcel-a', 'geography'],
  ['geography-edexcel', 'geography'],
  ['music-tech-ncfe', 'music-tech'],
  ['english-literature-eduqas', 'english-literature'],
  ['sociology-wjec', 'sociology'],
  ['science-ocr-b', 'science'],
  ['maths-aqa', 'maths'],
  ['history', 'history'],                    // no suffix — untouched
  ['separate-sciences', 'separate-sciences'] // 'sciences' is not a board
];

const regexes = [];
for (const [file, finder] of SOURCES) {
  const src = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const m = src.match(finder);
  t(file + ' reducer found in source', !!m);
  if (!m) continue;
  const body = m[1].slice(1, m[1].lastIndexOf('/'));
  const re = new RegExp(body);
  regexes.push([file, body, re]);
  for (const [input, want] of CASES) {
    const got = input.replace(re, '');
    t(file + ': ' + input + ' -> ' + want, got === want, 'got ' + got);
  }
}

// no drift: every copy must strip identically (pattern text may differ in
// grouping style, behaviour must not)
if (regexes.length > 1) {
  for (const [input] of CASES) {
    const outs = regexes.map(([f, b, re]) => input.replace(re, ''));
    t('all copies agree on ' + input, new Set(outs).size === 1, outs.join(' / '));
  }
}

console.log('u02: ' + fails + ' failure(s)');
process.exit(fails ? 1 : 0);
