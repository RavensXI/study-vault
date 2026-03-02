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

  // 2. Try demo auth (X-Demo-User header — temporary for testing)
  const demoUser = req.headers['x-demo-user'];
  if (demoUser && DEMO_ADMINS[demoUser]) {
    const profile = DEMO_ADMINS[demoUser];
    // Look up the school_id for Unity College
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
