# Diagram Pipeline — Pictorial Isotype Infographics

> **Unity-bespoke ONLY.** Free-tier lessons do not have Gemini diagrams — quality was too inconsistent at scale, and 299 existing Gemini figures were stripped from free-tier content on 22 Apr 2026. See the PIPELINE.md feature matrix.

> **GPT-image-2 replacement under evaluation.** OpenAI's image model produces significantly better diagrams (accurate text, scientific symbols, historical accuracy) at ~£0.12/image. Two-step pipeline planned: Claude agent decides if a diagram is genuinely additive, writes diagram type + content description, injected into a fixed template → GPT-image-2 generates. Parked pending QA completion. See `memory/gpt_image_2_evaluation.md` and `test-diagrams/`.

> **API Integration:** This document is read by the orchestration code and injected into the Gemini API call for Unity diagram generation.

Subject-agnostic process for creating data-driven pictorial infographics for Unity lesson pages. Established with Sport Science.

> **Default approach: Gemini-only.** The diagram prompt (stored on `pipeline_steps.diagram_prompt`) is sent directly to Gemini without a matplotlib baseline. For data-driven subjects, Claude Code generates matplotlib code as a separate inline step before calling the Gemini script.

> **Claude-API-based QA is DISABLED.** `scripts/lib/claude_qa.py` burned Anthropic API credits against Tom's separate account. Diagram QA is now done by Claude Code reviewing the generated images directly with the Read tool. Do not re-enable `claude_qa.py` without Tom's sign-off. See `memory/feedback_no_api_credits.md`.

---

## Overview

Every lesson gets one diagram. The pipeline produces a **pictorial isotype infographic** — a data visualisation where thematic icons and illustrations represent the data instead of abstract bars and lines. Think "editorial magazine infographic" or "BBC Bitesize visual" — something a teenager would find engaging and memorable.

Example: a chart about cardiac arrest survival shows rows of 10 human figures, with surviving figures in bold colour and non-surviving ones greyed out. A chart about pineapple production would use different-sized pineapples instead of bars.

---

## The 4 Steps

### Step 1: Research real data

Spin up research agents (one per lesson) to find citable statistics from peer-reviewed studies, government data (NHS, Sport England, ONS, etc.), or established academic sources.

- Data must be **factual and citable** — no made-up illustrative numbers
- Each agent returns chart-ready datasets with full source citations
- Look for data that tells a story relevant to the lesson content (e.g. injury rates by sport, survival rates over time, prevalence comparisons)

### Step 2: Generate matplotlib baseline

Use matplotlib to create a data-accurate chart. This step exists purely to **lock in the correct data** — visual polish doesn't matter yet.

- Chart types: bar, horizontal bar, grouped bar, line, dual-panel — whatever suits the data
- Use the subject's colour palette (see colour table below)
- Include source citation text on the chart itself
- Script naming: `generate_{subject}_diagrams.py`
- Output naming: `diagram_descriptive_name.jpg` in the subject's lesson folder

**Subject colour palettes:**

| Subject | Palette (dark → light) |
|---------|----------------------|
| Sport Science (orange) | `#9a3412` → `#c2410c` → `#ea580c` → `#f97316` → `#fb923c` → `#fdba74` |
| Business Theme 1 (cyan) | `#075985` → `#0891b2` → `#06b6d4` → `#22d3ee` → `#38bdf8` |
| Business Theme 2 (emerald) | `#064e3b` → `#059669` → `#10b981` → `#34d399` |
| Geography Paper 1 (indigo) | `#312e81` → `#4338ca` → `#4f46e5` → `#6366f1` → `#818cf8` |
| Geography Paper 2 (red) | `#7f1d1d` → `#b91c1c` → `#dc2626` → `#ef4444` → `#f87171` |
| History (varies by unit) | See CLAUDE.md unit colour themes |

### Step 3: Gemini pictorial isotype redesign

Send the matplotlib JPG to Gemini as input alongside a detailed prompt. Gemini transforms it into a thematic pictorial infographic.

**Model:** `gemini-3.1-flash-image-preview`
**API key:** `$GEMINI_API_KEY` environment variable (never hardcode)

