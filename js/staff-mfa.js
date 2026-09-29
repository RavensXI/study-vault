/* Two-factor sign-in for staff (Tom, 29 Sep 2026).

   Admin is Tom's own account plus a 6-digit code from Microsoft Authenticator (any TOTP app
   works). The secret goes only between Supabase and the phone: the page shows the QR code once,
   at enrolment, and never stores it. A session that passed the code step carries aal2, which
   the server (api/_lib/admin-auth.js) and the database rules require for admin powers.

   Used by /teacher/login (the one sign-in surface) and /admin/security.
     svMfa.status(sb)                      -> { factor, current, next }
     svMfa.challenge(sb, host, factor, ui) -> resolves when the code is accepted
     svMfa.enrol(sb, host, ui)             -> resolves when the first code is accepted
   `ui.heading(title, subtitle)` lets the page set its own heading. */
(function () {
  'use strict';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  async function status(sb) {
    var f = await sb.auth.mfa.listFactors();
    var verified = ((f.data && f.data.totp) || []).filter(function (x) { return x.status === 'verified'; });
    var a = await sb.auth.mfa.getAuthenticatorAssuranceLevel();
    var d = a.data || {};
    return { factor: verified[0] || null, current: d.currentLevel || 'aal1', next: d.nextLevel || 'aal1' };
  }

  // A 6-digit code form. onCode(code) resolves to an error message, or '' when accepted.
  function codeForm(host, label, button, onCode) {
    var wrap = document.createElement('form');
    wrap.className = 'sv-mfa-form';
    wrap.innerHTML =
      '<div class="form-group">' +
        '<label class="form-label" for="svMfaCode">' + esc(label) + '</label>' +
        '<input class="form-input sv-mfa-code" id="svMfaCode" type="text" inputmode="numeric" ' +
          'autocomplete="one-time-code" pattern="[0-9]{6}" maxlength="6" required>' +
      '</div>' +
      '<div class="form-error sv-mfa-error" role="alert"></div>' +
      '<button type="submit" class="form-btn">' + esc(button) + '</button>';
    host.appendChild(wrap);
    var input = wrap.querySelector('input'), err = wrap.querySelector('.sv-mfa-error'), btn = wrap.querySelector('button');
    input.focus();
    input.addEventListener('input', function () { input.value = input.value.replace(/\D/g, '').slice(0, 6); err.classList.remove('visible'); });
    wrap.addEventListener('submit', async function (e) {
      e.preventDefault();
      var code = input.value.trim();
      if (!/^\d{6}$/.test(code)) { err.textContent = 'Type the 6 digits from the app.'; err.classList.add('visible'); return; }
      btn.disabled = true; var was = btn.textContent; btn.textContent = 'Checking…';
      var msg = '';
      try { msg = await onCode(code); } catch (x) { msg = 'Could not check the code. Try again.'; }
      if (msg) { err.textContent = msg; err.classList.add('visible'); input.select(); btn.disabled = false; btn.textContent = was; }
    });
    return wrap;
  }

  /* The QR arrives as an SVG behind a "data:image/svg+xml;utf-8," prefix (supabase-js adds it),
     with the SVG unencoded. A '#' in it (a colour) ends a data address early and the image
     breaks, so take the SVG itself and encode it properly. */
  function qrSrc(q) {
    q = String(q || '');
    var i = q.search(/<(\?xml|svg)/);
    return i < 0 ? q : 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(q.slice(i));
  }

  function codeError(e) {
    var m = (e && e.message) || '';
    return /invalid|expired|code/i.test(m) ? 'That code did not work. Wait for the next code and try again.' : (m || 'That code did not work.');
  }

  function challenge(sb, host, factor, ui) {
    if (ui && ui.heading) ui.heading('Enter your code', 'Open Microsoft Authenticator and type the 6-digit code for StudyVault.');
    return new Promise(function (resolve) {
      codeForm(host, 'Code', 'Continue', async function (code) {
        var r = await sb.auth.mfa.challengeAndVerify({ factorId: factor.id, code: code });
        if (r.error) return codeError(r.error);
        resolve(true); return '';
      });
    });
  }

  async function enrol(sb, host, ui) {
    // Clear half-finished set-ups first: Supabase keeps an unverified factor until it is removed.
    var f = await sb.auth.mfa.listFactors();
    var stale = ((f.data && f.data.all) || []).filter(function (x) { return x.factor_type === 'totp' && x.status !== 'verified'; });
    for (var i = 0; i < stale.length; i++) { try { await sb.auth.mfa.unenroll({ factorId: stale[i].id }); } catch (e) {} }

    var r = await sb.auth.mfa.enroll({ factorType: 'totp', friendlyName: 'Microsoft Authenticator ' + new Date().toISOString().slice(0, 10) });
    if (r.error) throw r.error;
    var d = r.data;
    if (ui && ui.heading) ui.heading('Set up two-factor sign-in', 'Admin needs a code from your phone as well as your password.');
    var box = document.createElement('div');
    box.className = 'sv-mfa-enrol';
    box.innerHTML =
      '<ol class="sv-mfa-steps">' +
        '<li>Open Microsoft Authenticator and choose <strong>Add account</strong>, then <strong>Other account</strong>.</li>' +
        '<li>Scan this QR code.</li>' +
      '</ol>' +
      '<img class="sv-mfa-qr" alt="QR code for your authenticator app" src="' + esc(qrSrc(d.totp.qr_code)) + '">' +
      '<details class="sv-mfa-manual"><summary>Cannot scan it?</summary>' +
        '<p>In the app, choose <strong>Or enter code manually</strong> and type this key:</p>' +
        '<code class="sv-mfa-secret">' + esc(d.totp.secret.replace(/(.{4})/g, '$1 ').trim()) + '</code>' +
      '</details>' +
      '<ol class="sv-mfa-steps" start="3"><li>Type the 6-digit code the app shows.</li></ol>';
    host.appendChild(box);
    return new Promise(function (resolve) {
      codeForm(host, 'Code', 'Finish set-up', async function (code) {
        var v = await sb.auth.mfa.challengeAndVerify({ factorId: d.id, code: code });
        if (v.error) return codeError(v.error);
        resolve(true); return '';
      });
    });
  }

  // Minimal styles, on top of the page's own form classes (teacher.css).
  var css = document.createElement('style');
  css.textContent =
    '.sv-mfa-code{letter-spacing:.3em;font-size:1.25rem;text-align:center;font-variant-numeric:tabular-nums}' +
    '.sv-mfa-steps{margin:0 0 .9rem;padding-left:1.25rem;line-height:1.5}' +
    '.sv-mfa-steps li{margin:.25rem 0}' +
    '.sv-mfa-steps li::marker{font-family:inherit;font-weight:600}' +
    '.sv-mfa-enrol img.sv-mfa-qr{display:block;width:200px;height:200px;max-width:100%;margin:0 auto 1rem;padding:10px;background:#fff;border:1px solid #e4dfd2;border-radius:16px}' +
    '.sv-mfa-manual{margin:0 0 1rem}' +
    '.sv-mfa-manual summary{cursor:pointer;font-weight:600}' +
    '.sv-mfa-secret{display:block;margin-top:.5rem;padding:.6rem .8rem;background:#f4f1ea;border-radius:10px;font-size:.95rem;word-break:break-all;letter-spacing:.05em}';
  document.head.appendChild(css);

  window.svMfa = { status: status, challenge: challenge, enrol: enrol };
})();
