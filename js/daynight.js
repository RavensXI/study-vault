/* ============ Day and night, shared by the homepage, the builder and the dashboard ============
   Night is when the sun is down over the UK today: sunrise and sunset worked out from the date
   (after Meeus, by way of SunCalc) for the middle of the UK (54N 2.5W), so no location is asked.
   ?time=day or ?time=night in the address overrides it, for looking at both.
   window.SVDayNight = { isNight(), sunTimes(date) -> [riseMs, setMs] } */
(function(){
  function sunTimes(date){
    var rad=Math.PI/180, dayMs=864e5, J1970=2440588, J2000=2451545, J0=.0009, e=rad*23.4397;
    var lat=54.0*rad, lw=rad*2.5;
    var d=date.valueOf()/dayMs-.5+J1970-J2000;
    var n=Math.round(d-J0-lw/(2*Math.PI)), ds=J0+lw/(2*Math.PI)+n;
    var M=rad*(357.5291+.98560028*ds);
    var L=M+rad*(1.9148*Math.sin(M)+.02*Math.sin(2*M)+.0003*Math.sin(3*M))+rad*102.9372+Math.PI;
    var dec=Math.asin(Math.sin(e)*Math.sin(L));
    var noon=J2000+ds+.0053*Math.sin(M)-.0069*Math.sin(2*L);
    var w=Math.acos((Math.sin(-.833*rad)-Math.sin(lat)*Math.sin(dec))/(Math.cos(lat)*Math.cos(dec)));
    var set=J2000+J0+(w+lw)/(2*Math.PI)+n+.0053*Math.sin(M)-.0069*Math.sin(2*L), rise=noon-(set-noon);
    var ms=function(j){ return (j+.5-J1970)*dayMs; };
    return [ms(rise),ms(set)];
  }
  function isNight(){
    var t=null; try{ t=new URLSearchParams(location.search).get('time'); }catch(e){}
    if(t==='night') return true; if(t==='day') return false;
    var now=Date.now(), st=sunTimes(new Date()); return now<st[0]||now>st[1];
  }
  window.SVDayNight={ isNight:isNight, sunTimes:sunTimes };
})();
