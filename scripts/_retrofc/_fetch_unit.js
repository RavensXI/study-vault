/**
 * Generic unit fetcher for retro fact-check.
 * Usage: node scripts/_retrofc/_fetch_unit.js <subject-slug> <unit-slug>
 */
const fs = require('fs'), path = require('path');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const [subjectSlug, unitSlug] = process.argv.slice(2);

async function q(p) {
  const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
  if (!r.ok) throw new Error(p + ' -> ' + r.status + ' ' + await r.text());
  return r.json();
}

(async () => {
  const subs = await q(`subjects?slug=eq.${subjectSlug}&select=id,slug,name,school_id,status,exam_board,settings`);
  console.log('SUBJECTS:', subs.map(s => `${s.id} school=${s.school_id} status=${s.status} board=${s.exam_board}`).join(' | '));
  let unit = null, subject = null;
  for (const s of subs) {
    const us = await q(`units?subject_id=eq.${s.id}&slug=eq.${unitSlug}&select=id,slug,name,subtitle,sort_order,lesson_count`);
    if (us.length) { unit = us[0]; subject = s; }
  }
  if (!unit) throw new Error('unit not found');
  console.log('UNIT:', JSON.stringify(unit));

  const cols = 'id,lesson_number,slug,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status,tier,updated_at,hero_image_url';
  const rows = await q(`lessons?unit_id=eq.${unit.id}&select=${cols}&order=lesson_number`);

  const base = path.join('scripts', '_retrofc', 'units', `${subjectSlug}__${unitSlug}`);
  const dir = path.join(base, 'raw');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(base, '_raw.json'), JSON.stringify({ subject, unit, lessons: rows }, null, 1));

  for (const r of rows) {
    const nm = r.narration_manifest;
    const nmS = nm ? (Array.isArray(nm) ? `array len ${nm.length}` : `obj ${JSON.stringify(nm).length} chars`) : 'null';
    const out = `=== L${r.lesson_number} ${r.title} ===\nid: ${r.id}\nslug: ${r.slug}\nstatus: ${r.status} tier:${r.tier} updated:${r.updated_at}\nnarration_manifest: ${nmS}\n\n--- DESCRIPTION ---\n${r.description}\n\n--- CONTENT_HTML ---\n${r.content_html}\n\n--- CONCLUSION_HTML ---\n${r.conclusion_html}\n\n--- EXAM_TIP_HTML ---\n${r.exam_tip_html}\n\n--- PRACTICE_QUESTIONS ---\n${JSON.stringify(r.practice_questions, null, 1)}\n\n--- KNOWLEDGE_CHECKS ---\n${JSON.stringify(r.knowledge_checks, null, 1)}\n\n--- FLASHCARD_QUESTIONS ---\n${JSON.stringify(r.flashcard_questions, null, 1)}\n\n--- GLOSSARY_TERMS ---\n${JSON.stringify(r.glossary_terms, null, 1)}\n`;
    fs.writeFileSync(path.join(dir, `L${String(r.lesson_number).padStart(2, '0')}.txt`), out);
    console.log(`L${r.lesson_number}\t${r.title}\tid=${r.id}\tstatus=${r.status}\tchars=${(r.content_html || '').length}\tnm=${nmS}`);
  }
  console.log('TOTAL', rows.length, '-> ', base);
})().catch(e => { console.error(e); process.exit(1); });
