var W = {
  meta: {
    id: 'ohms-law-circuit-lab',
    title: 'Voltage & Resistance: Watch Current Change',
    teaches: 'Current is directly proportional to voltage and inversely proportional to resistance (V = IR)'
  },

  initialState: function () {
    return { voltage: 6, resistance: 20 };
  },

  apply: function (state, action) {
    var s = { voltage: state.voltage, resistance: state.resistance };
    if (!action) return s;
    if (action.t === 'set') {
      if (action.key === 'voltage') {
        var v = action.v;
        if (typeof v !== 'number' || v !== v) v = s.voltage;
        if (v < 0) v = 0;
        if (v > 12) v = 12;
        s.voltage = v;
      } else if (action.key === 'resistance') {
        var r = action.v;
        if (typeof r !== 'number' || r !== r) r = s.resistance;
        if (r < 1) r = 1;
        if (r > 100) r = 100;
        s.resistance = r;
      }
    } else if (action.t === 'reset') {
      s.voltage = 6;
      s.resistance = 20;
    }
    return s;
  },

  derive: function (state) {
    var V = state.voltage;
    var R = state.resistance;
    if (typeof R !== 'number' || R <= 0 || R !== R) R = 1e-9;
    var current = V / R;
    if (current !== current || current < 0) current = 0;
    var power = V * current;
    if (power !== power || power < 0) power = 0;
    var dotSpeedRaw = current * 1.4;
    var dotSpeed = dotSpeedRaw;
    if (dotSpeed > 7) dotSpeed = 7;
    if (dotSpeed < 0) dotSpeed = 0;
    return { current: current, power: power, dotSpeed: dotSpeed };
  },

  regions: function (state, w, h) {
    return [];
  },

  controls: [
    { key: 'voltage', label: 'Supply voltage', min: 0, max: 12, step: 0.5, value: 6, unit: 'V' },
    { key: 'resistance', label: 'Resistance', min: 1, max: 100, step: 1, value: 20, unit: '\u03a9' }
  ],

  render: function (ctx, state, derived, w, h, acc) {
    var ink = '#2d2a26';
    var muted = '#8d8880';
    var grid = '#e8e2d9';
    var accent = acc || '#c0562b';

    ctx.save();
    ctx.fillStyle = '#faf7f2';
    ctx.fillRect(0, 0, w, h);

    // ----- circuit loop geometry -----
    var margin = w * 0.12;
    var x0 = margin;
    var x1 = w - margin;
    var y0 = h * 0.22;
    var y1 = h * 0.72;

    ctx.strokeStyle = ink;
    ctx.lineWidth = 2;

    // top wire (with ammeter in the middle)
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(w * 0.42, y0);
    ctx.moveTo(w * 0.58, y0);
    ctx.lineTo(x1, y0);
    ctx.stroke();

    // right wire (resistor)
    ctx.beginPath();
    ctx.moveTo(x1, y0);
    ctx.lineTo(x1, y0 + (y1 - y0) * 0.28);
    ctx.moveTo(x1, y0 + (y1 - y0) * 0.72);
    ctx.lineTo(x1, y1);
    ctx.stroke();

    // bottom wire (with bulb)
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(w * 0.58, y1);
    ctx.moveTo(w * 0.42, y1);
    ctx.lineTo(x0, y1);
    ctx.stroke();

    // left wire (battery)
    ctx.beginPath();
    ctx.moveTo(x0, y1);
    ctx.lineTo(x0, y0 + (y1 - y0) * 0.62);
    ctx.moveTo(x0, y0 + (y1 - y0) * 0.38);
    ctx.lineTo(x0, y0);
    ctx.stroke();

    // ----- battery (cell count reflects voltage) -----
    var cellCount = Math.max(1, Math.min(4, Math.round(state.voltage / 3) + 1));
    var bMidY = y0 + (y1 - y0) * 0.5;
    var bHeight = (y1 - y0) * 0.24;
    var cellSpacing = bHeight / cellCount;
    ctx.save();
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2.5;
    for (var i = 0; i < cellCount; i++) {
      var cy = bMidY - bHeight / 2 + i * cellSpacing + cellSpacing / 2;
      // long line (positive)
      ctx.beginPath();
      ctx.moveTo(x0 - 10, cy - cellSpacing * 0.28);
      ctx.lineTo(x0 + 10, cy - cellSpacing * 0.28);
      ctx.stroke();
      // short thick line (negative)
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.moveTo(x0 - 6, cy + cellSpacing * 0.05);
      ctx.lineTo(x0 + 6, cy + cellSpacing * 0.05);
      ctx.stroke();
      ctx.lineWidth = 2.5;
    }
    ctx.restore();
    ctx.fillStyle = muted;
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(state.voltage.toFixed(1) + ' V', x0 - 34, bMidY);

    // ----- resistor coil (zigzag density reflects resistance) -----
    var rTop = y0 + (y1 - y0) * 0.28;
    var rBot = y0 + (y1 - y0) * 0.72;
    var rHeight = rBot - rTop;
    var zigs = Math.max(3, Math.min(12, Math.round(state.resistance / 9) + 3));
    var zigW = 12;
    ctx.beginPath();
    ctx.moveTo(x1, rTop);
    var seg = rHeight / zigs;
    for (var z = 0; z < zigs; z++) {
      var yMid = rTop + seg * (z + 0.5);
      var dir = (z % 2 === 0) ? -1 : 1;
      ctx.lineTo(x1 + dir * zigW, yMid);
    }
    ctx.lineTo(x1, rBot);
    ctx.stroke();
    ctx.save();
    ctx.translate(x1 + 26, (rTop + rBot) / 2);
    ctx.rotate(Math.PI / 2);
    ctx.fillStyle = muted;
    ctx.textAlign = 'center';
    ctx.fillText(Math.round(state.resistance) + ' \u03a9', 0, 0);
    ctx.restore();

    // ----- ammeter dial (top wire) -----
    var ax = w * 0.5;
    var ay = y0;
    var ammRadius = Math.min(w, h) * 0.075;
    var maxDisplayCurrent = 5; // dial full-scale, values beyond this pin the needle
    var frac = derived.current / maxDisplayCurrent;
    if (frac > 1) frac = 1;
    if (frac < 0) frac = 0;
    var needleAngle = Math.PI * (1 - frac) ; // 0..pi sweep, left=0A right=max

    ctx.beginPath();
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2;
    ctx.arc(ax, ay, ammRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // scale arc
    ctx.beginPath();
    ctx.strokeStyle = grid;
    ctx.lineWidth = 4;
    ctx.arc(ax, ay, ammRadius - 6, Math.PI, 0, false);
    ctx.stroke();

    // needle
    var needleLen = ammRadius - 8;
    var nx = ax - Math.cos(needleAngle) * needleLen;
    var ny = ay - Math.sin(needleAngle) * needleLen;
    ctx.beginPath();
    ctx.strokeStyle = accent;
    ctx.lineWidth = 2.5;
    ctx.moveTo(ax, ay);
    ctx.lineTo(nx, ny);
    ctx.stroke();
    ctx.beginPath();
    ctx.fillStyle = ink;
    ctx.arc(ax, ay, 2.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = ink;
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('A', ax, ay + ammRadius + 16);
    ctx.font = '11px sans-serif';
    ctx.fillStyle = muted;
    ctx.fillText(derived.current.toFixed(2) + ' A', ax, ay + ammRadius + 30);

    // ----- bulb (bottom wire, glow reflects power) -----
    var bx = w * 0.5;
    var by = y1;
    var bulbR = Math.min(w, h) * 0.06;
    var maxPower = 60; // reference bulb rating for full brightness
    var brightness = derived.power / maxPower;
    if (brightness > 1) brightness = 1;
    if (brightness < 0) brightness = 0;

    // glow halo
    if (brightness > 0.02) {
      var haloR = bulbR * (1.6 + brightness * 1.4);
      ctx.beginPath();
      ctx.fillStyle = 'rgba(230,180,60,' + (0.12 + brightness * 0.35) + ')';
      ctx.arc(bx, by, haloR, 0, Math.PI * 2);
      ctx.fill();
    }

    var glowVal = Math.round(230 - brightness * 30);
    ctx.beginPath();
    ctx.fillStyle = 'rgb(' + glowVal + ',' + Math.round(210 - brightness * 10 + brightness * 30) + ',' + Math.round(120 - brightness * 60 + 60) + ')';
    ctx.fillStyle = 'rgba(255,' + Math.round(200 + brightness * 40) + ',' + Math.round(80 + brightness * 60) + ',' + (0.5 + brightness * 0.5) + ')';
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2;
    ctx.arc(bx, by, bulbR, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // filament
    ctx.beginPath();
    ctx.strokeStyle = brightness > 0.4 ? '#7a4a10' : muted;
    ctx.lineWidth = 1.5;
    ctx.moveTo(bx - bulbR * 0.4, by + bulbR * 0.3);
    ctx.lineTo(bx - bulbR * 0.1, by - bulbR * 0.3);
    ctx.lineTo(bx + bulbR * 0.1, by + bulbR * 0.3);
    ctx.lineTo(bx + bulbR * 0.4, by - bulbR * 0.3);
    ctx.stroke();

    ctx.fillStyle = muted;
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(derived.power.toFixed(1) + ' W', bx, by + bulbR + 18);

    // ----- moving charge dots along the loop -----
    var perim = 2 * (x1 - x0) + 2 * (y1 - y0);
    var t = (typeof acc === 'number' ? acc : 0) * derived.dotSpeed * 18;
    var nDots = 10;
    ctx.fillStyle = accent;
    for (var d = 0; d < nDots; d++) {
      var dist = (t + (perim / nDots) * d) % perim;
      var p = pointOnLoop(dist, x0, y0, x1, y1);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 3.2, 0, Math.PI * 2);
      ctx.fill();
    }

    // ----- Ohm's law readout -----
    ctx.fillStyle = ink;
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('V = I \u00d7 R', 14, h - 14);
    ctx.font = '12px sans-serif';
    ctx.fillStyle = muted;
    ctx.fillText(
      state.voltage.toFixed(1) + ' V = ' + derived.current.toFixed(2) + ' A \u00d7 ' + Math.round(state.resistance) + ' \u03a9',
      110, h - 14
    );

    ctx.restore();

    function pointOnLoop(dist, x0, y0, x1, y1) {
      var topLen = x1 - x0;
      var rightLen = y1 - y0;
      var botLen = x1 - x0;
      var leftLen = y1 - y0;
      var d = dist;
      if (d < topLen) return { x: x0 + d, y: y0 };
      d -= topLen;
      if (d < rightLen) return { x: x1, y: y0 + d };
      d -= rightLen;
      if (d < botLen) return { x: x1 - d, y: y1 };
      d -= botLen;
      if (d < leftLen) return { x: x0, y: y1 - d };
      return { x: x0, y: y0 };
    }
  },

  caption: function (state, derived) {
    var v = state.voltage.toFixed(1);
    var r = Math.round(state.resistance);
    var i = derived.current.toFixed(2);
    if (state.voltage === 0) {
      return 'With no voltage across the circuit, no current flows: I = V/R = 0/' + r + ' = 0 A.';
    }
    return 'I = V/R = ' + v + '/' + r + ' = ' + i + ' A \u2014 raise the voltage and current rises; raise the resistance and current falls.';
  }
};

if (typeof module !== 'undefined') module.exports = W;