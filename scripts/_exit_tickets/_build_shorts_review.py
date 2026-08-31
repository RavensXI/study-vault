# Build a local QA page for the most RECENT shorts (the live feed is shuffled,
# so it surfaces old clips first). One player + a newest-first playlist: 200+
# <video> elements in one page hits Chrome's media-element cap and none load.
import html
import json
import urllib.parse
import urllib.request

OUT = r'C:\Users\tshau\Documents\Study Vault\.claude\worktrees\exit-tickets\_shorts_review.html'
DAYS = 4
H = {'User-Agent': 'Mozilla/5.0'}

d = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://www.studyvault.co.uk/data/_shorts_manifest.json', headers=H), timeout=90).read())
items = d if isinstance(d, list) else (d.get('items') or d.get('shorts') or [])
items = [i for i in items if i.get('created_at')]
items.sort(key=lambda i: i['created_at'], reverse=True)
days = sorted({i['created_at'][:10] for i in items}, reverse=True)[:DAYS]
sel = [i for i in items if i['created_at'][:10] in days]
print('including', len(sel), 'clips from', days)

data = [{
    'u': '/r2/' + urllib.parse.quote(i['url'], safe=''),   # same-origin proxy
    'raw': i['url'],
    't': i.get('topic') or i.get('title') or '',
    's': i['subject'], 'un': i['unit'], 'n': i['lesson_number'],
    'd': i['created_at'][:10], 'tm': i['created_at'][11:16],
} for i in sel]

page = '''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<title>Shorts QA — newest generations</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,800&display=swap" rel="stylesheet">
<style>
 *{box-sizing:border-box;margin:0;padding:0}
 body{background:#faf8f5;color:#2d2a26;font-family:Inter,system-ui,sans-serif;line-height:1.55}
 .top{padding:1.4rem 1.5rem .9rem;border-bottom:1px solid #e8e4df;background:#fff}
 h1{font-family:'Source Serif 4',Georgia,serif;font-size:1.5rem}
 .stand{color:#6b6560;font-size:.9rem;margin-top:.25rem;max-width:78ch}
 .layout{display:grid;grid-template-columns:minmax(300px,380px) 1fr;gap:1.5rem;padding:1.5rem;align-items:start}
 .player{position:sticky;top:1.5rem}
 video{width:100%;border-radius:14px;background:#000;aspect-ratio:9/16;max-height:74vh;
       box-shadow:0 6px 26px rgba(45,42,38,.18)}
 .nowplaying{margin-top:.7rem;font-size:.9rem;font-weight:600;min-height:2.4em}
 .np-sub{font-size:.75rem;color:#9b9590;font-weight:400;margin-top:.15rem}
 .pbtns{display:flex;gap:.5rem;margin-top:.7rem;flex-wrap:wrap}
 .btn{font:inherit;font-size:.8rem;font-weight:600;padding:.45rem .85rem;border:1px solid #e8e4df;
      background:#fff;border-radius:10px;cursor:pointer;color:#2d2a26;text-decoration:none}
 .btn:hover{border-color:#c06325;color:#c06325}
 .btn.primary{background:#2d2a26;color:#fff;border-color:#2d2a26}
 .filters{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem}
 .f{font:inherit;font-size:.82rem;font-weight:600;padding:.35rem .75rem;border:1px solid #e8e4df;
    background:#fff;border-radius:10px;cursor:pointer}
 .f.on{background:#2d2a26;color:#fff;border-color:#2d2a26}
 .row{display:flex;gap:.8rem;align-items:baseline;padding:.6rem .8rem;border-bottom:1px solid #f0ece7;
      cursor:pointer;border-radius:8px}
 .row:hover{background:#fff}
 .row.on{background:#fff;box-shadow:inset 3px 0 0 #c06325}
 .row .tm{font-size:.72rem;color:#c06325;font-weight:600;font-variant-numeric:tabular-nums;flex-shrink:0;width:3.2rem}
 .row .tp{font-size:.87rem;font-weight:500;flex:1}
 .row .sb{font-size:.72rem;color:#9b9590;flex-shrink:0}
 .count{font-size:.85rem;color:#6b6560;margin-bottom:.6rem}
 @media(max-width:860px){.layout{grid-template-columns:1fr}.player{position:static}}
</style></head><body>
<div class="top">
  <h1>Shorts QA &mdash; newest generations first</h1>
  <p class="stand">The live feed is shuffled, so it shows older clips first. This is ordered by generation time, newest at the top. Click any row to play it. <strong>Jump to ending</strong> skips to the last 6 seconds, where the untrimmed Gemini&nbsp;Notebook endcard sits.</p>
</div>
<div class="layout">
  <div class="player">
    <video id="v" controls playsinline preload="metadata"></video>
    <div class="nowplaying" id="np">Select a clip &rarr;</div>
    <div class="pbtns">
      <button class="btn primary" id="end">Jump to ending</button>
      <button class="btn" id="next">Next clip</button>
      <a class="btn" id="lesson" target="_blank" rel="noopener">Open lesson</a>
    </div>
  </div>
  <div>
    <div class="filters" id="filters"></div>
    <div class="count" id="count"></div>
    <div id="list"></div>
  </div>
</div>
<script>
const DATA = __DATA__;
const v=document.getElementById('v'), np=document.getElementById('np'),
      list=document.getElementById('list'), fw=document.getElementById('filters');
let cur=-1, view=[];
function play(i){
  cur=i; const c=view[i];
  v.src=c.u; v.load(); v.play().catch(()=>{});
  np.innerHTML=c.t+'<div class="np-sub">'+c.s+' &middot; '+c.un+' &middot; L'+c.n+' &middot; made '+c.tm+' on '+c.d+'</div>';
  document.getElementById('lesson').href='https://www.studyvault.co.uk/lesson/'+c.s+'/'+c.un+'/'+c.n;
  [...list.children].forEach((r,j)=>r.classList.toggle('on',j===i));
}
document.getElementById('end').onclick=()=>{
  const go=()=>{v.currentTime=Math.max(0,(v.duration||0)-6);v.play();};
  if(v.readyState>0) go(); else v.addEventListener('loadedmetadata',go,{once:true});
};
document.getElementById('next').onclick=()=>{ if(cur+1<view.length) play(cur+1); };
v.addEventListener('ended',()=>{ if(cur+1<view.length) play(cur+1); });
function render(day){
  view = day==='all' ? DATA : DATA.filter(c=>c.d===day);
  list.innerHTML='';
  view.forEach((c,i)=>{
    const r=document.createElement('div'); r.className='row';
    r.innerHTML='<span class="tm">'+c.tm+'</span><span class="tp">'+c.t+
                '</span><span class="sb">'+c.s+' L'+c.n+'</span>';
    r.onclick=()=>play(i); list.appendChild(r);
  });
  document.getElementById('count').textContent=view.length+' clips';
  [...fw.children].forEach(b=>b.classList.toggle('on',b.dataset.d===day));
  if(view.length) play(0);
}
const days=[...new Set(DATA.map(c=>c.d))];
[['all','All']].concat(days.map(d=>[d,d])).forEach(p=>{
  const b=document.createElement('button'); b.className='f'; b.dataset.d=p[0]; b.textContent=p[1];
  b.onclick=()=>render(p[0]); fw.appendChild(b);
});
render(days[0]);
</script></body></html>'''.replace('__DATA__', json.dumps(data))

open(OUT, 'w', encoding='utf-8').write(page)
print('written', OUT, len(page) // 1024, 'KB')
