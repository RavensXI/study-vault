/* Disclaimers popup — one "Disclaimers" link in the footer opens a single card
 * holding every required notice. Keeps the footer clean (just links) while giving
 * one place to point at. The Azure-TTS "near the player" narration note and the
 * on-map OS attribution still live in context; this popup is the consolidated home
 * and also carries the AI-video disclosure. Self-contained; loaded on every page. */
(function () {
  'use strict';

  var DISCLOSURES = [
    {
      h: 'Exam boards',
      t: 'StudyVault is an independent revision resource and is not affiliated with, endorsed by, or ' +
         'approved by AQA, Pearson Edexcel, OCR, WJEC or Eduqas. Exam board names and specification codes ' +
         'are used solely to identify the relevant courses. All lesson content is original to StudyVault.'
    },
    {
      h: 'AI-generated audio & video',
      t: 'Lesson narration is generated using AI text-to-speech. Lesson podcasts and StudyVault’s own ' +
         'overview videos are AI-generated. The voices are synthetic.'
    },
    {
      h: 'Maps',
      t: 'Based upon Ordnance Survey material. Contains OS data © Crown copyright and database right 2026.'
    }
  ];

  var CSS =
    '.sv-disc-overlay{position:fixed;inset:0;background:rgba(20,18,16,.42);display:none;align-items:center;' +
    'justify-content:center;z-index:9000;padding:1.25rem;opacity:0;transition:opacity .16s ease}' +
    '.sv-disc-overlay.open{display:flex;opacity:1}' +
    '.sv-disc-card{background:#fff;color:#2d2a26;max-width:460px;width:100%;border-radius:16px;padding:1.4rem 1.5rem 1.6rem;' +
    'box-shadow:0 18px 50px rgba(0,0,0,.22);position:relative;max-height:82vh;overflow:auto;' +
    'font-family:Inter,system-ui,sans-serif;transform:translateY(6px);transition:transform .16s ease}' +
    '.sv-disc-overlay.open .sv-disc-card{transform:none}' +
    '.sv-disc-title{font-size:1.15rem;font-weight:700;margin:0 0 .25rem}' +
    '.sv-disc-card h3{font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;' +
    'color:#8a8580;margin:1rem 0 .3rem}' +
    '.sv-disc-card p{font-size:.82rem;line-height:1.5;margin:0;color:#4a463f}' +
    '.sv-disc-close{position:absolute;top:.7rem;right:.8rem;border:none;background:transparent;font-size:1.5rem;' +
    'line-height:1;color:#8a8580;cursor:pointer;padding:.1rem .3rem;border-radius:8px}' +
    '.sv-disc-close:hover{color:#2d2a26;background:#f0ece5}' +
    '@media(prefers-color-scheme:dark){.sv-disc-card{background:#242019;color:#e8e3dc}' +
    '.sv-disc-card p{color:#c9c3ba}.sv-disc-close:hover{background:#3a352d}}';

  var overlay = null;

  function build() {
    if (overlay) return;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    overlay = document.createElement('div');
    overlay.className = 'sv-disc-overlay';
    var html = '<div class="sv-disc-card" role="dialog" aria-modal="true" aria-label="Disclaimers">' +
               '<button class="sv-disc-close" aria-label="Close disclaimers">×</button>' +
               '<h2 class="sv-disc-title">Disclaimers</h2>';
    DISCLOSURES.forEach(function (d) { html += '<h3>' + d.h + '</h3><p>' + d.t + '</p>'; });
    html += '</div>';
    overlay.innerHTML = html;
    // Append to <html>, not <body>: the page-entrance animation leaves a transform
    // on <body>, which would make it the containing block for our position:fixed
    // overlay and centre the card in the (tall) document instead of the viewport.
    document.documentElement.appendChild(overlay);

    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    overlay.querySelector('.sv-disc-close').addEventListener('click', close);
  }

  function open() { build(); overlay.classList.add('open'); }
  function close() { if (overlay) overlay.classList.remove('open'); }

  document.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('.sv-disclaimers-link') : null;
    if (link) { e.preventDefault(); open(); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
})();
