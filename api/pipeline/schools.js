const { supabase } = require('./_lib/supabase');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Admin-Password');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { data, error } = await supabase
    .from('schools')
    .select('id, name, slug')
    .order('name');

  if (error) return res.status(500).json({ error: error.message });
  return res.json({ schools: data || [] });
};
