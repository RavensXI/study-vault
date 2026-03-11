const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { guide_id, content_html, title } = req.body;

  if (!guide_id) {
    return res.status(400).json({ error: 'Missing guide_id' });
  }

  const updates = {};
  if (content_html !== undefined) updates.content_html = content_html;
  if (title !== undefined) updates.title = title;

  if (Object.keys(updates).length === 0) {
    return res.status(400).json({ error: 'No fields to update' });
  }

  const { error } = await supabase
    .from('guide_pages')
    .update(updates)
    .eq('id', guide_id);

  if (error) {
    return res.status(500).json({ error: 'Failed to update', detail: error.message });
  }

  return res.status(200).json({ status: 'ok', guide_id });
};
