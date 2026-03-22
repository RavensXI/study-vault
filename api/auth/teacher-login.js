const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL || 'https://baipckgywpnwapobwtsy.supabase.co',
  process.env.SUPABASE_SERVICE_KEY
);

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { email, password } = req.body || {};

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  // Sign in via Supabase Auth
  const { data: authData, error: authError } = await supabase.auth.signInWithPassword({
    email: email.trim().toLowerCase(),
    password,
  });

  if (authError || !authData.session) {
    return res.status(401).json({ error: authError?.message || 'Invalid email or password' });
  }

  const userId = authData.user.id;
  const session = {
    access_token: authData.session.access_token,
    refresh_token: authData.session.refresh_token,
    expires_at: authData.session.expires_at,
  };

  // Fetch teacher profile
  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('id, full_name, role, school_id')
    .eq('id', userId)
    .single();

  if (profileError || !profile) {
    return res.status(500).json({ error: 'Could not load profile' });
  }

  // Ensure the user has a teacher/admin role
  if (!['teacher', 'school_admin', 'platform_admin'].includes(profile.role)) {
    return res.status(403).json({ error: 'This login is for teachers only. Students should use the school code.' });
  }

  // Fetch teacher's assigned subjects
  const { data: teacherSubjects } = await supabase
    .from('teacher_subjects')
    .select('subject_id, subjects(id, name, slug)')
    .eq('teacher_id', userId);

  const subjects = (teacherSubjects || []).map(ts => ts.subjects).filter(Boolean);

  // Fetch school info if the teacher belongs to one
  let school = null;
  if (profile.school_id) {
    const { data: schoolData } = await supabase
      .from('schools')
      .select('id, name, slug')
      .eq('id', profile.school_id)
      .single();
    school = schoolData || null;
  }

  return res.json({
    session,
    profile: {
      id: profile.id,
      name: profile.full_name,
      role: profile.role,
      school_id: profile.school_id,
    },
    school,
    subjects,
  });
};
