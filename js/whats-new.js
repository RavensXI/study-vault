/**
 * What's New toast — small bottom-right card showing the most recent free-tier
 * subjects added to StudyVault.
 *
 * Triggers once per browser session (sessionStorage flag). Shows on any page
 * that loads this script. Slides in ~1.5s after load, auto-fades after ~12s,
 * dismissable with the close button.
 *
 * Live-queries Supabase for the 5 most recent `school_id IS NULL` subjects
 * with `status = 'live'`, sorted by created_at DESC.
 */
(function () {
  'use strict';

  var SESSION_KEY = 'sv-whats-new-shown';
  var SHOW_DELAY = 1500;
  var AUTO_HIDE = 12000;

  function lsGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  // Already shown this session — bail
  if (lsGet(SESSION_KEY) === '1') return;

  // Don't show on admin / teacher pages — these aren't student-facing
  if (window.location.pathname.indexOf('/admin/') === 0 ||
      window.location.pathname.indexOf('/teacher/') === 0) {
    return;
  }

  // Don't show on mobile-menu drawer / install-prompt territory — keep mobile clean
  // (We do show on mobile, just check the install prompt isn't already up)
  // No-op for now; install prompt has higher z-index so they could co-exist briefly.

  // Need supabase client — check if it's loaded
  function getSupabase() {
    if (typeof window.supabase !== 'undefined' && window.supabase.createClient) {
      return window.supabase.createClient(
        'https://baipckgywpnwapobwtsy.supabase.co',
        'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
      );
    }
    return null;
  }

  function relativeDate(iso) {
    if (!iso) return '';
    var then = new Date(iso).getTime();
    var now = Date.now();
    var diff = Math.max(0, now - then);
    var days = Math.floor(diff / (1000 * 60 * 60 * 24));
    if (days === 0) return 'today';
    if (days === 1) return 'yesterday';
    if (days < 7) return days + ' days ago';
    if (days < 14) return '1 week ago';
    if (days < 30) return Math.floor(days / 7) + ' weeks ago';
    if (days < 60) return '1 month ago';
    var months = Math.floor(days / 30);
    return months + ' months ago';
  }

  function buildToast(subjects) {
    var el = document.createElement('div');
    el.className = 'sv-whats-new';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', "What's new on StudyVault");

    var itemsHtml = subjects.map(function (s) {
      var when = relativeDate(s.created_at);
      var accent = s.color || '#7c3aed';
      var board = s.exam_board || '';
      return (
        '<a class="sv-whats-new-item" href="/browse/' + s.slug + '" style="--item-accent: ' + escapeHtml(accent) + '">' +
          '<span class="sv-whats-new-item-name">' + escapeHtml(s.name) + '</span>' +
          '<span class="sv-whats-new-item-meta">' +
            (board ? '<span class="sv-whats-new-item-board">' + escapeHtml(board) + '</span>' : '') +
            '<span class="sv-whats-new-item-when">' + when + '</span>' +
          '</span>' +
        '</a>'
      );
    }).join('');

    el.innerHTML =
      '<div class="sv-whats-new-head">' +
        '<div class="sv-whats-new-title-wrap">' +
          '<span class="sv-whats-new-eyebrow">New on StudyVault</span>' +
          '<span class="sv-whats-new-title">Recently added</span>' +
        '</div>' +
        '<button type="button" class="sv-whats-new-close" aria-label="Dismiss">×</button>' +
      '</div>' +
      '<div class="sv-whats-new-body">' + itemsHtml + '</div>';

    el.querySelector('.sv-whats-new-close').addEventListener('click', hide);

    document.body.appendChild(el);
    // Trigger reflow + animate in
    el.offsetHeight;
    requestAnimationFrame(function () { el.classList.add('active'); });

    // Auto-hide
    setTimeout(hide, AUTO_HIDE);

    function hide() {
      el.classList.remove('active');
      setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }, 400);
    }
  }

  function escapeHtml(s) {
    if (s == null) return '';
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  setTimeout(function () {
    var sb = getSupabase();
    if (!sb) return;
    sb.from('subjects')
      .select('name, slug, exam_board, color, created_at')
      .is('school_id', null)
      .eq('status', 'live')
      .order('created_at', { ascending: false })
      .limit(5)
      .then(function (res) {
        if (res.error || !res.data || res.data.length === 0) return;
        // Mark shown BEFORE we build the toast, so even if user navigates
        // away before it fully renders, we don't double-show on the next page.
        lsSet(SESSION_KEY, '1');
        buildToast(res.data);
      })
      .catch(function () { /* silently ignore */ });
  }, SHOW_DELAY);
})();
