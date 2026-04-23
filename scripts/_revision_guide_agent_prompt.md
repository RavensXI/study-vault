# Revision Guide Fill-In Agent Prompt Template

Agent fills in `{{SUBJECT_EXAMPLE_1}}`, `{{SUBJECT_EXAMPLE_2}}`, `{{SUBJECT_NAME}}`, `{{SUBJECT_SLUG}}`, `{{OTHER_TECHNIQUES_LINKS}}` across all 7 canonical revision-technique templates plus the hub page — then inserts them as rows in `guide_pages` table.

One agent per subject build (not per technique).

---

You are filling in 7 revision-technique guide pages plus a hub page for a new GCSE subject build on StudyVault.

## Subject context

**Subject:** {{SUBJECT_NAME}} ({{EXAM_BOARD}} {{SPEC_CODE}})
**Subject slug (for URLs):** `{{SUBJECT_SLUG}}`
**Subject ID (for Supabase):** `{{SUBJECT_ID}}`
**Target audience:** {{TARGET_AUDIENCE}}

## What you do

For each of the 8 template files in `docs/REVISION_TECHNIQUES/` (7 techniques + hub), produce the final HTML by substituting placeholders. Then insert them into Supabase.

### Templates to process

- `docs/REVISION_TECHNIQUES/hub.html` → slug `index`, sort_order 0
- `docs/REVISION_TECHNIQUES/retrieval-practice.html` → slug `retrieval-practice`, sort_order 1
- `docs/REVISION_TECHNIQUES/spaced-repetition.html` → slug `spaced-repetition`, sort_order 2
- `docs/REVISION_TECHNIQUES/interleaving.html` → slug `interleaving`, sort_order 3
- `docs/REVISION_TECHNIQUES/dual-coding.html` → slug `dual-coding`, sort_order 4
- `docs/REVISION_TECHNIQUES/elaborative-interrogation.html` → slug `elaborative-interrogation`, sort_order 5
- `docs/REVISION_TECHNIQUES/knowledge-organisers.html` → slug `knowledge-organisers`, sort_order 6
- `docs/REVISION_TECHNIQUES/timed-practice.html` → slug `timed-practice`, sort_order 7

### Placeholders to substitute

1. `{{SUBJECT_NAME}}` — with `{{SUBJECT_NAME}}` (literal)
2. `{{SUBJECT_SLUG}}` — with `{{SUBJECT_SLUG}}` (literal)
3. `{{SUBJECT_EXAMPLE_1}}` and `{{SUBJECT_EXAMPLE_2}}` — two distinct worked examples per technique, specific to this subject. 2-4 sentences each. See example quality bar in `docs/REVISION_TECHNIQUES/README.md`.
4. `{{OTHER_TECHNIQUES_LINKS}}` — in each technique page's sidebar, list links to the other 6 techniques (not this one). Format:
   ```
   <a href="/guide/{{SUBJECT_SLUG}}/revision-technique/retrieval-practice" class="sidebar-media-item"><strong>Retrieval Practice</strong></a>
   <a href="/guide/{{SUBJECT_SLUG}}/revision-technique/spaced-repetition" class="sidebar-media-item"><strong>Spaced Repetition</strong></a>
   ... etc, excluding the current page's technique
   ```
5. `{{HUB_INTRO}}` (hub page only) — one sentence, e.g. "Evidence-based techniques proven by cognitive science, tailored to GCSE {{SUBJECT_NAME}}."
6. `{{OPTIONAL_SUBJECT_SPECIFIC_CARD}}` (hub page only) — leave empty unless there's a genuinely subject-specific 8th technique you want to add (e.g. "Practising Calculations" for Science, "Vocabulary Laddering" for MFL). Most subjects skip this.

### Example quality

- Must use real {{SUBJECT_NAME}} content — real topics, real question types, real example content from this subject's spec
- Must be SPECIFIC, not generic. Not "use this technique in {{SUBJECT_NAME}}" but "After studying X, try Y". See README.md examples.
- Must show the technique in action
- 2-4 sentences each

Examples aim to make the technique vivid for a {{SUBJECT_NAME}} student — something they can try tomorrow.

### Insert into Supabase

After producing all 8 HTML strings, insert into the `guide_pages` table:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath('scripts/_insert_dummy')))
from lib.supabase_client import get_client
sb = get_client()

SUBJECT_ID = "{{SUBJECT_ID}}"
GUIDE_TYPE = "revision-technique"

pages = [
    {"slug": "index", "title": "Revision Techniques", "content_html": hub_html, "sort_order": 0},
    {"slug": "retrieval-practice", "title": "Retrieval Practice", "content_html": rp_html, "sort_order": 1},
    # ... etc
]
for p in pages:
    existing = sb.table("guide_pages").select("id").eq("subject_id", SUBJECT_ID).eq("guide_type", GUIDE_TYPE).eq("slug", p["slug"]).execute().data
    if existing:
        sb.table("guide_pages").update({...}).eq("id", existing[0]["id"]).execute()
    else:
        sb.table("guide_pages").insert({
            "subject_id": SUBJECT_ID,
            "guide_type": GUIDE_TYPE,
            "slug": p["slug"],
            "title": p["title"],
            "content_html": p["content_html"],
            "sort_order": p["sort_order"],
        }).execute()
```

Do NOT set `subjects.settings.has_exam_guides = true` — that's reserved for Unity-bespoke subjects with exam technique guides. This is revision-technique only.

## Return

Short summary: number of guide pages inserted/updated. Flag any placeholder you couldn't substitute (should be none).
