# Archived docs

Superseded by the pipeline rebuild of 22 Apr 2026. Kept for reference but not in active use.

| File | Replaced by | Why |
|---|---|---|
| `SUBJECT_PLAYBOOK.md` | `../PIPELINE.md` | Bloated to 461 lines; still referenced the Unity-bespoke `pipeline_generate.py` / `pipeline_steps` workflow that recent multi-board builds stopped using. New doc is ~270 lines and covers both free-tier and Unity. |
| `PIPELINE_ARCHITECTURE.md` | `../PIPELINE.md` | Content merged into the single master playbook. |
| `GENERATION_PROMPT.md` | `../CONTENT_PROMPT.md` (article) + `../PRACTICE_PIPELINE.md` (practice) + `../PLANNING_PROMPT.md` (planning) | Split by phase so each agent reads only what it needs. Old file conflated planning, content, exam guide generation, and revision guide generation. |
| `SUBJECT_PROMPT.md` | `../CONTENT_PROMPT.md` | Near-duplicate of GENERATION_PROMPT.md. |
| `REVISION_TECHNIQUE_TEMPLATE.md` | `../REVISION_TECHNIQUES/` | Single generic template replaced by 7 canonical technique files with subject-example placeholders. |
| `ROADMAP.md` | `SUBJECT_ROADMAP.md` + `CLAUDE.md` Active TODO | The old roadmap pre-dated the free-tier pivot. Use SUBJECT_ROADMAP.md for subject status and CLAUDE.md for current priorities. |
| `UNITY_AUDIT_REPORT.md`, `UNITY_CONTENT_CHECK_1-4.md`, `UNITY_MEDIA_CHECK.md` | — | One-off audit reports. Historical record only. |

`docs/EXAM_TECHNIQUE_TEMPLATE.md` was deleted entirely — new subjects do not generate exam technique guides (copyright-adjacent; per-lesson `exam_tip_html` + practice question mark schemes carry the load). Existing Unity subjects retain their exam guides — opt-in via `subjects.settings.has_exam_guides: true`, set by `scripts/_flag_existing_exam_guides.py`.
