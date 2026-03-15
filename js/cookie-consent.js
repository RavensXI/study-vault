/**
 * Cookie consent banner — shown to free users only (school users don't see ads).
 * Stores consent choice in localStorage. No cookies set until user accepts.
 */
(function () {
  var KEY = 'studyvault-cookie-consent';

  // Don't show for school students (they don't see ads)
  if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive()) return;

  // Check if already responded
  var consent = localStorage.getItem(KEY);
  if (consent) return;

  // Build banner
  var banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.innerHTML =
    '<div class="cookie-banner-inner">' +
      '<p>We use cookies to show relevant ads that help keep StudyVault free. ' +
        '<a href="/privacy.html">Privacy Policy</a></p>' +
      '<div class="cookie-banner-actions">' +
        '<button class="cookie-btn cookie-btn--reject" id="cookie-reject">Reject</button>' +
        '<button class="cookie-btn cookie-btn--accept" id="cookie-accept">Accept</button>' +
      '</div>' +
    '</div>';

  document.body.appendChild(banner);

  // Animate in
  requestAnimationFrame(function () {
    requestAnimationFrame(function () {
      banner.classList.add('visible');
    });
  });

  document.getElementById('cookie-accept').addEventListener('click', function () {
    localStorage.setItem(KEY, 'accepted');
    banner.classList.remove('visible');
    setTimeout(function () { banner.remove(); }, 300);
  });

  document.getElementById('cookie-reject').addEventListener('click', function () {
    localStorage.setItem(KEY, 'rejected');
    banner.classList.remove('visible');
    setTimeout(function () { banner.remove(); }, 300);
  });

  // Expose for ad scripts to check
  window.CookieConsent = {
    accepted: function () {
      return localStorage.getItem(KEY) === 'accepted';
    },
    responded: function () {
      return localStorage.getItem(KEY) !== null;
    }
  };
})();
