const { supabase } = require('./pipeline/_lib/supabase');
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

  return res.json({ ok: true });
};
