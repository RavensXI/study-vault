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
   - a window in the left-hand wall (off the page) lets in the sun by day and the moon by night:
     parallel light, so a slanted patch with the window's bars lands on the wall and plank, and
     the shelf's objects throw crisp shadows into it;
   - lamp on is night: the room dims (welcome.html's CSS), and round the lamp the render lifts
     it back to its daytime level, so its light is the brightest thing on the page;
   - and, as in a photograph, the eye's reference moves: under the light the camera pulls its
     exposure down a touch (which is what turns a pale wall warm rather than just white), and a
     patch the lamp should reach but can't (a cast shadow, a side turned away) reads darker.
     Nothing the lamp can't reach changes at all.

   Output is a handful of canvases in three sets: n (the lamp and the night it brings, shown with
   .lit), m (moonlight, with .night) and d (daylight, without .night). Over the wallpaper and the
   plank they come in pairs (multiply for the darkening, colour-dodge for the light: together
   exactly surface x gain); each object gets a relit copy laid over its own image; one glow
   sheet sits in front. welcome.html's CSS fades each set in and out. If anything here fails (a canvas that can't be
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
  night:{obj:.52, wall:[.5,.52,.6]},  /* how dark the room goes at night: objects, and the wall (a touch blue) */
  hole:{rx:470, ry:400, shift:90, drop:110},  /* round the lamp, while it's on, the room keeps its level */
  /* the window, in the left-hand wall off the page: how far out (x), its top and bottom above the
     shelf, how far it reaches out into the room (z0..z1), and the bar across it */
  win:{x:60, top:430, bottom:175, z0:160, z1:560, bar:22},
  sun:{dir:[.62,.40,-.68], I:.95, k:.8, expo:.55, tint:[1,.92,.74], kShadow:.4, shadowReach:1.4, soft:.012, spread:.35, samples:12, pen:.045, penMax:22},
  moon:{dir:[.60,.34,-.72], I:.5, k:.9, expo:0, tint:[.72,.84,1.08], kShadow:.3, shadowReach:1.4, soft:.02, spread:.5, samples:12, pen:.075, penMax:30},
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
const ZERO=[0,0];

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
  const lr=ledge.getBoundingClientRect(), lw=ledgeWrap.getBoundingClientRect(), rowR=row.getBoundingClientRect();
  const yBack=lr.top, faceH=lr.height*P.faceFrac;
  const shelfD=P.shelfDepth*S, c=faceH/shelfD;              /* oblique: screen y = world y + c*z */
  const shelfLine=yBack+faceH*.3;                           /* below this the wall is behind the plank */

  /* ---- the lamp: a spotlight at the shade's mouth, an emitter the size of the mouth ---- */
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
  /* unshadowed lamplight arriving at a point, per unit of facing (the caller applies n.l) */
  function reach(px,py,pz){
    const dx=px-Lc[0], dy=py-Lc[1], dz=pz-Lc[2], r2=dx*dx+dy*dy+dz*dz, r=Math.sqrt(r2);
    const sp=spot((dx*A[0]+dy*A[1]+dz*A[2])/r); if(sp<=0) return null;
    return {E:P.I0*sp*R02/r2, lx:-dx/r, ly:-dy/r, lz:-dz/r};
  }
  /* where the beam's axis meets the shelf top: the bounce comes off there */
  const tHit=(yBack-Lc[1])/A[1], pool=[Lc[0]+A[0]*tHit, yBack+c*clamp(Lc[2]+A[2]*tHit,0,shelfD)];
  const bR2=(P.bounceR*S)**2;
  const bounceAt=(x,y)=>P.bounce*Math.exp(-((x-pool[0])**2+((y-pool[1])*1.25)**2)/bR2);

  /* ---- the window: an opening in the left-hand wall (off the page), sun through it by day and
     moon by night. Parallel light, so a patch the shape of the window (two bars across it)
     lands slanted on the wall, and everything on the shelf throws a crisp shadow into it ---- */
  const W=P.win, xW=rowR.left-W.x*S;
  const wy0=yBack-W.top*S, wy1=yBack-W.bottom*S, wz0=W.z0*S, wz1=W.z1*S, wbar=W.bar*S;
  const wym=(wy0+wy1)/2, wzm=(wz0+wz1)/2;
  const sbox=(v,a,b,s)=>sstep(a-s,a+s,v)*(1-sstep(b-s,b+s,v));
  function mkWin(o){
    const D=norm(o.dir), L=[-D[0],-D[1],-D[2]];
    const u1=norm([-L[1],L[0],0]), u2=norm([L[1]*u1[2]-L[2]*u1[1], L[2]*u1[0]-L[0]*u1[2], L[0]*u1[1]-L[1]*u1[0]]);
    const dirs=[]; for(let j=0;j<o.samples;j++){ const th=j*2.39996323, rr=Math.sqrt((j+.5)/o.samples)*Math.tan(o.spread*D2R);
      dirs.push(norm([L[0]+rr*(Math.cos(th)*u1[0]+Math.sin(th)*u2[0]), L[1]+rr*(Math.cos(th)*u1[1]+Math.sin(th)*u2[1]), L[2]+rr*(Math.cos(th)*u1[2]+Math.sin(th)*u2[2])])); }
    return {...o, L, dirs};
  }
  const SUN=mkWin(P.sun), MOON=mkWin(P.moon);
  /* how much of the window a point sees along the light (soft with distance, like a real patch) */
  function winAp(Wn,px,py,pz){
    const L=Wn.L; const t=(xW-px)/L[0]; if(!(t>0)) return 0;
    const qy=py+L[1]*t, qz=pz+L[2]*t, s=Math.max(1.5*S,t*Wn.soft);
    const a=sbox(qy,wy0,wy1,s)*sbox(qz,wz0,wz1,s);
    if(a<=0.001) return 0;
    return a*(1-sbox(qz,wzm-wbar/2,wzm+wbar/2,s*.7))*(1-sbox(qy,wym-wbar/2,wym+wbar/2,s*.7));
  }

  /* ---- night: the room dims, save round the lamp while it's on ---- */
  const NK=P.night.obj, NW=P.night.wall;
  const hx=(ms[0]+pool[0])/2-P.hole.shift*S, hy=ms[1]+P.hole.drop*S, hrx=P.hole.rx*S, hry=P.hole.ry*S;
  const holeAt=(x,y)=>{ const e=Math.sqrt(((x-hx)/hrx)**2+((y-hy)/hry)**2);
    return (1-clamp((e-.28)/.72,0,1))*(1-sstep(lw.bottom-8*S,lw.bottom,y)); };
  const nObj=(x,y)=>NK+(1-NK)*holeAt(x,y);

  /* ---- the working area: this shelf's whole width, from above the case down to the plank ---- */
  const cell=P.cell;
  const X0=sr.left, X1=sr.right;
  const Y0=Math.max(sr.top-170*k,Math.min(ms[1]-P.reachU*S,wy0)), Y1=lw.bottom;
  const gw=Math.ceil((X1-X0)/cell), gh=Math.ceil((Y1-Y0)/cell);
  const imgs=[...row.querySelectorAll('.bk img, .prop img, img.bookend, .lampwrap .lamp')]
    .filter(i=>i.offsetWidth&&i.getClientRects().length&&i.complete&&i.naturalWidth);

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
  const blockedAt=(sx,sy,z)=>{ const gx=((sx-X0)/cell)|0, gy=((sy-Y0)/cell)|0;
    if(gx<0||gy<0||gx>=gw||gy>=gh) return false; const i=gy*gw+gx; return cov[i]>.35&&depth[i]>=z; };
  /* how much of the lamp's mouth a world point can see: march each ray back through the
     cut-outs (only the stretch of it still close enough to the wall to hit one) */
  function visibility(px,py,pz){
    let lit=0; const st=P.steps;
    for(let j=0;j<NS;j++){
      const dx=LX[j]-px, dy=LY[j]-py, dz=LZ[j]-pz;
      let tMax=1;
      if(dz>0){ if(pz>=Dmax){ lit++; continue; } tMax=Math.min(1,(Dmax-pz)/dz); }
      let blocked=false;
      for(let s=0;s<st;s++){
        const t=(s+.55)/st*tMax, z=pz+dz*t;
        if(blockedAt(px+dx*t, py+dy*t+c*z, z)){ blocked=true; break; }
      }
      if(!blocked) lit++;
    }
    return lit/NS;
  }
  /* the same for the window: a few directions across the sun's (or moon's) disc and sky */
  /* ...and how far along the light the thing in the way stands (WT: 0 when nothing is): a
     window's shadow is crisp at an object's foot and softens the further it falls, so that
     distance sets how much each shadow is blurred afterwards (softShadow) */
  let WT=0;
  function winVis(Wn,px,py,pz){
    WT=0; if(pz>=Dmax) return 1;
    let lit=0, tSum=0, nB=0; const st=14;
    const j0=((Math.sin(px*12.9898+py*78.233)*43758.5453)%1+1)%1;   /* per-point jitter: no banding */
    for(let di=0;di<Wn.dirs.length;di++){ const L=Wn.dirs[di];
      const sMax=(Dmax-pz)/L[2], jj=(j0+di*.618)%1; let hit=-1;
      for(let s=0;s<st;s++){ const t=(s+jj)/st*sMax, z=pz+L[2]*t;
        if(blockedAt(px+L[0]*t, py+L[1]*t+c*z, z)){ hit=t; break; } }
      if(hit<0) lit++; else { tSum+=hit; nB++; }
    }
    if(nB) WT=tSum/nB;
    return lit/Wn.dirs.length;
  }
  /* blur a shadow map by how far each shadow has fallen from what cast it */
  function softShadow(vis,tm,bl,w,h,cellPx,Wn){
    const tN=new Float32Array(w*h); for(let i=0;i<w*h;i++) tN[i]=tm[i]*bl[i];
    const R=Math.max(2,Math.round(Wn.penMax*S/cellPx));
    const tb=blur(tN,w,h,R), bb=blur(bl,w,h,R);
    const radii=[0,1,2,4,7,11].filter(r=>r<=Math.max(1,Math.ceil(Wn.penMax*S/cellPx)));
    const levels=radii.map(r=>r?blur(vis,w,h,r):vis);
    const out=new Float32Array(w*h);
    for(let i=0;i<w*h;i++){
      const t=bb[i]>.02?tb[i]/bb[i]:0, rr=(1.2*S+t*Wn.pen)/cellPx/2;   /* blur radius in cells */
      let k=0; while(k<radii.length-1&&radii[k+1]<rr) k++;
      if(k>=radii.length-1){ out[i]=levels[k][i]; continue; }
      const f=clamp((rr-radii[k])/(radii[k+1]-radii[k]),0,1);
      out[i]=levels[k][i]*(1-f)+levels[k+1][i]*f;
    }
    return out;
  }
  /* one surface's gain under one light. The light adds where it lands; where it should land
     but is blocked (a cast shadow) or the surface turns away it takes a little away: that local
     contrast is what makes it read as light rather than a tint. Under strong light the camera
     pulls its exposure down a touch, which turns a pale wall warm rather than just white. */
  function gain(out,E0,lit,bo,k,Lt){
    const miss=Math.min(1,E0*Lt.shadowReach)*(1-lit/Math.max(E0,1e-6))*Lt.kShadow;
    const L=k*(lit+bo), ex=1+L*Lt.expo;
    for(let ch=0;ch<3;ch++) out[ch]=(1+L*Lt.tint[ch])/ex-miss*(ch===2?.9:1);
  }
  const LAMP={tint:P.tint, expo:P.expo, kShadow:P.kShadow, shadowReach:P.shadowReach};
  const put4=(dm,da,o,g)=>{ for(let ch=0;ch<3;ch++){ const v=g[ch];
      dm[o+ch]=clamp(v,0,1)*255; da[o+ch]=v>1?(1-1/v)*255:0; } dm[o+3]=255; da[o+3]=255; };

  /* ---- wall: lamp, window and the night's lifting round the lamp, each its own pair ---- */
  const img2=()=>new ImageData(gw,gh);
  const wLm=img2(), wLa=img2(), wSm=img2(), wSa=img2(), wMm=img2(), wMa=img2(), wR=img2();
  const G=[0,0,0], one=[1,1,1];
  const wmap=(Wn,dm,da)=>({Wn,dm,da,E:new Float32Array(gw*gh),v:new Float32Array(gw*gh).fill(1),t:new Float32Array(gw*gh),b:new Float32Array(gw*gh)});
  const WMAPS=[wmap(SUN,wSm,wSa),wmap(MOON,wMm,wMa)];
  for(let y=0;y<gh;y++){ const sy=Y0+(y+.5)*cell;
    if(!await breathe()) return false;
    for(let x=0;x<gw;x++){
      const i=y*gw+x, sx=X0+(x+.5)*cell, o=i*4;
      const ey=Math.min(1,y/(30/cell));               /* soften into the top edge so it never shows */
      let gL=one, gS=one, gM=one;
      if(sy<shelfLine&&!(cov[i]>.97)){
        const R=reach(sx,sy,0);
        let E0=0, lit=0;
        if(R){ E0=R.E*Math.max(0,R.lz); lit=E0*visibility(sx,sy,0); }
        const bo=bounceAt(sx,sy)*Math.min(1,(shelfLine-sy)/(40*S)+.2);
        if(E0>0||bo>.002){ gain(G,E0,lit,bo,P.kWall,LAMP); gL=G.map(v=>1+(v-1)*ey); }
        for(const Wm of WMAPS){
          const ap=winAp(Wm.Wn,sx,sy,0); if(ap<=0) continue;
          Wm.E[i]=Wm.Wn.I*ap*Wm.Wn.L[2]; Wm.v[i]=winVis(Wm.Wn,sx,sy,0); Wm.t[i]=WT; Wm.b[i]=WT>0?1:0;
        }
      }
      put4(wLm.data,wLa.data,o,gL);
      /* the lamp's own pool keeps its daytime level at night: a lift of 1/night round it */
      const h=holeAt(sx,sy);
      for(let ch=0;ch<3;ch++){ const g=(NW[ch]+(1-NW[ch])*h)/NW[ch]; wR.data[o+ch]=(1-1/g)*255; }
      wR.data[o+3]=255;
    }
  }
  /* the window's shadows, softened by distance, then turned into light */
  for(const Wm of WMAPS){
    if(!await breathe()) return false;
    const v=softShadow(Wm.v,Wm.t,Wm.b,gw,gh,cell,Wm.Wn);
    for(let y=0;y<gh;y++){ const ey=Math.min(1,y/(30/cell));
      for(let x=0;x<gw;x++){ const i=y*gw+x, o=i*4, E=Wm.E[i];
        if(E>0){ gain(G,E,E*v[i],0,Wm.Wn.k,Wm.Wn); for(let ch=0;ch<3;ch++) G[ch]=1+(G[ch]-1)*ey; put4(Wm.dm.data,Wm.da.data,o,G); }
        else put4(Wm.dm.data,Wm.da.data,o,one); } }
  }
  tm.wall=performance.now()-T0;
  await pause(); if(!alive()) return false;

  /* ---- plank: its top face takes the pool of light, the window patch and the shadows ---- */
  const pc=P.cell, px0=lw.left;
  const pw=Math.ceil(lw.width/pc), ph=Math.ceil(lw.height/pc);
  const pNm=new ImageData(pw,ph), pNa=new ImageData(pw,ph), pDm=new ImageData(pw,ph), pDa=new ImageData(pw,ph);
  const GL=[0,0,0], GM=[0,0,0], GS=[0,0,0], GN=[0,0,0], np=pw*ph;
  const pmap=Wn=>({Wn,E:new Float32Array(np),v:new Float32Array(np).fill(1),t:new Float32Array(np),b:new Float32Array(np)});
  const PS=pmap(SUN), PM=pmap(MOON), lampG=new Float32Array(np*3);
  for(let y=0;y<ph;y++){ const sy=lw.top+(y+.5)*pc, f=(sy-yBack)/faceH;
    if(!await breathe()) return false;
    for(let x=0;x<pw;x++){
      const sx=px0+(x+.5)*pc, i=y*pw+x;
      let E0=0, lit=0;
      if(f>=-.05&&f<=1.05){
        const pz=clamp((sy-yBack)/c,0,shelfD), R=reach(sx,yBack,pz), roll=1-sstep(.86,1.05,f);
        if(R){ const top=R.E*Math.max(0,-R.ly);
          /* the top face, rolling over at the front edge, where the rounded lip catches a thin line of light */
          E0=top*roll;
          const lipHi=P.plankLip*top*Math.exp(-(((f-.9)/.045)**2));
          if(E0+lipHi>.002) lit=(E0+lipHi)*visibility(sx,yBack,pz); }
        for(const Pm of [PS,PM]){
          const ap=winAp(Pm.Wn,sx,yBack,pz)*roll; if(ap<=0) continue;
          const E=Pm.Wn.I*ap*(-Pm.Wn.L[1]); if(E<=0) continue;
          Pm.E[i]=E; Pm.v[i]=winVis(Pm.Wn,sx,yBack,pz); Pm.t[i]=WT; Pm.b[i]=WT>0?1:0;
        }
      }
      gain(GL,E0,lit,f<1?bounceAt(sx,yBack)*.5:0,P.kPlank,LAMP);
      const n=nObj(sx,sy); for(let ch=0;ch<3;ch++) lampG[i*3+ch]=n*GL[ch];
    }
  }
  if(!await breathe()) return false;
  const vS=softShadow(PS.v,PS.t,PS.b,pw,ph,pc,SUN), vM=softShadow(PM.v,PM.t,PM.b,pw,ph,pc,MOON);
  for(let i=0;i<np;i++){ const o=i*4;
    GM[0]=GM[1]=GM[2]=1; GS[0]=GS[1]=GS[2]=1;
    if(PM.E[i]>0) gain(GM,PM.E[i],PM.E[i]*vM[i],0,MOON.k*.9,MOON);
    if(PS.E[i]>0) gain(GS,PS.E[i],PS.E[i]*vS[i],0,SUN.k*.9,SUN);
    for(let ch=0;ch<3;ch++) GN[ch]=lampG[i*3+ch]*GM[ch];
    put4(pNm.data,pNa.data,o,GN); put4(pDm.data,pDa.data,o,GS);
  }
  tm.plank=performance.now()-T0;
  await pause(); if(!alive()) return false;

  /* ---- each object, relit from its own pixels: a night copy (lamp, moon, the room's dimming)
     and, where the sun reaches it, a day copy ---- */
  const cr=Math.cos(-P.rimRot*D2R), sn=Math.sin(-P.rimRot*D2R), rA=P.rimA*S, rB=P.rimB*S;
  const ell=(sx,sy)=>{ const dx=sx-ms[0], dy=sy-ms[1], u=dx*cr-dy*sn, v=dx*sn+dy*cr; return Math.sqrt((u/rA)**2+(v/rB)**2); };
  const objLayers=[];
  for(const o of objs){
    const {img,M,kind,D}=o;
    const su=Math.hypot(M.ux,M.uy), sv=Math.hypot(M.vx,M.vy);
    const bw=Math.round(M.W*su*dpr), bh=Math.round(M.H*sv*dpr); if(bw<2||bh<2) continue;
    const src=pixelsOf(img,bw,bh), d=src.data, n=bw*bh;
    const outN=new ImageData(bw,bh), oN=outN.data, outD=new ImageData(bw,bh), oD=outD.data;
    let sunTouched=false;
    const mat=MAT[kind]||MAT.def;
    const alpha=new Float32Array(n), lum=new Float32Array(n);
    for(let i=0;i<n;i++){ alpha[i]=d[i*4+3]/255; lum[i]=(.3*d[i*4]+.59*d[i*4+1]+.11*d[i*4+2])/255; }
    const shape=blur(alpha,bw,bh,Math.max(2,Math.round(P.round*S*su/k*dpr))), paint=blur(lum,bw,bh,Math.max(1,Math.round(dpr)));
    const Ux=M.ux/su, Uy=M.uy/su, Vx=M.vx/sv, Vy=M.vy/sv;          /* image axes on screen */
    /* this object's own shadow maps, traced from its own face (the wall's maps are a different
       plane: borrowing them smudged the wall's shadows onto the objects' edges) */
    const oc=P.cell, cs=[mapPt(M,0,0),mapPt(M,M.W,0),mapPt(M,0,M.H),mapPt(M,M.W,M.H)];
    const oX=Math.min(...cs.map(p=>p[0]))-oc, oY=Math.min(...cs.map(p=>p[1]))-oc;
    const ow=Math.ceil((Math.max(...cs.map(p=>p[0]))+oc-oX)/oc)+1, oh=Math.ceil((Math.max(...cs.map(p=>p[1]))+oc-oY)/oc)+1;
    const ovL=new Float32Array(ow*oh), ovS=new Float32Array(ow*oh), ovM=new Float32Array(ow*oh);
    for(let y=0;y<oh;y++){ if(!await breathe()) return false; for(let x=0;x<ow;x++){
      const sx=oX+(x+.5)*oc, sy=oY+(y+.5)*oc, py=sy-c*D, i=y*ow+x;
      ovL[i]=reach(sx,py,D)?visibility(sx,py,D):1;
      ovS[i]=winAp(SUN,sx,py,D)>0?winVis(SUN,sx,py,D):1;
      ovM[i]=winAp(MOON,sx,py,D)>0?winVis(MOON,sx,py,D):1; } }
    const gAt=(g,sx,sy)=>{ const gx=clamp((sx-oX)/oc-.5,0,ow-1.001), gy=clamp((sy-oY)/oc-.5,0,oh-1.001);
      const x=gx|0, y=gy|0, fx=gx-x, fy=gy-y, i=y*ow+x;
      return (g[i]*(1-fx)+g[i+1]*fx)*(1-fy)+(g[i+ow]*(1-fx)+g[i+ow+1]*fx)*fy; };
    const bumpS=P.bumpShape*mat.bump*S*dpr, bumpP=P.bumpPaint*mat.bump*dpr;
    const du=M.W/bw, dv=M.H/bh, kd=P.kObj*mat.kd;
    const specCol=(r,g,b)=>mat.metal?[r*1.5+40,(g*1.45+30)*.92,(b*1.3+10)*.8]:[255,236*.92,205*.8];
    for(let y=0;y<bh;y++){ if(!await breathe()) return false; for(let x=0;x<bw;x++){
      const i=y*bw+x, q=i*4, a=d[q+3]; if(!a) continue;
      const u=(x+.5)*du, v=(y+.5)*dv, sx=M.ox+u*M.ux+v*M.vx, sy=M.oy+u*M.uy+v*M.vy;
      const r0=d[q], g0=d[q+1], b0=d[q+2];
      const nt=nObj(sx,sy);
      let rN, gN, bN;
      if(kind==='lamp'&&u<M.W*.62&&v<M.H*.5){
        /* the shade stands behind its own beam: only its opening changes */
        rN=r0*nt; gN=g0*nt; bN=b0*nt;
        const e=ell(sx,sy);
        if(e<1.14){
          const lm=(.3*r0+.59*g0+.11*b0)/255;
          const inside=1-sstep(.84,1,e), ring=Math.exp(-(((e-1)/.07)**2));
          const t=sstep(.1,1,e), m=.72+.5*lm;
          let gr=255*m, gg=(246-70*t)*m, gb=(218-128*t)*m;
          const db=Math.sqrt((sx-bs[0])**2+(sy-bs[1])**2)/(P.bulbR*S), core=Math.exp(-db*db);
          gr+=255*core; gg+=250*core; gb+=238*core;
          const w=inside*.95;
          rN=rN*(1-w)+gr*w; gN=gN*(1-w)+gg*w; bN=bN*(1-w)+gb*w;
          rN+=95*ring; gN+=66*ring; bN+=28*ring;
        }
        oN[q]=rN; oN[q+1]=gN; oN[q+2]=bN; oN[q+3]=a;
        continue;
      }
      /* a normal from the silhouette (rounded edges) and the paint (brush relief) */
      const xl=x>0?i-1:i, xr=x<bw-1?i+1:i, yu=y>0?i-bw:i, yd=y<bh-1?i+bw:i;
      const gx=(shape[xr]-shape[xl])*bumpS+(paint[xr]-paint[xl])*bumpP;
      const gy=(shape[yd]-shape[yu])*bumpS+(paint[yd]-paint[yu])*bumpP;
      let nx=-(gx*Ux+gy*Vx), ny=-(gx*Uy+gy*Vy), nz=1; const nl=Math.sqrt(nx*nx+ny*ny+1); nx/=nl; ny/=nl; nz/=nl;
      const py=sy-c*D;
      const lightBy=(lx,ly,lz,E,vv,Lt,outG)=>{   /* diffuse gain into outG, returns the specular */
        const ndl=nx*lx+ny*ly+nz*lz, wrap=Math.max(0,(ndl+P.wrap)/(1+P.wrap));
        gain(outG,E,E*wrap*vv,0,kd,Lt);
        if(ndl<=0) return 0;
        const hz=lz+1, hl=Math.sqrt(lx*lx+ly*ly+hz*hz);
        return Math.pow(Math.max(0,(nx*lx+ny*ly+nz*hz)/hl),mat.shin)*E*vv*mat.ks;
      };
      /* night: lamp and moon, over the dimmed room */
      const R=reach(sx,py,D);
      let spL=0; if(R){ spL=lightBy(R.lx,R.ly,R.lz,R.E,gAt(ovL,sx,sy),LAMP,GL); } else gain(GL,0,0,0,kd,LAMP);
      const bo=bounceAt(sx,sy)*.8*kd; for(let ch=0;ch<3;ch++) GL[ch]+=bo*P.tint[ch];
      const apM=winAp(MOON,sx,py,D); let spM=0;
      if(apM>0){ spM=lightBy(MOON.L[0],MOON.L[1],MOON.L[2],MOON.I*apM,gAt(ovM,sx,sy),MOON,GM); } else { GM[0]=GM[1]=GM[2]=1; }
      const scN=specCol(r0,g0,b0);
      oN[q]=r0*nt*GL[0]*GM[0]+spL*scN[0]+spM*.6*scN[0]*.8; oN[q+1]=g0*nt*GL[1]*GM[1]+spL*scN[1]+spM*.6*scN[1]*.9;
      oN[q+2]=b0*nt*GL[2]*GM[2]+spL*scN[2]+spM*.6*scN[2]*1.1; oN[q+3]=a;
      /* day: the sun through the window */
      const apS=winAp(SUN,sx,py,D);
      if(apS>0){ sunTouched=true;
        const spS=lightBy(SUN.L[0],SUN.L[1],SUN.L[2],SUN.I*apS,gAt(ovS,sx,sy),SUN,GS);
        oD[q]=r0*GS[0]+spS*scN[0]; oD[q+1]=g0*GS[1]+spS*scN[1]; oD[q+2]=b0*GS[2]+spS*scN[2]; }
      else { oD[q]=r0; oD[q+1]=g0; oD[q+2]=b0; }
      oD[q+3]=a;
    } }
    const place=(cv)=>{ const st=cv.style; st.left=img.offsetLeft+'px'; st.top=img.offsetTop+'px'; st.width=img.offsetWidth+'px'; st.height=img.offsetHeight+'px';
      const tf=getComputedStyle(img).transform; if(tf&&tf!=='none'){ st.transform=tf; st.transformOrigin=getComputedStyle(img).transformOrigin; } };
    const cn=layer('obj n',bw,bh); cn.getContext('2d').putImageData(outN,0,0); place(cn);
    let cd=null; if(sunTouched){ cd=layer('obj d',bw,bh); cd.getContext('2d').putImageData(outD,0,0); place(cd); }
    objLayers.push([img,cn,cd]);
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
    const fe=Math.min(1,Math.min(x,hw-1-x,y)/(40/hc));
    glow.data[o]=clamp(h+bl,0,1)*255*fe; glow.data[o+1]=clamp(h*.8+bl*.86,0,1)*255*fe; glow.data[o+2]=clamp(h*.55+bl*.66,0,1)*255*fe; glow.data[o+3]=255;
  } }
  tm.glow=performance.now()-T0;
  await pause(); if(!alive()) return false;

  /* ---- swap the layers in. Lamp layers drawn while the lamp is already on (a resize) arrive
     settled: the filament only warms up when someone pulls the cord. Day and moon layers
     arrive with a soft fade. ---- */
  SETTLED=stage.classList.contains('lit');
  stage.querySelectorAll('.ll-cv').forEach(e=>e.remove());
  stage.querySelectorAll('.ll-own').forEach(e=>e.classList.remove('ll-own'));
  const before=stage.querySelector('.booktip');
  const toStage=(cv,sx,sy,sw,sh,z)=>{ const st=cv.style; st.left=(sx-sr.left)/k+'px'; st.top=(sy-sr.top)/k+'px';
    st.width=sw/k+'px'; st.height=sh/k+'px'; st.zIndex=z; stage.insertBefore(cv,before); };
  const put=(cls,id,w,h)=>{ const cv=layer(cls,w,h); cv.getContext('2d').putImageData(id,0,0); return cv; };
  for(const [cls,id] of [['mul d',wSm],['add d',wSa],['mul m',wMm],['add m',wMa],['add n',wR],['mul n',wLm],['add n',wLa]])
    toStage(put(cls,id,gw,gh),X0,Y0,gw*cell,gh*cell,0);
  const kl=lw.width/ledgeWrap.offsetWidth||1;
  [put('mul n',pNm,pw,ph),put('add n',pNa,pw,ph),put('mul d',pDm,pw,ph),put('add d',pDa,pw,ph)].forEach(cv=>{ const st=cv.style;
    st.left='0'; st.top='0'; st.zIndex=2; st.width=pw*pc/kl+'px'; st.height=ph*pc/kl+'px'; ledgeWrap.appendChild(cv); });
  ledgeWrap.classList.add('ll-own');
  for(const [img,cn,cd] of objLayers){ if(cd) img.after(cd); img.after(cn);
    const grp=img.closest('.bk, .prop'); if(grp) grp.classList.add('ll-own'); }
  toStage(put('scr n',glow,hw,hh),hx0,hy0,hw*hc,hh*hc,3);
  const all=stage.querySelectorAll('.ll-cv');
  if(SETTLED) all.forEach(c=>{ if(c.classList.contains('n')) c.classList.add('settled'); });
  all.forEach(c=>{ if(!c.classList.contains('n')) c.classList.add('fresh'); });
  requestAnimationFrame(()=>requestAnimationFrame(()=>stage.querySelectorAll('.ll-cv.fresh').forEach(c=>c.classList.remove('fresh'))));
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
