-- Typed-recall flashcards (19 Sep 2026): cards generated from the lesson's own glossary and
-- sentences, judged by Jev when the student types an answer. Kept apart from the curated
-- flashcard_questions deck so nothing that reads that column changes.
-- Shape: [{ "kind": "term"|"definition"|"cloze"|"list", "front": str, "answer": str,
--           "items"?: [str], "src": "glossary"|"sentence" }]
alter table public.lessons add column if not exists recall_cards jsonb not null default '[]'::jsonb;
comment on column public.lessons.recall_cards is 'Generated typed-recall cards (term/definition/cloze/list); see scripts/flashcards/build_recall_cards.py';
