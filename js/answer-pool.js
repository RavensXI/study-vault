/* The anonymous answer pool, pupil side (26 Sep 2026; server side api/pool.js).

   svPool.add(key, {a, v})     a short typed answer and the verdict ('right' | 'wrong' | 'partly');
                               over 60 characters it is not counted
   svPool.add(key, {chose, v}) a chosen option (the site's own text), shortened to 60 characters
   svPool.add(key, {got, of})  the mark an AI-marked written answer received. The
                               writing itself is never sent.

   Question keys (five parts, all lower case):
     subject/unit/lesson/bronze|silver|gold/i   practice problem bank (i = place in the stored tier);
                                                answer '*' = a multi-part control (only the verdict
                                                counts); 'q:<quality>' = AI-marked writing (band only)
     subject/unit/lesson/kc/i                   knowledge check (quick quiz) question i; '*' for match-ups
     subject/unit/lesson/pq/i                   end-of-lesson exam question i: the MARK only (got/of)
     subject/unit/lesson/fcq/i                  typed flashcard from the lesson's question deck, card i
     subject/unit/lesson/fcr/i                  typed flashcard from the lesson's recall cards, card i
   (Interactive widgets are not counted: they publish mastery, not each choice.)

   Nothing identifies the pupil: rows carry only the key, the answer or mark and the verdict.
   Rows queue in memory and go with sendBeacon when the page is hidden or left, or every 20.
   Sends nothing for staff (admin sign-in, /admin, /teacher), demo pupils (?demo= or a demo
   profile), Demo High School and the test schools, or an answer the safeguarding check
   flagged (callers pass {flagged: true}, or simply do not call). A missing /api/pool is
   harmless: the beacon just fails. */
(function () {
  'use strict';
  var SKIP_SCHOOLS = ['8ab707cc-7e3d-4243-bb12-315a29a94163',   // Demo High School
                      '99bd48fd-f9c6-4ea4-b4a0-2d0b5c808614',   // Fork Test School
                      '88f0130d-372d-4f1c-86b4-7670b096bc7a'];  // Safeguarding Test School

  function parse(raw) { try { return raw ? JSON.parse(raw) : null; } catch (e) { return null; } }

  function off() {
    try {
      if (/^\/(admin|teacher)(\/|$)/.test(location.pathname)) return true;
      if (/[?&]demo=/.test(location.search) || localStorage.getItem('sv-demo-student')) return true;
      var auth = parse(sessionStorage.getItem('studyvault-auth')) || parse(localStorage.getItem('studyvault-auth'));
      if (auth && auth.role && auth.role !== 'student') return true;
      var school = parse(sessionStorage.getItem('studyvault-school')) || parse(localStorage.getItem('sv-school'));
      if (school && SKIP_SCHOOLS.indexOf(school.school_id) !== -1) return true;
    } catch (e) { return true; }
    return false;
  }

  var queue = [];
  function flush() {
    if (!queue.length) return;
    var rows = queue.splice(0, 50);
    try {
      var body = new Blob([JSON.stringify({ rows: rows })], { type: 'application/json' });
      if (!(navigator.sendBeacon && navigator.sendBeacon('/api/pool', body))) {
        fetch('/api/pool', { method: 'POST', headers: { 'Content-Type': 'application/json' },
                             body: JSON.stringify({ rows: rows }), keepalive: true }).catch(function () {});
      }
    } catch (e) {}
    if (queue.length) flush();
  }

  function slug(s) { return String(s == null ? '' : s).toLowerCase(); }

  window.svPool = {
    key: function (subject, unit, lesson, set, i) {
      return [slug(subject), slug(unit), parseInt(lesson, 10) || 0, slug(set), parseInt(i, 10) || 0].join('/');
    },
    add: function (key, d) {
      if (!key || !d || d.flagged || off()) return;
      var row;
      if (d.of != null) row = { k: key, got: d.got, of: d.of };
      else {
        /* a chosen option is the site's own wording, so a long one is shortened; a TYPED answer
           longer than 60 characters is the pupil's own writing and is not counted at all */
        var chosen = d.a == null && d.chose != null;
        var a = chosen ? d.chose : d.a;
        if (Array.isArray(a)) a = a.join(' ');
        a = String(a == null ? '' : a).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
        if (chosen) a = a.slice(0, 60).trim();
        if (!a || a.length > 60 || ['right', 'wrong', 'partly'].indexOf(d.v) === -1) return;
        row = { k: key, a: a, v: d.v };
      }
      queue.push(row);
      if (queue.length >= 20) flush();
    },
    flush: flush
  };

  window.addEventListener('pagehide', flush);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flush(); });
})();
