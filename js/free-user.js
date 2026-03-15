/**
 * Free user session utility — manages localStorage prefs for anonymous visitors.
 * Separate from SchoolSession (sessionStorage) which is for school students.
 */
(function () {
  var KEY = 'studyvault-free-prefs';

  window.FreeUser = {
    get: function () {
      try {
        var raw = localStorage.getItem(KEY);
        return raw ? JSON.parse(raw) : null;
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
      return prefs.subjects.find(function (s) { return s.slug === slug; }) || null;
    }
  };
})();
