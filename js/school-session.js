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
    },

    /** Inject school logo into the page header brand area. */
    injectLogo: function () {
      if (!this.isActive()) return;
      var session = this.get();
      var brand = document.querySelector('.header-brand');
      if (!brand || brand.querySelector('.school-logo')) return;

      // School logo URLs keyed by slug (local images)
      var logos = {
        'unity-college': '/images/unity-college-logo.png'
      };
      var logoUrl = logos[session.school_slug];
      if (!logoUrl) return;

      var img = document.createElement('img');
      img.className = 'school-logo';
      img.src = logoUrl;
      img.alt = session.school_name;

      // Insert left of the StudyVault logo
      brand.insertBefore(img, brand.firstChild);
    }
  };

  // Auto-inject logo on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      SchoolSession.injectLogo();
    });
  } else {
    SchoolSession.injectLogo();
  }
})();