**API call format:**
```python
import json, base64, urllib.request

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3.1-flash-image-preview"

with open(matplotlib_path, "rb") as f:
    img_data = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "contents": [{"parts": [
        {"text": prompt},
        {"inlineData": {"mimeType": "image/jpeg", "data": img_data}}
    ]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                             headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(req, timeout=180) as resp:
    result = json.loads(resp.read().decode("utf-8"))

for candidate in result.get("candidates", []):
    for part in candidate.get("content", {}).get("parts", []):
        if "inlineData" in part:
            img_bytes = base64.b64decode(part["inlineData"]["data"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)
```

Use `responseModalities: ["TEXT", "IMAGE"]` — NOT `responseMimeType`. The API returns both a text commentary and the generated image.

**Prompt template:**

```
You are a world-class infographic designer creating a pictorial isotype chart
for a GCSE [Subject] revision website (students aged 15-16). The site uses a
[colour] theme.

I'm giving you a matplotlib chart with REAL DATA. Transform it into a THEMATIC
PICTORIAL INFOGRAPHIC — not just a prettier chart, but one where the visual
metaphor matches the topic.

STYLE DIRECTION — PICTORIAL / ISOTYPE:
- Instead of abstract bars or lines, represent the data using THEMATIC ICONS
  or ILLUSTRATIONS related to the subject
- For example: if this were about football injuries, the bars would be made of
  stacked football boots. If about survival rates, show rows of human figures
  where surviving ones are bold [colour] and non-surviving ones are greyed out.
- Think "editorial magazine infographic" or "BBC Bitesize visual"
- Icons/illustrations should be clean, flat-design, vector-style (not realistic
  or photographic)

THIS CHART: [describe what the data shows]
[list specific data points with exact numbers]

VISUAL FORMAT: [describe how icons should represent the data — be specific
about what each icon means, how many to show, what colours to use]

DATA RULES:
- Preserve ALL numbers exactly
- Include source: "[citation]"
- Include key message: "[takeaway]"

DESIGN RULES:
- [Subject] colour scheme (primary: #XXXXXX, accents: ...)
- Landscape orientation, roughly 1800x1050 pixels
- White or very light warm cream background
- Clean modern sans-serif typography
- No watermarks, no photographic elements, no AI artifacts
- Flat design, vector-illustration style
```

**Key prompting tips:**
- Be extremely specific about the VISUAL FORMAT section — tell Gemini exactly what icons to use, how many, and what each represents
- Specify exact figure counts (e.g. "exactly 10 figures per row, each = 10%") to keep the maths clean and readable
- Include all data points explicitly in the prompt — don't rely on Gemini reading them from the matplotlib image
- Name the exact colours to use (hex codes)

### Step 4: Automated QA (built into `generate_diagrams.py`)

QA is now **automatic** — after each Gemini generation, the image is sent to Claude Sonnet for review. If QA fails, the prompt is wrapped with anti-garbling guardrails and regenerated. Up to 3 attempts per diagram. Only uploads to R2 when QA passes.

**QA module:** `scripts/lib/claude_qa.py` — requires `ANTHROPIC_API_KEY` env var.

**QA checklist (checked by Claude Sonnet):**
1. **Text accuracy** — any misspellings, garbled text, truncated words, or nonsensical text?
2. **Duplicate labels** — any text label appearing more than once when it shouldn't?
3. **Arrow/flow issues** — arrows pointing wrong directions, excessive/redundant arrows?
4. **Content accuracy** — is the scientific content accurate and relevant?
5. **Visual quality** — any AI artifacts, blurry areas, cut-off elements?
6. **Prompt leaks** — any visible hex codes, "GCSE", "aged 15-16", or other meta-text?
7. **Colour scheme** — does the diagram use the unit's accent colour?

**Guardrails applied on retry:** Anti-garbling prefix added to prompt on attempts 2+. Instructs Gemini to spell-check all text, avoid rendering meta-instructions, avoid duplicate labels, and use the correct accent colour.

**To skip QA** (e.g. for speed during testing): `--skip-qa` flag.

**Manual QA scripts** (for retroactive checks on existing diagrams):
- `scripts/qa_pull_diagrams.py` — download all diagrams for a subject from R2
- `scripts/qa_regen_diagrams.py` — regenerate specific failing diagrams

---

## Helper Scripts

**Subject-agnostic script (new, recommended):**
- `scripts/generate_diagrams.py --job-id <uuid>` — processes any subject by reading `diagram_prompt` from `pipeline_steps`. Accepts `--lessons 1,2,3` filter and `--dry-run`. Uses shared library (`scripts/lib/`).

