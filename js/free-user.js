/**
 * Free user session utility — manages localStorage prefs for anonymous visitors.
 * Separate from SchoolSession (sessionStorage) which is for school students.
 */
(function () {
  var KEY = 'studyvault-free-prefs';

  // One-time slug migration applied on every read so it's idempotent and we
  // don't have to ship a separate migration script. Free-tier History was
  // renamed `history` → `history-edexcel` so the AQA build can take `history-aqa`.
  // Existing free-tier users with `slug: 'history'` get rewritten + saved back.
  function migrateHistorySlug(prefs) {
    if (!prefs || !prefs.subjects) return prefs;
    var changed = false;
    prefs.subjects.forEach(function (s) {
      if (s.slug === 'history') {
        s.slug = 'history-edexcel';
        if (!s.examBoard) s.examBoard = 'edexcel';
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
        return migrateHistorySlug(JSON.parse(raw));
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
