/* SV Widget */
var DEF = [3, 4, 0, 5, 1, 2];

function svReadAssign(p) {
  var a = [], i, v, src = null;
  if (p && p.assignment && typeof p.assignment.length === 'number') src = p.assignment;
  for (i = 0; i < 6; i++) {
    v = src ? src[i] : (p ? p['assignment_' + i] : undefined);
    v = Math.round(Number(v));
    if (!isFinite(v)) v = DEF[i];
    if (v < 0) v = 0;
    if (v > 5) v = 5;
    a.push(v);
  }
  return a;
}

function svWrap(ctx, text, maxW) {
  var words = String(text).split(' '), lines = [], cur = '', i, t;
  for (i = 0; i < words.length; i++) {
    t = cur ? cur + ' ' + words[i] : words[i];
    if (cur && ctx.measureText(t).width > maxW) { lines.push(cur); cur = words[i]; }
    else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

function svCard(ctx, x, y, cw, ch, r) {
  if (r > ch / 2) r = ch / 2;
  if (r > cw / 2) r = cw / 2;
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + cw - r, y);
  ctx.quadraticCurveTo(x + cw, y, x + cw, y + r);
  ctx.lineTo(x + cw, y + ch - r);
  ctx.quadraticCurveTo(x + cw, y + ch, x + cw - r, y + ch);
  ctx.lineTo(x + r, y + ch);
  ctx.quadraticCurveTo(x, y + ch, x, y + ch - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

var W = {
  meta: {
    id: 'match-the-minister',
    title: 'Match the Minister to Their Mark',
    teaches: 'Cecil, Walsingham, Robert Cecil and the Privy Council each had a distinct, indispensable role — and Mary, Queen of Scots is not Mary I.',
    kind: 'explore'
  },

  NAMES: [
    'William Cecil (Lord Burghley)',
    'Sir Francis Walsingham',
    'Robert Cecil',
    'The Privy Council',
    'Mary, Queen of Scots',
    'Mary I'
  ],

  FACTS: [
    'Principal Secretary 1558–1572, then Lord Treasurer to 1598. John Guy called him \u2018the indispensable man\u2019.',
    'Principal Secretary from 1573. Ran agents and codebreakers such as Thomas Phelippes; uncovered the Babington Plot, 1586.',
    'Burghley\u2019s son, the queen\u2019s \u2018little elf\u2019. Secured the peaceful succession of James VI/I in 1603.',
    'About 19\u201320 hand-picked men, meeting two or three times a week. It \u2018advised; the queen decided\u2019.',
    'Elizabeth\u2019s Catholic Stuart cousin. Executed at Fotheringhay Castle, February 1587.',
    '\u2018Bloody Mary\u2019, Elizabeth\u2019s half-sister, queen 1553\u20131558 \u2014 died before this depth study begins.'
  ],

  /* right-hand column is shuffled: visual slot q displays fact SHUFFLE[q] */
  SHUFFLE: [2, 5, 0, 4, 1, 3],

  controls: [
    { key: 'assignment_0', label: 'Fact matched to William Cecil', min: 0, max: 5, step: 1, value: 3, unit: '' },
    { key: 'assignment_1', label: 'Fact matched to Francis Walsingham', min: 0, max: 5, step: 1, value: 4, unit: '' },
    { key: 'assignment_2', label: 'Fact matched to Robert Cecil', min: 0, max: 5, step: 1, value: 0, unit: '' },
    { key: 'assignment_3', label: 'Fact matched to the Privy Council', min: 0, max: 5, step: 1, value: 5, unit: '' },
    { key: 'assignment_4', label: 'Fact matched to Mary, Queen of Scots', min: 0, max: 5, step: 1, value: 1, unit: '' },
    { key: 'assignment_5', label: 'Fact matched to Mary I', min: 0, max: 5, step: 1, value: 2, unit: '' }
  ],

  derive: function (p) {
    var a = svReadAssign(p), i, correct = 0, seen = [0, 0, 0, 0, 0, 0], valid = true;
    for (i = 0; i < 6; i++) {
      if (a[i] === i) correct++;
      seen[a[i]] = seen[a[i]] + 1;
    }
    for (i = 0; i < 6; i++) { if (seen[i] !== 1) valid = false; }
    return {
      assignment: a,
      correctCount: correct,
      allMatched: (correct === 6 && valid),
      maryConfused: (a[4] === 5 && a[5] === 4),
      cecilRobertConfused: (a[0] === 2 && a[2] === 0),
      isValidPermutation: valid
    };
  },

  render: function (ctx, p, d, w, h, acc) {
    var GREEN = '#3f7d4e', RED = '#a8443a', INK = '#2d2a26', MUTED = '#8d8880', GRID = '#e8e2d9';
    var a = d.assignment || svReadAssign(p);
    var i, q, f, x;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#f7f2ea';
    ctx.fillRect(0, 0, w, h);

    /* table planks */
    ctx.strokeStyle = GRID;
    ctx.lineWidth = 1;
    for (x = 48; x < w; x += 48) {
      ctx.beginPath(); ctx.moveTo(x + 0.5, 0); ctx.lineTo(x + 0.5, h); ctx.stroke();
    }

    /* ---- scoreboard ---- */
    var top = 34;
    ctx.textBaseline = 'middle';
    ctx.textAlign = 'left';
    ctx.font = 'bold 13px Georgia, serif';
    ctx.fillStyle = INK;
    ctx.fillText('Matched correctly: ' + d.correctCount + ' / 6', 10, 16);
    var pipX = w - 10 - 6 * 13;
    for (i = 0; i < 6; i++) {
      ctx.beginPath();
      ctx.arc(pipX + i * 13 + 5, 16, 4.5, 0, Math.PI * 2);
      ctx.fillStyle = (a[i] === i) ? GREEN : '#ffffff';
      ctx.fill();
      ctx.strokeStyle = (a[i] === i) ? GREEN : MUTED;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
    ctx.strokeStyle = GRID;
    ctx.beginPath(); ctx.moveTo(0, top - 6.5); ctx.lineTo(w, top - 6.5); ctx.stroke();

    /* ---- geometry ---- */
    var gap = 5;
    var rowH = (h - top - 6 - gap * 5) / 6;
    if (rowH < 16) rowH = 16;
    var nx = 10;
    var nw = Math.max(84, Math.min(158, w * 0.30));
    var colGap = Math.max(30, w * 0.09);
    var fx = nx + nw + colGap;
    var fw = w - 10 - fx;
    if (fw < 60) { fw = 60; }

    function rowY(k) { return top + k * (rowH + gap); }
    function rowMid(k) { return rowY(k) + rowH / 2; }

    var posOf = [0, 0, 0, 0, 0, 0];
    for (q = 0; q < 6; q++) posOf[this.SHUFFLE[q]] = q;

    /* ---- connecting lines ---- */
    for (i = 0; i < 6; i++) {
      f = a[i];
      q = posOf[f];
      var y1 = rowMid(i), y2 = rowMid(q);
      var ok = (f === i);
      ctx.strokeStyle = ok ? GREEN : RED;
      ctx.lineWidth = ok ? 2 : 1.4;
      ctx.beginPath();
      ctx.moveTo(nx + nw, y1);
      ctx.bezierCurveTo(nx + nw + colGap * 0.55, y1, fx - colGap * 0.55, y2, fx, y2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(fx, y2, 2.6, 0, Math.PI * 2);
      ctx.fillStyle = ok ? GREEN : RED;
      ctx.fill();
    }

    /* ---- name cards ---- */
    var nFont = rowH >= 40 ? 11 : 10;
    for (i = 0; i < 6; i++) {
      var ok2 = (a[i] === i);
      svCard(ctx, nx, rowY(i), nw, rowH, 4);
      ctx.fillStyle = ok2 ? '#eef5ee' : '#fffdf9';
      ctx.fill();
      ctx.lineWidth = ok2 ? 2 : 1;
      ctx.strokeStyle = ok2 ? GREEN : (a[i] === i ? GREEN : RED);
      ctx.stroke();
      /* accent spine */
      ctx.fillStyle = ok2 ? GREEN : acc;
      ctx.fillRect(nx + 1, rowY(i) + 3, 3, rowH - 6);

      ctx.font = 'bold ' + nFont + 'px Georgia, serif';
      ctx.fillStyle = INK;
      ctx.textAlign = 'left';
      var nlines = svWrap(ctx, this.NAMES[i], nw - 26);
      var ly = rowMid(i) - (nlines.length - 1) * (nFont + 2) / 2;
      for (q = 0; q < nlines.length; q++) {
        ctx.fillText(nlines[q], nx + 10, ly + q * (nFont + 2));
      }
      /* tick / cross */
      ctx.textAlign = 'center';
      ctx.font = 'bold 11px Georgia, serif';
      ctx.fillStyle = ok2 ? GREEN : RED;
      ctx.fillText(ok2 ? '\u2713' : '\u2715', nx + nw - 9, rowMid(i));
    }

    /* ---- fact cards ---- */
    var fFont = rowH >= 46 ? 10 : 9;
    for (q = 0; q < 6; q++) {
      f = this.SHUFFLE[q];
      var claimedBy = -1, claims = 0, j;
      for (j = 0; j < 6; j++) { if (a[j] === f) { claims++; if (claimedBy < 0) claimedBy = j; } }
      var right = (claims > 0 && a[f] === f);
      var edge = claims === 0 ? MUTED : (right ? GREEN : RED);
      svCard(ctx, fx, rowY(q), fw, rowH, 4);
      ctx.fillStyle = right ? '#eef5ee' : (claims === 0 ? '#f2ede4' : '#fdf3f1');
      ctx.fill();
      ctx.lineWidth = right ? 2 : 1;
      ctx.strokeStyle = edge;
      ctx.stroke();

      /* drag handle dots */
      ctx.fillStyle = MUTED;
      for (j = 0; j < 3; j++) {
        ctx.beginPath();
        ctx.arc(fx + 8, rowMid(q) - 5 + j * 5, 1.1, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.font = fFont + 'px Georgia, serif';
      ctx.fillStyle = claims === 0 ? MUTED : INK;
      ctx.textAlign = 'left';
      var flines = svWrap(ctx, this.FACTS[f], fw - 26);
      var maxL = Math.max(1, Math.floor((rowH - 6) / (fFont + 2)));
      if (flines.length > maxL) flines = flines.slice(0, maxL);
      var fy = rowMid(q) - (flines.length - 1) * (fFont + 2) / 2;
      for (j = 0; j < flines.length; j++) {
        ctx.fillText(flines[j], fx + 16, fy + j * (fFont + 2));
      }
    }

    /* ---- overlays for the classic slips ---- */
    ctx.textAlign = 'center';
    ctx.font = 'bold 10px Georgia, serif';
    if (d.maryConfused) {
      ctx.fillStyle = RED;
      ctx.fillText('the two Marys are swapped', (nx + nw + fx) / 2, rowMid(4) + (rowH + gap) / 2);
    } else if (d.cecilRobertConfused) {
      ctx.fillStyle = RED;
      ctx.fillText('father and son swapped', (nx + nw + fx) / 2, (rowMid(0) + rowMid(2)) / 2);
    } else if (!d.isValidPermutation) {
      ctx.fillStyle = MUTED;
      ctx.fillText('one fact, two claimants', (nx + nw + fx) / 2, top - 18 > 12 ? top - 18 : rowMid(0));
    }
  },

  caption: function (p, d) {
    if (d.allMatched) {
      return 'All six matched: Cecil ran <b>administration and finance</b>, Walsingham ran <b>intelligence</b>, Robert Cecil secured the <b>1603 succession</b>, and the Privy Council <b>advised; the queen decided</b>.';
    }
    if (d.maryConfused) {
      return 'The two Marys are swapped. <b>Mary, Queen of Scots</b> was Elizabeth\u2019s Catholic Stuart cousin, executed in 1587; <b>Mary I</b> was her half-sister, queen 1553\u20131558 \u2014 the commonest slip in Elizabethan answers. Score: ' + d.correctCount + '/6.';
    }
    if (d.cecilRobertConfused) {
      return 'Father and son are swapped. <b>William Cecil</b> held office 1558\u20131598; his son <b>Robert</b> took over and managed the succession of James VI/I in 1603. Score: ' + d.correctCount + '/6.';
    }
    if (!d.isValidPermutation) {
      return 'Two names are claiming the same fact \u2014 each of the six facts belongs to exactly one person. Score so far: <b>' + d.correctCount + '/6</b>.';
    }
    if (d.correctCount >= 4) {
      return '<b>' + d.correctCount + '/6</b> \u2014 close. Check the red lines: who was Principal Secretary <i>from 1573</i>, and who was Lord Treasurer <i>from 1572</i>?';
    }
    return '<b>' + d.correctCount + '/6</b> correct. Look for the giveaway detail on each card \u2014 a date of office, a codebreaker\u2019s name, a nickname, a number of councillors.';
  }
};

if (typeof module !== 'undefined') module.exports = W;