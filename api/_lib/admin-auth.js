/**
 * Admin access (Tom, 29 Sep 2026): the shared ADMIN_PASSWORD is retired. An admin is a signed-in
 * Supabase account whose profile role is platform_admin AND whose session passed the two-factor
 * step (the token's `aal` claim is 'aal2' — a code from Microsoft Authenticator). A platform_admin
 * signed in with a password alone is treated as a teacher everywhere (api/pipeline/_lib/auth.js),
 * and the database rules ask for aal2 too (supabase/migrations/20260929200000_admin_mfa.sql).
 *
 * Scheduled jobs keep their own CRON_SECRET; nothing here touches that.
 */
const { supabase } = require('../pipeline/_lib/supabase');

// The token's claims. getUser() has already checked the signature by the time this is read.
function claims(token) {
  try {
    const part = String(token).split('.')[1] || '';
    return JSON.parse(Buffer.from(part.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8'));
  } catch (e) { return {}; }
}

function bearer(req) {
  const h = req.headers.authorization || req.headers.Authorization || '';
  return h.startsWith('Bearer ') ? h.slice(7) : null;
}

// { user, profile, aal } for any valid token, or null.
async function staffFromRequest(req) {
  const token = bearer(req);
  if (!token) return null;
  const { data, error } = await supabase.auth.getUser(token);
  if (error || !data || !data.user) return null;
  const { data: profile } = await supabase.from('profiles')
    .select('id, role, school_id, full_name').eq('id', data.user.id).maybeSingle();
  if (!profile) return null;
  return { user: data.user, profile, aal: claims(token).aal || 'aal1' };
}

// { user, profile } when the request comes from an admin who passed the two-factor step; else null.
async function adminFromRequest(req) {
  const s = await staffFromRequest(req);
  return (s && s.profile.role === 'platform_admin' && s.aal === 'aal2') ? { user: s.user, profile: s.profile } : null;
}

// As above, but answers 401 itself. Use: const admin = await requireAdmin(req, res); if (!admin) return;
async function requireAdmin(req, res) {
  const admin = await adminFromRequest(req);
  if (!admin) res.status(401).json({ error: 'Admin sign-in with a two-factor code is required.', mfa: true });
  return admin;
}

module.exports = { claims, staffFromRequest, adminFromRequest, requireAdmin };
