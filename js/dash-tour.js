/* "Show me around": the dashboard tour (Tom, 13 Sep 2026).
   Short muted clips of the demo students' dashboards, one per feature, with a
   title and two sentences each — so a new student sees the revisit slot, the
   quick check, a rest day and the rest even though their own dashboard has
   none of those states yet. Opens once on the first dashboard visit
   (sv-dash-tour-v1, account-synced), then from "Show me around" in the footer
   and the avatar menu; ?tour=1 forces it. Clips are recorded by
   scripts/dashboard_tour/record.py into assets/tour/ (manifest.json); the
   modal itself is js/tour-player.js, shared with the lesson tour. */
(function () {
  'use strict';
  var KEY = 'sv-dash-tour-v1';
  var STEPS = [
    { id: 'plan', title: 'Your plan for today',
      text: 'Every day, StudyVault picks three short things for you to do: a quick recap, one lesson, and a few flashcards. Press Start and it takes you through them one at a time. Most days it takes about 20 minutes.' },
    { id: 'revisit', title: 'Revisit: a quick recap',
      text: 'The first thing each day is a handful of questions on lessons you did a while ago. This is what stops you forgetting them. Get them right and you move on. Get them wrong and that lesson goes back on your list so you can do it again.' },
    { id: 'quickcheck', title: 'Already know a topic? Prove it and skip ahead',
      text: 'If you told us you feel confident about a topic, a lesson on it starts with a quick check instead of the full lesson. Get at least 4 out of 5 on the quiz, then at least half marks on an exam question, and that lesson is ticked off without reading it. If not, you do the lesson as normal.' },
    { id: 'books', title: 'Your subjects are the books',
      text: 'Each book on the shelf is one of your subjects. Tap a book to see its topics, then tap a topic to see its lessons. You can start any lesson from here. A book fills with colour from the bottom as you work through it.' },
    { id: 'rings', title: 'The coloured outlines',
      text: 'Each topic has an outline that tells you how well you know it right now. Green means it is secure. Amber means you are getting there. Red means it needs work. The colours change by themselves as you do quizzes, flashcards and exam questions.' },
    { id: 'week', title: 'How your week is going',
      text: 'Tap "This week" to see what you have done: the days you revised, the lessons you finished, the quizzes you passed and the flashcards you got right. On a Monday it shows you last week first, so you can see how it went.' },
    { id: 'flashcards', title: 'Flashcards',
      text: 'Flashcards are quick question-and-answer cards from the lessons you have done. Tap a card to see the answer, then say whether you got it right. Cards you get wrong come back sooner. Cards you know come back less often.' },
    { id: 'podcast', title: 'Listen while you do something else',
      text: 'The play button at the top plays a short podcast about one of your topics, a bit like a radio show. Use the skip button to change to another one. It keeps playing if you lock your phone, and finishing one counts as work on that lesson.' },
    { id: 'timer', title: 'The revision timer',
      text: 'Tap the timer at the top and choose 15, 25 or 45 minutes. It keeps counting as you move between pages, and it chimes when your time is up. Useful for deciding to do "just 25 minutes" and then stopping.' },
    { id: 'restday', title: 'Days off',
      text: 'When you set up your plan, you choose which days you revise. On your days off there is nothing you have to do. But if you fancy it, your plan shows what is coming up next, so you can get ahead. Anything you do on a day off is a bonus.' },
    { id: 'planner', title: 'Your exam countdown',
      text: 'The number at the top is how many days until your first exam. Tap it to see your whole plan on a calendar, right up to your last exam, including your days off and holidays. You can change your revising days and how long you revise here too.' },
    { id: 'reading', title: 'Make it easier on your eyes',
      text: 'Tap the moon at the top to switch to dark mode, make the text bigger, change to an easier-to-read font, or put a colour tint over the page. Whatever you pick stays on across every page, including the lessons.' }
  ];

  var dq = new URLSearchParams(location.search);
  var tour = window.svTourPlayer ? svTourPlayer({ key: KEY, manifest: '/assets/tour/manifest.json', kicker: 'Show me around', steps: STEPS }) : null;
  if (!tour) return;
  function open(at) { tour.open(at); }
  function close() { tour.close(); }
  function g(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  window.svDashTour = { open: open, close: close };

  /* doors: the footer link (every dashboard), the avatar menu item (signed in — see dash-data.js) */
  function doors() {
    var row = document.querySelector('.legalrow');
    if (row && !row.querySelector('.tourlink')) {
      var a = document.createElement('a'); a.href = '#'; a.className = 'tourlink'; a.textContent = 'Show me around';
      a.addEventListener('click', function (e) { e.preventDefault(); open(0); });
      row.insertBefore(document.createTextNode(' · '), row.firstChild); row.insertBefore(a, row.firstChild);
    }
  }
  function boot() {
    doors();
    if (dq.get('tour') === '1') { setTimeout(function () { open(0); }, 900); return; }
    if (dq.get('demo') || dq.get('arrange') || dq.get('tour') === '0') return;
    if (g(KEY)) return;
    /* first dashboard visit: let the page settle, then show them round once */
    setTimeout(function () { if (!g(KEY)) open(0); }, 1600);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
