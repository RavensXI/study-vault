/* Active listening = six named behaviours.
   Self-contained. No network, no storage, no timers. */
(function () {
  'use strict';

  var BEH = {
    eye:   { label: 'Eye contact',             echo: 'eye contact' },
    open:  { label: 'Open body language',      echo: 'open body language' },
    nod:   { label: 'Nodding and encouraging', echo: 'nodding and encouraging' },
    para:  { label: 'Paraphrasing back',       echo: 'paraphrasing back' },
    ask:   { label: 'Clarifying question',     echo: 'a clarifying question' },
    wait:  { label: 'Not interrupting',        echo: 'not interrupting' },
    quiet: { label: 'Just listening quietly',  echo: 'just listening quietly' }
  };

  function opt(key, why) {
    return { key: key, label: BEH[key].label, echo: BEH[key].echo, why: why };
  }

  var MASTERY = 'Three in a row — you have it. Six behaviours, three jobs: eye contact and ' +
    'open body language show attention; nodding and not interrupting keep them talking; ' +
    'paraphrasing and clarifying questions check you have understood.';

  var ROUNDS = [
    {
      id: 'doyle-para',
      set: 'Residential home. Priya, a support worker, is with Mr Doyle, a resident.',
      ask: 'Which active-listening behaviour is Priya using in her reply?',
      turns: [
        { who: 'Mr Doyle', text: 'They’ve moved my tablets to eight. Nobody asked me. I’ve taken them at six for twelve years.',
          note: 'Two things: the change, and not being asked.' },
        { who: 'Priya', text: 'So it’s the timing that has thrown you — and that nobody checked with you first.',
          note: 'His meaning, her words — handed back for checking.' }
      ],
      answer: 'para',
      right: 'Priya gives Mr Doyle’s meaning back in her own words, so he can correct her if she has it wrong. It checks understanding and asks for nothing new.',
      options: [
        opt('para', ''),
        opt('ask', 'A clarifying question asks for something she has not got. Priya adds nothing new — she hands his own point back to be checked. That is paraphrasing back.'),
        opt('nod', 'Nodding keeps him going without taking a turn. Priya took a turn and restated his point: paraphrasing back.'),
        opt('wait', 'She did wait, but the question is what her reply does — it says his meaning back for checking. Paraphrasing back.'),
        opt('quiet', 'Quiet attention sends nothing back. Mr Doyle only knows his point landed because Priya restated it: paraphrasing back.')
      ]
    },
    {
      id: 'nursery-ask',
      set: 'Nursery. Sam, a nursery worker, is speaking with a parent at collection time.',
      ask: 'Which active-listening behaviour is Sam using in his reply?',
      turns: [
        { who: 'Parent', text: 'He’s been out of sorts all week. He didn’t want to come in this morning, and that’s not like him.',
          note: 'Vague — it could be sleep, illness or upset.' },
        { who: 'Sam', text: 'When you say out of sorts — is that mainly the mornings, or at home in the evenings too?',
          note: 'Asks for the detail rather than assuming.' }
      ],
      answer: 'ask',
      right: 'Out of sorts could mean anything, so Sam asks for the detail instead of guessing. It gets him something the parent has not yet said.',
      options: [
        opt('ask', ''),
        opt('para', 'A paraphrase adds nothing new. Sam’s reply asks for what he has not got — which mornings, which evenings: a clarifying question.'),
        opt('nod', 'Nodding is a signal without words. Sam takes a turn and asks for missing detail: a clarifying question.'),
        opt('eye', 'Eye contact is what his face does, not what his words do. His words ask for detail he was never given: a clarifying question.'),
        opt('quiet', 'Quiet attention would leave Sam acting on out of sorts and guessing which it is. He asks instead: a clarifying question.')
      ]
    },
    {
      id: 'ade-wait',
      set: 'Day centre. Ade has had a stroke and needs longer to find his words.',
      ask: 'This exchange goes wrong. Which active-listening behaviour is missing?',
      turns: [
        { who: 'Ade', text: 'I wanted to ask about the… the trip, the one on…',
          note: 'Searching for a word. Not finished.' },
        { who: 'Worker', text: 'The Thursday trip? To the garden centre? I’ll put you down for it.',
          note: 'She fills the gap and answers a question he never asked.' },
        { who: 'Ade', text: '…No. Never mind.',
          note: 'He withdraws. The point is lost.' }
      ],
      answer: 'wait',
      right: 'Finishing Ade’s sentence took the words out of his mouth, and he gave up on his own question. Waiting through a pause is work, and it protects his dignity.',
      options: [
        opt('wait', ''),
        opt('para', 'There was nothing to paraphrase — Ade never reached the end of his sentence. What was missing was the wait: not interrupting.'),
        opt('ask', 'She did ask, twice — but over him, before he had finished. The missing behaviour is not interrupting.'),
        opt('nod', 'A nod would have helped, but the harm here was done by speech, not by silence. The missing behaviour is not interrupting.'),
        opt('quiet', 'That is the opposite of what happened — the worker spoke over him. Named properly, the behaviour she skipped is not interrupting.')
      ]
    },
    {
      id: 'clinic-nod',
      set: 'Health centre. A health care assistant is with a woman who is anxious about a procedure.',
      ask: 'This exchange goes wrong. Which active-listening behaviour is missing?',
      turns: [
        { dir: true, text: 'The assistant faces her, holds eye contact and does not interrupt. Her face does not move and she makes no sound.',
          note: 'Attending — but sending nothing back.' },
        { who: 'Woman', text: 'I’ve been worrying since the letter came. My sister had the same thing done and she said—',
          note: 'She is starting to disclose.' },
        { who: 'Woman', text: '…Anyway. It doesn’t matter.',
          note: 'Nothing came back, so she stops.' }
      ],
      answer: 'nod',
      right: 'The assistant was attending, but the woman got nothing back — no nod, no mm hm. A blank face reads as disinterest, so the disclosure closed down.',
      options: [
        opt('nod', ''),
        opt('eye', 'She held it the whole time. What she never gave was a nod or an mm: nodding and encouraging.'),
        opt('wait', 'She never interrupted — that was the trouble. She gave nothing at all. The missing behaviour is nodding and encouraging.'),
        opt('open', 'She was turned towards the woman throughout. What was missing was the running signal that says keep going: nodding and encouraging.'),
        opt('quiet', 'That is exactly what she did, and the woman stopped anyway. Attention with no outward signal reads as absence. What was missing is nodding and encouraging.')
      ]
    },
    {
      id: 'lounge-open',
      set: 'Residential home. A resident comes over to the manager on duty.',
      ask: 'Which active-listening behaviour is the manager using?',
      turns: [
        { who: 'Resident', text: 'Have you got a minute? It’s about the laundry again.',
          note: 'He is testing whether now is a good time.' },
        { dir: true, text: 'The manager puts down her clipboard, turns her chair to face him and uncrosses her arms.',
          note: 'Clipboard down, chair turned, arms open.' }
      ],
      answer: 'open',
      right: 'Turning towards him with the clipboard down and her arms uncrossed says you have my time. It is the signal that makes it safe to start.',
      options: [
        opt('open', ''),
        opt('eye', 'That is what her eyes do. Here the whole signal is the body — turned towards him, arms uncrossed: open body language.'),
        opt('nod', 'Nodding keeps a speaker going once they have started. He has barely begun. What she gave him is open body language.'),
        opt('wait', 'She has had no chance to interrupt yet. She answered him with her posture: open body language.'),
        opt('quiet', 'Quiet is not something he can see. He can see the clipboard go down and the chair turn: open body language.')
      ]
    },
    {
      id: 'tenant-paraphrase',
      set: 'Supported living. A tenant tells his key worker why he has stopped going to the Tuesday group.',
      ask: 'Which reply is a paraphrase of what he has just said?',
      long: true,
      turns: [
        { who: 'Tenant', text: 'It’s not the group. It’s getting there. Two buses, and if the first one is late I walk in halfway through and everyone looks up.',
          note: 'Two reasons: the journey, and being watched walking in.' }
      ],
      answer: 'p1',
      right: 'His meaning, in her words, with nothing added. He can now hear whether she has understood, and put her right if she has not.',
      options: [
        { key: 'p1', label: '“So it’s the journey putting you off — two buses, then walking in late.”',
          echo: 'the reply about the journey', why: '' },
        { key: 'p2', label: '“Have you thought about the community minibus? I can book you a seat.”',
          echo: 'the minibus offer', why: 'That is a solution, and it arrives before she has shown she understood the problem. A paraphrase adds nothing: so it is the journey putting you off.' },
        { key: 'p3', label: '“The buses round here are dreadful. I waited forty minutes on Monday.”',
          echo: 'the reply about her own bus wait', why: 'That moves the subject to her. A paraphrase keeps it his: so it is the journey putting you off.' },
        { key: 'p4', label: '“Sorry, hang on — did you sign the trip form before you go on?”',
          echo: 'the question about the trip form', why: 'That cuts across him mid-point. It is an interruption, not a paraphrase. The paraphrase is: so it is the journey putting you off.' }
      ]
    },
    {
      id: 'fall-eye',
      set: 'Care home. Mrs Herron is telling a worker about a fall she had in the night.',
      ask: 'Which active-listening behaviour is the worker using?',
      turns: [
        { who: 'Mrs Herron', text: 'I got up for the bathroom and the next thing I knew I was on the floor by the wardrobe.',
          note: 'A fall in the night — this matters to her.' },
        { dir: true, text: 'The worker keeps her eyes on Mrs Herron. The call buzzer sounds down the corridor and she does not look up.',
          note: 'The gaze holds through the buzzer.' }
      ],
      answer: 'eye',
      right: 'Not looking away when the buzzer goes tells Mrs Herron she has the worker’s whole attention. A glance at the door would have ended the story.',
      options: [
        opt('eye', ''),
        opt('open', 'That is posture — how she is turned and held. Here the whole signal is the gaze she keeps when the buzzer goes: eye contact.'),
        opt('nod', 'Nothing here moves and nothing makes a sound. What she holds is her gaze: eye contact.'),
        opt('wait', 'True, but she is doing something visible rather than only refraining. She holds her gaze through the buzzer: eye contact.'),
        opt('quiet', 'Quiet on its own is invisible. Mrs Herron can see one thing: that the worker’s eyes have not left her. Eye contact.')
      ]
    },
    {
      id: 'collection-para',
      set: 'Nursery. A parent changes the collection arrangements at the door.',
      ask: 'This exchange goes wrong. Which active-listening behaviour is missing?',
      turns: [
        { who: 'Parent', text: 'My mum’s getting him Thursday and Friday — no, sorry, Thursday. Friday I’ll come, but later, about half four.',
          note: 'She corrects herself mid-sentence.' },
        { who: 'Worker', text: 'No problem, I’ll note it down.',
          note: 'Agreement, not a check.' },
        { dir: true, text: 'She writes: Grandma — Thursday and Friday.',
          note: 'The correction is lost.' }
      ],
      answer: 'para',
      right: 'Saying it back — Grandma Thursday, you on Friday at about half four — would have caught the correction the parent made mid-sentence. That is what paraphrasing is for.',
      options: [
        opt('para', ''),
        opt('ask', 'Nothing was left out: the parent gave it all and corrected herself. It needed saying back, not asking again — paraphrasing back.'),
        opt('nod', 'The worker did respond, with no problem. What she never did was check she had it right: paraphrasing back.'),
        opt('eye', 'Even with perfect eye contact she would still have written the wrong day. Only saying it back catches that: paraphrasing back.'),
        opt('quiet', 'She was quiet and she was attentive, and she still got it wrong. Attention is not the same as checking: paraphrasing back.')
      ]
    }
  ];

  var CSS =
  '.svw-alb{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;' +
    '-webkit-text-size-adjust:100%}' +
  '.svw-alb *{box-sizing:border-box}' +
  '.svw-alb .alb-kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
    'text-transform:uppercase;color:var(--alb-accent,#8a6a4f)}' +
  '.svw-alb .alb-title{margin:.18rem 0 0;font-family:"Source Serif 4",Georgia,serif;' +
    'font-weight:600;font-size:1.2rem;line-height:1.2}' +
  '.svw-alb .alb-frame{margin:.5rem 0 0;font-size:.85rem;line-height:1.45;font-weight:500}' +
  '.svw-alb .alb-set{color:#8d8880;font-weight:400}' +
  '.svw-alb .alb-panel{margin:.65rem 0 0;background:#faf8f5;border:1px solid #efe9e0;' +
    'border-radius:12px;padding:.65rem .75rem}' +
  '.svw-alb .alb-turn{margin:0}' +
  '.svw-alb .alb-turn + .alb-turn{margin-top:.45rem}' +
  '.svw-alb .alb-line{margin:0;font-size:.84rem;line-height:1.4}' +
  '.svw-alb .alb-who{font-weight:700;color:var(--alb-accent,#8a6a4f)}' +
  '.svw-alb .alb-dir{margin:0;font-size:.8rem;line-height:1.4;font-style:italic;color:#5b564e}' +
  '.svw-alb .alb-note{margin:.16rem 0 0;font-size:.73rem;line-height:1.35;color:#8d8880;display:none}' +
  '.svw-alb.is-done .alb-note{display:block}' +
  '.svw-alb .alb-opts{margin:.7rem 0 0;display:grid;gap:.4rem;' +
    'grid-template-columns:repeat(auto-fit,minmax(146px,1fr))}' +
  '.svw-alb .alb-opts.is-long{grid-template-columns:1fr}' +
  '.svw-alb .alb-opt{font:inherit;font-size:.82rem;font-weight:600;line-height:1.3;text-align:left;' +
    'padding:.5rem .6rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;' +
    'color:#2d2a26;cursor:pointer;display:block;width:100%}' +
  '.svw-alb .alb-opts.is-long .alb-opt{font-weight:500}' +
  '.svw-alb .alb-opt.is-picked{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
  '.svw-alb .alb-opt.is-answer{background:rgba(79,125,99,.10);border-color:#4f7d63;color:#2d2a26}' +
  '.svw-alb .alb-opt[disabled]{cursor:default}' +
  '.svw-alb .alb-opt.is-hidden{display:none}' +
  '.svw-alb .alb-tag{display:block;margin-top:.2rem;font-size:.68rem;font-weight:700;' +
    'letter-spacing:.07em;text-transform:uppercase;color:#8d8880}' +
  '.svw-alb .alb-opt.is-answer .alb-tag{color:#4f7d63}' +
  '.svw-alb .alb-opt.is-picked .alb-tag{color:#cfc8bd}' +
  '.svw-alb .alb-bar{margin:.7rem 0 0;display:flex;align-items:center;justify-content:space-between;gap:.6rem}' +
  '.svw-alb .alb-run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums}' +
  '.svw-alb .alb-go{font:inherit;font-size:.84rem;font-weight:600;padding:.55rem 1.05rem;' +
    'border:1px solid #2d2a26;border-radius:10px;background:#2d2a26;color:#fff;cursor:pointer;' +
    'white-space:nowrap;flex:none}' +
  '.svw-alb .alb-go[disabled]{background:#efe9e0;border-color:#e0d9cd;color:#a9a29a;cursor:default}' +
  '.svw-alb .alb-cap{margin:.6rem 0 0;font-size:.84rem;line-height:1.5;display:none}' +
  '.svw-alb.is-done .alb-cap{display:block}' +
  '.svw-alb .alb-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
    'clip-path:inset(50%);white-space:nowrap}';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  window.SVWidget = {
    meta: {
      id: 'active-listening-behaviours',
      title: 'Name the behaviour',
      teaches: 'Active listening is six distinct, nameable behaviours, each doing a different job for the speaker.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

      var wrap = el('div', 'svw-alb');
      wrap.style.setProperty('--alb-accent', accent);
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      wrap.appendChild(el('p', 'alb-kick', 'Active listening'));
      wrap.appendChild(el('h3', 'alb-title', 'Name the behaviour'));

      var frame = el('p', 'alb-frame');
      var setSpan = el('span', 'alb-set');
      var askSpan = el('span');
      frame.appendChild(setSpan);
      frame.appendChild(document.createTextNode(' '));
      frame.appendChild(askSpan);
      wrap.appendChild(frame);

      /* transcript: three fixed slots, built once, hidden when unused */
      var panel = el('div', 'alb-panel');
      var slots = [];
      for (var s = 0; s < 3; s++) {
        var turn = el('div', 'alb-turn');
        var line = el('p', 'alb-line');
        var who = el('span', 'alb-who');
        var said = el('span');
        line.appendChild(who);
        line.appendChild(document.createTextNode(' '));
        line.appendChild(said);
        var dir = el('p', 'alb-dir');
        var note = el('p', 'alb-note');
        turn.appendChild(line);
        turn.appendChild(dir);
        turn.appendChild(note);
        panel.appendChild(turn);
        slots.push({ turn: turn, line: line, who: who, said: said, dir: dir, note: note });
      }
      wrap.appendChild(panel);

      /* five fixed option buttons */
      var opts = el('div', 'alb-opts');
      var btns = [];
      for (var b = 0; b < 5; b++) {
        var ob = el('button', 'alb-opt');
        ob.type = 'button';
        var lab = el('span');
        var tag = el('span', 'alb-tag');
        ob.appendChild(lab);
        ob.appendChild(tag);
        opts.appendChild(ob);
        btns.push({ btn: ob, lab: lab, tag: tag });
      }
      wrap.appendChild(opts);

      var bar = el('div', 'alb-bar');
      var run = el('span', 'alb-run', '');
      var go = el('button', 'alb-go', 'Check');
      go.type = 'button';
      go.disabled = true;
      bar.appendChild(run);
      bar.appendChild(go);
      wrap.appendChild(bar);

      var cap = el('p', 'alb-cap');
      wrap.appendChild(cap);

      var sr = el('p', 'alb-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var queue = shuffle(ROUNDS.slice());
      var qi = 0;
      var round = null;
      var picked = null;
      var done = false;
      var streak = 0, attempted = 0, mastered = false;

      function publish(correct) {
        root.dataset.svState = JSON.stringify({
          round: round ? round.id : null,
          choice: picked,
          answer: done && round ? round.answer : null,
          correct: typeof correct === 'boolean' ? correct : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function paintRun() {
        if (mastered) { run.textContent = 'You have it — keep going if you like.'; return; }
        if (streak === 2) { run.textContent = '2 right in a row — one more and you have it.'; return; }
        if (streak === 1) { run.textContent = '1 right in a row.'; return; }
        run.textContent = attempted ? 'Run back to zero — three in a row finishes it.' : '';
      }

      function loadRound() {
        if (qi >= queue.length) { queue = shuffle(ROUNDS.slice()); qi = 0; }
        round = queue[qi++];
        picked = null;
        done = false;
        wrap.classList.remove('is-done');

        setSpan.textContent = round.set;
        askSpan.textContent = round.ask;

        for (var i = 0; i < slots.length; i++) {
          var t = round.turns[i], sl = slots[i];
          if (!t) { sl.turn.style.display = 'none'; continue; }
          sl.turn.style.display = '';
          if (t.dir) {
            sl.line.style.display = 'none';
            sl.dir.style.display = '';
            sl.dir.textContent = t.text;
          } else {
            sl.dir.style.display = 'none';
            sl.line.style.display = '';
            sl.who.textContent = t.who + ':';
            sl.said.textContent = t.text;
          }
          sl.note.textContent = t.note || '';
          sl.note.style.display = t.note ? '' : 'none';
        }

        opts.classList.toggle('is-long', !!round.long);
        var pool = shuffle(round.options.slice());
        for (var k = 0; k < btns.length; k++) {
          var o = pool[k], ui = btns[k];
          ui.btn.className = 'alb-opt';
          ui.btn.disabled = false;
          ui.tag.textContent = '';
          ui.btn.setAttribute('aria-pressed', 'false');
          if (!o) { ui.btn.className = 'alb-opt is-hidden'; ui.key = null; continue; }
          ui.key = o.key;
          ui.lab.textContent = o.label;
        }

        go.textContent = 'Check';
        go.disabled = true;
        cap.textContent = '';
        paintRun();
        publish(null);
      }

      function pick(key) {
        if (done) return;
        picked = key;
        for (var k = 0; k < btns.length; k++) {
          var on = btns[k].key === key;
          btns[k].btn.classList.toggle('is-picked', on);
          btns[k].btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        go.disabled = false;
        publish(null);
      }

      function find(key) {
        for (var i = 0; i < round.options.length; i++) {
          if (round.options[i].key === key) return round.options[i];
        }
        return null;
      }

      function commit() {
        if (!picked) return;
        done = true;
        attempted++;
        var chosen = find(picked);
        var right = picked === round.answer;

        if (right) { streak++; if (streak >= 3) mastered = true; }
        else { streak = 0; }

        for (var k = 0; k < btns.length; k++) {
          var ui = btns[k];
          ui.btn.disabled = true;
          if (!ui.key) continue;
          if (ui.key === round.answer) {
            ui.btn.className = 'alb-opt is-answer';
            ui.tag.textContent = right ? 'your answer · the behaviour' : 'the behaviour';
          } else if (ui.key === picked) {
            ui.btn.className = 'alb-opt is-picked';
            ui.tag.textContent = 'your answer';
          } else {
            ui.btn.className = 'alb-opt is-hidden';
          }
        }

        var text = right
          ? 'Right — ' + chosen.echo + '. ' + round.right
          : 'Not quite — you said ' + chosen.echo + '. ' + chosen.why;
        if (right && streak === 3) text = 'Right — ' + chosen.echo + '. ' + MASTERY;
        cap.textContent = text;
        wrap.classList.add('is-done');
        sr.textContent = text;

        go.textContent = mastered ? 'Another anyway' : 'Next scenario';
        go.disabled = false;
        paintRun();
        publish(right);
      }

      opts.addEventListener('click', function (ev) {
        for (var k = 0; k < btns.length; k++) {
          if (btns[k].key && btns[k].btn.contains(ev.target)) { pick(btns[k].key); return; }
        }
      });

      go.addEventListener('click', function () {
        if (done) loadRound(); else commit();
      });

      loadRound();
    }
  };
})();
