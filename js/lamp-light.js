/* ============ Lamp light: the landing shelf, relit by its reading lamp ============
   The landing page's lamp used to light the room with CSS gradients. This renders the light
   instead. The scene is treated as a shallow 3D box seen from the front: the wall is the plane
   z=0, the books and props are flat cut-outs standing a little in front of it (z = their depth),
   the shelf top runs from the wall out to its front edge, and the lamp's shade is a spotlight
   hanging above them all. From that, with the real cut-out shapes of the painted objects:

   - the wall gets the cone the shade throws: inverse-square falloff, the soft edge of the shade's
     cut-off, a little spill, and a warm bounce off the lit shelf;
   - every object casts a shadow (onto the wall, the shelf top and each other) by tracing rays from
     the surface back to an emitter the size of the shade's mouth, so shadows are sharp at the
     foot of an object and soften with distance, like real ones;
   - every object is shaded by its own shape (normals estimated from its silhouette and paint),
     with a brass sheen on the trophy and a glassy glint on the inkwell;
   - the inside of the shade glows, the bulb blooms, a faint haze hangs in the beam;
   - and, as in a photograph, the eye's reference moves: under the light the camera pulls its
     exposure down a touch (which is what turns a pale wall warm rather than just white), and a
     patch the lamp should reach but can't (a cast shadow, a side turned away) reads darker.
     Nothing the lamp can't reach changes at all.

   Output is a handful of canvases: two over the wallpaper and two over the plank (multiply for
   the darkening, colour-dodge for the light: together exactly surface x gain), one relit copy of
   each object laid over its own image, and one glow sheet in front. welcome.html's CSS fades
   them in and out with the lamp's .lit class. If anything here fails (a canvas that can't be
   read, say, on file://) the page keeps its simpler CSS light. The work is sliced into ~12ms
   pieces so the page never stalls while it draws; window.__lampLight.P holds every dial. */
