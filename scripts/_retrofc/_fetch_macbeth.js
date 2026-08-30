const URL = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_KEY;
async function q(path){
  const r = await fetch(`${URL}/rest/v1/${path}`, {headers:{apikey:KEY, Authorization:`Bearer ${KEY}`}});
  if(!r.ok) throw new Error(path+' -> '+r.status+' '+await r.text());
  return r.json();
}
(async()=>{
  const all = await q(`units?subject_id=eq.ebecab63-5c56-4c4c-9393-9c3fd335f8a1&select=id,slug,name,sort_order,lesson_count&order=sort_order`);
  console.log(JSON.stringify(all,null,1));
  const l = await q(`lessons?select=*&limit=1`);
  console.log('LESSON COLS:', Object.keys(l[0]).join(', '));
})();
