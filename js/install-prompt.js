/**
 * PWA install prompt — gentle nudge to add StudyVault to the home screen.
 *
 * Trigger windows (whichever fires first):
 *   1. Knowledge-check completion (positive engagement moment)
 *   2. Second visit, ≥1 day after first visit (return = intent signal)
 *
 * Platform handling:
 *   • Android (or any browser firing beforeinstallprompt) — capture the
 *     event, defer it, fire prompt() when the user taps Install.
 *   • iOS Safari — show instructions referencing the Share button.
 *     Programmatic install isn't available; we can only guide.
 *   • iOS Chrome/Firefox, desktop, anything else without
 *     beforeinstallprompt and not iOS Safari — do nothing.
 *
 * Show conditions:
 *   • Mobile only (≤768px width OR coarse pointer)
 *   • Not running in standalone (already installed)
 *   • Not snoozed (snooze = dismiss → 14 days)
 *   • Not permanently suppressed (install completed once)
 *
 * State (localStorage):
 *   sv-pwa-first-visit  — ms timestamp, set on first ever load
 *   sv-pwa-snooze-until — ms timestamp; null/missing = not snoozed
 *   sv-pwa-installed    — '1' once the install completes; never show again
 */
(function () {
  'use strict';

  var KEY_FIRST = 'sv-pwa-first-visit';
  var KEY_SNOOZE = 'sv-pwa-snooze-until';
  var KEY_INSTALLED = 'sv-pwa-installed';
  var SNOOZE_MS = 14 * 24 * 60 * 60 * 1000; // 14 days
  var SECOND_VISIT_THRESHOLD_MS = 24 * 60 * 60 * 1000; // 1 day

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  // Mark first visit if missing
  if (!lsGet(KEY_FIRST)) {
    lsSet(KEY_FIRST, String(Date.now()));
  }

  function isStandalone() {
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) return true;
    // iOS Safari standalone
    if (window.navigator.standalone === true) return true;
    return false;
  }

  function isMobileLike() {
    if (window.innerWidth <= 768) return true;
    if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) return true;
    return false;
  }

  function isIOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  }

  function isIOSSafari() {
    if (!isIOS()) return false;
    // CriOS = Chrome iOS, FxiOS = Firefox iOS, EdgiOS = Edge iOS, OPiOS = Opera iOS
    var ua = navigator.userAgent;
    if (/CriOS|FxiOS|EdgiOS|OPiOS/.test(ua)) return false;
    return /Safari/.test(ua);
  }

  function isSnoozed() {
    var until = parseInt(lsGet(KEY_SNOOZE) || '0', 10);
    return until && Date.now() < until;
  }

  function isEligible() {
    if (isStandalone()) return false;
    if (lsGet(KEY_INSTALLED) === '1') return false;
    if (isSnoozed()) return false;
    if (!isMobileLike()) return false;
    return true;
  }

  function isSecondVisitWindow() {
    var first = parseInt(lsGet(KEY_FIRST) || '0', 10);
    if (!first) return false;
    return (Date.now() - first) >= SECOND_VISIT_THRESHOLD_MS;
  }

  // ---- Banner DOM ----
  var bannerEl = null;
  var deferredPrompt = null;

  function makeBanner(mode) {
    if (bannerEl) return bannerEl;
    var el = document.createElement('div');
    el.className = 'sv-install-banner';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', 'Install StudyVault');

    var iconHtml =
      '<div class="sv-install-banner-icon">' +
        '<img src="/images/icon-192.png" alt="" width="38" height="38">' +
      '</div>';

    var bodyHtml;
    if (mode === 'android') {
      bodyHtml =
        '<div class="sv-install-banner-body">' +
          '<p class="sv-install-banner-title">Add StudyVault to your home screen</p>' +
          '<p class="sv-install-banner-text">Quicker to open, fewer taps to get back to revising.</p>' +
          '<div class="sv-install-banner-actions">' +
            '<button type="button" class="sv-install-banner-btn" data-action="install">Install</button>' +
          '</div>' +
        '</div>';
    } else {
      // iOS Safari
      bodyHtml =
        '<div class="sv-install-banner-body">' +
          '<p class="sv-install-banner-title">Add StudyVault to your home screen</p>' +
          '<p class="sv-install-banner-text">Tap ' +
            '<svg class="ios-share" width="14" height="18" viewBox="0 0 14 18" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
              '<path d="M7 12V2M3 5l4-4 4 4" stroke="#7c3aed" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
              '<path d="M2 9v6a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9" stroke="#7c3aed" stroke-width="1.6" stroke-linecap="round"/>' +
            '</svg>' +
            ' (Share) at the bottom of Safari, then choose <strong>Add to Home Screen</strong>.' +
          '</p>' +
        '</div>';
    }

    el.innerHTML =
      iconHtml +
      bodyHtml +
      '<button type="button" class="sv-install-banner-dismiss" aria-label="Dismiss">×</button>';

    el.querySelector('.sv-install-banner-dismiss').addEventListener('click', function () {
      lsSet(KEY_SNOOZE, String(Date.now() + SNOOZE_MS));
      hide();
    });

    var installBtn = el.querySelector('[data-action="install"]');
    if (installBtn) {
      installBtn.addEventListener('click', function () {
        if (!deferredPrompt) { hide(); return; }
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (choice) {
          if (choice && choice.outcome === 'accepted') {
            lsSet(KEY_INSTALLED, '1');
          } else {
            // User dismissed the native prompt — snooze briefly
            lsSet(KEY_SNOOZE, String(Date.now() + SNOOZE_MS));
          }
          deferredPrompt = null;
          hide();
        });
      });
    }

    document.body.appendChild(el);
    bannerEl = el;
    return el;
  }

  function show(mode) {
    if (!isEligible()) return;
    if (mode === 'android' && !deferredPrompt) return;
    if (mode === 'ios' && !isIOSSafari()) return;
    var el = makeBanner(mode);
    // Force reflow so transition runs
    el.offsetHeight;
    requestAnimationFrame(function () { el.classList.add('active'); });
  }

  function hide() {
    if (!bannerEl) return;
    bannerEl.classList.remove('active');
    setTimeout(function () {
      if (bannerEl && bannerEl.parentNode) bannerEl.parentNode.removeChild(bannerEl);
      bannerEl = null;
    }, 400);
  }

  // ---- Capture beforeinstallprompt (Android, Chrome desktop, etc.) ----
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
  });

  // If install completes outside our flow (e.g. user clicked install via
  // browser menu), record it so we don't keep nagging.
  window.addEventListener('appinstalled', function () {
    lsSet(KEY_INSTALLED, '1');
    hide();
  });

  // ---- Trigger 1: knowledge-check completion ----
  document.addEventListener('kc-completed', function () {
    if (!isEligible()) return;
    if (deferredPrompt) {
      // Slight delay to let any post-KC UI settle
      setTimeout(function () { show('android'); }, 1200);
    } else if (isIOSSafari()) {
      setTimeout(function () { show('ios'); }, 1200);
    }
  });

  // ---- Trigger 2: second-visit dwell ----
  // Wait until the page has been visible for ~6s — only worth nudging
  // someone who's actually looking at the page on a return visit.
  if (isSecondVisitWindow()) {
    setTimeout(function () {
      if (!isEligible()) return;
      if (deferredPrompt) {
        show('android');
      } else if (isIOSSafari()) {
        show('ios');
      }
    }, 6000);
  }
})();
