const { supabase } = require('../pipeline/_lib/supabase');

function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

// Returns rows aggregated by lower-cased school name with submission
// count and first/last seen. The frontend can choose between the
// aggregated view and the raw row stream.
module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });

  if (req.method === 'GET') {
    const view = req.query.view || 'aggregated';

    if (view === 'raw') {
      const { data, error } = await supabase
        .from('picker_school_submissions')
        .select('id, school_name, is_directory_match, created_at')
        .order('created_at', { ascending: false })
        .limit(2000);
      if (error) return res.status(500).json({ error: error.message });
      return res.json({ submissions: data || [] });
    }

    // Aggregated by case-insensitive school name. Pull all rows and
    // bucket in memory — table is tiny (sales signal only) and this
    // avoids needing a Postgres view or RPC.
    const { data, error } = await supabase
      .from('picker_school_submissions')
      .select('school_name, is_directory_match, created_at')
      .order('created_at', { ascending: false })
      .limit(5000);
    if (error) return res.status(500).json({ error: error.message });

    const buckets = new Map();
    (data || []).forEach((r) => {
      const key = r.school_name.toLowerCase();
      let b = buckets.get(key);
      if (!b) {
        b = {
          school_name: r.school_name,
          submission_count: 0,
          first_seen: r.created_at,
          last_seen: r.created_at,
          any_directory_match: false,
        };
        buckets.set(key, b);
      }
      b.submission_count += 1;
      if (r.created_at < b.first_seen) b.first_seen = r.created_at;
      if (r.created_at > b.last_seen) b.last_seen = r.created_at;
      if (r.is_directory_match) b.any_directory_match = true;
    });

    const schools = Array.from(buckets.values()).sort((a, b) => {
      if (b.submission_count !== a.submission_count) {
        return b.submission_count - a.submission_count;
      }
      return b.last_seen.localeCompare(a.last_seen);
    });
    return res.json({ schools, total_submissions: data ? data.length : 0 });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
