const { supabase } = require('./pipeline/_lib/supabase');
const { notifyAdmin, escHtml } = require('./_lib/notify');
const crypto = require('crypto');

const R2_ACCOUNT_ID = process.env.R2_ACCOUNT_ID;
const R2_ACCESS_KEY_ID = process.env.R2_ACCESS_KEY_ID;
const R2_SECRET_ACCESS_KEY = process.env.R2_SECRET_ACCESS_KEY;
const R2_BUCKET = 'studyvault-images';
const R2_PUBLIC_URL = 'https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev';

// Allow up to ~3MB JSON bodies (Vercel default would be 1MB) — screenshots eat space
module.exports.config = {
  api: { bodyParser: { sizeLimit: '4mb' } },
};

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = req.body || {};
  const message = String(body.message || '').trim().slice(0, 2000);
  const email = String(body.email || '').trim().slice(0, 200);
  const page_url = String(body.page_url || '').trim().slice(0, 500);
  const viewport_size = String(body.viewport_size || '').trim().slice(0, 50);
  const screenshotData = body.screenshot; // data:image/jpeg;base64,...

  if (!message) return res.status(400).json({ error: 'Description is required' });
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const ipHeader = (req.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || req.socket?.remoteAddress
    || '';
  const userAgent = String(req.headers['user-agent'] || '').slice(0, 300);

  // Light per-IP rate limit: 10 reports/hour
  if (ipHeader) {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();
    const { count } = await supabase
      .from('bug_reports')
      .select('id', { count: 'exact', head: true })
      .gt('created_at', oneHourAgo)
      .ilike('user_agent', '%' + ipHeader + '%');
    if ((count || 0) >= 10) {
      return res.status(429).json({ error: 'Too many reports, try again later' });
    }
  }

  // Optional screenshot upload
  let screenshot_url = null;
  if (screenshotData && typeof screenshotData === 'string' && screenshotData.startsWith('data:image/')) {
    if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY) {
      console.warn('R2 not configured; bug report saved without screenshot');
    } else {
      try {
        const match = screenshotData.match(/^data:(image\/\w+);base64,(.+)$/);
        if (match) {
          const mime = match[1];
          const buf = Buffer.from(match[2], 'base64');
          // Cap size at ~3.5MB even after base64 decode — anything larger is suspicious
          if (buf.length > 3.5 * 1024 * 1024) {
            console.warn('Screenshot too large, skipping upload');
          } else {
            const ext = mime === 'image/png' ? 'png' : 'jpg';
            const hash = crypto.createHash('md5').update(buf).digest('hex').substring(0, 10);
            const ts = new Date().toISOString().slice(0, 10); // 2026-04-26
            const key = `bug-reports/${ts}/${hash}.${ext}`;
            const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
            const s3 = new S3Client({
              region: 'auto',
              endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
              credentials: {
                accessKeyId: R2_ACCESS_KEY_ID,
                secretAccessKey: R2_SECRET_ACCESS_KEY,
              },
            });
            await s3.send(new PutObjectCommand({
              Bucket: R2_BUCKET,
              Key: key,
              Body: buf,
              ContentType: mime,
            }));
            screenshot_url = `${R2_PUBLIC_URL}/${key}`;
          }
        }
      } catch (e) {
        console.error('screenshot upload failed', e);
        // Don't block the report — save without the screenshot
      }
    }
  }

  const { error } = await supabase.from('bug_reports').insert({
    message,
    email: email || null,
    page_url: page_url || null,
    screenshot_url,
    viewport_size: viewport_size || null,
    user_agent: ipHeader ? `${ipHeader} | ${userAgent}` : userAgent || null,
  });

  if (error) {
    console.error('bug_report insert failed', error);
    return res.status(500).json({ error: 'Could not save report' });
  }

  // Fire-and-forget admin email — don't block the response if the email
  // service is down or the API key is missing.
  notifyAdmin({
    subject: `[StudyVault Bug] ${message.slice(0, 60)}${message.length > 60 ? '...' : ''}`,
    text:
      `New bug report on StudyVault\n\n` +
      `Description:\n${message}\n\n` +
      `Reporter email: ${email || '(not provided)'}\n` +
      `Page: ${page_url || '(unknown)'}\n` +
      `Viewport: ${viewport_size || '(unknown)'}\n` +
      `Screenshot: ${screenshot_url || '(none)'}\n\n` +
      `Triage at: https://www.studyvault.co.uk/admin/bugs`,
    html:
      `<h2 style="font-family:sans-serif;margin:0 0 0.5em">New bug report</h2>` +
      `<p style="font-family:sans-serif;white-space:pre-wrap;background:#f6f6f6;padding:0.75em 1em;border-radius:6px;border-left:3px solid #f59e0b">${escHtml(message)}</p>` +
      `<table style="font-family:sans-serif;font-size:0.9em;border-collapse:collapse;margin-top:1em">` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Reporter</td><td>${escHtml(email || '(not provided)')}</td></tr>` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Page</td><td>${escHtml(page_url || '(unknown)')}</td></tr>` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Viewport</td><td>${escHtml(viewport_size || '(unknown)')}</td></tr>` +
      (screenshot_url ? `<tr><td style="padding:4px 12px 4px 0;color:#666">Screenshot</td><td><a href="${escHtml(screenshot_url)}">${escHtml(screenshot_url)}</a></td></tr>` : '') +
      `</table>` +
      (screenshot_url ? `<p style="margin-top:1em"><img src="${escHtml(screenshot_url)}" alt="Bug screenshot" style="max-width:100%;border:1px solid #ddd;border-radius:6px"></p>` : '') +
      `<p style="margin-top:1.5em;font-family:sans-serif"><a href="https://www.studyvault.co.uk/admin/bugs" style="background:#2d2a26;color:#fff;padding:0.6em 1.2em;text-decoration:none;border-radius:6px;font-weight:600">Open admin triage &rarr;</a></p>`,
  }).catch((e) => console.error('[bug-report] notify error:', e));

  return res.json({ ok: true });
};
