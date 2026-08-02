/**
 * Exam Countdown — compact pill showing days until next exam.
 * Practice/lesson: sits in the header bar's left dead space.
 * Browse: sits inside the hero section under the title.
 * Dismissible via localStorage.
 */
(function () {
  'use strict';

  var HIDE_KEY = 'studyvault-hide-countdown';
  var DATES_PATH = (new Date() < new Date('2026-08-21'))
    ? '/data/exam-dates-2026.json' : '/data/exam-dates-2027.json';
  var DATES_YEAR = DATES_PATH.indexOf('2027') !== -1 ? 2027 : 2026;

  function getSubjectSlug() {
    var match = window.location.pathname.match(/^\/(browse|lesson|practice|guide)\/([^/]+)/);
    return match ? match[2] : null;
  }

  function getPageType() {
    var match = window.location.pathname.match(/^\/(browse|lesson|practice|guide)\//);
    return match ? match[1] : null;
  }

  function getExamBoard() {
    if (window._examBoard) return window._examBoard.toLowerCase();
    return null;
  }

  function normaliseSlug(slug) {
    // Strip board suffix plus optional single-letter spec variant (e.g.
    // "-edexcel-a", "-edexcel-b") so both Geography Edexcel A and B
    // resolve to the same "geography" key in the exam-dates JSON.
    var base = slug.replace(/-(aqa|edexcel|ocr|eduqas|wjec|ncfe)(-[a-z])?$/, '');
    var aliases = {
      'mathematics': 'maths',
      'combined-science': 'science',
      'science-severnvale': 'science',
      'religious-studies': 'religious-education',
      'food-preparation-and-nutrition': 'food-technology',
      'food': 'food-technology',
      'gcse-music': 'music'
    };
    return aliases[base] || base;
  }

  function detectBoard(slug) {
    // Same regex as normaliseSlug — captures the board name even when a
    // spec-variant letter follows (e.g. "geography-edexcel-a").
    var suffixMatch = slug.match(/-(aqa|edexcel|ocr|eduqas|wjec|ncfe)(-[a-z])?$/);
    if (suffixMatch) return suffixMatch[1];
    var board = getExamBoard();
    if (board) return board;
    return 'aqa';
  }

  function findNextExam(exams) {
    var now = new Date();
    now.setHours(0, 0, 0, 0);
    var upcoming = [];
    for (var i = 0; i < exams.length; i++) {
      var examDate = new Date(exams[i].date + 'T00:00:00');
      if (examDate >= now) {
        var diffDays = Math.ceil((examDate - now) / 86400000);
        upcoming.push({ paper: exams[i].paper, date: exams[i].date, session: exams[i].session, days: diffDays });
      }
    }
    upcoming.sort(function (a, b) { return a.days - b.days; });
    return upcoming.length > 0 ? upcoming[0] : null;
  }

  function formatDate(dateStr) {
    var d = new Date(dateStr + 'T00:00:00');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return days[d.getDay()] + ' ' + d.getDate() + ' ' + months[d.getMonth()];
  }

  function getUrgencyClass(days) {
    if (days <= 7) return 'exam-cd-urgent';
    if (days <= 30) return 'exam-cd-soon';
    return '';
  }

  function renderPill(exam) {
    var daysLabel = exam.days === 0 ? 'Today!' : exam.days === 1 ? 'Tomorrow' : exam.days + 'd';
    var sessionLabel = exam.session === 'am' ? 'AM' : 'PM';

    var pill = document.createElement('div');
    pill.className = 'exam-cd ' + getUrgencyClass(exam.days);
    pill.innerHTML =
      '<svg class="exam-cd-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' +
      '<span class="exam-cd-days">' + daysLabel + '</span>' +
      '<span class="exam-cd-label">' + exam.paper + '</span>' +
      '<span class="exam-cd-date">' + formatDate(exam.date) + ' ' + sessionLabel + '</span>' +
      '<button class="exam-cd-x" title="Hide countdown" aria-label="Hide">&times;</button>';

    pill.querySelector('.exam-cd-x').addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      pill.style.opacity = '0';
      pill.style.transform = 'translateY(-4px)';
      setTimeout(function () { pill.remove(); }, 250);
      sessionStorage.setItem(HIDE_KEY, 'true');
    });

    return pill;
  }

  function injectStyles() {
    if (document.getElementById('exam-cd-css')) return;
    var s = document.createElement('style');
    s.id = 'exam-cd-css';
    s.textContent =
      /* Base pill */
      '.exam-cd{display:inline-flex;align-items:center;gap:0.35rem;font-family:Inter,system-ui,sans-serif;' +
        'font-size:0.75rem;background:#f0f7ff;border:1px solid #c7deff;border-radius:999px;' +
        'padding:0.25rem 0.6rem 0.25rem 0.45rem;color:#1e3a5f;white-space:nowrap;' +
        'transition:opacity 0.25s,transform 0.25s;animation:examCdIn 0.35s cubic-bezier(0.16,1,0.3,1)}' +
      '.exam-cd-clock{width:13px;height:13px;color:#2563eb;flex-shrink:0}' +
      '.exam-cd-days{font-weight:700;color:#1d4ed8;font-size:0.78rem}' +
      '.exam-cd-label{color:#475569;font-weight:500}' +
      '.exam-cd-date{color:#94a3b8;font-size:0.7rem}' +
      '.exam-cd-x{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1rem;' +
        'line-height:1;padding:0 0 0 0.15rem;transition:color 0.15s}' +
      '.exam-cd-x:hover{color:#475569}' +
      /* Soon (<30 days) */
      '.exam-cd-soon{background:#fefce8;border-color:#fde68a}' +
      '.exam-cd-soon .exam-cd-clock{color:#d97706}' +
      '.exam-cd-soon .exam-cd-days{color:#b45309}' +
      /* Urgent (<7 days) */
      '.exam-cd-urgent{background:#fef2f2;border-color:#fca5a5}' +
      '.exam-cd-urgent .exam-cd-clock{color:#dc2626}' +
      '.exam-cd-urgent .exam-cd-days{color:#b91c1c}' +
      /* Header placement (practice pages — left panel dead space) */
      '.exam-cd-header{position:absolute;left:1rem;top:50%;transform:translateY(-50%)}' +
      /* Lesson page — above the title */
      '.exam-cd-lesson{margin-bottom:0.5rem}' +
      /* Hero placement (browse pages) */
      '.exam-cd-hero{margin-top:0.75rem}' +
      /* Dark mode */
      '.dark-mode .exam-cd{background:#1e293b;border-color:#334155;color:#cbd5e1}' +
      '.dark-mode .exam-cd-days{color:#60a5fa}' +
      '.dark-mode .exam-cd-clock{color:#60a5fa}' +
      '.dark-mode .exam-cd-label{color:#94a3b8}' +
      '.dark-mode .exam-cd-date{color:#64748b}' +
      '.dark-mode .exam-cd-x{color:#64748b}' +
      '.dark-mode .exam-cd-x:hover{color:#94a3b8}' +
      '.dark-mode .exam-cd-soon{background:#292524;border-color:#854d0e}' +
      '.dark-mode .exam-cd-soon .exam-cd-clock,.dark-mode .exam-cd-soon .exam-cd-days{color:#fbbf24}' +
      '.dark-mode .exam-cd-urgent{background:#2a1515;border-color:#991b1b}' +
      '.dark-mode .exam-cd-urgent .exam-cd-clock,.dark-mode .exam-cd-urgent .exam-cd-days{color:#f87171}' +
      '@keyframes examCdIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}' +
      /* Mobile: hide date to save space, keep days + paper */
      '@media(max-width:600px){.exam-cd-date{display:none}.exam-cd-header{left:0.5rem;font-size:0.7rem}}' +
      /* Very small: hide label too, just show days */
      '@media(max-width:400px){.exam-cd-label{display:none}}';
    document.head.appendChild(s);
  }

  var _initInFlight = false;

  async function init() {
    if (sessionStorage.getItem(HIDE_KEY) === 'true') return;
    // Idempotency: if a pill is already in the DOM, do nothing.
    if (document.querySelector('.exam-cd')) return;
    // Async race guard: prevents two concurrent init calls (e.g. the 500ms
    // auto-fire + a loader's explicit call) from both passing the DOM check
    // before either has rendered, then both rendering a pill after fetch
    // resolves. Without this, dynamic pages reliably end up with two pills.
    if (_initInFlight) return;
    _initInFlight = true;

    try {
      var cohortYear = parseInt(localStorage.getItem('studyvault-exam-year') || '', 10);
      if (cohortYear && cohortYear > DATES_YEAR) return;
      var slug = getSubjectSlug();
      if (!slug) return;
      var pageType = getPageType();

      var board = detectBoard(slug);
      var normSlug = normaliseSlug(slug);

      var resp;
      try { resp = await fetch(DATES_PATH); if (!resp.ok) return; } catch (e) { return; }
      var allDates = await resp.json();

      var boardDates = allDates[board] || allDates['aqa'];
      var exams = boardDates[normSlug];
      if (!exams || exams.length === 0) return;

      var next = findNextExam(exams);
      if (!next) return;

      // Final defensive check before mutating the DOM. Even with the
      // in-flight flag, if a previous init wrote a pill THEN finished
      // (clearing the flag) and another init fires before we get here,
      // we still want to bail rather than stack pills.
      if (document.querySelector('.exam-cd')) return;

      injectStyles();
      var pill = renderPill(next);

      if (pageType === 'practice') {
        // Practice page — header's left panel dead space
        pill.classList.add('exam-cd-header');
        var header = document.querySelector('.page-header');
        if (header) {
          header.style.position = 'relative';
          header.appendChild(pill);
        }
      } else if (pageType === 'lesson') {
        // Article lesson — above the lesson title
        pill.classList.add('exam-cd-lesson');
        var lessonHeader = document.querySelector('.lesson-header');
        if (lessonHeader) {
          lessonHeader.insertBefore(pill, lessonHeader.firstChild);
        }
      } else {
        // Browse page — place inside hero section
        pill.classList.add('exam-cd-hero');
        var hero = document.querySelector('.hero');
        if (hero) {
          hero.appendChild(pill);
        }
      }
    } finally {
      _initInFlight = false;
    }
  }

  window.initExamCountdown = init;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(init, 500); });
  } else {
    setTimeout(init, 500);
  }
})();
