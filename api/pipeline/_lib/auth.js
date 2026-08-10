const { supabase } = require('./supabase');

/**
 * Verify the request has a valid Supabase JWT or the admin/teacher password.
 * Returns { user, profile } on success, or sends an error response.
 */
async function requireTeacher(req, res) {
  // 1. Try Supabase JWT (SSO users)
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
        return { user, profile };
      }
    }
  }

  // 2. Try admin/teacher password (header or body)
  const adminPw = req.headers['x-admin-password'] || (req.body && req.body._admin_password);
  if (adminPw) {
    let role = null;
    if (process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD) role = 'platform_admin';
    if (process.env.TEACHER_PASSWORD && adminPw === process.env.TEACHER_PASSWORD) role = 'teacher';

    if (role) {
      // Look up the school_id for Unity College (default school for admin/teacher)
      const { data: school } = await supabase
        .from('schools')
        .select('id')
        .eq('slug', 'unity-college')
        .single();
      return {
        user: { id: role },
        profile: { id: role, full_name: role === 'platform_admin' ? 'Admin' : 'Teacher', role, school_id: school?.id || null }
      };
    }
  }

  res.status(401).json({ error: 'Not authenticated. Log in first.' });
  return null;
}

module.exports = { requireTeacher };
