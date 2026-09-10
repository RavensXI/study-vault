/* welcome-live.js — the two homepage sections that show the real product
   instead of a picture of it: a live lesson (or workbook) from the library on
   the tablet, and the catalogue as a painted bookshelf. Both fetch with the
   public anon key and paint the baked copy in js/welcome-fallback.js first,
   so neither is ever empty. */
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

  /* ================= 1. a real lesson, live, on the tablet ================= */
  /* One curated lesson per painted subject family: chosen for a striking hero
     photograph and a strong opening (8 Sep 2026). */
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
    hsc:       {s:'health-social-care-ocr',u:'principles-of-care',n:1,name:'Health & Social Care'},
    /* workbook (practice-first) subjects: the tablet shows the real workbook page */
    maths:     {s:'maths-aqa',u:'number',n:1,name:'GCSE Maths',practice:true},
    lang:      {s:'english-language-aqa',u:'paper-1-reading',n:1,name:'GCSE English Language',practice:true},
    french:    {s:'french-aqa',u:'people-and-lifestyle',n:1,name:'GCSE French',practice:true},
    spanish:   {s:'spanish-aqa',u:'people-and-lifestyle',n:1,name:'GCSE Spanish',practice:true},
    german:    {s:'german-aqa',u:'people-and-lifestyle',n:1,name:'GCSE German',practice:true}
  };
  var DEFAULT='geog';
  var frame=document.getElementById('lessoniframe'), note=document.getElementById('lf-note'),
      openLink=document.getElementById('lf-open'), which=document.getElementById('lf-which'),
      side=document.getElementById('lessonside'), wbnote=document.getElementById('workbooknote');
  var currentKey=null, armed=false, lastToggled=null, ready=false;
  /* `picked` is a top-level const in the page script: global lexical scope, not a window property */
  function pickedKeys(){ try{ return (typeof picked!=='undefined' ? picked : []).slice(); }catch(e){ return []; } }
  /* the subject the visitor touched LAST drives the tablet (ticked on = show it);
     otherwise their latest non-core pick; the four pre-ticked cores never do
     on their own, so the default stays until they choose. */
  var CORE={maths:1,lang:1,lit:1,science:1};
  function lessonKey(){
    var ks=pickedKeys();
    if(lastToggled && ks.indexOf(lastToggled)>=0 && LESSONS[lastToggled]) return lastToggled;
    for(var i=ks.length-1;i>=0;i--){ if(!CORE[ks[i]] && LESSONS[ks[i]]) return ks[i]; }
    return DEFAULT;
  }
  function ordinal(n){ return ['one','two','three','four','five','six'][n-1]||String(n); }
  function unitName(u){ return u.replace(/-/g,' ').replace(/\b(paper|aos)\s*(\d)/i,function(m,a,b){ return a[0].toUpperCase()+a.slice(1)+' '+b; }); }
  function setFrame(key){
    if(!frame||key===currentKey) return;
    var L=LESSONS[key]; currentKey=key; ready=false; openTarget=null; syncPressed();
    var path='/'+(L.practice?'practice':'lesson')+'/'+L.s+'/'+L.u+'/'+L.n;
    if(openLink){ openLink.href=path; openLink.textContent=(L.practice?'Open this workbook':'Open this lesson')+' →'; }
    if(which) which.textContent=L.name+', '+(L.practice?'workbook':'lesson')+' '+ordinal(L.n);
    if(side){ side.classList.toggle('workbook',!!L.practice); }
    if(wbnote) wbnote.hidden=!L.practice;
    document.querySelectorAll('.showme[data-target]').forEach(function(b){ b.setAttribute('aria-disabled',L.practice?'true':'false'); });
    if(note){ note.classList.toggle('workbook',!!L.practice); note.textContent='Loading '+L.name+'…'; }
    frame.src=path+'?embed=1';
  }
  function caption(L,title){
    if(L.practice) return L.name+' is a workbook subject — '+(title?'“'+title+'”: ':'')+'type an answer and it marks you. No narration or flashcards here; those belong to reading subjects.';
    return (title?'“'+title+'” — ':'')+L.name+', '+unitName(L.u)+', lesson '+ordinal(L.n)+'. The real page, live from the library: scroll it, or press one of the five.';
  }
  /* the frame reports when the real page has rendered, and what state it is in */
  var openTarget=null;
  function syncPressed(){
    document.querySelectorAll('.showme[data-target]').forEach(function(b){ b.setAttribute('aria-pressed',b.dataset.target===openTarget?'true':'false'); });
  }
  var STATE_NOTE={
    kc:{on:'The five-question knowledge check is open on the tablet. Press again to close it.',off:'No knowledge check on this one.'},
    flashcards:{on:'Flashcards are open on the tablet. Press again to close them.',off:'No flashcards on this one.'},
    narration:{on:'Playing — the narration reads the lesson aloud and follows along on the page. Press again to pause.',off:'The narration could not start on this one.',paused:'Paused. Press again to carry on.'},
    practice:{on:'Six practice questions in the exam’s own style, open on the tablet. Answer one and the tutor marks it. Press again to close.',off:'No practice questions on this one.'},
    lesson:{on:'The lesson itself — written to the specification, with a real photograph.',off:''}
  };
  addEventListener('message',function(e){
    if(e.origin!==location.origin) return;
    var d=e.data||{}; if(!currentKey) return; var L=LESSONS[currentKey];
    if(d.type==='sv-embed-ready'){ ready=true; if(note) note.textContent=caption(L,d.title||''); }
    if(d.type==='sv-embed-state'){
      var t=d.target, s=STATE_NOTE[t]||{};
      openTarget=(d.open && t!=='lesson')? t : null;
      syncPressed();
      if(note) note.textContent=(d.open? s.on : (d.closed? caption(L,'') : (d.paused? s.paused : s.off)))||caption(L,'');
    }
  });
  /* five captions = five controls that move the real page inside the frame.
     Pressing the same one again closes what it opened (quiz, cards, narration). */
  document.querySelectorAll('.showme[data-target]').forEach(function(b){
    b.setAttribute('aria-pressed','false');
    b.addEventListener('click',function(){
      if(!currentKey) setFrame(lessonKey());
      var L=LESSONS[currentKey]; if(L.practice){ if(note) note.textContent=caption(L,''); return; }
      var send=function(){ try{ frame.contentWindow.postMessage({type:'sv-embed-show',target:b.dataset.target},location.origin); }catch(e){} };
      if(ready) send(); else { var n=0, w=setInterval(function(){ if(ready||++n>60){ clearInterval(w); if(ready) send(); } },100); }
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
  function onPickChange(slug){ lastToggled=slug; if(!armed){ arm(); return; } clearTimeout(swapTimer); swapTimer=setTimeout(function(){ setFrame(lessonKey()); },350); }
  if(typeof window.togglePick==='function'){
    var _tp=window.togglePick;
    window.togglePick=function(slug){ var r=_tp.apply(this,arguments); onPickChange(slug); return r; };
  }

  /* ================= 2. the catalogue: a painted bookshelf ================= */
  /* welcome's family slug -> the browse base slug. A live row belongs to the
     family when its slug is the base or starts with base + '-'. */
  var FAMILY={maths:'maths',lang:'english-language',lit:'english-literature',science:'science',triple:'separate-sciences',
    history:'history',geog:'geography',french:'french',spanish:'spanish',german:'german',cs:'computer-science',business:'business',
    pe:'physical-education',psych:'psychology',rs:'religious-studies',socio:'sociology',econ:'economics',stats:'statistics',
    media:'media-studies',film:'film-studies',drama:'drama',music:'music',mtech:'music-technology',dt:'design-technology',
    eng:'engineering',electronics:'electronics',it:'it',astro:'astronomy',geology:'geology',classics:'classical-civilisation',
    citizenship:'citizenship',food:'food-preparation-and-nutrition',hosp:'hospitality-catering',hsc:'health-social-care'};
  /* the vocational awards have their own painted spines (Sunburst, 8 Sep 2026) */
  var VOC={'cambridge-nationals-child-development':'child-development','cambridge-nationals-creative-imedia':'creative-imedia',
    'cambridge-nationals-engineering-design':'engineering-design','cambridge-nationals-engineering-manufacture':'engineering-manufacture',
    'cambridge-nationals-engineering-programmable-systems':'programmable-systems','cambridge-nationals-enterprise-and-marketing':'enterprise-marketing',
    'cambridge-nationals-sport-science':'sport-science','cambridge-nationals-sport-studies':'sport-studies',
    'l12-construction-built-environment':'construction','l12-ict':'ict','l12-retail-business':'retail-business','l12-sport-and-coaching-principles':'sport-coaching'};
  var VOC_LABEL={'cambridge-nationals-':'Cambridge National','l12-':'Level 1/2 Award'};
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
    rows.filter(function(r){ return !used[r.slug] && VOC[r.slug]; }).forEach(function(r){
      var pre=Object.keys(VOC_LABEL).filter(function(p){return r.slug.indexOf(p)===0;})[0];
      fams.push({key:VOC[r.slug],name:r.name,voc:VOC_LABEL[pre],art:'assets/lw/shelf/book_'+VOC[r.slug]+'.webp',boards:[{label:boardLabel(r.board),slug:r.slug}]});
    });
    return fams;
  }
  function hashv(s){ var h=0; for(var i=0;i<s.length;i++) h=(h*31+s.charCodeAt(i))>>>0; return (0.93+(h%13)/100).toFixed(2); }
  function propEl(name){ var p=document.createElement('span'); p.className='prop prop-'+name; p.innerHTML='<img draggable="false" src="assets/lw/shelf/prop_'+name+'.webp" alt="">'; return p; }
  function bookendEl(mirror){ var be=document.createElement('img'); be.className='bookend'+(mirror?' mirror':''); be.src='assets/lw/shelf/'+(mirror?'bookend2_marble.png':'bookend2.webp'); be.alt=''; return be; }
  var current=null, tip=document.getElementById('booktip');
  function renderCatalogue(rows){
    var host=document.getElementById('catshelves'), panel=document.getElementById('catboards'), sub=document.getElementById('catsub');
    if(!host||!panel) return;
    var fams=group(rows);
    if(sub) sub.textContent=fams.length+' subjects across '+rows.length+' board specifications. Tap a book to see its boards and go straight in.';
    host.innerHTML=''; current=null; panel.hidden=true;
    var half=Math.ceil(fams.length/2), rowsOf=[fams.slice(0,half),fams.slice(half)];
    var PROPS=[['@bookstack',null],[null,'@owl']]; /* [leading, trailing] per row */
    rowsOf.forEach(function(list,ri){
      var row=document.createElement('div'); row.className='catrow';
      var shelf=document.createElement('div'); shelf.className='shelf';
      var bks=document.createElement('span'); bks.className='bks';
      if(ri===0) bks.appendChild(bookendEl(false));
      if(PROPS[ri][0]) bks.appendChild(propEl(PROPS[ri][0].slice(1)));
      list.forEach(function(f,i){
        var b=document.createElement('button'); b.type='button'; b.className='bk'; b.dataset.key=f.key;
        b.setAttribute('aria-expanded','false'); b.setAttribute('aria-label',f.name+(f.voc?' ('+f.voc+')':''));
        b.style.setProperty('--vf',hashv(f.key));
        var n=list.length, lean=0, shift=0;
        if(typeof leanFor==='function'){ lean=leanFor(i,n,false); shift=shiftFor(i,n,false); }
        b.style.setProperty('--lean',lean+'deg'); b.style.setProperty('--shift',shift+'px');
        b.innerHTML='<img draggable="false" src="'+f.art+'" alt="">';
        b.addEventListener('click',function(){ open(f,b,panel); });
        b.addEventListener('mouseenter',function(){ showTip(f,b); });
        b.addEventListener('mouseleave',function(){ if(tip) tip.classList.remove('on'); });
        bks.appendChild(b);
      });
      if(PROPS[ri][1]) bks.appendChild(propEl(PROPS[ri][1].slice(1)));
      if(ri===rowsOf.length-1) bks.appendChild(bookendEl(true));
      shelf.appendChild(bks); row.appendChild(shelf);
      var lw=document.createElement('div'); lw.className='ledgewrap'; lw.innerHTML='<img class="ledge" src="assets/lw/shelf/ledge_strip.webp" alt="">';
      row.appendChild(lw); host.appendChild(row);
    });
  }
  function showTip(f,b){
    var stage=document.getElementById('stage-landing'); if(!tip||!stage) return;
    var r=b.getBoundingClientRect(), sr=stage.getBoundingClientRect(), z=window.__svz||1;
    tip.innerHTML='<span class="tn">'+esc(f.name)+'</span><span class="tb">'+esc((f.voc?f.voc+' · ':'')+f.boards.map(function(x){return x.label;}).join(' · '))+'</span>';
    tip.style.left=((r.left+r.width/2-sr.left)/z)+'px'; tip.style.top=((r.top-sr.top+4)/z)+'px';
    tip.classList.add('on');
  }
  function open(f,btn,panel){
    var host=document.getElementById('catshelves');
    host.querySelectorAll('.bk[aria-expanded="true"]').forEach(function(t){ t.setAttribute('aria-expanded','false'); });
    if(current===f.key){ current=null; panel.hidden=true; return; }
    current=f.key; btn.setAttribute('aria-expanded','true');
    panel.hidden=false;
    panel.innerHTML='<div class="cb-head"><img src="'+f.art+'" alt=""><b>'+esc(f.name)+'</b>'
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
