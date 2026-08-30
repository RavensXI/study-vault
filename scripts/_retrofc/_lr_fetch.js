const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs = require('fs'), path = require('path');
const UNIT = '170f32cc-ff7e-4ae6-8376-3dd18d1208f4';
const OUT = 'scripts/_retrofc/units/english-literature-aqa__love-and-relationships';
const q = async p => { const r = await fetch(SB + '/rest/v1/' + p, { headers: { apikey: KEY, Authorization: 'Bearer ' + KEY } }); if (!r.ok) throw new Error(p + ' ' + r.status + ' ' + await r.text()); return r.json(); };
(async () => {
  const cols = 'id,lesson_number,slug,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status,tier,updated_at';
  const rows = await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  fs.mkdirSync(path.join(OUT, 'raw'), { recursive: true });
  fs.writeFileSync(path.join(OUT, '_raw.json'), JSON.stringify(rows, null, 1));
  for (const r of rows) {
    const nm = r.narration_manifest;
    const nmS = nm ? (Array.isArray(nm) ? `array len ${nm.length}` : `obj ${Object.keys(nm).join('|')}`) : 'null';
    const out = `=== L${r.lesson_number} ${r.title} ===\nid: ${r.id}\nslug: ${r.slug}\nstatus: ${r.status} tier:${r.tier} updated:${r.updated_at}\nnarration_manifest: ${nmS}\n\n--- DESCRIPTION ---\n${r.description}\n\n--- CONTENT_HTML ---\n${r.content_html}\n\n--- CONCLUSION_HTML ---\n${r.conclusion_html}\n\n--- EXAM_TIP_HTML ---\n${r.exam_tip_html}\n\n--- PRACTICE_QUESTIONS ---\n${JSON.stringify(r.practice_questions, null, 1)}\n\n--- KNOWLEDGE_CHECKS ---\n${JSON.stringify(r.knowledge_checks, null, 1)}\n\n--- FLASHCARD_QUESTIONS ---\n${JSON.stringify(r.flashcard_questions, null, 1)}\n\n--- GLOSSARY_TERMS ---\n${JSON.stringify(r.glossary_terms, null, 1)}\n`;
    fs.writeFileSync(path.join(OUT, 'raw', `L${String(r.lesson_number).padStart(2, '0')}.txt`), out);
    console.log(`L${r.lesson_number}\t${r.title}\tstatus=${r.status}\tchars=${(r.content_html || '').length}\tnm=${nmS}\t${r.id}`);
  }
  console.log('TOTAL', rows.length);
})();
