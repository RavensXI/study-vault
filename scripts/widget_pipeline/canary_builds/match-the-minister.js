(function () {
  'use strict';

  var ENTITIES = [
    { id: 'cecil', label: 'William Cecil (Lord Burghley)' },
    { id: 'walsingham', label: 'Sir Francis Walsingham' },
    { id: 'robertCecil', label: 'Robert Cecil' },
    { id: 'privyCouncil', label: 'The Privy Council' }
  ];

  var DESCRIPTOR_BASE = [
    { id: 'd1', text: 'Served as Principal Secretary 1558\u20131572, then Lord Treasurer 1572\u20131598 \u2014 almost the whole reign', correctEntity: 'cecil' },
    { id: 'd2', text: "Trained his son Robert to succeed him, producing an almost seamless transition of power in 1598", correctEntity: 'cecil' },
    { id: 'd3', text: 'Uncovered the Babington Plot in 1586 using intercepted, decrypted ciphers', correctEntity: 'walsingham' },
    { id: 'd4', text: 'Personally funded a network of agents from his own pocket and died in debt in 1590', correctEntity: 'walsingham' },
    { id: 'd5', text: "Nicknamed the queen's 'little elf' \u2014 small, hunchbacked and sharp-tongued", correctEntity: 'robertCecil' },
    { id: 'd6', text: 'Secured the peaceful succession of James VI of Scotland as James I in 1603', correctEntity: 'robertCecil' },
    { id: 'd7', text: 'Around 19\u201320 hand-picked men who met two or three times a week to debate policy', correctEntity: 'privyCouncil' },
    { id: 'd8', text: "Advised the queen on her options but left the final ruling to her \u2014 'the Council advised, the queen decided'", correctEntity: 'privyCouncil' }
  ];

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function initialState() {
    var descriptors = shuffle(DESCRIPTOR_BASE.map(function (d) { return { id: d.id, text: d.text, correctEntity: d.correctEntity }; }));
    var pool = shuffle(descriptors.map(function (d) { return d.id; }));
    return {
      entities: ENTITIES.slice(),
      descriptors: descriptors,
      matched: {},
      pool: pool,
      selectedEntity: null,
      lastResult: null,
      mistakes: 0,
      attempts: 0
    };
  }

  function derive(s) {
    var matchedCount = Object.keys(s.matched).length;
    var entityProgress = {};
    s.entities.forEach(function (e) { entityProgress[e.id] = 0; });
    Object.keys(s.matched).forEach(function (dId) {
      var eId = s.matched[dId];
      entityProgress[eId] = (entityProgress[eId] || 0) + 1;
    });
    var complete = matchedCount === s.descriptors.length;
    var accuracy = s.attempts > 0 ? matchedCount / s.attempts : null;
    return { matchedCount: matchedCount, complete: complete, entityProgress: entityProgress, accuracy: accuracy };
  }

  function findDescriptor(s, id) {
    for (var i = 0; i < s.descriptors.length; i++) {
      if (s.descriptors[i].id === id) return s.descriptors[i];
    }
    return null;
  }

  function apply(s, action) {
    if (action.t === 'reset') {
      return initialState();
    }
    if (action.t === 'selectEntity') {
      var d0 = derive(s);
      if (d0.entityProgress[action.entity] >= 2) {
        return Object.assign({}, s);
      }
      return Object.assign({}, s, { selectedEntity: action.entity });
    }
    if (action.t === 'attemptMatch') {
      if (s.selectedEntity === null) return Object.assign({}, s);
      if (Object.prototype.hasOwnProperty.call(s.matched, action.descriptor)) return Object.assign({}, s);
      var desc = findDescriptor(s, action.descriptor);
      if (!desc) return Object.assign({}, s);
      var correct = desc.correctEntity === s.selectedEntity;
      var newAttempts = s.attempts + 1;
      if (correct) {
        var newMatched = Object.assign({}, s.matched);
        newMatched[action.descriptor] = s.selectedEntity;
        var newPool = s.pool.filter(function (id) { return id !== action.descriptor; });
        return Object.assign({}, s, {
          matched: newMatched,
          pool: newPool,
          selectedEntity: null,
          lastResult: { descriptorId: action.descriptor, entityId: s.selectedEntity, correct: true },
          attempts: newAttempts
        });
      } else {
        return Object.assign({}, s, {
          mistakes: s.mistakes + 1,
          attempts: newAttempts,
          lastResult: { descriptorId: action.descriptor, entityId: s.selectedEntity, correct: false }
        });
      }
    }
    return Object.assign({}, s);
  }

  window.SVWidget = {
    meta: {
      id: 'match-the-minister',
      title: 'Match the Minister to Their Mark',
      teaches: "Cecil, Walsingham, Robert Cecil and the Privy Council each had a distinct role, method and personality that made them indispensable in different ways"
    },
    mount: function (root, ctx) {
      var accent = (ctx && ctx.accent) || '#a5673f';
      var reducedMotion = !!(ctx && ctx.reducedMotion);

      var style = document.createElement('style');
      style.textContent = [
        '.mtm-wrap{font-family:Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;padding:16px;border-radius:14px;box-sizing:border-box;max-width:900px;}',
        '.mtm-wrap *{box-sizing:border-box;}',
        '.mtm-header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:12px;}',
        '.mtm-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.25rem;margin:0;}',
        '.mtm-stats{font-size:0.9rem;color:#8d8880;display:flex;gap:14px;flex-wrap:wrap;}',
        '.mtm-stats b{color:#2d2a26;}',
        '.mtm-board{display:grid;grid-template-columns:1fr;gap:20px;}',
        '@media(min-width:640px){.mtm-board{grid-template-columns:1.1fr 1fr;}}',
        '.mtm-col-title{font-size:0.8rem;text-transform:uppercase;letter-spacing:0.05em;color:#8d8880;margin:0 0 8px 2px;}',
        '.mtm-entities{display:flex;flex-direction:column;gap:10px;}',
        '.mtm-entity{border:1px solid #e8e2d9;background:#fff;border-radius:14px;padding:10px;transition:border-color .15s,box-shadow .15s;}',
        '.mtm-entity.selected{border-color:' + accent + ';box-shadow:0 0 0 3px ' + accent + '33;}',
        '.mtm-entity.full{opacity:0.85;}',
        '.mtm-entity-head{width:100%;text-align:left;background:none;border:none;font-family:"Source Serif 4",Georgia,serif;font-size:1.02rem;font-weight:600;color:#2d2a26;padding:4px 6px;cursor:pointer;border-radius:8px;}',
        '.mtm-entity-head:hover{background:#f2ece2;}',
        '.mtm-entity-head:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px;}',
        '.mtm-entity-head[disabled]{cursor:default;}',
        '.mtm-slots{display:flex;flex-direction:column;gap:6px;margin-top:6px;}',
        '.mtm-slot{min-height:44px;border:1px dashed #d8d0c2;border-radius:10px;padding:8px 10px;font-size:0.85rem;display:flex;align-items:center;gap:6px;background:#faf8f5;}',
        '.mtm-slot.filled{border-style:solid;border-color:#2f9e5c;background:#eef8f1;color:#204d34;}',
        '.mtm-tick{color:#2f9e5c;font-weight:700;flex-shrink:0;}',
        '.mtm-grid{display:grid;grid-template-columns:1fr;gap:8px;}',
        '@media(min-width:420px){.mtm-grid{grid-template-columns:1fr 1fr;}}',
        '.mtm-tile{border:1px solid #e8e2d9;background:#fff;border-radius:12px;padding:10px;font-size:0.83rem;text-align:left;cursor:pointer;line-height:1.3;transition:border-color .15s,background .15s;}',
        '.mtm-tile:hover{border-color:' + accent + ';}',
        '.mtm-tile:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px;}',
        '.mtm-tile.wrong{background:#fbe3e0;border-color:#c0392b;animation:mtm-shake .35s;}',
        '.mtm-tile.disabled-hint{opacity:0.55;cursor:not-allowed;}',
        '@keyframes mtm-shake{10%,90%{transform:translateX(-1px);}20%,80%{transform:translateX(2px);}30%,50%,70%{transform:translateX(-4px);}40%,60%{transform:translateX(4px);}}',
        '.mtm-footer{margin-top:14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;}',
        '.mtm-btn{background:' + accent + ';color:#fff;border:none;border-radius:10px;padding:8px 16px;font-size:0.9rem;cursor:pointer;font-family:Inter,sans-serif;}',
        '.mtm-btn:hover{filter:brightness(0.95);}',
        '.mtm-btn.secondary{background:#fff;color:' + accent + ';border:1px solid ' + accent + ';}',
        '.mtm-hint{font-size:0.85rem;color:#8d8880;}',
        '.mtm-complete{margin-top:10px;padding:10px 14px;background:#eef8f1;border:1px solid #2f9e5c;border-radius:10px;color:#204d34;font-size:0.9rem;}'
      ].join('\n');
      root.appendChild(style);

      var wrap = document.createElement('div');
      wrap.className = 'mtm-wrap';
      root.appendChild(wrap);

      var state = initialState();
      var wrongTileId = null; // used briefly to trigger shake class

      function publish() {
        var d = derive(state);
        root.dataset.svState = JSON.stringify({
          matchedCount: d.matchedCount,
          complete: d.complete,
          mistakes: state.mistakes,
          attempts: state.attempts,
          accuracy: d.accuracy,
          selectedEntity: state.selectedEntity,
          lastResult: state.lastResult
        });
      }

      function dispatch(action) {
        state = apply(state, action);
        publish();
        render();
      }

      function entityLabel(id) {
        for (var i = 0; i < ENTITIES.length; i++) if (ENTITIES[i].id === id) return ENTITIES[i].label;
        return id;
      }

      function render() {
        var d = derive(state);
        wrap.innerHTML = '';

        var header = document.createElement('div');
        header.className = 'mtm-header';
        var h = document.createElement('h2');
        h.className = 'mtm-title';
        h.textContent = 'Match the Minister to Their Mark';
        var stats = document.createElement('div');
        stats.className = 'mtm-stats';
        stats.innerHTML = '<span>Matched: <b>' + d.matchedCount + ' / ' + state.descriptors.length + '</b></span>' +
          '<span>Mistakes: <b>' + state.mistakes + '</b></span>';
        header.appendChild(h);
        header.appendChild(stats);
        wrap.appendChild(header);

        var board = document.createElement('div');
        board.className = 'mtm-board';
        wrap.appendChild(board);

        // left column
        var leftCol = document.createElement('div');
        var leftTitle = document.createElement('p');
        leftTitle.className = 'mtm-col-title';
        leftTitle.textContent = 'Choose a minister, then a fact';
        leftCol.appendChild(leftTitle);
        var entitiesWrap = document.createElement('div');
        entitiesWrap.className = 'mtm-entities';
        leftCol.appendChild(entitiesWrap);
        board.appendChild(leftCol);

        state.entities.forEach(function (ent) {
          var box = document.createElement('div');
          var progress = d.entityProgress[ent.id] || 0;
          var isFull = progress >= 2;
          box.className = 'mtm-entity' + (state.selectedEntity === ent.id ? ' selected' : '') + (isFull ? ' full' : '');

          var headBtn = document.createElement('button');
          headBtn.className = 'mtm-entity-head';
          headBtn.type = 'button';
          headBtn.textContent = ent.label + (isFull ? ' \u2713 complete' : '');
          if (isFull) headBtn.setAttribute('disabled', 'true');
          headBtn.addEventListener('click', function () {
            dispatch({ t: 'selectEntity', entity: ent.id });
          });
          box.appendChild(headBtn);

          var slots = document.createElement('div');
          slots.className = 'mtm-slots';
          var descIdsForEntity = Object.keys(state.matched).filter(function (k) { return state.matched[k] === ent.id; });
          for (var i = 0; i < 2; i++) {
            var slot = document.createElement('div');
            if (descIdsForEntity[i]) {
              slot.className = 'mtm-slot filled';
              var desc = findDescriptor(state, descIdsForEntity[i]);
              var tick = document.createElement('span');
              tick.className = 'mtm-tick';
              tick.textContent = '\u2713';
              slot.appendChild(tick);
              var txt = document.createElement('span');
              txt.textContent = desc ? desc.text : '';
              slot.appendChild(txt);
            } else {
              slot.className = 'mtm-slot';
              slot.textContent = 'Empty slot';
              slot.style.color = '#b8b0a2';
            }
            slots.appendChild(slot);
          }
          box.appendChild(slots);
          entitiesWrap.appendChild(box);
        });

        // right column
        var rightCol = document.createElement('div');
        var rightTitle = document.createElement('p');
        rightTitle.className = 'mtm-col-title';
        rightTitle.textContent = 'Description tiles';
        rightCol.appendChild(rightTitle);
        var grid = document.createElement('div');
        grid.className = 'mtm-grid';
        rightCol.appendChild(grid);
        board.appendChild(rightCol);

        state.pool.forEach(function (descId) {
          var desc = findDescriptor(state, descId);
          if (!desc) return;
          var tile = document.createElement('button');
          tile.type = 'button';
          tile.className = 'mtm-tile';
          if (!state.selectedEntity) tile.classList.add('disabled-hint');
          if (wrongTileId === descId) tile.classList.add('wrong');
          tile.textContent = desc.text;
          tile.setAttribute('tabindex', '0');
          tile.addEventListener('click', function () {
            if (!state.selectedEntity) return;
            var beforeMatched = Object.prototype.hasOwnProperty.call(state.matched, descId);
            dispatch({ t: 'attemptMatch', descriptor: descId });
            var afterMatched = Object.prototype.hasOwnProperty.call(state.matched, descId);
            if (!afterMatched && !beforeMatched) {
              wrongTileId = descId;
              render();
              if (reducedMotion) {
                setTimeout(function () { wrongTileId = null; render(); }, 200);
              } else {
                setTimeout(function () { wrongTileId = null; render(); }, 420);
              }
            }
          });
          grid.appendChild(tile);
        });

        // footer
        var footer = document.createElement('div');
        footer.className = 'mtm-footer';
        var hint = document.createElement('span');
        hint.className = 'mtm-hint';
        if (d.complete) {
          hint.textContent = 'All matched! Well done.';
        } else if (state.selectedEntity) {
          hint.textContent = 'Selected: ' + entityLabel(state.selectedEntity) + ' \u2014 now click a matching fact.';
        } else {
          hint.textContent = 'Click a minister\u2019s name on the left to begin.';
        }
        footer.appendChild(hint);

        var resetBtn = document.createElement('button');
        resetBtn.className = 'mtm-btn secondary';
        resetBtn.type = 'button';
        resetBtn.textContent = 'Reset';
        resetBtn.addEventListener('click', function () {
          wrongTileId = null;
          dispatch({ t: 'reset' });
        });
        footer.appendChild(resetBtn);
        wrap.appendChild(footer);

        if (d.complete) {
          var done = document.createElement('div');
          done.className = 'mtm-complete';
          var acc = d.accuracy !== null ? Math.round(d.accuracy * 100) : 0;
          done.textContent = 'Board complete \u2014 ' + state.attempts + ' attempts, ' + state.mistakes + ' mistake' + (state.mistakes === 1 ? '' : 's') + ' (' + acc + '% accuracy).';
          wrap.appendChild(done);
        }
      }

      publish();
      render();
    }
  };
})();