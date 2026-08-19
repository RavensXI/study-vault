var W = {
  meta: {
    id: 'match-the-minister',
    title: 'Match the Minister to Their Mark',
    teaches: "Cecil, Walsingham, Robert Cecil and the Privy Council each had a distinct role, method and personality that made them indispensable in different ways"
  },

  initialState: function () {
    var entities = [
      { id: 'cecil', label: 'William Cecil (Lord Burghley)' },
      { id: 'walsingham', label: 'Francis Walsingham' },
      { id: 'robertCecil', label: 'Robert Cecil' },
      { id: 'privyCouncil', label: 'The Privy Council' }
    ];
    var descriptors = [
      { id: 'd1', text: "Uncovered the Babington Plot in 1586 using intercepted, decrypted ciphers", correctEntity: 'walsingham' },
      { id: 'd2', text: "Around 19-20 hand-picked men met two or three times a week to debate policy", correctEntity: 'privyCouncil' },
      { id: 'd3', text: "Nicknamed the queen's 'little elf' - small, hunchbacked, sharp-tongued", correctEntity: 'robertCecil' },
      { id: 'd4', text: "Principal Secretary 1558-1572, then Lord Treasurer 1572-1598 - almost the whole reign", correctEntity: 'cecil' },
      { id: 'd5', text: "Personally funded his network of agents and died in debt, 1590", correctEntity: 'walsingham' },
      { id: 'd6', text: "Secured the peaceful succession of James VI of Scotland as James I in 1603", correctEntity: 'robertCecil' },
      { id: 'd7', text: "Historian John Guy called him 'the indispensable man'; trained his son Robert to succeed him", correctEntity: 'cecil' },
      { id: 'd8', text: "Advised the queen on policy, but she alone made the final decision (Penry Williams)", correctEntity: 'privyCouncil' }
    ];
    return {
      entities: entities,
      descriptors: descriptors,
      matched: {},
      pool: descriptors.map(function (d) { return d.id; }),
      selectedEntity: null,
      lastResult: null,
      mistakes: 0,
      attempts: 0
    };
  },

  apply: function (state, action) {
    function findDescriptor(id) {
      for (var i = 0; i < state.descriptors.length; i++) {
        if (state.descriptors[i].id === id) return state.descriptors[i];
      }
      return null;
    }
    function progressFor(entity) {
      var c = 0;
      for (var k in state.matched) {
        if (state.matched.hasOwnProperty(k) && state.matched[k] === entity) c++;
      }
      return c;
    }
    function copyMatched() {
      var m = {};
      for (var k in state.matched) { if (state.matched.hasOwnProperty(k)) m[k] = state.matched[k]; }
      return m;
    }

    if (action.t === 'selectEntity') {
      if (progressFor(action.entity) >= 2) return state;
      return {
        entities: state.entities,
        descriptors: state.descriptors,
        matched: state.matched,
        pool: state.pool,
        selectedEntity: action.entity,
        lastResult: null,
        mistakes: state.mistakes,
        attempts: state.attempts
      };
    }

    if (action.t === 'attemptMatch') {
      if (state.selectedEntity === null) return state;
      if (state.matched.hasOwnProperty(action.descriptor)) return state;
      var d = findDescriptor(action.descriptor);
      if (!d) return state;
      var attempts = state.attempts + 1;
      if (d.correctEntity === state.selectedEntity) {
        var matched = copyMatched();
        matched[d.id] = state.selectedEntity;
        var pool = state.pool.filter(function (id) { return id !== d.id; });
        return {
          entities: state.entities,
          descriptors: state.descriptors,
          matched: matched,
          pool: pool,
          selectedEntity: null,
          lastResult: { descriptorId: d.id, entityId: state.selectedEntity, correct: true },
          mistakes: state.mistakes,
          attempts: attempts
        };
      } else {
        return {
          entities: state.entities,
          descriptors: state.descriptors,
          matched: state.matched,
          pool: state.pool,
          selectedEntity: state.selectedEntity,
          lastResult: { descriptorId: d.id, entityId: state.selectedEntity, correct: false },
          mistakes: state.mistakes + 1,
          attempts: attempts
        };
      }
    }

    if (action.t === 'reset') {
      return W.initialState();
    }

    return state;
  },

  derive: function (state) {
    var matchedCount = 0;
    for (var k in state.matched) { if (state.matched.hasOwnProperty(k)) matchedCount++; }
    var entityProgress = {};
    for (var i = 0; i < state.entities.length; i++) {
      var eid = state.entities[i].id;
      var c = 0;
      for (var kk in state.matched) {
        if (state.matched.hasOwnProperty(kk) && state.matched[kk] === eid) c++;
      }
      entityProgress[eid] = c;
    }
    var complete = matchedCount === state.descriptors.length;
    var accuracy = state.attempts > 0 ? matchedCount / state.attempts : null;
    return {
      matchedCount: matchedCount,
      complete: complete,
      entityProgress: entityProgress,
      accuracy: accuracy
    };
  },

  regions: function (state, w, h) {
    var margin = 16;
    var leftW = w * 0.42;
    var rightX = leftW + margin * 2;
    var rightW = w - rightX - margin;
    var topY = 70;
    var boxH = (h - topY - margin) / 4;
    var regs = [];

    for (var i = 0; i < state.entities.length; i++) {
      var e = state.entities[i];
      regs.push({
        x: margin, y: topY + i * boxH, w: leftW, h: boxH - 10,
        action: { t: 'selectEntity', entity: e.id }
      });
    }

    var cols = 2, rows = 4;
    var tileW = (rightW - margin * (cols - 1)) / cols;
    var tileH = (h - topY - margin) / rows - 8;
    for (var idx = 0; idx < state.pool.length; idx++) {
      var col = idx % cols, row = Math.floor(idx / cols);
      regs.push({
        x: rightX + col * (tileW + margin),
        y: topY + row * (tileH + 8),
        w: tileW, h: tileH,
        action: { t: 'attemptMatch', descriptor: state.pool[idx] }
      });
    }

    regs.push({ x: w - 90, y: 8, w: 80, h: 26, action: { t: 'reset' } });

    return regs;
  },

  controls: [],

  render: function (ctx, state, derived, w, h, acc) {
    var ink = '#2d2a26', muted = '#8d8880', grid = '#e8e2d9';
    ctx.fillStyle = '#faf7f2';
    ctx.fillRect(0, 0, w, h);

    // header
    ctx.fillStyle = ink;
    ctx.font = 'bold 15px sans-serif';
    ctx.textBaseline = 'top';
    ctx.fillText('Mistakes: ' + state.mistakes + '    Matched: ' + derived.matchedCount + ' / 8', 16, 8);

    // reset button
    ctx.strokeStyle = muted;
    ctx.strokeRect(w - 90, 8, 80, 26);
    ctx.fillStyle = muted;
    ctx.font = '12px sans-serif';
    ctx.fillText('Reset', w - 74, 15);

    var margin = 16;
    var leftW = w * 0.42;
    var rightX = leftW + margin * 2;
    var rightW = w - rightX - margin;
    var topY = 70;
    var boxH = (h - topY - margin) / 4;

    // boxes
    for (var i = 0; i < state.entities.length; i++) {
      var e = state.entities[i];
      var bx = margin, by = topY + i * boxH, bw = leftW, bh = boxH - 10;
      var selected = state.selectedEntity === e.id;

      ctx.fillStyle = '#fff';
      ctx.fillRect(bx, by, bw, bh);
      ctx.lineWidth = selected ? 3 : 1;
      ctx.strokeStyle = selected ? acc : grid;
      ctx.strokeRect(bx, by, bw, bh);

      ctx.fillStyle = ink;
      ctx.font = 'bold 13px sans-serif';
      ctx.fillText(e.label, bx + 8, by + 6);

      // slots
      var matchedHere = [];
      for (var di = 0; di < state.descriptors.length; di++) {
        var d = state.descriptors[di];
        if (state.matched[d.id] === e.id) matchedHere.push(d);
      }
      var slotH = (bh - 30) / 2;
      for (var s = 0; s < 2; s++) {
        var sy = by + 28 + s * (slotH + 4);
        ctx.strokeStyle = grid;
        ctx.strokeRect(bx + 8, sy, bw - 16, slotH - 4);
        if (matchedHere[s]) {
          ctx.fillStyle = '#eef7ee';
          ctx.fillRect(bx + 8, sy, bw - 16, slotH - 4);
          ctx.strokeStyle = '#3a7d3a';
          ctx.strokeRect(bx + 8, sy, bw - 16, slotH - 4);
          ctx.fillStyle = ink;
          ctx.font = '11px sans-serif';
          wrapText(ctx, matchedHere[s].text, bx + 12, sy + 4, bw - 40, 13);
          ctx.fillStyle = '#3a7d3a';
          ctx.font = 'bold 14px sans-serif';
          ctx.fillText('\u2713', bx + bw - 22, sy + 4);
        } else {
          ctx.fillStyle = muted;
          ctx.font = '11px sans-serif';
          ctx.fillText('empty', bx + 12, sy + slotH / 2 - 10);
        }
      }
    }

    // pool tiles
    var cols = 2, rows = 4;
    var tileW = (rightW - margin * (cols - 1)) / cols;
    var tileH = (h - topY - margin) / rows - 8;
    for (var idx = 0; idx < state.pool.length; idx++) {
      var col = idx % cols, row = Math.floor(idx / cols);
      var tx = rightX + col * (tileW + margin);
      var ty = topY + row * (tileH + 8);
      var id = state.pool[idx];
      var isBad = state.lastResult && state.lastResult.correct === false && state.lastResult.descriptorId === id;

      ctx.fillStyle = isBad ? '#f8e2e0' : '#fff';
      ctx.fillRect(tx, ty, tileW, tileH);
      ctx.strokeStyle = isBad ? '#b8433a' : grid;
      ctx.lineWidth = isBad ? 2 : 1;
      ctx.strokeRect(tx, ty, tileW, tileH);

      var text = '';
      for (var q = 0; q < state.descriptors.length; q++) {
        if (state.descriptors[q].id === id) { text = state.descriptors[q].text; break; }
      }
      ctx.fillStyle = ink;
      ctx.font = '11px sans-serif';
      wrapText(ctx, text, tx + 6, ty + 6, tileW - 12, 13);
    }

    function wrapText(ctx, text, x, y, maxW, lh) {
      var words = text.split(' ');
      var line = '';
      var yy = y;
      for (var wI = 0; wI < words.length; wI++) {
        var test = line + words[wI] + ' ';
        if (ctx.measureText(test).width > maxW && line !== '') {
          ctx.fillText(line, x, yy);
          line = words[wI] + ' ';
          yy += lh;
        } else {
          line = test;
        }
      }
      ctx.fillText(line, x, yy);
    }
  },

  caption: function (state, derived) {
    if (derived.complete) {
      return 'All eight matched, with ' + state.mistakes + ' mistake' + (state.mistakes === 1 ? '' : 's') + ' - Cecil managed money and time, Walsingham managed secrets, Robert Cecil managed the succession, and the Council only advised.';
    }
    if (state.selectedEntity) {
      var label = '';
      for (var i = 0; i < state.entities.length; i++) {
        if (state.entities[i].id === state.selectedEntity) label = state.entities[i].label;
      }
      return 'Now find both descriptions that belong to ' + label + '.';
    }
    if (state.mistakes > 0) {
      return "Careful - Cecil's patient finance work is easily confused with Walsingham's secret intelligence work.";
    }
    return 'Click a minister on the left, then click the description tile that matches them.';
  }
};

if (typeof module !== 'undefined') module.exports = W;