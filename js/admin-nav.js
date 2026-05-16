/* admin-nav.js — dropdown behaviour for the admin navigation bar */
(function () {
  'use strict';

  var path = window.location.pathname;

  // Map each menu-item href to its group trigger label
  var GROUP_PATHS = {
    '/admin/pipeline':     'build',
    '/admin/editor':       'build',
    '/admin/editor-guide': 'build',
    '/admin/build-status': 'build',
    '/admin/review':       'qa',
    '/admin/practice-qa':  'qa',
    '/admin/images':       'qa',
    '/admin/requests':     'manage',
    '/admin/bugs':         'manage',
    '/admin/schools':      'manage'
  };

  function init() {
    var triggers = document.querySelectorAll('.admin-nav-trigger');
    var menus    = document.querySelectorAll('.admin-nav-menu');

    // --- Highlight current group trigger + item ---
    var currentGroup = GROUP_PATHS[path] || null;

    triggers.forEach(function (btn) {
      var group = btn.dataset.group;
      if (group && group === currentGroup) {
        btn.classList.add('is-current');
      }
    });

    menus.forEach(function (menu) {
      menu.querySelectorAll('a').forEach(function (link) {
        // Normalise: strip trailing slash for comparison
        var href = link.getAttribute('href').replace(/\/$/, '');
        var curr = path.replace(/\/$/, '');
        if (href === curr) {
          link.classList.add('is-current-item');
        }
      });
    });

    // --- Toggle helpers ---
    function closeAll() {
      triggers.forEach(function (btn) {
        btn.setAttribute('aria-expanded', 'false');
      });
      menus.forEach(function (menu) {
        menu.classList.remove('is-open');
      });
    }

    function openMenu(trigger, menu) {
      closeAll();
      trigger.setAttribute('aria-expanded', 'true');
      menu.classList.add('is-open');
    }

    // --- Wire triggers ---
    triggers.forEach(function (btn) {
      var menu = btn.nextElementSibling;
      if (!menu || !menu.classList.contains('admin-nav-menu')) return;

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var isOpen = menu.classList.contains('is-open');
        if (isOpen) {
          closeAll();
        } else {
          openMenu(btn, menu);
        }
      });
    });

    // --- Outside click ---
    document.addEventListener('click', function () {
      closeAll();
    });

    // --- Escape key ---
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeAll();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
