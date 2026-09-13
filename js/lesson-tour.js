/* "Show me around" for a lesson page (Tom, 13 Sep 2026). Replaces the old
   click-through spotlight tour in js/reader-skin.js: short muted clips of a
   real lesson, one per feature, each with a plain-language description.
   Opens once (sv-lesson-tour-v2, account-synced) on the first ordinary lesson,
   then from "Replay tour" in the side panel; ?tour=1 forces, ?tour=0 / ?notour=1
   suppress. Never inside an embed, and never on a listening lesson (its docked
   player covers the page). Clips: scripts/dashboard_tour/record.py --set lesson. */
(function () {
  'use strict';
  var STEPS = [
    { id: 'read', title: 'Make the page comfortable to read',
      text: 'The bar above the lesson sets up how the page looks. Tap "Read your way" for bigger text, more space between the lines, or a font that is easier to read. Dark mode and colour tints are here too. Whatever you choose stays on for every page.' },
    { id: 'listen', title: 'Have it read to you',
      text: 'Press play and the lesson is read aloud while you follow the words. If there is a podcast on this topic, switch to it using the tab above the player. It keeps playing if you lock your phone.' },
    { id: 'text', title: 'Help inside the text',
      text: 'Underlined words show what they mean when you tap them. The boxes hold the facts you must know. The little lightbulbs give you a tip on how to revise that bit.' },
    { id: 'stuck', title: 'Stuck on a bit?',
      text: 'Tap any paragraph and three choices appear. Simplify rewrites it in easier words. Explain says it a different way. Ask the tutor lets you ask a question about it.' },
    { id: 'quiz', title: 'The quick quiz',
      text: 'Five quick questions on the lesson. You are told straight away which ones you got right, and why the others were wrong. Passing the quiz is one of the things that finishes the lesson.' },
    { id: 'flashcards', title: 'Flashcards for this lesson',
      text: 'Five question-and-answer cards made from this lesson. Tap a card to flip it, then say if you got it right. The ones you get wrong come round again sooner. They also join your daily flashcards on the dashboard.' },
    { id: 'practice', title: 'Exam questions, marked for you',
      text: 'Real exam-style questions with marks. Write your answer and tap "AI mark my answer". You get a mark out of the total and feedback on what would have earned more. Half marks or better finishes this part of the lesson.' },
    { id: 'tutor', title: 'Ask the tutor',
      text: 'A tutor that knows this lesson. Ask it anything about the topic in your own words and it answers in plain English. It will not write your exam answer for you.' },
    { id: 'media', title: 'Video and more',
      text: 'A short video explains the lesson. "Related media" has hand-picked videos, articles and podcasts if you want to go further.' },
    { id: 'focus', title: 'Focus mode',
      text: 'Focus mode fades everything except the paragraph you are reading, so your eyes stay on one thing at a time. Tap it again to turn it off.' },
    { id: 'progress', title: 'Finishing a lesson',
      text: 'The icons at the top of the side panel show what you have done in this lesson: the quiz, flashcards, an exam question, the video, the podcast. Do enough of them and the lesson is finished. Then "Next lesson" takes you on to the next one.' }
  ];
  var dq = new URLSearchParams(location.search);
  var tour = window.svTourPlayer ? svTourPlayer({ key: 'sv-lesson-tour-v2', manifest: '/assets/tour/lesson/manifest.json', kicker: 'Show me around', steps: STEPS }) : null;
  if (!tour) return;
  window.svLessonTour = tour;
  function listening() { return !!document.querySelector('.sv-listening') || document.body.classList.contains('sv-listening-mode'); }
  function boot() {
    if (window.SV_EMBED) return;
    if (dq.get('tour') === '1') { setTimeout(function () { tour.open(0); }, 1200); return; }
    if (dq.get('tour') === '0' || dq.get('notour') === '1') { try { localStorage.setItem('sv-lesson-tour-v2', '1'); } catch (e) {} return; }
    if (tour.seen()) return;
    /* wait for the lesson to land (the loader injects it), then show them round once */
    (function poll(n) {
      if (tour.seen()) return;
      if (document.getElementById('lesson-title') && document.getElementById('lesson-title').textContent.trim() && document.querySelector('.sv-panel')) {
        if (listening()) return;                       /* runs on their next ordinary lesson instead */
        setTimeout(function () { if (!tour.seen()) tour.open(0); }, 1400); return;
      }
      if (n > 0) setTimeout(function () { poll(n - 1); }, 500);
    })(40);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
