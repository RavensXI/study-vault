const URL = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
const fs=require('fs'), path=require('path');
const UNIT='ce6cd0d6-72b3-47fe-aafd-57d396898470';
async function q(p){const r=await fetch(`${URL}/rest/v1/${p}`,{headers:{apikey:KEY,Authorization:`Bearer ${KEY}`}});if(!r.ok)throw new Error(p+' -> '+r.status+' '+await r.text());return r.json();}
(async()=>{
  const cols='id,lesson_number,slug,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest,status,tier,updated_at';
  const rows=await q(`lessons?unit_id=eq.${UNIT}&select=${cols}&order=lesson_number`);
  const dir='scripts/_retrofc/raw'; fs.mkdirSync(dir,{recursive:true});
  fs.writeFileSync('scripts/_retrofc/_macbeth_raw.json', JSON.stringify(rows,null,1));
  for(const r of rows){
    const nm = r.narration_manifest;
    const nmSummary = nm ? (Array.isArray(nm)? `array len ${nm.length}` : `obj keys ${Object.keys(nm).join('|')} ${JSON.stringify(nm).length} chars`) : 'null';
    let out = `=== L${r.lesson_number} ${r.title} ===\nid: ${r.id}\nslug: ${r.slug}\nstatus: ${r.status} tier:${r.tier} updated:${r.updated_at}\nnarration_manifest: ${nmSummary}\n\n--- DESCRIPTION ---\n${r.description}\n\n--- CONTENT_HTML ---\n${r.content_html}\n\n--- CONCLUSION_HTML ---\n${r.conclusion_html}\n\n--- EXAM_TIP_HTML ---\n${r.exam_tip_html}\n\n--- PRACTICE_QUESTIONS ---\n${JSON.stringify(r.practice_questions,null,1)}\n\n--- KNOWLEDGE_CHECKS ---\n${JSON.stringify(r.knowledge_checks,null,1)}\n\n--- FLASHCARD_QUESTIONS ---\n${JSON.stringify(r.flashcard_questions,null,1)}\n\n--- GLOSSARY_TERMS ---\n${JSON.stringify(r.glossary_terms,null,1)}\n`;
    fs.writeFileSync(path.join(dir,`L${String(r.lesson_number).padStart(2,'0')}.txt`), out);
    console.log(`L${r.lesson_number}\t${r.title}\t${r.id}\tstatus=${r.status}\tchars=${(r.content_html||'').length}\tnm=${nmSummary}`);
  }
  console.log('TOTAL', rows.length);
})();