**Per-subject scripts (deprecated, kept for reference):**
- `scripts/generate_drama_diagrams.py`
- `scripts/gemini_regen.py` (standalone helper for single diagram re-generation)

### `scripts/generate_diagrams.py` (recommended)

Generic diagram generator that works for any subject. Reads the `diagram_prompt` stored on each lesson's `pipeline_steps` row and sends it to Gemini. Usage:

```
python scripts/generate_diagrams.py --job-id <uuid>
python scripts/generate_diagrams.py --job-id <uuid> --lessons 1,2,3
python scripts/generate_diagrams.py --job-id <uuid> --dry-run
```

### `scripts/gemini_regen.py`

Regeneration helper for QC agents. Takes a matplotlib backup image, an output path, and a prompt file:

```
python scripts/gemini_regen.py <matplotlib_backup.jpg> <output.jpg> <prompt.txt>
```

The agent writes its corrected prompt to a `.txt` file, then calls this script. 180-second timeout.

### `generate_{subject}_diagrams.py` (deprecated)

Per-subject matplotlib generation script. Contains one function per lesson that creates the data-accurate baseline chart. Run with:

```
python generate_{subject}_diagrams.py
```

Generates all diagrams for the subject in one go. Skips existing files unless forced.

### `generate_{subject}_gemini_infographics.py` (deprecated)

Per-subject Gemini batch script. Contains tailored pictorial prompts for each lesson. Backs up matplotlib originals as `*_matplotlib.jpg` before overwriting. 5-second delay between API calls for rate limiting.

---

## Diagram Placement in Lessons

Position diagrams at **content-relevant locations** — not always at the top of the lesson. The diagram should appear next to the content it illustrates.

Good placement examples:
- A diagram about injury types → after the section explaining those injury types
- A chart comparing conditions → between the sections on those conditions
- A survival rate chart → after the section discussing why timing matters

HTML pattern:
```html
<figure class="diagram">
  <img src="diagram_descriptive_name.jpg"
       alt="Descriptive alt text explaining what the infographic shows">
</figure>
```

Keep diagrams well away from other images (15+ lines of content between). Full width, 720px max.

---

## Common Gemini Issues

These are the most frequent problems found during QC — watch for them:

| Issue | Description | Fix |
|-------|-------------|-----|
| Duplicate labels | Text appears both above and below icons | Explicitly state "label ONLY above" or "label ONLY below" in prompt |
| Garbled text | Overlapping or corrupted label text | Simplify labels, reduce text density in prompt |
| Wrong order | Data items rearranged from the original | Number the items in the prompt ("1. First, 2. Second...") |
| Mismatched panels | Multi-panel layouts with swapped content | Describe each panel's position explicitly ("LEFT panel shows X, RIGHT panel shows Y") |
| Packed figures | Isotype figures too close together to count | Specify spacing ("clear gap between each figure") |
| Missing elements | Callouts or annotations dropped | List required annotations as a separate checklist in the prompt |
| Data hallucination | Numbers changed from the original | Always cross-reference against matplotlib backup |

## GPT-Image-2 house style (agreed with Tom, 4 Sep 2026)

Bake-off of 4 Sep (GPT-Image-2 vs MAI-Image-2.6 vs 2.6-Flash on Foundry, ten
GCSE diagram prompts): GPT-Image-2 at MEDIUM quality is the pick — nine of ten
usable, 1,756 output tokens per 1024² image, billed £30 per million on Foundry
(≈5.3p). LOW (196 tokens) got electron counts and a valve label wrong; HIGH is
three times the price for no accuracy gain on diagrams. Endpoint:
`POST {FOUNDRY_ENDPOINT}/openai/v1/images/generations`, header `api-key`,
body `{prompt, model:"gpt-image-2", size, quality:"medium"}`. Page:
https://claude.ai/code/artifact/96301c0a-13bd-4e33-8dc6-dae5da48706c

### Prompt template

Two parts. The **brief** is written per lesson by a Claude agent from the
lesson content (pay for reasoning in Claude, not in the image model). The
**style block** is fixed.

