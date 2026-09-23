/* The pupil's side of the safeguarding route (23 Sep 2026; server side in
   api/_lib/safeguard.js).

   svAuthHeaders(headers)   adds the pupil's sign-in to a request, when there is
                            one, so the server can tell which school's
                            safeguarding lead should hear about a concern.
                            Nothing else is read from it.
   svShowSupport(anchor, d) when a reply carries d.support, shows the support
                            panel: after `anchor` if one is given, otherwise as
                            a panel at the foot of the screen. Shown once per
                            anchor; never promises the pupil confidentiality. */
(function () {
  'use strict';
  var TOKEN_KEY = 'sb-baipckgywpnwapobwtsy-auth-token';

  window.svAuthHeaders = function (headers) {
    headers = headers || {};
    try {
      var raw = localStorage.getItem(TOKEN_KEY);
      var tok = raw ? (JSON.parse(raw) || {}).access_token : null;
      if (tok) headers['Authorization'] = 'Bearer ' + tok;
    } catch (e) {}
    return headers;
  };

  var CSS = '' +
    '.sv-support{margin:14px 0 4px;padding:16px 18px;border:1px solid #d9cfbd;border-radius:12px;background:#fbf8f3;color:#26231e;' +
      'font:400 15px/1.55 "Source Serif 4",Georgia,serif;text-align:left}' +
    '.sv-support h4{margin:0 0 6px;font:700 15px/1.35 Inter,system-ui,sans-serif;color:#26231e}' +
    '.sv-support p{margin:0 0 8px}' +
    '.sv-support ul{margin:0 0 8px;padding-left:18px}' +
    '.sv-support li{margin:0 0 4px}' +
    '.sv-support a{color:#b0561c;font-weight:600}' +
    '.sv-support .sv-support-school{margin:8px 0 0;color:#4d493f;font-size:14px}' +
    '.sv-support-float{position:fixed;left:16px;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:10050;max-width:520px;margin:0 auto;' +
      'box-shadow:0 10px 30px rgba(40,30,20,.18)}' +
    '.sv-support-close{float:right;margin:-4px -6px 0 8px;border:0;background:transparent;font:600 20px/1 Inter,system-ui,sans-serif;color:#7d7868;cursor:pointer;padding:4px 8px}' +
    '.sv-support-close:focus-visible{outline:2px solid #b0561c;border-radius:6px}' +
    'body.dark-mode .sv-support{background:#2a2622;border-color:#4a4238;color:#ece6dc}' +
    'body.dark-mode .sv-support h4{color:#ece6dc}' +
    'body.dark-mode .sv-support .sv-support-school{color:#c9c0b2}' +
    'body.dark-mode .sv-support a{color:#e39a63}';

  function style() {
    if (document.getElementById('sv-support-css')) return;
    var s = document.createElement('style'); s.id = 'sv-support-css'; s.textContent = CSS;
    document.head.appendChild(s);
  }
  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function panelHtml(d, floating) {
    return (floating ? '<button type="button" class="sv-support-close" aria-label="Close">&times;</button>' : '') +
      '<h4>If something is worrying you, you do not have to deal with it alone.</h4>' +
      '<p>You can talk to someone now, for free:</p>' +
      '<ul>' +
        '<li><b>Childline</b>: call 0800 1111, or chat at <a href="https://www.childline.org.uk" target="_blank" rel="noopener">childline.org.uk</a></li>' +
        '<li><b>Shout</b>: text SHOUT to 85258</li>' +
        '<li>If you are in danger now, call <b>999</b>.</li>' +
      '</ul>' +
      '<p>A teacher or another adult you trust can help too.</p>' +
      (d && d.school_name ? '<p class="sv-support-school">Because you are at ' + esc(d.school_name) + ', your school’s safeguarding lead may be told, so that someone can help.</p>' : '');
  }

  window.svShowSupport = function (anchor, d) {
    if (!d || !d.support) return;
    style();
    if (anchor && anchor.parentNode) {
      if (anchor.nextElementSibling && anchor.nextElementSibling.classList.contains('sv-support')) return;
      var box = document.createElement('div');
      box.className = 'sv-support'; box.setAttribute('role', 'note');
      box.innerHTML = panelHtml(d, false);
      anchor.parentNode.insertBefore(box, anchor.nextSibling);
      return;
    }
    if (document.querySelector('.sv-support-float')) return;
    var fl = document.createElement('div');
    fl.className = 'sv-support sv-support-float'; fl.setAttribute('role', 'dialog'); fl.setAttribute('aria-label', 'Support');
    fl.innerHTML = panelHtml(d, true);
    fl.querySelector('.sv-support-close').addEventListener('click', function () { fl.remove(); });
    document.body.appendChild(fl);
  };
})();
