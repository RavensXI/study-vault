/**
 * School session utility — shared across all page loaders.
 * Stores the student's school context in sessionStorage.
 */
(function () {
  var KEY = 'studyvault-school';
  /* The account copy of a class-derived school session. It syncs with the account
     (js/account-sync.js whitelist), so a student who joined a class on one device is
     routed to the school's lessons on every device. Session storage is still what the
     loaders read; this key seeds it on every page load. */
  var ACCOUNT_KEY = 'sv-school';
  var TOKEN_KEY = 'sb-baipckgywpnwapobwtsy-auth-token';
  var CLASS_SUBJECTS_KEY = 'sv-class-subjects';   /* the subjects of the student's classes: [{slug, school?}] */

  /* bespoke slug -> wizard family, for the dashboard's subject-to-slug step */
  var FAMILY = { 'history': 'history', 'geography': 'geog', 'science': 'science', 'separate-sciences': 'triple',
    'english-literature': 'lit', 'english-language': 'lang', 'religious-studies': 'rs', 'religious-education': 'rs',
    'computer-science': 'cs', 'business': 'business', 'design-technology': 'dt', 'drama': 'drama',
    'gcse-music': 'music', 'music': 'music', 'food-preparation-and-nutrition': 'food', 'food-technology': 'food',
    'french': 'french', 'spanish': 'spanish', 'german': 'german', 'sport-science': 'pe', 'creative-imedia': 'it',
    'maths': 'maths', 'science-severnvale': 'science' };

  window.SchoolSession = {
    get: function () {
      try {
        var raw = sessionStorage.getItem(KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    },

    set: function (data) {
      sessionStorage.setItem(KEY, JSON.stringify(data));
    },

    clear: function () {
      sessionStorage.removeItem(KEY);
    },

    isActive: function () {
      return this.get() !== null;
    },

    getSchoolId: function () {
      var s = this.get();
      return s ? s.school_id : null;
    },

    /** The school's bespoke slug for a wizard family ('history' -> 'history'), or null. */
    bespokeFor: function (family) {
      var s = this.get();
      if (!s || !s.bespoke_subjects) return null;
      for (var i = 0; i < s.bespoke_subjects.length; i++) {
        if (FAMILY[s.bespoke_subjects[i]] === family) return s.bespoke_subjects[i];
      }
      return null;
    },
    familyOf: function (slug) { return FAMILY[slug] || null; },

    /** Seed the tab's session from the account copy. Runs at script load, before any
        loader, so the very first query on a new tab already targets the school. */
    fromAccount: function () {
      try {
        if (!this.isActive()) {
          var raw = localStorage.getItem(ACCOUNT_KEY);
          if (raw) { var s = JSON.parse(raw); if (s && s.school_id) this.set(s); }
        }
      } catch (e) {}
      /* what this page was built against; any later answer that differs means a reload */
      var cur = this.get(); this._booted = cur ? cur.school_id : null;
    },

    /* the page built its lists against _booted; if the account copy now says something
       else (account sync delivered the key after load, or a class was joined), rebuild */
    rebootIfChanged: function () {
      var acc = null; try { acc = JSON.parse(localStorage.getItem(ACCOUNT_KEY) || 'null'); } catch (e) {}
      var cur = this.get();
      if (cur && !cur.via) return;                 /* a real school sign-in is never overridden */
      var want = acc && acc.school_id ? acc.school_id : null;
      if (want !== (this._booted || null)) {
        if (acc && acc.school_id) this.set(acc); else if (cur && cur.via === 'class') this.clear();
        location.reload();
      }
    },

    /** Ask the server which classes the signed-in student is in and route them to
        their school's lessons. Cheap (one call), so it runs on every page load in the
        background; the page reloads only when the answer changes from nothing to a
        school, or from one school to none. Class-derived sessions never override a
        session set by a school sign-in (SSO), which carries no `via`. */
    refreshFromClasses: function (opts) {
      opts = opts || {};
      var tok = null;
      try { var raw = JSON.parse(localStorage.getItem(TOKEN_KEY) || 'null'); if (raw && raw.access_token) tok = raw.access_token; } catch (e) {}
      if (!tok) return Promise.resolve(null);
      var self = this;
      return fetch('/api/class/mine', { headers: { 'Authorization': 'Bearer ' + tok } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d) return null;
          var had = null; try { had = JSON.parse(localStorage.getItem(ACCOUNT_KEY) || 'null'); } catch (e) {}
          var now = d.school || null;
          var cur = self.get();
          if (cur && !cur.via) return now;            /* a real school sign-in wins */
          var newKey = (had && had.school_id) !== (now && now.school_id);
          try {
            if (now) localStorage.setItem(ACCOUNT_KEY, JSON.stringify(now)); else localStorage.removeItem(ACCOUNT_KEY);
          } catch (e) {}
          /* a class on a free-tier subject is authoritative for its board: "Maths (Edexcel)"
             means the student sits Edexcel Maths whatever they picked in the wizard. The
             dashboard applies it (it owns the family map); a changed list means a rebuild. */
          var classSubs = []; var seen = {};
          (d.classes || []).forEach(function (c) {
            if (!c.subject_slug) return; var id = (c.subject_school_id || '') + ':' + c.subject_slug; if (seen[id]) return; seen[id] = true;
            classSubs.push(c.subject_school_id ? { slug: c.subject_slug, school: c.subject_school_id } : { slug: c.subject_slug });
          });
          classSubs.sort(function (a, b) { return (a.school || '') + a.slug < (b.school || '') + b.slug ? -1 : 1; });
          var hadSubs = null; try { hadSubs = localStorage.getItem(CLASS_SUBJECTS_KEY); } catch (e) {}
          var subsChanged = JSON.stringify(classSubs) !== (hadSubs || '[]');
          try { if (classSubs.length) localStorage.setItem(CLASS_SUBJECTS_KEY, JSON.stringify(classSubs)); else localStorage.removeItem(CLASS_SUBJECTS_KEY); } catch (e) {}
          if (subsChanged && window.svApplyClassSubjects) { try { window.svApplyClassSubjects(classSubs); } catch (e) {} }
          if (now) { self.set(now); if (window.svCarrySchoolProgress) { try { window.svCarrySchoolProgress(now); } catch (e) {} } }
          else if (cur && cur.via === 'class') self.clear();
          if ((newKey || subsChanged) && window.svProgressPushSoon) { try { svProgressPushSoon(); } catch (e) {} }
          /* reload when the page was built against a different answer than the one we now hold */
          if (opts.reload !== false && (subsChanged || ((now && now.school_id) || null) !== (self._booted || null))) location.reload();
          return now;
        })
        .catch(function () { return null; });
    },

    /** Check if the school has bespoke content for a subject slug. */
    hasBespoke: function (subjectSlug) {
      var s = this.get();
      if (!s || !s.bespoke_subjects) return false;
      return s.bespoke_subjects.indexOf(subjectSlug) !== -1;
    },

    /** Check if the school subscribes to a subject (ad-free generic). */
    isSubscribed: function (subjectSlug) {
      var s = this.get();
      if (!s) return false;
      // Bespoke subjects are implicitly subscribed
      if (s.bespoke_subjects && s.bespoke_subjects.indexOf(subjectSlug) !== -1) return true;
      if (s.subscribed_subjects && s.subscribed_subjects.indexOf(subjectSlug) !== -1) return true;
      return false;
    },

    /** Check if ads should show for a given subject. */
    showAds: function (subjectSlug) {
      if (!this.isActive()) return true;  // Free user — show ads
      if (this.isSubscribed(subjectSlug)) return false;  // Subscribed — no ads
      return true;  // School student but subject not subscribed — show ads
    },

    /** Redirect to homepage if no school session. Returns true if redirected. */
    requireOrRedirect: function () {
      if (!this.isActive()) {
        window.location.href = '/';
        return true;
      }
      return false;
    },

    /** Inject the school logo into the header, centred in the middle gap
        (between the unit pill on the left and the nav/tour button on the
        right). Kept separate from the StudyVault wordmark, which stays put. */
    injectLogo: function () {
      if (!this.isActive()) return;
      var session = this.get();
      var headerInner = document.querySelector('.page-header-inner');
      if (!headerInner || headerInner.querySelector('.header-school-logo')) return;

      // School logo URLs keyed by slug (local images)
      var logos = {
        'unity-college': '/images/unity-college-logo.png',
        'severn-vale': '/images/severn-vale-logo.png'
      };
      var logoUrl = logos[session.school_slug];
      if (!logoUrl) return;

      var img = document.createElement('img');
      img.className = 'header-school-logo';
      img.src = logoUrl;
      img.alt = session.school_name;

      // Sit between the unit pill and the nav. At >=1400px the StudyVault
      // wordmark is pulled into the gutter, leaving [pills | logo | nav] so
      // space-between centres the logo in the gap.
      var nav = document.getElementById('header-nav');
      if (nav) {
        headerInner.insertBefore(img, nav);
        // Also place a copy at the top of the slide-in burger menu, so the
        // school logo is present on mobile / tablet (<=960px) where the header
        // logo is hidden.
        if (!nav.querySelector('.drawer-school-logo')) {
          var drawerImg = document.createElement('img');
          drawerImg.className = 'drawer-school-logo';
          drawerImg.src = logoUrl;
          drawerImg.alt = session.school_name;
          nav.insertBefore(drawerImg, nav.firstChild);
        }
      } else {
        headerInner.appendChild(img);
      }
    }
  };

  /* A student who revised on the free tier and then joined a class keeps what they did:
     data/school-lesson-map.json pairs each free-tier lesson with the school lesson on the
     same topic. Visited flags, completion dates and topic ratings carry across to the twin
     (never overwriting school-side work); knowledge-check scores do not, because the
     questions differ. Free-tier progress is left in place. */
  window.svCarrySchoolProgress = function (school) {
    if (!school || !school.school_slug) return;
    var flagKey = 'sv-school-carried';
    try { var f = JSON.parse(localStorage.getItem(flagKey) || 'null'); if (f && f.school === school.school_slug) return; } catch (e) {}
    fetch('/data/school-lesson-map.json').then(function (r) { return r.ok ? r.json() : null; }).then(function (all) {
      var map = all && all[school.school_slug]; if (!map) return;
      var g = function (k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } };
      var put = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
      var done = g('sv-lessons-done', {}), when = g('sv-lessons-when', {}), visited = g('studyvault-visited', {}), w = g('sv-welcome', {});
      var rag = (w && w.rag) || {}; var moved = 0;
      Object.keys(map).forEach(function (freeSub) {
        var m = map[freeSub]; var to = m.to; if (!to || !school.bespoke_subjects || school.bespoke_subjects.indexOf(to) < 0) return;
        Object.keys(done).forEach(function (key) {
          if (key.indexOf(freeSub + '/') !== 0) return;
          var unit = key.slice(freeSub.length + 1);
          (done[key] || []).forEach(function (n) {
            var tgt = m.lessons[unit + '/' + n]; if (!tgt) return;
            var tu = tgt.split('/')[0], tn = parseInt(tgt.split('/')[1], 10);
            var tk = to + '/' + tu; done[tk] = done[tk] || [];
            if (done[tk].indexOf(tn) < 0) { done[tk].push(tn); moved++; }
            var wk = tk + '/' + tn; if (!when[wk] && when[key + '/' + n]) when[wk] = when[key + '/' + n];
            var slug = 'lesson-' + (tn < 10 ? '0' + tn : tn);
            visited[tu] = visited[tu] || []; if (visited[tu].indexOf(slug) < 0) visited[tu].push(slug);
          });
        });
        if (rag[freeSub] && !rag[to]) rag[to] = rag[freeSub];
        Object.keys(rag).forEach(function (k) {
          if (k.indexOf(freeSub + '/') !== 0) return;
          var tu = (m.units || {})[k.slice(freeSub.length + 1)]; if (tu && !rag[to + '/' + tu]) rag[to + '/' + tu] = rag[k];
        });
      });
      put('sv-lessons-done', done); put('sv-lessons-when', when); put('studyvault-visited', visited);
      w.rag = rag; put('sv-welcome', w);
      put(flagKey, { school: school.school_slug, at: new Date().toISOString(), moved: moved });
      if (window.svProgressPushSoon) { try { svProgressPushSoon(); } catch (e) {} }
    }).catch(function () {});
  };

  /* seed from the account copy before any loader runs; refresh from the server after load;
     and when account sync lands the key after the page has built, rebuild once */
  SchoolSession.fromAccount();
  document.addEventListener('sv-account-synced', function () { SchoolSession.rebootIfChanged(); });
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(function () { SchoolSession.refreshFromClasses(); }, 800); });
  } else {
    setTimeout(function () { SchoolSession.refreshFromClasses(); }, 800);
  }

  // Auto-inject logo on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      SchoolSession.injectLogo();
    });
  } else {
    SchoolSession.injectLogo();
  }
})();
