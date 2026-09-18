const { supabase } = require('../pipeline/_lib/supabase');

/**
 * A student gives their name. The first name is optional at sign-up; the join
 * page asks for it when the profile has none, because a class screen that says
 * "Student" is no use to a teacher. Writes the profile row and the auth
 * metadata, so every reader of either sees the same name.
 *
 * POST { name }   Authorization: Bearer <student token>
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const authHeader = req.headers.authorization || '';
  if (!authHeader.startsWith('Bearer ')) return res.status(401).json({ error: 'Sign in first.' });
  const { data: userData, error: authError } = await supabase.auth.getUser(authHeader.slice(7));
  if (authError || !userData || !userData.user) return res.status(401).json({ error: 'Your sign-in has expired. Sign in again.' });
  const id = userData.user.id;

  const name = String((req.body || {}).name || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  if (name.length < 2) return res.status(400).json({ error: 'Type your name so your teacher knows who you are.' });

  const { error } = await supabase.from('profiles').update({ full_name: name }).eq('id', id);
  if (error) return res.status(500).json({ error: 'Could not save that.', detail: error.message });
  try { await supabase.auth.admin.updateUserById(id, { user_metadata: { full_name: name, sv_name: name } }); } catch (e) { /* the profile row is what the class screen reads */ }
  return res.status(200).json({ ok: true, name: name });
};
