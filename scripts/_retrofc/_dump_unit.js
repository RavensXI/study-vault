/** dump selected lessons of a unit to JSON for exact-string work */
const fs = require('fs');
const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const UNIT = process.argv[2];
const OUT = process.argv[3];
async function q(p) { const r = await fetch(`${SB}/rest/v1/${p}`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }); if (!r.ok) throw new Error(p + ' ' + r.status + await r.text()); return r.json(); }
(async () => {
  const cols = 'id,lesson_number,title,slug,status,description,content_html,conclusion_html,exam_tip_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  fs.writeFileSync(OUT, JSON.stringify(rows, null, 1), 'utf8');
  console.log(`wrote ${rows.length} rows -> ${OUT}`);
  for (const r of rows) console.log(`  L${String(r.lesson_number).padStart(2, '0')} ${r.status} ${r.id} ${r.title}`);
})().catch(e => { console.error(e); process.exit(1); });
