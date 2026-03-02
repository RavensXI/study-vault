const { supabase } = require('./supabase');

/**
 * Verify the request has a valid Supabase JWT from a teacher/admin.
 * Returns { user, profile } on success, or sends an error response.
 */
async function requireTeacher(req, res) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ error: 'Missing auth token' });
    return null;
  }

  const token = authHeader.replace('Bearer ', '');
  const { data: { user }, error: authError } = await supabase.auth.getUser(token);
  if (authError || !user) {
    res.status(401).json({ error: 'Invalid token' });
    return null;
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('id, role, school_id, full_name')
    .eq('id', user.id)
    .single();

  if (profileError || !profile) {
    res.status(403).json({ error: 'Profile not found' });
    return null;
  }

  const allowed = ['teacher', 'school_admin', 'platform_admin'];
  if (!allowed.includes(profile.role)) {
    res.status(403).json({ error: 'Insufficient permissions' });
    return null;
  }

  return { user, profile };
}

module.exports = { requireTeacher };
