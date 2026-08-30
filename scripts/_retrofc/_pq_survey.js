const URL=process.env.SUPABASE_URL, KEY=process.env.SUPABASE_SERVICE_KEY;
async function q(p){const r=await fetch(`${URL}/rest/v1/${p}`,{headers:{apikey:KEY,Authorization:`Bearer ${KEY}`}});if(!r.ok)throw new Error(p+' '+r.status+' '+await r.text());return r.json();}
(async()=>{
  const units = await q(`units?subject_id=eq.ebecab63-5c56-4c4c-9393-9c3fd335f8a1&select=id,slug`);
  const byUnit={};
  let totalQ=0, dupTop=0, mismatch30=0, typeCounts={};
  for(const u of units){
    const ls = await q(`lessons?unit_id=eq.${u.id}&select=id,lesson_number,practice_questions`);
    let ud=0, um=0, uq=0;
    for(const l of ls){
      for(const pq of (l.practice_questions||[])){
        totalQ++; uq++;
        typeCounts[pq.type]=(typeCounts[pq.type]||0)+1;
        const m=pq.marks||'';
        if((m.match(/Top band/g)||[]).length>1){dupTop++; ud++;}
        if(/^30 marks/.test(pq.type||'') && /Top band \(10-12\)/.test(m)){mismatch30++; um++;}
      }
    }
    byUnit[u.slug]={q:uq,dupTop:ud,mismatch30:um};
  }
  console.log('TOTAL PQ:',totalQ,' dupTopBand:',dupTop,' type30-vs-12band:',mismatch30);
  console.log('\nPER UNIT:'); for(const [k,v] of Object.entries(byUnit)) if(v.dupTop||v.mismatch30) console.log(` ${k}: q=${v.q} dupTop=${v.dupTop} mismatch30=${v.mismatch30}`);
  console.log('\nTOP TYPES:'); Object.entries(typeCounts).sort((a,b)=>b[1]-a[1]).slice(0,15).forEach(([t,c])=>console.log(`  ${c}\t${t}`));
})();
