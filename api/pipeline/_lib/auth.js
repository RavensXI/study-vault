const { supabase } = require('./supabase');
const { claims } = require('../../_lib/admin-auth');

/**
 * Verify the request has a valid Supabase JWT for a teacher, school admin or platform admin.
 * Returns { user, profile } on success, or sends a 401 and returns null.
 *
 * Two-factor rule (29 Sep 2026): a platform_admin whose session has NOT passed the two-factor
 * step (token `aal` is not 'aal2') is treated as a teacher here: their own classes and
 * subjects still work, but no admin power (every other school, the free tier, staff reads).
 * The shared ADMIN_PASSWORD is no longer accepted (api/_lib/admin-auth.js).
 */
async function requireTeacher(req, res) {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabase.auth.getUser(token);
    if (!authError && user) {
      const { data: profile } = await supabase
        .from('profiles')
        .select('id, role, school_id, full_name')
        .eq('id', user.id)
        .single();

      if (profile && ['teacher', 'school_admin', 'platform_admin'].includes(profile.role)) {
        if (profile.role === 'platform_admin' && claims(token).aal !== 'aal2') {
          return { user, profile: Object.assign({}, profile, { role: 'teacher' }), mfaPending: true };
        }
        return { user, profile };
      }
    }
  }

  res.status(401).json({ error: 'Not authenticated. Log in first.' });
  return null;
}

module.exports = { requireTeacher };
