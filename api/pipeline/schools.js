const { supabase } = require('./_lib/supabase');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Admin-Password');
  if (req.method === 'OPTIONS') return res.status(200).end();

  // Only return schools that have bespoke subjects
  const { data: subjectSchools } = await supabase
    .from('subjects')
    .select('school_id')
    .not('school_id', 'is', null);

  const schoolIds = [...new Set((subjectSchools || []).map(s => s.school_id))];
  if (schoolIds.length === 0) return res.json({ schools: [] });

  const { data, error } = await supabase
    .from('schools')
    .select('id, name, slug')
    .in('id', schoolIds)
    .order('name');

  if (error) return res.status(500).json({ error: error.message });
  return res.json({ schools: data || [] });
};