```
{diagram_form} of {subject}: {content sentence or two}.
These labels must appear, spelled exactly like this: {label list}.
The diagram must show: {2-3 facts the vision gate will check}.
Do not include a title, a caption or a key. Any lettering on drawn objects must be real,
correctly spelled words in English or the period language, appropriate to the date shown.

Style: a modern GCSE textbook illustration on a warm off-white paper background
(#faf8f5), clean vector-like line work with soft flat colour fills and gentle
shading for depth. Use the accent colour {accent} ONLY for label text, leader
lines and arrows. Physical materials keep their natural colours (rock browns
and greys, magma orange-red, water blue, vegetation green, oxygenated blood
red, deoxygenated blood blue); abstract shapes with no natural colour (circuit
symbols, wave curves, geometry) in neutral greys. Clear humanist sans-serif
labels with thin leader lines, generous margins, no photographic realism, no
clutter, no logos, no real people, no exam-board names.
```

- `{diagram_form}`: name it every time — flat cross-section, 3D block
  cutaway, flat schematic, flowchart, dot-and-cross, labelled graph, timeline.
  Left unnamed, the same prompt comes back in different forms across a unit.
- `{accent}`: `units.accent` from Supabase.
- A key is added ONLY when colour carries meaning (blood, states of matter,
  plate types); otherwise the labels do the work and a key duplicates them.
- Title and caption never go in the image. The lesson heading already exists
  and the caption lives in the HTML `<figcaption>` (editable, narratable).
- Size: landscape 3:2 (`1536x1024`) fits the 1000px article column better
  than square. Read the token count on the first image — it differs from the
  1,756 measured at 1024².
- Foundation lessons: the label list excludes Higher-only terms; a Higher
  diagram gets its own brief.

### Vision gate (mandatory, same as heroes)

A Claude vision pass receives the label list and the fact list and answers
three questions: every label present and spelled correctly? every OTHER word in
the picture legible, correctly spelled, right for the date and suitable for a
GCSE audience (unverifiable text is flagged for Tom, not rejected)? each fact
true in the picture? Period insignia are allowed where accurate (Tom, 4 Sep):
the gate does not sanitise history. Any "no" rejects the image and the retry prompt
carries the gate's note ("the aorta arrows pointed into the heart"). Even
GPT-Image-2 medium drew a sector with its apex off-centre and MAI-2.6 reversed
the aorta, so nothing ships ungated. Budget one retry in three.

### Rollout rule

Canary before fleet: one unit end to end (brief → image → gate → retry →
figure inserted, with the real accepted-diagram cost read from the Foundry
monitor) before any wider run. Estimate at 4 Sep prices: ≈£185 for one diagram
per free-tier lesson at 1024², before retries and before the landscape
re-measure.

### Visual forms (Tom, 4 Sep 2026): not every lesson wants a labelled diagram

The brief agent chooses ONE `visual_form` per lesson, and `none` is a valid
answer (a themed literary-analysis lesson or an ethics debate has nothing to
draw; do not force one). Forms:

| Form | Use when | Text allowed in the image | Gate checks |
|---|---|---|---|
| `labelled-diagram` | a structure or process with parts (sciences, physical geography, maths) | the closed label list only | labels present, spelled, none extra; facts true |
| `data-picture` | one number series carries the point (hyperinflation, casualty figures, unemployment, trade) | axis titles + the supplied data points, verbatim | every number matches the lesson; axis scale honest (log labelled as log) |
| `scene` (RARE) | an idea that a single object-metaphor can carry without a caption (a split figure, a ledger, a map torn in two). Tom rejected the Versailles table scene (4 Sep): faceless figures read as creepy and the picture did not explain itself. Rules: no faceless people; people only as anonymous anchor figures with normal faces (the wheelbarrow worker), never named historical figures; if the idea needs a caption to be understood, choose `none` instead | at most one short in-picture word the brief supplies | objects/dress period-correct; no invented text; a reader can say what it means without the caption |
| `timeline` / `sequence` | order carries the meaning | the supplied dates/step names | order and dates match the lesson |
| `map` | place carries the meaning | the supplied place names | places positioned correctly; borders of the right year |

Landscape `1536x1024` at medium returned 1,372 output tokens (≈4.1p), LESS
than the 1,756 at 1024² — landscape is both the better fit and the cheaper
size. Worked example of `data-picture` (4 Sep, Weimar hyperinflation with the
wheelbarrow, approved by Tom) is in the session scratchpad
`foundry/gpt-image-2-scene__hist-hyperinflation.png`; the Versailles `scene`
was rejected.
