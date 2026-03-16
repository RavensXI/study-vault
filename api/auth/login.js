const { supabase } = require('../pipeline/_lib/supabase');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { password, code } = req.body || {};

  // --- Student school code login ---
  if (code) {
    const { data: schools } = await supabase
      .from('schools')
      .select('id, name, slug, settings');

    const match = (schools || []).find(s =>
      s.settings && s.settings.student_code === code.toLowerCase().trim()
    );

    if (match) {
      // Check if school has bespoke subjects (school_id set on subjects table)
      const { data: bespokeSubjects } = await supabase
        .from('subjects')
        .select('slug')
        .eq('school_id', match.id);

      return res.json({
        role: 'student',
        school_id: match.id,
        school_name: match.name,
        school_slug: match.slug,
        subscribed_subjects: (match.settings && match.settings.subscribed_subjects) || [],
        bespoke_subjects: (bespokeSubjects || []).map(s => s.slug),
      });
    }
    return res.status(401).json({ error: 'Invalid school code' });
  }

  // --- Admin / teacher password login ---
  if (!password) {
    return res.status(400).json({ error: 'Password or school code required' });
  }

  if (process.env.ADMIN_PASSWORD && password === process.env.ADMIN_PASSWORD) {
    return res.json({ role: 'admin' });
  }

  if (process.env.TEACHER_PASSWORD && password === process.env.TEACHER_PASSWORD) {
    return res.json({ role: 'teacher' });
  }

  return res.status(401).json({ error: 'Incorrect password' });
};
