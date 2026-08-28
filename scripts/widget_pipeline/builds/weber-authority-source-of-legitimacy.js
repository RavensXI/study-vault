/* ============================================================
   weber-authority-source-of-legitimacy — "Obeyed — but on what grounds?"

   The student never picks a type NAME. They pick (1) the reason the
   obedience holds and (2) what happens to it when the person is gone.
   The widget then names what Weber called it. So the round cannot be
   answered by pattern-matching a personality trait onto a label
   ("charismatic = popular"): the only way through is the source of
   legitimacy, tested twice — once directly, once by succession.

   Every case is an original, neutral situation in which the person
   being obeyed has NO force available, so "they are forced" is
   committable in every round and is falsified by the case's own
   detail rather than by assertion.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- the model -------------------------------------------- */

  var TYPES = {
    trad:  { name: 'traditional',    succ: 'custom' },
    char:  { name: 'charismatic',    succ: 'person' },
    legal: { name: 'rational-legal', succ: 'post' }
  };

  var REASONS = [
    { key: 'trad',  label: 'It has always been done this way.',
      echo: 'it has always been done this way' },
    { key: 'char',  label: 'This person is extraordinary.',
      echo: 'this person is extraordinary' },
    { key: 'legal', label: 'The rules give the post the right.',
      echo: 'the rules give the post the right' },
    { key: 'force', label: 'They have no choice — they are forced.',
      echo: 'they are forced' }
  ];

  var SUCCS = [
    { key: 'custom', label: '…passes to the next in line, by custom.',
      echo: 'it passes to the next in line by custom' },
    { key: 'person', label: '…goes with them. Nothing to hand on.',
      echo: 'it goes with them' },
    { key: 'post',   label: '…passes to whoever holds the post next.',
      echo: 'it passes to whoever holds the post next' }
  ];

  var R = {}, S = {};
  REASONS.forEach(function (o) { R[o.key] = o; });
  SUCCS.forEach(function (o) { S[o.key] = o; });

  var SUCCWHY = {
    legal: 'The office outlives whoever fills it, which is what makes this kind of authority stable.',
    trad:  'The grounds are handed down with the position, so custom carries it across.',
    char:  'Weber called the struggle to keep it going after the founder routinisation — with no post to hand on, the next person must win it from scratch.'
  };

  /* Original cases. In every one the person has nothing to force with. */
  var CASES = [
    { id: 'supply', type: 'legal',
      text: 'A supply teacher nobody has met takes the register in a hall of Year 11. She knows not one name and has no sanction here. Every student answers.',
      subj: 'The supply teacher',
      noforce: 'she knows nobody and has no sanction to use',
      why: 'Weber argued the hall is answering the post, not the woman.',
      gone: 'the next teacher handed that register is answered the same way',
      no: { trad: 'nobody in that hall has seen her before, so no custom points at her',
            char: 'they know nothing about her at all — she could be anyone' } },

    { id: 'show', type: 'trad',
      text: 'One family has judged the village show vegetables for a hundred years. This year it is the grandson, who grows nothing. Growers take his verdict.',
      subj: 'The grandson',
      noforce: 'there is no prize money and nothing lost by walking away',
      why: 'Weber argued the grounds are the custom itself: it has been this family, so it stays this family.',
      gone: 'his own son will judge on exactly the same grounds',
      no: { char: 'the grandson has grown nothing and nobody calls him remarkable',
            legal: 'there is no committee and no post he was appointed to' } },

    { id: 'climate', type: 'char',
      text: 'A Year 12 student set up the lunchtime climate group. She holds no post, gives no orders and can make nobody come. Thirty turn up for her each week.',
      subj: 'The Year 12 student',
      noforce: 'she gives no orders and can make nobody come',
      why: 'Weber argued the claim rests on the person: they follow her because they find her out of the ordinary.',
      gone: 'the next student who stands up has to win the room from nothing',
      no: { trad: 'the group started this term, so there is no custom to lean on',
            legal: 'she holds no post, so no rule can be handing her the right' } },

    { id: 'ref', type: 'legal',
      text: 'A referee takes a park league match. No crowd, no camera, nobody to report a player to, and the men are twice her size. She sends one off; he walks.',
      subj: 'The referee',
      noforce: 'she is outsized, unwatched and has nobody to report him to',
      why: 'Weber argued the laws of the game give whoever holds the whistle the right to decide.',
      gone: 'next week’s referee sends players off with the same right',
      no: { trad: 'she is new to the league and no custom points at her',
            char: 'nothing here is personal to her — she is unknown and outsized' } },

    { id: 'firm', type: 'trad',
      text: 'The founder’s granddaughter runs the family firm. The job was never advertised and a manager sets the pay. Staff say she is no sharper, but do as she asks.',
      subj: 'The granddaughter',
      noforce: 'a manager sets the pay, so she holds nothing over them',
      why: 'Weber argued she is obeyed as the founder’s line, not as the best candidate.',
      gone: 'her own daughter will be asked next, on the same grounds',
      no: { char: 'the staff say plainly that she is no sharper than they are',
            legal: 'no rule hands her the say and the job was never advertised' } },

    { id: 'coach', type: 'char',
      text: 'A volunteer took over the Sunday football sessions; six players became sixty in a year. He holds no badge and no contract. The players come for him.',
      subj: 'The volunteer',
      noforce: 'he holds no contract and nothing at all over anybody',
      why: 'Weber argued the grounds are the man himself, and nothing else.',
      gone: 'a replacement inherits the pitch and the kit, but not the sixty players',
      no: { trad: 'the sessions are one year old, so no custom has formed',
            legal: 'he holds no badge, no contract and no post' } },

    { id: 'clerk', type: 'legal',
      text: 'A polling clerk hands out ballot papers and sends each voter to a booth. She is unpaid, there for one day, and can stop nobody. Everyone does as she says.',
      subj: 'The polling clerk',
      noforce: 'she is paid nothing and can stop nobody',
      why: 'Weber argued they obey the role the rules set out, not the volunteer filling it.',
      gone: 'the clerk on duty at the next election directs the queue the same way',
      no: { trad: 'she is a volunteer for one day, so no custom attaches to her',
            char: 'nothing about her personally is in play — she is unpaid and unknown' } },

    { id: 'crown', type: 'trad',
      text: 'A monarch opens parliament. She commands no army and can pass no law; the crown came to her from her father. The chamber follows her lead through it.',
      subj: 'The monarch',
      noforce: 'she commands no army and can pass no law',
      why: 'Weber argued the grounds are inheritance and long custom, not office and not personal gift.',
      gone: 'the crown moves to her heir and the ceremony carries on unchanged',
      no: { char: 'the ceremony would run the same way for whoever inherited',
            legal: 'nobody appointed her and no rule book put her there' } },

    { id: 'band', type: 'char',
      text: 'The singer in a new band sets the set list and rehearsal times. She owns none of the gear and pays nobody. The others follow her for what she does on stage.',
      subj: 'The singer',
      noforce: 'she owns none of the gear and pays nobody',
      why: 'Weber argued this rests on a personal gift the other three believe in.',
      gone: 'if she walks, the other three are back to arguing it out from scratch',
      no: { trad: 'the band is new, so there is no custom in it',
            legal: 'there is no post and no rule — she was never appointed anything' } }
  ];

  var OPEN_CAP = 'Look at what each person does not have, as much as what they do.';

  var MASTERY = 'Weber’s question is never how hard the order is pushed but why it is accepted: long custom, an extraordinary person, or rules that give the post its right. Only the personal one cannot be handed on.';

  /* ---------- styles (every selector under .svw-wba) ----------------- */

  var CSS = [
    '.svw-wba{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;-webkit-font-smoothing:antialiased}',
    '.svw-wba *{box-sizing:border-box}',
    '.svw-wba [hidden]{display:none!important}',
    '.svw-wba .wba-kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--wba-accent)}',
    '.svw-wba .wba-title{margin:.14rem 0 0;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.14rem;line-height:1.24}',
    '.svw-wba .wba-frame{margin:.26rem 0 .45rem;font-size:.8rem;line-height:1.45;color:#5b564e}',
    '.svw-wba .wba-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.58rem .62rem .55rem}',
    '.svw-wba .wba-case{margin:0 0 .45rem;font-size:.84rem;line-height:1.42}',
    '.svw-wba .wba-step{display:flex;align-items:baseline;gap:.36rem;margin:0 0 .28rem;font-size:.7rem;font-weight:700;letter-spacing:.03em;color:#5b564e}',
    '.svw-wba .wba-chip{flex:none;display:inline-block;min-width:17px;height:17px;line-height:17px;text-align:center;border-radius:50%;background:var(--wba-tint);color:var(--wba-accent);font-size:.66rem;font-weight:700}',
    '.svw-wba .wba-opts{display:flex;flex-direction:column;gap:.2rem}',
    '.svw-wba .wba-opt{display:block;width:100%;min-height:31px;padding:.3rem .5rem;text-align:left;font:inherit;font-size:.79rem;font-weight:600;color:#2d2a26;background:#fff;border:1px solid #e0d9cd;border-radius:9px;cursor:pointer}',
    '.svw-wba .wba-sopt{min-height:28px;font-size:.77rem;font-weight:500;color:#5b564e}',
    '.svw-wba .wba-opt.is-picked{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-wba .wba-opt.is-you{background:#f1ece4;border-color:#b8b1a5;color:#2d2a26}',
    '.svw-wba .wba-opt.is-home{background:var(--wba-tint);border-color:var(--wba-accent);color:#2d2a26}',
    '.svw-wba .wba-opt[disabled]{cursor:default;opacity:1}',
    '.svw-wba .wba-tag{display:block;margin-top:.08rem;font-size:.66rem;font-weight:600;color:var(--wba-accent)}',
    '.svw-wba .wba-g2{margin-top:.45rem}',
    '.svw-wba .wba-bar{display:flex;align-items:center;gap:.6rem;margin-top:.5rem}',
    '.svw-wba .wba-run{flex:1;min-width:0;margin:0;font-size:.74rem;line-height:1.3;color:#8d8880}',
    '.svw-wba .wba-go{flex:none;font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-wba .wba-go.is-live{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-wba .wba-go[disabled]{cursor:default;color:#a49e94;background:#f4f1ec;border-color:#e6e0d6}',
    '.svw-wba .wba-cap{margin:.42rem 0 0;font-size:.8rem;line-height:1.45;color:#2d2a26;min-height:3em}',
    '.svw-wba .wba-cap b{font-weight:600}',
    '.svw-wba .wba-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-wba .wba-opt:focus-visible,.svw-wba .wba-go:focus-visible{outline:2px solid var(--wba-accent);outline-offset:2px}',
    '.svw-wba.wba-motion .wba-opt,.svw-wba.wba-motion .wba-go{transition:background-color .12s ease,border-color .12s ease,color .12s ease}'
  ].join('\n');

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'weber-authority-source-of-legitimacy',
      title: 'Obeyed — but on what grounds?',
      teaches: 'Weber’s three types of authority differ in the source of legitimacy — why people accept the right to be obeyed — not in the leader’s personality.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#7a6a52';
      var reduced = !!ctx.reducedMotion;

      root.classList.add('svw-wba');
      if (!reduced) root.classList.add('wba-motion');
      root.style.setProperty('--wba-accent', accent);
      root.style.setProperty('--wba-tint', accent + '22');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      root.appendChild(el('p', 'wba-kick', 'Power and authority'));
      root.appendChild(el('h3', 'wba-title', 'Obeyed — but on what grounds?'));
      root.appendChild(el('p', 'wba-frame',
        'Each of these people is obeyed. Decide what the obedience rests on, and whether it would survive them.'));

      var stage = el('div', 'wba-stage');
      var caseP = el('p', 'wba-case');
      stage.appendChild(caseP);

      /* step 1 — the reason */
      var step1 = el('div', 'wba-step');
      step1.appendChild(el('span', 'wba-chip', '1'));
      step1.appendChild(el('span', null, 'Why do they obey?'));
      stage.appendChild(step1);

      var opts1 = el('div', 'wba-opts');
      var rBtn = {};
      REASONS.forEach(function (o) {
        var b = el('button', 'wba-opt');
        b.type = 'button';
        var lab = el('span', null, o.label);
        var tag = el('span', 'wba-tag', '');
        tag.hidden = true;
        b.appendChild(lab);
        b.appendChild(tag);
        b.addEventListener('click', function () { pickReason(o.key); });
        rBtn[o.key] = { btn: b, tag: tag };
        opts1.appendChild(b);
      });
      stage.appendChild(opts1);

      /* step 2 — the succession test, disclosed once step 1 is set */
      var g2 = el('div', 'wba-g2');
      g2.hidden = true;
      var step2 = el('div', 'wba-step');
      step2.appendChild(el('span', 'wba-chip', '2'));
      var step2Txt = el('span', null, '');
      step2.appendChild(step2Txt);
      g2.appendChild(step2);

      var opts2 = el('div', 'wba-opts');
      var sBtn = {};
      SUCCS.forEach(function (o) {
        var b = el('button', 'wba-opt wba-sopt');
        b.type = 'button';
        b.appendChild(el('span', null, o.label));
        b.addEventListener('click', function () { pickSucc(o.key); });
        sBtn[o.key] = { btn: b };
        opts2.appendChild(b);
      });
      g2.appendChild(opts2);
      stage.appendChild(g2);

      root.appendChild(stage);

      var bar = el('div', 'wba-bar');
      var run = el('p', 'wba-run', '');
      var go = el('button', 'wba-go', 'Check');
      go.type = 'button';
      bar.appendChild(run);
      bar.appendChild(go);
      root.appendChild(bar);

      var cap = el('p', 'wba-cap', '');
      root.appendChild(cap);

      var sr = el('p', 'wba-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---------- state ---------- */
      var seat = 0;
      var cur = CASES[0];
      var reason = null;
      var succ = null;
      var revealed = false;
      var streak = 0;
      var attempted = 0;
      var mastered = false;

      function sync(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted,
                  round: cur.id, type: cur.type };
        if (extra) Object.keys(extra).forEach(function (k) { s[k] = extra[k]; });
        root.dataset.svState = JSON.stringify(s);
      }

      function say(html) {
        cap.innerHTML = html;
        sr.textContent = cap.textContent;
      }

      function armGo() {
        var ready = !!(reason && succ);
        go.disabled = !ready;
        go.classList.toggle('is-live', ready);
      }

      function renderCase() {
        caseP.textContent = cur.text;
        step2Txt.textContent = cur.subj + ' is gone for good. The obedience…';
        REASONS.forEach(function (o) {
          var r = rBtn[o.key];
          r.btn.hidden = false;
          r.btn.disabled = false;
          r.btn.classList.remove('is-picked', 'is-you', 'is-home');
          r.tag.hidden = true;
          r.tag.textContent = '';
        });
        SUCCS.forEach(function (o) {
          var b = sBtn[o.key].btn;
          b.hidden = false;
          b.disabled = false;
          b.classList.remove('is-picked', 'is-you', 'is-home');
        });
        g2.hidden = true;
        reason = null;
        succ = null;
        revealed = false;
        go.textContent = 'Check';
        armGo();
        cap.textContent = OPEN_CAP;
        sync();
      }

      function pickReason(key) {
        if (revealed) return;
        reason = key;
        REASONS.forEach(function (o) {
          rBtn[o.key].btn.classList.toggle('is-picked', o.key === key);
        });
        g2.hidden = false;
        armGo();
        sr.textContent = R[key].label + ' chosen. Now settle what happens when ' +
                         cur.subj.toLowerCase() + ' is gone.';
        sync({ reason: key, succession: succ });
      }

      function pickSucc(key) {
        if (revealed) return;
        succ = key;
        SUCCS.forEach(function (o) {
          sBtn[o.key].btn.classList.toggle('is-picked', o.key === key);
        });
        armGo();
        sr.textContent = S[key].label + ' chosen. Press Check.';
        sync({ reason: reason, succession: key });
      }

      function reveal(homeSucc) {
        revealed = true;
        /* the control the student was on is about to be disabled; park focus
           on the one thing still worth pressing rather than losing it to body */
        var hadFocus = root.contains(document.activeElement);
        REASONS.forEach(function (o) {
          var r = rBtn[o.key];
          r.btn.classList.remove('is-picked');
          r.btn.disabled = true;
          if (o.key === cur.type) {
            r.btn.classList.add('is-home');
            r.tag.hidden = false;
            r.tag.textContent = 'Weber: ' + TYPES[cur.type].name + ' authority';
          } else if (o.key === reason) {
            r.btn.classList.add('is-you');
          } else {
            r.btn.hidden = true;
          }
        });
        SUCCS.forEach(function (o) {
          var b = sBtn[o.key].btn;
          b.classList.remove('is-picked');
          b.disabled = true;
          if (o.key === homeSucc) b.classList.add('is-home');
          else if (o.key === succ) b.classList.add('is-you');
          else b.hidden = true;
        });
        if (hadFocus && !root.contains(document.activeElement)) go.focus();
      }

      function commit() {
        var t = TYPES[cur.type];
        var okReason = reason === cur.type;
        var okSucc = succ === t.succ;
        var correct = okReason && okSucc;

        attempted += 1;
        streak = correct ? streak + 1 : 0;
        var justMastered = false;
        if (correct && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        reveal(t.succ);

        var body;
        if (correct && justMastered) {
          body = '<b>Right — ' + t.name + ' authority. Three in a row, you have it.</b> ' + MASTERY;
        } else if (correct) {
          body = '<b>Right — ' + t.name + ' authority.</b> You said ' + R[reason].echo +
                 ', and that ' + S[succ].echo + '. ' + cur.why + ' So ' + cur.gone + '.';
        } else if (reason === 'force') {
          body = '<b>Not quite — you said they are forced.</b> Nothing here can force them: ' +
                 cur.noforce + '. Weber kept <b>power</b> for making people comply, and <b>authority</b> ' +
                 'for obedience people accept as right. Here ' + R[cur.type].echo + ' — that is <b>' +
                 t.name + '</b> authority.';
        } else if (!okReason) {
          body = '<b>Not quite — you said ' + R[reason].echo + '.</b> But ' + cur.no[reason] + '. ' +
                 cur.why + ' That is <b>' + t.name + '</b> authority, and ' + cur.gone + '.';
        } else {
          body = '<b>Not quite — you said ' + S[succ].echo + '.</b> Your reason was right: ' +
                 R[reason].echo + '. That is <b>' + t.name + '</b> authority, so ' + cur.gone +
                 '. ' + SUCCWHY[cur.type];
        }
        say(body);

        if (mastered) {
          run.textContent = correct ? 'You have it. Keep going if you want.'
                                    : 'You had it — that one slipped.';
          go.textContent = 'Another anyway';
        } else if (streak === 0) {
          run.textContent = 'Run back to zero — three in a row finishes it.';
          go.textContent = 'Next case';
        } else {
          run.textContent = streak + ' right in a row — ' + (3 - streak) + ' more and you have it.';
          go.textContent = 'Next case';
        }
        go.disabled = false;
        go.classList.remove('is-live');
        sync({ reason: reason, succession: succ, correct: correct });
      }

      go.addEventListener('click', function () {
        if (revealed) {
          seat = (seat + 1) % CASES.length;
          cur = CASES[seat];
          renderCase();
          sr.textContent = 'New case. ' + cur.text;
          return;
        }
        if (reason && succ) commit();
      });

      renderCase();
    }
  };
}());
