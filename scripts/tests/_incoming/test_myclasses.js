const path=require('path');
const REPO='C:/Users/tshau/Documents/Study Vault';
const authPath=require.resolve(path.join(REPO,'api/pipeline/_lib/auth.js'));
let AUTH=null;
require.cache[authPath]={id:authPath,filename:authPath,loaded:true,exports:{requireTeacher:async()=>AUTH}};
const {createClient}=require(path.join(REPO,'node_modules/@supabase/supabase-js'));
const sb=createClient(process.env.SUPABASE_URL,process.env.SUPABASE_SERVICE_KEY);
const h=require(path.join(REPO,'api/teacher/my-classes.js'));
const res=()=>{const r={code:null,body:null};r.status=c=>{r.code=c;return r;};r.json=b=>{r.body=b;return r;};return r;};
(async()=>{
  const {data:t}=await sb.from('profiles').select('id,full_name,role,school_id').eq('id','bd4ab587-db2e-4f41-87e7-69218f51b234').single();
  AUTH={profile:t};
  const r=res(); await h({method:'GET',headers:{},query:{},body:{}},r);
  console.log('teacher:',t.full_name,'->',r.code);
  console.log('classes:',r.body.classes.length);
  r.body.classes.slice(0,5).forEach(c=>console.log('   '+String(c.name).padEnd(7)+' '+c.joinCode+'  '+String(c.size).padStart(2)+' students  '+(c.subject||'no subject')));
  console.log('subjects offered:',r.body.subjects.length);
  console.log('   own-school first:',JSON.stringify(r.body.subjects.slice(0,3)));
})();
