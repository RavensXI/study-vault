/* =====================================================================
   StudyVault subject icons — single source of truth.
   Loaded by home-ink.html (the live hero) AND icons.html (the viewer),
   so the two can never drift. Each draw fn fills a bold silhouette in a
   0..S box; the hero samples its filled pixels as dot targets.
   To refine an icon, edit it HERE and both update.
   ===================================================================== */
function _tri(c,a,b,cc){c.beginPath();c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.lineTo(cc[0],cc[1]);c.closePath();c.fill();}
function _rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath();c.fill();}
function _dc(c,x,y,r){c.beginPath();c.arc(x,y,r,0,6.2832);c.fill();}
function _hole(c,fn){c.save();c.globalCompositeOperation='destination-out';fn();c.restore();}
function _tx(c,s,ch,size,yf){c.font='bold '+Math.round(s*size)+'px Georgia, "Times New Roman", serif';c.textAlign='center';c.textBaseline='middle';c.fillText(ch,s/2,s*(yf||0.54));}
/* render a professional SVG icon path (Phosphor, 256 viewBox) scaled into the 0..s box */
function _svg(d){ var p=new Path2D(d); return function(c,s){ c.save(); c.scale(s/256,s/256); c.fill(p); c.restore(); }; }
var _PH={
  mouse:"M144,16H112A64.07,64.07,0,0,0,48,80v96a64.07,64.07,0,0,0,64,64h32a64.07,64.07,0,0,0,64-64V80A64.07,64.07,0,0,0,144,16Zm48,64v24H136V32h8A48.05,48.05,0,0,1,192,80ZM112,32h8v72H64V80A48.05,48.05,0,0,1,112,32Z",
  handshake:"M254.3,107.91,228.78,56.85a16,16,0,0,0-21.47-7.15L182.44,62.13,130.05,48.27a8.14,8.14,0,0,0-4.1,0L73.56,62.13,48.69,49.7a16,16,0,0,0-21.47,7.15L1.7,107.9a16,16,0,0,0,7.15,21.47l27,13.51,55.49,39.63a8.06,8.06,0,0,0,2.71,1.25l64,16a8,8,0,0,0,7.6-2.1l40-40,15.08-15.08,26.42-13.21a16,16,0,0,0,7.15-21.46Zm-54.89,33.37L165,113.72a8,8,0,0,0-10.68.61C136.51,132.27,116.66,130,104,122L147.24,80h31.81l27.21,54.41Zm-41.87,41.86L99.42,168.61l-49.2-35.14,28-56L128,64.28l9.8,2.59-45,43.68-.08.09a16,16,0,0,0,2.72,24.81c20.56,13.13,45.37,11,64.91-5L188,152.66Zm-25.72,34.8a8,8,0,0,1-7.75,6.06,8.13,8.13,0,0,1-1.95-.24L80.41,213.33a7.89,7.89,0,0,1-2.71-1.25L51.35,193.26a8,8,0,0,1,9.3-13l25.11,17.94L126,208.24A8,8,0,0,1,131.82,217.94Z",
  users:"M64.12,147.8a4,4,0,0,1-4,4.2H16a8,8,0,0,1-7.8-6.17,8.35,8.35,0,0,1,1.62-6.93A67.79,67.79,0,0,1,37,117.51a40,40,0,1,1,66.46-35.8,3.94,3.94,0,0,1-2.27,4.18A64.08,64.08,0,0,0,64,144C64,145.28,64,146.54,64.12,147.8Zm182-8.91A67.76,67.76,0,0,0,219,117.51a40,40,0,1,0-66.46-35.8,3.94,3.94,0,0,0,2.27,4.18A64.08,64.08,0,0,1,192,144c0,1.28,0,2.54-.12,3.8a4,4,0,0,0,4,4.2H240a8,8,0,0,0,7.8-6.17A8.33,8.33,0,0,0,246.17,138.89Zm-89,43.18a48,48,0,1,0-58.37,0A72.13,72.13,0,0,0,65.07,212,8,8,0,0,0,72,224H184a8,8,0,0,0,6.93-12A72.15,72.15,0,0,0,157.19,182.07Z",
  buildings:"M239.73,208H224V96a16,16,0,0,0-16-16H164a4,4,0,0,0-4,4V208H144V32.41a16.43,16.43,0,0,0-6.16-13,16,16,0,0,0-18.72-.69L39.12,72A16,16,0,0,0,32,85.34V208H16.27A8.18,8.18,0,0,0,8,215.47,8,8,0,0,0,16,224H240a8,8,0,0,0,8-8.53A8.18,8.18,0,0,0,239.73,208ZM76,184a8,8,0,0,1-8.53,8A8.18,8.18,0,0,1,60,183.72V168.27A8.19,8.19,0,0,1,67.47,160,8,8,0,0,1,76,168Zm0-56a8,8,0,0,1-8.53,8A8.19,8.19,0,0,1,60,127.72V112.27A8.19,8.19,0,0,1,67.47,104,8,8,0,0,1,76,112Zm40,56a8,8,0,0,1-8.53,8,8.18,8.18,0,0,1-7.47-8.26V168.27a8.19,8.19,0,0,1,7.47-8.26,8,8,0,0,1,8.53,8Zm0-56a8,8,0,0,1-8.53,8,8.19,8.19,0,0,1-7.47-8.26V112.27a8.19,8.19,0,0,1,7.47-8.26,8,8,0,0,1,8.53,8Z",
  laptop:"M232,168h-8V72a24,24,0,0,0-24-24H56A24,24,0,0,0,32,72v96H24a8,8,0,0,0-8,8v16a24,24,0,0,0,24,24H216a24,24,0,0,0,24-24V176A8,8,0,0,0,232,168ZM112,72h32a8,8,0,0,1,0,16H112a8,8,0,0,1,0-16ZM224,192a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8v-8H224Z",
  desktop:"M208,40H48A24,24,0,0,0,24,64V176a24,24,0,0,0,24,24h72v16H96a8,8,0,0,0,0,16h64a8,8,0,0,0,0-16H136V200h72a24,24,0,0,0,24-24V64A24,24,0,0,0,208,40Zm0,144H48a8,8,0,0,1-8-8V160H216v16A8,8,0,0,1,208,184Z",
  monitor:"M232,64V176a24,24,0,0,1-24,24H48a24,24,0,0,1-24-24V64A24,24,0,0,1,48,40H208A24,24,0,0,1,232,64ZM160,216H96a8,8,0,0,0,0,16h64a8,8,0,0,0,0-16Z",
  floppy:"M219.31,72,184,36.69A15.86,15.86,0,0,0,172.69,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V83.31A15.86,15.86,0,0,0,219.31,72ZM208,208H184V152a16,16,0,0,0-16-16H88a16,16,0,0,0-16,16v56H48V48H172.69L208,83.31ZM160,72a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h56A8,8,0,0,1,160,72Z",
  chats:"M232.07,186.76a80,80,0,0,0-62.5-114.17A80,80,0,1,0,23.93,138.76l-7.27,24.71a16,16,0,0,0,19.87,19.87l24.71-7.27a80.39,80.39,0,0,0,25.18,7.35,80,80,0,0,0,108.34,40.65l24.71,7.27a16,16,0,0,0,19.87-19.86Zm-16.25,1.47L224,216l-27.76-8.17a8,8,0,0,0-6,.63,64.05,64.05,0,0,1-85.87-24.88A79.93,79.93,0,0,0,174.7,89.71a64,64,0,0,1,41.75,92.48A8,8,0,0,0,215.82,188.23Z"
};
var ICON_DRAW = {
  maths:function(c,s){ _tx(c,s,'π',0.88,0.57); },
  stats:function(c,s){ /* pie chart — disc with a clear pizza-slice wedge removed */
    var cx=s*0.5,cy=s*0.5,R=s*0.34; _dc(c,cx,cy,R);
    _hole(c,function(){ c.beginPath();c.moveTo(cx,cy);c.arc(cx,cy,R+3,-0.32*Math.PI,0.06*Math.PI);c.closePath();c.fill(); });
    _hole(c,function(){ c.save();c.lineWidth=s*0.022;c.strokeStyle='#000';
      c.beginPath();c.moveTo(cx,cy);c.lineTo(cx+Math.cos(0.62*Math.PI)*R,cy+Math.sin(0.62*Math.PI)*R);c.stroke();
      c.beginPath();c.moveTo(cx,cy);c.lineTo(cx+Math.cos(1.25*Math.PI)*R,cy+Math.sin(1.25*Math.PI)*R);c.stroke();c.restore(); });
  },
  englang:function(c,s){ _tx(c,s,'Aa',0.5,0.56); },
  englit:function(c,s){ /* open book — pages splay UP-and-out to a V (valley at the spine) */
    var mx=s*0.5;
    c.beginPath();c.moveTo(mx,s*0.45);c.lineTo(s*0.1,s*0.28);c.lineTo(s*0.1,s*0.6);c.lineTo(mx,s*0.72);c.closePath();c.fill();
    c.beginPath();c.moveTo(mx,s*0.45);c.lineTo(s*0.9,s*0.28);c.lineTo(s*0.9,s*0.6);c.lineTo(mx,s*0.72);c.closePath();c.fill();
  },
  science:function(c,s){ var nx=s*0.42,nw=s*0.16,ny=s*0.14; c.fillRect(nx,ny,nw,s*0.2); c.beginPath();c.moveTo(nx,ny+s*0.18);c.lineTo(nx+nw,ny+s*0.18);c.lineTo(s*0.82,s*0.82);c.lineTo(s*0.18,s*0.82);c.closePath();c.fill(); c.fillRect(s*0.16,s*0.8,s*0.68,s*0.06); },
  sciences:function(c,s){ /* atom — nucleus + 3 crossing orbit rings */
    var cx=s*0.5,cy=s*0.5; _dc(c,cx,cy,s*0.085);
    c.save();c.lineWidth=s*0.038;c.strokeStyle=c.fillStyle;
    for(var i=0;i<3;i++){ c.save();c.translate(cx,cy);c.rotate(i*Math.PI/3);c.beginPath();c.ellipse(0,0,s*0.36,s*0.145,0,0,6.2832);c.stroke();c.restore(); }
    c.restore();
  },
  history:function(c,s){ var m=s*0.2; _tri(c,[m,m],[s-m,m],[s*0.5,s*0.5]); _tri(c,[s*0.5,s*0.5],[s-m,s-m],[m,s-m]); c.fillRect(m*0.7,m*0.55,s-m*1.4,s*0.055); c.fillRect(m*0.7,s-m*0.55-s*0.055,s-m*1.4,s*0.055); },
  geography:function(c,s){ var b=s*0.8; _tri(c,[s*0.06,b],[s*0.4,s*0.24],[s*0.66,b]); _tri(c,[s*0.46,b],[s*0.74,s*0.4],[s*0.96,b]); },
  geology:function(c,s){ var t=s*0.22; c.beginPath();c.moveTo(s*0.3,t);c.lineTo(s*0.7,t);c.lineTo(s*0.88,s*0.42);c.lineTo(s*0.5,s*0.86);c.lineTo(s*0.12,s*0.42);c.closePath();c.fill(); },
  astronomy:function(c,s){ _dc(c,s*0.46,s*0.5,s*0.32); _hole(c,function(){_dc(c,s*0.6,s*0.42,s*0.28);}); var sx=s*0.78,sy=s*0.26,r=s*0.1; c.fillRect(sx-s*0.018,sy-r,s*0.036,r*2); c.fillRect(sx-r,sy-s*0.018,r*2,s*0.036); },
  re:function(c,s){ /* Christian cross */ c.fillRect(s*0.43,s*0.15,s*0.14,s*0.7); c.fillRect(s*0.27,s*0.34,s*0.46,s*0.14); },
  psychology:function(c,s){ /* light bulb — ideas / the mind */
    _dc(c,s*0.5,s*0.41,s*0.26);                    // bulb
    c.fillRect(s*0.41,s*0.58,s*0.18,s*0.09);       // neck
    _rr(c,s*0.41,s*0.66,s*0.18,s*0.08,s*0.02);     // screw band 1
    _rr(c,s*0.43,s*0.745,s*0.14,s*0.07,s*0.02);    // screw band 2
    c.fillRect(s*0.45,s*0.815,s*0.1,s*0.05);       // base tip
  },
  sociology:function(c,s){ /* two speech bubbles — conversation / society (separated, pronounced tails) */
    _rr(c, s*0.1, s*0.13, s*0.42, s*0.29, s*0.07);                                  // bubble 1 (upper-left)
    c.beginPath();c.moveTo(s*0.18,s*0.42);c.lineTo(s*0.12,s*0.58);c.lineTo(s*0.34,s*0.42);c.closePath();c.fill();  // tail down-left
    _rr(c, s*0.5, s*0.5, s*0.4, s*0.26, s*0.07);                                     // bubble 2 (lower-right)
    c.beginPath();c.moveTo(s*0.66,s*0.76);c.lineTo(s*0.84,s*0.76);c.lineTo(s*0.8,s*0.92);c.closePath();c.fill();   // tail down-right
  },
  citizenship:function(c,s){ c.fillRect(s*0.48,s*0.18,s*0.04,s*0.56); c.fillRect(s*0.3,s*0.74,s*0.4,s*0.05); c.fillRect(s*0.2,s*0.26,s*0.6,s*0.04); function pan(x){c.beginPath();c.arc(x,s*0.42,s*0.12,0,Math.PI);c.closePath();c.fill();c.fillRect(x-s*0.001,s*0.28,s*0.002,s*0.14);} pan(s*0.24); pan(s*0.76); _dc(c,s*0.5,s*0.2,s*0.05); },
  business:function(c,s){ _rr(c,s*0.14,s*0.34,s*0.72,s*0.46,s*0.05); c.fillRect(s*0.38,s*0.24,s*0.24,s*0.12); _hole(c,function(){c.fillRect(s*0.4,s*0.26,s*0.2,s*0.08);}); _hole(c,function(){c.fillRect(s*0.14,s*0.52,s*0.72,s*0.05);}); },
  economics:function(c,s){ /* big bold pound sign (UK currency) */ _tx(c,s,'£',0.96,0.55); },
  enterprise:function(c,s){ /* rocket — cleaner, bolder, solid capsule */
    c.beginPath();
    c.moveTo(s*0.5,s*0.12);
    c.quadraticCurveTo(s*0.67,s*0.26,s*0.67,s*0.46);
    c.lineTo(s*0.67,s*0.64); c.lineTo(s*0.33,s*0.64); c.lineTo(s*0.33,s*0.46);
    c.quadraticCurveTo(s*0.33,s*0.26,s*0.5,s*0.12); c.closePath();c.fill();
    _tri(c,[s*0.33,s*0.5],[s*0.18,s*0.74],[s*0.33,s*0.66]);          // left fin
    _tri(c,[s*0.67,s*0.5],[s*0.82,s*0.74],[s*0.67,s*0.66]);          // right fin
    c.beginPath();c.moveTo(s*0.42,s*0.64);c.quadraticCurveTo(s*0.5,s*0.92,s*0.58,s*0.64);c.closePath();c.fill(); // flame
    _hole(c,function(){_dc(c,s*0.5,s*0.38,s*0.072);});               // window
  },
  retail:function(c,s){ _rr(c,s*0.2,s*0.34,s*0.6,s*0.5,s*0.05); _hole(c,function(){c.save();c.lineWidth=s*0.06;c.strokeStyle='#000';c.beginPath();c.arc(s*0.5,s*0.34,s*0.13,Math.PI,2*Math.PI);c.stroke();c.restore();}); c.save();c.lineWidth=s*0.055;c.strokeStyle=c.fillStyle;c.beginPath();c.arc(s*0.5,s*0.36,s*0.13,Math.PI,2*Math.PI);c.stroke();c.restore(); },
  cs:function(c,s){ _tx(c,s,'</>',0.34,0.56); },
  it:_svg(_PH.floppy),                /* IT — Phosphor floppy disk */
  imedia:function(c,s){ c.beginPath();c.moveTo(s*0.3,s*0.2);c.lineTo(s*0.3,s*0.78);c.lineTo(s*0.44,s*0.64);c.lineTo(s*0.54,s*0.86);c.lineTo(s*0.64,s*0.82);c.lineTo(s*0.54,s*0.6);c.lineTo(s*0.74,s*0.6);c.closePath();c.fill(); },
  media:function(c,s){ /* retro TV with antenna — broadcast media */
    c.save();c.lineWidth=s*0.03;c.strokeStyle=c.fillStyle;c.lineCap='round';
    c.beginPath();c.moveTo(s*0.5,s*0.44);c.lineTo(s*0.35,s*0.16);c.moveTo(s*0.5,s*0.44);c.lineTo(s*0.65,s*0.16);c.stroke();c.restore();
    _rr(c,s*0.17,s*0.42,s*0.66,s*0.4,s*0.05);
    _hole(c,function(){_rr(c,s*0.22,s*0.47,s*0.42,s*0.3,s*0.03);});
    _dc(c,s*0.74,s*0.53,s*0.022); _dc(c,s*0.74,s*0.63,s*0.022);
    c.fillRect(s*0.27,s*0.82,s*0.05,s*0.06); c.fillRect(s*0.68,s*0.82,s*0.05,s*0.06);
  },
  film:function(c,s){ c.save();c.translate(s*0.5,s*0.56);c.rotate(-0.06);c.translate(-s*0.5,-s*0.56); c.fillRect(s*0.14,s*0.46,s*0.72,s*0.34); c.beginPath();c.moveTo(s*0.14,s*0.44);c.lineTo(s*0.86,s*0.32);c.lineTo(s*0.86,s*0.2);c.lineTo(s*0.14,s*0.32);c.closePath();c.fill(); _hole(c,function(){for(var i=0;i<4;i++){var x=s*(0.2+i*0.18);c.beginPath();c.moveTo(x,s*0.42);c.lineTo(x+s*0.06,s*0.3);c.lineTo(x+s*0.1,s*0.3);c.lineTo(x+s*0.04,s*0.42);c.closePath();c.fill();}}); c.restore(); },
  drama:function(c,s){ c.beginPath();c.moveTo(s*0.22,s*0.26);c.lineTo(s*0.78,s*0.26);c.bezierCurveTo(s*0.78,s*0.7,s*0.64,s*0.84,s*0.5,s*0.84);c.bezierCurveTo(s*0.36,s*0.84,s*0.22,s*0.7,s*0.22,s*0.26);c.closePath();c.fill(); _hole(c,function(){_dc(c,s*0.38,s*0.44,s*0.06);_dc(c,s*0.62,s*0.44,s*0.06);c.save();c.beginPath();c.arc(s*0.5,s*0.58,s*0.14,0.15*Math.PI,0.85*Math.PI);c.lineWidth=s*0.05;c.strokeStyle='#000';c.stroke();c.restore();}); },
  music:function(c,s){ _dc(c,s*0.36,s*0.74,s*0.13); c.fillRect(s*0.47,s*0.2,s*0.05,s*0.56); c.beginPath();c.moveTo(s*0.52,s*0.2);c.quadraticCurveTo(s*0.78,s*0.28,s*0.7,s*0.5);c.quadraticCurveTo(s*0.74,s*0.32,s*0.52,s*0.32);c.closePath();c.fill(); },
  pe:function(c,s){ /* dumbbell — bold: thick bar + chunky weight blocks */
    c.fillRect(s*0.32,s*0.42,s*0.36,s*0.16);                        // thick bar
    _rr(c,s*0.1,s*0.26,s*0.15,s*0.48,s*0.04);                       // left weight
    _rr(c,s*0.75,s*0.26,s*0.15,s*0.48,s*0.04);                      // right weight
    _rr(c,s*0.24,s*0.34,s*0.08,s*0.32,s*0.02);                      // left collar
    _rr(c,s*0.68,s*0.34,s*0.08,s*0.32,s*0.02);                      // right collar
  },
  sport:function(c,s){ c.beginPath();c.moveTo(s*0.3,s*0.2);c.lineTo(s*0.7,s*0.2);c.lineTo(s*0.66,s*0.46);c.bezierCurveTo(s*0.64,s*0.56,s*0.36,s*0.56,s*0.34,s*0.46);c.closePath();c.fill(); c.save();c.lineWidth=s*0.045;c.strokeStyle=c.fillStyle; c.beginPath();c.arc(s*0.3,s*0.28,s*0.1,0.5*Math.PI,1.5*Math.PI,true);c.stroke(); c.beginPath();c.arc(s*0.7,s*0.28,s*0.1,1.5*Math.PI,0.5*Math.PI,true);c.stroke();c.restore(); c.fillRect(s*0.46,s*0.54,s*0.08,s*0.14); c.fillRect(s*0.36,s*0.68,s*0.28,s*0.07); c.fillRect(s*0.32,s*0.75,s*0.36,s*0.07); },
  food:function(c,s){ /* fork & knife (shared with Hospitality, per Tom) — food / catering */
    var fx=s*0.36;
    c.fillRect(fx-s*0.025,s*0.42,s*0.05,s*0.42);
    for(var i=0;i<3;i++){c.fillRect(fx-s*0.06+i*s*0.05,s*0.16,s*0.024,s*0.17);}
    _rr(c,fx-s*0.06,s*0.3,s*0.12,s*0.07,s*0.02);
    var kx=s*0.64;
    c.fillRect(kx-s*0.02,s*0.46,s*0.045,s*0.38);
    c.beginPath();c.moveTo(kx-s*0.035,s*0.16);c.quadraticCurveTo(kx+s*0.07,s*0.22,kx+s*0.025,s*0.48);c.lineTo(kx-s*0.035,s*0.48);c.closePath();c.fill();
  },
  hospitality:function(c,s){ /* fork & knife — catering / dining */
    var fx=s*0.36;
    c.fillRect(fx-s*0.025,s*0.42,s*0.05,s*0.42);
    for(var i=0;i<3;i++){c.fillRect(fx-s*0.06+i*s*0.05,s*0.16,s*0.024,s*0.17);}
    _rr(c,fx-s*0.06,s*0.3,s*0.12,s*0.07,s*0.02);
    var kx=s*0.64;
    c.fillRect(kx-s*0.02,s*0.46,s*0.045,s*0.38);
    c.beginPath();c.moveTo(kx-s*0.035,s*0.16);c.quadraticCurveTo(kx+s*0.07,s*0.22,kx+s*0.025,s*0.48);c.lineTo(kx-s*0.035,s*0.48);c.closePath();c.fill();
  },
  dt:function(c,s){ c.save();c.translate(s*0.5,s*0.5);c.rotate(0.7);c.translate(-s*0.5,-s*0.5); c.fillRect(s*0.46,s*0.3,s*0.08,s*0.5); _rr(c,s*0.3,s*0.22,s*0.4,s*0.16,s*0.04); c.restore(); },
  engineering:function(c,s){ /* big open-ended spanner gripping a bolt */
    c.save();c.translate(s*0.5,s*0.5);c.rotate(-0.66);c.translate(-s*0.5,-s*0.5);
    _rr(c,s*0.44,s*0.4,s*0.12,s*0.46,s*0.04);                       // handle
    c.beginPath();c.arc(s*0.5,s*0.3,s*0.16,0,6.2832);c.fill();      // head (solid disc)
    _hole(c,function(){ _dc(c,s*0.5,s*0.3,s*0.07);                  // bolt hole
      c.fillRect(s*0.428,s*0.07,s*0.144,s*0.26); });                // open-jaw slot cut to the top
    c.restore();
  },
  electronics:function(c,s){ /* lightning bolt — electronics / electric */
    c.beginPath();
    c.moveTo(s*0.58,s*0.1);c.lineTo(s*0.28,s*0.54);c.lineTo(s*0.46,s*0.54);c.lineTo(s*0.4,s*0.9);
    c.lineTo(s*0.74,s*0.42);c.lineTo(s*0.55,s*0.42);c.lineTo(s*0.64,s*0.1);c.closePath();c.fill();
  },
  construction:function(c,s){ /* traffic cone — construction site / built environment */
    c.beginPath();c.moveTo(s*0.43,s*0.2);c.lineTo(s*0.57,s*0.2);c.lineTo(s*0.74,s*0.78);c.lineTo(s*0.26,s*0.78);c.closePath();c.fill(); // cone body
    _rr(c,s*0.43,s*0.13,s*0.14,s*0.08,s*0.03);          // top knob
    _rr(c,s*0.14,s*0.78,s*0.72,s*0.09,s*0.03);          // base slab
    _hole(c,function(){ c.beginPath();c.moveTo(s*0.35,s*0.46);c.lineTo(s*0.65,s*0.46);c.lineTo(s*0.685,s*0.58);c.lineTo(s*0.315,s*0.58);c.closePath();c.fill(); }); // reflective stripe
  },
  hsc:function(c,s){ c.beginPath();c.moveTo(s*0.5,s*0.8);c.bezierCurveTo(s*0.1,s*0.52,s*0.22,s*0.2,s*0.5,s*0.4);c.bezierCurveTo(s*0.78,s*0.2,s*0.9,s*0.52,s*0.5,s*0.8);c.closePath();c.fill(); },
  childdev:function(c,s){ /* toy building blocks (shape-sorter) — early years / child play */
    _rr(c,s*0.13,s*0.5,s*0.35,s*0.35,s*0.04);                                  // bottom-left block
    _hole(c,function(){_dc(c,s*0.305,s*0.675,s*0.1);});                        // circle cut
    _rr(c,s*0.52,s*0.5,s*0.35,s*0.35,s*0.04);                                  // bottom-right block
    _hole(c,function(){c.beginPath();c.moveTo(s*0.695,s*0.57);c.lineTo(s*0.6,s*0.76);c.lineTo(s*0.79,s*0.76);c.closePath();c.fill();}); // triangle cut
    _rr(c,s*0.325,s*0.14,s*0.35,s*0.35,s*0.04);                                // top block
    _hole(c,function(){_rr(c,s*0.42,s*0.235,s*0.16,s*0.16,s*0.02);});          // square cut
  },
  classics:function(c,s){ c.fillRect(s*0.2,s*0.18,s*0.6,s*0.08); c.fillRect(s*0.26,s*0.26,s*0.48,s*0.06); for(var i=0;i<4;i++){c.fillRect(s*(0.3+i*0.12),s*0.32,s*0.07,s*0.46);} c.fillRect(s*0.24,s*0.78,s*0.52,s*0.07); c.fillRect(s*0.18,s*0.85,s*0.64,s*0.07); },
  language:function(c,s){ _rr(c,s*0.14,s*0.2,s*0.72,s*0.5,s*0.1); c.beginPath();c.moveTo(s*0.3,s*0.68);c.lineTo(s*0.3,s*0.86);c.lineTo(s*0.48,s*0.68);c.closePath();c.fill(); _hole(c,function(){_dc(c,s*0.36,s*0.45,s*0.04);_dc(c,s*0.5,s*0.45,s*0.04);_dc(c,s*0.64,s*0.45,s*0.04);}); },
  _default:function(c,s){ var t=s*0.27,b=s*0.77,mx=s*0.5; c.beginPath();c.moveTo(mx,t);c.lineTo(s*0.13,t*1.4);c.lineTo(s*0.13,b);c.lineTo(mx,b*0.9);c.closePath();c.fill(); c.beginPath();c.moveTo(mx,t);c.lineTo(s*0.87,t*1.4);c.lineTo(s*0.87,b);c.lineTo(mx,b*0.9);c.closePath();c.fill(); }
};
