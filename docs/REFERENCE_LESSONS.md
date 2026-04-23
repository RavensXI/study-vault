# Reference Lessons

Pinned Supabase lesson IDs that the content pipeline uses as structural examples. Agents fetch these specific lessons, never "pick a recent one" — that's how drift (Level descriptors, component codes, spec codes) propagated in previous builds.

---

## Article format — `religious-education/christianity-practices/1` "Worship & Prayer"

| Field | Value |
|---|---|
| Lesson ID | `21447890-d512-42c6-85f9-90b4133c06e3` |
| Subject ID | `8efd391b-1981-46a2-a22f-0baf45925c2b` |
| Unit ID | `e0d9cc87-9854-4d91-a646-fa3a72644d05` |
| Subject | Religious Education (AQA 8062), generic / free-tier |
| URL | `/lesson/religious-education/christianity-practices/1` |

**Why this is the reference:**
- Zero copyright drift — no spec codes, no component codes, no Level descriptors anywhere. Mark schemes use StudyVault rubric format correctly.
- 817 words of content, 3 collapsibles, 2 key-facts with actionable revision tips (e.g. *"Without looking, name the four forms of Christian worship and write one distinguishing feature of each"* — not vague exam advice).
- 9 glossary terms, all inline as `<dfn class="term" data-def="…">`.
- 5 flashcards, 5 knowledge checks (2 MCQ + 2 fill + 1 match), 6 practice questions.
- Proper HTML entity usage (`&mdash;`, `&lsquo;`, `&ldquo;`, `&rdquo;`).
- No `<!-- DIAGRAM -->` placeholder — correct pattern for free-tier article lessons.
- 2026-spec-updated, AQA (the dominant board), conceptual subject that generalises cleanly to History, English Lit, Sociology, Psychology, etc.

**Fetching it in a script:**
```python
from lib.supabase_client import get_client
sb = get_client()
reference = sb.table('lessons').select('*').eq('id', '21447890-d512-42c6-85f9-90b4133c06e3').single().execute().data
# Use reference['content_html'] as the structural example injected into the content agent prompt.
```

---

## Practice format — `english-language/paper-1-reading/1` "Explicit and Implicit Information"

| Field | Value |
|---|---|
| Lesson ID | `83ab6156-e0e5-4011-bb79-2c7a70bbdc41` |
| Subject ID | `efa491aa-c7f2-4c5d-91e5-f156afe97f7c` |
| Unit ID | `852ddb2e-a761-44ec-a090-60e67c6631df` |
| Subject | English Language (AQA 8700), generic / free-tier |
| URL | `/practice/english-language/paper-1-reading/1` |

**Why this is the reference:**
- Zero copyright drift — no spec codes, no component codes, no Level descriptors, no exam board rubric phrasing anywhere in `practice_data`.
- Schema-defining: this is the lesson the factory pipeline was built around. Everything in `scripts/factory/FACTORY_RULES.md` was validated on this lesson first.
- Full structural coverage: method card with 5 imperative steps, exam_context set, 2 worked examples (Bronze + Silver tier), full 20-problem bank (8 Bronze / 7 Silver / 5 Gold), AI marking prompts defined for `inference` and `evaluation`.
- Seven different input types showcased: `ai_mark`, `connotation_picker`, `evidence_match`, `highlight_evidence`, `misleading_summary`, `multiple_choice`, `traffic_light`. Demonstrates the variety an article-skill practice unit can contain.
- Free-tier (school_id NULL) — matches the target audience for nearly every future build.

**Fetching it in a script:**
```python
from lib.supabase_client import get_client
sb = get_client()
reference = sb.table('lessons').select('*').eq('id', '83ab6156-e0e5-4011-bb79-2c7a70bbdc41').single().execute().data
# Use reference['practice_data'] as the structural example injected into practice factory stages.
```

**Which practice subjects follow this pattern:**
- English Language (all 4 boards) — uses exactly this shape
- Geography Skills — similar shape plus custom centre panels (charts, OS maps, ruler, stats tools)
- Languages (Spanish/French/German) — similar shape with language-specific input types (see `scripts/language-practice/PRACTICE_DATA_SCHEMA.md`)
- Science calculation units — similar shape with equation hint toggles (see `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md`)

---

## Practice format (Language/MFL-style) — `spanish/popular-culture/1` "Free-Time Activities and Hobbies"

Language practice has seven input types that exist nowhere else on the platform. Agents building French, German, Spanish, or any new GCSE language need a language-specific reference — the English Lang reference doesn't cover dictation audio, target-language AI marking, role play scenarios, or grammar-drill input types.

| Field | Value |
|---|---|
| Lesson ID | `934d507a-841c-48ed-8608-836ea49cc7f4` |
| Subject ID | `0e28f9e6-a5c4-453d-94d1-273adcfc6a93` |
| Unit ID | `96e32322-136b-4756-b07a-986261db45e6` |
| Subject | Spanish (AQA 8692), Unity bespoke |
| URL | `/practice/spanish/popular-culture/1` |

