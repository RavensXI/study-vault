/* welcome-live.js — the two homepage sections that show the real product
   instead of a picture of it: a live lesson from the library, and the
   catalogue as a tappable grid. Both fetch with the public anon key and paint
   the baked copy in js/welcome-fallback.js first, so neither is ever empty. */
(function(){
  var SB_URL='https://baipckgywpnwapobwtsy.supabase.co';
  var SB_KEY='sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';
  var H={apikey:SB_KEY,Authorization:'Bearer '+SB_KEY};
  var LIB=window.SV_LIB||{SUBJECTS:[]};
  var FB=window.SV_FALLBACK||{};
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function get(path){
    return fetch(SB_URL+'/rest/v1/'+path,{headers:H}).then(function(r){ if(!r.ok) throw new Error(String(r.status)); return r.json(); });
  }

  /* ================= 1. a real lesson, live, in a frame ================= */
  /* One curated lesson per painted subject family: chosen for a striking hero
     photograph and a strong opening (8 Sep 2026). Practice-format families
     (maths, English Language, the languages) have no entry and fall back. */
  var LESSONS={
    geog:      {s:'geography-aqa',u:'paper-1',n:1,name:'GCSE Geography'},
    history:   {s:'history-aqa',u:'germany-democracy-dictatorship',n:1,name:'GCSE History'},
    science:   {s:'science-aqa',u:'biology-paper-1',n:1,name:'GCSE Combined Science'},
    triple:    {s:'separate-sciences',u:'biology-paper-1',n:1,name:'GCSE Biology'},
    lit:       {s:'english-literature-aqa',u:'macbeth',n:1,name:'GCSE English Literature'},
    business:  {s:'business-aqa',u:'business-real-world',n:1,name:'GCSE Business'},
    cs:        {s:'computer-science-aqa',u:'algorithms',n:1,name:'GCSE Computer Science'},
    pe:        {s:'physical-education-aqa',u:'human-body-and-movement',n:1,name:'GCSE Physical Education'},
    psych:     {s:'psychology-aqa',u:'memory',n:1,name:'GCSE Psychology'},
    rs:        {s:'religious-studies-aqa',u:'christianity-beliefs',n:1,name:'GCSE Religious Studies'},
    socio:     {s:'sociology-aqa',u:'studying-society-research-methods',n:1,name:'GCSE Sociology'},
    econ:      {s:'economics-aqa',u:'economic-foundations-and-resource-allocation',n:1,name:'GCSE Economics'},
    stats:     {s:'statistics-aqa',u:'planning-designing-enquiry',n:1,name:'GCSE Statistics'},
    media:     {s:'media-studies-aqa',u:'media-language',n:1,name:'GCSE Media Studies'},
    film:      {s:'film-studies-eduqas',u:'film-form-and-language',n:1,name:'GCSE Film Studies'},
    drama:     {s:'drama-aqa',u:'theatre-roles-stagecraft',n:1,name:'GCSE Drama'},
    music:     {s:'music-aqa',u:'aos1-western-classical',n:1,name:'GCSE Music'},
    mtech:     {s:'music-technology',u:'music-business',n:1,name:'Music Technology'},
    dt:        {s:'design-technology',u:'core-technical',n:1,name:'GCSE Design & Technology'},
    eng:       {s:'engineering-aqa',u:'engineering-materials',n:1,name:'GCSE Engineering'},
    electronics:{s:'electronics-eduqas',u:'discovering-electronics',n:1,name:'GCSE Electronics'},
    it:        {s:'it-ocr',u:'it-in-the-digital-world',n:1,name:'IT'},
    astro:     {s:'astronomy-edexcel',u:'naked-eye-astronomy',n:1,name:'GCSE Astronomy'},
    geology:   {s:'geology-eduqas',u:'rocks-and-minerals',n:1,name:'GCSE Geology'},
    classics:  {s:'classical-civilisation-ocr',u:'greek-and-roman-mythology',n:1,name:'GCSE Classical Civilisation'},
    citizenship:{s:'citizenship-aqa',u:'politics-participation-active-citizenship',n:1,name:'GCSE Citizenship'},
    food:      {s:'food-preparation-and-nutrition-aqa',u:'food-nutrition-and-health',n:1,name:'GCSE Food Preparation & Nutrition'},
    hosp:      {s:'hospitality-catering',u:'the-hospitality-and-catering-industry',n:1,name:'Hospitality & Catering'},
    hsc:       {s:'health-social-care-ocr',u:'principles-of-care',n:1,name:'Health & Social Care'}
  };
  var DEFAULT='geog';
  var frame=document.getElementById('lessoniframe'), kicker=document.getElementById('lf-kicker'),
      openLink=document.getElementById('lf-open'), which=document.getElementById('lf-which');
  var currentKey=null, armed=false;
  /* `picked` is a top-level const in the page script: global lexical scope, not a window property */
  function pickedKeys(){ try{ return (typeof picked!=='undefined' ? picked : []).slice(); }catch(e){ return []; } }
  /* the visitor's LATEST option drives the frame; the four pre-ticked cores
     (maths, English x2, science) never do, so the default stays until they choose */
  var CORE={maths:1,lang:1,lit:1,science:1};
  function lessonKey(){
    var ks=pickedKeys();
    for(var i=ks.length-1;i>=0;i--){ if(!CORE[ks[i]] && LESSONS[ks[i]]) return ks[i]; }
    return DEFAULT;
  }
  function ordinal(n){ return ['one','two','three','four','five','six'][n-1]||String(n); }
  function setFrame(key){
    if(!frame||key===currentKey) return;
    var L=LESSONS[key]; currentKey=key;
    var path='/lesson/'+L.s+'/'+L.u+'/'+L.n;
    if(kicker) kicker.textContent=L.name+' · Lesson '+L.n+' · loading…';
    if(openLink) openLink.href=path;
    if(which) which.textContent=L.name+', lesson '+ordinal(L.n);
    frame.src=path+'?embed=1';
  }
  /* the frame reports when the real lesson has rendered */
  addEventListener('message',function(e){
    if(e.origin!==location.origin) return;
    var d=e.data||{};
    if(d.type==='sv-embed-ready' && currentKey){ var L=LESSONS[currentKey]; if(kicker) kicker.textContent=L.name+' · Lesson '+L.n+' · '+(d.title||''); }
  });
  /* five captions = five controls that move the real page inside the frame */
  document.querySelectorAll('.showme[data-target]').forEach(function(b){
    b.addEventListener('click',function(){
      if(!currentKey) setFrame(lessonKey());
      var send=function(){ try{ frame.contentWindow.postMessage({type:'sv-embed-show',target:b.dataset.target},location.origin); }catch(e){} };
      send();
      frame.scrollIntoView({block:'nearest'});
    });
  });
  /* lazy: create the frame when the section approaches; then follow the picker */
  function arm(){
    if(armed) return; armed=true; setFrame(lessonKey());
  }
  var sec=document.getElementById('sec-inside');
  if(sec && 'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ if(es.some(function(x){return x.isIntersecting;})){ arm(); io.disconnect(); } },{rootMargin:'800px 0px'});
    io.observe(sec);
    /* belt and braces: the zoomed canvas can confuse the observer's rects */
    addEventListener('scroll',function onS(){ if(window.scrollY>120){ arm(); removeEventListener('scroll',onS); } },{passive:true});
    setTimeout(function(){ if(!armed && sec.getBoundingClientRect().top<innerHeight*2) arm(); },1500);
  } else arm();
  var swapTimer=null;
  function onPickChange(){ if(!armed){ arm(); return; } clearTimeout(swapTimer); swapTimer=setTimeout(function(){ setFrame(lessonKey()); },350); }
  if(typeof window.togglePick==='function'){
    var _tp=window.togglePick;
    window.togglePick=function(slug){ var r=_tp.apply(this,arguments); onPickChange(); return r; };
  }

  /* ================= 2. the catalogue, tappable ================= */
  /* welcome's family slug -> the browse base slug. A live row belongs to the
     family when its slug is the base or starts with base + '-'. */
  var FAMILY={maths:'maths',lang:'english-language',lit:'english-literature',science:'science',triple:'separate-sciences',
    history:'history',geog:'geography',french:'french',spanish:'spanish',german:'german',cs:'computer-science',business:'business',
    pe:'physical-education',psych:'psychology',rs:'religious-studies',socio:'sociology',econ:'economics',stats:'statistics',
    media:'media-studies',film:'film-studies',drama:'drama',music:'music',mtech:'music-technology',dt:'design-technology',
    eng:'engineering',electronics:'electronics',it:'it',astro:'astronomy',geology:'geology',classics:'classical-civilisation',
    citizenship:'citizenship',food:'food-preparation-and-nutrition',hosp:'hospitality-catering',hsc:'health-social-care'};
  var VOC_LABEL={'cambridge-nationals-':'Cambridge National','l12-':'Level 1/2 Award'};
  var VOC_SHORT={'Cambridge National':'CN','Level 1/2 Award':'L1/2'};
  function boardLabel(b){ return ({'Eduqas / WJEC':'Eduqas','Pearson Edexcel':'Edexcel'})[b]||b||''; }
  function inFamily(slug,base){ return slug===base||slug.indexOf(base+'-')===0; }
  function group(rows){
    var fams=[], used={};
    LIB.SUBJECTS.forEach(function(s){
      var base=FAMILY[s.slug]; if(!base) return;
      var mine=rows.filter(function(r){ return inFamily(r.slug,base); });
      mine.forEach(function(r){ used[r.slug]=1; });
      if(mine.length) fams.push({key:s.slug,name:s.name,c:s.c,art:'assets/lw/shelf/book_'+s.slug+'.webp',
        boards:mine.map(function(r){return {label:boardLabel(r.board),slug:r.slug};})});
    });
    /* vocational awards live outside the painted library: list them plainly */
    rows.filter(function(r){ return !used[r.slug] && (r.slug.indexOf('cambridge-nationals-')===0||r.slug.indexOf('l12-')===0); })
      .forEach(function(r){
        var pre=Object.keys(VOC_LABEL).filter(function(p){return r.slug.indexOf(p)===0;})[0];
        fams.push({key:r.slug,name:r.name,voc:VOC_LABEL[pre],boards:[{label:boardLabel(r.board),slug:r.slug}]});
      });
    return fams;
  }
  var current=null;
  function renderCatalogue(rows){
    var grid=document.getElementById('catgrid'), panel=document.getElementById('catboards'), sub=document.getElementById('catsub');
    if(!grid||!panel) return;
    var fams=group(rows);
    if(sub) sub.textContent=fams.length+' subjects across '+rows.length+' board specifications. Tap one to see its boards and go straight in.';
    grid.innerHTML=''; current=null; panel.hidden=true;
    fams.forEach(function(f,i){
      var b=document.createElement('button'); b.type='button'; b.className='ctile'+(f.voc?' voc':''); b.setAttribute('aria-expanded','false');
      if(f.c) b.style.setProperty('--tc',f.c);
      var n=f.boards.length;
      b.innerHTML=(f.art?'<img src="'+f.art+'" alt="">':'<span class="cvoc" title="'+esc(f.voc)+'">'+esc(VOC_SHORT[f.voc]||f.voc)+'</span>')
        +'<span class="cname">'+esc(f.name)+'</span><span class="cn">'+n+(n===1?' board':' boards')+'</span>';
      b.addEventListener('click',function(){ open(i,fams,grid,panel,b); });
      grid.appendChild(b);
    });
  }
  function open(i,fams,grid,panel,tile){
    var f=fams[i];
    grid.querySelectorAll('.ctile').forEach(function(t){ t.setAttribute('aria-expanded','false'); t.classList.remove('on'); });
    if(current===i){ current=null; panel.hidden=true; return; }
    current=i; tile.setAttribute('aria-expanded','true'); tile.classList.add('on');
    panel.hidden=false;
    panel.innerHTML='<div class="cb-head">'+(f.art?'<img src="'+f.art+'" alt="">':'')+'<b>'+esc(f.name)+'</b>'
      +(f.voc?'<span class="cb-voc">'+esc(f.voc)+'</span>':'')+'</div>'
      +'<div class="cb-boards">'+f.boards.map(function(b){
        return '<a class="cb-board" href="/browse/'+esc(b.slug)+'"><span class="cb-lbl">'+esc(b.label)+'</span><span class="cb-go">Open &rarr;</span></a>';
      }).join('')+'</div>';
    var r=panel.getBoundingClientRect(); if(r.bottom>innerHeight) panel.scrollIntoView({block:'nearest',behavior:'smooth'});
  }
  function loadCatalogue(){
    if(FB.catalogue) renderCatalogue(FB.catalogue);
    get('subjects?school_id=is.null&status=eq.live&select=slug,name,exam_board&order=slug').then(function(rows){
      if(!rows||!rows.length) return;
      renderCatalogue(rows.map(function(r){ return {slug:r.slug,name:r.name,board:r.exam_board}; }));
    }).catch(function(){});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',loadCatalogue);
  else loadCatalogue();
})();
