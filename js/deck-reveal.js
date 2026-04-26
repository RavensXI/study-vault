/* StudyVault — Deck Reveal Animation
   Replaces every direct child of `container` with a shimmer placeholder,
   then stagger-flips the real cards back in. Used for personalisation
   moments: Unity tier picker close, free-tier wizard completion, and
   first-visit-per-subject browse landing.

   Options:
     shimmerClass: 'home-card-shimmer' (default) or 'unit-card-shimmer'
     stagger:      ms between consecutive card reveals (default 110)
     initialPause: ms shimmer-only before first card (default 280)
     animLength:   ms the flip animation runs (default 700)
*/
(function () {
  'use strict';

  function runDeckReveal(container, options) {
    if (!container) return;
    options = options || {};
    var shimmerClass = options.shimmerClass || 'home-card-shimmer';
    var stagger = options.stagger != null ? options.stagger : 110;
    var initialPause = options.initialPause != null ? options.initialPause : 280;
    var animLength = options.animLength != null ? options.animLength : 700;

    var cards = Array.prototype.slice.call(container.children);
    if (cards.length === 0) return;

    // Detach the real cards and replace with shimmers
    container.innerHTML = '';
    cards.forEach(function (card, i) {
      // Strip prior reveal state so the animation always fires fresh
      if (card.classList) {
        card.classList.remove('sv-visible', 'deck-reveal');
      }
      var shim = document.createElement('div');
      shim.className = shimmerClass;
      shim.dataset.deckIdx = String(i);
      container.appendChild(shim);
    });

    // Stagger-replace each shimmer with its real card
    cards.forEach(function (card, i) {
      setTimeout(function () {
        var shim = container.querySelector('[data-deck-idx="' + i + '"]');
        if (!shim) return;
        card.classList.add('deck-reveal');
        shim.replaceWith(card);
        setTimeout(function () {
          // sv-visible counters the underlying .sv-reveal opacity:0 rule on
          // home-cards, keeping the card visible after deck-reveal is removed
          card.classList.add('sv-visible');
          card.classList.remove('deck-reveal');
        }, animLength);
      }, initialPause + i * stagger);
    });
  }

  window._svDeckReveal = runDeckReveal;
})();
