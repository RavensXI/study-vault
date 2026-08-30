const URL=process.env.SUPABASE_URL, KEY=process.env.SUPABASE_SERVICE_KEY;
const fs=require('fs');
const UNIT='ce6cd0d6-72b3-47fe-aafd-57d396898470';
async function q(p){const r=await fetch(`${URL}/rest/v1/${p}`,{headers:{apikey:KEY,Authorization:`Bearer ${KEY}`}});if(!r.ok)throw new Error(p+' '+r.status);return r.json();}
const MUST_GONE=[
 [5,'all great Neptune’s ocean” cannot wash away'],
 [8,'Malcolm describes Scotland as a place where'],
 [8,'down-fallen birthright'],
 [6,'>simile</dfn> of wading'],
 [6,'barren sceptre in my grip”'],
 [1,'essential For the exam'],
 [2,'Aristotelian structure of tragedy that'],
 [5,'Relating to the religious beliefs and practices'],
 [3,'A direct address to an absent person'],
 [9,'The act of killing oneself, considered a mortal sin'],
 [4,'symbolizes'],[6,'symbolizes'],
];
const MUST_PRESENT=[
 [5,'all the perfumes of Arabia will not sweeten this little hand'],
 [8,'down-fall’n birthdom'],
 [8,'Macduff calls the country their'],
 [6,'>metaphor</dfn> of wading'],
 [6,'barren sceptre in my gripe”'],
 [2,'Seneca'],
 [7,'people “float upon a wild and violent sea.”'],
];
(async()=>{
  const rows=await q(`lessons?unit_id=eq.${UNIT}&select=id,lesson_number,title,content_html,exam_tip_html,conclusion_html,practice_questions,flashcard_questions,glossary_terms,narration_manifest&order=lesson_number`);
  const by=new Map(rows.map(r=>[r.lesson_number,r]));
  let fail=0;
  console.log('--- removed strings ---');
  for(const [n,s] of MUST_GONE){const h=by.get(n).content_html; const hit=h.includes(s); console.log(`${hit?'FAIL':'ok  '} L${n}: "${s.slice(0,50)}"`); if(hit)fail++;}
  console.log('--- required strings ---');
  for(const [n,s] of MUST_PRESENT){const h=by.get(n).content_html; const hit=h.includes(s); console.log(`${hit?'ok  ':'FAIL'} L${n}: "${s.slice(0,50)}"`); if(!hit)fail++;}

  console.log('--- practice question band integrity ---');
  let dup=0,mis=0,mis4=0;
  for(const r of rows) for(const pq of r.practice_questions){
    const m=pq.marks||'';
    if((m.match(/Top band/g)||[]).length>1){dup++;console.log(`FAIL dupTop L${r.lesson_number}`);}
    if(/^30 marks/.test(pq.type)&&/\(10-12\)/.test(m)){mis++;console.log(`FAIL 30/12 L${r.lesson_number}`);}
    if(/^4 marks/.test(pq.type)&&/^6 marks:/m.test(m)){mis4++;console.log(`FAIL 4/6 L${r.lesson_number}`);}
  }
  console.log(`dupTopBand=${dup}  type30-band12=${mis}  type4-band6=${mis4}`); fail+=dup+mis+mis4;

  console.log('--- narration manifest integrity (every narrated id has a clip) ---');
  for(const r of rows){
    const html=(r.content_html||'')+(r.exam_tip_html||'')+(r.conclusion_html||'');
    const ids=[...html.matchAll(/data-narration-id="([^"]+)"/g)].map(m=>m[1]);
    const man=new Set((r.narration_manifest||[]).map(e=>e.id));
    const missing=ids.filter(i=>!man.has(i));
    const orphan=[...man].filter(i=>!ids.includes(i));
    const bad=(r.narration_manifest||[]).filter(e=>!e.src||!/^https:\/\/pub-.*\.mp3$/.test(e.src));
    console.log(`${missing.length||orphan.length||bad.length?'FAIL':'ok  '} L${String(r.lesson_number).padStart(2,'0')}  ids=${ids.length} manifest=${man.size} missing=${missing.length} orphan=${orphan.length} badsrc=${bad.length}`);
    fail+=missing.length+orphan.length+bad.length;
  }
  console.log('--- entity / board sweep (post-fix) ---');
  const ENT=/&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5});/g, BD=/\b(Edexcel|OCR|Eduqas|WJEC)\b/g;
  for(const r of rows){
    const j=JSON.stringify([r.practice_questions,r.knowledge_checks,r.flashcard_questions,r.glossary_terms]);
    const e=j.match(ENT), b=(j+r.content_html).match(BD);
    if(e){console.log(`FAIL entity L${r.lesson_number}`,[...new Set(e)]);fail++;}
    if(b){console.log(`FAIL board L${r.lesson_number}`,[...new Set(b)]);fail++;}
  }
  console.log(`\n=== VERIFY ${fail===0?'PASS':'FAIL ('+fail+')'} ===`);
  const bk=JSON.parse(fs.readFileSync('scripts/_retrofc/_pilot_macbeth_backup.json','utf8'));
  console.log(`backup: ${bk.lessons.length} lessons, fields=${bk.lessons.reduce((a,l)=>a+l.fields_changed.length,0)}, bytes=${fs.statSync('scripts/_retrofc/_pilot_macbeth_backup.json').size}`);
})();
