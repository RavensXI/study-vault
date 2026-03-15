const { supabase } = require('../pipeline/_lib/supabase');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { code } = req.body || {};
  if (!code) {
    return res.status(400).json({ error: 'School code required' });
  }

  // Look up school by student_code in settings jsonb
  const { data: schools, error } = await supabase
    .from('schools')
    .select('id, name, slug, settings');

  const match = (schools || []).find(function(s) {
    return s.settings && s.settings.student_code === code.toLowerCase().trim();
  });

  const data = match || null;

  if (error || !data) {
    return res.status(401).json({ error: 'Invalid school code' });
  }

  return res.json({
    school_id: data.id,
    school_name: data.name,
    school_slug: data.slug,
  });
};
