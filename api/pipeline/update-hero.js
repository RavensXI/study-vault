const { requireTeacher } = require('./_lib/auth');
const { resolveLessonWrite } = require('./_lib/scope');
const { writeOverride } = require('./_lib/overrides');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { lesson_id, hero_image_url, hero_image_alt, hero_image_caption, hero_image_position } = req.body;

  if (!lesson_id) {
    return res.status(400).json({ error: 'Missing lesson_id' });
  }

  const updates = {};
  if (hero_image_url !== undefined) updates.hero_image_url = hero_image_url;
  if (hero_image_alt !== undefined) updates.hero_image_alt = hero_image_alt;
  if (hero_image_caption !== undefined) updates.hero_image_caption = hero_image_caption;
  if (hero_image_position !== undefined) updates.hero_image_position = hero_image_position;

  if (Object.keys(updates).length === 0) {
    return res.status(400).json({ error: 'No fields to update' });
  }

  const write = await resolveLessonWrite(auth, res, lesson_id);
  if (!write) return;

  if (write.mode === 'override') {
    const r = await writeOverride(lesson_id, write.schoolId, updates, auth);
    if (!r.ok) return res.status(500).json({ error: 'Failed to save', detail: r.error });
    return res.status(200).json({
      status: 'ok', lesson_id, scope: 'school',
      school_id: write.schoolId, created: r.created
    });
  }

  const { error } = await supabase
    .from('lessons')
    .update(updates)
    .eq('id', lesson_id);

  if (error) {
    return res.status(500).json({ error: 'Failed to update', detail: error.message });
  }

  return res.status(200).json({ status: 'ok', lesson_id });
};
