(function () {
  'use strict';

  var ENTITIES = [
    { id: 'cecil', name: 'William Cecil, Lord Burghley' },
    { id: 'walsingham', name: 'Sir Francis Walsingham' },
    { id: 'robertCecil', name: 'Robert Cecil' },
    { id: 'privyCouncil', name: 'The Privy Council' }
  ];

  var DESCRIPTORS = [
    {
      id: 'd1',
      correctEntity: 'cecil',
      text: 'Principal Secretary from 1558, then Lord Treasurer from 1572 \u2014 in office almost the entire reign',
      why: 'He served from the day Elizabeth became queen until his death in 1598.',
      hint: 'Whose career runs right across the reign, 1558 to 1598?'
    },
    {
      id: 'd2',
      correctEntity: 'cecil',
      text: 'Weighed every option in patient written memoranda; John Guy called him \u2018the indispensable man\u2019',
      why: 'Paperwork and patience \u2014 not secrecy \u2014 were his method.',
      hint: 'Whose method was careful administration rather than spycraft?'
    },
    {
      id: 'd3',
      correctEntity: 'walsingham',
      text: 'Uncovered the Babington Plot in 1586 using intercepted, decrypted ciphers',
      why: 'The evidence convicted Mary, Queen of Scots, executed at Fotheringhay in 1587.',
      hint: 'Who ran the informants, the double agents and the code-breakers?'
    },
    {
      id: 'd4',
      correctEntity: 'walsingham',
      text: 'Paid his agents out of his own pocket and died in debt in 1590',
      why: 'The Crown would not fund spies, so he funded them himself \u2014 and kept them secret.',
      hint: 'Who ended up poor because he financed secret work himself?'
    },
    {
      id: 'd5',
      correctEntity: 'robertCecil',
      text: 'Small, hunchbacked and sharp-tongued \u2014 the queen\u2019s \u2018little elf\u2019',
      why: 'Elizabeth\u2019s nickname for Burghley\u2019s younger son.',
      hint: 'Which minister did Elizabeth tease about his size?'
    },
    {
      id: 'd6',
      correctEntity: 'robertCecil',
      text: 'Handled the secret negotiations that brought James VI of Scotland to the throne in 1603',
      why: 'He secured a peaceful succession after Elizabeth\u2019s death.',
      hint: 'Who was still the leading minister after 1598, and after 1603?'
    },
    {
      id: 'd7',
      correctEntity: 'privyCouncil',
      text: 'Around 19\u201320 hand-picked men, meeting two or three times a week',
      why: 'A body of many men, with a Clerk keeping the notes.',
      hint: 'Which of these is a group, not a single person?'
    },
    {
      id: 'd8',
      correctEntity: 'privyCouncil',
      text: 'Debated policy and summarised the choices \u2014 but, as Penry Williams put it, it advised while the queen decided',
      why: 'Advice only: ultimate authority stayed firmly with Elizabeth.',
      hint: 'Who could argue over the options but never make the final ruling?'
    }
  ];

  function byId(id) {
    for (var i = 0; i < DESCRIPTORS.length; i++) if (DESCRIPTORS[i].id === id) return DESCRIPTORS[i];
    return null;
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function initialState() {
    var order = shuffle(DESCRIPTORS.map(function (d) { return d.id; }));
    return {
      descriptors: DESCRIPTORS,
      pool: order,
      matched: {},
      selectedEntity: null,
      lastResult: null,
      mistakes: 0,
      attempts: 0
    };
  }

  function derive(s) {
    var keys = Object.keys(s.matched);
    var prog = {};
    ENTITIES.forEach(function (e) { prog[e.id] = 0; });
    keys.forEach(function (k) { prog[s.matched[k]] = (prog[s.matched[k]] || 0) + 1; });
    return {
      matchedCount: keys.length,
      complete: keys.length === DESCRIPTORS.length,
      entityProgress: prog,
      accuracy: s.attempts === 0 ? null : keys.length / s.attempts
    };
  }

  function apply(s, a) {
    var d;
    if (a.t === 'selectEntity') {
      var prog = derive(s).entityProgress;
      if (prog[a.entity] >= 2) return s;
      return {
        descriptors: s.descriptors, pool: s.pool, matched: s.matched,
        selectedEntity: s.selectedEntity === a.entity ? null : a.entity,
        lastResult: null, mistakes: s.mistakes, attempts: s.attempts
      };
    }
    if (a.t === 'attemptMatch') {
      if (!s.selectedEntity) return s;
      if (Object.prototype.hasOwnProperty.call(s.matched, a.descriptor)) return s;
      d = byId(a.descriptor);
      if (!d) return s;
      var correct = d.correctEntity === s.selectedEntity;
      if (correct) {
        var nm = {};
        Object.keys(s.matched).forEach(function (k) { nm[k] = s.matched[k]; });
        nm[d.id] = s.selectedEntity;
        return {
          descriptors: s.descriptors,
          pool: s.pool.filter(function (x) { return x !== d.id; }),
          matched: nm,
          selectedEntity: null,
          lastResult: { descriptorId: d.id, entityId: s.selectedEntity, correct: true },
          mistakes: s.mistakes,
          attempts: s.attempts + 1
        };
      }
      return {
        descriptors: s.descriptors, pool: s.pool, matched: s.matched,
        selectedEntity: s.selectedEntity,
        lastResult: { descriptorId: d.id, entityId: s.selectedEntity, correct: false },
        mistakes: s.mistakes + 1,
        attempts: s.attempts + 1
      };
    }
    if (a.t === 'reset') return initialState();
    return s;
  }

  var CSS = [
    '.mtm{--ink:#2d2a26;--muted:#8d8880;--line:#e8e2d9;--paper:#faf8f5;--ok:#3f7d52;--bad:#b4443a;',
    'font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;',
    'color:var(--ink);background:var(--paper);padding:16px;border-radius:16px;box-sizing:border-box;}',
    '.mtm *{box-sizing:border-box;}',
    '.mtm h2{font-family:"Source Serif 4",Georgia,serif;font-size:19px;margin:0 0 2px;font-weight:600;}',
    '.mtm .sub{font-size:13px;color:var(--muted);margin:0 0 12px;line-height:1.45;}',
    '.mtm .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px;}',
    '.mtm .chip{font-size:12px;border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 10px;color:var(--ink);}',
    '.mtm .chip b{font-variant-numeric:tabular-nums;}',
    '.mtm .track{flex:1 1 90px;height:6px;background:#efeae1;border-radius:999px;overflow:hidden;min-width:70px;}',
    '.mtm .fill{height:100%;background:var(--accent);width:0;transition:width .35s ease;}',
    '.mtm .reduced .fill{transition:none;}',
    '.mtm .feedback{border:1px solid var(--line);background:#fff;border-radius:12px;padding:9px 12px;font-size:13px;line-height:1.45;min-height:40px;display:flex;align-items:center;margin-bottom:12px;}',
    '.mtm .feedback.ok{border-color:var(--ok);background:#f2f8f3;color:#28563a;}',
    '.mtm .feedback.bad{border-color:var(--bad);background:#fdf1ef;color:#8e2f27;}',
    '.mtm .board{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:14px;}',
    '.mtm.narrow .board{grid-template-columns:1fr;}',
    '.mtm .colhead{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:0 0 6px;}',
    '.mtm .ent{background:#fff;border:1px solid var(--line);border-radius:14px;padding:8px;margin-bottom:10px;transition:border-color .18s ease,background .18s ease;}',
    '.mtm .ent.sel{border-color:var(--accent);background:#fffdf7;box-shadow:inset 0 0 0 1px var(--accent);}',
    '.mtm .ent.full{opacity:.85;}',
    '.mtm .entbtn{display:flex;width:100%;align-items:baseline;justify-content:space-between;gap:8px;background:none;border:0;padding:6px 6px 8px;text-align:left;cursor:pointer;color:inherit;font:inherit;border-radius:10px;}',
    '.mtm .entbtn:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}',
    '.mtm .entname{font-family:"Source Serif 4",Georgia,serif;font-size:15px;font-weight:600;line-height:1.25;}',
    '.mtm .count{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap;}',
    '.mtm .ent.full .count{color:var(--ok);}',
    '.mtm .slot{border:1px dashed #d9d2c6;border-radius:10px;min-height:42px;margin:0 0 6px;padding:8px 10px;font-size:12.5px;line-height:1.4;color:var(--muted);display:flex;gap:8px;align-items:flex-start;}',
    '.mtm .slot:last-child{margin-bottom:2px;}',
    '.mtm .slot.filled{border-style:solid;border-color:#cfe0d3;background:#f4f9f5;color:var(--ink);}',
    '.mtm .slot .tick{flex:0 0 auto;color:var(--ok);font-weight:700;line-height:1.3;}',
    '.mtm .slot .why{display:block;color:var(--muted);font-size:11.5px;margin-top:3px;}',
    '.mtm .pool{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:8px;align-content:start;}',
    '.mtm.narrow .pool{grid-template-columns:1fr;}',
    '.mtm .tile{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 11px;font:inherit;font-size:12.8px;line-height:1.42;text-align:left;color:var(--ink);cursor:pointer;transition:border-color .15s ease,transform .15s ease,background .15s ease;}',
    '.mtm .tile:hover{border-color:var(--accent);}',
    '.mtm .tile:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}',
    '.mtm .tile.wrong{border-color:var(--bad);background:#fdecea;color:#8e2f27;}',
    '.mtm .tile.shake{animation:mtmshake .42s ease;}',
    '@keyframes mtmshake{0%,100%{transform:translateX(0)}15%{transform:translateX(-6px)}30%{transform:translateX(6px)}45%{transform:translateX(-4px)}60%{transform:translateX(4px)}80%{transform:translateX(-2px)}}',
    '.mtm .pop{animation:mtmpop .32s ease;}',
    '@keyframes mtmpop{0%{transform:scale(.94);opacity:.4}100%{transform:scale(1);opacity:1}}',
    '.mtm .done{border:1px solid var(--accent);background:#fffdf7;border-radius:12px;padding:12px 14px;font-size:13.5px;line-height:1.5;}',
    '.mtm .done b{font-family:"Source Serif 4",Georgia,serif;}',
    '.mtm .foot{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:12px;flex-wrap:wrap;}',
    '.mtm .hintline{font-size:12px;color:var(--muted);flex:1 1 auto;}',
    '.mtm .reset{font:inherit;font-size:13px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:7px 14px;cursor:pointer;color:var(--ink);}',
    '.mtm .reset:hover{border-color:var(--accent);}',
    '.mtm .reset:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'match-the-minister',
      title: 'Match the Minister to Their Mark',
      teaches: 'Cecil, Walsingham, Robert Cecil and the Privy Council each had a distinct role, method and personality that made them indispensable in different ways'
    },
    mount: function (root, ctx) {
      var accent = (ctx && ctx.accent) || '#b8860b';
      var reduced = !!(ctx && ctx.reducedMotion);

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      var wrap = document.createElement('div');
      wrap.className = 'mtm' + (reduced ? ' reduced' : '');
      wrap.style.setProperty('--accent', accent);
      root.appendChild(wrap);

      wrap.innerHTML =
        '<h2>Match the minister to their mark</h2>' +
        '<p class="sub">Choose a minister (or the Council) on the left, then choose the description that belongs to them. Two each. Watch the traps: Cecil\u2019s patient paperwork is not Walsingham\u2019s secrecy, and the Council only advised.</p>' +
        '<div class="bar">' +
          '<span class="chip">Matched <b id="mtm-m">0</b>/8</span>' +
          '<span class="chip">Mistakes <b id="mtm-x">0</b></span>' +
          '<span class="track"><span class="fill" id="mtm-fill"></span></span>' +
        '</div>' +
        '<div class="feedback" id="mtm-fb" role="status" aria-live="polite"></div>' +
        '<div class="board">' +
          '<div><p class="colhead">The people</p><div id="mtm-ents"></div></div>' +
          '<div><p class="colhead">The marks they left</p><div class="pool" id="mtm-pool"></div></div>' +
        '</div>' +
        '<div class="foot"><span class="hintline" id="mtm-hint"></span>' +
        '<button type="button" class="reset" id="mtm-reset">Shuffle &amp; start again</button></div>';

      var elM = wrap.querySelector('#mtm-m');
      var elX = wrap.querySelector('#mtm-x');
      var elFill = wrap.querySelector('#mtm-fill');
      var elFb = wrap.querySelector('#mtm-fb');
      var elEnts = wrap.querySelector('#mtm-ents');
      var elPool = wrap.querySelector('#mtm-pool');
      var elHint = wrap.querySelector('#mtm-hint');
      var elReset = wrap.querySelector('#mtm-reset');

      var state = initialState();
      var focusKey = null;
      var justMatched = null;
      var shakeId = null;
      var shakeTimer = null;

      function entityName(id) {
        for (var i = 0; i < ENTITIES.length; i++) if (ENTITIES[i].id === id) return ENTITIES[i].name;
        return id;
      }

      function feedback() {
        var d = derive(state);
        elFb.className = 'feedback';
        if (d.complete) {
          var pct = Math.round(d.matchedCount / state.attempts * 100);
          elFb.classList.add('ok');
          elFb.textContent = 'All eight placed. ' + state.attempts + ' attempts, ' + state.mistakes +
            ' mistake' + (state.mistakes === 1 ? '' : 's') + ' \u2014 ' + pct + '% accuracy.';
          return;
        }
        var lr = state.lastResult;
        if (lr) {
          var desc = byId(lr.descriptorId);
          if (lr.correct) {
            elFb.classList.add('ok');
            elFb.textContent = 'Correct \u2014 ' + entityName(lr.entityId) + '. ' + desc.why;
          } else {
            elFb.classList.add('bad');
            elFb.textContent = 'Not ' + entityName(lr.entityId) + '. ' + desc.hint;
          }
          return;
        }
        if (state.selectedEntity) {
          elFb.textContent = 'Now pick a description that fits ' + entityName(state.selectedEntity) + '.';
        } else {
          elFb.textContent = 'Start by choosing a name on the left.';
        }
      }

      function render() {
        var d = derive(state);
        elM.textContent = String(d.matchedCount);
        elX.textContent = String(state.mistakes);
        elFill.style.width = (d.matchedCount / 8 * 100) + '%';

        elEnts.innerHTML = '';
        ENTITIES.forEach(function (e) {
          var prog = d.entityProgress[e.id] || 0;
          var card = document.createElement('div');
          card.className = 'ent' + (state.selectedEntity === e.id ? ' sel' : '') + (prog === 2 ? ' full' : '');

          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'entbtn';
          btn.setAttribute('aria-pressed', state.selectedEntity === e.id ? 'true' : 'false');
          btn.dataset.focus = 'ent-' + e.id;
          if (prog === 2) btn.setAttribute('aria-disabled', 'true');
          btn.innerHTML = '<span class="entname"></span><span class="count"></span>';
          btn.querySelector('.entname').textContent = e.name;
          btn.querySelector('.count').textContent = prog === 2 ? '2/2 \u2713' : prog + '/2';
          btn.addEventListener('click', function () {
            focusKey = 'ent-' + e.id;
            justMatched = null;
            state = apply(state, { t: 'selectEntity', entity: e.id });
            if (derive(state).entityProgress[e.id] >= 2) {
              elFb.className = 'feedback';
              elFb.textContent = entityName(e.id) + ' is already complete \u2014 pick another.';
              publish();
              return;
            }
            render();
          });
          card.appendChild(btn);

          var mine = Object.keys(state.matched).filter(function (k) { return state.matched[k] === e.id; });
          for (var i = 0; i < 2; i++) {
            var slot = document.createElement('div');
            slot.className = 'slot';
            if (mine[i]) {
              var dd = byId(mine[i]);
              slot.className += ' filled';
              if (justMatched === mine[i] && !reduced) slot.className += ' pop';
              var tick = document.createElement('span');
              tick.className = 'tick';
              tick.textContent = '\u2713';
              var txt = document.createElement('span');
              txt.appendChild(document.createTextNode(dd.text));
              var why = document.createElement('span');
              why.className = 'why';
              why.textContent = dd.why;
              txt.appendChild(why);
              slot.appendChild(tick);
              slot.appendChild(txt);
            } else {
              slot.textContent = 'empty slot';
            }
            card.appendChild(slot);
          }
          elEnts.appendChild(card);
        });

        elPool.innerHTML = '';
        if (d.complete) {
          var done = document.createElement('div');
          done.className = 'done';
          done.innerHTML = '<b>Board complete.</b> Cecil turned decisions into working policy for forty years; ' +
            'Walsingham bought secrets with his own money; Robert Cecil carried the machine into a new reign; ' +
            'the Privy Council supplied the arguments \u2014 but Elizabeth alone supplied the decision.';
          elPool.appendChild(done);
        } else {
          state.pool.forEach(function (id) {
            var dd = byId(id);
            var t = document.createElement('button');
            t.type = 'button';
            t.className = 'tile';
            t.dataset.focus = 'tile-' + id;
            t.textContent = dd.text;
            if (shakeId === id) {
              t.classList.add('wrong');
              if (!reduced) t.classList.add('shake');
            }
            t.addEventListener('click', function () {
              justMatched = null;
              if (!state.selectedEntity) {
                elFb.className = 'feedback';
                elFb.textContent = 'Choose a name on the left first, then this tile.';
                publish();
                return;
              }
              var before = state;
              focusKey = 'tile-' + id;
              state = apply(state, { t: 'attemptMatch', descriptor: id });
              var lr = state.lastResult;
              if (lr && lr.correct) {
                justMatched = id;
                shakeId = null;
                focusKey = null;
                render();
                var next = elPool.querySelector('.tile');
                if (next) next.focus(); else elReset.focus();
              } else if (state !== before) {
                shakeId = id;
                render();
                if (shakeTimer) clearTimeout(shakeTimer);
                shakeTimer = setTimeout(function () {
                  shakeId = null;
                  var el = elPool.querySelector('[data-focus="tile-' + id + '"]');
                  if (el) el.classList.remove('wrong', 'shake');
                }, 620);
              }
            });
            elPool.appendChild(t);
          });
        }

        elHint.textContent = derive(state).complete
          ? 'Try again for a clean run with no mistakes.'
          : (state.selectedEntity ? 'Selected: ' + entityName(state.selectedEntity) : 'Nothing selected.');

        feedback();

        if (focusKey) {
          var f = wrap.querySelector('[data-focus="' + focusKey + '"]');
          if (f) f.focus();
          focusKey = null;
        }
        publish();
      }

      function publish() {
        var d = derive(state);
        root.dataset.svState = JSON.stringify({
          matchedCount: d.matchedCount,
          complete: d.complete,
          mistakes: state.mistakes,
          attempts: state.attempts,
          accuracy: d.accuracy === null ? null : Math.round(d.accuracy * 100) / 100,
          selectedEntity: state.selectedEntity,
          entityProgress: d.entityProgress,
          lastResult: state.lastResult
        });
      }

      elReset.addEventListener('click', function () {
        if (shakeTimer) clearTimeout(shakeTimer);
        shakeId = null;
        justMatched = null;
        state = apply(state, { t: 'reset' });
        render();
        elReset.focus();
      });

      function fit() {
        var w = root.clientWidth || wrap.clientWidth || 900;
        wrap.classList.toggle('narrow', w < 620);
      }
      if (typeof ResizeObserver !== 'undefined') {
        var ro = new ResizeObserver(fit);
        ro.observe(root);
      } else {
        window.addEventListener('resize', fit);
      }
      fit();
      render();
    }
  };
})();