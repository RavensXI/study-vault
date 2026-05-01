/**
 * Admin notification helper — emails studyvault.info@gmail.com when a bug
 * report or subject request lands.
 *
 * Uses Resend (https://resend.com) — free tier 100 emails/day, simple HTTP
 * API. Configure via Vercel env vars:
 *
 *   RESEND_API_KEY    — required; get from resend.com → API Keys
 *   NOTIFY_TO         — optional; defaults to studyvault.info@gmail.com
 *   NOTIFY_FROM       — optional; defaults to "StudyVault <onboarding@resend.dev>"
 *                       (Resend's default sandbox sender — no domain
 *                       verification needed). For a branded sender like
 *                       "alerts@studyvault.co.uk", verify the domain in
 *                       Resend first.
 *
 * If RESEND_API_KEY is missing the helper logs and returns silently — never
 * blocks the user-facing API response.
 */

async function notifyAdmin({ subject, html, text }) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.warn('[notify] RESEND_API_KEY not set; skipping admin notification');
    return { skipped: true };
  }

  const fromAddress = process.env.NOTIFY_FROM || 'StudyVault <onboarding@resend.dev>';
  const toAddress = process.env.NOTIFY_TO || 'studyvault.info@gmail.com';

  try {
    const resp = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: fromAddress,
        to: toAddress,
        subject,
        html: html || `<pre>${(text || '').replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]))}</pre>`,
        text: text || '',
      }),
    });
    if (!resp.ok) {
      const body = await resp.text();
      console.error('[notify] Resend send failed:', resp.status, body);
      return { ok: false, status: resp.status };
    }
    return { ok: true };
  } catch (e) {
    console.error('[notify] Resend request error:', e);
    return { ok: false, error: String(e) };
  }
}

function escHtml(s) {
  return String(s || '').replace(/[<>&"']/g, c => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

module.exports = { notifyAdmin, escHtml };
