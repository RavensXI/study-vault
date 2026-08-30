/* ============================================================
   One command that tells a widget builder whether the thing works.

   node scripts/widget_pipeline/harness/check.mjs <widget.js> [--json]

   Replaces the browser session each agent was otherwise improvising:
   spinning up a page, mounting the widget at several widths, reading
   heights, hunting overflow. That loop cost ~30 tool calls and a pile of
   screenshots per widget. This is one call returning one verdict.

   Zero dependencies: headless Chrome renders a self-measuring page and
   --dump-dom hands back the JSON. Real layout engine, real heights.
   ============================================================ */
import { execFile } from 'node:child_process';
import { readFileSync, writeFileSync, mkdtempSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium'
].find(p => existsSync(p));

const widgetPath = process.argv[2];
const asJson = process.argv.includes('--json');
if (!widgetPath) {
  console.error('usage: node check.mjs <widget.js> [--json]');
  process.exit(2);
}
if (!CHROME) {
  console.error('no Chrome or Edge found; cannot measure.');
  process.exit(2);
}

const src = readFileSync(resolve(widgetPath), 'utf8');
const staticProblems = [];

/* Contract breaches worth catching before spending a browser launch. */
const forbidden = [
  [/\bfetch\s*\(/, 'fetch() - widgets must be self-contained, no network'],
  [/XMLHttpRequest/, 'XMLHttpRequest - no network'],
  [/\bnew\s+Function\b/, 'new Function - not allowed'],
  [/(^|[^.\w])eval\s*\(/, 'eval() - not allowed'],
  [/localStorage|sessionStorage/, 'storage access - widgets must not persist outside root'],
  [/https?:\/\/(?!www\.w3\.org)/, 'an absolute http(s) URL - no remote assets, CSP will block it']
];
for (const [re, msg] of forbidden) {
  if (re.test(src)) staticProblems.push(msg);
}
if (!/window\.SVWidget\s*=/.test(src)) {
  staticProblems.push('never assigns window.SVWidget');
}

/* CSS scoping is NOT checked by regex here - guessing selectors out of
   JavaScript produced false positives every time. selfcheck.html instead
   plants real page furniture outside the widget and reports if the
   widget's styles reach it, which is the thing that actually matters. */

const dir = mkdtempSync(join(tmpdir(), 'svcheck-'));
const page = join(dir, 'run.html');
const harness = readFileSync(join(HERE, 'selfcheck.html'), 'utf8');
if (!harness.includes('<!--WIDGET-->')) {
  console.error('selfcheck.html has lost its <!--WIDGET--> placeholder');
  process.exit(2);
}
writeFileSync(page, harness.replace('<!--WIDGET-->', '<script>' + src + '</script>'), 'utf8');

execFile(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  '--virtual-time-budget=8000', '--run-all-compositor-stages-before-draw',
  '--dump-dom', 'file:///' + page.replace(/\\/g, '/')
], { maxBuffer: 40 * 1024 * 1024, timeout: 90000 }, (err, stdout) => {
  let verdict = null;
  const m = stdout && stdout.match(/SVCHECK([\s\S]*?)ENDSVCHECK/);
  if (m) {
    try { verdict = JSON.parse(m[1]); } catch (e) { /* leave null */ }
  }
  if (!verdict) {
    const out = {
      ok: false,
      problems: ['harness produced no verdict' + (err ? ': ' + err.message : '')].concat(staticProblems)
    };
    console.log(asJson ? JSON.stringify(out, null, 1) : render(out));
    process.exit(1);
  }
  verdict.problems = staticProblems.concat(verdict.problems || []);
  verdict.ok = verdict.ok && staticProblems.length === 0;
  console.log(asJson ? JSON.stringify(verdict, null, 1) : render(verdict));
  process.exit(verdict.ok ? 0 : 1);
});

function render(v) {
  const L = [];
  L.push((v.ok ? 'PASS  ' : 'FAIL  ') + ((v.info && v.info.id) || ''));
  if (v.widths && Object.keys(v.widths).length) {
    L.push('');
    L.push('  width   height  budget');
    for (const [w, m] of Object.entries(v.widths)) {
      L.push('  ' + String(w).padStart(5) + 'px ' + String(m.height).padStart(6) + 'px ' +
             String(m.budget).padStart(6) + 'px' + (m.over ? '   OVER' : ''));
    }
  }
  if (v.info) {
    L.push('');
    L.push('  commit control: ' + (v.info.hasCommit ? 'yes' : 'NO') +
           '   state exposed: ' + (v.info.exposesState ? 'yes' : 'NO') +
           '   keyboard reachable: ' + (v.info.focusables || 0) +
           '   controls moving state: ' + (v.info.buttonsThatChangedState ?? '?') +
           '/' + (v.info.buttons ?? '?'));
  }
  if (v.problems && v.problems.length) {
    L.push('');
    for (const p of v.problems) L.push('  - ' + p);
  }
  return L.join('\n');
}
