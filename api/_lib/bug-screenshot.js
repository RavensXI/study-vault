/**
 * Bug-report screenshots (Tom, 29 Sep 2026): a screenshot can show a pupil's screen, so it is
 * deleted from R2 the moment its report is closed (fixed / wontfix), and the report itself 30
 * days later (delete_after; daily housekeeping in api/cron/weekly-digest.js). Open reports keep
 * theirs until closed. Screenshots live under bug-reports/ in the public images bucket.
 */
const R2_BUCKET = 'studyvault-images';
const RETAIN_DAYS = 30;

// The R2 key from the stored URL (the custom domain or an old r2.dev address).
function keyOf(url) {
  const u = String(url || ''), i = u.indexOf('/bug-reports/');
  return i < 0 ? null : u.slice(i + 1);
}

// Deletes one screenshot; true when it is gone (or there was none to delete).
async function deleteScreenshot(url) {
  const key = keyOf(url);
  if (!key) return !url;
  if (!key.startsWith('bug-reports/')) return false;          // never touch anything else in the bucket
  const { R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY } = process.env;
  if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY) return false;
  const { S3Client, DeleteObjectCommand } = require('@aws-sdk/client-s3');
  const s3 = new S3Client({ region: 'auto', endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
    credentials: { accessKeyId: R2_ACCESS_KEY_ID, secretAccessKey: R2_SECRET_ACCESS_KEY } });
  try { await s3.send(new DeleteObjectCommand({ Bucket: R2_BUCKET, Key: key })); return true; }
  catch (e) { console.error('[bug-screenshot] delete failed', key, e.message); return false; }
}

function deleteAfter() { return new Date(Date.now() + RETAIN_DAYS * 864e5).toISOString(); }

module.exports = { deleteScreenshot, deleteAfter, RETAIN_DAYS };
