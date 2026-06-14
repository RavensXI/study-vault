/* Design-lab homepage life — localhost only. Adds the interactive flourishes
   the redesigned home leans on: a rotating subject word in the hero headline,
   cursor-driven 3D tilt on the subject cards, and a hover "continue" arrow.
   Non-destructive (reads the existing grid); remove the <script> to drop it.
   Respects prefers-reduced-motion and only tilts on a fine pointer. */
(function () {
  'use strict';
  if (location.hostname !== '127.0.0.1' && location.hostname !== 'localhost') return;

  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  var TILT = 5; // max degrees

  function enhanceCards() {
    var cards = [].slice.call(document.querySelectorAll('#home-grid .home-card'));
    cards.forEach(function (card) {
      // hover "continue" arrow
      if (!card.querySelector('.home-card-go')) {
        var body = card.querySelector('.home-card-body') || card;
        var go = document.createElement('span');
        go.className = 'home-card-go';
        go.setAttribute('aria-hidden', 'true');
        go.innerHTML = ARROW;
        body.appendChild(go);
      }
      // cursor-driven tilt
      if (!reduced && finePointer && !card.dataset.tilt) {
        card.dataset.tilt = '1';
        card.addEventListener('mousemove', function (e) {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          card.style.setProperty('--ty', (px * TILT).toFixed(2) + 'deg');
          card.style.setProperty('--tx', (-py * TILT).toFixed(2) + 'deg');
        });
        card.addEventListener('mouseleave', function () {
          card.style.setProperty('--tx', '0deg');
          card.style.setProperty('--ty', '0deg');
        });
      }
    });
    return cards;
  }

  function startRotator(cards) {
    var rot = document.querySelector('.hero-rotator');
    if (!rot) return;
    var subs = cards.map(function (c) {
      var nameEl = c.querySelector('h3, .home-card-name');
      var accent = (c.style.getPropertyValue('--card-accent') || '').trim() || '#566a72';
      return { name: nameEl ? nameEl.textContent.trim() : '', accent: accent };
    }).filter(function (s) { return s.name; });
    if (!subs.length) return;

    function set(s) {
      rot.textContent = s.name;
      // muted to match the card board labels (color-mix toward warm grey)
      rot.style.setProperty('--rot-accent', 'color-mix(in srgb, ' + s.accent + ' 62%, #71695f)');
    }
    set(subs[0]);
    if (reduced || subs.length < 2) return;

    var i = 0;
    setInterval(function () {
      i = (i + 1) % subs.length;
      rot.classList.add('is-swapping');
      setTimeout(function () {
        set(subs[i]);
        rot.classList.remove('is-swapping');
      }, 300);
    }, 2800);
  }

  // the grid is pruned to the user's subjects on load — wait for it to settle
  function go(tries) {
    var cards = enhanceCards();
    if (!cards.length && tries < 12) { setTimeout(function () { go(tries + 1); }, 250); return; }
    startRotator(cards);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(function () { go(0); }, 700); });
  } else {
    setTimeout(function () { go(0); }, 700);
  }
})();
