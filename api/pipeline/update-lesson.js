const { requireTeacher } = require('./_lib/auth');
const { requireOwnership } = require('./_lib/scope');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { lesson_id, content_html, exam_tip_html, conclusion_html,
          practice_questions, knowledge_checks, flashcard_questions, glossary_terms } = req.body;

  if (!lesson_id) {
    return res.status(400).json({ error: 'Missing lesson_id' });
  }

  const updates = {};
  if (content_html !== undefined) updates.content_html = content_html;
  if (exam_tip_html !== undefined) updates.exam_tip_html = exam_tip_html;
  if (conclusion_html !== undefined) updates.conclusion_html = conclusion_html;
  if (practice_questions !== undefined) updates.practice_questions = practice_questions;
  if (knowledge_checks !== undefined) updates.knowledge_checks = knowledge_checks;
  if (flashcard_questions !== undefined) updates.flashcard_questions = flashcard_questions;
  if (glossary_terms !== undefined) updates.glossary_terms = glossary_terms;

  if (Object.keys(updates).length === 0) {
    return res.status(400).json({ error: 'No fields to update' });
  }

  // requireTeacher says who is calling; this says what they may touch.
  if (!(await requireOwnership(auth, res, 'lesson', lesson_id))) return;

  const { error } = await supabase
    .from('lessons')
    .update(updates)
    .eq('id', lesson_id);

  if (error) {
    return res.status(500).json({ error: 'Failed to update', detail: error.message });
  }

  return res.status(200).json({ status: 'ok', lesson_id });
};
