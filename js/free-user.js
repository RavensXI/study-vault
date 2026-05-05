/**
 * Free user session utility — manages localStorage prefs for anonymous visitors.
 * Separate from SchoolSession (sessionStorage) which is for school students.
 */
(function () {
  var KEY = 'studyvault-free-prefs';

  // One-time slug migrations applied on every read (idempotent — re-runs are
  // no-ops once a user has been migrated). Avoids needing a separate migration
  // script — users get rewritten silently on next page load.
  //
  // History split (Apr 2026): `history` → `history-edexcel` so the AQA build
  // could take `history-aqa`.
  //
  // Free-tier slug consistency refactor (May 2026): every free-tier subject
  // now ends with -{board}. Old bare-slug entries get rewritten:
  //   english-language    → english-language-aqa
  //   english-literature  → english-literature-aqa
  //   maths               → maths-edexcel
  //   science             → science-aqa
  //   religious-education → religious-studies-aqa  (also baseSlug rename)
  //   geography           → geography-aqa
  //   health-social-care  → health-social-care-edexcel
  var SLUG_MIGRATIONS = {
    'history':             { slug: 'history-edexcel',          examBoard: 'edexcel' },
    'english-language':    { slug: 'english-language-aqa',     examBoard: 'aqa' },
    'english-literature':  { slug: 'english-literature-aqa',   examBoard: 'aqa' },
    'maths':               { slug: 'maths-edexcel',            examBoard: 'edexcel' },
    'science':             { slug: 'science-aqa',              examBoard: 'aqa' },
    'religious-education': { slug: 'religious-studies-aqa',    examBoard: 'aqa', baseSlug: 'religious-studies' },
    'geography':           { slug: 'geography-aqa',            examBoard: 'aqa' },
    'health-social-care':  { slug: 'health-social-care-edexcel', examBoard: 'edexcel' }
  };

  function migrateSlugs(prefs) {
    if (!prefs || !prefs.subjects) return prefs;
    var changed = false;
    prefs.subjects.forEach(function (s) {
      var mig = SLUG_MIGRATIONS[s.slug];
      if (mig) {
        s.slug = mig.slug;
        if (!s.examBoard && mig.examBoard) s.examBoard = mig.examBoard;
        if (mig.baseSlug && s.baseSlug && SLUG_MIGRATIONS[s.baseSlug]) {
          // baseSlug also needs renaming (e.g. religious-education → religious-studies)
          s.baseSlug = mig.baseSlug;
        }
        changed = true;
      }
    });
    if (changed) {
      try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch (e) {}
    }
    return prefs;
  }

  window.FreeUser = {
    get: function () {
      try {
        var raw = localStorage.getItem(KEY);
        if (!raw) return null;
        return migrateSlugs(JSON.parse(raw));
      } catch (e) {
        return null;
      }
    },

    set: function (data) {
      data.createdAt = data.createdAt || new Date().toISOString();
      localStorage.setItem(KEY, JSON.stringify(data));
    },

    clear: function () {
      localStorage.removeItem(KEY);
    },

    isActive: function () {
      var prefs = this.get();
      return prefs !== null && prefs.subjects && prefs.subjects.length > 0;
    },

    getSubjectSlugs: function () {
      var prefs = this.get();
      if (!prefs || !prefs.subjects) return [];
      return prefs.subjects.map(function (s) { return s.slug; });
    },

    getSubject: function (slug) {
      var prefs = this.get();
      if (!prefs || !prefs.subjects) return null;
      // Match by exact slug or by baseSlug (for multi-board subjects)
      return prefs.subjects.find(function (s) { return s.slug === slug || s.baseSlug === slug; }) || null;
    }
  };
})();
