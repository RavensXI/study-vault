window.SVWidget = {
  meta: {
    id: 'essex-patronage-cascade',
    title: 'Cut the Wine Money, Watch Essex Fall',
    teaches: 'Withdrawing Essex\u2019s sweet wines monopoly cut his income, drove up his debt and drained his followers, leaving rebellion as the only option left \u2014 and one doomed to fail, because patronage, not force, held followers loyal.'
  },

  mount: function (root, ctx) {
    'use strict';

    var acc = (ctx && ctx.accent) || '#9a6a3a';
    var reduced = !!(ctx && ctx.reducedMotion);

    var INK = '#2d2a26', MUT = '#8d8880', GRID = '#e8e2d9', PAPER = '#faf8f5';
    var RED = '#a8433a', RED_DK = '#7d2f28';
    var uid = 'ex' + Math.floor(Math.random() * 100000);

    /* ---------- tiny helpers ---------- */
    function mk(tag, styles, text) {
      var e = document.createElement(tag);
      if (styles) { for (var k in styles) { e.style[k] = styles[k]; } }
      if (text != null) { e.textContent = text; }
      return e;
    }
    function hexToRgba(h, a) {
      var m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(h);
      if (!m) { return h; }
      return 'rgba(' + parseInt(m[1], 16) + ',' + parseInt(m[2], 16) + ',' + parseInt(m[3], 16) + ',' + a + ')';
    }
    function shade(h, amt) {
      var m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(h);
      if (!m) { return h; }
      var out = '#';
      for (var i = 1; i <= 3; i++) {
        var v = parseInt(m[i], 16) + Math.round(255 * amt);
        v = Math.max(0, Math.min(255, v));
        out += ('0' + v.toString(16)).slice(-2);
      }
      return out;
    }
    function money(n) { return '\u00a3' + n.toLocaleString('en-GB'); }

    /* ---------- model ---------- */
    var p = { monopolyRenewed: 0, monthsSinceLapse: 4, essexChoice: 1 };

    function compute(par) {
      var income = par.monopolyRenewed === 1 ? 4000 : 0;
      var debt = par.monopolyRenewed === 1 ? 3000 : 3000 + 500 * par.monthsSinceLapse;
      var followers = par.monopolyRenewed === 1
        ? 300
        : Math.max(0, Math.min(300, 300 - 25 * par.monthsSinceLapse));
      var financiallyRuined = debt > income;
      var rebellionAttempted = par.essexChoice === 1;
      var rebellionSucceeds = rebellionAttempted && followers >= 250;

      var seal, dest, colour, outcomeLabel, why;

      if (par.monopolyRenewed === 1 && !rebellionAttempted) {
        seal = 'FAVOUR'; dest = 0; colour = acc;
        outcomeLabel = 'Favour restored \u2014 Essex keeps his household, his followers and his place at court.';
        why = 'The wine money still pays his agents, soldiers and dependents, so the men who rely on him stay. Patronage flowing from the Crown, through Essex, to his followers is what holds them there.';
      } else if (par.monopolyRenewed === 1 && rebellionAttempted) {
        seal = 'SEIZED'; dest = 0.5; colour = acc;
        outcomeLabel = 'Counterfactual \u2014 with the wine money still flowing, 300 men march with him and the rising holds together. This is not what happened.';
        why = 'A well-funded magnate can still buy men. That is exactly why Elizabeth did not renew the licence: cutting the income was cheaper and safer than fighting the following it paid for.';
      } else if (!rebellionAttempted) {
        seal = 'RUIN'; dest = 0; colour = MUT;
        outcomeLabel = 'Ruin without rebellion \u2014 Essex submits and keeps his head, but after ' + par.monthsSinceLapse + ' month' + (par.monthsSinceLapse === 1 ? '' : 's') + ' his debts stand at ' + money(debt) + ' and only ' + followers + ' followers remain.';
        why = 'Submission was survivable. Contemporaries thought Essex rebelled because he believed ruin was already certain \u2014 his creditors were closing in and there was nothing left to promise his men.';
      } else if (rebellionSucceeds) {
        seal = 'SEIZED'; dest = 0.5; colour = acc;
        outcomeLabel = 'Counterfactual \u2014 rising this soon after the lapse, Essex still musters ' + followers + ' men and the march holds together. This is not what happened.';
        why = 'Strike before the following melts away and numbers are on his side. But every month without the monopoly takes men off his list, so delay decides the outcome.';
      } else {
        seal = 'TREASON'; dest = 1; colour = RED;
        if (par.monthsSinceLapse === 4) {
          outcomeLabel = 'Rebellion and execution \u2014 about 200 followers march out of Essex House on 8 February 1601, melt away within hours, and Essex is beheaded at the Tower on 25 February 1601.';
        } else {
          outcomeLabel = 'Rebellion and execution \u2014 only ' + followers + ' men march, Londoners stay indoors, and Essex is condemned as a traitor.';
        }
        why = 'Cecil had been warned, had Essex proclaimed a traitor and got royal heralds onto the streets first. Force could not replace patronage overnight: men who were not being paid or promised anything simply went home.';
      }

      return {
        income: income, debt: debt, followers: followers,
        financiallyRuined: financiallyRuined,
        rebellionAttempted: rebellionAttempted,
        rebellionSucceeds: rebellionSucceeds,
        outcomeLabel: outcomeLabel,
        seal: seal, dest: dest, colour: colour, why: why
      };
    }

    /* ---------- shell ---------- */
    root.style.fontFamily = 'Inter, system-ui, -apple-system, "Segoe UI", Arial, sans-serif';
    root.style.color = INK;
    root.style.lineHeight = '1.45';
    root.style.fontSize = '15px';
    root.style.maxWidth = '900px';
    root.style.boxSizing = 'border-box';

    var card = function () {
      return mk('div', {
        background: '#ffffff', border: '1px solid ' + GRID, borderRadius: '14px',
        padding: '14px', boxSizing: 'border-box', marginBottom: '12px'
      });
    };

    var head = mk('div', { marginBottom: '10px' });
    var h = mk('h2', {
      font: '600 20px/1.25 "Source Serif 4", Georgia, serif', margin: '0 0 6px 0', color: INK
    }, 'Cut the wine money, watch Essex fall');
    var intro = mk('p', { margin: '0', color: MUT, fontSize: '14px' },
      'October 1600. You sit with Elizabeth\u2019s Privy Council. Decide whether the sweet wines monopoly is renewed, how long the licence stays lapsed, and how the Earl of Essex responds.');
    head.appendChild(h); head.appendChild(intro);
    root.appendChild(head);

    /* ---------- controls ---------- */
    var cCard = card();
    var cGrid = mk('div', {
      display: 'grid', gap: '14px',
      gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))'
    });
    cCard.appendChild(cGrid);

    function labelFor(txt) {
      return mk('div', { font: '600 12px/1.3 Inter, sans-serif', color: INK, marginBottom: '7px' }, txt);
    }

    function segmented(key, opts, onSel) {
      var wrapS = mk('div', { display: 'flex', gap: '6px', flexWrap: 'wrap' });
      var items = [];
      opts.forEach(function (o) {
        var lab = mk('label', {
          flex: '1 1 96px', textAlign: 'center', padding: '9px 8px',
          border: '1px solid ' + GRID, borderRadius: '10px', cursor: 'pointer',
          fontSize: '13px', background: '#fff', color: MUT, position: 'relative',
          boxSizing: 'border-box'
        });
        var inp = document.createElement('input');
        inp.type = 'radio';
        inp.name = key + '-' + uid;
        inp.value = String(o.v);
        inp.setAttribute('data-key', key);
        inp.style.position = 'absolute';
        inp.style.opacity = '0';
        inp.style.width = '1px';
        inp.style.height = '1px';
        inp.style.margin = '0';
        var sp = mk('span', null, o.txt);
        lab.appendChild(inp); lab.appendChild(sp);
        inp.addEventListener('change', function () { if (inp.checked) { onSel(o.v); } });
        inp.addEventListener('focus', function () { lab.style.outline = '2px solid ' + acc; lab.style.outlineOffset = '2px'; });
        inp.addEventListener('blur', function () { lab.style.outline = 'none'; });
        items.push({ inp: inp, lab: lab, v: o.v });
        wrapS.appendChild(lab);
      });
      return {
        node: wrapS,
        set: function (v) {
          items.forEach(function (b) {
            var on = (b.v === v);
            b.inp.checked = on;
            b.lab.style.background = on ? acc : '#fff';
            b.lab.style.color = on ? '#fff' : MUT;
            b.lab.style.borderColor = on ? acc : GRID;
            b.lab.style.fontWeight = on ? '600' : '500';
          });
        }
      };
    }

    /* control 1 */
    var b1 = mk('div');
    b1.appendChild(labelFor('Elizabeth renews the sweet wines monopoly?'));
    var seg1 = segmented('monopolyRenewed',
      [{ v: 0, txt: 'No \u2014 let it lapse' }, { v: 1, txt: 'Yes \u2014 renew' }],
      function (v) { p.monopolyRenewed = v; render(); });
    b1.appendChild(seg1.node);
    cGrid.appendChild(b1);

    /* control 2 */
    var b2 = mk('div');
    b2.appendChild(labelFor('Months since the licence lapsed'));
    var slider = document.createElement('input');
    slider.type = 'range'; slider.min = '0'; slider.max = '12'; slider.step = '1';
    slider.value = '4';
    slider.setAttribute('data-key', 'monthsSinceLapse');
    slider.setAttribute('aria-label', 'Months since the licence lapsed');
    slider.style.width = '100%';
    slider.style.accentColor = acc;
    slider.style.margin = '4px 0 0 0';
    function onMonths() { p.monthsSinceLapse = parseInt(slider.value, 10) || 0; render(); }
    slider.addEventListener('input', onMonths);
    slider.addEventListener('change', onMonths);
    b2.appendChild(slider);
    var monthRead = mk('div', { font: '500 12px Inter, sans-serif', color: MUT, marginTop: '4px' }, '');
    b2.appendChild(monthRead);
    cGrid.appendChild(b2);

    /* control 3 */
    var b3 = mk('div');
    b3.appendChild(labelFor('Essex\u2019s response'));
    var seg3 = segmented('essexChoice',
      [{ v: 0, txt: 'Submit quietly' }, { v: 1, txt: 'March out in revolt' }],
      function (v) { p.essexChoice = v; render(); });
    b3.appendChild(seg3.node);
    cGrid.appendChild(b3);

    var histRow = mk('div', { marginTop: '12px', display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' });
    var histBtn = mk('button', {
      font: '600 12px Inter, sans-serif', color: INK, background: PAPER,
      border: '1px solid ' + GRID, borderRadius: '999px', padding: '7px 13px', cursor: 'pointer'
    }, 'Set to 8 February 1601');
    histBtn.type = 'button';
    histBtn.addEventListener('click', function () {
      p.monopolyRenewed = 0; p.monthsSinceLapse = 4; p.essexChoice = 1; render();
    });
    histBtn.addEventListener('focus', function () { histBtn.style.outline = '2px solid ' + acc; histBtn.style.outlineOffset = '2px'; });
    histBtn.addEventListener('blur', function () { histBtn.style.outline = 'none'; });
    var histFlag = mk('span', { font: '600 12px Inter, sans-serif', color: acc }, '');
    histRow.appendChild(histBtn); histRow.appendChild(histFlag);
    cCard.appendChild(histRow);
    root.appendChild(cCard);

    /* ---------- stat strip ---------- */
    var sCard = card();
    var sGrid = mk('div', {
      display: 'grid', gap: '10px',
      gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))'
    });
    function statBox(name) {
      var box = mk('div', {
        background: PAPER, border: '1px solid ' + GRID, borderRadius: '10px', padding: '9px 10px'
      });
      var l = mk('div', { font: '600 10px Inter, sans-serif', color: MUT, letterSpacing: '.06em' }, name.toUpperCase());
      var v = mk('div', { font: '600 19px "Source Serif 4", Georgia, serif', color: INK, marginTop: '2px' }, '\u2014');
      box.appendChild(l); box.appendChild(v);
      sGrid.appendChild(box);
      return v;
    }
    var vIncome = statBox('Income');
    var vDebt = statBox('Debt');
    var vFollowers = statBox('Followers');
    var vRuin = statBox('Finances');
    sCard.appendChild(sGrid);
    root.appendChild(sCard);

    /* ---------- canvas ---------- */
    var vCard = card();
    var cv = document.createElement('canvas');
    cv.style.display = 'block';
    cv.style.width = '100%';
    cv.setAttribute('role', 'img');
    vCard.appendChild(cv);
    root.appendChild(vCard);
    var c2d = cv.getContext('2d');

    /* ---------- outcome ---------- */
    var oCard = card();
    oCard.style.borderLeft = '3px solid ' + acc;
    var oTop = mk('div', { display: 'flex', gap: '10px', alignItems: 'baseline', flexWrap: 'wrap' });
    var oChip = mk('span', {
      font: '700 11px Inter, sans-serif', letterSpacing: '.08em', color: '#fff',
      background: acc, borderRadius: '999px', padding: '4px 11px'
    }, 'RUIN');
    var oTitle = mk('span', { font: '600 13px Inter, sans-serif', color: MUT }, 'Outcome');
    oTop.appendChild(oChip); oTop.appendChild(oTitle);
    var oText = mk('p', { margin: '9px 0 0 0', font: '400 15px/1.5 Inter, sans-serif', color: INK }, '');
    oText.setAttribute('aria-live', 'polite');
    var oWhy = mk('p', { margin: '8px 0 0 0', font: '400 13.5px/1.5 Inter, sans-serif', color: MUT }, '');
    oCard.appendChild(oTop); oCard.appendChild(oText); oCard.appendChild(oWhy);
    root.appendChild(oCard);

    /* ---------- drawing ---------- */
    function roundRect(c, x, y, w, hh, r) {
      c.beginPath();
      c.moveTo(x + r, y);
      c.arcTo(x + w, y, x + w, y + hh, r);
      c.arcTo(x + w, y + hh, x, y + hh, r);
      c.arcTo(x, y + hh, x, y, r);
      c.arcTo(x, y, x + w, y, r);
      c.closePath();
    }
    function fitText(c, txt, maxW, maxPx) {
      var size = maxPx;
      c.font = '700 ' + size + 'px Inter, sans-serif';
      while (c.measureText(txt).width > maxW && size > 6) {
        size -= 0.5;
        c.font = '700 ' + size + 'px Inter, sans-serif';
      }
    }

    var tokenPos = 1, targetPos = 1, raf = null;

    function draw(d) {
      var cssW = Math.max(280, Math.round(vCard.clientWidth - 28));
      var gTop = 4, gH = 190, sH = 152;
      var H = gTop + gH + 10 + sH;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.round(cssW * dpr);
      cv.height = Math.round(H * dpr);
      cv.style.height = H + 'px';
      c2d.setTransform(dpr, 0, 0, dpr, 0, 0);
      c2d.clearRect(0, 0, cssW, H);
      c2d.textBaseline = 'alphabetic';

      var pad = 6, gap = 6;
      var colW = (cssW - pad * 2 - gap * 2) / 3;
      var gy0 = gTop + 60, gy1 = gTop + gH - 20;

      /* panels */
      var i, px;
      for (i = 0; i < 3; i++) {
        px = pad + i * (colW + gap);
        c2d.fillStyle = '#fff';
        c2d.strokeStyle = GRID;
        c2d.lineWidth = 1;
        roundRect(c2d, px + 0.5, gTop + 0.5, colW - 1, gH - 1, 10);
        c2d.fill(); c2d.stroke();
      }

      function panelText(px2, title, value, sub, valCol) {
        c2d.textAlign = 'left';
        c2d.font = '700 9px Inter, sans-serif';
        c2d.fillStyle = MUT;
        c2d.fillText(title, px2 + 9, gTop + 16);
        c2d.font = '600 17px "Source Serif 4", Georgia, serif';
        c2d.fillStyle = valCol || INK;
        c2d.fillText(value, px2 + 9, gTop + 37);
        c2d.font = '400 8.5px Inter, sans-serif';
        c2d.fillStyle = MUT;
        c2d.fillText(sub, px2 + 9, gTop + 50);
      }

      /* 1. income coins */
      px = pad;
      panelText(px, 'INCOME', money(d.income), 'sweet wines, per year', d.income ? INK : MUT);
      var coinW = Math.min(colW - 30, 44);
      var cx = px + colW / 2;
      for (i = 0; i < 8; i++) {
        var cyC = gy1 - i * 8;
        c2d.beginPath();
        c2d.ellipse(cx, cyC, coinW / 2, 4.4, 0, 0, Math.PI * 2);
        if (d.income > 0) {
          c2d.fillStyle = acc; c2d.fill();
          c2d.strokeStyle = shade(acc, -0.18); c2d.lineWidth = 1; c2d.stroke();
        } else {
          c2d.strokeStyle = GRID; c2d.lineWidth = 1; c2d.stroke();
        }
      }
      c2d.textAlign = 'center';
      c2d.font = '400 8px Inter, sans-serif';
      c2d.fillStyle = MUT;
      c2d.fillText(d.income > 0 ? 'each coin \u00a3500' : 'licence lapsed', cx, gTop + gH - 7);

      /* 2. debt tower */
      px = pad + colW + gap;
      panelText(px, 'DEBT', money(d.debt), 'owed to creditors', d.financiallyRuined ? RED_DK : INK);
      cx = px + colW / 2;
      var brickW = Math.min(colW - 30, 46);
      var bricks = Math.round(d.debt / 750);
      for (i = 0; i < bricks; i++) {
        var by = gy1 - i * 9 - 7;
        c2d.fillStyle = RED;
        c2d.fillRect(cx - brickW / 2, by, brickW, 7);
        c2d.strokeStyle = RED_DK; c2d.lineWidth = 1;
        c2d.strokeRect(cx - brickW / 2 + 0.5, by + 0.5, brickW - 1, 6);
      }
      var iy = gy1 - (d.income / 750) * 9;
      c2d.save();
      c2d.setLineDash([3, 3]);
      c2d.strokeStyle = d.income > 0 ? shade(acc, -0.1) : MUT;
      c2d.lineWidth = 1;
      c2d.beginPath();
      c2d.moveTo(px + 7, iy); c2d.lineTo(px + colW - 7, iy);
      c2d.stroke();
      c2d.restore();
      c2d.textAlign = 'right';
      c2d.font = '600 8px Inter, sans-serif';
      c2d.fillStyle = d.income > 0 ? shade(acc, -0.1) : MUT;
      c2d.fillText('income line', px + colW - 8, iy - 3);
      c2d.textAlign = 'center';
      c2d.font = '400 8px Inter, sans-serif';
      c2d.fillStyle = d.financiallyRuined ? RED_DK : MUT;
      c2d.fillText(d.financiallyRuined ? 'debt above income' : 'debt below income', cx, gTop + gH - 7);

      /* 3. followers */
      px = pad + 2 * (colW + gap);
      panelText(px, 'FOLLOWERS', String(d.followers), 'men still looking to him', INK);
      var present = Math.round(d.followers / 25);
      var cellW = (colW - 18) / 4;
      for (i = 0; i < 12; i++) {
        var col = i % 4, rw = Math.floor(i / 4);
        var fx = px + 9 + cellW * (col + 0.5);
        var fy = gy0 + 6 + rw * 32;
        var on = i < present;
        c2d.beginPath();
        c2d.arc(fx, fy, 3.1, 0, Math.PI * 2);
        c2d.beginPath();
        c2d.moveTo(fx - 6, fy + 17);
        c2d.lineTo(fx - 3.6, fy + 5);
        c2d.lineTo(fx + 3.6, fy + 5);
        c2d.lineTo(fx + 6, fy + 17);
        c2d.closePath();
        if (on) { c2d.fillStyle = acc; c2d.fill(); }
        else { c2d.strokeStyle = GRID; c2d.lineWidth = 1; c2d.stroke(); }
        c2d.beginPath();
        c2d.arc(fx, fy, 3.1, 0, Math.PI * 2);
        if (on) { c2d.fillStyle = shade(acc, -0.12); c2d.fill(); }
        else { c2d.strokeStyle = GRID; c2d.stroke(); }
      }
      c2d.textAlign = 'center';
      c2d.font = '400 8px Inter, sans-serif';
      c2d.fillStyle = MUT;
      c2d.fillText('1 figure = 25 men', px + colW / 2, gTop + gH - 7);

      /* ---- scene ---- */
      var sTop = gTop + gH + 10;
      var ground = sTop + sH - 26;

      c2d.strokeStyle = GRID; c2d.lineWidth = 1;
      c2d.beginPath(); c2d.moveTo(pad, ground + 0.5); c2d.lineTo(cssW - pad, ground + 0.5); c2d.stroke();

      var bW = Math.min(78, cssW * 0.22);
      var houseCx = pad + 8 + bW / 2;
      var towerCx = cssW - pad - 8 - bW / 2;

      /* dotted road */
      c2d.save();
      c2d.setLineDash([2, 5]);
      c2d.strokeStyle = GRID;
      c2d.beginPath(); c2d.moveTo(houseCx, ground - 2); c2d.lineTo(towerCx, ground - 2); c2d.stroke();
      c2d.restore();

      var hiHouse = (d.dest === 0), hiTower = (d.dest === 1);

      /* Essex House */
      (function () {
        var w = bW * 0.78, hh = 34;
        var x = houseCx - w / 2, y = ground - hh;
        c2d.fillStyle = hiHouse ? hexToRgba(d.colour, 0.12) : '#fff';
        c2d.strokeStyle = hiHouse ? d.colour : INK;
        c2d.lineWidth = hiHouse ? 1.6 : 1.1;
        c2d.fillRect(x, y, w, hh); c2d.strokeRect(x + 0.5, y + 0.5, w - 1, hh - 1);
        c2d.beginPath();
        c2d.moveTo(x - 3, y); c2d.lineTo(houseCx, y - 15); c2d.lineTo(x + w + 3, y);
        c2d.closePath(); c2d.fill(); c2d.stroke();
        c2d.fillStyle = hiHouse ? d.colour : MUT;
        c2d.fillRect(houseCx - 4, ground - 12, 8, 12);
        c2d.fillStyle = GRID;
        c2d.fillRect(x + 5, y + 7, 8, 8);
        c2d.fillRect(x + w - 13, y + 7, 8, 8);
        c2d.strokeStyle = MUT; c2d.lineWidth = 1;
        c2d.strokeRect(x + 5.5, y + 7.5, 7, 7);
        c2d.strokeRect(x + w - 12.5, y + 7.5, 7, 7);
      })();

      /* The Tower */
      (function () {
        var w = bW * 0.8, hh = 40;
        var x = towerCx - w / 2, y = ground - hh;
        c2d.fillStyle = hiTower ? hexToRgba(RED, 0.10) : '#fff';
        c2d.strokeStyle = hiTower ? RED_DK : INK;
        c2d.lineWidth = hiTower ? 1.6 : 1.1;
        c2d.fillRect(x, y, w, hh); c2d.strokeRect(x + 0.5, y + 0.5, w - 1, hh - 1);
        var t = 0;
        for (t = 0; t < 4; t++) {
          var nx = x + 2 + t * (w - 6) / 3.6;
          c2d.fillRect(nx, y - 5, (w - 6) / 7.2, 5);
          c2d.strokeRect(nx + 0.5, y - 4.5, (w - 6) / 7.2 - 1, 4);
        }
        var tw = 7;
        [x - tw + 1, x + w - 1].forEach(function (tx) {
          c2d.fillRect(tx, y - 8, tw, hh + 8);
          c2d.strokeRect(tx + 0.5, y - 7.5, tw - 1, hh + 7);
          c2d.beginPath();
          c2d.moveTo(tx - 1, y - 8); c2d.lineTo(tx + tw / 2, y - 15); c2d.lineTo(tx + tw + 1, y - 8);
          c2d.closePath(); c2d.fill(); c2d.stroke();
        });
        c2d.fillStyle = hiTower ? RED_DK : MUT;
        c2d.fillRect(towerCx - 4, ground - 11, 8, 11);
      })();

      c2d.textAlign = 'center';
      c2d.font = '600 9px Inter, sans-serif';
      c2d.fillStyle = hiHouse ? d.colour : MUT;
      c2d.fillText('Essex House', houseCx, ground + 14);
      c2d.fillStyle = hiTower ? RED_DK : MUT;
      c2d.fillText('The Tower', towerCx, ground + 14);
      c2d.font = '400 8px Inter, sans-serif';
      c2d.fillStyle = MUT;
      c2d.fillText('the Str