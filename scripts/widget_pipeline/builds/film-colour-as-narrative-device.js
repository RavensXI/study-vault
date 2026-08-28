/* film-colour-as-narrative-device
   One abstract mock-frame — shapes standing for figure, light and ground —
   is re-graded live by the student. Each round states what a sequence in
   Skyfall has to do; the student picks the grade that does that job, then
   reads what their own choice tells an audience, and commits both before
   any verdict appears.

   One model does everything: a palette carries a fixed meaning (PAL[x].signal)
   and each round names which palette serves its need, so the reveal can never
   contradict the marking. The misconception — that colour is simply how a
   place happened to look — is a committable option in every round, whichever
   grade the student chooses.

   No stills and no photographs: the frame is a schematic, drawn in SVG and
   labelled as one. Self-contained; every selector scoped to .svw-fcol. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* ---- the model -------------------------------------------------------
     A palette means the same thing wherever it is used. That is the point
     the widget is making, so the same reading is offered in every round the
     palette appears in, and every verdict is derived from it. */
  var PAL = {
    ungraded: {
      name: 'Ungraded',
      c: { bg: '#d6cfc4', back: '#e6e0d5', key: '#f7f3ec', glow: '#ded7cb',
           fig: '#8d8377', floor: '#c6bfb3', rim: '#a79d90' }
    },
    neon: {
      name: 'Cold neon',
      c: { bg: '#06121a', back: '#0e2b39', key: '#3fd0cf', glow: '#17798a',
           fig: '#04090d', floor: '#08202b', rim: '#5fdcd6' },
      signal: 'The light comes from the city outside. Nobody in the room owns it or can turn it off.',
      echo: 'light nobody in the room can turn off'
    },
    tungsten: {
      name: 'Warm tungsten',
      c: { bg: '#1a1208', back: '#3d2c15', key: '#f4b75e', glow: '#a5722c',
           fig: '#120c05', floor: '#241809', rim: '#f9d08f' },
      signal: 'Somebody lives here and looks after the place. It is on your side.',
      echo: 'somewhere somebody lives'
    },
    daylight: {
      name: 'Flat daylight',
      c: { bg: '#c9ccce', back: '#e3e6e7', key: '#ffffff', glow: '#dcdfe1',
           fig: '#787d81', floor: '#b3b7ba', rim: '#a4a9ad' },
      signal: 'This is an ordinary place on an ordinary day, and you are shown every face and every corner.',
      echo: 'an ordinary place with nothing hidden'
    },
    gold: {
      name: 'Lantern gold',
      c: { bg: '#170d04', back: '#4d2e0c', key: '#f7c455', glow: '#bd7d1f',
           fig: '#0f0803', floor: '#2c1906', rim: '#ffdd85' },
      signal: 'This is what money looks like. The room is expensive, and it is lit to be shown off.',
      echo: 'what money looks like'
    },
    bluegrey: {
      name: 'Cold blue-grey',
      c: { bg: '#161b21', back: '#2c353e', key: '#8296a6', glow: '#47555f',
           fig: '#0d1115', floor: '#1d242b', rim: '#9fb3c2' },
      signal: 'This is an official place, full of offices and corridors, where you are kept at arm’s length.',
      echo: 'an official place'
    },
    slate: {
      name: 'Slate grey',
      c: { bg: '#343940', back: '#565059', key: '#8f9299', glow: '#666066',
           fig: '#20242a', floor: '#43484e', rim: '#a0a4aa' },
      signal: 'This is bare, open country, with nothing to hide behind and nobody to call for help.',
      echo: 'bare, open country'
    },
    highkey: {
      name: 'High-key white',
      c: { bg: '#e7e9eb', back: '#f5f6f7', key: '#ffffff', glow: '#edeff1',
           fig: '#969b9f', floor: '#dadce0', rim: '#bcc0c3' },
      signal: 'Everything here is clean, well funded and working properly.',
      echo: 'everything working properly'
    },
    fire: {
      name: 'Fire orange',
      c: { bg: '#07050a', back: '#1e0e06', key: '#ff7d21', glow: '#ad3f07',
           fig: '#050305', floor: '#160b05', rim: '#ffa14e' },
      signal: 'One fierce warm light in the dark, and the thing giving that warmth is destroying something.',
      echo: 'warmth from something being destroyed'
    }
  };

  /* Every round: a sequence from Skyfall, what it has to do, and the three
     grades on the table. Exactly one meets the need. Every grade carries a
     tempting misreading (dud) and the decoration misconception (mis), so
     both wrong pictures stay enterable whichever grade is committed. */
  var ROUNDS = [
    {
      id: 'shanghai',
      where: 'Shanghai · an empty glass tower, night',
      need: 'Bond follows a killer into a dark, empty tower, and they fight without saying a word. ' +
            'The shot has to keep both men as black outlines, so we watch the fight and not their faces.',
      key: { cx: 76, cy: 30, r: 25 }, band: { x: 22, w: 106 }, two: true,
      ok: 'neon',
      teach: 'The room lights are off. All the light comes from one huge advertising screen on the ' +
             'building outside, so we see outlines instead of faces. The light belongs to the city, ' +
             'not to Bond.',
      gs: [
        { p: 'neon',
          dud: { t: 'That the city is exciting and modern, so the fight looks stylish.',
                 e: 'just a stylish look',
                 why: 'The style is a side effect, not the reason. The blue does a job: it comes from outside, it belongs to the city, and it lets you see two bodies but no faces.' },
          mis: { t: 'Nothing in particular — the advert outside was blue, so the shots came out blue.',
                 e: 'nothing in particular',
                 why: 'The screen outside is something the film put there. Making it the only light in the room is the choice, and blue is what that choice looks like.' } },
        { p: 'tungsten',
          fail: 'Warm light would make the tower feel like somebody’s place. This scene needs a room that is on nobody’s side, so Bond has nothing to fall back on.',
          dud: { t: 'That violence is coming, because warm colours make you think of heat and blood.',
                 e: 'a sign that violence is coming',
                 why: 'Warm light usually means shelter, not danger. Think how a lit window looks when you are out in the cold. Nothing in this tower is meant to shelter anybody.' },
          mis: { t: 'Nothing in particular — an office at night just looks however its own lights make it look.',
                 e: 'nothing in particular',
                 why: 'The office was built and lit for the camera. Somebody decided to switch the room lights off and let one screen outside do all the lighting.' } },
        { p: 'daylight',
          fail: 'Flat daylight shows you everything. This fight works because you are shown almost nothing: two black outlines against a bright screen.',
          dud: { t: 'That the audience is meant to feel safe, because bright light means nothing bad can happen.',
                 e: 'a sign the audience should feel safe',
                 why: 'Even light does not make a scene safe. It only makes it clear. Seeing clearly is the problem here: you would get both faces, and the fight would lose what makes it work.' },
          mis: { t: 'Nothing in particular — this is simply what a camera records in a normal room.',
                 e: 'nothing in particular',
                 why: 'A camera records whatever it is given. Flat, even light has to be set up just like any other look, so it is a choice too.' } }
      ]
    },

    {
      id: 'macau',
      where: 'Macau · the floating casino, night',
      need: 'Bond walks into a floating casino. Money decides everything here, and none of his usual ' +
            'authority counts. The shot has to show that before anyone explains where he is.',
      key: { cx: 166, cy: 26, r: 20 }, band: null, two: false,
      ok: 'gold',
      teach: 'The gold explains the room before anybody speaks. It tells us this place was built to be ' +
             'looked at, that it runs on money, and that there is nothing here Bond can appeal to.',
      gs: [
        { p: 'gold',
          dud: { t: 'That the room is friendly, because gold is warm and warm means welcoming.',
                 e: 'a sign the room is friendly',
                 why: 'The gold here is for showing off, not for welcoming you. The room is warm the way a shop window is warm: lit so that you want what is inside.' },
          mis: { t: 'Nothing in particular — the casino was full of gold lanterns, so the shots came out gold.',
                 e: 'nothing in particular',
                 why: 'Somebody chose to fill the room with gold lanterns, and the colour work pushes that gold further. What a room contains is decided long before the camera arrives.' } },
        { p: 'bluegrey',
          fail: 'Cold blue-grey is the colour this film gives to offices. In the casino it would make the room look like somewhere with rules, and this is a place with none.',
          dud: { t: 'That danger is close, because cold colours are how films signal a threat.',
                 e: 'a sign that danger is close',
                 why: 'Not always. This film uses the same blue-grey for MI6 down in the tunnels, and there it means beaten down, not dangerous. What a colour means depends on what it is put next to.' },
          mis: { t: 'Nothing in particular — it would just be a cooler-looking version of the same room.',
                 e: 'nothing in particular',
                 why: 'A cooler room is a different room. Take the gold away and the casino stops looking like money’s own ground.' } },
        { p: 'neon',
          fail: 'Neon is street light: public, electric and free to anyone walking past. This room has to feel private, closed off and paid for.',
          dud: { t: 'That the casino is glamorous, because neon is the colour of nightlife.',
                 e: 'a sign the casino is glamorous',
                 why: 'Neon is public glamour, out in the street, free for anyone to look at. The casino’s gold is private and paid for, and that difference is what the room is about.' },
          mis: { t: 'Nothing in particular — Macau is a neon city, so a neon look would just be accurate.',
                 e: 'nothing in particular',
                 why: 'Being true to life is not what colour is for. A neon casino would match the streets outside and still tell us the wrong thing about the room.' } }
      ]
    },

    {
      id: 'tunnel',
      where: 'London · MI6 working from a tunnel',
      need: 'MI6 has been bombed out of its building. It now runs the whole service from an old tunnel. ' +
            'The shot has to show an organisation cut down to bare brick walls.',
      key: { cx: 118, cy: 16, r: 23 }, band: null, two: true,
      ok: 'bluegrey',
      teach: 'The colour tells you the plot. MI6 has lost its building, its list of agents and its ' +
             'reputation, and you learn all three from walls you can barely see and light nobody ' +
             'would choose to work in.',
      gs: [
        { p: 'bluegrey',
          dud: { t: 'That MI6 is more secretive now, because dim light hides what people are doing.',
                 e: 'a sign MI6 is being secretive',
                 why: 'Secrets in this film are kept by how much of a face you are allowed to see, not by how cold the walls are. The tunnels are not hiding anything.' },
          mis: { t: 'Nothing in particular — a tunnel is cold and grey whether anybody plans it or not.',
                 e: 'nothing in particular',
                 why: 'A tunnel can be lit any way the crew chooses. A few warm lamps would make the same brick look like a safe shelter instead of a step down in the world.' } },
        { p: 'gold',
          fail: 'Warm gold makes a place feel safe. Use it here and moving underground would look like coming home, when it has to feel like a service driven into a hole.',
          dud: { t: 'That the service is old and traditional, because gold looks historic.',
                 e: 'a sign the service is old and traditional',
                 why: 'Gold makes us think of money before it makes us think of age. It would make the tunnels look like a private club with plenty of funding, when the funding and the building have both gone.' },
          mis: { t: 'Nothing in particular — the tunnels are old, so warm old lighting would just suit them.',
                 e: 'nothing in particular',
                 why: 'Matching the location is not the job. The tunnels could be lit warm or cold, and whichever you pick is what the audience will believe about MI6.' } },
        { p: 'highkey',
          fail: 'Bright white light says everything is running properly. This scene is about a service that has stopped, so that light would contradict the story.',
          dud: { t: 'That the scene is tense, because hard white light feels cold and clinical.',
                 e: 'a sign the scene is tense',
                 why: 'Hard white light suits a laboratory or a police interview, where everything is visible and under control. This scene is about losing control.' },
          mis: { t: 'Nothing in particular — you have to light a dark tunnel somehow so people can see.',
                 e: 'nothing in particular',
                 why: 'A dark tunnel has to be lit somehow, and how much light you give it is the decision. This film gives just enough to follow the scene.' } }
      ]
    },

    {
      id: 'moor',
      where: 'Scotland · the road to Skyfall Lodge',
      need: 'Bond drives M north to the house he grew up in. They have no back-up and nothing but an old ' +
            'car. The shot has to strip the film back to two people in open country.',
      key: { cx: 120, cy: 18, r: 44 }, band: null, two: true,
      ok: 'slate',
      teach: 'The colour takes the Bond film apart. The cities, the gadgets and the service have all ' +
             'gone. The colours drop to wet slate and dead heather, and all that is left is two people ' +
             'with no help coming.',
      gs: [
        { p: 'slate',
          dud: { t: 'That the scene is sad, because grey is a sad colour.',
                 e: 'a sign the scene is sad',
                 why: 'The grey is not there to make you feel sad. It shows what Bond has left: the gadgets, the cities and the service have all gone, and what remains is a cold house and two people.' },
          mis: { t: 'Nothing in particular — Scotland in bad weather is grey, so the shots came out grey.',
                 e: 'nothing in particular',
                 why: 'Plenty of films have made the same Scottish moor look golden. A crew chooses which weather to wait for and which colours to push, and this one turns down every warm option.' } },
        { p: 'tungsten',
          fail: 'Warm light would promise a happy homecoming. Bond is going back to an empty house, so warmth would tell us the wrong thing about what is waiting.',
          dud: { t: 'That the family who own the house are kind, so we are ready to like them.',
                 e: 'a sign the family are kind',
                 why: 'There is no family left in the house. Warm light would promise a welcome that nobody is there to give, and the story needs Bond arriving somewhere emptied out.' },
          mis: { t: 'Nothing in particular — sunlight over a moor is warm, so a warm look is just realistic.',
                 e: 'nothing in particular',
                 why: 'Being realistic is not what colour is for. This film keeps every warm colour off the moor until the moment the house catches fire.' } },
        { p: 'highkey',
          fail: 'Bright white light would make the country look easy to handle. This scene needs the opposite: two people with nowhere to hide, in weather that does not care.',
          dud: { t: 'That the moor is beautiful, so the audience gets a break before the fight.',
                 e: 'a beautiful break before the fight',
                 why: 'It is beautiful either way. Bright, even light would make the moor look welcoming, and the whole point of this landscape is that it will not help him.' },
          mis: { t: 'Nothing in particular — you light a landscape so the audience can see it, and that is all.',
                 e: 'nothing in particular',
                 why: 'How much light you use, and how cold it is, are both decisions. The same moor can be made to look like a nice day out or a place you have to survive.' } }
      ]
    },

    {
      id: 'burning',
      where: 'Skyfall Lodge · the house burns',
      need: 'The house Bond grew up in burns while the fight goes on in front of it. The whole ending ' +
            'has been cold and grey. Now one warm thing, the fire, has to feel like a loss.',
      key: { cx: 88, cy: 46, r: 32 }, band: null, two: true,
      ok: 'fire',
      teach: 'What matters is the change. The film has spent hours on cold neon, office blue and wet ' +
             'slate. So when one orange light finally arrives, the only warm thing left is the fire ' +
             'burning Bond’s childhood home.',
      gs: [
        { p: 'fire',
          dud: { t: 'That the sequence is exciting, because fire and explosions look spectacular.',
                 e: 'just a spectacular fire',
                 why: 'It is spectacular, but that is only the surface. This is the one warm light in the whole ending, and the thing giving that warmth is Bond’s home burning down.' },
          mis: { t: 'Nothing in particular — a burning house is orange, so the shots came out orange.',
                 e: 'nothing in particular',
                 why: 'The fire really is orange. The decision is to let it fill the whole frame and keep everything else black, after holding warm colour back for the entire ending.' } },
        { p: 'bluegrey',
          fail: 'Cold blue-grey is what this film uses for offices. Nothing about this night is office business, and it would wipe out the one moment the colour finally changes.',
          dud: { t: 'That the night is cold, which is honest for a Scottish moor in winter.',
                 e: 'just a cold, realistic night',
                 why: 'Being honest about the weather is not what the shot is for. The ending has already been cold all the way through. The fire is where that stops, and the change is the point.' },
          mis: { t: 'Nothing in particular — night scenes are blue, and this is a night scene.',
                 e: 'nothing in particular',
                 why: 'Night looks blue in films because films decided long ago to make it blue. Here the film breaks its own habit.' } },
        { p: 'highkey',
          fail: 'Bright white light would come from nowhere. The fire has to be the only light, so the thing destroying the house is also the only thing letting us see.',
          dud: { t: 'That the danger is clear, because you can see everything that is happening.',
                 e: 'a way of showing everything',
                 why: 'You would, and that is the problem. The fire shows you the fight in pieces: a shape, a face, then darkness again. Flat light would show you all of it at once.' },
          mis: { t: 'Nothing in particular — you have to light a night scene somehow.',
                 e: 'nothing in particular',
                 why: 'A night scene has to be lit somehow, and there were many ways to do it. Somebody chose this one, and that choice is the grade.' } }
      ]
    }
  ];

  var CSS = [
'.svw-fcol{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4;-webkit-text-size-adjust:100%}',
'.svw-fcol *{box-sizing:border-box}',
'.svw-fcol p{margin:0}',
'.svw-fcol .f-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--f-acc);margin:0 0 .16rem}',
'.svw-fcol .f-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.16;margin:0 0 .3rem}',
'.svw-fcol .f-need{font-size:.8rem;line-height:1.44;color:#5b564e;margin:0 0 .48rem}',
'.svw-fcol .f-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.45rem;margin:0 0 .48rem}',
'.svw-fcol .f-where{font-size:.66rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--f-acc);margin:0 0 .26rem}',
'.svw-fcol .f-shot{display:block;width:100%;max-width:420px;height:auto;margin:0 auto;border-radius:6px}',
'.svw-fcol .f-note{font-size:.68rem;line-height:1.34;color:#8d8880;margin:.26rem 0 0;text-align:center}',
'.svw-fcol .f-map{display:none;font-size:.78rem;line-height:1.4;margin:.3rem 0 0;padding-top:.3rem;border-top:1px solid #e8e2d9}',
'.svw-fcol .f-map.on{display:block}',
'.svw-fcol .f-mname{font-weight:700}',
'.svw-fcol .f-ask{display:block}',
'.svw-fcol .f-ask.off{display:none}',
'.svw-fcol .f-gh{display:flex;align-items:center;gap:.4rem;font-size:.78rem;font-weight:600;line-height:1.3;margin:0 0 .26rem}',
'.svw-fcol .f-chip{flex:0 0 auto;width:1.12rem;height:1.12rem;border-radius:50%;background:var(--f-acc);color:#fff;font-size:.66rem;font-weight:700;display:flex;align-items:center;justify-content:center}',
'.svw-fcol .f-gh.sleep{color:#a9a39a}',
'.svw-fcol .f-gh.sleep .f-chip{background:#ddd7cd}',
'.svw-fcol .f-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:.3rem;margin:0 0 .4rem}',
'.svw-fcol .f-tile{font:inherit;font-size:.72rem;font-weight:600;line-height:1.24;color:#2d2a26;background:#fff;border:1px solid #ddd7cd;border-radius:10px;padding:.3rem;cursor:pointer;text-align:center}',
'.svw-fcol .f-tile[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-fcol .f-sw{display:flex;height:9px;border:1px solid #e8e2d9;border-radius:3px;overflow:hidden;margin:0 0 .24rem}',
'.svw-fcol .f-sw i{flex:1 1 0;display:block}',
'.svw-fcol .f-opts{display:flex;flex-direction:column;gap:.26rem}',
'.svw-fcol .f-opts.off{display:none}',
'.svw-fcol .f-opt{font:inherit;font-size:.78rem;line-height:1.32;font-weight:500;text-align:left;color:#2d2a26;background:#fff;border:1px solid #ddd7cd;border-radius:10px;padding:.34rem .55rem;cursor:pointer;width:100%}',
'.svw-fcol .f-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-fcol .f-opt[disabled]{cursor:default;color:#a9a39a;background:#faf8f5}',
'.svw-fcol .f-fb{display:none}',
'.svw-fcol .f-fb.on{display:block}',
'.svw-fcol .f-flag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 .14rem}',
'.svw-fcol .f-flag.ok{color:#4f7d63}',
'.svw-fcol .f-flag.no{color:#5b564e}',
'.svw-fcol .f-say{font-size:.8rem;line-height:1.45;margin:0}',
'.svw-fcol .f-act{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin-top:.46rem}',
'.svw-fcol .f-run{font-size:.75rem;line-height:1.35;color:#5b564e}',
'.svw-fcol .f-go{flex:0 0 auto;font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.46rem .95rem;cursor:pointer}',
'.svw-fcol .f-go[disabled]{background:#faf8f5;color:#a9a39a;border-color:#ddd7cd;cursor:default}',
'.svw-fcol .f-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
'.svw-fcol.f-anim .f-shot rect,.svw-fcol.f-anim .f-shot circle,.svw-fcol.f-anim .f-shot path{transition:fill .3s cubic-bezier(.16,1,.3,1)}'
  ].join('\n');

  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag), k;
    for (k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]); }
    return n;
  }

  /* One human shape: head plus torso, feet on the local origin. Drawn twice
     per figure — once offset towards the key light in the rim colour, once
     over it in the silhouette colour — which is how a backlit body reads. */
  var BODY = 'M-6.4 0 L-5.2 -17 L-8.6 -25.5 L-4 -28.6 L4 -28.6 L8.6 -25.5 L5.2 -17 L6.4 0 Z';

  function figureGroup(baseX) {
    var g = sv('g', {});
    var rimG = sv('g', { transform: 'translate(1.6 -1)' });
    var rimHead = sv('circle', { cx: 0, cy: -33, r: 5 });
    var rimBody = sv('path', { d: BODY });
    rimG.appendChild(rimHead); rimG.appendChild(rimBody);
    var head = sv('circle', { cx: 0, cy: -33, r: 5 });
    var body = sv('path', { d: BODY });
    g.appendChild(rimG);
    g.appendChild(head); g.appendChild(body);
    return { g: g, rimG: rimG, x: baseX, rim: [rimHead, rimBody], fig: [head, body] };
  }

  function lower(s) { return s.charAt(0).toLowerCase() + s.slice(1); }

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
    var reduced = !!ctx.reducedMotion;

    var wrap = document.createElement('div');
    wrap.className = 'svw-fcol' + (reduced ? '' : ' f-anim');
    wrap.style.setProperty('--f-acc', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    wrap.insertAdjacentHTML('beforeend',
      '<p class="f-kick">Cinematography</p>' +
      '<p class="f-title">Grade the shot</p>' +
      '<p class="f-need" id="fneed"></p>' +
      '<div class="f-stage">' +
        '<p class="f-where" id="fwhere"></p>' +
        '<div id="fshot"></div>' +
        '<p class="f-note">A diagram, not a still: the shapes stand for a person, a light and the ground.</p>' +
        '<p class="f-map" id="fmap"><span class="f-mname" id="fmname"></span><span id="fmsig"></span></p>' +
      '</div>' +
      '<div class="f-ask" id="fask">' +
        '<p class="f-gh" id="fgh1"><span class="f-chip">1</span><span>Grade the shot.</span></p>' +
        '<div class="f-tiles" id="ftiles" role="group" aria-label="Grade the shot"></div>' +
        '<p class="f-gh sleep" id="fgh2"><span class="f-chip">2</span><span>What would an audience take from it?</span></p>' +
        '<div class="f-opts" id="fopts" role="group" aria-label="What would an audience take from it"></div>' +
      '</div>' +
      '<div class="f-fb" id="ffb"><span class="f-flag" id="fflag"></span><p class="f-say" id="fsay"></p></div>' +
      '<div class="f-act"><p class="f-run" id="frun"></p>' +
        '<button type="button" class="f-go" id="fgo" disabled>Check</button></div>' +
      '<p class="f-sr" id="fsr" aria-live="polite"></p>');

    root.appendChild(wrap);

    var elNeed  = wrap.querySelector('#fneed');
    var elWhere = wrap.querySelector('#fwhere');
    var elMap   = wrap.querySelector('#fmap');
    var elMName = wrap.querySelector('#fmname');
    var elMSig  = wrap.querySelector('#fmsig');
    var elAsk   = wrap.querySelector('#fask');
    var elGh2   = wrap.querySelector('#fgh2');
    var elOpts  = wrap.querySelector('#fopts');
    var elFb    = wrap.querySelector('#ffb');
    var elFlag  = wrap.querySelector('#fflag');
    var elSay   = wrap.querySelector('#fsay');
    var elRun   = wrap.querySelector('#frun');
    var elGo    = wrap.querySelector('#fgo');
    var elSr    = wrap.querySelector('#fsr');

    /* ---- the frame, built once and repainted ---------------------------- */
    var svg = sv('svg', {
      'class': 'f-shot', viewBox: '0 0 239 100',
      role: 'img', 'aria-label': 'Diagram of a shot: two figures, a light source and the ground'
    });
    var pBg    = sv('rect', { x: 0, y: 0, width: 239, height: 100 });
    var pBack  = sv('rect', { x: 0, y: 0, width: 239, height: 70 });
    var pBand  = sv('rect', { x: 0, y: 4, width: 1, height: 62, opacity: '.5' });
    var pHalo  = sv('circle', { cx: 0, cy: 0, r: 1, opacity: '.55' });
    var pKey   = sv('circle', { cx: 0, cy: 0, r: 1, opacity: '.92' });
    var pFloor = sv('rect', { x: 0, y: 70, width: 239, height: 30 });
    var pHoriz = sv('rect', { x: 0, y: 69.4, width: 239, height: 1.1, opacity: '.4' });
    var figA = figureGroup(152), figB = figureGroup(52);
    figA.g.setAttribute('transform', 'translate(152 79)');
    figB.g.setAttribute('transform', 'translate(52 77) scale(.78)');
    [pBg, pBack, pBand, pHalo, pKey, pFloor, pHoriz, figB.g, figA.g]
      .forEach(function (n) { svg.appendChild(n); });
    wrap.querySelector('#fshot').appendChild(svg);

    function paint(id) {
      var c = PAL[id].c;
      pBg.setAttribute('fill', c.bg);
      pBack.setAttribute('fill', c.back);
      pBand.setAttribute('fill', c.glow);
      pHalo.setAttribute('fill', c.glow);
      pKey.setAttribute('fill', c.key);
      pFloor.setAttribute('fill', c.floor);
      pHoriz.setAttribute('fill', c.key);
      [figA, figB].forEach(function (f) {
        f.rim.forEach(function (n) { n.setAttribute('fill', c.rim); });
        f.fig.forEach(function (n) { n.setAttribute('fill', c.fig); });
      });
    }

    /* ---- controls, built once ------------------------------------------ */
    var tiles = [], swatches = [], names = [], i, j, b, sw, nm, seg, segs;
    for (i = 0; i < 3; i++) {
      b = document.createElement('button');
      b.type = 'button';
      b.className = 'f-tile';
      b.setAttribute('aria-pressed', 'false');
      sw = document.createElement('span');
      sw.className = 'f-sw';
      segs = [];
      for (j = 0; j < 3; j++) { seg = document.createElement('i'); sw.appendChild(seg); segs.push(seg); }
      nm = document.createElement('span');
      b.appendChild(sw); b.appendChild(nm);
      b.addEventListener('click', onGrade);
      wrap.querySelector('#ftiles').appendChild(b);
      tiles.push(b); swatches.push(segs); names.push(nm);
    }

    var opts = [];
    for (i = 0; i < 3; i++) {
      b = document.createElement('button');
      b.type = 'button';
      b.className = 'f-opt';
      b.disabled = true;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', onRead);
      wrap.querySelector('#fopts').appendChild(b);
      opts.push(b);
    }

    /* ---- state ---------------------------------------------------------- */
    var state = { streak: 0, mastered: false, attempted: 0 };
    var order = [], cursor = 0, round = null;
    var gShown = [], rShown = [], gPick = -1, rPick = -1, revealed = false;

    function shuffle(a) {
      for (var k = a.length - 1; k > 0; k--) {
        var m = Math.floor(Math.random() * (k + 1)), t = a[k]; a[k] = a[m]; a[m] = t;
      }
      return a;
    }

    function nextRound() {
      if (cursor >= order.length) {
        var last = order.length ? order[order.length - 1] : -1;
        order = shuffle(ROUNDS.map(function (_, n) { return n; }));
        if (order[0] === last && order.length > 1) {
          var s = order[0]; order[0] = order[1]; order[1] = s;
        }
        cursor = 0;
      }
      round = ROUNDS[order[cursor++]];
      gShown = shuffle(round.gs.slice());
      gPick = -1; rPick = -1; revealed = false;

      elNeed.textContent = round.need;
      elWhere.textContent = round.where;

      pBand.setAttribute('x', round.band ? round.band.x : 0);
      pBand.setAttribute('width', round.band ? round.band.w : 0);
      pHalo.setAttribute('cx', round.key.cx);
      pHalo.setAttribute('cy', round.key.cy);
      pHalo.setAttribute('r', Math.round(round.key.r * 1.75));
      pKey.setAttribute('cx', round.key.cx);
      pKey.setAttribute('cy', round.key.cy);
      pKey.setAttribute('r', round.key.r);
      figB.g.setAttribute('opacity', round.two ? '1' : '0');
      /* the rim falls on the side the key light is actually on */
      [figA, figB].forEach(function (f) {
        f.rimG.setAttribute('transform',
          'translate(' + (f.x < round.key.cx ? 1.6 : -1.6) + ' -1)');
      });
      paint('ungraded');

      for (var n = 0; n < 3; n++) {
        var pal = PAL[gShown[n].p];
        names[n].textContent = pal.name;
        swatches[n][0].style.background = pal.c.back;
        swatches[n][1].style.background = pal.c.key;
        swatches[n][2].style.background = pal.c.floor;
        tiles[n].setAttribute('aria-pressed', 'false');
        opts[n].setAttribute('aria-pressed', 'false');
        opts[n].disabled = true;
        opts[n].textContent = '';
      }
      elGh2.className = 'f-gh sleep';
      elOpts.classList.add('off');   /* no empty pills before a grade is set */
      elMap.classList.remove('on');
      elAsk.classList.remove('off');
      elFb.classList.remove('on');
      elGo.textContent = 'Check';
      elGo.disabled = true;
      publish();
    }

    /* Part two is always about the grade the student has just chosen, so the
       question never leaks whether that choice was the right one — and the
       misconception is on the table whichever grade they took. */
    function loadReadings() {
      var g = gShown[gPick], pal = PAL[g.p];
      rShown = shuffle([
        { kind: 'signal', t: pal.signal, e: pal.echo },
        { kind: 'dud', t: g.dud.t, e: g.dud.e, why: g.dud.why },
        { kind: 'mis', t: g.mis.t, e: g.mis.e, why: g.mis.why }
      ]);
      for (var n = 0; n < 3; n++) {
        opts[n].textContent = rShown[n].t;
        opts[n].disabled = false;
        opts[n].setAttribute('aria-pressed', 'false');
      }
      elOpts.classList.remove('off');
    }

    function onGrade(ev) {
      if (revealed) return;
      var btn = ev.currentTarget, was = gPick;
      gPick = tiles.indexOf(btn);
      for (var n = 0; n < 3; n++) {
        tiles[n].setAttribute('aria-pressed', tiles[n] === btn ? 'true' : 'false');
      }
      paint(gShown[gPick].p);
      if (gPick !== was) { rPick = -1; loadReadings(); }
      elGh2.className = 'f-gh';
      elGo.disabled = (rPick < 0);
      publish();
    }

    function onRead(ev) {
      if (revealed || gPick < 0) return;
      var btn = ev.currentTarget;
      rPick = opts.indexOf(btn);
      for (var n = 0; n < 3; n++) {
        opts[n].setAttribute('aria-pressed', opts[n] === btn ? 'true' : 'false');
      }
      elGo.disabled = false;
      publish();
    }

    function clearPicks() {
      gPick = -1; rPick = -1;
      for (var n = 0; n < 3; n++) {
        tiles[n].setAttribute('aria-pressed', 'false');
        opts[n].setAttribute('aria-pressed', 'false');
        opts[n].disabled = true;
        opts[n].textContent = '';
      }
      elGh2.className = 'f-gh sleep';
      elOpts.classList.add('off');
      paint('ungraded');
      elGo.disabled = true;
      publish();
    }

    function reveal() {
      revealed = true;
      state.attempted++;
      var g = gShown[gPick], pal = PAL[g.p], read = rShown[rPick];
      var gradeOk = (g.p === round.ok), readOk = (read.kind === 'signal');
      var right = gradeOk && readOk;
      var okPal = PAL[round.ok];

      if (right) { state.streak++; if (state.streak >= 3) state.mastered = true; }
      else { state.streak = 0; }

      /* One clause, chosen by the bigger error. A wrong reading of the right
         grade is corrected on its own terms; a wrong grade is corrected first,
         and the misconception always gets its own answer. */
      var body;
      if (right) {
        body = round.teach;
      } else if (gradeOk) {
        body = read.why + ' ' + pal.name + ' is telling the audience: ' + lower(pal.signal);
      } else if (readOk) {
        body = 'You read that colour correctly, and that is exactly why it does not work for this scene. ' + g.fail;
      } else if (read.kind === 'mis') {
        body = read.why + ' ' + g.fail;
      } else {
        body = g.fail + ' And ' + pal.name.toLowerCase() + ' does not say that. What it does say is: ' + lower(pal.signal);
      }

      elFlag.textContent = right ? 'Right' : 'Not quite';
      elFlag.className = 'f-flag ' + (right ? 'ok' : 'no');
      elSay.textContent = '— you graded it ' + pal.name.toLowerCase() + ' and read it as ' +
        read.e + '. ' + body +
        (right && state.streak === 3
          ? ' You have it: colour is an argument about what a scene means, not a record of how the place looked.'
          : '');

      /* The round ends in the grade the film uses, so the palette and its
         reading are shown together and cannot drift apart. */
      paint(round.ok);
      elMName.textContent = 'Graded ' + okPal.name.toLowerCase() + ': ';
      elMSig.textContent = lower(okPal.signal);
      elMap.classList.add('on');
      elAsk.classList.add('off');
      elFb.classList.add('on');

      if (state.streak >= 3) {
        elRun.textContent = 'Three in a row — you have it.';
        elGo.textContent = 'Another anyway';
      } else if (right) {
        elRun.textContent = state.streak === 1
          ? '1 right in a row — two more.'
          : '2 right in a row — one more.';
        elGo.textContent = 'Next scene';
      } else {
        elRun.textContent = state.attempted > 1 ? 'Run back to nought.' : '';
        elGo.textContent = 'Next scene';
      }
      elSr.textContent = (right ? 'Right. ' : 'Not quite. ') + elSay.textContent;
      publish();
    }

    elGo.addEventListener('click', function () {
      if (!revealed) {
        if (gPick < 0 || rPick < 0) return;
        reveal();
      } else {
        nextRound();
      }
      elGo.focus();
    });

    wrap.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !revealed && (gPick >= 0 || rPick >= 0)) clearPicks();
    });

    function publish() {
      root.dataset.svState = JSON.stringify({
        scene: round ? round.id : null,
        answer: round ? round.ok : null,
        grade: gPick >= 0 ? gShown[gPick].p : null,
        gradeOk: gPick < 0 ? null : (gShown[gPick].p === round.ok),
        reading: rPick >= 0 ? rShown[rPick].kind : null,
        revealed: revealed,
        streak: state.streak,
        mastered: state.mastered,
        attempted: state.attempted
      });
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: 'film-colour-as-narrative-device',
      title: 'Grade the shot',
      teaches: 'The colour of a shot is a storytelling choice, not a record of how the place happened to ' +
               'look. Each palette makes a claim about where we are and what we should feel, so the ' +
               'same shapes mean different things under different colours.'
    },
    mount: mount
  };
})();
