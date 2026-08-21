/* cross-cutting-structural-device
   Two original devised-theatre fragments sit side by side. The student
   predicts what the AUDIENCE gets when a director intercuts them rather
   than playing one and then the other, commits, and only then watches the
   intercut running order play with the emergent effect written at each cut.
   All scene material is original and neutral: no published play is quoted. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     The pairs. Each carries two scenes, the intercut running order the
     reveal plays, and four question shapes. Every question holds one
     committable misconception (m:true) so the wrong picture the widget
     exists to falsify can actually be entered.
     --------------------------------------------------------------- */
  var PAIRS = [
    {
      id: 'candles',
      a: { slug: 'A · A kitchen. Six o’clock.',
           lines: ['MAYA: One for every year. One for luck.',
                   'MUM: Wait for your dad. He’s never late.'] },
      b: { slug: 'B · An office corridor. Six o’clock.',
           lines: ['MANAGER: Effective from the month’s end.',
                   'DAD: I’ll tell them at the weekend.'] },
      strip: [
        ['A', 'MAYA: One for every year. One for luck.'],
        ['cut', 'cut mid-wish, with the match still lit —'],
        ['B', 'MANAGER: Effective from the month’s end.'],
        ['cut', '— and back, the letter now in the room with them'],
        ['A', 'MUM: Wait for your dad. He’s never late.']
      ],
      qs: [
        { type: 'effect',
          q: 'A director intercuts these two scenes. What does that do to the kitchen for an audience?',
          opts: [
            { t: 'Fragile — the wish is heard with the letter', ok: true },
            { t: 'Less tense — we already know the news',
              why: 'Knowing before the characters do is dramatic irony, and it tightens the scene rather than releasing it — we watch them walk towards something we can already see.' },
            { t: 'Faster — the play stops dragging',
              why: 'Pace is a by-product. A structural device is chosen for what the pairing means, not to stop a scene outstaying its welcome.' },
            { t: 'Nothing new — each scene means what it says', m: true,
              why: 'The letter changes no word in the kitchen, but it changes what those words mean to us: “He’s never late” now lands as an ache.' }
          ],
          teach: 'Set against the letter, the celebration turns fragile. That fragility is created by the juxtaposition — it is in neither scene alone.' },
        { type: 'adds',
          q: 'What does the intercutting give the audience that neither scene holds on its own?',
          opts: [
            { t: 'Knowledge the family has not got, so every hopeful line aches.', ok: true,
              e: 'knowledge the family has not got' },
            { t: 'A quicker route through the plot, so no scene outstays its welcome.',
              e: 'a quicker route through the plot',
              why: 'That is pacing, and pacing is a side effect. Cross-cutting is a structural choice about meaning.' },
            { t: 'Nothing extra — two scenes side by side still mean what each one says.', m: true,
              e: 'nothing extra',
              why: 'Side by side is exactly the point: the audience does the joining, and what they join is not written in either scene.' }
          ],
          teach: 'The juxtaposition creates dramatic irony for the audience — we hold the letter while the family holds the candle.' },
        { type: 'cut',
          q: 'Where should the director cut away from the kitchen for the sharpest effect?',
          opts: [
            { t: 'Mid-wish, on “one for luck”', ok: true },
            { t: 'After the kitchen scene has finished',
              why: 'Waiting for a scene to finish is sequence, not cross-cutting. The two worlds never overlap, so nothing is held in tension.' },
            { t: 'Anywhere — the cut only changes scene', m: true,
              why: 'Placement is the whole craft. Cutting on the word “luck” makes the corridor answer it; cutting anywhere else lets the wish settle first.' }
          ],
          teach: 'Cut on the wish and the corridor answers it. The audience hears luck and redundancy in one breath — that collision is the effect.' },
        { type: 'exam',
          q: 'Which sentence would earn the marks in an answer about this moment?',
          opts: [
            { t: 'Cross-cutting sets the wish against the letter, so the celebration feels fragile.', ok: true,
              e: 'cross-cutting sets the wish against the letter' },
            { t: 'The playwright uses cross-cutting between the kitchen and the corridor.', m: true,
              e: 'the playwright uses cross-cutting',
              why: 'True, and worth nothing on its own. The device is named and the effect is missing — the commonest way a good point scores zero.' },
            { t: 'The kitchen scene is happy and the corridor scene is sad.',
              e: 'one scene is happy, one is sad',
              why: 'That is a summary of content. It names no device and no effect, so there is nothing for the audience to experience in it.' }
          ],
          teach: 'Name the device, then say what the juxtaposition creates for the audience. Device plus effect is the sentence that scores.' }
      ]
    },

    {
      id: 'rehearsal',
      a: { slug: 'A · A rehearsal room. First week.',
           lines: ['SAM: Sorry. I’ll move. I’m in the way.',
                   'DIRECTOR: Stand where you like, Sam.'] },
      b: { slug: 'B · The same room. Six years on.',
           lines: ['SAM: We go from the top. Everybody watching.',
                   'SAM: Stand where you like. I’ll find you.'] },
      strip: [
        ['A', 'DIRECTOR: Stand where you like, Sam.'],
        ['cut', 'the same room, six years later —'],
        ['B', 'SAM: Stand where you like. I’ll find you.'],
        ['cut', '— the borrowed line, now said by the one who needed it'],
        ['A', 'SAM: Sorry. I’ll move. I’m in the way.']
      ],
      qs: [
        { type: 'effect',
          q: 'Both scenes show the same person. What does intercutting them do for an audience?',
          opts: [
            { t: 'Change becomes measurable, not reported', ok: true },
            { t: 'The timeline blurs and Sam is hard to follow',
              why: 'The slugs keep the years clear. Cross-cutting asks the audience to compare, not to guess which scene is which.' },
            { t: 'It saves staging the six years in between',
              why: 'It does save them, but that is economy, not meaning. Played in sequence it would save them too, and the comparison would vanish.' },
            { t: 'Nothing new — a shy Sam and a bold Sam', m: true,
              why: 'Alone, each scene is one temperament. Held together, they become a distance travelled — and distance is not written in either scene.' }
          ],
          teach: 'Side by side, the two Sams stop being descriptions and become a measurement. The audience does the measuring — that is what the structure creates.' },
        { type: 'adds',
          q: 'What does the juxtaposition add that neither scene contains alone?',
          opts: [
            { t: 'A measure of change: the later line only means something beside the earlier one.', ok: true,
              e: 'a measure of change' },
            { t: 'Extra information about the rehearsal room and how it is run.',
              e: 'information about the room',
              why: 'The room is the constant, not the content. It is there so the audience has something fixed to measure the change against.' },
            { t: 'Nothing — each scene already says everything it means.', m: true,
              e: 'nothing is added',
              why: '“Stand where you like” is ordinary on its own. Only the pairing turns it into proof that Sam has become the person who once needed saying to.' }
          ],
          teach: 'The repeated line carries no weight by itself. The juxtaposition loads it, and the audience feels six years in one sentence.' },
        { type: 'cut',
          q: 'Where should the cut fall so the change registers hardest?',
          opts: [
            { t: 'On the repeated line, so it returns in another mouth', ok: true },
            { t: 'At the very start, before either Sam speaks',
              why: 'An early cut costs nothing, because nothing has been said yet for the other scene to answer.' },
            { t: 'It makes no difference where the cut lands', m: true,
              why: 'It makes all the difference. Cut on the repeated line and the audience hears the echo; cut elsewhere and the echo is simply missed.' }
          ],
          teach: 'Cut on the echo and the audience hears the same words twice in two mouths. The structure states the change without a line of dialogue saying so.' },
        { type: 'exam',
          q: 'Which sentence would earn the marks in an answer about this structure?',
          opts: [
            { t: 'Cross-cutting sets the two Sams side by side, so the audience measures the change.', ok: true,
              e: 'cross-cutting lets the audience measure the change' },
            { t: 'The play cross-cuts between Sam early on and Sam six years later.', m: true,
              e: 'the play cross-cuts between the two Sams',
              why: 'The device is named and stops. An examiner has nothing to credit until you say what the pairing does to the audience.' },
            { t: 'Sam is nervous in the first scene and confident in the second.',
              e: 'Sam is nervous, then confident',
              why: 'Character description, and both halves are true read alone — which is precisely the reading the structure is built to defeat.' }
          ],
          teach: 'Device, then effect. “This juxtaposition creates … for the audience” is the clause that turns a spotted technique into a mark.' }
      ]
    },

    {
      id: 'phonecall',
      a: { slug: 'A · A ward office. Late.',
           lines: ['NURSE: I’ll ring the family before I go.',
                   'NURSE: Better they hear it tonight.'] },
      b: { slug: 'B · A front room. The same hour.',
           lines: ['GRAN: Home by Friday. Bed’s made up.',
                   'GRAN: Nobody rings this late. Good sign.'] },
      strip: [
        ['A', 'NURSE: I’ll ring the family before I go.'],
        ['cut', 'the receiver is already lifted —'],
        ['B', 'GRAN: Nobody rings this late. Good sign.'],
        ['cut', '— hope, spoken straight into a call on its way'],
        ['A', 'NURSE: Better they hear it tonight.']
      ],
      qs: [
        { type: 'effect',
          q: 'The two scenes are intercut. What does the front room feel like now?',
          opts: [
            { t: 'Dread — each hopeful line is a countdown', ok: true },
            { t: 'Surprise — the news lands on us with Gran',
              why: 'Surprise needs the audience kept in the dark. Cross-cutting deliberately does the opposite: it hands us the news early so we watch it travel.' },
            { t: 'Relief — we are told what is coming',
              why: 'Being told is not relief when the other room cannot be warned. Knowing first is what makes it unbearable.' },
            { t: 'No change — the front room is simply hopeful', m: true,
              why: 'The words are hopeful; the meaning is not. “Good sign” only reads as hope if you have not just watched the nurse lift the receiver.' }
          ],
          teach: 'The juxtaposition turns hope into dread for the audience. Nothing in the front room has changed except what we know while we watch it.' },
        { type: 'adds',
          q: 'What does the intercut structure add that neither scene holds alone?',
          opts: [
            { t: 'Inevitability: the audience knows the two rooms must meet.', ok: true,
              e: 'inevitability' },
            { t: 'A neat way to cover the time the phone call takes.',
              e: 'a way to cover the time',
              why: 'Cross-cutting can compress time, but that is housekeeping. Here it exists so the audience holds both rooms at once.' },
            { t: 'Nothing — bad news in one room, hope in the other, as written.', m: true,
              e: 'nothing is added',
              why: 'Read apart, one room is sad and the other is hopeful. Read together, the hopeful room becomes the painful one — and that is not on either page.' }
          ],
          teach: 'Held together, the two rooms create inevitability. The audience is not waiting to find out; it is waiting to watch it arrive.' },
        { type: 'cut',
          q: 'Where should the director cut for the collision to bite hardest?',
          opts: [
            { t: 'On “Good sign”, straight to the dialling', ok: true },
            { t: 'After the nurse has finished the call',
              why: 'By then the audience has nothing left to dread. The tension lives in the gap between the receiver going up and the phone ringing.' },
            { t: 'Anywhere — the cut just moves us between rooms', m: true,
              why: 'Moving between rooms is the least of it. Land the cut on the most hopeful line and the audience feels the two realities touch.' }
          ],
          teach: 'Cut on the hope and drop it onto the dialling. The audience holds both rooms in one second — that overlap is the whole device.' },
        { type: 'exam',
          q: 'Which sentence would earn the marks in an answer about this moment?',
          opts: [
            { t: 'Cutting from the dialling to “Good sign” turns Gran’s hope into dread for us.', ok: true,
              e: 'the cut turns hope into dread' },
            { t: 'The playwright cross-cuts between the ward and the front room.', m: true,
              e: 'the playwright cross-cuts between the rooms',
              why: 'Spotting the device is the easy half. Without the audience’s experience attached, the sentence stays at description.' },
            { t: 'Gran is hopeful, but the nurse has bad news to give.',
              e: 'Gran is hopeful, the nurse is not',
              why: 'Plot summary. It treats the two scenes as separate reports, which is exactly what the structure refuses to let them be.' }
          ],
          teach: 'Name the cut, then name what it does to us. Device plus audience effect is the sentence that scores.' }
      ]
    },

    {
      id: 'speech',
      a: { slug: 'A · A town hall. Rehearsing.',
           lines: ['LEADER: This town looks after its own.',
                   'AIDE: Warmer on “its own”. Try it again.'] },
      b: { slug: 'B · A shuttered door. The same evening.',
           lines: ['VOLUNTEER: We shut at four. Try Thursday.',
                   'PARENT: Thursday is three days.'] },
      strip: [
        ['A', 'LEADER: This town looks after its own.'],
        ['cut', 'the claim is still in the air —'],
        ['B', 'PARENT: Thursday is three days.'],
        ['cut', '— and the door has answered the speech for us'],
        ['A', 'AIDE: Warmer on “its own”. Try it again.']
      ],
      qs: [
        { type: 'effect',
          q: 'The speech and the doorway are intercut. What does an audience do with them?',
          opts: [
            { t: 'Irony — we judge the speech by the door', ok: true },
            { t: 'Balance — we see both sides and take neither',
              why: 'The two scenes are not weighted equally. One is rehearsed, the other is happening — and the audience notices which is which.' },
            { t: 'Suspense — we wait to learn if it is true',
              why: 'There is no waiting. The doorway has already answered the claim, so the audience is judging, not wondering.' },
            { t: 'Neither changes — a speech and a closed door', m: true,
              why: 'Alone, the speech is warm and the door is unlucky. Together, the speech becomes a lie — and no line in either scene says so.' }
          ],
          teach: 'The juxtaposition creates irony for the audience: the claim is tested against the evidence, and the audience delivers the verdict itself.' },
        { type: 'adds',
          q: 'What does the pairing add that neither scene contains on its own?',
          opts: [
            { t: 'A verdict the audience reaches itself, unstated by either scene.', ok: true,
              e: 'a verdict the audience reaches itself' },
            { t: 'A change of location, so the staging stays varied.',
              e: 'a change of location',
              why: 'Variety is decoration. If the second scene could be swapped for any other location, the structure is doing no work.' },
            { t: 'Nothing — each scene means exactly what its own words mean.', m: true,
              e: 'nothing is added',
              why: '“Looks after its own” means one thing in a town hall and another beside a shut door. The audience supplies the second meaning.' }
          ],
          teach: 'Neither scene calls the leader a hypocrite. The structure makes the audience conclude it, which is why the point lands harder than a speech ever could.' },
        { type: 'cut',
          q: 'Where should the director cut away from the speech?',
          opts: [
            { t: 'On “looks after its own”, so the door replies', ok: true },
            { t: 'Once the speech has been rehearsed twice',
              why: 'Let the claim finish and the audience files it away. The cut has to interrupt the claim for the door to read as a reply.' },
            { t: 'Anywhere — the cut signals a new scene', m: true,
              why: 'A cut placed on the boast makes the doorway answer it. Placed anywhere else, the two scenes are just two scenes.' }
          ],
          teach: 'Cut on the boast and the shut door becomes the reply. The audience puts the question and the answer together — that is the structure working.' },
        { type: 'exam',
          q: 'Which sentence would earn the marks in an answer about this structure?',
          opts: [
            { t: 'Cutting from the rehearsed speech to the shut door lets the audience judge the claim.', ok: true,
              e: 'the cut lets the audience judge the claim' },
            { t: 'The playwright cross-cuts between the town hall and the doorway.', m: true,
              e: 'the playwright cross-cuts between the two places',
              why: 'The device is identified and abandoned. Add the audience’s experience and the same observation becomes an argument.' },
            { t: 'The leader’s speech is not true for everybody in the town.',
              e: 'the speech is not true for everybody',
              why: 'That is your conclusion without the evidence. The mark is for showing how the structure made the audience reach it.' }
          ],
          teach: 'Device, then effect: “this juxtaposition creates … for the audience”. Naming cross-cutting and stopping is the commonest way a good point scores nothing.' }
      ]
    }
  ];

  var CSS = [
    '.svw-xcut{display:flex;flex-direction:column;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4;-webkit-text-size-adjust:100%}',
    '.svw-xcut *{box-sizing:border-box}',
    '.svw-xcut .x-head{display:flex;align-items:baseline;justify-content:space-between;gap:.6rem}',
    '.svw-xcut .x-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--x-accent)}',
    '.svw-xcut .x-streak{font-size:.7rem;font-weight:600;color:#8d8880;font-variant-numeric:tabular-nums;text-align:right}',
    '.svw-xcut .x-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;margin:.1rem 0 .3rem}',
    '.svw-xcut .x-frame{font-size:.8rem;line-height:1.42;color:#5b564e;margin:0 0 .45rem}',
    '.svw-xcut .x-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem}',
    '.svw-xcut .x-scenes{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:.5rem}',
    '.svw-xcut .x-card{background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:.42rem .55rem}',
    '.svw-xcut .x-slug{font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880;margin-bottom:.3rem}',
    '.svw-xcut .x-line{font-size:.8rem;line-height:1.38;margin:0 0 .15rem}',
    '.svw-xcut .x-line:last-child{margin-bottom:0}',
    '.svw-xcut .x-strip{display:block}',
    '.svw-xcut .x-beat{display:flex;gap:.5rem;align-items:baseline;background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:.38rem .55rem}',
    '.svw-xcut .x-tag{font-size:.62rem;font-weight:700;letter-spacing:.06em;color:#8d8880;flex:0 0 auto}',
    '.svw-xcut .x-btext{font-size:.8rem;line-height:1.35;flex:1 1 auto}',
    '.svw-xcut .x-cutrow{display:flex;gap:.45rem;align-items:baseline;padding:.22rem .1rem .22rem .3rem}',
    '.svw-xcut .x-dot{flex:0 0 auto;width:6px;height:6px;border-radius:50%;background:var(--x-accent);transform:translateY(-1px)}',
    '.svw-xcut .x-cuttext{font-size:.74rem;line-height:1.3;color:#5b564e;font-style:italic;flex:1 1 auto}',
    '.svw-xcut .x-q{font-size:.84rem;font-weight:600;line-height:1.38;margin:.5rem 0 .35rem}',
    '.svw-xcut .x-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.35rem}',
    '.svw-xcut .x-opt{font:inherit;font-size:.8rem;line-height:1.34;text-align:left;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .55rem;cursor:pointer;width:100%}',
    '.svw-xcut .x-opt:hover{border-color:#c9c1b4}',
    '.svw-xcut .x-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-xcut .x-opt:disabled{cursor:default;opacity:.62}',
    '.svw-xcut .x-opt.is-answer:disabled{opacity:1;border-color:#4f7d63;background:#fff;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-xcut .x-opt.is-picked:disabled{opacity:1}',
    '.svw-xcut .x-act{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.45rem 0 0}',
    '.svw-xcut .x-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-xcut .x-go[disabled]{background:#faf8f5;color:#8d8880;border-color:#ddd7cd;cursor:default}',
    '.svw-xcut .x-cap{font-size:.82rem;line-height:1.5;color:#5b564e;margin:.42rem 0 0;min-height:2.5rem}',
    '.svw-xcut .x-cap b{color:#2d2a26}',
    '.svw-xcut .x-cap .x-ok{color:#4f7d63}',
    '.svw-xcut .x-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-xcut .is-off{display:none}',
    '.svw-xcut.x-done .x-cap{order:1}',
    '.svw-xcut.x-done .x-act{order:2}',
    '.svw-xcut .x-fade{opacity:1}',
    '.svw-xcut.x-anim .x-fade{opacity:0;transition:opacity .38s cubic-bezier(.16,1,.3,1)}',
    '.svw-xcut.x-anim.x-played .x-fade{opacity:1}',
    '.svw-xcut.x-anim .x-fade:nth-child(2){transition-delay:.09s}',
    '.svw-xcut.x-anim .x-fade:nth-child(3){transition-delay:.18s}',
    '.svw-xcut.x-anim .x-fade:nth-child(4){transition-delay:.27s}',
    '.svw-xcut.x-anim .x-fade:nth-child(5){transition-delay:.36s}'
  ].join('\n');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'cross-cutting-structural-device',
      title: 'Two scenes, one cut',
      teaches: 'Cross-cutting is a structural choice: the meaning lives in the juxtaposition, not inside either scene.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      root.innerHTML = '';
      root.className = 'svw-xcut';
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      root.style.setProperty('--x-accent', accent);
      var reduced = !!ctx.reducedMotion;
      if (!reduced) root.classList.add('x-anim');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* ---- state ---- */
      var streak = 0, attempted = 0, mastered = false;
      var pair = null, item = null, order = null, picked = -1, committed = false;
      var lastPair = -1, lastType = '';

      /* ---- fixed furniture, built once ---- */
      var head = el('div', 'x-head');
      head.appendChild(el('span', 'x-kick', 'Structure'));
      var streakEl = el('span', 'x-streak is-off', '');
      head.appendChild(streakEl);
      root.appendChild(head);

      root.appendChild(el('h3', 'x-title', 'Two scenes, one cut'));
      root.appendChild(el('p', 'x-frame',
        'Two scenes from a devised piece. A director will intercut them, not play one and then the other.'));

      var stage = el('div', 'x-stage');
      var scenes = el('div', 'x-scenes');
      var cardA = el('div', 'x-card'), cardB = el('div', 'x-card');
      var slugA = el('div', 'x-slug'), slugB = el('div', 'x-slug');
      cardA.appendChild(slugA); cardB.appendChild(slugB);
      var lineA = [el('p', 'x-line'), el('p', 'x-line')];
      var lineB = [el('p', 'x-line'), el('p', 'x-line')];
      lineA.forEach(function (p) { cardA.appendChild(p); });
      lineB.forEach(function (p) { cardB.appendChild(p); });
      scenes.appendChild(cardA); scenes.appendChild(cardB);
      var strip = el('div', 'x-strip is-off');
      var rows = [];
      for (var r = 0; r < 5; r++) {
        var row;
        if (r % 2 === 0) {
          row = el('div', 'x-beat x-fade');
          row.appendChild(el('span', 'x-tag'));
          row.appendChild(el('span', 'x-btext'));
        } else {
          row = el('div', 'x-cutrow x-fade');
          row.appendChild(el('span', 'x-dot'));
          row.appendChild(el('span', 'x-cuttext'));
        }
        rows.push(row);
        strip.appendChild(row);
      }
      stage.appendChild(scenes); stage.appendChild(strip);
      root.appendChild(stage);

      var qEl = el('p', 'x-q');
      root.appendChild(qEl);

      var optWrap = el('div', 'x-opts');
      var optBtns = [];
      for (var o = 0; o < 4; o++) {
        var b = el('button', 'x-opt');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        (function (idx) {
          b.addEventListener('click', function () { pick(idx); });
        })(o);
        optBtns.push(b);
        optWrap.appendChild(b);
      }
      root.appendChild(optWrap);

      var act = el('div', 'x-act');
      var go = el('button', 'x-go', 'See it intercut');
      go.type = 'button';
      go.disabled = true;
      go.addEventListener('click', function () {
        if (!committed) commit(); else newRound();
      });
      act.appendChild(go);
      root.appendChild(act);

      var cap = el('p', 'x-cap');
      root.appendChild(cap);
      var sr = el('p', 'x-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !committed && picked >= 0) { pick(-1); }
      });

      /* ---- rendering ---- */
      function setCap(html) { cap.innerHTML = html; }

      function pushState(extra) {
        var s = {
          pair: pair ? pair.id : null,
          question: item ? item.type : null,
          picked: picked,
          committed: committed,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        };
        if (extra) for (var k in extra) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      function pick(idx) {
        if (committed || !order || idx >= order.length) return;
        picked = (picked === idx) ? -1 : idx;
        for (var i = 0; i < optBtns.length; i++) {
          optBtns[i].setAttribute('aria-pressed', String(i === picked));
        }
        go.disabled = picked < 0;
        pushState();
      }

      function shortOf(opt) { return opt.e || opt.t; }

      function newRound() {
        /* pick a pair and a question shape, never repeating either back to back */
        var pi = lastPair, guard = 0;
        while ((pi === lastPair) && guard++ < 40) pi = Math.floor(Math.random() * PAIRS.length);
        lastPair = pi;
        pair = PAIRS[pi];
        var choices = pair.qs.filter(function (q) { return q.type !== lastType; });
        if (!choices.length) choices = pair.qs;
        item = choices[Math.floor(Math.random() * choices.length)];
        lastType = item.type;

        /* shuffle the options, keeping a map back to the authored objects */
        order = item.opts.map(function (_, i) { return i; });
        for (var i = order.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1)), t = order[i]; order[i] = order[j]; order[j] = t;
        }

        committed = false;
        picked = -1;

        slugA.textContent = pair.a.slug;
        slugB.textContent = pair.b.slug;
        lineA[0].textContent = pair.a.lines[0];
        lineA[1].textContent = pair.a.lines[1];
        lineB[0].textContent = pair.b.lines[0];
        lineB[1].textContent = pair.b.lines[1];
        scenes.classList.remove('is-off');
        strip.classList.add('is-off');
        root.classList.remove('x-done');
        root.classList.remove('x-played');

        qEl.textContent = item.q;
        optWrap.classList.remove('is-off');
        for (var k = 0; k < optBtns.length; k++) {
          var btn = optBtns[k];
          if (k < order.length) {
            btn.classList.remove('is-off', 'is-answer', 'is-picked');
            btn.disabled = false;
            btn.setAttribute('aria-pressed', 'false');
            btn.textContent = item.opts[order[k]].t;
          } else {
            btn.classList.add('is-off');
            btn.disabled = true;
            btn.textContent = '';
          }
        }

        go.textContent = 'See it intercut';
        go.disabled = true;
        setCap('Both scenes are written. The choice is whether the audience holds them one at a time — or both at once.');
        renderStreak();
        pushState();
      }

      function renderStreak() {
        if (attempted === 0) { streakEl.classList.add('is-off'); return; }
        streakEl.classList.remove('is-off');
        if (mastered) streakEl.textContent = 'You have it';
        else if (streak === 0) streakEl.textContent = 'Back to zero';
        else if (streak === 1) streakEl.textContent = '1 right in a row';
        else streakEl.textContent = streak + ' in a row — one more';
      }

      function commit() {
        if (committed || picked < 0 || picked >= order.length) return;
        var opt = item.opts[order[picked]];
        var right = !!opt.ok;
        committed = true;
        attempted++;
        streak = right ? streak + 1 : 0;
        var justMastered = false;
        if (streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        /* play the intercut running order in the same stage */
        for (var r2 = 0; r2 < 5; r2++) {
          var spec = pair.strip[r2];
          var kids = rows[r2].children;
          if (spec[0] === 'cut') { kids[1].textContent = spec[1]; }
          else { kids[0].textContent = spec[0]; kids[1].textContent = spec[1]; }
        }
        scenes.classList.add('is-off');
        strip.classList.remove('is-off');
        root.classList.add('x-done');
        if (!reduced) {
          /* one forced reflow, then the staggered fade; no timers left running */
          void strip.offsetWidth;
          root.classList.add('x-played');
        }

        /* lock the options, mark what was chosen and what was right */
        for (var k = 0; k < optBtns.length && k < order.length; k++) {
          optBtns[k].disabled = true;
          if (k === picked) optBtns[k].classList.add('is-picked');
          if (item.opts[order[k]].ok) optBtns[k].classList.add('is-answer');
        }
        optWrap.classList.add('is-off');

        var msg;
        if (right) {
          msg = '<b class="x-ok">Right</b> — you chose “' + esc(shortOf(opt)) + '”. ' + esc(item.teach);
        } else {
          var answer = null;
          for (var a = 0; a < item.opts.length; a++) if (item.opts[a].ok) answer = item.opts[a];
          msg = '<b>Not quite</b> — you chose “' + esc(shortOf(opt)) + '”. ' +
                esc(opt.why || '') + ' The one that holds up: “' + esc(shortOf(answer)) + '”. ' +
                esc(item.teach);
        }
        if (justMastered) {
          msg += ' <b>Three in a row — you have it.</b> Cross-cutting is structural: the audience holds both scenes at once, and the meaning is made where they touch.';
        }
        setCap(msg);
        sr.textContent = (right ? 'Right. ' : 'Not quite. ') + cap.textContent;

        go.textContent = mastered ? 'Another anyway' : 'Next pair';
        go.disabled = false;
        renderStreak();
        pushState({ correct: right });
      }

      function esc(s) {
        return String(s == null ? '' : s)
          .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      }

      newRound();
      /* first render should not advertise a run that does not exist yet */
      streakEl.classList.add('is-off');
      pushState();
    }
  };
})();
