var W = {
  meta: {
    id: 'insulate-to-target',
    title: 'Insulate the House to Hit 85% Efficiency',
    teaches: 'Increasing insulation thickness and choosing better materials reduces wasted thermal energy, raising efficiency toward (but never above) 100%, at a cost trade-off.'
  },

  initialState: function () {
    return {
      loftThickness: 100,
      wallChoice: 0,
      glazingChoice: 0
    };
  },

  apply: function (state, action) {
    var s = {
      loftThickness: state.loftThickness,
      wallChoice: state.wallChoice,
      glazingChoice: state.glazingChoice
    };
    if (action.t === 'set') {
      if (action.key === 'loftThickness') {
        var t = action.v;
        if (t < 0) t = 0;
        if (t > 300) t = 300;
        s.loftThickness = t;
      } else if (action.key === 'wallChoice') {
        var wc = Math.round(action.v);
        if (wc < 0) wc = 0;
        if (wc > 2) wc = 2;
        s.wallChoice = wc;
      } else if (action.key === 'glazingChoice') {
        var gc = Math.round(action.v);
        if (gc < 0) gc = 0;
        if (gc > 1) gc = 1;
        s.glazingChoice = gc;
      }
      return s;
    }
    if (action.t === 'reset') {
      return { loftThickness: 100, wallChoice: 0, glazingChoice: 0 };
    }
    return s;
  },

  derive: function (state) {
    var t = state.loftThickness;
    var wallLossArr = [350, 150, 75];
    var windowLossArr = [200, 75];
    var wallCostArr = [0, 250, 900];
    var glazingCostArr = [0, 350];

    var loftLoss = 200 - 0.5 * t;
    if (loftLoss < 0) loftLoss = 0;

    var wallLoss = wallLossArr[state.wallChoice];
    var windowLoss = windowLossArr[state.glazingChoice];

    var heatLossRate = loftLoss + wallLoss + windowLoss;
    var inputPower = 2000;
    var efficiency = 1 - heatLossRate / inputPower;
    if (efficiency < 0) efficiency = 0;
    if (efficiency > 1) efficiency = 1;

    var loftCost = t * 1.5;
    var wallCost = wallCostArr[state.wallChoice];
    var glazingCost = glazingCostArr[state.glazingChoice];
    var cost = loftCost + wallCost + glazingCost;

    var target = 0.85;
    var hitTarget = efficiency >= target;

    return {
      heatLossRate: heatLossRate,
      efficiency: efficiency,
      cost: cost,
      hitTarget: hitTarget,
      loftLoss: loftLoss,
      wallLoss: wallLoss,
      windowLoss: windowLoss,
      target: target
    };
  },

  regions: function (state, w, h) {
    // A small reset button top-right
    return [
      { x: w - 90, y: 10, w: 80, h: 26, action: { t: 'reset' } }
    ];
  },

  controls: [
    { key: 'loftThickness', label: 'Loft insulation thickness', min: 0, max: 300, step: 50, value: 100, unit: 'mm' },
    { key: 'wallChoice', label: 'Wall type (0=none,1=cavity,2=solid+insulated)', min: 0, max: 2, step: 1, value: 0, unit: '' },
    { key: 'glazingChoice', label: 'Glazing (0=single,1=double)', min: 0, max: 1, step: 1, value: 0, unit: '' }
  ],

  render: function (ctx, state, derived, w, h, acc) {
    var ink = '#2d2a26';
    var muted = '#8d8880';
    var grid = '#e8e2d9';

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#faf7f2';
    ctx.fillRect(0, 0, w, h);

    // Layout
    var houseX = 40, houseY = 60, houseW = w * 0.5, houseH = h * 0.55;
    var loftH = 30;

    // --- Reset button ---
    ctx.fillStyle = grid;
    ctx.fillRect(w - 90, 10, 80, 26);
    ctx.strokeStyle = muted;
    ctx.strokeRect(w - 90, 10, 80, 26);
    ctx.fillStyle = ink;
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Reset', w - 50, 27);

    // --- House outline ---
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2;
    ctx.strokeRect(houseX, houseY + loftH, houseW, houseH - loftH);

    // Roof (triangle) representing loft
    ctx.beginPath();
    ctx.moveTo(houseX - 10, houseY + loftH);
    ctx.lineTo(houseX + houseW / 2, houseY - 20);
    ctx.lineTo(houseX + houseW + 10, houseY + loftH);
    ctx.closePath();
    ctx.fillStyle = '#d8cbb3';
    ctx.fill();
    ctx.stroke();

    // Loft insulation thickness shading (yellow band under roof)
    var loftFrac = state.loftThickness / 300;
    var insulH = 6 + loftFrac * 22;
    ctx.fillStyle = '#e8d27a';
    ctx.fillRect(houseX + 4, houseY + loftH - insulH, houseW - 8, insulH);
    ctx.strokeStyle = muted;
    ctx.strokeRect(houseX + 4, houseY + loftH - insulH, houseW - 8, insulH);

    // Wall shading based on wallChoice
    var wallColors = ['#efe7db', '#d8d0c0', '#b9ac93'];
    ctx.fillStyle = wallColors[state.wallChoice];
    ctx.fillRect(houseX, houseY + loftH, 14, houseH - loftH);
    ctx.fillRect(houseX + houseW - 14, houseY + loftH, 14, houseH - loftH);
    ctx.strokeStyle = muted;
    ctx.strokeRect(houseX, houseY + loftH, 14, houseH - loftH);
    ctx.strokeRect(houseX + houseW - 14, houseY + loftH, 14, houseH - loftH);

    // Window
    var winX = houseX + houseW / 2 - 30, winY = houseY + loftH + 30, winW = 60, winH = 50;
    ctx.fillStyle = '#cfe6ec';
    ctx.fillRect(winX, winY, winW, winH);
    ctx.strokeStyle = ink;
    ctx.strokeRect(winX, winY, winW, winH);
    if (state.glazingChoice === 1) {
      // double glazing - draw a second inner pane line
      ctx.strokeStyle = muted;
      ctx.strokeRect(winX + 6, winY + 6, winW - 12, winH - 12);
    }

    // Heater inside, label input power
    ctx.fillStyle = acc;
    ctx.fillRect(houseX + houseW / 2 - 18, houseY + houseH - 40, 36, 24);
    ctx.fillStyle = '#fff';
    ctx.font = '10px sans-serif';
    ctx.fillText('2000W', houseX + houseW / 2, houseY + houseH - 24);

    // --- Heat loss arrows ---
    function drawArrow(x1, y1, x2, y2, len) {
      // wavy red line with arrowhead, length scaled by len (px)
      var dx = x2 - x1, dy = y2 - y1;
      var mag = Math.sqrt(dx * dx + dy * dy) || 1;
      var ux = dx / mag, uy = dy / mag;
      var segs = 4;
      ctx.strokeStyle = '#c0392b';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      for (var i = 1; i <= segs; i++) {
        var t = i / segs;
        var px = x1 + ux * len * t;
        var py = y1 + uy * len * t;
        var perpX = -uy, perpY = ux;
        var wob = (i % 2 === 0 ? 4 : -4);
        ctx.lineTo(px + perpX * wob, py + perpY * wob);
      }
      ctx.stroke();
      // arrowhead
      var tipX = x1 + ux * len, tipY = y1 + uy * len;
      ctx.beginPath();
      ctx.moveTo(tipX, tipY);
      ctx.lineTo(tipX - ux * 8 + perpArrow(ux, uy, 1), tipY - uy * 8);
      ctx.stroke();
      function perpArrow() { return 0; }
    }

    // scale losses to px length
    var loftArrowLen = 10 + (derived.loftLoss / 200) * 40;
    var wallArrowLen = 10 + (derived.wallLoss / 350) * 40;
    var winArrowLen = 10 + (derived.windowLoss / 200) * 40;

    // loft arrow (upward from roof)
    drawArrow(houseX + houseW / 2, houseY - 10, houseX + houseW / 2, houseY - 10 - loftArrowLen, loftArrowLen);
    // left wall arrow
    drawArrow(houseX, houseY + loftH + 40, houseX - wallArrowLen, houseY + loftH + 40, wallArrowLen);
    // right wall arrow
    drawArrow(houseX + houseW, houseY + loftH + 40, houseX + houseW + wallArrowLen, houseY + loftH + 40, wallArrowLen);
    // window arrow
    drawArrow(winX + winW / 2, winY + winH + 5, winX + winW / 2, winY + winH + 5 + winArrowLen, winArrowLen);

    // labels for losses
    ctx.fillStyle = ink;
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Loft loss: ' + derived.loftLoss.toFixed(0) + ' W', houseX, houseY - 26);
    ctx.fillText('Wall loss: ' + derived.wallLoss.toFixed(0) + ' W', houseX + houseW + wallArrowLen + 8, houseY + loftH + 44);
    ctx.fillText('Window loss: ' + derived.windowLoss.toFixed(0) + ' W', winX - 10, winY + winH + winArrowLen + 20);

    // --- Efficiency bar ---
    var barX = w - 70, barY = 60, barW = 26, barH = h * 0.55;
    ctx.strokeStyle = ink;
    ctx.strokeRect(barX, barY, barW, barH);
    var fillH = derived.efficiency * barH;
    ctx.fillStyle = derived.hitTarget ? acc : '#c0392b';
    ctx.fillRect(barX, barY + barH - fillH, barW, fillH);

    // target line at 85%
    var targetY = barY + barH - (derived.target * barH);
    ctx.strokeStyle = ink;
    ctx.setLineDash([4, 3]);
    ctx.beginPath();
    ctx.moveTo(barX - 6, targetY);
    ctx.lineTo(barX + barW + 6, targetY);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('85% target', barX + barW + 8, targetY + 3);

    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = ink;
    ctx.fillText((derived.efficiency * 100).toFixed(0) + '%', barX + barW / 2, barY - 8);
    ctx.font = '11px sans-serif';
    ctx.fillText('Efficiency', barX + barW / 2, barY + barH + 16);

    // --- Cost coin stack ---
    var coinX = w - 160, coinY = h - 40;
    var numCoins = Math.round(derived.cost / 150);
    if (numCoins > 12) numCoins = 12;
    ctx.textAlign = 'left';
    ctx.font = '11px sans-serif';
    ctx.fillStyle = ink;
    ctx.fillText('Cost: £' + derived.cost.toFixed(0), coinX - 4, coinY + 20);
    for (var c = 0; c < numCoins; c++) {
      ctx.beginPath();
      ctx.arc(coinX + 10, coinY - c * 8, 9, 0, Math.PI * 2);
      ctx.fillStyle = '#d8b23a';
      ctx.fill();
      ctx.strokeStyle = '#8d6d1f';
      ctx.stroke();
    }

    // --- Status message ---
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = derived.hitTarget ? acc : '#c0392b';
    ctx.fillText(
      derived.hitTarget ? 'Target reached!' : 'Below target',
      20, h - 12
    );
  },

  caption: function (state, derived) {
    if (derived.hitTarget) {
      return 'Efficiency ' + (derived.efficiency * 100).toFixed(0) +
        '% meets the 85% target — total cost £' + derived.cost.toFixed(0) +
        '. Can you reach it more cheaply?';
    }
    return 'Efficiency is only ' + (derived.efficiency * 100).toFixed(0) +
      '% — heat is still escaping at ' + derived.heatLossRate.toFixed(0) +
      ' W. Improve insulation to cut losses and reach 85%.';
  }
};

if (typeof module !== 'undefined') module.exports = W;