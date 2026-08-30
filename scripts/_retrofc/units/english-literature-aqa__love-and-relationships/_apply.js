/**
 * Retro fact-check applier for english-literature-aqa / love-and-relationships.
 *
 * Reads _plan.json (array of {lesson_number, id, findings:[...], edits:[{field, find, replace, count}]}).
 * For each lesson, in order:
 *   1. fetch the live row
 *   2. apply every edit as an exact string replacement (JSON fields are edited as
 *      their serialised form, then re-parsed so shape is preserved)
 *   3. verify each `find` occurred exactly `count` times - abort the lesson otherwise
 *   4. append the BEFORE values to _backup.json and FLUSH TO DISK
 *   5. PATCH lessons?id=eq.<id>
 *   6. append to _report.json and FLUSH TO DISK
 *
 * A killed run loses nothing: backup is written before the PATCH.
 *
 * Usage: node _apply.js --dry-run | node _apply.js
 */
const fs = require('fs');
const path = require('path');

const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const HERE = __dirname;
const PLAN = path.join(HERE, process.env.PLAN_FILE || '_plan.json');
const BACKUP = path.join(HERE, '_backup.json');
const REPORT = path.join(HERE, '_report.json');
const DRY = process.argv.includes('--dry-run');

const JSON_FIELDS = new Set(['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']);

const hdr = { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' };

async function get(p) {
  const r = await fetch(SB + '/rest/v1/' + p, { headers: hdr });
  if (!r.ok) throw new Error(p + ' -> ' + r.status + ' ' + await r.text());
  return r.json();
}
async function patch(id, body) {
  const r = await fetch(SB + '/rest/v1/lessons?id=eq.' + id, {
    method: 'PATCH', headers: { ...hdr, Prefer: 'return=minimal' }, body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error('PATCH ' + id + ' -> ' + r.status + ' ' + await r.text());
}

function load(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return fallback; }
}
function flush(file, obj) { fs.writeFileSync(file, JSON.stringify(obj, null, 1)); }

(async () => {
  const plan = load(PLAN, null);
  if (!plan) throw new Error('no _plan.json');

  const backup = load(BACKUP, { unit: 'english-literature-aqa/love-and-relationships', lessons: [] });
  const report = load(REPORT, {
    unit: 'english-literature-aqa/love-and-relationships',
    unit_id: '170f32cc-ff7e-4ae6-8376-3dd18d1208f4',
    subject_id: 'ebecab63-5c56-4c4c-9393-9c3fd335f8a1',
    started: new Date().toISOString(),
    lessons: []
  });

  for (const p of plan) {
    // The resume guard applies to the main plan only; a supplementary PLAN_FILE
    // is by definition a second pass over lessons already marked applied.
    if (!process.env.PLAN_FILE && report.lessons.some(l => l.lesson_number === p.lesson_number && l.applied)) {
      console.log(`L${p.lesson_number}: already applied, skipping`); continue;
    }
    const cols = 'id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms';
    const [row] = await get(`lessons?id=eq.${p.id}&select=${cols}`);
    if (!row) throw new Error('L' + p.lesson_number + ': row not found');

    const before = {}, update = {};
    let failed = null;

    // group edits by field so multiple edits to one field compose
    const byField = {};
    for (const e of (p.edits || [])) (byField[e.field] ||= []).push(e);

    for (const [field, edits] of Object.entries(byField)) {
      const isJson = JSON_FIELDS.has(field);
      const orig = row[field];
      let s = isJson ? JSON.stringify(orig) : (orig || '');
      for (const e of edits) {
        const want = e.count === undefined ? 1 : e.count;
        // JSON-field finds are written as the SERIALISED form already, so they
        // must NOT be re-escaped here - that would turn " into \" and never match.
        const find = e.find;
        const repl = e.replace;
        const n = s.split(find).length - 1;
        if (n !== want) { failed = `L${p.lesson_number} ${field}: expected ${want} of ${JSON.stringify(e.find).slice(0, 70)}, found ${n}`; break; }
        s = s.split(find).join(repl);
      }
      if (failed) break;
      before[field] = orig;
      update[field] = isJson ? JSON.parse(s) : s;
    }

    if (failed) { console.error('!! ' + failed); process.exitCode = 1; break; }

    // Merge, never replace: on a supplementary pass the EARLIEST recorded value
    // for a field must survive, or the true pre-fix original is lost.
    const bi = backup.lessons.findIndex(l => l.lesson_number === p.lesson_number);
    if (bi >= 0) {
      const prev = backup.lessons[bi];
      for (const [f, v] of Object.entries(before)) if (!(f in prev.before)) prev.before[f] = v;
      prev.backed_up_at = prev.backed_up_at || new Date().toISOString();
      prev.last_touched_at = new Date().toISOString();
    } else {
      backup.lessons.push({
        lesson_number: p.lesson_number, id: p.id, title: row.title,
        backed_up_at: new Date().toISOString(), before
      });
    }
    if (!DRY) flush(BACKUP, backup);          // <-- backup on disk BEFORE the write

    if (!DRY) await patch(p.id, update);

    const ri = report.lessons.findIndex(l => l.lesson_number === p.lesson_number);
    const rep = {
      lesson_number: p.lesson_number, id: p.id, title: row.title,
      fields_changed: Object.keys(update),
      fixed: p.findings.filter(f => f.action === 'fixed'),
      flagged: p.findings.filter(f => f.action === 'flagged'),
      verified_clean: p.findings.filter(f => f.action === 'verified'),
      applied: !DRY, applied_at: DRY ? null : new Date().toISOString()
    };
    if (ri >= 0) {
      const prev = report.lessons[ri];             // supplementary pass: union, not overwrite
      const uniq = (a, b) => { const seen = new Set(a.map(x => x.id)); return a.concat(b.filter(x => !seen.has(x.id))); };
      rep.fields_changed = [...new Set(prev.fields_changed.concat(rep.fields_changed))];
      rep.fixed = uniq(prev.fixed, rep.fixed);
      rep.flagged = uniq(prev.flagged, rep.flagged);
      rep.verified_clean = uniq(prev.verified_clean || [], rep.verified_clean);
      report.lessons[ri] = rep;
    } else report.lessons.push(rep);
    flush(REPORT, report);

    console.log(`L${p.lesson_number} ${DRY ? '[dry]' : 'PATCHED'}  fields: ${Object.keys(update).join(', ') || '(none)'}  fixed=${rep.fixed.length} flagged=${rep.flagged.length}`);
  }
  console.log('done');
})();
