const { supabase } = require('./pipeline/_lib/supabase');

// Public endpoint: record an optional school name from the free-tier
// wizard's final step. Tom uses this for school-level interest signal
// (sales targeting). Deliberately captures NO per-student PII — no
// IP, no user-agent, no name, no email — just the school string and
// a timestamp.
module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = req.body || {};
  const school_name = String(body.school_name || '').trim().slice(0, 200);
  const is_directory_match = body.is_directory_match === true;

  if (!school_name) {
    return res.status(400).json({ error: 'School name is required' });
  }
  // Cheap sanity check: must contain at least one letter, can't be all
  // punctuation/whitespace garbage. Most schools include "School",
  // "Academy", "College", "High", etc., but we don't enforce that.
  if (!/[A-Za-z]/.test(school_name)) {
    return res.status(400).json({ error: 'Invalid school name' });
  }

  const { error } = await supabase.from('picker_school_submissions').insert({
    school_name,
    is_directory_match,
  });

  if (error) {
    console.error('picker_school_submissions insert failed', error);
    return res.status(500).json({ error: 'Could not save submission' });
  }

  return res.json({ ok: true });
};
