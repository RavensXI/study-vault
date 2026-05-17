# RS Edexcel Content Workspace — Prep Report

**Subject:** Religious Studies (Edexcel 1RA0)
**Workspace:** `scripts/_content_religious-studies-edexcel/`
**Plan source:** `scripts/_plan_religious-studies-edexcel.json` (1,569 lines)

---

## Batch summary

| Batch | Units | Lessons | Transfer-score distribution |
|-------|-------|---------|----------------------------|
| b01 | paper-1-catholic-christianity | 6 | high×5, fresh×1 |
| b02 | paper-1-christianity | 6 | high×5, fresh×1 |
| b03 | paper-1-islam | 6 | high×5, fresh×1 |
| b04 | paper-2-buddhism, paper-2-hinduism, paper-2-judaism, paper-2-sikhism | 16 | high×15, medium×1 |
| b05 | paper-2-catholic-christianity, paper-2-christianity, paper-2-islam | 12 | high×12 |
| b06 | paper-3-philosophy-ethics-catholic, paper-3-philosophy-ethics-christianity, paper-3-philosophy-ethics-islam | 15 | medium×14, fresh×1 |
| b07 | paper-4-marks-gospel, paper-4-quran | 10 | fresh×10 |
| **Total** | **15 units** | **71** | **high×54, medium×15, fresh×13** |

---

## Files in this workspace

| File | Purpose |
|------|---------|
| `_AGENT_PROMPT.md` | System prompt for content agents — read before generating any lesson |
| `_RELATED_MEDIA_PROMPT.md` | System prompt for Phase 4 related media curation agents |
| `_reference_lesson.json` | RE L01 "Worship & Prayer" (Supabase `21447890-d512-42c6-85f9-90b4133c06e3`) — structural template |
| `_aqa_source_lessons.json` | AQA RS source lessons (stub — populate by running `_fetch_aqa_sources.py` first) |
| `_fetch_aqa_sources.py` | Fetches AQA RS lessons from Supabase into `_aqa_source_lessons.json` |
| `_fetch_lesson_ids.py` | Patches `lesson_id: LOOKUP_BY_SLUG` placeholders in batch files with real Supabase UUIDs |
| `_gen_batches.py` | Regenerates all batch files from the plan (re-run if plan changes) |
| `_batch_b01.json` … `_batch_b07.json` | Batch input files — one per agent run |
| `lessons/` | Output directory — content agents write `{lesson_slug}.json` here |

---

## Before running content agents — setup checklist

1. **Populate AQA source lessons:**
   ```
   python scripts/_content_religious-studies-edexcel/_fetch_aqa_sources.py
   ```
   This fills `_aqa_source_lessons.json` with real lesson content from the `religious-studies-aqa` subject in Supabase. Batches b01–b05 all reference this file heavily (transfer_score = high).

2. **Patch lesson UUIDs into batch files:**
   ```
   python scripts/_content_religious-studies-edexcel/_fetch_lesson_ids.py
   ```
   Replaces `"lesson_id": "LOOKUP_BY_SLUG"` placeholders with real Supabase UUIDs. The insertion script uses these to find the right lesson row.

3. **Create output directory:**
   ```
   mkdir scripts/_content_religious-studies-edexcel/lessons
   ```

---

## Batch priorities and agent guidance

### High-priority / low-effort (run first)
- **b05** (12 lessons, all high-transfer, 3 Abrahamic Paper 2 units): highest reuse from AQA source. Fastest to generate once AQA source file is populated.
- **b01, b02, b03** (6 lessons each, 5 high / 1 fresh): Paper 1 units with strong AQA coverage. The single fresh lesson per unit (L06, Sources/Forms) is dense but has detailed section_markers.

### Medium-effort
- **b04** (16 lessons, 15 high + 1 medium): Four smaller Paper 2 religions. Hinduism L03 is the one medium-transfer lesson — Buddhist cosmology section needs extra care. Buddhism has Edexcel-specific Sutta anchors (Buddhavamsa, Milinda Panha, Kimsila, Vakkali, Mangala, Anapanasati) not in AQA.

### Highest-effort / fresh content
- **b06** (15 lessons, 14 medium + 1 fresh): Paper 3 Philosophy & Ethics is the fact-check minefield. Aquinas/kalam/theodicy attribution errors are documented misconceptions. Each religion route requires different doctrinal framing. The agent prompt has an explicit attribution table.
- **b07** (10 lessons, all fresh): Paper 4 Textual Studies — no AQA source at all. Mark's Gospel and Qur'an lessons must be built entirely from the section_markers and spec_references. All passage references in section_markers are spec-verified — preserve them exactly.

---

## Transfer-score distribution — full picture

- **54 × high** (76%): direct adaptation from AQA RS with Edexcel command-word swap
- **15 × medium** (21%): significant rework required (Paper 3 religion-specific framing, Hinduism cosmology, some Paper 2 lessons with more Edexcel-named content)
- **13 × fresh** (18%): zero AQA source — built from spec + section_markers only:
  - b01 L06: Sources/Forms in Catholic Christianity (Vatican II, magisterium, Catholic art)
  - b02 L06: Sources/Forms in Christianity (denominations, Filioque, CS Lewis, Christian art)
  - b03 L06: Sources/Authority in Islam (Sufi figures, mosque, calligraphy, Shari'ah)
  - b06 3B L03: Religious Upbringing as Argument (Proverbs 22:6, Dawkins)
  - b07 × 10: All Paper 4 textual studies lessons

---

## RS-specific quality flags (from fact-check memory)

Three categories of past-drift caught in other RS builds — agents must not repeat:

1. **Attribution errors**: Aquinas given seven Just War criteria (correct: CCC 2309), kalam attributed to Aquinas (correct: al-Ghazali), soul-making attributed to Augustine (correct: Irenaeus/Hick). These are documented in `_AGENT_PROMPT.md` with a reference table.

2. **Scripture fabrication**: invented Qur'an verse numbers, wrong Bible chapter:verse combinations, Guru Granth Sahib page numbers pulled from thin air. The agent prompt instructs: use only citations from `section_markers`; paraphrase without attribution when uncertain.

3. **Mark's Gospel longer ending**: citing Mark 16:9–20. The spec ends at 16:8. Hard ban in agent prompt.

---

## Insertion

After Phase 3 content generation, insert with:
```
python scripts/insert_lessons.py --subject religious-studies-edexcel --workspace scripts/_content_religious-studies-edexcel/lessons/
```
(or the equivalent insertion script for this workspace — check `scripts/` for the latest pattern used by business-edexcel / sociology-aqa builds)
