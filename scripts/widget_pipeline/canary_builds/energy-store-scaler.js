/* SV Widget */
var W = {
  meta: {
    id: 'energy-store-scaler',
    title: 'Squash the Ball: KE vs GPE Scaling',
    teaches: 'Kinetic energy scales with the square of speed, while gravitational potential energy scales linearly with mass and height',
    kind: 'explore'
  },

  controls: [
    { key: 'mass',   label: 'Mass of ball',        min: 1, max: 10, step: 1, value: 2,  unit: 'kg' },
    { key: 'height', label: 'Height above ground', min: 0, max: 20, step: 1, value: 5,  unit: 'm' },
    { key: 'speed',  label: 'Speed of ball',       min: 0, max: 20, step: 1, value: 10, unit: 'm/s' }
  ],

  derive: function (p) {
    var m = p.mass, hh = p.height, v = p.speed;
    var g = 10;
    var ke = 0.5 * m * v * v;
    var gpe = m * g * hh;
    return {
      ke: ke,
      gpe: gpe,
      total: ke + gpe,
      keDoubledSpeed: 0.5 * m * (2 * v) * (2 * v),
      gpeDoubledHeight: m * g * (2 * hh)
    };
  },

  render: function (ctx, p, d, w, h, acc) {
    var ink = '#2d2a26', muted = '#8d8880', grid = '#e8e2d9';

    function fmt(v) {
      if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
      return v.toFixed(1);
    }

    ctx.clearRect(0, 0, w, h);
    ctx.lineWidth = 1;
    ctx.textBaseline = 'alphabetic';

    var sceneW = Math.max(115, Math.min(w * 0.40, 230));
    var yb = h - 46;            // baseline / ground
    var ytop = 56;              // top of bar area
    var sceneTop = 52;

    /* ---------- scene: ball at height ---------- */
    var bx = Math.round(sceneW * 0.44);
    var span = yb - sceneTop;
    var ballY = yb - (p.height / 20) * span;
    var r = 5 + 1.7 * p.mass;
    if (ballY - r < 8) ballY = 8 + r;

    // ground
    ctx.strokeStyle = ink;
    ctx.beginPath();
    ctx.moveTo(6, yb + 0.5);
    ctx.lineTo(sceneW - 6, yb + 0.5);
    ctx.stroke();
    ctx.strokeStyle = grid;
    for (var gx = 10; gx < sceneW - 6; gx += 9) {
      ctx.beginPath();
      ctx.moveTo(gx, yb + 1);
      ctx.lineTo(gx - 5, yb + 7);
      ctx.stroke();
    }

    // height line
    if (p.height > 0) {
      ctx.strokeStyle = muted;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(bx + 0.5, yb);
      ctx.lineTo(bx + 0.5, ballY);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // ball
    ctx.globalAlpha = 0.18;
    ctx.fillStyle = acc;
    ctx.beginPath();
    ctx.arc(bx, ballY, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.strokeStyle = acc;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(bx, ballY, r, 0, Math.PI * 2);
    ctx.stroke();
    ctx.lineWidth = 1;

    // speed arrow
    ctx.font = '11px system-ui, sans-serif';
    if (p.speed > 0) {
      var maxLen = Math.max(26, sceneW * 0.30);
      var len = (p.speed / 20) * maxLen;
      var ax = bx + r + 3, ay = ballY;
      ctx.strokeStyle = ink;
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(ax + len, ay);
      ctx.stroke();
      ctx.fillStyle = ink;
      ctx.beginPath();
      ctx.moveTo(ax + len + 6, ay);
      ctx.lineTo(ax + len, ay - 4);
      ctx.lineTo(ax + len, ay + 4);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = muted;
      ctx.textAlign = 'left';
      ctx.fillText('v = ' + p.speed + ' m/s', ax, ay - 9);
    } else {
      ctx.fillStyle = muted;
      ctx.textAlign = 'left';
      ctx.fillText('at rest', bx + r + 5, ballY + 4);
    }

    // labels in scene
    ctx.fillStyle = muted;
    ctx.textAlign = 'left';
    ctx.fillText('m = ' + p.mass + ' kg', bx - r, ballY + r + 13);
    if (p.height > 0) {
      ctx.fillText('h = ' + p.height + ' m', bx + 5, (yb + ballY) / 2 + 4);
    } else {
      ctx.fillText('h = 0 m', bx + 5, yb - 6);
    }
    ctx.fillText('g = 10 N/kg', 8, yb + 22);

    /* ---------- bars ---------- */
    var bx0 = sceneW + 14;
    var bw2 = w - bx0 - 10;
    var scaleMax = Math.max(d.keDoubledSpeed, d.gpeDoubledHeight, 200);
    var pxPerJ = (yb - ytop) / scaleMax;

    // gridlines
    ctx.strokeStyle = grid;
    for (var i = 1; i <= 4; i++) {
      var gy2 = Math.round(yb - (yb - ytop) * i / 4) + 0.5;
      ctx.beginPath();
      ctx.moveTo(bx0, gy2);
      ctx.lineTo(bx0 + bw2, gy2);
      ctx.stroke();
    }
    ctx.strokeStyle = ink;
    ctx.beginPath();
    ctx.moveTo(bx0, yb + 0.5);
    ctx.lineTo(bx0 + bw2, yb + 0.5);
    ctx.stroke();

    var bwid = Math.max(20, Math.min(54, bw2 / 4.5));

    function drawBar(cx, val, ghost, name, eq, ghostNote) {
      var hReal = val * pxPerJ;
      var hGhost = ghost * pxPerJ;
      var x = cx - bwid / 2;

      // ghost
      if (hGhost > 0.5) {
        ctx.globalAlpha = 0.13;
        ctx.fillStyle = acc;
        ctx.fillRect(x, yb - hGhost, bwid, hGhost);
        ctx.globalAlpha = 1;
        ctx.strokeStyle = acc;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(x, yb - hGhost + 0.5);
        ctx.lineTo(x + bwid, yb - hGhost + 0.5);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = muted;
        ctx.font = '10px system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(ghostNote + ' ' + fmt(ghost) + ' J',
                     cx, Math.max(46, yb - hGhost - 5));
      }

      // real bar
      if (hReal > 0.5) {
        ctx.fillStyle = acc;
        ctx.fillRect(x, yb - hReal, bwid, hReal);
      }

      // value
      ctx.fillStyle = ink;
      ctx.font = 'bold 12px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(fmt(val) + ' J', cx, yb - hReal - 6 > 44 ? yb - hReal - 6 : 44);

      // name + equation
      ctx.fillText(name, cx, yb + 16);
      ctx.fillStyle = muted;
      ctx.font = '10px system-ui, sans-serif';
      ctx.fillText(eq, cx, yb + 29);
    }

    drawBar(bx0 + bw2 * 0.28, d.ke, d.keDoubledSpeed, 'KE', 'Ek = 1/2 m v\u00b2', 'double v:');
    drawBar(bx0 + bw2 * 0.74, d.gpe, d.gpeDoubledHeight, 'GPE', 'Ep = m g h', 'double h:');

    // readout at top
    ctx.font = '11px system-ui, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = ink;
    ctx.fillText('Double the speed \u2192 KE \u00d7 4', bx0, 16);
    ctx.fillStyle = muted;
    ctx.fillText('Double the height (or mass) \u2192 that store \u00d7 2', bx0, 30);
    ctx.textAlign = 'right';
    ctx.fillStyle = ink;
    ctx.fillText('total = ' + fmt(d.total) + ' J', bx0 + bw2, 16);
  },

  caption: function (p, d) {
    function fmt(v) {
      if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
      return v.toFixed(1);
    }
    var head = 'm = ' + p.mass + ' kg, v = ' + p.speed + ' m/s, h = ' + p.height +
               ' m gives KE = <b>' + fmt(d.ke) + ' J</b> and GPE = <b>' + fmt(d.gpe) + ' J</b>. ';
    if (p.speed === 0 && p.height === 0) {
      return head + 'The ball is at rest on the ground, so both stores are empty \u2014 there is no energy to transfer.';
    }
    if (p.speed === 0) {
      return head + 'At rest all the energy sits in the gravitational potential store; doubling the height to ' +
             (p.height * 2) + ' m would only double it to ' + fmt(d.gpeDoubledHeight) + ' J.';
    }
    return head + 'Doubling the speed to ' + (p.speed * 2) + ' m/s would take KE to <b>' +
           fmt(d.keDoubledSpeed) + ' J</b> \u2014 four times bigger, because v is squared \u2014 while doubling the height only doubles GPE to ' +
           fmt(d.gpeDoubledHeight) + ' J.';
  }
};

if (typeof module !== 'undefined') module.exports = W;