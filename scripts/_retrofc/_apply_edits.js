/**
 * Retro fact-check: apply the surgical edits in <unit-dir>/_edits.json to the
 * live lessons, with an incremental backup in the exact shape that
 * _renarrate_from_backup.py reads ({lessons:[{id, lesson_number, before:{}}]}).
 *
 * Usage:
 *   node scripts/_retrofc/_apply_edits.js <unit-dir> [--dry-run]
 *
 * _edits.json is an array. Two kinds of edit:
 *   text edit  {lesson, field, find, replace, severity, note}
 *              field in description | content_html | exam_tip_html | conclusion_html
 *              `find` must occur EXACTLY ONCE in the field's current value (after
 *              any earlier edit to the same field) or the edit is skipped.
 *   json edit  {lesson, field, path, expect?, value, severity, note}
 *              field in practice_questions | knowledge_checks | flashcard_questions
 *              | glossary_terms. `path` like "[2].correct" or "[0].options[1]".
 *              If `expect` is given the current value must deep-equal it.
 *
 * Nothing is written unless every check for that edit passes; a skipped edit
 * never blocks the others. Fresh rows are fetched from Supabase (never from
 * _raw.json) so edits are applied to what is live right now.
 */
const fs = require('fs');
const path = require('path');

const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const DRY = process.argv.includes('--dry-run');
const DIR = path.resolve(process.argv[2] || '');
if (!DIR || !fs.existsSync(path.join(DIR, '_raw.json'))) {
  console.error('usage: _apply_edits.js <unit-dir> [--dry-run]  (unit-dir must hold _raw.json)');
  process.exit(2);
}
const EDITS_F = path.join(DIR, '_edits.json');
const BACKUP_F = path.join(DIR, '_backup.json');
const LOG_F = path.join(DIR, '_fix.log');
const RESULT_F = path.join(DIR, '_apply_result.json');

const TEXT_FIELDS = new Set(['description', 'content_html', 'exam_tip_html', 'conclusion_html']);
const JSON_FIELDS = new Set(['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']);
const ALL_FIELDS = [...TEXT_FIELDS, ...JSON_FIELDS];

const lines = [];
const L = (s) => { console.log(s); lines.push(s); };

async function q(p, opts) {
  const r = await fetch(`${SB}/rest/v1/${p}`, {
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
    ...opts,
  });
  if (!r.ok) throw new Error(`${p} -> ${r.status} ${await r.text()}`);
  return r.json();
}

function parsePath(p) {
  const toks = [];
  const re = /\[(\d+)\]|\.?([A-Za-z_][A-Za-z0-9_]*)|^(\d+)/g;
  let m;
  while ((m = re.exec(p)) !== null) {
    if (m[1] !== undefined) toks.push(Number(m[1]));
    else if (m[2] !== undefined) toks.push(m[2]);
    else if (m[3] !== undefined) toks.push(Number(m[3]));
  }
  return toks;
}
function getAt(obj, toks) { let c = obj; for (const t of toks) { if (c == null) return undefined; c = c[t]; } return c; }
function setAt(obj, toks, v) { let c = obj; for (let i = 0; i < toks.length - 1; i++) c = c[toks[i]]; c[toks[toks.length - 1]] = v; }
const deq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const countOcc = (hay, needle) => { if (!needle) return 0; let n = 0, i = 0; while ((i = hay.indexOf(needle, i)) !== -1) { n++; i += needle.length; } return n; };