**Why this lesson:**
- Zero copyright drift
- **Ten distinct input types showcased in one lesson** — more variety than any other practice reference: `vocab_match` (×2), `gap_fill` (×3), `translate` (×4, both directions), `dictation` (×3, audio-based), `sentence_builder` (×2), `multiple_choice` (×2), `spot_correct`, `reorder`, `role_play`, `ai_mark`
- All three language AI marking prompts defined: `writing` (extended response), `role_play` (Paper 2 scenarios), `translate_to_target` (English → target language)
- `target_lang: "es"` consistently set on every problem — this field drives language-specific accent bars, dictation voice selection, and SSML narration pipeline
- 3 worked examples across tiers, proper Bronze/Silver/Gold distribution
- &ldquo;Hobbies&rdquo; is a universal GCSE language topic — generalises cleanly to French, German, Italian, Mandarin, or any future language build

**Fetching it:**
```python
from lib.supabase_client import get_client
sb = get_client()
reference = sb.table('lessons').select('*').eq('id', '934d507a-841c-48ed-8608-836ea49cc7f4').single().execute().data
```

**Schema details:** `scripts/language-practice/PRACTICE_DATA_SCHEMA.md` covers the full 12 language input types, tier distribution rules, and the target_lang / dictation audio / AI marking conventions. Agents fetching this reference should also read that schema doc.

**Which practice subjects follow this pattern:**
- Spanish, French, German (all Unity, AQA) — use exactly this shape
- Any new GCSE language build (Italian, Mandarin, Latin language paper, Polish, etc.)
- NOT: English Language (different — passage-based analysis, different input types), Maths (different — calculation-based), Science calcs (different — equation recall)

Caveat: this reference is Unity-bespoke (school_id set), because no free-tier Spanish currently exists. The structural pattern is identical regardless of tier — when free-tier languages get built, they'll follow this exact shape. School_id is set at the subject row, not baked into the practice_data itself, so the reference is safe to use for free-tier builds.

---

## Practice format (Maths-style) — `maths-aqa/graphs/3` "Quadratic Graphs"

Maths is structurally different enough from the English Language practice shape that it needs its own pin. No passages. Different input types entirely. Deterministic solutions, no AI marking prompts. Lesson-level tier flag instead of per-problem. Chart.js inline on some problems.

| Field | Value |
|---|---|
| Lesson ID | `c8bc060f-c094-4b04-abec-5577523f8667` |
| Subject ID | `d7155cfc-805d-4703-a2c2-3b9c858ce2cc` |
| Unit ID | `42867546-7cf3-4c7c-8c25-38c988a6ad89` |
| Subject | Mathematics (AQA 8300), generic / free-tier |
| URL | `/practice/maths-aqa/graphs/3` |

**Why this lesson:**
- Zero copyright drift across all 20 problems
- Showcases three of the five Maths input types in one lesson: `multiple_choice`, `single_value`, and the Maths-unique `two_solutions` (used when an equation has two valid roots — agents building Maths-adjacent subjects like Further Maths need to see this)
- Full 20-problem tier distribution (Bronze/Silver/Gold), 3 worked examples, clean misconception entries
- Mid-course topic, not a trivial warm-up — shows what a substantive Maths lesson looks like

**For the Chart.js inline problem pattern** (graph-plotting questions where students read values off an embedded Chart.js chart), cross-reference `maths-aqa/graphs/1` "Plotting & Reading Linear Graphs" (ID `cc326bc8-362b-4a54-875c-f7a7ffc1b77d`). Agents should fetch this secondary reference only when a lesson needs chart-embedded questions.

**Schema details:** see `memory/project_maths_practice_rebuild.md` for the full Maths `practice_data` schema including the five input types, misconception pattern registry, Foundation/Higher lesson-level tiering, and Chart.js config conventions.

**Which practice subjects follow this pattern:**
- Mathematics (all 4 boards) — uses exactly this shape
- Statistics, Further Maths, Astronomy calculations — if built, would follow this shape
- NOT: English Language, Languages, Science calcs — those have their own shapes (see above)

---

## Maintenance

If a reference lesson is edited in `/admin/editor`, re-validate compliance before the next subject build. A reference lesson that drifts will drift every future lesson generated from it. Check for:
- Spec codes in description or content_html (grep for board codes like `8062`, `J277`, `1MA1`)
- Level descriptors in practice question mark schemes (grep `Level [1-9]`)
- Component codes in practice question types (grep `Component \d`, `Paper \d`)
- StudyVault rubric present (Mastering / Secure / Developing / Emerging)

Validation script: `scripts/_audit_reference_candidates.py` (run before any subject build).
