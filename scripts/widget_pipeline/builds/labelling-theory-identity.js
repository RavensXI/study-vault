/* labelling-theory-identity — a label as a chain of stages, each one doing work. */
(function () {
  'use strict';

  /* Every round hands the student a chain that has already run part-way and
     asks for the NEXT link. One option in every round is the misconception
     itself: nothing follows, it is only a name. Cases alternate between the
     crime lesson (Becker) and the schools lesson (teacher expectations). */
  var ROUNDS = [
    {
      id: 'kai-1', world: 'Crime and deviance', tag: 'crime',
      chain: [
        { tag: 'Label applied', t: 'Kai, 15, is caught with a stolen bike. The police give him a caution.' }
      ],
      ask: 'What does the caution change next?',
      answerTag: 'Others react',
      answerName: 'the reaction stage',
      why: 'Becker argued that an act does not make someone deviant on its own — the reaction to it does. So the first thing a label moves is other people’s behaviour.',
      opts: [
        { t: 'Kai and his friends are put off offending by the caution.',
          note: 'That is deterrence, the argument that punishment frightens people off. Labelling theory asks a different question: what the caution does to how everyone now sees Kai.' },
        { t: 'Nothing — a caution is only a record on a file.', nothing: true,
          note: 'That is the picture labelling theory exists to argue against. From this point on, people act on the label.' },
        { t: 'People who know start treating him as the boy who steals.', right: true },
        { t: 'Kai joins a group of offenders and steals regularly.',
          note: 'That is the far end of the chain, not the next link. Becker called it a deviant career, and several stages come before it.' }
      ]
    },
    {
      id: 'amira-1', world: 'In school', tag: 'school',
      chain: [
        { tag: 'Label applied', t: 'In September, Miss Doyle decides Amira is not a top-set pupil and puts her in set 4.' },
        { tag: 'Others react', t: 'Set 4 get shorter tasks, easier texts and fewer demanding questions.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Doors close',
      answerName: 'the doors-closing stage',
      why: 'Setting turns a September judgement into an entry decision. Easier work leads to the lower tier of paper, and the highest grades go with it.',
      opts: [
        { t: 'Nothing — a set is only a way of organising the timetable.', nothing: true,
          note: 'A set decides what a pupil is taught and which paper they sit, so it is never only administration.' },
        { t: 'She is put in for the foundation paper, where the top grades cannot be awarded.', right: true },
        { t: 'Amira decides she is no good at the subject and gives up.',
          note: 'That comes later, once the label has been on her a while. Something more practical closes first.' },
        { t: 'Amira works harder to prove Miss Doyle wrong and moves up.',
          note: 'That does happen — Fuller found pupils who reject a label and work to disprove it. But it needs the doors to stay open, and one has already shut.' }
      ]
    },
    {
      id: 'kai-2', world: 'Crime and deviance', tag: 'crime',
      chain: [
        { tag: 'Others react', t: 'Kai’s caution is known at school and on his estate. Shopkeepers watch him and a teacher moves his seat.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Master status',
      answerName: 'master status',
      why: 'Becker called this a master status: the label outranks everything else about a person. Kai is still a brother, a goalkeeper and a student, but those come second now.',
      opts: [
        { t: 'Kai stops applying for jobs because nobody will take him.',
          note: 'The closed doors do come, but something has to change in how Kai is seen first — that is why they close.' },
        { t: 'The word “thief” now comes before everything else about him.', right: true },
        { t: 'Nothing more — people will have forgotten it by next term.', nothing: true,
          note: 'A label is not a rumour that fades. Once it is attached in public it becomes the thing Kai is known for.' },
        { t: 'Kai is taken to court and convicted of the theft.',
          note: 'Labelling theory is not following the legal process here. It follows what the label does to Kai’s standing with the people around him.' }
      ]
    },
    {
      id: 'jordan-1', world: 'In school', tag: 'school',
      chain: [
        { tag: 'Label applied', t: 'Two weeks in, Mr Ellis has Jordan down as one of the bright ones, though his primary scores were ordinary.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Others react',
      answerName: 'the reaction stage',
      why: 'Rosenthal and Jacobson told teachers that pupils picked at random would make sudden progress, and those pupils gained more. The expectation was not magic — it travelled through attention, harder questions and patience.',
      opts: [
        { t: 'Mr Ellis asks Jordan harder questions and waits longer for his answers.', right: true },
        { t: 'The rest of the class are marked down to make room at the top.',
          note: 'Labelling is not a quota. Nothing is taken from anyone else — what changes is how one pupil is taught.' },
        { t: 'Jordan’s marks go up.',
          note: 'They may, but not on their own. An expectation can only reach a pupil through what the teacher actually does.' },
        { t: 'Nothing — Jordan will do as well as his real ability allows.', nothing: true,
          note: 'That assumes ability is only measured, never built. Rosenthal and Jacobson found a false expectation still changed results.' }
      ]
    },
    {
      id: 'kai-3', world: 'Crime and deviance', tag: 'crime',
      chain: [
        { tag: 'Master status', t: 'The word “thief” now comes before everything else people know about Kai.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Doors close',
      answerName: 'the doors-closing stage',
      why: 'Becker argued that the label takes the ordinary opportunities away first. Shut out of the usual routes, a person is left with the routes the label allows.',
      opts: [
        { t: 'Nothing — he can still do everything he did before.', nothing: true,
          note: 'He can, but he is no longer allowed to. Other people hold most of the routes, and they are acting on the label.' },
        { t: 'Kai starts offending regularly with others who share the label.',
          note: 'That is where this ends, but not yet. He has to lose the ordinary options before the deviant ones look like the only ones left.' },
        { t: 'The police return the bike and cancel the caution.',
          note: 'Labelling theory is about what happens once a label sticks, not about undoing it.' },
        { t: 'His Saturday job and his football club drop him.', right: true }
      ]
    },
    {
      id: 'amira-2', world: 'In school', tag: 'school',
      chain: [
        { tag: 'Doors close', t: 'Amira has spent a year in set 4 on easier work, entered for the foundation paper.' },
        { tag: 'Master status', t: 'Around school she is now known simply as one of the bottom set.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Taken on',
      answerName: 'the pupil taking the label on',
      why: 'This is the step students miss. The label has to reach the pupil’s own view of herself before it can change what she does.',
      opts: [
        { t: 'Amira is moved up to set 2 at Christmas.',
          note: 'Movement between sets is possible on paper. In practice the easier work she has been given makes moving up harder, not easier.' },
        { t: 'Nothing — she will still be marked on what she can actually do.', nothing: true,
          note: 'She will, and that is the trap: by then what she can do has been changed by a year of easier work.' },
        { t: 'Amira comes to see herself as no good at this and stops trying.', right: true },
        { t: 'Her grades come out low and the school treats that as proof.',
          note: 'That is the last link and it is coming. But a label only changes results once the pupil has taken it on.' }
      ]
    },
    {
      id: 'kai-4', world: 'Crime and deviance', tag: 'crime',
      chain: [
        { tag: 'Doors close', t: 'The job and the club have dropped Kai. The people who will still have him carry the same label.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Deviant career',
      answerName: 'a deviant career',
      why: 'Lemert called this secondary deviance: offending produced by the reaction, not by whatever caused the first act. On this account the caution has done more to make Kai an offender than the theft did.',
      opts: [
        { t: 'He settles into that group and offending becomes routine.', right: true },
        { t: 'Nothing — he is the same person he was before the caution.', nothing: true,
          note: 'He is, and the theory agrees. What has changed is everyone around him, and that is enough to change what he does.' },
        { t: 'He is arrested again for the original bike theft.',
          note: 'A second arrest for the same act is not what the theory predicts. It predicts new offending, produced by the reaction to the first.' },
        { t: 'The label wears off once he leaves school.',
          note: 'That would be true if a label were only a name. Becker argued it works like a career, where each stage makes the next one more likely.' }
      ]
    },
    {
      id: 'jordan-2', world: 'In school', tag: 'school',
      chain: [
        { tag: 'Others react', t: 'Mr Ellis gives Jordan harder questions, more time to answer and a place in the extension group.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Taken on',
      answerName: 'the pupil taking the label on',
      why: 'The chain runs the same way upwards as downwards. A positive label reaches the pupil through how he is treated, and he takes it on as part of who he is.',
      opts: [
        { t: 'Jordan finishes the year with the best results in the class.',
          note: 'That is the end of the chain, not the next link. The pupil has to take the label on first; the results follow from that.' },
        { t: 'Mr Ellis notices his mistake and moves Jordan back.',
          note: 'Labels are rarely tested against the evidence. Once a teacher has typed a pupil, later work tends to be read as fitting the type.' },
        { t: 'Nothing — extra questions do not change what a pupil can do.', nothing: true,
          note: 'They change what he practises and what he thinks he is for, and both of those change what he can do.' },
        { t: 'Jordan starts to think of himself as good at this and takes risks.', right: true }
      ]
    },
    {
      id: 'amira-3', world: 'In school', tag: 'school',
      chain: [
        { tag: 'Taken on', t: 'Amira now says she is just no good at it, and she has stopped trying in lessons.' }
      ],
      ask: 'What does the label change next?',
      answerTag: 'Prophecy confirmed',
      answerName: 'the prophecy confirming itself',
      why: 'This is the self-fulfilling prophecy closing. A prediction that was not true when it was made has been made true by the way people acted on it.',
      opts: [
        { t: 'Nothing — her results will show what she was capable of all along.', nothing: true,
          note: 'They will show what she can do now, after a year of being taught as a bottom-set pupil. That is not the same thing.' },
        { t: 'The school apologises and has her paper re-marked.',
          note: 'Nobody in the chain thinks a mistake has been made. That is the point — the result is read as proof.' },
        { t: 'Her results come out low, and the first judgement looks correct.', right: true },
        { t: 'Miss Doyle is shown to have been wrong about Amira.',
          note: 'The opposite happens. The low result is treated as evidence that Miss Doyle judged well, so the next pupil gets the same treatment.' }
      ]
    }
  ];

  var OPEN_CAP = 'The stages run in order, and each one sets up the next.';

  var MASTERY = 'Three in a row — you have it. A label does not sit still: others act on it, doors close, it becomes the first thing anyone sees, and the person takes it on — so the result ends up matching the label. Becker argued that the reaction, not the act, makes the career. It is not automatic, though: some labels never stick, and some people reject them.';

  var CSS = [
    '.svw-lbi{font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;-webkit-font-smoothing:antialiased}',
    '.svw-lbi *{box-sizing:border-box}',
    '.svw-lbi .lbi-kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--lbi-accent)}',
    '.svw-lbi .lbi-title{margin:.14rem 0 0;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.14rem;line-height:1.24}',
    '.svw-lbi .lbi-frame{margin:.3rem 0 .55rem;font-size:.8rem;line-height:1.45;color:#5b564e}',
    '.svw-lbi .lbi-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.58rem .62rem .5rem}',
    '.svw-lbi .lbi-world{display:inline-block;margin:0 0 .38rem;padding:.14rem .42rem;font-size:.66rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--lbi-accent);background:var(--lbi-tint);border-radius:6px}',
    '.svw-lbi .lbi-chain{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.3rem}',
    '.svw-lbi .lbi-rung{position:relative;padding-left:1.05rem}',
    '.svw-lbi .lbi-rung[hidden]{display:none}',
    '.svw-lbi .lbi-rung::before{content:"";position:absolute;left:.1rem;top:.28rem;width:7px;height:7px;border-radius:50%;background:#b8b1a5}',
    '.svw-lbi .lbi-rung::after{content:"";position:absolute;left:.29rem;top:.62rem;bottom:-.34rem;width:0;border-left:1px solid #d5cec2}',
    '.svw-lbi .lbi-rung.is-end::after{display:none}',
    '.svw-lbi .lbi-rung.is-open::after{border-left-style:dashed;bottom:-.9rem}',
    '.svw-lbi .lbi-rung.is-new::before{background:var(--lbi-accent)}',
    '.svw-lbi .lbi-rung.is-new .lbi-tag{color:var(--lbi-accent)}',
    '.svw-lbi .lbi-tag{display:block;font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;line-height:1.25;color:#8d8880}',
    '.svw-lbi .lbi-txt{display:block;font-size:.78rem;line-height:1.4;color:#2d2a26}',
    '.svw-lbi .lbi-ask{margin:.45rem 0 0;font-size:.8rem;font-weight:600;line-height:1.4}',
    '.svw-lbi .lbi-ask[hidden]{display:none}',
    '.svw-lbi .lbi-opts{display:flex;flex-direction:column;gap:.26rem;margin-top:.5rem}',
    '.svw-lbi .lbi-opt{display:block;width:100%;padding:.4rem .55rem;text-align:left;font:inherit;font-size:.78rem;line-height:1.34;font-weight:500;color:#2d2a26;background:#fff;border:1px solid #e0d9cd;border-radius:9px;cursor:pointer}',
    '.svw-lbi .lbi-opt[hidden]{display:none}',
    '.svw-lbi .lbi-opt.is-picked{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-lbi .lbi-opt.is-you{background:#f1ece4;border-color:#b8b1a5;color:#2d2a26;cursor:default}',
    '.svw-lbi .lbi-oy{display:block;margin-top:.16rem;font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880}',
    '.svw-lbi .lbi-oy[hidden]{display:none}',
    '.svw-lbi .lbi-bar{display:flex;align-items:center;gap:.6rem;margin-top:.55rem}',
    '.svw-lbi .lbi-run{flex:1;min-width:0;margin:0;font-size:.72rem;line-height:1.3;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-lbi .lbi-go{flex:none;font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-lbi .lbi-go.is-live{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-lbi .lbi-go[disabled]{opacity:.5;cursor:default}',
    '.svw-lbi .lbi-cap{margin:.45rem 0 0;font-size:.8rem;line-height:1.45;color:#2d2a26;min-height:3.2em}',
    '.svw-lbi .lbi-cap b{font-weight:600}',
    '.svw-lbi .lbi-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-lbi .lbi-opt:focus-visible,.svw-lbi .lbi-go:focus-visible{outline:2px solid var(--lbi-accent);outline-offset:2px}',
    '.svw-lbi.lbi-motion .lbi-opt,.svw-lbi.lbi-motion .lbi-go{transition:background-color .12s ease,border-color .12s ease,color .12s ease}'
  ].join('\n');

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'labelling-theory-identity',
      title: 'What the label does next',
      teaches: 'A label is a self-reinforcing chain — reaction, closed doors, master status, self-fulfilling prophecy — not a passive description.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#7a6a52';
      var reduced = !!ctx.reducedMotion;

      root.classList.add('svw-lbi');
      if (!reduced) root.classList.add('lbi-motion');
      root.style.setProperty('--lbi-accent', accent);
      root.style.setProperty('--lbi-tint', accent + '22');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      root.appendChild(el('p', 'lbi-kick', 'Labelling theory'));
      root.appendChild(el('h3', 'lbi-title', 'What the label does next'));
      root.appendChild(el('p', 'lbi-frame',
        'A label does not stop working at the moment it is given. Each case picks up part-way through the process — decide what the label changes next.'));

      var stage = el('div', 'lbi-stage');
      var world = el('p', 'lbi-world', '');
      stage.appendChild(world);

      /* three rung slots: two of given history, one for the answer */
      var chain = el('ol', 'lbi-chain');
      var rungs = [];
      for (var r = 0; r < 3; r++) {
        var li = el('li', 'lbi-rung');
        var tg = el('span', 'lbi-tag', '');
        var tx = el('span', 'lbi-txt', '');
        li.appendChild(tg);
        li.appendChild(tx);
        li.hidden = true;
        chain.appendChild(li);
        rungs.push({ li: li, tag: tg, txt: tx });
      }
      stage.appendChild(chain);

      var ask = el('p', 'lbi-ask', '');
      stage.appendChild(ask);

      var optsWrap = el('div', 'lbi-opts');
      var opts = [];
      for (var i = 0; i < 4; i++) {
        (function (idx) {
          var b = el('button', 'lbi-opt');
          b.type = 'button';
          var t = el('span', 'lbi-ot', '');
          var y = el('span', 'lbi-oy', 'Your answer');
          y.hidden = true;
          b.appendChild(t);
          b.appendChild(y);
          b.addEventListener('click', function () { pick(idx); });
          optsWrap.appendChild(b);
          opts.push({ btn: b, txt: t, you: y });
        }(i));
      }
      stage.appendChild(optsWrap);
      root.appendChild(stage);

      var bar = el('div', 'lbi-bar');
      var run = el('p', 'lbi-run', '');
      var go = el('button', 'lbi-go', 'Check');
      go.type = 'button';
      bar.appendChild(run);
      bar.appendChild(go);
      root.appendChild(bar);

      var cap = el('p', 'lbi-cap', OPEN_CAP);
      root.appendChild(cap);

      var sr = el('p', 'lbi-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---- state ---- */
      var seat = 0;
      var current = ROUNDS[0];
      var rightIdx = 0;
      var picked = null;
      var revealed = false;
      var streak = 0;
      var attempted = 0;
      var mastered = false;

      function answerIndex(round) {
        for (var k = 0; k < round.opts.length; k++) {
          if (round.opts[k].right) return k;
        }
        return 0;
      }

      function sync(extra) {
        var s = {
          streak: streak, mastered: mastered, attempted: attempted,
          round: current.id, world: current.tag, stage: current.answerTag
        };
        if (extra) {
          Object.keys(extra).forEach(function (k) { s[k] = extra[k]; });
        }
        root.dataset.svState = JSON.stringify(s);
      }

      function renderRound() {
        rightIdx = answerIndex(current);
        world.textContent = current.world;

        var given = current.chain.length;
        for (var k = 0; k < rungs.length; k++) {
          var slot = rungs[k];
          slot.li.classList.remove('is-new', 'is-open', 'is-end', 'is-mid');
          if (k < given) {
            slot.li.hidden = false;
            slot.tag.textContent = current.chain[k].tag;
            slot.txt.textContent = current.chain[k].t;
            slot.li.classList.add(k === given - 1 ? 'is-open' : 'is-mid');
          } else {
            slot.li.hidden = true;
            slot.tag.textContent = '';
            slot.txt.textContent = '';
          }
        }

        ask.hidden = false;
        ask.textContent = current.ask;

        for (var j = 0; j < opts.length; j++) {
          var o = opts[j];
          o.txt.textContent = current.opts[j].t;
          o.btn.hidden = false;
          o.btn.disabled = false;
          o.btn.classList.remove('is-picked', 'is-you');
          o.you.hidden = true;
        }

        picked = null;
        revealed = false;
        go.textContent = 'Check';
        go.disabled = true;
        go.classList.remove('is-live');
        cap.textContent = OPEN_CAP;
        sync({ picked: null });
      }

      function pick(idx) {
        if (revealed) return;
        picked = idx;
        for (var j = 0; j < opts.length; j++) {
          opts[j].btn.classList.toggle('is-picked', j === idx);
        }
        go.disabled = false;
        go.classList.add('is-live');
        sr.textContent = current.opts[idx].t + ' chosen. Press Check.';
        sync({ picked: idx });
      }

      function clearPick() {
        if (revealed || picked === null) return;
        var was = picked;
        picked = null;
        for (var j = 0; j < opts.length; j++) {
          opts[j].btn.classList.remove('is-picked');
        }
        /* Check is about to go dead - do not leave focus stranded on it */
        if (document.activeElement === go) opts[was].btn.focus();
        go.disabled = true;
        go.classList.remove('is-live');
        sr.textContent = 'Choice cleared.';
        sync({ picked: null });
      }

      function commit() {
        var right = current.opts[rightIdx];
        var chose = current.opts[picked];
        var correct = picked === rightIdx;

        attempted += 1;
        streak = correct ? streak + 1 : 0;
        var justMastered = false;
        if (correct && streak >= 3 && !mastered) { mastered = true; justMastered = true; }
        revealed = true;

        /* the chain grows by the real next link */
        var given = current.chain.length;
        rungs[given - 1].li.classList.remove('is-open');
        var tail = rungs[given];
        tail.li.hidden = false;
        tail.li.classList.add('is-new', 'is-end');
        tail.tag.textContent = current.answerTag;
        tail.txt.textContent = right.t;

        ask.hidden = true;
        for (var j = 0; j < opts.length; j++) {
          var o = opts[j];
          o.btn.disabled = true;
          o.btn.classList.remove('is-picked');
          if (!correct && j === picked) {
            o.btn.hidden = false;
            o.btn.classList.add('is-you');
            o.you.hidden = false;
          } else {
            o.btn.hidden = true;
          }
        }

        var body;
        if (correct && justMastered) {
          body = '<b>Right — “' + chose.t + '”</b> That is ' + current.answerName + '. ' + MASTERY;
        } else if (correct) {
          body = '<b>Right — “' + chose.t + '”</b> That is ' + current.answerName + '. ' + current.why;
        } else {
          body = '<b>Not quite — you said “' + chose.t + '”</b> ' + chose.note +
                 ' Next comes ' + current.answerName + '. ' + right.t;
        }
        cap.innerHTML = body;
        sr.textContent = cap.textContent;

        if (mastered) {
          run.textContent = correct ? 'You have it. Keep going if you like.'
                                    : 'That one slipped. Worth another.';
          go.textContent = 'Another anyway';
        } else if (streak === 0) {
          run.textContent = 'Back to zero. Three in a row ends it.';
          go.textContent = 'Next case';
        } else if (streak === 1) {
          run.textContent = '1 right — two more to go.';
          go.textContent = 'Next case';
        } else {
          run.textContent = '2 right in a row — one more.';
          go.textContent = 'Next case';
        }
        go.disabled = false;
        go.classList.remove('is-live');
        sync({ picked: picked, correct: correct });
      }

      go.addEventListener('click', function () {
        if (revealed) {
          seat = (seat + 1) % ROUNDS.length;
          current = ROUNDS[seat];
          renderRound();
          sr.textContent = 'New case. ' + current.chain[0].t + ' ' + current.ask;
          return;
        }
        if (picked === null) return;
        commit();
      });

      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') clearPick();
      });

      renderRound();
    }
  };
}());
