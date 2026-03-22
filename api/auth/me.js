const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL || 'https://baipckgywpnwapobwtsy.supabase.co',
  process.env.SUPABASE_SERVICE_KEY
);

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Extract Bearer token
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authorization header required (Bearer token)' });
  }

  const token = authHeader.replace('Bearer ', '');

  // Validate the JWT and get the user
  const { data: { user }, error: authError } = await supabase.auth.getUser(token);
  if (authError || !user) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  // Fetch the profile
  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('id, full_name, role, school_id, created_at')
    .eq('id', user.id)
    .single();

  if (profileError || !profile) {
    return res.status(404).json({ error: 'Profile not found' });
  }

  // Fetch school info if the user belongs to one
  let school = null;
  if (profile.school_id) {
    const { data: schoolData } = await supabase
      .from('schools')
      .select('id, name, slug, settings')
      .eq('id', profile.school_id)
      .single();

    if (schoolData) {
      school = {
        id: schoolData.id,
        name: schoolData.name,
        slug: schoolData.slug,
      };
    }
  }

  // Fetch teacher's assigned subjects (only for teacher/admin roles)
  let subjects = [];
  if (['teacher', 'school_admin', 'platform_admin'].includes(profile.role)) {
    const { data: teacherSubjects } = await supabase
      .from('teacher_subjects')
      .select('subject_id, subjects(id, name, slug, exam_board)')
      .eq('teacher_id', user.id);

    subjects = (teacherSubjects || []).map(ts => ts.subjects).filter(Boolean);
  }

  return res.json({
    profile: {
      id: profile.id,
      name: profile.full_name,
      role: profile.role,
      school_id: profile.school_id,
      email: user.email,
      created_at: profile.created_at,
    },
    school,
    subjects,
  });
};
