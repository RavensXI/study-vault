const { supabase } = require('../pipeline/_lib/supabase');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { password, code } = req.body || {};

  // --- Student school codes: RETIRED (1 Sep 2026) ---
  // School sign-in is SSO (Microsoft / Google) with a school-email fallback.
  // The old landing page at /index.html still carried the code form, so a
  // student with last year's code could open a school session and reach
  // bespoke content outside the identity model. Refuse every code here so no
  // client, old or new, can mint a student session from a shared secret.
  if (code) {
    return res.status(410).json({
      error: 'School codes have been retired. Sign in with your school account instead.',
    });
  }

  // --- Admin / teacher password login ---
  if (!password) {
    return res.status(400).json({ error: 'Password or school code required' });
  }

  if (process.env.ADMIN_PASSWORD && password === process.env.ADMIN_PASSWORD) {
    return res.json({ role: 'admin' });
  }

  if (process.env.TEACHER_PASSWORD && password === process.env.TEACHER_PASSWORD) {
    // Look up default school for shared teacher password (Unity College)
    const { data: school } = await supabase
      .from('schools')
      .select('id')
      .eq('slug', 'unity-college')
      .single();
    return res.json({ role: 'teacher', school_id: school ? school.id : null });
  }

  return res.status(401).json({ error: 'Incorrect password' });
};
