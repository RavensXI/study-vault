/* Page titles for Google results, browser tabs and link previews (Tom, 28 Sep 2026).
   Shared by api/seo.js (the server-written <head>) and the page loaders (document.title), so
   the title never changes when a page finishes loading. The titles on the pages themselves
   are untouched: this is only the <title> text.

   Search Console showed our lessons on page 1 of Google with ~0.5% of people clicking. The old
   titles ran to 68-105 characters, so Google cut them after "GCSE English…", and a set-text
   lesson ("Act 3: The Ending and the Phone Call") never named the book people searched for.
   Now: the book first (English Literature and Drama), then the lesson, then the shortest
   course label that keeps the whole title within the ~60 characters Google shows. */
(function (root) {
  var MAX = 65;   // Google shows ~600px, about 60-65 characters
  var SET_TEXT = /^(english literature|drama)$/i;
  var SHORT = {
    'Food Preparation and Nutrition': 'Food & Nutrition', 'Design and Technology': 'D&T',
    'Religious Studies': 'RS', 'Physical Education': 'PE', 'English Literature': 'English Lit',
    'English Language': 'English Language', 'Construction and the Built Environment': 'Construction',
    'Engineering Programmable Systems': 'Engineering', 'Engineering Manufacture': 'Engineering',
    'Combined Science A (Gateway)': 'Combined Science', 'Combined Science B (Twenty First Century)': 'Combined Science',
    'Separate Sciences A (Gateway)': 'Separate Sciences', 'Separate Sciences B (Twenty First Century)': 'Separate Sciences',
    'Sport and Coaching Principles': 'Sport', 'Health and Social Care': 'Health & Social Care'
  };
  function board(b) { return String(b || '').replace(/^Pearson /, '').replace(/ \/ WJEC$/, ''); }
  function norm(s) { return String(s || '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').trim(); }

  // "Blood Brothers by Willy Russell" -> "Blood Brothers"
  // "Poetry: Youth and Age" -> "Youth and Age"
  function textName(unitName) { return String(unitName || '').replace(/\s+by\s+[A-Z][\s\S]*$/, '').replace(/^[^:]*:\s*/, '').trim(); }

  function label(head, name, b, setText) {
    var n = String(name || ''), s = SHORT[n] || n, bb = board(b);
    var c = setText ? ['GCSE ' + n + (bb ? ' ' + bb : ''), bb ? 'GCSE ' + bb : 'GCSE', 'GCSE']
                    : ['GCSE ' + n + (bb ? ' ' + bb : ''), 'GCSE ' + s + (bb ? ' ' + bb : ''), 'GCSE ' + s, 'GCSE'];
    for (var i = 0; i < c.length; i++) if ((head + ' | ' + c[i]).length <= MAX) return c[i];
    return 'GCSE';
  }

  // A lesson or practice page. unitName is optional (without it the book is not prefixed).
  function lessonTitle(title, unitName, subjectName, examBoard) {
    var head = String(title || '');
    var setText = SET_TEXT.test(String(subjectName || ''));
    var book = setText ? textName(unitName) : '';
    if (book && norm(head).indexOf(norm(book)) === -1) head = book + (head.indexOf(':') !== -1 ? ' ' : ': ') + head;
    return head + ' | ' + label(head, subjectName, examBoard, setText);
  }

  // A unit page, a subject page or a revision-technique guide.
  function unitTitle(unitName, subjectName, examBoard) {
    return String(unitName || '') + ' | ' + label(String(unitName || ''), subjectName, examBoard, false);
  }
  function subjectTitle(subjectName, examBoard) {
    var t = 'GCSE ' + subjectName + (examBoard ? ' ' + board(examBoard) : '') + ' revision';
    return (t + ' | StudyVault').length <= MAX ? t + ' | StudyVault' : t;
  }

  // What the page gives, after the lesson's own one-line description (Google shows ~155 characters).
  function lessonDescription(description, kind) {
    var tail = kind === 'practice' ? 'Free GCSE practice questions, marked as you answer.'
             : kind === 'listening' ? 'Free GCSE guided listening, with the music and exam points.'
             : 'Free GCSE revision notes, practice questions and flashcards.';
    var d = String(description || '').trim();
    if (d && !/[.!?]$/.test(d)) d += '.';
    if (!d) return tail;
    // a long description stays whole rather than have the tail cut off mid-sentence in the result
    if ((d + ' ' + tail).length <= 160) return d + ' ' + tail;
    return (d + ' Free GCSE revision.').length <= 160 ? d + ' Free GCSE revision.' : d;
  }

  var api = { lessonTitle: lessonTitle, unitTitle: unitTitle, subjectTitle: subjectTitle, lessonDescription: lessonDescription };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.svSeo = api;
})(this);
