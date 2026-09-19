/* Typed recall: the student types what they remember and a judge (Jev, via
   /api/flashcards/judge) says whether it matches the card's own answer. Shared by
   the lesson flashcard modal (js/main.js) and the dashboard deck (classic.html).
   Never blocks a session: any failure returns null and the card falls back to the
   flip-and-rate flow the site has always had. */
(function () {
  'use strict';
  var ENDPOINT = '/api/flashcards/judge';
  var disabledUntil = 0;         /* after a 503/429 the judge sits out for a minute */

  function judge(card, typed) {
    if (!card || !typed || !String(typed).trim()) return Promise.resolve(null);
    if (Date.now() < disabledUntil) return Promise.resolve(null);
    var body = { kind: card.kind || 'recall', front: card.front, answer: card.answer, typed: String(typed).slice(0, 600) };
    if (card.items && card.items.length) body.items = card.items;
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var t = ctrl ? setTimeout(function () { ctrl.abort(); }, 9000) : null;
    return fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) {
        if (r.status === 503 || r.status === 429) disabledUntil = Date.now() + 60000;
        return r.ok ? r.json() : null;
      })
      .then(function (d) { if (t) clearTimeout(t); return (d && d.verdict) ? d : null; })
      .catch(function () { if (t) clearTimeout(t); return null; });
  }

  /* the words a student sees for each verdict; a full sentence, no jargon */
  var WORDS = {
    right: { head: 'Right', line: 'That matches the answer.' },
    partly: { head: 'Nearly there', line: 'Part of it, not all of it. Read the answer, then move on.' },
    wrong: { head: 'Not this time', line: 'Read the answer and try it again later.' }
  };
  function words(verdict) { return WORDS[verdict] || WORDS.wrong; }

  /* which of the four card kinds to say on the badge and in the prompt */
  var KIND_LABEL = { recall: 'Question', term: 'What does it mean?', definition: 'Name the term', cloze: 'Fill the gap', list: 'Name them all' };
  var KIND_PLACEHOLDER = { recall: 'Type what you remember…', term: 'Type what it means…', definition: 'Type the term…', cloze: 'Type the missing word or words…', list: 'Type them, one per line or comma-separated…' };

  window.svRecall = { judge: judge, words: words, kindLabel: function (k) { return KIND_LABEL[k] || 'Question'; }, placeholder: function (k) { return KIND_PLACEHOLDER[k] || KIND_PLACEHOLDER.recall; } };
})();