(function(){
'use strict';

/* ---- the lamp and the room. Lengths are in "lamp px": px at a 330px-tall lamp ---- */
const P={
  mouth:[0.232,0.310],           /* centre of the shade's opening, as fractions of the lamp art */
  bulb:[0.262,0.258],            /* the bulb, up inside the shade */
  rimA:58, rimB:21, rimRot:28,   /* the opening: ellipse semi-axes and tilt (deg) */
  bulbR:15,
  zL:165,                        /* how far out from the wall the shade's mouth is */
  axis:[-0.45,0.82,-0.36],       /* the way the shade points (x right, y down, z out of the wall) */
  inner:30, outer:60, spillTo:84,/* cone half-angles (deg): full beam, the shade's cut-off, spill */
  lip:.14, spill:.07,
  lightR:16,                     /* emitter radius: sets how soft the shadows are */
  R0:240, I0:1.55,                /* irradiance I0 at R0, falling off as 1/r^2 */
  tint:[1.0,0.72,0.42],          /* tungsten, about 2700K, as a gain on each channel */
  kWall:.75, kObj:.72, kPlank:.95, plankLip:.55,
  expo:.7,                       /* local exposure pull-down under the light */
  kShadow:.58, shadowReach:1.6,  /* how dark a blocked patch goes, and how soon full strength */
  bounce:.26, bounceR:340,        /* warm fill bouncing off the lit shelf */
  wrap:.2, round:7, bumpShape:3.2, bumpPaint:1.4,
  haze:.035, bloom:.45,
  dusk:.17, duskTint:[1,1.01,.93],      /* the rest of the page dims this much while the lamp is on */
  duskRx:760, duskRy:430, duskShift:200, duskDrop:120,   /* the lamp's own pool is left alone */
  shelfDepth:240,                /* the wall to the plank's front edge */
  faceFrac:0.315,                /* the plank's top face, as a share of the ledge strip */
  depth:{book:72, bookstack:112, trophy:80, inkwell:118, bookend:60, lamp:150, def:80},
  reachL:980, reachR:330, reachU:420,   /* the working area round the lamp */
  samples:10, steps:10, cell:3, debug:false
};
const MAT={
  book:{kd:1, ks:.10, shin:14, metal:0, bump:1},
  bookstack:{kd:1, ks:.10, shin:14, metal:0, bump:1},
  trophy:{kd:.55, ks:1.25, shin:30, metal:1, bump:1.6},
  inkwell:{kd:.85, ks:1.1, shin:70, metal:0, bump:1.5},
  bookend:{kd:.9, ks:.3, shin:22, metal:0, bump:1},
  lamp:{kd:.6, ks:1.0, shin:26, metal:1, bump:1.4},
  def:{kd:.95, ks:.15, shin:16, metal:0, bump:1}
};

const D2R=Math.PI/180;
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
const sstep=(a,b,x)=>{ const t=clamp((x-a)/(b-a),0,1); return t*t*(3-2*t); };
function norm(v){ const l=Math.hypot(v[0],v[1],v[2])||1; return [v[0]/l,v[1]/l,v[2]/l]; }

/* where an <img> actually is on screen, transforms and zoom included: drop three probes at its
   corners (in its offset parent, the same box its offsets are measured in) and read them back */
function affine(img){
  const par=img.offsetParent; if(!par) return null;
  const L=img.offsetLeft, T=img.offsetTop, W=img.offsetWidth, H=img.offsetHeight;
  if(!W||!H) return null;
  let own=null; const cs=getComputedStyle(img);
  if(cs.transform&&cs.transform!=='none'){
    const o=cs.transformOrigin.split(' ').map(parseFloat);
    own=new DOMMatrix().translate(o[0],o[1]).multiply(new DOMMatrix(cs.transform)).translate(-o[0],-o[1]);
  }
  const mk=(x,y)=>{ const d=document.createElement('i');
    d.style.cssText='position:absolute;display:block;left:'+x+'px;top:'+y+'px;width:0;height:0;margin:0;padding:0;border:0';
    par.appendChild(d); return d; };
  const a=mk(L,T), b=mk(L+W,T), c=mk(L,T+H);
  const ra=a.getBoundingClientRect(), rb=b.getBoundingClientRect(), rc=c.getBoundingClientRect();
  a.remove(); b.remove(); c.remove();
  const M={ox:ra.left, oy:ra.top, ux:(rb.left-ra.left)/W, uy:(rb.top-ra.top)/W,
    vx:(rc.left-ra.left)/H, vy:(rc.top-ra.top)/H, W, H, L, T, par};
  if(own){ /* fold the image's own transform in: local -> own -> parent-box affine */
    const base={...M};
    const map=(u,v)=>{ const p=own.transformPoint(new DOMPoint(u,v));
      return [base.ox+p.x*base.ux+p.y*base.vx, base.oy+p.x*base.uy+p.y*base.vy]; };
    const o=map(0,0), px=map(1,0), py=map(0,1);
    M.ox=o[0]; M.oy=o[1]; M.ux=px[0]-o[0]; M.uy=px[1]-o[1]; M.vx=py[0]-o[0]; M.vy=py[1]-o[1];
  }
  return M;
}
const mapPt=(M,u,v)=>[M.ox+u*M.ux+v*M.vx, M.oy+u*M.uy+v*M.vy];

/* the image's colour filters (saturate, brightness...), baked into our copy of its pixels.
   The canvas's own ctx.filter is the same engine as CSS where it exists; else do it by hand. */
function colourFilters(f){
  const out=[]; let i=0;
  while(i<f.length){
    const m=/([a-z-]+)\(/.exec(f.slice(i)); if(!m) break;
    const start=i+m.index+m[0].length; let depth=1, j=start;
    while(j<f.length&&depth){ if(f[j]==='(') depth++; else if(f[j]===')') depth--; j++; }
    const name=m[1], arg=f.slice(start,j-1).trim();
    if(name!=='drop-shadow'&&name!=='blur'&&name!=='url') out.push(name+'('+arg+')');
    i=j;
  }
  return out;
}
let CTXFILTER=null;
function ctxFilterWorks(){
  if(CTXFILTER!==null) return CTXFILTER;
  try{ const c=document.createElement('canvas').getContext('2d'); c.filter='saturate(2)'; CTXFILTER=c.filter==='saturate(2)'; }
  catch(e){ CTXFILTER=false; }
  return CTXFILTER;
}
function applyFiltersByHand(d,list){
  for(const fn of list){
    const m=/([a-z-]+)\(([^)]*)\)/.exec(fn); if(!m) continue;
    let a=parseFloat(m[2]); if(m[2].trim().endsWith('%')) a/=100; if(isNaN(a)) a=1;
    for(let i=0;i<d.length;i+=4){
      let r=d[i]/255,g=d[i+1]/255,b=d[i+2]/255;
      if(m[1]==='brightness'){ r*=a; g*=a; b*=a; }
      else if(m[1]==='contrast'){ r=(r-.5)*a+.5; g=(g-.5)*a+.5; b=(b-.5)*a+.5; }
      else if(m[1]==='saturate'){
        const R=(.213+.787*a)*r+(.715-.715*a)*g+(.072-.072*a)*b,
              G=(.213-.213*a)*r+(.715+.285*a)*g+(.072-.072*a)*b,
              B=(.213-.213*a)*r+(.715-.715*a)*g+(.072+.928*a)*b; r=R; g=G; b=B; }
      else if(m[1]==='sepia'){ const k=1-a;
        const R=(.393+.607*k)*r+(.769-.769*k)*g+(.189-.189*k)*b,
              G=(.349-.349*k)*r+(.686+.314*k)*g+(.168-.168*k)*b,
              B=(.272-.272*k)*r+(.534-.534*k)*g+(.131+.869*k)*b; r=R; g=G; b=B; }
      d[i]=clamp(r,0,1)*255; d[i+1]=clamp(g,0,1)*255; d[i+2]=clamp(b,0,1)*255;
    }
  }
}
function pixelsOf(img,bw,bh){
  const c=document.createElement('canvas'); c.width=bw; c.height=bh;
  const x=c.getContext('2d',{willReadFrequently:true});
  const list=colourFilters(getComputedStyle(img).filter||'');
  const byCtx=list.length&&ctxFilterWorks();
  if(byCtx) x.filter=list.join(' ');
  x.drawImage(img,0,0,bw,bh);
  const id=x.getImageData(0,0,bw,bh);      /* throws on a tainted canvas: caller falls back */
  if(list.length&&!byCtx) applyFiltersByHand(id.data,list);
  return id;
}
/* separable box blur, run twice (close to a gaussian) */
function blur(src,w,h,r){
  if(r<1) return src.slice();
  let a=src.slice(), b=new Float32Array(src.length);
  for(let pass=0;pass<2;pass++){
    for(let y=0;y<h;y++){ let s=0; const o=y*w;
      for(let x=-r;x<=r;x++) s+=a[o+clamp(x,0,w-1)];
      for(let x=0;x<w;x++){ b[o+x]=s/(2*r+1); s+=a[o+clamp(x+r+1,0,w-1)]-a[o+clamp(x-r,0,w-1)]; } }
    for(let x=0;x<w;x++){ let s=0;
      for(let y=-r;y<=r;y++) s+=b[clamp(y,0,h-1)*w+x];
      for(let y=0;y<h;y++){ a[y*w+x]=s/(2*r+1); s+=b[clamp(y+r+1,0,h-1)*w+x]-b[clamp(y-r,0,h-1)*w+x]; } }
  }
  return a;
}
function kindOf(img){
  if(img.classList.contains('lamp')) return 'lamp';
  if(img.classList.contains('bookend')) return 'bookend';
  const pr=img.closest('.prop'); if(pr){ const c=[...pr.classList].find(c=>c.startsWith('prop-')); return c?c.slice(5):'def'; }
  if(img.closest('.bk')) return 'book';
  return 'def';
}
let SETTLED=false, GEN=0;
function layer(cls,w,h){ const c=document.createElement('canvas'); c.className='ll-cv '+cls; c.width=Math.max(1,w); c.height=Math.max(1,h);
  c.setAttribute('aria-hidden','true'); return c; }

async function render(stage,gen){
  const alive=()=>gen===GEN;
  const pause=()=>new Promise(r=>setTimeout(r,0));
  /* long loops hand the main thread back every ~12ms so the page never stalls */
  let slice=performance.now();
  const breathe=async()=>{ if(performance.now()-slice<12) return true; await pause(); slice=performance.now(); return alive(); };
  const T0=performance.now(), tm={};
  const lampImg=[...stage.querySelectorAll('.lampwrap .lamp')].find(l=>l.offsetWidth&&l.getClientRects().length);
  if(!lampImg||!lampImg.complete||!lampImg.naturalWidth) return false;
  const row=lampImg.closest('.caserow'), ledgeWrap=row&&row.querySelector('.ledgewrap'), ledge=ledgeWrap&&ledgeWrap.querySelector('.ledge');
  if(!ledge) return false;

  const sr=stage.getBoundingClientRect(), k=(sr.width/stage.offsetWidth)||1;
  const dpr=Math.min(2,window.devicePixelRatio||1);
  const LM=affine(lampImg); if(!LM) return false;
  const S=Math.hypot(LM.vx,LM.vy)*LM.H/330;                 /* screen px per lamp px */
  const lr=ledge.getBoundingClientRect(), lw=ledgeWrap.getBoundingClientRect();
  const yBack=lr.top, faceH=lr.height*P.faceFrac;
  const shelfD=P.shelfDepth*S, c=faceH/shelfD;              /* oblique: screen y = world y + c*z */

  /* ---- the light: a spotlight at the shade's mouth, an emitter the size of the mouth ---- */
  const ms=mapPt(LM,P.mouth[0]*LM.W,P.mouth[1]*LM.H), bs=mapPt(LM,P.bulb[0]*LM.W,P.bulb[1]*LM.H);
  const zL=P.zL*S, Lc=[ms[0], ms[1]-c*zL, zL];
  const A=norm(P.axis), cosI=Math.cos(P.inner*D2R), cosO=Math.cos(P.outer*D2R), cosS=Math.cos(P.spillTo*D2R);
  const e1=norm([A[1],-A[0],0]), e2=norm([A[1]*e1[2]-A[2]*e1[1], A[2]*e1[0]-A[0]*e1[2], A[0]*e1[1]-A[1]*e1[0]]);
  const NS=P.samples, LX=new Float32Array(NS), LY=new Float32Array(NS), LZ=new Float32Array(NS);
  for(let j=0;j<NS;j++){ /* a sunflower spiral over the mouth: even coverage, no banding */
    const rr=Math.sqrt((j+.5)/NS)*P.lightR*S, th=j*2.39996323, ca=Math.cos(th), sa=Math.sin(th);
    LX[j]=Lc[0]+rr*(ca*e1[0]+sa*e2[0]); LY[j]=Lc[1]+rr*(ca*e1[1]+sa*e2[1]); LZ[j]=Lc[2]+rr*(ca*e1[2]+sa*e2[2]); }
  const R02=(P.R0*S)**2, lipC=cosO+.22*(cosI-cosO);
  /* the shade's beam: a full core, a soft cut-off with the reflector's brighter lip just inside
     it, then a little spill scattered off the shade's rim */
  function spot(ct){
    if(ct<cosS) return 0;
    const core=sstep(cosO,cosI,ct), hot=.6+.4*sstep(cosI,1,ct);
    const lip=P.lip*Math.exp(-(((ct-lipC)/.03)**2));
    return core*(hot+lip)+P.spill*sstep(cosS,cosO,ct);
  }
  /* unshadowed light arriving at a point, per unit of facing (the caller applies n.l) */
  function reach(px,py,pz){
    const dx=px-Lc[0], dy=py-Lc[1], dz=pz-Lc[2], r2=dx*dx+dy*dy+dz*dz, r=Math.sqrt(r2);
    const sp=spot((dx*A[0]+dy*A[1]+dz*A[2])/r); if(sp<=0) return null;
    return {E:P.I0*sp*R02/r2, lx:-dx/r, ly:-dy/r, lz:-dz/r};
  }
  /* where the beam's axis meets the shelf top: the bounce comes off there */
  const tHit=(yBack-Lc[1])/A[1], pool=[Lc[0]+A[0]*tHit, yBack+c*clamp(Lc[2]+A[2]*tHit,0,shelfD)];
  const bR2=(P.bounceR*S)**2;
  const bounceAt=(x,y)=>P.bounce*Math.exp(-((x-pool[0])**2+((y-pool[1])*1.25)**2)/bR2);

  /* ---- the working area: the wall the lamp can reach, from above the case to the shelf ---- */
  const cell=P.cell;
  const X0=Math.max(sr.left,ms[0]-P.reachL*S), X1=Math.min(sr.right,ms[0]+P.reachR*S);
  const Y0=Math.max(sr.top-170*k,ms[1]-P.reachU*S), Y1=lw.bottom;
  const gw=Math.ceil((X1-X0)/cell), gh=Math.ceil((Y1-Y0)/cell);
  const inBox=(r)=>r.right>X0&&r.left<X1&&r.bottom>Y0&&r.top<Y1;
  const imgs=[...row.querySelectorAll('.bk img, .prop img, img.bookend, .lampwrap .lamp')]
    .filter(i=>i.offsetWidth&&i.getClientRects().length&&i.complete&&i.naturalWidth&&inBox(i.getBoundingClientRect()));

  /* depth map: which cut-out covers each cell, and how far out from the wall its front is */
  const depth=new Float32Array(gw*gh).fill(-1), cov=new Float32Array(gw*gh);
  const objs=[];
  const rc=document.createElement('canvas'); rc.width=gw; rc.height=gh;
  const rx=rc.getContext('2d',{willReadFrequently:true});
  let Dmax=0;
  for(const img of imgs){
    const M=img===lampImg?LM:affine(img); if(!M) continue;
    const kind=kindOf(img), ob={img,M,kind,D:(P.depth[kind]||P.depth.def)*S}; objs.push(ob);
    if(kind==='lamp') continue;                     /* the lamp holds the light; it shades nothing it lights */
    let D=ob.D;
    const cs=[mapPt(M,0,0),mapPt(M,M.W,0),mapPt(M,0,M.H),mapPt(M,M.W,M.H)];
    const bx0=clamp(Math.floor((Math.min(...cs.map(p=>p[0]))-X0)/cell)-1,0,gw), bx1=clamp(Math.ceil((Math.max(...cs.map(p=>p[0]))-X0)/cell)+1,0,gw);
    const by0=clamp(Math.floor((Math.min(...cs.map(p=>p[1]))-Y0)/cell)-1,0,gh), by1=clamp(Math.ceil((Math.max(...cs.map(p=>p[1]))-Y0)/cell)+1,0,gh);
    if(bx1<=bx0||by1<=by0) continue;
    rx.setTransform(1,0,0,1,0,0); rx.clearRect(bx0,by0,bx1-bx0,by1-by0);
    rx.setTransform(M.ux/cell,M.uy/cell,M.vx/cell,M.vy/cell,(M.ox-X0)/cell,(M.oy-Y0)/cell);
    rx.drawImage(img,0,0,M.W,M.H);
    const a=rx.getImageData(bx0,by0,bx1-bx0,by1-by0).data, bw_=bx1-bx0;
    /* the painting says who stands in front: images come in paint order, so anything drawn over
       an earlier object must be at least a little nearer than it (else the trophy's handle,
       tucked behind the History book, would throw its shadow onto the book's spine) */
    for(let y=by0;y<by1;y++) for(let x=bx0;x<bx1;x++){
      const i=y*gw+x;
      if(a[((y-by0)*bw_+(x-bx0))*4+3]>128&&cov[i]>.5&&depth[i]+4*S>D) D=depth[i]+4*S;
    }
    ob.D=D; Dmax=Math.max(Dmax,D);
    for(let y=by0;y<by1;y++) for(let x=bx0;x<bx1;x++){
      const al=a[((y-by0)*bw_+(x-bx0))*4+3]/255; if(al<.04) continue;
      const i=y*gw+x; if(al>cov[i]) cov[i]=al; if(al>.5&&D>depth[i]) depth[i]=D;
    }
  }
  tm.depth=performance.now()-T0;
  await pause(); if(!alive()) return false;
  /* how much of the mouth a world point can see: march each ray back through the cut-outs
     (only the stretch of it that is still close enough to the wall to hit one) */
  function visibility(px,py,pz){
    let lit=0; const st=P.steps;
    for(let j=0;j<NS;j++){
      const dx=LX[j]-px, dy=LY[j]-py, dz=LZ[j]-pz;
      let tMax=1;
      if(dz>0){ if(pz>=Dmax){ lit++; continue; } tMax=Math.min(1,(Dmax-pz)/dz); }
      let blocked=false;
      for(let s=0;s<st;s++){
        const t=(s+.55)/st*tMax, z=pz+dz*t;
        const gx=((px+dx*t-X0)/cell)|0, gy=((py+dy*t+c*z-Y0)/cell)|0;
        if(gx<0||gy<0||gx>=gw||gy>=gh) continue;
        const i=gy*gw+gx;
        if(cov[i]>.35&&depth[i]>=z){ blocked=true; break; }
      }
      if(!blocked) lit++;
    }
    return lit/NS;
  }
  /* one surface's gain. The lamp adds warm light where it lands; where it should land but is
     blocked (a cast shadow) or the surface turns away (a form shadow) it takes a little away:
     that local contrast is what makes a lamp read as light rather than a tint */
  const T=P.tint;
  function gain(out,o,E0,lit,bo,k){
    const miss=Math.min(1,E0*P.shadowReach)*(1-lit/Math.max(E0,1e-6))*P.kShadow;
    /* a camera looking at a lamplit patch pulls its exposure down a little there: on a pale wall
       that is what turns 'brighter' into 'warmer' (blue sinks as red climbs) */
    const L=k*(lit+bo), ex=1+L*P.expo;
    for(let ch=0;ch<3;ch++) out[o+ch]=(1+L*T[ch])/ex-miss*(ch===2?.9:1);
  }

  /* ---- wall ---- */
  const wallMul=new ImageData(gw,gh), wallAdd=new ImageData(gw,gh), G=new Float32Array(3);
  const shelfLine=yBack+faceH*.3;                   /* below this the wall is behind the plank */
  for(let y=0;y<gh;y++){ const sy=Y0+(y+.5)*cell;
    if(!await breathe()) return false;
    for(let x=0;x<gw;x++){
      const i=y*gw+x, sx=X0+(x+.5)*cell;
      const pz=0, py=sy;                          /* the wall itself; objects are relit on their own */
      let E0=0, lit=0, bo=0;
      if(sy<shelfLine&&!(cov[i]>.97)){
        const R=reach(sx,py,pz);
        if(R){ const v=visibility(sx,py,pz); E0=R.E*Math.max(0,R.lz); lit=E0*v; }
        bo=bounceAt(sx,sy)*Math.min(1,(shelfLine-sy)/(40*S)+.2);
      }
      gain(G,0,E0,lit,bo,P.kWall);
      /* soften into the edges of the working area so it never shows */
      const ex=Math.min(x,gw-1-x)/(30/cell), ey=Math.min(y,gh)/(30/cell), fe=Math.min(1,ex,ey);
      const o=i*4;
      for(let ch=0;ch<3;ch++){ const g=1+(G[ch]-1)*fe;
        wallMul.data[o+ch]=clamp(g,0,1)*255; wallAdd.data[o+ch]=g>1?(1-1/g)*255:0; }
      wallMul.data[o+3]=255; wallAdd.data[o+3]=255;
    }
  }
  tm.wall=performance.now()-T0;
  await pause(); if(!alive()) return false;

  /* ---- plank: its top face takes the pool of light and the objects' shadows ---- */
  const pc=P.cell, px0=Math.max(lw.left,X0), px1=Math.min(lw.right,X1);
  const pw=Math.ceil((px1-px0)/pc), ph=Math.ceil(lw.height/pc);
  const plMul=new ImageData(pw,ph), plAdd=new ImageData(pw,ph);
  for(let y=0;y<ph;y++){ const sy=lw.top+(y+.5)*pc, f=(sy-yBack)/faceH;
    if(!await breathe()) return false;
    for(let x=0;x<pw;x++){
      const sx=px0+(x+.5)*pc, o=(y*pw+x)*4;
      let E0=0, lit=0;
      if(f>=-.05&&f<=1.05){
        const pz=clamp((sy-yBack)/c,0,shelfD), R=reach(sx,yBack,pz);
        if(R){ const top=R.E*Math.max(0,-R.ly);
          /* the top face, rolling over at the front edge, where the rounded lip catches a thin line of light */
          E0=top*(1-sstep(.86,1.05,f));
          const lipHi=P.plankLip*top*Math.exp(-(((f-.9)/.045)**2));
          if(E0+lipHi>.002) lit=(E0+lipHi)*visibility(sx,yBack,pz); }
      }
      const bo=f<1?bounceAt(sx,yBack)*.5:0;
      gain(G,0,E0,lit,bo,P.kPlank);
      const ex=Math.min(x,pw-1-x)/(30/pc), fe=Math.min(1,ex);
      for(let ch=0;ch<3;ch++){ const g=1+(G[ch]-1)*fe;
        plMul.data[o+ch]=clamp(g,0,1)*255; plAdd.data[o+ch]=g>1?(1-1/g)*255:0; }
      plMul.data[o+3]=255; plAdd.data[o+3]=255;
    }
  }
  tm.plank=performance.now()-T0;
  await pause(); if(!alive()) return false;

  /* ---- each object, relit from its own pixels ---- */
  const cr=Math.cos(-P.rimRot*D2R), sn=Math.sin(-P.rimRot*D2R), rA=P.rimA*S, rB=P.rimB*S;
  const ell=(sx,sy)=>{ const dx=sx-ms[0], dy=sy-ms[1], u=dx*cr-dy*sn, v=dx*sn+dy*cr; return Math.sqrt((u/rA)**2+(v/rB)**2); };
  const objLayers=[];
  for(const o of objs){
    const {img,M,kind,D}=o;
    const su=Math.hypot(M.ux,M.uy), sv=Math.hypot(M.vx,M.vy);
    const bw=Math.round(M.W*su*dpr), bh=Math.round(M.H*sv*dpr); if(bw<2||bh<2) continue;
    const src=pixelsOf(img,bw,bh), d=src.data, n=bw*bh;
    const out=new ImageData(bw,bh), od=out.data;
    const mat=MAT[kind]||MAT.def;
    let shape=null, paint=null;
    {
      const alpha=new Float32Array(n), lum=new Float32Array(n);
      for(let i=0;i<n;i++){ alpha[i]=d[i*4+3]/255; lum[i]=(.3*d[i*4]+.59*d[i*4+1]+.11*d[i*4+2])/255; }
      shape=blur(alpha,bw,bh,Math.max(2,Math.round(P.round*S*su/k*dpr))); paint=blur(lum,bw,bh,Math.max(1,Math.round(dpr)));
    }
    const Ux=M.ux/su, Uy=M.uy/su, Vx=M.vx/sv, Vy=M.vy/sv;          /* image axes on screen */
    /* this object's own shadow map, traced from its own face (the wall's map is a different
       plane: borrowing it smudged the wall's shadows onto the objects' edges) */
    let ov=null, oX=0, oY=0, ow=0, oh=0; const oc=P.cell;
    {
      const cs=[mapPt(M,0,0),mapPt(M,M.W,0),mapPt(M,0,M.H),mapPt(M,M.W,M.H)];
      oX=Math.min(...cs.map(p=>p[0]))-oc; oY=Math.min(...cs.map(p=>p[1]))-oc;
      ow=Math.ceil((Math.max(...cs.map(p=>p[0]))+oc-oX)/oc)+1; oh=Math.ceil((Math.max(...cs.map(p=>p[1]))+oc-oY)/oc)+1;
      ov=new Float32Array(ow*oh);
      for(let y=0;y<oh;y++){ if(!await breathe()) return false; for(let x=0;x<ow;x++){
        const sx=oX+(x+.5)*oc, sy=oY+(y+.5)*oc, py=sy-c*D;
        ov[y*ow+x]=reach(sx,py,D)?visibility(sx,py,D):1; } }
    }
    const ovAt=(sx,sy)=>{ const gx=clamp((sx-oX)/oc-.5,0,ow-1.001), gy=clamp((sy-oY)/oc-.5,0,oh-1.001);
      const x=gx|0, y=gy|0, fx=gx-x, fy=gy-y, i=y*ow+x;
      return (ov[i]*(1-fx)+ov[i+1]*fx)*(1-fy)+(ov[i+ow]*(1-fx)+ov[i+ow+1]*fx)*fy; };
    const bumpS=P.bumpShape*mat.bump*S*dpr, bumpP=P.bumpPaint*mat.bump*dpr;
    const du=M.W/bw, dv=M.H/bh;
    for(let y=0;y<bh;y++){ if(!await breathe()) return false; for(let x=0;x<bw;x++){
      const i=y*bw+x, q=i*4, a=d[q+3]; if(!a) continue;
      const u=(x+.5)*du, v=(y+.5)*dv, sx=M.ox+u*M.ux+v*M.vx, sy=M.oy+u*M.uy+v*M.vy;
      let r=d[q], g=d[q+1], b=d[q+2];
      if(kind==='lamp'&&u<M.W*.62&&v<M.H*.5){
        /* the shade stands behind its own beam: only its opening changes */
        const e=ell(sx,sy);
        if(e<1.14){
          const lum=(.3*r+.59*g+.11*b)/255;
          const inside=1-sstep(.84,1,e), ring=Math.exp(-(((e-1)/.07)**2));
          const t=sstep(.1,1,e), m=.72+.5*lum;
          let gr=255*m, gg=(246-70*t)*m, gb=(218-128*t)*m;
          const db=Math.sqrt((sx-bs[0])**2+(sy-bs[1])**2)/(P.bulbR*S), core=Math.exp(-db*db);
          gr+=255*core; gg+=250*core; gb+=238*core;
          const w=inside*.95;
          r=r*(1-w)+gr*w; g=g*(1-w)+gg*w; b=b*(1-w)+gb*w;
          r+=95*ring; g+=66*ring; b+=28*ring;
        }
      } else {
        /* a normal from the silhouette (rounded edges) and the paint (brush relief) */
        const xl=x>0?i-1:i, xr=x<bw-1?i+1:i, yu=y>0?i-bw:i, yd=y<bh-1?i+bw:i;
        const gx=(shape[xr]-shape[xl])*bumpS+(paint[xr]-paint[xl])*bumpP;
        const gy=(shape[yd]-shape[yu])*bumpS+(paint[yd]-paint[yu])*bumpP;
        let nx=-(gx*Ux+gy*Vx), ny=-(gx*Uy+gy*Vy), nz=1; const nl=Math.sqrt(nx*nx+ny*ny+1); nx/=nl; ny/=nl; nz/=nl;
        const py=sy-c*D, R=reach(sx,py,D);
        let E0=0, lit=0, spec=0;
        if(R){
          const vv=ovAt(sx,sy), ndl=nx*R.lx+ny*R.ly+nz*R.lz, wrap=Math.max(0,(ndl+P.wrap)/(1+P.wrap));
          E0=R.E; lit=R.E*wrap*vv;
          if(ndl>0){ const hx=R.lx, hy=R.ly, hz=R.lz+1, hl=Math.sqrt(hx*hx+hy*hy+hz*hz);
            spec=Math.pow(Math.max(0,(nx*hx+ny*hy+nz*hz)/hl),mat.shin)*R.E*vv*mat.ks; }
        }
        gain(G,0,E0,lit,bounceAt(sx,sy)*.8,P.kObj*mat.kd);
        const sr_=mat.metal?r*1.5+40:255, sg=mat.metal?g*1.45+30:236, sb=mat.metal?b*1.3+10:205;
        r=r*G[0]+spec*sr_; g=g*G[1]+spec*sg*.92; b=b*G[2]+spec*sb*.8;
      }
      od[q]=r; od[q+1]=g; od[q+2]=b; od[q+3]=a;   /* the typed array clamps */
    } }
    const cv=layer('obj',bw,bh); cv.getContext('2d').putImageData(out,0,0);
    const st=cv.style; st.left=img.offsetLeft+'px'; st.top=img.offsetTop+'px'; st.width=img.offsetWidth+'px'; st.height=img.offsetHeight+'px';
    const tf=getComputedStyle(img).transform; if(tf&&tf!=='none'){ st.transform=tf; st.transformOrigin=getComputedStyle(img).transformOrigin; }
    objLayers.push([img,cv]);
    await pause(); if(!alive()) return false;
  }
  tm.objects=performance.now()-T0;

  /* ---- in front: the bulb's bloom and the faint haze in the beam ---- */
  const hc=4, hx0=Math.max(X0,ms[0]-P.reachL*S), hx1=Math.min(X1,ms[0]+320*S), hy0=Math.max(Y0,ms[1]-300*S), hy1=lw.bottom;
  const hw=Math.ceil((hx1-hx0)/hc), hh=Math.ceil((hy1-hy0)/hc);
  const glow=new ImageData(hw,hh);
  const zs=10, zTop=shelfD*1.15, soft=(40*S)**2;
  for(let y=0;y<hh;y++){ if(!await breathe()) return false; for(let x=0;x<hw;x++){
    const sx=hx0+(x+.5)*hc, sy=hy0+(y+.5)*hc, o=(y*hw+x)*4;
    /* haze: light scattered toward us along the line of sight, in front of whatever is there */
    const gx=((sx-X0)/cell)|0, gy=((sy-Y0)/cell)|0, gi=gy*gw+gx;
    let z0=(gx>=0&&gy>=0&&gx<gw&&gy<gh&&cov[gi]>.35&&depth[gi]>0)?depth[gi]:0;
    if(sy>yBack+faceH) z0=Math.max(z0,shelfD);
    let h=0;
    if(z0<zTop) for(let s=0;s<zs;s++){
      const z=z0+(zTop-z0)*(s+.5)/zs, py=sy-c*z, dx=sx-Lc[0], dy=py-Lc[1], dz=z-Lc[2], r2=dx*dx+dy*dy+dz*dz;
      const sp=spot((dx*A[0]+dy*A[1]+dz*A[2])/Math.sqrt(r2)); if(sp>0) h+=sp*R02/(r2+soft);
    }
    h*=P.haze*(zTop-z0)/zTop/zs*6;
    /* bloom: a tight core over the shade's opening, then wider, softer skirts */
    const e=ell(sx,sy), dm=Math.sqrt((sx-ms[0])**2+(sy-ms[1])**2)/S;
    const bl=P.bloom*(.5*Math.exp(-((Math.max(0,e-.5)/.5)**2))+.2*Math.exp(-((dm/90)**2))+.09/(1+(dm/150)**2));
    /* fade out at the edges of the sheet */
    const fe=Math.min(1,Math.min(x,hw-1-x,y)/(40/hc));
    glow.data[o]=clamp(h+bl,0,1)*255*fe; glow.data[o+1]=clamp(h*.8+bl*.86,0,1)*255*fe; glow.data[o+2]=clamp(h*.55+bl*.66,0,1)*255*fe; glow.data[o+3]=255;
  } }
  tm.glow=performance.now()-T0;

  await pause(); if(!alive()) return false;
  /* ---- swap the layers in. Drawn while the lamp is already on (a resize), they arrive
     settled: the filament only warms up when someone pulls the cord ---- */
  SETTLED=stage.classList.contains('lit');
  stage.querySelectorAll('.ll-cv').forEach(e=>e.remove());
  const toStage=(cv,sx,sy,sw,sh,z)=>{ const st=cv.style; st.left=(sx-sr.left)/k+'px'; st.top=(sy-sr.top)/k+'px';
    st.width=sw/k+'px'; st.height=sh/k+'px'; st.zIndex=z; stage.insertBefore(cv,stage.querySelector('.booktip')); };
  const put=(cls,id,w,h)=>{ const cv=layer(cls,w,h); cv.getContext('2d').putImageData(id,0,0); return cv; };
  toStage(put('mul',wallMul,gw,gh),X0,Y0,gw*cell,gh*cell,0);
  toStage(put('add',wallAdd,gw,gh),X0,Y0,gw*cell,gh*cell,0);
  const kl=lw.width/ledgeWrap.offsetWidth||1;
  [put('mul',plMul,pw,ph),put('add',plAdd,pw,ph)].forEach(cv=>{ const st=cv.style;
    st.left=(px0-lw.left)/kl+'px'; st.top='0'; st.zIndex=2; st.width=pw*pc/kl+'px'; st.height=ph*pc/kl+'px'; ledgeWrap.appendChild(cv); });
  for(const [img,cv] of objLayers) img.after(cv);
  /* the rest of the room settles into evening while the lamp is on: the whole page dims a
     little (a touch cool, against the lamp's warmth), except round the lamp, where its light is */
  const dusk=document.createElement('div'); dusk.className='ll-cv dusk'; dusk.setAttribute('aria-hidden','true');
  const dm=[(Math.min(ms[0],pool[0])+Math.max(ms[0],pool[0]))/2-P.duskShift*S, ms[1]+P.duskDrop*S];
  const dc=P.duskTint.map(t=>Math.round(255*(1-P.dusk*t)));
  dusk.style.cssText='left:0;top:'+(-170)+'px;width:100%;height:calc(100% + 170px);z-index:3;'
    +'background:radial-gradient('+(P.duskRx*S/k)+'px '+(P.duskRy*S/k)+'px at '+((dm[0]-sr.left)/k)+'px '+((dm[1]-sr.top)/k+170)+'px,'
    +'#fff 0%,#fff 28%,rgb('+dc.join(',')+') 100%)';
  /* ...but the two doors stay bright: they are the page's controls, not part of the room */
  const drs=[...stage.querySelectorAll('.slot.door')].filter(d=>d.offsetWidth&&d.getClientRects().length);
  if(drs.length){
    const top=sr.top-170*k, imgs_=['linear-gradient(#000,#000)'], sz=['100% 100%'], pos=['0 0'];
    for(const d of drs){ const r=d.getBoundingClientRect(), w=r.width/k, h=r.height/k, rad=parseFloat(getComputedStyle(d).borderTopLeftRadius)||0;
      imgs_.push('url("data:image/svg+xml,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'"><rect width="'+w+'" height="'+h+'" rx="'+rad+'"/></svg>')+'")');
      sz.push(w+'px '+h+'px'); pos.push(((r.left-sr.left)/k)+'px '+((r.top-top)/k)+'px'); }
    const st=dusk.style;
    st.webkitMaskImage=st.maskImage=imgs_.join(',');
    st.webkitMaskSize=st.maskSize=sz.join(','); st.webkitMaskPosition=st.maskPosition=pos.join(',');
    st.webkitMaskRepeat=st.maskRepeat='no-repeat';
    st.webkitMaskComposite='xor'; st.maskComposite='exclude';
  }
  stage.insertBefore(dusk,stage.querySelector('.booktip'));
  toStage(put('scr',glow,hw,hh),hx0,hy0,hw*hc,hh*hc,3);
  if(SETTLED) stage.querySelectorAll('.ll-cv').forEach(c=>c.classList.add('settled'));
  stage.classList.add('relit');
  tm.total=performance.now()-T0;
  if(P.debug) console.log('lamp light', JSON.stringify(Object.fromEntries(Object.entries(tm).map(([a,b])=>[a,Math.round(b)]))));
  return true;
}

/* the page waits on this before the lamp's first automatic click (never more than ~1.5s) */
let readyFn; const READY=new Promise(r=>readyFn=r);
window.__lampLightReady=Promise.race([READY,new Promise(r=>setTimeout(r,2600))]);

function start(){
  const stage=document.getElementById('stage-landing'); if(!stage){ readyFn(); return; }
  let timer=0, lastW=innerWidth;
  const fail=(e)=>{ stage.classList.remove('relit'); stage.querySelectorAll('.ll-cv').forEach(c=>c.remove());
    if(window.console) console.warn('lamp light: keeping the CSS light', e); };
  const run=()=>{ const gen=++GEN;
    return render(stage,gen).then(ok=>{ if(gen===GEN) readyFn(); return ok; }, e=>{ fail(e); readyFn(); return false; }); };
  const later=(ms)=>{ clearTimeout(timer); timer=setTimeout(run,ms); };
  if(document.readyState==='complete') later(0); else addEventListener('load',()=>later(0));
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(()=>{ if(document.readyState==='complete') later(60); });
  addEventListener('resize',()=>{ if(innerWidth!==lastW){ lastW=innerWidth; later(220); } });
  /* the tuning bench (?tune=1) moves things about: redraw the shadows where they now fall */
  stage.addEventListener('pointerup',()=>{ if(document.documentElement.classList.contains('bench')) later(150); });
  /* lamp off: the next switch-on should warm up again */
  new MutationObserver(()=>{ if(!stage.classList.contains('lit')) stage.querySelectorAll('.ll-cv.settled').forEach(c=>c.classList.remove('settled')); })
    .observe(stage,{attributes:true,attributeFilter:['class']});
  window.__lampLight={render:run, P};
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();
