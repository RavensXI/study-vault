/* ============================================================
   piaget-qualitative-stages

   A classic Piagetian task is put to a named child at a named stage.
   The student predicts HOW that child answers, commits, and then hears
   the child answer in their own words.

   The point being made: a stage is a different RULE for making sense of
   the same situation, not a smaller helping of the adult answer. So two
   wrong predictions are always on offer - "the same answer, just less
   sure" and "they know really, they just say it wrong" - alongside the
   answer that belongs to a neighbouring stage.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- art: one small diagram per task ---------- */

  function svg(label, body) {
    return '<svg class="pqs-art" viewBox="0 0 300 72" xmlns="http://www.w3.org/2000/svg" ' +
           'role="img" aria-label="' + label + '">' + body + '</svg>';
  }

  var ART = {
    liquid: function (a) {
      return svg('Two glasses: a wide one and a tall thin one, holding the same juice.',
        '<path d="M48 20 L48 62 L86 62 L86 20" fill="none" stroke="#8d8880" stroke-width="1.4"/>' +
        '<rect x="49" y="36" width="36" height="25" fill="' + a + '" opacity="0.55"/>' +
        '<path d="M178 8 L178 62 L198 62 L198 8" fill="none" stroke="#8d8880" stroke-width="1.4"/>' +
        '<rect x="179" y="13" width="18" height="48" fill="' + a + '" opacity="0.55"/>' +
        '<line x1="104" y1="42" x2="152" y2="42" stroke="#8d8880" stroke-width="1.4"/>' +
        '<path d="M152 42 L145 38 L145 46 Z" fill="#8d8880"/>' +
        '<text x="128" y="34" font-size="10" fill="#8d8880" text-anchor="middle">poured</text>' +
        '<text x="67" y="71" font-size="10" fill="#8d8880" text-anchor="middle">unchanged</text>' +
        '<text x="188" y="71" font-size="10" fill="#8d8880" text-anchor="middle">tall, thin</text>');
    },
    counters: function (a) {
      var s = '';
      var i, xs1 = [72, 98, 124, 150, 176, 202], xs2 = [54, 88, 122, 156, 190, 224];
      for (i = 0; i < 6; i++) s += '<circle cx="' + xs1[i] + '" cy="24" r="5.5" fill="' + a + '" opacity="0.55"/>';
      for (i = 0; i < 6; i++) s += '<circle cx="' + xs2[i] + '" cy="50" r="5.5" fill="' + a + '" opacity="0.55"/>';
      return svg('Two rows of six counters; the lower row is spread out further.',
        s + '<text x="6" y="28" font-size="10" fill="#8d8880">row A</text>' +
        '<text x="6" y="54" font-size="10" fill="#8d8880">row B</text>');
    },
    mountains: function (a) {
      return svg('A model of three mountains on a table, with a child at the front and a doll at the side.',
        '<line x1="40" y1="52" x2="220" y2="52" stroke="#8d8880" stroke-width="1.4"/>' +
        '<polygon points="46,52 80,14 114,52" fill="none" stroke="#5b564e" stroke-width="1.3"/>' +
        '<polygon points="80,14 90,25 70,25" fill="#e0d9cd"/>' +
        '<polygon points="102,52 130,28 158,52" fill="none" stroke="#5b564e" stroke-width="1.3"/>' +
        '<line x1="130" y1="28" x2="130" y2="19" stroke="#5b564e" stroke-width="1.3"/>' +
        '<line x1="126" y1="23" x2="134" y2="23" stroke="#5b564e" stroke-width="1.3"/>' +
        '<polygon points="148,52 174,36 200,52" fill="none" stroke="#5b564e" stroke-width="1.3"/>' +
        '<rect x="170" y="44" width="9" height="8" fill="none" stroke="#5b564e" stroke-width="1.1"/>' +
        '<circle cx="112" cy="64" r="4.5" fill="#5b564e"/>' +
        '<text x="122" y="67" font-size="10" fill="#8d8880">child sits here</text>' +
        '<circle cx="248" cy="38" r="4.5" fill="' + a + '"/>' +
        '<text x="248" y="54" font-size="10" fill="#8d8880" text-anchor="middle">doll</text>');
    },
    flowers: function (a) {
      var s = '', i, x;
      for (i = 0; i < 7; i++) {
        x = 62 + i * 28;
        s += '<circle cx="' + x + '" cy="24" r="7" fill="none" stroke="#8d8880" stroke-width="1.3"/>' +
             '<circle cx="' + x + '" cy="24" r="2" fill="#8d8880"/>';
      }
      for (i = 0; i < 3; i++) {
        x = 62 + i * 28;
        s += '<circle cx="' + x + '" cy="54" r="7" fill="' + a + '" opacity="0.6"/>';
      }
      return svg('Seven daisies in one row and three roses in another.',
        s + '<text x="8" y="27" font-size="10" fill="#8d8880">daisies</text>' +
        '<text x="8" y="57" font-size="10" fill="#8d8880">roses</text>');
    },
    logic: function (a) {
      return svg('Two statements and a question: all cats bark; Rex is a cat; does Rex bark?',
        '<rect x="18" y="6" width="264" height="19" rx="5" fill="none" stroke="#8d8880" stroke-width="1.2"/>' +
        '<text x="30" y="19.5" font-size="10.5" fill="#5b564e">All cats bark.</text>' +
        '<rect x="18" y="28" width="264" height="19" rx="5" fill="none" stroke="#8d8880" stroke-width="1.2"/>' +
        '<text x="30" y="41.5" font-size="10.5" fill="#5b564e">Rex is a cat.</text>' +
        '<rect x="18" y="50" width="264" height="19" rx="5" fill="none" stroke="' + a + '" ' +
        'stroke-width="1.4" stroke-dasharray="4 3"/>' +
        '<text x="30" y="63.5" font-size="10.5" fill="#2d2a26">So — does Rex bark?</text>');
    },
    pendulum: function (a) {
      return svg('A bar with three pendulums of different string lengths and weights.',
        '<line x1="50" y1="12" x2="250" y2="12" stroke="#5b564e" stroke-width="2"/>' +
        '<line x1="85" y1="12" x2="85" y2="36" stroke="#8d8880" stroke-width="1.2"/>' +
        '<circle cx="85" cy="41" r="5" fill="' + a + '" opacity="0.6"/>' +
        '<line x1="150" y1="12" x2="150" y2="48" stroke="#8d8880" stroke-width="1.2"/>' +
        '<circle cx="150" cy="55" r="8" fill="' + a + '" opacity="0.6"/>' +
        '<line x1="215" y1="12" x2="215" y2="26" stroke="#8d8880" stroke-width="1.2"/>' +
        '<circle cx="215" cy="33" r="8" fill="' + a + '" opacity="0.6"/>' +
        '<text x="150" y="70" font-size="10" fill="#8d8880" text-anchor="middle">' +
        'different lengths and weights</text>');
    },
    toy: function (a) {
      return svg('A toy duck, and the same duck hidden under a cloth.',
        '<ellipse cx="66" cy="46" rx="16" ry="10" fill="' + a + '" opacity="0.6"/>' +
        '<circle cx="82" cy="33" r="7.5" fill="' + a + '" opacity="0.6"/>' +
        '<path d="M89 31 L97 34 L89 37 Z" fill="#8d8880"/>' +
        '<line x1="112" y1="42" x2="152" y2="42" stroke="#8d8880" stroke-width="1.4"/>' +
        '<path d="M152 42 L145 38 L145 46 Z" fill="#8d8880"/>' +
        '<path d="M164 58 Q174 20 204 24 Q234 28 242 58 Z" fill="#e8e3db" stroke="#8d8880" stroke-width="1.2"/>' +
        '<ellipse cx="202" cy="48" rx="16" ry="9" fill="none" stroke="#8d8880" ' +
        'stroke-width="1.1" stroke-dasharray="3 3" opacity="0.75"/>' +
        '<text x="70" y="70" font-size="10" fill="#8d8880" text-anchor="middle">toy duck</text>' +
        '<text x="203" y="70" font-size="10" fill="#8d8880" text-anchor="middle">under the cloth</text>');
    }
  };

  /* ---------- the rounds ---------- */

  var PRE = 'Pre-operational (roughly 2 to 7 years)';
  var CON = 'Concrete operational (roughly 7 to 11 years)';
  var FOR = 'Formal operational (from roughly 11 years)';
  var SEN = 'Sensorimotor (roughly birth to 2 years)';

  var ROUNDS = [
    {
      id: 'liquid-pre', art: 'liquid', who: 'Maya, 4', stage: PRE,
      frame: 'Two identical glasses hold the same juice. Maya watches you pour one into a tall, thin glass.',
      ask: 'Predict what Maya says when you ask which glass has more.',
      says: 'That one’s got more! Look how high it comes up.',
      correct: {
        t: 'The tall thin glass has more — the juice comes up higher.',
        s: 'she says the tall glass has more',
        f: 'Piaget called this centration: Maya judges by height alone and drops the width out of the picture. She cannot run the pour backwards in her head, so “nothing was added” does not help her.'
      },
      lessSure: {
        t: 'The same amount — the right answer, only said less confidently.',
        s: 'the same answer, only less sure',
        f: 'What changes between stages is the rule, not the confidence. Maya is certain. She judges by height alone, so she reaches a different answer, not a weaker version of yours.'
      },
      knowsWrong: {
        t: 'She knows it is the same, but muddles her words and says “more”.',
        s: 'she knows really and says it wrong',
        f: 'Piaget found children hold this judgement and defend it. Ask again, pour it back, ask a third time — Maya still says the tall glass has more. It is what she believes, not a slip of the tongue.'
      },
      others: [{
        t: 'The same — you only poured it, so you could pour it straight back.',
        s: 'the same, because you could pour it back',
        f: 'That is the concrete operational answer, from roughly seven. It needs reversibility — undoing the pour mentally — which Maya has not developed. Same task, different rule, different answer.'
      }]
    },
    {
      id: 'liquid-concrete', art: 'liquid', who: 'Sam, 9', stage: CON,
      frame: 'Two identical glasses hold the same juice. Sam watches you pour one into a tall, thin glass.',
      ask: 'Predict what Sam says when you ask which glass has more.',
      says: 'It’s the same. You only poured it — pour it back and it looks like it did before.',
      correct: {
        t: 'The same — nothing was added, and you could pour it back.',
        s: 'the same, and you could pour it back',
        f: 'Reversibility and decentring: Sam undoes the pour in his head and holds height and width at once. Note what he leans on — real glasses, in front of him. This stage works on tangible things.'
      },
      lessSure: {
        t: 'The tall one has more, he thinks — though he is not very sure.',
        s: 'the tall glass, said unsurely',
        f: 'Sam is not a hesitant four-year-old. Conservation is not a confidence upgrade on the younger answer. It is a new operation: he reverses the pour mentally, so the height stops fooling him.'
      },
      knowsWrong: {
        t: 'He can see the tall one has more, but says “the same” to please you.',
        s: 'he says the same only to please you',
        f: 'Piaget tested exactly this by asking again and pouring back. Sam gives reasons: nothing added, and you could pour it back. The explanation is the evidence, not compliance.'
      },
      others: [{
        t: 'The tall thin glass has more, because the juice is higher.',
        s: 'the tall glass has more',
        f: 'That is the pre-operational answer, roughly 2 to 7, driven by centration on height. By nine Sam decentres and reverses, so the same task gets the opposite answer.'
      }]
    },
    {
      id: 'counters-pre', art: 'counters', who: 'Zara, 5', stage: PRE,
      frame: 'Two rows of six counters sit level. Zara watches you spread one row out so it stretches further.',
      ask: 'Predict what Zara says when you ask which row has more.',
      says: 'That row’s got more now. Look, it’s longer.',
      correct: {
        t: 'The longer row has more, because it stretches further.',
        s: 'the longer row has more',
        f: 'Conservation of number: Zara centres on length and ignores that no counter was added or removed. The counting is not the problem — she can count six — the rule she judges by is.'
      },
      lessSure: {
        t: 'Six each — the right answer, but she hedges and is unsure.',
        s: 'six each, just unsurely',
        f: 'She is not part-way to your answer. Zara answers confidently from a different rule: longer looks like more. Stages differ in kind, not in how sure the child sounds.'
      },
      knowsWrong: {
        t: 'She knows both rows have six, but says the wrong one out of habit.',
        s: 'she knows it is six and says it wrong',
        f: 'Ask her to count both rows and she says six and six — then still points at the longer row as “more”. Holding both at once is the finding, not a wording slip.'
      },
      others: [{
        t: 'Six each — you only moved them, you did not add any.',
        s: 'six each, because you only moved them',
        f: 'That is the concrete operational answer, from roughly seven. It rests on identity and reversibility: nothing was added, and the row could be pushed back together. Zara is not there yet.'
      }]
    },
    {
      id: 'mountains-pre', art: 'mountains', who: 'Jonah, 4', stage: PRE,
      frame: 'A model of three mountains sits on a table. Jonah sits at the front, a doll round to the side.',
      ask: 'Predict which picture Jonah chooses for what the doll can see.',
      says: 'She sees the big snowy one at the front — same as me.',
      correct: {
        t: 'The picture of his own view, not the doll’s.',
        s: 'the picture of his own view',
        f: 'Egocentrism, in Piaget and Inhelder’s three mountains task. It is not selfishness: Jonah cannot picture the scene from a position he is not sitting in, so his own view is the only one there is.'
      },
      lessSure: {
        t: 'The doll’s view — the right card, but chosen hesitantly.',
        s: 'the doll’s view, chosen hesitantly',
        f: 'Jonah chooses quickly and without doubt. The gap is not certainty, it is the mental operation of rotating the scene. A different rule gives a different card, not a shakier one.'
      },
      knowsWrong: {
        t: 'He knows what the doll sees, but points to the wrong card by mistake.',
        s: 'he knows and points wrongly by mistake',
        f: 'Piaget moved the doll around and asked again and again. Jonah keeps choosing his own view wherever the doll goes. A mistake would move about; this does not.'
      },
      others: [{
        t: 'The card showing the small mountain in front, as the doll sees it.',
        s: 'the doll’s view',
        f: 'That is the concrete operational answer, from roughly seven, once a child can imagine another position. The skill is not naming stages but knowing whose viewpoint a child can take.'
      }]
    },
    {
      id: 'mountains-concrete', art: 'mountains', who: 'Priya, 9', stage: CON,
      frame: 'A model of three mountains sits on a table. Priya sits at the front, a doll round to the side.',
      ask: 'Predict which picture Priya chooses for what the doll can see.',
      says: 'From over there the little one with the cross is in front, and the snowy one is behind it.',
      correct: {
        t: 'The card showing the doll’s view from the side.',
        s: 'the doll’s view from the side',
        f: 'Decentring: Priya holds her own view and the doll’s at once and rotates the scene mentally. The model is in front of her — this stage is strong on real, visible things.'
      },
      lessSure: {
        t: 'Her own view — she is not confident enough to picture the doll’s.',
        s: 'her own view, from lack of confidence',
        f: 'Confidence is not the variable. A nine-year-old can perform the rotation; a four-year-old cannot perform it at all. Stages differ in what the child can do, not in how boldly they do it.'
      },
      knowsWrong: {
        t: 'She still only sees her own view really, but has learnt the trick.',
        s: 'she has learnt the trick',
        f: 'Piaget tested new doll positions the child had never met. Priya works those out too, and explains what is behind what. The explanation is what separates understanding from a trick.'
      },
      others: [{
        t: 'The picture of the view she can see herself.',
        s: 'her own view',
        f: 'That is the pre-operational answer, roughly 2 to 7, driven by egocentrism. Same task, five years later, the opposite card — which is why Piaget called the change qualitative.'
      }]
    },
    {
      id: 'flowers-pre', art: 'flowers', who: 'Ellie, 5', stage: PRE,
      frame: 'Seven daisies and three roses lie on the table. Ellie can see all of them.',
      ask: 'Predict what Ellie says when asked: are there more daisies, or more flowers?',
      says: 'More daisies — there’s only three roses.',
      correct: {
        t: 'More daisies, because there are only three roses.',
        s: 'more daisies',
        f: 'Class inclusion. Ellie cannot hold the part, daisies, and the whole, flowers, in mind together, so she compares daisies with roses — the only comparison her rule allows.'
      },
      lessSure: {
        t: 'More flowers — the right answer, but said with a shrug.',
        s: 'more flowers, said with a shrug',
        f: 'She answers firmly, and she is not nearly right. Once the whole class splits into daisies against roses, “more flowers” is not available to her at any level of confidence.'
      },
      knowsWrong: {
        t: 'She knows daisies are flowers, but the question confuses her wording.',
        s: 'she knows but words it wrongly',
        f: 'Ask whether daisies are flowers and she says yes. Ask the comparison again and she still says more daisies. Holding both together is the point: this is a limit on reasoning, not on wording.'
      },
      others: [{
        t: 'More flowers, because the daisies are flowers as well.',
        s: 'more flowers, because daisies are flowers',
        f: 'That is the concrete operational answer, from roughly seven, when a child can treat daisies as a group and as part of a bigger group at once. Ellie cannot do both yet.'
      }]
    },
    {
      id: 'flowers-concrete', art: 'flowers', who: 'Ryan, 9', stage: CON,
      frame: 'Seven daisies and three roses lie on the table in front of Ryan.',
      ask: 'Predict what Ryan says when asked: are there more daisies, or more flowers?',
      says: 'More flowers. The daisies are flowers too — so that’s ten flowers and seven daisies.',
      correct: {
        t: 'More flowers — daisies are flowers too, so ten against seven.',
        s: 'more flowers, ten against seven',
        f: 'Class inclusion mastered: Ryan keeps the subclass inside the class and compares part with whole. Note he is counting objects he can see — this stage leans on the tangible.'
      },
      lessSure: {
        t: 'More daisies — he half-sees the trap but is not confident.',
        s: 'more daisies, half-seeing the trap',
        f: 'This is not a half-answer. Ryan runs a different operation from a five-year-old and gets a different result. Between the stages the rule changes; the child does not simply become surer.'
      },
      knowsWrong: {
        t: 'He means more flowers but says “more daisies” by accident.',
        s: 'he says daisies by accident',
        f: 'Ryan justifies it: ten flowers, seven daisies. Where a child can explain the answer, the answer is not an accident — and the explanation is what Piaget listened for.'
      },
      others: [{
        t: 'More daisies, because there are only three roses.',
        s: 'more daisies',
        f: 'That is the pre-operational answer, roughly 2 to 7, from failing class inclusion. Matching stage names to tasks is not the skill — knowing which comparison the child can hold in mind is.'
      }]
    },
    {
      id: 'hypo-concrete', art: 'logic', who: 'Leo, 9', stage: CON,
      frame: 'You tell Leo: “All cats bark. Rex is a cat.” Then you ask him whether Rex barks.',
      ask: 'Predict what Leo says.',
      says: 'No! Cats don’t bark, they miaow. Dogs bark.',
      correct: {
        t: 'He rejects it — cats do not bark, so the question is wrong.',
        s: 'he rejects the premise',
        f: 'Concrete operational thinking stays tied to the real. Leo cannot set a known fact aside and reason inside a made-up premise, so he corrects the world instead of following the logic.'
      },
      lessSure: {
        t: 'Yes, Rex barks — the right answer, but he is unsure of it.',
        s: 'yes, said unsurely',
        f: 'Leo is emphatic, not hesitant. What the next stage adds is a new move — treating a statement as a supposition to reason from, whether or not it happens to be true.'
      },
      knowsWrong: {
        t: 'He follows the logic but blurts out “no” without thinking.',
        s: 'he follows the logic but blurts no',
        f: 'Slow it down and repeat the premise, and Leo still argues about cats. He is answering the question he is able to answer. That is the limit, not a rushed answer.'
      },
      others: [
        {
          t: 'Yes — if all cats bark and Rex is a cat, then Rex barks.',
          s: 'yes, because it follows',
          f: 'That is the formal operational answer, from roughly eleven: reasoning from a premise whether or not it is true. It is exactly the move Leo cannot make yet.'
        },
        {
          t: 'He talks about his own cat instead, and what she does.',
          s: 'he talks about his own cat',
          f: 'That is closer to a pre-operational response — answering from personal experience without engaging the form of the question. By nine Leo does engage: he takes the claim on and rejects it.'
        }
      ]
    },
    {
      id: 'hypo-formal', art: 'logic', who: 'Nadia, 14', stage: FOR,
      frame: 'You tell Nadia: “All cats bark. Rex is a cat.” Then you ask her whether Rex barks.',
      ask: 'Predict what Nadia says.',
      says: 'If all cats bark, then yes — Rex barks. It isn’t true really, but that’s what follows.',
      correct: {
        t: 'Yes — within the premise it follows, even though it is untrue.',
        s: 'yes, because it follows from the premise',
        f: 'Formal operational thinking: Nadia holds the premise as a supposition and reasons inside it. The last stage adds abstract, hypothetical reasoning — no extra facts, a new kind of move.'
      },
      lessSure: {
        t: 'No, cats miaow — she almost sees the logic but is unsure.',
        s: 'no, cats miaow',
        f: 'That is the earlier answer, and unsureness is not what produces it. Nadia separates “is it true?” from “does it follow?” — a distinction a nine-year-old cannot draw at all.'
      },
      knowsWrong: {
        t: 'She knows cats do not bark and says so, meaning the same thing.',
        s: 'she says cats do not bark',
        f: 'She knows that too, and will say so — but she answers the question asked. Holding both, “not true” and “it follows”, is the new ability.'
      },
      others: [
        {
          t: 'No — cats do not bark, so the question is wrong.',
          s: 'no, the question is wrong',
          f: 'That is the concrete operational answer, roughly 7 to 11, where reasoning stays tied to real facts. Nadia can set the facts aside for the length of an argument.'
        },
        {
          t: 'Yes, but only after checking with a real dog first.',
          s: 'she checks with a real dog',
          f: 'Needing a real object to think with is the concrete stage. Formal operational reasoning runs on the words alone, and that is the whole difference.'
        }
      ]
    },
    {
      id: 'pendulum-concrete', art: 'pendulum', who: 'Owen, 10', stage: CON,
      frame: 'Owen has strings of several lengths and weights of several sizes, and is asked what makes a pendulum swing faster.',
      ask: 'Predict how Owen goes about finding out.',
      says: 'I put the big weight on the short string and it went fast — so it’s the heavy one.',
      correct: {
        t: 'He changes two things at once, then judges from what he saw.',
        s: 'he changes two things at once',
        f: 'Concrete operational reasoning handles real objects well, but not the whole system of possibilities. Length and weight moved together, so Owen cannot tell which one did it.'
      },
      lessSure: {
        t: 'He tests one thing at a time, but is unsure of his conclusion.',
        s: 'one at a time, but unsure',
        f: 'Isolating a variable is not a confident version of muddling two. It is a plan made before touching anything, and that planning is what the next stage brings.'
      },
      knowsWrong: {
        t: 'He knows to keep the weight the same, but forgets in the moment.',
        s: 'he knows but forgets',
        f: 'Ask Owen why the short string was faster and he answers “the weight”. He is not forgetting a plan; he never had one, because holding a variable still has not arrived.'
      },
      others: [
        {
          t: 'He changes only the length, keeping weight and push the same.',
          s: 'he changes one thing at a time',
          f: 'That is the formal operational answer, from roughly eleven: controlling variables so each possibility is tested in turn. Owen judges from whatever he happened to see.'
        },
        {
          t: 'He decides it must be the push, without trying anything.',
          s: 'he decides without trying',
          f: 'Owen does experiment — he is happy with real apparatus. His limit is designing the test, not a reluctance to test.'
        }
      ]
    },
    {
      id: 'pendulum-formal', art: 'pendulum', who: 'Amara, 14', stage: FOR,
      frame: 'Amara has strings of several lengths and weights of several sizes, and is asked what makes a pendulum swing faster.',
      ask: 'Predict how Amara goes about finding out.',
      says: 'I’ll keep the weight the same and change only the length. Then if it changes, it was the length.',
      correct: {
        t: 'She changes one thing at a time, holding the others still.',
        s: 'she changes one thing at a time',
        f: 'Formal operational thinking: Amara lists the possible causes first, then tests them one at a time. She is reasoning about what could be true, not only about what she has already seen.'
      },
      lessSure: {
        t: 'She swaps several things at once, unsure how to start.',
        s: 'she swaps several at once',
        f: 'That is the earlier approach, and hesitancy is not what causes it. Amara can plan the whole set of tests before touching the apparatus — a move a ten-year-old cannot make at any confidence.'
      },
      knowsWrong: {
        t: 'She is really just copying a method she was taught at school.',
        s: 'she copies a taught method',
        f: 'Give her a new problem — what makes a ball roll further — and she isolates variables there too. Piaget looked for reasoning that transfers, and this transfers.'
      },
      others: [
        {
          t: 'She tries the heavy weight on the short string and calls it settled.',
          s: 'heavy weight on short string',
          f: 'That is the concrete operational approach, roughly 7 to 11: judging from one striking combination. Amara separates the variables so the result means something.'
        },
        {
          t: 'She cannot begin until somebody shows her how it is done.',
          s: 'she waits to be shown',
          f: 'This is not about being taught. What arrives at this stage is systematic hypothesis testing — planning the tests from the possibilities, unprompted.'
        }
      ]
    },
    {
      id: 'toy-sensorimotor', art: 'toy', who: 'Rosa, 6 months', stage: SEN,
      frame: 'Rosa is reaching for a toy duck. While she watches, you cover it completely with a cloth.',
      ask: 'Predict what Rosa does next.',
      says: 'Rosa stops reaching, looks away, and picks up her cup instead.',
      saysIsAction: true,
      correct: {
        t: 'She stops reaching and turns away, as if the duck has gone.',
        s: 'she stops reaching',
        f: 'Object permanence has not developed. Piaget found infants under about eight months behave as though a hidden object no longer exists — out of sight is out of the world, not merely out of view.'
      },
      lessSure: {
        t: 'She reaches for the cloth, but slowly and unsurely.',
        s: 'she reaches slowly, unsurely',
        f: 'She does not search at all. This is not a weaker version of searching: for Rosa there is nothing there to search for, which is a different situation, not a smaller one.'
      },
      knowsWrong: {
        t: 'She knows the duck is there but cannot coordinate her hands yet.',
        s: 'she knows but cannot reach',
        f: 'She was reaching accurately a second earlier. The reaching stops when the duck is covered and restarts when it reappears: what changed is what she thinks exists, not what her hands can do.'
      },
      others: [{
        t: 'She pulls the cloth off straight away and grabs the duck.',
        s: 'she pulls the cloth off',
        f: 'That comes once object permanence is established, from about eight months. Same cloth, same duck, a completely different world — the first qualitative shift Piaget describes.'
      }]
    },
    {
      id: 'toy-pre', art: 'toy', who: 'Alfie, 3', stage: PRE,
      frame: 'Alfie is playing with a toy duck. While he watches, you cover it completely with a cloth.',
      ask: 'Predict what Alfie does next.',
      says: 'It’s under there — I saw you put it there.',
      correct: {
        t: 'He pulls the cloth off at once — he knows the duck is under it.',
        s: 'he pulls the cloth off at once',
        f: 'Object permanence settled at about eight months, long before this stage. Alfie’s limits lie elsewhere now — conservation, egocentrism. Stages are kinds of thinking, not amounts of it.'
      },
      lessSure: {
        t: 'He finds it, but hesitantly — not quite sure it is still there.',
        s: 'he finds it hesitantly',
        f: 'There is no hesitation to find. Each stage has its own competence: hidden objects stopped being a puzzle for Alfie at about eight months, even though a tall glass of juice will still fool him.'
      },
      knowsWrong: {
        t: 'He searches under the wrong cloth, muddling what he saw.',
        s: 'he searches under the wrong cloth',
        f: 'Searching where an object used to be is an earlier infant error, at roughly eight to twelve months. At three, Alfie tracks the hiding place he actually watched.'
      },
      others: [{
        t: 'He stops looking, as though the duck no longer exists.',
        s: 'he stops looking',
        f: 'That is the early sensorimotor response, before about eight months. Assuming a baby-ish task must go with the youngest stage is the rote matching to avoid: check what this child can do.'
      }]
    }
  ];

  var MASTERY = 'three in a row, so you have it: a stage is a different rule for the same task, ' +
    'not more of the same knowledge. The ages are only guides — McGarrigle and Donaldson found ' +
    'children conserve younger when a “naughty teddy” spoils the row.';

  /* ---------- styles, scoped under the root class ---------- */

  var CSS = [
    '.svw-pqs{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;',
    'background:transparent;box-sizing:border-box;max-width:100%;}',
    '.svw-pqs *,.svw-pqs *::before,.svw-pqs *::after{box-sizing:border-box;}',
    '.svw-pqs .pqs-head{display:flex;align-items:baseline;justify-content:space-between;gap:.6rem;}',
    '.svw-pqs .pqs-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;}',
    '.svw-pqs .pqs-run{font-size:.72rem;font-weight:600;color:#8d8880;font-variant-numeric:tabular-nums;',
    'white-space:nowrap;}',
    '.svw-pqs .pqs-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;',
    'line-height:1.2;margin:.15rem 0 .25rem;}',
    '.svw-pqs .pqs-frame{font-size:.84rem;line-height:1.45;color:#5b564e;margin:0 0 .5rem;}',
    '.svw-pqs .pqs-frame b{color:#2d2a26;font-weight:600;}',
    '.svw-pqs .pqs-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
    'padding:.5rem .55rem .45rem;}',
    '.svw-pqs .pqs-art{display:block;width:100%;max-width:330px;height:auto;margin:0 auto;}',
    '.svw-pqs .pqs-who{font-size:.74rem;font-weight:600;color:#5b564e;margin:.25rem 0 0;',
    'text-align:center;line-height:1.35;}',
    '.svw-pqs .pqs-bubble{display:none;margin:.45rem 0 0;border:1px solid #e0d9cd;border-radius:12px;',
    'padding:.4rem .55rem;background:#fff;}',
    '.svw-pqs .pqs-bubble.is-on{display:block;}',
    '.svw-pqs .pqs-bublab{font-size:.66rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;',
    'color:#8d8880;margin:0 0 .05rem;}',
    '.svw-pqs .pqs-bubtext{font-size:.86rem;line-height:1.45;margin:0;color:#2d2a26;}',
    '.svw-pqs .pqs-bubtext.is-action{font-style:italic;color:#5b564e;}',
    '.svw-pqs .pqs-opts{display:flex;flex-direction:column;gap:.38rem;margin-top:.55rem;}',
    '.svw-pqs .pqs-opt{display:block;width:100%;text-align:left;font-family:inherit;font-size:.82rem;',
    'line-height:1.35;font-weight:500;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;',
    'border-radius:10px;padding:.42rem .55rem;cursor:pointer;}',
    '.svw-pqs .pqs-opt.is-picked{background:#2d2a26;border-color:#2d2a26;color:#fff;font-weight:600;}',
    '.svw-pqs .pqs-opt.is-picked[disabled]{background:#fff;border:1.5px solid #2d2a26;',
    'color:#2d2a26;font-weight:600;cursor:default;}',
    '.svw-pqs .pqs-opt.is-gone{display:none;}',
    '.svw-pqs .pqs-opt:focus-visible{outline:2px solid #2d2a26;outline-offset:2px;}',
    '.svw-pqs .pqs-go{display:block;width:100%;margin-top:.55rem;font-family:inherit;font-size:.82rem;',
    'font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;',
    'padding:.5rem .95rem;cursor:pointer;}',
    '.svw-pqs .pqs-go[disabled]{background:#faf8f5;color:#a8a29a;border-color:#e0d9cd;cursor:default;}',
    '.svw-pqs .pqs-cap{font-size:.86rem;line-height:1.46;color:#2d2a26;margin:.5rem 0 0;min-height:2.6em;}',
    '.svw-pqs .pqs-cap b{font-weight:700;}',
    '.svw-pqs .pqs-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);',
    'clip-path:inset(50%);white-space:nowrap;}',
    '.svw-pqs.pqs-motion .pqs-opt{transition:background-color .12s ease,color .12s ease;}'
  ].join('');

  /* ---------- helpers ---------- */

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

  /* ---------- the widget ---------- */

  window.SVWidget = {
    meta: {
      id: 'piaget-qualitative-stages',
      title: 'Predict what the child says',
      teaches: 'Piaget’s stages are qualitatively different ways of reasoning, not age labels or amounts of cleverness.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      root.classList.add('svw-pqs');
      if (!reduced) root.classList.add('pqs-motion');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      var head = el('div', 'pqs-head');
      var kick = el('span', 'pqs-kick', 'Cognitive development');
      kick.style.color = accent;
      var run = el('span', 'pqs-run', '');
      head.appendChild(kick); head.appendChild(run);
      root.appendChild(head);

      root.appendChild(el('h3', 'pqs-title', 'Predict what the child says'));

      var frame = el('p', 'pqs-frame');
      root.appendChild(frame);

      var stage = el('div', 'pqs-stage');
      var artWrap = el('div', 'pqs-artwrap');
      var who = el('p', 'pqs-who');
      var bubble = el('div', 'pqs-bubble');
      var bubLab = el('p', 'pqs-bublab', '');
      var bubText = el('p', 'pqs-bubtext', '');
      bubble.appendChild(bubLab); bubble.appendChild(bubText);
      stage.appendChild(artWrap); stage.appendChild(who); stage.appendChild(bubble);
      root.appendChild(stage);

      var optWrap = el('div', 'pqs-opts');
      var opts = [];
      for (var i = 0; i < 4; i++) {
        var b = el('button', 'pqs-opt', '');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        optWrap.appendChild(b);
        opts.push(b);
      }
      root.appendChild(optWrap);

      var go = el('button', 'pqs-go', 'Check the prediction');
      go.type = 'button';
      root.appendChild(go);

      var cap = el('p', 'pqs-cap', '');
      root.appendChild(cap);

      var sr = el('p', 'pqs-sr', '');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ----- state ----- */
      var order = shuffle(ROUNDS.map(function (_, k) { return k; }));
      var cursor = 0;
      var round = null, cards = [], picked = -1, revealed = false;
      var streak = 0, attempted = 0, mastered = false;

      function report() {
        root.dataset.svState = JSON.stringify({
          streak: streak,
          mastered: mastered,
          attempted: attempted,
          round: round ? round.id : null,
          picked: picked < 0 ? null : cards[picked].k,
          correct: revealed ? (cards[picked].k === 'correct') : null
        });
      }

      function nextRound() {
        if (cursor >= order.length) {
          var last = order[order.length - 1];
          order = shuffle(ROUNDS.map(function (_, k) { return k; }));
          if (order[0] === last) { order.push(order.shift()); }
          cursor = 0;
        }
        round = ROUNDS[order[cursor++]];

        /* options: always at least one of the two "amount" misconceptions,
           plus every neighbouring-stage answer this task has. */
        cards = [{ k: 'correct', o: round.correct }];
        if (round.others.length >= 2) {
          var mk = Math.random() < 0.5 ? 'lessSure' : 'knowsWrong';
          cards.push({ k: mk, o: round[mk] });
          cards.push({ k: 'other', o: round.others[0] });
          cards.push({ k: 'other', o: round.others[1] });
        } else {
          cards.push({ k: 'lessSure', o: round.lessSure });
          cards.push({ k: 'knowsWrong', o: round.knowsWrong });
          cards.push({ k: 'other', o: round.others[0] });
        }
        shuffle(cards);

        frame.innerHTML = '';
        frame.appendChild(document.createTextNode(round.frame + ' '));
        frame.appendChild(el('b', null, round.ask));

        artWrap.innerHTML = ART[round.art](accent);
        who.textContent = round.who + ' · ' + round.stage;

        bubble.classList.remove('is-on');
        bubText.classList.remove('is-action');

        for (var j = 0; j < 4; j++) {
          opts[j].textContent = cards[j].o.t;
          opts[j].className = 'pqs-opt';
          opts[j].disabled = false;
          opts[j].setAttribute('aria-pressed', 'false');
        }

        picked = -1;
        revealed = false;
        go.textContent = 'Check the prediction';
        go.disabled = true;
        cap.textContent = '';
        drawRun();
        report();
      }

      function drawRun() {
        if (mastered) {
          run.textContent = 'You have it';
        } else if (streak > 0) {
          run.textContent = streak === 2
            ? '2 right in a row — one more'
            : '1 right in a row';
        } else {
          run.textContent = '';
        }
      }

      function pick(idx) {
        if (revealed) return;
        picked = idx;
        for (var j = 0; j < 4; j++) {
          var on = j === idx;
          opts[j].classList.toggle('is-picked', on);
          opts[j].setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        go.disabled = false;
        sr.textContent = 'Prediction chosen: ' + cards[idx].o.t;
        report();
      }

      function reveal() {
        revealed = true;
        attempted++;
        var card = cards[picked];
        var right = card.k === 'correct';

        if (right) { streak++; } else { streak = 0; }
        var justMastered = right && streak >= 3 && !mastered;
        if (justMastered) mastered = true;

        for (var j = 0; j < 4; j++) {
          if (j !== picked) opts[j].classList.add('is-gone');
          opts[j].disabled = true;
        }

        bubLab.textContent = round.saysIsAction
          ? 'What ' + round.who.split(',')[0] + ' does'
          : round.who.split(',')[0] + ' says';
        bubText.textContent = round.saysIsAction
          ? round.says
          : '“' + round.says + '”';
        bubText.classList.toggle('is-action', !!round.saysIsAction);
        bubble.classList.add('is-on');

        cap.textContent = '';
        cap.appendChild(el('b', null, right ? 'Right — ' : 'Not quite — '));
        if (justMastered) {
          cap.appendChild(document.createTextNode(MASTERY));
        } else {
          cap.appendChild(document.createTextNode(
            'you predicted ' + card.o.s + '. ' + card.o.f));
        }

        go.textContent = mastered ? 'Another anyway' : 'Next task';
        go.disabled = false;
        drawRun();
        sr.textContent = (right ? 'Right. ' : 'Not quite. ') + round.who + ': ' + round.says;
        report();
      }

      opts.forEach(function (b, idx) {
        b.addEventListener('click', function () { pick(idx); });
      });

      go.addEventListener('click', function () {
        if (!revealed) {
          if (picked < 0) return;
          reveal();
        } else {
          var hadFocus = document.activeElement === go;
          nextRound();
          if (hadFocus) opts[0].focus();
        }
      });

      nextRound();
    }
  };
})();
