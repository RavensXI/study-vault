/**
 * Exam Countdown — shows days until next exam for the current subject.
 * Dismissible via localStorage. Works on browse, lesson, and practice pages.
 */
(function () {
  'use strict';

  var HIDE_KEY = 'studyvault-hide-countdown';
  var DATES_PATH = '/data/exam-dates-2026.json';

  // ---- Detect subject slug from URL ----
  function getSubjectSlug() {
    var path = window.location.pathname;
    // /browse/{subject}, /lesson/{subject}/..., /practice/{subject}/...
    var match = path.match(/^\/(browse|lesson|practice|guide)\/([^/]+)/);
    return match ? match[2] : null;
  }

  // ---- Detect exam board from page context ----
  function getExamBoard() {
    // lesson-loader sets this on the subject object; browse-loader has it too
    // Try reading from Supabase data already on page
    if (window._examBoard) return window._examBoard.toLowerCase();
    // Fallback: check meta or DOM for board info
    var boardEl = document.querySelector('[data-exam-board]');
    if (boardEl) return boardEl.getAttribute('data-exam-board').toLowerCase();
    return null;
  }

  // ---- Map subject slugs to exam-dates keys ----
  // Handles board-specific slugs like "english-literature-edexcel"
  function normaliseSlug(slug) {
    // Strip board suffix for multi-board subjects
    var base = slug.replace(/-(aqa|edexcel|ocr|eduqas|wjec)$/, '');
    // Map any aliases
    var aliases = {
      'mathematics': 'maths',
      'combined-science': 'science',
      'religious-studies': 'religious-education',
      'food-preparation-and-nutrition': 'food-technology',
      'food': 'food-technology'
    };
    return aliases[base] || base;
  }

  // ---- Detect board from slug suffix or SchoolSession ----
  function detectBoard(slug) {
    // Check slug suffix first (e.g. "english-literature-edexcel")
    var suffixMatch = slug.match(/-(aqa|edexcel|ocr|eduqas|wjec)$/);
    if (suffixMatch) return suffixMatch[1];

    // Check if board was set by loader
    var board = getExamBoard();
    if (board) return board;

    // Default to AQA for Unity school subjects
    if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive()) {
      return 'aqa';
    }

    return 'aqa'; // safe default
  }

  // ---- Find next upcoming exam ----
  function findNextExam(exams) {
    var now = new Date();
    now.setHours(0, 0, 0, 0);
    var upcoming = [];

    for (var i = 0; i < exams.length; i++) {
      var examDate = new Date(exams[i].date + 'T00:00:00');
      if (examDate >= now) {
        var diffMs = examDate - now;
        var diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
        upcoming.push({
          paper: exams[i].paper,
          date: exams[i].date,
          session: exams[i].session,
          days: diffDays
        });
      }
    }

    upcoming.sort(function (a, b) { return a.days - b.days; });
    return upcoming.length > 0 ? upcoming[0] : null;
  }

  // ---- Format date for display ----
  function formatDate(dateStr) {
    var d = new Date(dateStr + 'T00:00:00');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return days[d.getDay()] + ' ' + d.getDate() + ' ' + months[d.getMonth()];
  }

  // ---- Render the countdown banner ----
  function renderCountdown(exam) {
    var daysText;
    if (exam.days === 0) {
      daysText = '<strong>Today</strong>';
    } else if (exam.days === 1) {
      daysText = '<strong>Tomorrow</strong>';
    } else {
      daysText = '<strong>' + exam.days + ' days</strong>';
    }

    var sessionLabel = exam.session === 'am' ? 'morning' : 'afternoon';

    var banner = document.createElement('div');
    banner.className = 'exam-countdown';
    banner.innerHTML =
      '<div class="exam-countdown-inner">' +
        '<svg class="exam-countdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' +
        '<span class="exam-countdown-text">' +
          daysText + ' until ' + exam.paper +
          '<span class="exam-countdown-date"> — ' + formatDate(exam.date) + ' (' + sessionLabel + ')</span>' +
        '</span>' +
        '<button class="exam-countdown-hide" title="Hide countdown" aria-label="Hide exam countdown">&times;</button>' +
      '</div>';

    // Urgency classes
    if (exam.days <= 7) {
      banner.classList.add('exam-countdown-urgent');
    } else if (exam.days <= 21) {
      banner.classList.add('exam-countdown-soon');
    }

    // Hide button
    banner.querySelector('.exam-countdown-hide').addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      banner.classList.add('exam-countdown-hiding');
      setTimeout(function () {
        banner.remove();
      }, 300);
      localStorage.setItem(HIDE_KEY, 'true');
    });

    return banner;
  }

  // ---- Inject CSS ----
  function injectStyles() {
    if (document.getElementById('exam-countdown-styles')) return;
    var style = document.createElement('style');
    style.id = 'exam-countdown-styles';
    style.textContent =
      '.exam-countdown {' +
        'background: linear-gradient(135deg, #eff6ff, #f0fdf4);' +
        'border: 1px solid #bfdbfe;' +
        'border-radius: 12px;' +
        'padding: 0.6rem 1rem;' +
        'margin: 0 auto 1.25rem;' +
        'max-width: 700px;' +
        'animation: countdownSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);' +
        'font-family: Inter, system-ui, sans-serif;' +
      '}' +
      '.exam-countdown-inner {' +
        'display: flex;' +
        'align-items: center;' +
        'gap: 0.5rem;' +
      '}' +
      '.exam-countdown-icon {' +
        'width: 18px; height: 18px;' +
        'color: #2563eb;' +
        'flex-shrink: 0;' +
      '}' +
      '.exam-countdown-text {' +
        'flex: 1;' +
        'font-size: 0.85rem;' +
        'color: #1e3a5f;' +
        'line-height: 1.4;' +
      '}' +
      '.exam-countdown-text strong {' +
        'color: #1d4ed8;' +
        'font-weight: 700;' +
      '}' +
      '.exam-countdown-date {' +
        'color: #64748b;' +
        'font-size: 0.8rem;' +
      '}' +
      '.exam-countdown-hide {' +
        'background: none;' +
        'border: none;' +
        'font-size: 1.2rem;' +
        'color: #94a3b8;' +
        'cursor: pointer;' +
        'padding: 0 0.25rem;' +
        'line-height: 1;' +
        'transition: color 0.2s;' +
      '}' +
      '.exam-countdown-hide:hover { color: #475569; }' +
      /* Soon (< 3 weeks) */
      '.exam-countdown-soon {' +
        'background: linear-gradient(135deg, #fefce8, #fff7ed);' +
        'border-color: #fde68a;' +
      '}' +
      '.exam-countdown-soon .exam-countdown-icon { color: #d97706; }' +
      '.exam-countdown-soon .exam-countdown-text strong { color: #b45309; }' +
      /* Urgent (< 1 week) */
      '.exam-countdown-urgent {' +
        'background: linear-gradient(135deg, #fef2f2, #fff1f2);' +
        'border-color: #fca5a5;' +
      '}' +
      '.exam-countdown-urgent .exam-countdown-icon { color: #dc2626; }' +
      '.exam-countdown-urgent .exam-countdown-text strong { color: #b91c1c; }' +
      /* Hiding animation */
      '.exam-countdown-hiding {' +
        'opacity: 0;' +
        'transform: translateY(-8px);' +
        'transition: opacity 0.3s, transform 0.3s;' +
      '}' +
      '@keyframes countdownSlideIn {' +
        'from { opacity: 0; transform: translateY(-10px); }' +
        'to { opacity: 1; transform: translateY(0); }' +
      '}' +
      /* Dark mode */
      '.dark-mode .exam-countdown {' +
        'background: linear-gradient(135deg, #1e293b, #1a2332);' +
        'border-color: #334155;' +
      '}' +
      '.dark-mode .exam-countdown-text { color: #cbd5e1; }' +
      '.dark-mode .exam-countdown-text strong { color: #60a5fa; }' +
      '.dark-mode .exam-countdown-date { color: #94a3b8; }' +
      '.dark-mode .exam-countdown-hide { color: #64748b; }' +
      '.dark-mode .exam-countdown-hide:hover { color: #94a3b8; }' +
      '.dark-mode .exam-countdown-soon {' +
        'background: linear-gradient(135deg, #292524, #2a2015);' +
        'border-color: #854d0e;' +
      '}' +
      '.dark-mode .exam-countdown-soon .exam-countdown-icon { color: #fbbf24; }' +
      '.dark-mode .exam-countdown-soon .exam-countdown-text strong { color: #fbbf24; }' +
      '.dark-mode .exam-countdown-urgent {' +
        'background: linear-gradient(135deg, #2a1515, #2d1a1a);' +
        'border-color: #991b1b;' +
      '}' +
      '.dark-mode .exam-countdown-urgent .exam-countdown-icon { color: #f87171; }' +
      '.dark-mode .exam-countdown-urgent .exam-countdown-text strong { color: #f87171; }' +
      /* Mobile */
      '@media (max-width: 600px) {' +
        '.exam-countdown { margin: 0 1rem 1rem; }' +
        '.exam-countdown-date { display: block; margin-top: 0.15rem; }' +
      '}';
    document.head.appendChild(style);
  }

  // ---- Main ----
  async function init() {
    // Check if hidden
    if (localStorage.getItem(HIDE_KEY) === 'true') return;

    var slug = getSubjectSlug();
    if (!slug) return;

    var board = detectBoard(slug);
    var normSlug = normaliseSlug(slug);

    // Fetch exam dates
    var resp;
    try {
      resp = await fetch(DATES_PATH);
      if (!resp.ok) return;
    } catch (e) { return; }

    var allDates = await resp.json();

    // Look up exams for this board + subject
    var boardDates = allDates[board];
    if (!boardDates) boardDates = allDates['aqa']; // fallback
    var exams = boardDates[normSlug];
    if (!exams || exams.length === 0) return;

    // Find next upcoming exam
    var next = findNextExam(exams);
    if (!next) return; // all exams have passed

    // Render
    injectStyles();
    var banner = renderCountdown(next);

    // Insert after hero section on browse pages, or after header on lesson/practice pages
    var hero = document.querySelector('.hero');
    if (hero && hero.nextSibling) {
      hero.parentNode.insertBefore(banner, hero.nextSibling);
    } else {
      // Lesson/practice page — insert at top of main content
      var main = document.querySelector('.lesson-content') ||
                 document.querySelector('#practice-page') ||
                 document.querySelector('.content');
      if (main) {
        main.insertBefore(banner, main.firstChild);
      }
    }
  }

  // ---- Expose for loaders to call after content is ready ----
  window.initExamCountdown = init;

  // Also auto-init after a short delay (in case no loader calls it)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(init, 500);
    });
  } else {
    setTimeout(init, 500);
  }
})();
