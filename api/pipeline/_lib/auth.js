const { supabase } = require('./supabase');

// Demo accounts allowed to use the pipeline (temporary — remove once SSO is active)
const DEMO_ADMINS = {
  emma: { id: 'emma', full_name: 'Emma Wilson', role: 'platform_admin', school_id: null },
  jake: { id: 'jake', full_name: 'Jake Thompson', role: 'platform_admin', school_id: null },
};

/**
 * Verify the request has a valid Supabase JWT or demo token.
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

  // 3. Legacy demo auth (X-Demo-User header — kept for backwards compat)
  const demoUser = req.headers['x-demo-user'];
  if (demoUser && DEMO_ADMINS[demoUser]) {
    const profile = DEMO_ADMINS[demoUser];
    const { data: school } = await supabase
      .from('schools')
      .select('id')
      .eq('slug', 'unity-college')
      .single();
    profile.school_id = school?.id || null;
    return { user: { id: profile.id }, profile };
  }

  res.status(401).json({ error: 'Not authenticated. Log in first.' });
  return null;
}

module.exports = { requireTeacher };
