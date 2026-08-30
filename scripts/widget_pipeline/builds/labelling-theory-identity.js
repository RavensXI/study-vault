/* ============================================================
   labelling-theory-identity — "The same act, twice"

   Two people commit an identical act. One is labelled, one is not.
   The student predicts, one step at a time, what happens next to ONE
   of them — and which one is asked changes from step to step. So the
   answer "nothing much changes, the act is in the past" is CORRECT for
   the unlabelled twin and WRONG for the labelled twin. The prediction
   is therefore real and variable, and the misconception is enterable
   at every single round.

   One scenario model drives the question, the chain cells, the
   feedback and the verdict, so the reveal cannot drift.
   ============================================================ */
(function () {
  'use strict';

  var ASKLINE = 'Predict what labelling theory expects next — for each of them.';

  /* ---------- the model ------------------------------------------------
     Every sequence is generated from this. correct answer is a property
     of the TRACK, not of the step: the labelled twin follows the label,
     the unlabelled twin follows nothing.                                */

  var SCENARIOS = [
    {
      id: 'homework',
      a: 'Sam', b: 'Jo',
      headA: 'Sam — put on report', headB: 'Jo — a quiet word',
      frame: 'Sam and Jo hand in the same copied homework. Sam is put on report as a cheat; Jo gets a quiet word.',
      order: ['A', 'B', 'A'],
      steps: [
        {
          ask: 'Over the next term, how do teachers treat {n}?',
          o: {
            same:  { t: 'Much as before — one piece of work, now dealt with.', e: 'teachers treat {n} much as before' },
            label: { t: 'Suspicious first — {n}’s work is checked before anyone’s.', e: '{n}’s work gets checked before anyone else’s' },
            alt:   { t: 'They give {n} extra help so it does not happen again.', e: '{n} is given extra help' }
          },
          out: { A: '{a}’s work is checked before anyone else’s.', B: '{b} is trusted exactly as before.' },
          why: {
            A: 'That is labelling — the reaction to the act, not the act itself, is doing the work.',
            B: 'No label was made to stick to {b}, so the identical act leads nowhere.'
          },
          con: { A: '{b} copied the same homework and is still trusted.', B: '{a}, on the same act, is now checked first.' },
          miss: {
            A: { same: 'The copying is in the past; the report is not.',
                 alt:  'Extra help is kinder, but the report has set an expectation instead.' },
            B: { label: 'That is {a}’s term. {b} was never labelled anything.',
                 alt:   'Nothing was recorded, so there is nothing for staff to act on.' }
          },
          chip: { A: 'Work checked before anyone’s', B: 'Trusted as before' }
        },
        {
          ask: 'A year on, how does {n} see themselves?',
          o: {
            same:  { t: 'No different — one telling-off does not change who you are.', e: '{n} sees themselves no differently' },
            label: { t: 'As someone who cheats — after a while it starts to feel true.', e: '{n} comes to see themselves as someone who cheats' },
            alt:   { t: '{n} rejects the label and sets out to prove it wrong.', e: '{n} rejects the label outright' }
          },
          out: { A: '{a} starts to accept it: I am the one who cheats.', B: '{b} sees themselves exactly as before.' },
          why: {
            A: 'That is the self-fulfilling prophecy — the label changes how staff act, and a year of being checked first is the evidence {a} learns from.',
            B: 'Nobody has treated {b} differently, so there is nothing for {b} to live up to.'
          },
          con: { A: '{b} copied the same homework and thinks nothing of it.', B: '{a}, on the same act, is starting to believe it.' },
          miss: {
            A: { same: 'A telling-off would not. A year of being checked first does.',
                 alt:  'Some do reject it — but {a} has a year of being watched as the evidence.' },
            B: { label: 'Nobody has been treating {b} as a cheat, so there is nothing to absorb.',
                 alt:   'There is no label on {b} to reject.' }
          },
          chip: { A: 'Starts to think: I am a cheat', B: 'Sees themselves no differently' }
        },
        {
          ask: 'By Year 11, what does {n} do?',
          o: {
            same:  { t: 'Carries on much like any other pupil in the year.', e: '{n} carries on like any other pupil' },
            label: { t: 'Stops trying in the subject, and mixes with others in trouble.', e: '{n} stops trying and mixes with others in trouble' },
            alt:   { t: 'Works twice as hard and is moved up a set.', e: '{n} works twice as hard and moves up' }
          },
          out: { A: '{a} stops trying, and settles in with the pupils staff already watch.', B: '{b} carries on like anyone else.' },
          why: {
            A: '‘Cheat’ has become a master status — the first thing staff see, before anything else {a} is — and {a} is on a deviant career, a school life organised around the label.',
            B: 'With no label there is no master status, and no career built on one.'
          },
          con: { A: '{b} did the same thing in Year 10 and is doing fine.', B: '{a}, on the same act, has given up.' },
          miss: {
            A: { same: 'That is {b}’s Year 11, not {a}’s.',
                 alt:  'Some pupils do — but two years of being checked first make that a hard argument to keep having.' },
            B: { label: 'That is {a}. Nothing was ever pinned on {b}.',
                 alt:   '{b} has nothing to prove and no set to climb out of.' }
          },
          chip: { A: 'Stops trying; joins others in trouble', B: 'Carries on like anyone else' }
        }
      ]
    },

    {
      id: 'wall',
      a: 'Rae', b: 'Max',
      headA: 'Rae — police caution', headB: 'Max — sorted at home',
      frame: 'Rae and Max spray-paint the same wall on the same night. Rae is stopped by police and cautioned; Max’s parents pay for the paint.',
      order: ['B', 'A', 'B'],
      steps: [
        {
          ask: 'Over the next year, how do people locally treat {n}?',
          o: {
            same:  { t: 'The same as before — the wall was repainted and forgotten.', e: 'people treat {n} the same as before' },
            label: { t: 'As one to watch — {n} is asked about it first.', e: '{n} is treated as one to watch' },
            alt:   { t: '{n} is offered a place on a youth project and moves on.', e: '{n} is offered a youth project place' }
          },
          out: { A: '{a} is the first person asked when anything happens.', B: '{b} is treated no differently at all.' },
          why: {
            A: 'That is labelling — the caution, not the paint, is doing the work. A label sticks when someone has the power to make it stick.',
            B: 'No official label was attached to {b}, so the identical act leads nowhere.'
          },
          con: { A: '{b} sprayed the same wall and nothing follows.', B: '{a} did exactly the same thing and is now one to watch.' },
          miss: {
            A: { same: 'The paint was cleaned off. The caution was not.',
                 alt:  'Support does happen — but a caution is a public label first.' },
            B: { label: 'That is {a}’s year, not {b}’s. No caution was ever recorded.',
                 alt:   'Nothing official happened, so neither a project nor suspicion follows.' }
          },
          chip: { A: 'Known locally as one to watch', B: 'Nothing follows' }
        },
        {
          ask: 'Applying for a Saturday job, what happens to {n}?',
          o: {
            same:  { t: 'Nothing — one night with a spray can does not follow you.', e: 'the night does not follow {n} at all' },
            label: { t: 'The caution comes up and the shop takes someone else.', e: 'the caution comes up and {n} loses the job' },
            alt:   { t: '{n} explains it honestly and is taken on to prove themselves.', e: '{n} explains it and is taken on' }
          },
          out: { A: '{a} is turned down; the caution is on the record.', B: '{b} gets the job — there is no record to find.' },
          why: {
            A: 'The label has closed a door. Narrowing what a person can do is exactly what makes a label more than a name.',
            B: 'With no record, {b}’s options are untouched by an act both of them committed.'
          },
          con: { A: '{b} did the same thing and gets the job.', B: '{a}, on the same act, is turned down.' },
          miss: {
            A: { same: 'It would not have, had it stayed between the two of them.',
                 alt:  'Honesty helps in some places — but the record is the shop’s evidence.' },
            B: { label: 'There is nothing on {b} for the shop to find.',
                 alt:   'There is nothing to explain — nobody ever wrote it down.' }
          },
          chip: { A: 'Turned down for the job', B: 'Gets the Saturday job' }
        },
        {
          ask: 'Two years on, what does {n} do?',
          o: {
            same:  { t: 'Gets on with life — that night is just a story now.', e: '{n} simply gets on with life' },
            label: { t: 'Spends time with others who have records, and offends again.', e: '{n} offends again, among others with records' },
            alt:   { t: 'Steers clear of trouble to shake the record off.', e: '{n} steers clear to shake the record off' }
          },
          out: { A: '{a} offends again, among the people still open to {a}.', B: '{b} gets into no further trouble.' },
          why: {
            A: '‘Offender’ has become a master status — the first thing anyone sees — and {a} is on a deviant career, a life organised around the label.',
            B: 'No label, no master status, and nothing for a life to organise itself around.'
          },
          con: { A: '{b} sprayed the same wall and is in no trouble at all.', B: '{a}, on the same evidence, is offending again.' },
          miss: {
            A: { same: 'A caution is not a story you can put down when you like.',
                 alt:  'Some manage it — but doors keep closing, and the people still open to {a} have records too.' },
            B: { label: '{b} has no record, and no group pulling {b} in.',
                 alt:   'There is no record for {b} to shake off.' }
          },
          chip: { A: 'Offends again — a deviant career', B: 'No further trouble' }
        }
      ]
    },

    {
      id: 'lateness',
      a: 'Kit', b: 'Ash',
      headA: 'Kit — named, on report', headB: 'Ash — logged as a bus issue',
      frame: 'Kit and Ash are late six times in a term. Kit is named as a problem and put on report; Ash’s is logged as a bus issue.',
      order: ['A', 'A', 'B'],
      steps: [
        {
          ask: 'In lessons that term, how do staff read {n}’s behaviour?',
          o: {
            same:  { t: 'As lateness, and as nothing more than lateness.', e: 'staff read it as lateness and nothing more' },
            label: { t: 'Whatever {n} does is now read as not caring.', e: 'everything {n} does is read as not caring' },
            alt:   { t: 'Staff sort out a lift for {n} and the lateness stops.', e: 'staff sort out a lift for {n}' }
          },
          out: { A: 'A yawn or a missing pen is now read as {a} not caring.', B: '{b}’s lateness stays a bus problem and nothing more.' },
          why: {
            A: 'That is labelling — once a label is applied, ordinary behaviour gets reread through it.',
            B: 'The same lateness, described differently, carries no label at all.'
          },
          con: { A: '{b} was late just as often, and nothing is read into it.', B: '{a} was late just as often, and is now read differently.' },
          miss: {
            A: { same: 'It was lateness until the year meeting named a problem.',
                 alt:  'Practical help exists — but {a} was named as a problem, not as a transport case.' },
            B: { label: 'Nobody named {b} as anything.',
                 alt:   'Possible — but the wording of the log did the work here: it kept the label off.' }
          },
          chip: { A: 'Everything read as ‘not caring’', B: 'Lateness, nothing more' }
        },
        {
          ask: 'At the next set review, where does {n} end up?',
          o: {
            same:  { t: 'In the same set — the marks have not changed.', e: '{n} stays in the same set' },
            label: { t: 'Moved down — staff doubt {n} will keep up.', e: '{n} is moved down a set' },
            alt:   { t: 'Moved up — staff want to give {n} a fresh start.', e: '{n} is moved up a set' }
          },
          out: { A: '{a} is moved down, on exactly the same marks as before.', B: '{b} stays put; the marks decide it.' },
          why: {
            A: 'The label has changed what {a} is offered. Setting turns a reputation into a timetable, and a lower set into a lower grade.',
            B: 'With no label in play, the marks are what the review sees.'
          },
          con: { A: '{b}’s marks are no better, and {b} stays put.', B: '{a}, on the same marks, is moved down.' },
          miss: {
            A: { same: 'The marks have not changed. The reputation has.',
                 alt:  'A fresh start is what {b} effectively gets — {b} was never named.' },
            B: { label: 'There is nothing on {b} for the review to act on.',
                 alt:   'Nothing has changed for {b}, upwards or downwards.' }
          },
          chip: { A: 'Moved down a set', B: 'Stays in the same set' }
        },
        {
          ask: 'By the end of the year, what is {n} known as?',
          o: {
            same:  { t: 'As one pupil among thirty.', e: '{n} is one pupil among thirty' },
            label: { t: 'As ‘the one who doesn’t care’ — before anything else.', e: '{n} is known first as ‘the one who doesn’t care’' },
            alt:   { t: 'As the pupil who turned things around.', e: '{n} is known as the pupil who turned it around' }
          },
          out: { A: 'Doesn’t care comes before anything else anyone knows about {a}.', B: '{b} is one pupil among thirty.' },
          why: {
            A: 'That is a master status — the label that overrides everything else a person is, and it follows {a} into next year.',
            B: 'Nothing was ever made to stick, so nothing overrides the rest of {b}.'
          },
          con: { A: '{b} was late as often and is known for nothing in particular.', B: '{a} was late as often and is known for one thing only.' },
          miss: {
            A: { same: 'That is {b}. {a} was named in a meeting.',
                 alt:  'It happens — but the report followed {a} all year.' },
            B: { label: 'Nobody built that label for {b}.',
                 alt:   'There was nothing for {b} to turn around.' }
          },
          chip: { A: 'Known first as ‘doesn’t care’', B: 'One pupil among thirty' }
        }
      ]
    }
  ];

  /* option order rotates so the same answer is never in the same place */
  var ROT = [['same', 'label', 'alt'], ['alt', 'same', 'label'], ['label', 'alt', 'same']];

  var MASTERY =
    'Three in a row — you have it. A label is a process, not a description: ' +
    'it changes how others treat you, then how you see yourself, and can harden into a ' +
    'master status — the first thing anyone sees — pulling a person into a deviant career, ' +
    'a life organised round it. Interactionists such as Becker argue this; critics reply that ' +
    'not everyone accepts a label, and that it plays down personal responsibility.';

  var CSS = [
    '.svw-lab{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;position:relative}',
    '.svw-lab *{box-sizing:border-box}',
    '.svw-lab .lab-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--lab-accent);margin:0 0 .15rem}',
    '.svw-lab .lab-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.18rem;line-height:1.2;margin:0 0 .25rem}',
    '.svw-lab .lab-frame{font-size:.81rem;line-height:1.42;color:#5b564e;margin:0 0 .5rem}',
    '.svw-lab .lab-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .55rem}',
    '.svw-lab .lab-grid{display:grid;grid-template-columns:16px 1fr 1fr;gap:.3rem .35rem}',
    /* column heads are table headers, not controls: no box, just a rule */
    '.svw-lab .lab-head{font-size:.7rem;font-weight:600;line-height:1.25;padding:0 .12rem .22rem;color:#8d8880;border-bottom:1px solid #e0d9cd}',
    '.svw-lab .lab-head.is-asked{color:var(--lab-accent);border-bottom:2px solid var(--lab-accent)}',
    '.svw-lab .lab-n{font-size:.64rem;font-weight:700;color:#a09a90;display:flex;align-items:center;justify-content:center;line-height:1}',
    '.svw-lab .lab-cell{font-size:.72rem;line-height:1.28;padding:.3rem .4rem;border-radius:8px;background:#fff;border:1px solid #e8e2d9;color:#2d2a26}',
    '.svw-lab .lab-row{display:contents}',
    '.svw-lab .lab-row[hidden]{display:none}',
    '.svw-lab .lab-ask{font-size:.86rem;font-weight:600;line-height:1.34;margin:.5rem 0 .35rem}',
    '.svw-lab .lab-opts{display:grid;gap:.28rem}',
    '.svw-lab .lab-opts[hidden]{display:none}',
    '.svw-lab .lab-opt{display:block;width:100%;text-align:left;font-family:inherit;font-size:.79rem;font-weight:500;line-height:1.3;padding:.4rem .6rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-lab .lab-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-lab .lab-foot{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin-top:.42rem}',
    '.svw-lab .lab-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.42rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-lab .lab-go[disabled]{opacity:.35;cursor:default}',
    '.svw-lab .lab-run{font-size:.75rem;color:#8d8880}',
    '.svw-lab .lab-cap{font-size:.84rem;line-height:1.48;color:#5b564e;margin:.45rem 0 0;min-height:3em}',
    '.svw-lab .lab-v{font-weight:700;color:#2d2a26}',
    '.svw-lab .lab-v.is-ok{color:#4f7d63}',
    '.svw-lab .lab-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
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
      title: 'The same act, twice',
      teaches: 'Labelling is a process, not a description: it changes treatment, then opportunities, then self-image, then behaviour.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};

      /* ---- accent, read from our own node if not handed one ---- */
      var accent = ctx.accent;
      if (!/^#[0-9a-fA-F]{6}$/.test(accent || '')) {
        try { accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) { accent = ''; }
      }
      if (!/^#[0-9a-fA-F]{6}$/.test(accent)) accent = '#8a6a4f';
      /* reducedMotion: honoured by declaring no transitions or timers at all */
      void ctx.reducedMotion;

      /* ---- shell, built once and then mutated ---- */
      var wrap = el('div', 'svw-lab');
      wrap.style.setProperty('--lab-accent', accent);
      wrap.style.setProperty('--lab-tint', accent + '14');
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      wrap.appendChild(el('p', 'lab-kicker', 'Labelling theory'));
      wrap.appendChild(el('h3', 'lab-title', 'The same act, twice'));
      var frame = el('p', 'lab-frame', '');
      wrap.appendChild(frame);

      var stage = el('div', 'lab-stage');
      var grid = el('div', 'lab-grid');
      grid.appendChild(el('div', 'lab-n', ''));
      var headA = el('div', 'lab-head', '');
      var headB = el('div', 'lab-head', '');
      grid.appendChild(headA);
      grid.appendChild(headB);

      var rows = [];
      for (var r = 0; r < 3; r++) {
        var row = el('div', 'lab-row');
        row.hidden = true;
        var num = el('div', 'lab-n', String(r + 1));
        var ca = el('div', 'lab-cell', '');
        var cb = el('div', 'lab-cell', '');
        row.appendChild(num); row.appendChild(ca); row.appendChild(cb);
        grid.appendChild(row);
        rows.push({ row: row, a: ca, b: cb });
      }
      stage.appendChild(grid);
      wrap.appendChild(stage);

      var ask = el('p', 'lab-ask', '');
      wrap.appendChild(ask);

      var opts = el('div', 'lab-opts');
      var optBtns = [];
      for (var i = 0; i < 3; i++) {
        var b = el('button', 'lab-opt', '');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b);
        optBtns.push(b);
      }
      wrap.appendChild(opts);

      var foot = el('div', 'lab-foot');
      var go = el('button', 'lab-go', 'Check');
      go.type = 'button';
      go.disabled = true;
      var run = el('span', 'lab-run', '');
      foot.appendChild(go); foot.appendChild(run);
      wrap.appendChild(foot);

      var cap = el('p', 'lab-cap');
      var capV = el('span', 'lab-v', '');
      var capT = document.createTextNode('');
      cap.appendChild(capV); cap.appendChild(capT);
      wrap.appendChild(cap);

      var sr = el('p', 'lab-sr', '');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var si = 0, sti = 0, picked = null, answered = false;
      var streak = 0, attempted = 0, mastered = false, verdict = null;

      function sc() { return SCENARIOS[si]; }
      function step() { return sc().steps[sti]; }
      function track() { return sc().order[sti]; }
      function askedName() { return track() === 'A' ? sc().a : sc().b; }

      function fill(s) {
        if (!s) return '';
        return s.replace(/\{a\}/g, sc().a).replace(/\{b\}/g, sc().b).replace(/\{n\}/g, askedName());
      }

      function publish() {
        root.dataset.svState = JSON.stringify({
          streak: streak, mastered: mastered, attempted: attempted,
          scenario: sc().id, step: sti + 1, asked: track(),
          picked: picked, verdict: verdict
        });
      }

      function showRun() {
        /* once mastered the caption says it; a second copy is furniture */
        if (mastered) { run.textContent = ''; return; }
        if (streak === 1) { run.textContent = '1 right in a row — two more.'; return; }
        if (streak === 2) { run.textContent = '2 right in a row — one more and you have it.'; return; }
        run.textContent = attempted && !streak ? 'Back to nought — three in a row ends it.' : '';
      }

      function say(head, ok, body) {
        capV.textContent = head;
        capV.className = ok ? 'lab-v is-ok' : 'lab-v';
        capT.nodeValue = body;
        sr.textContent = head + ' ' + body;
      }

      function renderScenario() {
        var s = sc();
        frame.textContent = s.frame + ' ' + ASKLINE;
        headA.textContent = s.headA;
        headB.textContent = s.headB;
        for (var k = 0; k < rows.length; k++) {
          rows[k].row.hidden = true;
          rows[k].a.textContent = '';
          rows[k].b.textContent = '';
        }
        sti = 0;
        renderStep();
      }

      function renderStep() {
        var st = step(), t = track();
        answered = false;
        picked = null;
        verdict = null;
        headA.classList.toggle('is-asked', t === 'A');
        headB.classList.toggle('is-asked', t === 'B');
        ask.textContent = fill(st.ask);
        var order = ROT[(si + sti) % 3];
        for (var i = 0; i < 3; i++) {
          var key = order[i];
          optBtns[i].textContent = fill(st.o[key].t);
          optBtns[i].dataset.opt = key;
          optBtns[i].setAttribute('aria-pressed', 'false');
          optBtns[i].disabled = false;
        }
        opts.hidden = false;
        go.textContent = 'Check';
        go.disabled = true;
        say('', false, attempted
          ? 'Same act, different label. Which of the two are you predicting for?'
          : 'Both did the same thing. Only one of them was labelled for it.');
        showRun();
        publish();
      }

      function choose(i) {
        if (answered) return;
        picked = optBtns[i].dataset.opt;
        for (var k = 0; k < 3; k++) {
          optBtns[k].setAttribute('aria-pressed', optBtns[k] === optBtns[i] ? 'true' : 'false');
        }
        go.disabled = false;
        publish();
      }

      function commit() {
        if (answered || !picked) return;
        var st = step(), t = track();
        var right = (t === 'A') ? 'label' : 'same';
        var ok = picked === right;
        answered = true;
        attempted++;
        verdict = ok ? 'right' : 'wrong';
        streak = ok ? streak + 1 : 0;

        /* reveal BOTH tracks for this step, from the model */
        rows[sti].a.textContent = st.chip.A;
        rows[sti].b.textContent = st.chip.B;
        rows[sti].row.hidden = false;

        opts.hidden = true;
        for (var k = 0; k < 3; k++) optBtns[k].disabled = true;

        var echo = fill(st.o[picked].e);
        var body;
        if (ok) {
          body = ' — you said ' + echo + '. ' + fill(st.why[t]) + ' ' + fill(st.con[t]);
        } else {
          body = ' — you said ' + echo + '. ' + fill(st.miss[t][picked]) +
                 ' What happens: ' + fill(st.out[t]) + ' ' + fill(st.why[t]);
        }

        if (ok && streak === 3 && !mastered) {
          mastered = true;
          say('Right', true, ' — you said ' + echo + '. ' + MASTERY);
        } else {
          say(ok ? 'Right' : 'Not quite', ok, body);
        }

        var last = (sti === sc().steps.length - 1);
        go.textContent = mastered ? 'Another anyway' : (last ? 'Next pair' : 'Next step');
        go.disabled = false;
        showRun();
        publish();
      }

      function advance() {
        if (sti < sc().steps.length - 1) {
          sti++;
          renderStep();
        } else {
          si = (si + 1) % SCENARIOS.length;
          renderScenario();
        }
      }

      optBtns.forEach(function (b, i) {
        b.addEventListener('click', function () { choose(i); });
      });
      go.addEventListener('click', function () {
        if (answered) advance(); else commit();
      });

      renderScenario();
    }
  };
})();
