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
        ['cut', 'cut here, in the middle of the wish —'],
        ['B', 'MANAGER: Effective from the month’s end.'],
        ['cut', '— now we know why he will be late tonight'],
        ['A', 'MUM: Wait for your dad. He’s never late.']
      ],
      qs: [
        { type: 'effect',
          q: 'A director cuts back and forth between these two scenes. What does that do to the kitchen scene for an audience?',
          opts: [
            { t: 'The celebration starts to feel fragile, because we can see the letter and the family cannot.', ok: true,
              e: 'the celebration starts to feel fragile' },
            { t: 'It feels less tense, because the audience already knows the bad news.',
              e: 'it feels less tense',
              why: 'Knowing something before the characters do is called dramatic irony, and it makes a scene more tense, not less. We sit there waiting for the family to find out.' },
            { t: 'Nothing changes. The kitchen scene still means what it says on its own.', m: true,
              e: 'nothing changes',
              why: 'The letter does not change a single word in the kitchen, but it changes what those words mean to us. On its own, “He’s never late” is ordinary. Next to the letter it hurts.' }
          ],
          teach: 'Because the two scenes run together, we hold the birthday and the letter in mind at the same time. That is what makes the celebration feel fragile, and it is in neither scene on its own.' },
        { type: 'adds',
          q: 'What does cutting between the scenes give the audience that neither scene gives on its own?',
          opts: [
            { t: 'Knowledge the family has not got: we know about the letter while they light the candles.', ok: true,
              e: 'knowledge the family has not got' },
            { t: 'A faster pace, so that neither scene has time to drag.',
              e: 'a faster pace',
              why: 'Cutting between scenes can speed a play up, but that is a side effect. A writer chooses it for what the two scenes mean when we hold them together.' },
            { t: 'Nothing extra. Two scenes side by side still mean what each one says.', m: true,
              e: 'nothing extra',
              why: 'Putting them side by side is the whole point. The audience joins the two scenes up, and what we join them into is written in neither of them.' }
          ],
          teach: 'Watching both scenes almost at once gives us information the family has not got. That is dramatic irony, and here it is made by the structure, not by any line in the script.' },
        { type: 'cut',
          q: 'Where should the director cut away from the kitchen to make the strongest effect?',
          opts: [
            { t: 'In the middle of the wish, on the words “one for luck”.', ok: true,
              e: 'cut in the middle of the wish' },
            { t: 'After the kitchen scene has finished, so that no scene gets interrupted.',
              e: 'cut after the kitchen scene ends',
              why: 'If you wait for a scene to finish, you have written a sequence, not a cross-cut. The two worlds never overlap, so the audience never holds them at the same time.' },
            { t: 'It does not matter where. The cut only tells us the scene has changed.', m: true,
              e: 'it does not matter where',
              why: 'Where the cut lands is the whole craft. Cut on the word “luck” and the corridor seems to answer it. Cut any later and the wish has already settled, so nothing collides.' }
          ],
          teach: 'Cutting on the wish drops the redundancy letter straight on top of the word “luck”. The audience gets luck and job loss in the same second, and that is what makes the moment land.' },
        { type: 'exam',
          q: 'Which sentence would earn marks in an answer about this moment?',
          opts: [
            { t: 'Cross-cutting makes us hear the birthday wish while we can see the letter, so the celebration feels fragile.', ok: true,
              e: 'cross-cutting makes the celebration feel fragile' },
            { t: 'The playwright uses cross-cutting between the kitchen scene and the corridor scene.', m: true,
              e: 'the playwright uses cross-cutting',
              why: 'This is true, and on its own it earns nothing. It names the technique and then stops, without saying what the technique does to the audience.' },
            { t: 'The kitchen scene is happy and the corridor scene is sad.',
              e: 'one scene is happy, one is sad',
              why: 'This describes what happens in each scene. It names no technique and no effect on the audience, so there is nothing for an examiner to credit.' }
          ],
          teach: 'Name the technique, then say what it does to the audience. “Cross-cutting … so the audience …” is the shape of a sentence that scores.' }
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
        ['cut', 'cut to the same room, six years later —'],
        ['B', 'SAM: Stand where you like. I’ll find you.'],
        ['cut', '— the same words, now said by Sam'],
        ['A', 'SAM: Sorry. I’ll move. I’m in the way.']
      ],
      qs: [
        { type: 'effect',
          q: 'Both scenes show the same person. What does cutting between them do for an audience?',
          opts: [
            { t: 'We can measure how far Sam has changed, instead of being told about it.', ok: true,
              e: 'we can measure how far Sam has changed' },
            { t: 'It saves the writer having to stage the six years in between.',
              e: 'it saves staging the six years',
              why: 'It does save them, but playing the scenes one after the other would save them too. That is economy, not meaning, and the comparison would be lost.' },
            { t: 'Nothing new. One scene shows a shy Sam and the other shows a confident Sam.', m: true,
              e: 'nothing new: a shy Sam and a confident Sam',
              why: 'On its own, each scene shows one personality. Put together, they show how far Sam has travelled, and that distance is written in neither scene.' }
          ],
          teach: 'Because we see both versions of Sam almost at once, we do the measuring ourselves. The change is made by putting the scenes together, not by anything either scene says.' },
        { type: 'adds',
          q: 'What does the pairing add that neither scene contains on its own?',
          opts: [
            { t: 'A measure of change: Sam’s later line only means something next to the earlier one.', ok: true,
              e: 'a measure of change' },
            { t: 'More information about the rehearsal room and the way it is run.',
              e: 'information about the room',
              why: 'The room stays the same on purpose. It is the fixed thing that lets the audience see what has changed about Sam.' },
            { t: 'Nothing. Each scene already says everything it means.', m: true,
              e: 'nothing is added',
              why: '“Stand where you like” is an ordinary line. Only the pairing turns it into proof that Sam has become the person who once needed to hear it.' }
          ],
          teach: 'The repeated line carries no weight by itself. Hearing it twice, six years apart, lets the audience feel the whole change in one sentence.' },
        { type: 'cut',
          q: 'Where should the cut fall so that the change registers most strongly?',
          opts: [
            { t: 'On the repeated line, so that we hear the same words in the other mouth.', ok: true,
              e: 'cut on the repeated line' },
            { t: 'Right at the start, before either version of Sam has spoken.',
              e: 'cut at the very start',
              why: 'An early cut costs nothing, because neither scene has said anything yet for the other one to answer.' },
            { t: 'It makes no difference where the cut falls.', m: true,
              e: 'it makes no difference',
              why: 'It makes all the difference. Cut on the repeated line and the audience hears the echo. Cut anywhere else and the echo is simply missed.' }
          ],
          teach: 'Cutting on the repeated line lets us hear the same words twice, in two different mouths. The structure shows the change without one line of dialogue explaining it.' },
        { type: 'exam',
          q: 'Which sentence would earn marks in an answer about this structure?',
          opts: [
            { t: 'Cross-cutting puts the two versions of Sam side by side, so the audience measures the change itself.', ok: true,
              e: 'cross-cutting lets the audience measure the change' },
            { t: 'The play cross-cuts between Sam in the first week and Sam six years later.', m: true,
              e: 'the play cross-cuts between the two Sams',
              why: 'The technique is named and then dropped. Until you say what the pairing does to the audience, there is nothing for an examiner to credit.' },
            { t: 'Sam is nervous in the first scene and confident in the second.',
              e: 'Sam is nervous, then confident',
              why: 'This describes each scene separately, which is exactly the reading the structure is built to defeat. It also names no technique.' }
          ],
          teach: 'Technique first, then effect. “This juxtaposition creates … for the audience” is the clause that turns a named technique into a mark.' }
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
        ['cut', 'cut with the phone already in her hand —'],
        ['B', 'GRAN: Nobody rings this late. Good sign.'],
        ['cut', '— she says it as the call is on its way'],
        ['A', 'NURSE: Better they hear it tonight.']
      ],
      qs: [
        { type: 'effect',
          q: 'The two scenes are cut together. What does the front room feel like now?',
          opts: [
            { t: 'Every hopeful line feels like a countdown, because we know the call is coming.', ok: true,
              e: 'every hopeful line feels like a countdown' },
            { t: 'It becomes a surprise, because the audience finds out at the same time as Gran.',
              e: 'it becomes a surprise',
              why: 'A surprise needs the audience kept in the dark. Cross-cutting does the opposite on purpose: it tells us first, so we watch the news travel towards her.' },
            { t: 'Nothing changes. The front room is simply a hopeful scene.', m: true,
              e: 'nothing changes',
              why: 'The words are hopeful, but the meaning is not. “Good sign” only sounds hopeful if you have not just watched the nurse pick up the phone.' }
          ],
          teach: 'Nothing in the front room has changed except what we know while we watch it. Because we have seen the nurse dialling, Gran’s hope turns into dread for us.' },
        { type: 'adds',
          q: 'What does cutting between the scenes add that neither scene has on its own?',
          opts: [
            { t: 'A sense that it is inevitable: we know the two rooms are about to meet.', ok: true,
              e: 'a sense that it is inevitable' },
            { t: 'A tidy way of covering the time that the phone call takes.',
              e: 'a way of covering the time',
              why: 'Cutting between scenes can squeeze time, but that is stagecraft. Here it exists so that the audience holds both rooms in mind at once.' },
            { t: 'Nothing. One room has bad news and the other has hope, exactly as written.', m: true,
              e: 'nothing is added',
              why: 'Read apart, one room is sad and one is hopeful. Read together, the hopeful room becomes the painful one, and that change is on neither page.' }
          ],
          teach: 'Holding the two rooms together makes the ending feel inevitable. We are not waiting to find out what happens; we are waiting to watch it arrive.' },
        { type: 'cut',
          q: 'Where should the director cut so that the two rooms collide hardest?',
          opts: [
            { t: 'On “Good sign”, straight to the nurse dialling.', ok: true,
              e: 'cut on “Good sign”' },
            { t: 'After the nurse has finished making the call.',
              e: 'cut after the call is over',
              why: 'By then there is nothing left to dread. The tension lives in the gap between the nurse picking up the phone and the phone ringing in the front room.' },
            { t: 'Anywhere. The cut just moves us from one room to the other.', m: true,
              e: 'anywhere will do',
              why: 'Moving between rooms is the least of it. Land the cut on the most hopeful line and the audience feels the two rooms touch.' }
          ],
          teach: 'Cutting from Gran’s hope straight to the dialling puts both rooms in the same second. That overlap is the point: for a moment we are in both rooms at once.' },
        { type: 'exam',
          q: 'Which sentence would earn marks in an answer about this moment?',
          opts: [
            { t: 'Cutting from the nurse dialling to “Good sign” turns Gran’s hope into dread for the audience.', ok: true,
              e: 'the cut turns Gran’s hope into dread' },
            { t: 'The playwright cross-cuts between the ward office and the front room.', m: true,
              e: 'the playwright cross-cuts between the rooms',
              why: 'Spotting the technique is the easy half. Without saying what it does to the audience, the sentence stays at description and earns nothing.' },
            { t: 'Gran is hopeful, but the nurse has bad news to give her.',
              e: 'Gran is hopeful, the nurse is not',
              why: 'This is plot summary. It treats the two scenes as two separate reports, which is exactly what the structure refuses to let them be.' }
          ],
          teach: 'Name the cut, then name what it does to us. Technique plus audience effect is the sentence that scores.' }
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
        ['cut', 'cut on the claim, before it can settle —'],
        ['B', 'PARENT: Thursday is three days.'],
        ['cut', '— the shut door has answered the speech'],
        ['A', 'AIDE: Warmer on “its own”. Try it again.']
      ],
      qs: [
        { type: 'effect',
          q: 'The speech and the doorway are cut together. What does that do for an audience?',
          opts: [
            { t: 'We judge the speech against the shut door, so the speech sounds false.', ok: true,
              e: 'we judge the speech against the shut door' },
            { t: 'It feels balanced, because we see both sides and take neither.',
              e: 'it feels balanced',
              why: 'The two scenes are not weighted equally. One is being rehearsed and the other is actually happening, and an audience notices which is which.' },
            { t: 'Neither scene changes. A speech is a speech and a closed door is a closed door.', m: true,
              e: 'neither scene changes',
              why: 'On their own, the speech is warm and the shut door is bad luck. Together, the speech becomes a lie, and no line in either scene says so.' }
          ],
          teach: 'Because the claim and the evidence arrive almost together, the audience tests one against the other. That is irony: the audience works it out instead of being told.' },
        { type: 'adds',
          q: 'What does the pairing add that neither scene contains on its own?',
          opts: [
            { t: 'A judgement the audience reaches on its own, which neither scene states.', ok: true,
              e: 'a judgement the audience reaches itself' },
            { t: 'A change of location, so that the staging stays varied.',
              e: 'a change of location',
              why: 'Variety is decoration. If the second scene could be swapped for any other place, the structure is doing no work at all.' },
            { t: 'Nothing. Each scene means exactly what its own words mean.', m: true,
              e: 'nothing is added',
              why: '“Looks after its own” means one thing in a town hall and something else beside a shut door. The audience supplies that second meaning.' }
          ],
          teach: 'Neither scene calls the leader a hypocrite. The structure makes the audience decide it, which is why it lands harder than any speech could.' },
        { type: 'cut',
          q: 'Where should the director cut away from the speech?',
          opts: [
            { t: 'On “looks after its own”, so that the shut door answers it.', ok: true,
              e: 'cut on “looks after its own”' },
            { t: 'Once the speech has been rehearsed through twice.',
              e: 'cut after the speech is finished',
              why: 'Let the claim finish and the audience files it away as ordinary. The cut has to interrupt the claim for the door to feel like a reply.' },
            { t: 'Anywhere. The cut just signals that a new scene is starting.', m: true,
              e: 'anywhere will do',
              why: 'A cut placed on the boast makes the doorway answer it. Placed anywhere else, the two scenes are simply two scenes.' }
          ],
          teach: 'Cutting on the boast turns the shut door into the reply. The audience puts the claim and the answer together, and that is the structure doing the work.' },
        { type: 'exam',
          q: 'Which sentence would earn marks in an answer about this structure?',
          opts: [
            { t: 'Cutting from the rehearsed speech to the shut door lets the audience judge the claim.', ok: true,
              e: 'the cut lets the audience judge the claim' },
            { t: 'The playwright cross-cuts between the town hall and the shuttered doorway.', m: true,
              e: 'the playwright cross-cuts between the two places',
              why: 'The technique is named and then abandoned. Add what the audience experiences and the same observation becomes an argument.' },
            { t: 'The leader’s speech is not true for everybody in the town.',
              e: 'the speech is not true for everybody',
              why: 'That is your conclusion without the evidence. The mark is for showing how the structure made the audience reach it.' }
          ],
          teach: 'Technique, then effect. Naming cross-cutting and stopping there is the commonest way a good point scores nothing.' }
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
    '.svw-xcut .x-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem}',
    '.svw-xcut .x-scenes{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:.4rem}',
    '.svw-xcut .x-card{background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:.35rem .5rem}',
    '.svw-xcut .x-slug{font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880;margin-bottom:.22rem}',
    '.svw-xcut .x-line{font-size:.8rem;line-height:1.38;margin:0 0 .15rem}',
    '.svw-xcut .x-line:last-child{margin-bottom:0}',
    '.svw-xcut .x-strip{display:block}',
    '.svw-xcut .x-beat{display:flex;gap:.5rem;align-items:baseline;background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:.38rem .55rem}',
    '.svw-xcut .x-tag{font-size:.62rem;font-weight:700;letter-spacing:.06em;color:#8d8880;flex:0 0 auto}',
    '.svw-xcut .x-btext{font-size:.8rem;line-height:1.35;flex:1 1 auto}',
    '.svw-xcut .x-cutrow{display:flex;gap:.45rem;align-items:baseline;padding:.22rem .1rem .22rem .3rem}',
    '.svw-xcut .x-dot{flex:0 0 auto;width:6px;height:6px;border-radius:50%;background:var(--x-accent);transform:translateY(-1px)}',
    '.svw-xcut .x-cuttext{font-size:.74rem;line-height:1.3;color:#5b564e;font-style:italic;flex:1 1 auto}',
    '.svw-xcut .x-q{font-size:.84rem;font-weight:600;line-height:1.36;margin:.45rem 0 .3rem}',
    '.svw-xcut .x-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.3rem}',
    '.svw-xcut .x-opt{font:inherit;font-size:.8rem;line-height:1.32;text-align:left;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.36rem .5rem;cursor:pointer;width:100%}',
    '.svw-xcut .x-opt:hover{border-color:#c9c1b4}',
    '.svw-xcut .x-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-xcut .x-opt:disabled{cursor:default;opacity:.62}',
    '.svw-xcut .x-opt.is-answer:disabled{opacity:1;border-color:#4f7d63;background:#fff;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-xcut .x-opt.is-picked:disabled{opacity:1}',
    '.svw-xcut .x-act{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.45rem 0 0}',
    '.svw-xcut .x-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-xcut .x-go[disabled]{background:#faf8f5;color:#8d8880;border-color:#ddd7cd;cursor:default}',
    '.svw-xcut .x-cap{font-size:.82rem;line-height:1.5;color:#5b564e;margin:.42rem 0 0;min-height:1.5rem}',
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
        'Two scenes from a devised piece. The director will cut back and forth between them, instead of playing one and then the other.'));

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
      var go = el('button', 'x-go', 'See them cut together');
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

        go.textContent = 'See them cut together';
        go.disabled = true;
        setCap('Both scenes are already written. You choose the cut.');
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
                esc(opt.why || '') + ' The right answer was “' + esc(shortOf(answer)) + '”. ' +
                esc(item.teach);
        }
        if (justMastered) {
          msg += ' <b>Three in a row — you have it.</b> Cross-cutting is a structural choice: the audience holds both scenes in mind at once, and the meaning comes from the pair, not from either scene on its own.';
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
