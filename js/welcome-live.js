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

  /* ================= 1. a real lesson, live ================= */
  var LESSON={subject:'geology-eduqas',unit:'rocks-and-minerals',n:1,kicker:'GCSE Geology · Rocks and Minerals · Lesson 1'};
  function firstBlocks(html,n){
    var parts=html.split(/(?=<h2\b)/).filter(function(p){return /^\s*<h2/.test(p);}).slice(0,n);
    return parts.map(function(p){
      p=p.replace(/\s*data-narration-id="[^"]*"/g,'').replace(/<dfn[^>]*>([\s\S]*?)<\/dfn>/g,'<b class="term">$1</b>');
      var segs=p.match(/<h2>[\s\S]*?<\/h2>|<p>[\s\S]*?<\/p>/g)||[];
      return segs.slice(0,2).join('');
    }).join('');
  }
  function renderLesson(d){
    var host=document.getElementById('livelesson'); if(!host) return;
    var pq=d.pq||{}; var lines=String(pq.text||'').split('\n');
    var stem=lines[0], opts=lines.slice(1).filter(Boolean);
    host.innerHTML=
      '<div class="lp-hero"><img src="'+esc(d.hero)+'" alt="'+esc(d.hero_alt)+'"><span class="plate" aria-hidden="true">1</span></div>'
      +'<div class="lp-body">'
      +'<div class="lp-kicker">'+esc(d.kicker)+'</div>'
      +'<h3 class="lp-title">'+esc(d.title)+'</h3>'
      +'<div class="lp-content">'+d.content+'</div>'
      +'<div class="lp-q"><span class="plate" aria-hidden="true">2</span>'
      +'<div class="lp-qhead">Practice question <span class="lp-qtype">'+esc(pq.type||'')+'</span></div>'
      +'<p class="lp-stem">'+esc(stem)+'</p>'
      +(opts.length?'<ul class="lp-opts">'+opts.map(function(o){return '<li>'+esc(o)+'</li>';}).join('')+'</ul>':'')
      +'<button type="button" class="lp-reveal" aria-expanded="false">Reveal the mark scheme</button>'
      +'<p class="lp-answer" hidden>'+esc(pq.marks||'')+'</p></div>'
      +'<div class="lp-tools">'
      +'<div class="lp-tool"><span class="plate" aria-hidden="true">3</span><b>Knowledge check</b><span>'+esc(d.kc)+' questions</span></div>'
      +'<div class="lp-tool"><span class="plate" aria-hidden="true">4</span><b>Flashcards</b><span>'+esc(d.fc)+' cards</span></div>'
      +'<div class="lp-tool"><span class="plate" aria-hidden="true">5</span><b>Read aloud</b><span>narration + podcast</span></div>'
      +'</div>'
      +'<a class="lp-open" href="'+esc(d.url)+'">Open this lesson &rarr;</a>'
      +'</div>';
    var btn=host.querySelector('.lp-reveal'), ans=host.querySelector('.lp-answer');
    btn.addEventListener('click',function(){ var on=ans.hidden; ans.hidden=!on; btn.setAttribute('aria-expanded',String(on)); btn.textContent=on?'Hide the mark scheme':'Reveal the mark scheme'; });
    host.classList.add('is-ready');
  }
  function loadLesson(){
    if(FB.lesson) renderLesson(FB.lesson);              /* paint the baked copy first: never an empty frame */
    get('subjects?slug=eq.'+LESSON.subject+'&school_id=is.null&select=id').then(function(s){
      if(!s.length) throw new Error('no subject');
      return get('units?subject_id=eq.'+s[0].id+'&slug=eq.'+LESSON.unit+'&select=id');
    }).then(function(u){
      if(!u.length) throw new Error('no unit');
      return get('lessons?unit_id=eq.'+u[0].id+'&lesson_number=eq.'+LESSON.n+'&status=eq.live&select=title,hero_image_url,hero_image_alt,content_html,practice_questions,knowledge_checks,flashcard_questions');
    }).then(function(rows){
      var l=rows&&rows[0]; if(!l||!l.content_html) throw new Error('no lesson');
      renderLesson({title:l.title,hero:l.hero_image_url,hero_alt:l.hero_image_alt||'',content:firstBlocks(l.content_html,2),
        pq:(l.practice_questions||[])[0]||{},kc:(l.knowledge_checks||[]).length,fc:(l.flashcard_questions||[]).length,
        url:'/lesson/'+LESSON.subject+'/'+LESSON.unit+'/'+LESSON.n,kicker:LESSON.kicker});
    }).catch(function(){ /* the baked copy stays up */ });
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

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){ loadLesson(); loadCatalogue(); });
  else { loadLesson(); loadCatalogue(); }
})();
