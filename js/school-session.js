/**
 * School session utility — shared across all page loaders.
 * Stores the student's school context in sessionStorage.
 */
(function () {
  var KEY = 'studyvault-school';

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

    /** Redirect to homepage if no school session. Returns true if redirected. */
    requireOrRedirect: function () {
      if (!this.isActive()) {
        window.location.href = '/';
        return true;
      }
      return false;
    }
  };
})();