(async () => {
  const raw = JSON.parse(fs.readFileSync(path.join(DIR, '_raw.json'), 'utf8'));
  const unitId = raw.unit.id;
  let edits = [];
  if (fs.existsSync(EDITS_F)) edits = JSON.parse(fs.readFileSync(EDITS_F, 'utf8'));
  if (!Array.isArray(edits)) throw new Error('_edits.json must be an array');
  L(`=== APPLY EDITS ${raw.subject.slug}/${raw.unit.slug}  ${edits.length} edits  ${DRY ? 'DRY RUN' : 'LIVE'}  ${new Date().toISOString()}`);

  const rows = await q(`lessons?unit_id=eq.${unitId}&select=id,lesson_number,title,${ALL_FIELDS.join(',')}&order=lesson_number`);
  const byNum = new Map(rows.map(r => [r.lesson_number, r]));

  const backup = fs.existsSync(BACKUP_F)
    ? JSON.parse(fs.readFileSync(BACKUP_F, 'utf8'))
    : { generated_at: new Date().toISOString(), unit_id: unitId, subject: raw.subject.slug, unit: raw.unit.slug, lessons: [] };

  const result = { applied: 0, skipped: 0, lessons_changed: 0, fields_changed: 0, skips: [] };
  const byLesson = new Map();
  edits.forEach((e, i) => { e._i = i; if (!byLesson.has(e.lesson)) byLesson.set(e.lesson, []); byLesson.get(e.lesson).push(e); });

  for (const [num, list] of [...byLesson.entries()].sort((a, b) => a[0] - b[0])) {
    const row = byNum.get(num);
    if (!row) { list.forEach(e => { result.skipped++; result.skips.push({ i: e._i, why: `no live lesson ${num}` }); L(`  SKIP #${e._i} L${num}: no such lesson`); }); continue; }
    const work = {};       // field -> working value
    const original = {};   // field -> original value (for backup)
    const touched = new Set();
    for (const e of list) {
      const f = e.field;
      if (!(TEXT_FIELDS.has(f) || JSON_FIELDS.has(f))) { result.skipped++; result.skips.push({ i: e._i, why: `bad field ${f}` }); L(`  SKIP #${e._i} L${num}.${f}: field not editable`); continue; }
      if (!(f in work)) { original[f] = row[f]; work[f] = JSON_FIELDS.has(f) ? JSON.parse(JSON.stringify(row[f] == null ? null : row[f])) : (row[f] || ''); }
      if (TEXT_FIELDS.has(f)) {
        const n = countOcc(work[f], e.find);
        if (n !== 1) { result.skipped++; result.skips.push({ i: e._i, why: `find occurs ${n}x in L${num}.${f}` }); L(`  SKIP #${e._i} L${num}.${f}: find occurs ${n} times (need exactly 1)`); continue; }
        if (typeof e.replace !== 'string') { result.skipped++; result.skips.push({ i: e._i, why: 'replace missing' }); L(`  SKIP #${e._i} L${num}.${f}: replace missing`); continue; }
        work[f] = work[f].replace(e.find, () => e.replace);
      } else {
        const toks = parsePath(String(e.path || ''));
        if (!toks.length || work[f] == null) { result.skipped++; result.skips.push({ i: e._i, why: `bad path ${e.path}` }); L(`  SKIP #${e._i} L${num}.${f}: bad path`); continue; }
        const cur = getAt(work[f], toks);
        if (cur === undefined && e.expect !== undefined) { result.skipped++; result.skips.push({ i: e._i, why: `path ${e.path} not found` }); L(`  SKIP #${e._i} L${num}.${f}${e.path}: path not found`); continue; }
        if (e.expect !== undefined && !deq(cur, e.expect)) { result.skipped++; result.skips.push({ i: e._i, why: `expect mismatch at ${e.path}` }); L(`  SKIP #${e._i} L${num}.${f}${e.path}: current value differs from expect`); continue; }
        try { setAt(work[f], toks, e.value); } catch (err) { result.skipped++; result.skips.push({ i: e._i, why: `set failed ${err.message}` }); L(`  SKIP #${e._i} L${num}.${f}${e.path}: ${err.message}`); continue; }
      }
      touched.add(f);
      result.applied++;
      L(`  ok   #${e._i} L${num}.${f}${e.path ? e.path : ''} [${e.severity || '?'}] ${(e.note || '').slice(0, 110)}`);
    }
    if (!touched.size) continue;
    const patch = {};
    const before = {};
    for (const f of touched) {
      if (deq(work[f], original[f])) continue;   // net no-op (e.g. edit then revert)
      patch[f] = work[f];
      before[f] = original[f];
    }
    if (!Object.keys(patch).length) continue;
    result.lessons_changed++;
    result.fields_changed += Object.keys(patch).length;
    if (DRY) { L(`  DRY  L${num}: would PATCH ${Object.keys(patch).join(', ')}`); continue; }
    // backup BEFORE the write, and flush it to disk before the write
    let entry = backup.lessons.find(b => b.id === row.id);
    if (!entry) { entry = { id: row.id, lesson_number: num, title: row.title, before: {} }; backup.lessons.push(entry); }
    for (const f of Object.keys(before)) if (!(f in entry.before)) entry.before[f] = before[f];   // keep the earliest original
    fs.writeFileSync(BACKUP_F, JSON.stringify(backup, null, 1));
    await q(`lessons?id=eq.${row.id}`, { method: 'PATCH', body: JSON.stringify(patch) });
    L(`  PATCH L${num}: ${Object.keys(patch).join(', ')}`);
  }
  L(`=== ${result.applied} applied, ${result.skipped} skipped, ${result.lessons_changed} lessons / ${result.fields_changed} fields ${DRY ? 'would change' : 'changed'}`);
  if (!DRY) {
    fs.writeFileSync(RESULT_F, JSON.stringify(result, null, 1));
    fs.appendFileSync(LOG_F, lines.join('\n') + '\n');
  }
  if (result.skipped) process.exitCode = 3;
})().catch(e => { console.error(e); process.exit(1); });
