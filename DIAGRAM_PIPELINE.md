# Diagram Pipeline — Pictorial Isotype Infographics

Subject-agnostic process for creating data-driven pictorial infographics for lesson pages. Established with Sport Science, reusable for all future subjects.

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

### Step 4: QC agent review

Spin up dedicated QC agents (one per image) to carefully inspect each Gemini output. Each agent gets:

- The generated image to inspect
- The original matplotlib backup for data comparison
- The prompt that was used
- A structured checklist

**QC checklist:**
1. **Text accuracy** — any misspellings, garbled text, or duplicated labels?
2. **Data accuracy** — do all numbers match the original data? Are items in the correct order?
3. **Label duplication** — are labels appearing both above AND below icons (a common Gemini artefact)?
4. **AI artifacts** — any visual glitches, blurry text, or nonsensical elements?
5. **Readability** — can a 15-year-old clearly read all text at normal zoom?
6. **Layout** — is the composition balanced? Is anything cut off or cramped?

**If issues are found:**
- Agent writes a corrected prompt (referencing specific issues to fix)
- Regenerates using `gemini_regen.py` helper script
- Max 3 iterations per image
- If still failing after 3 attempts, keep the matplotlib version

**File management after QC:**
- Final Gemini version → `diagram_name.jpg` (this is what the lesson HTML references)
- Matplotlib backup → `diagram_name_matplotlib.jpg`
- Update alt text in the lesson HTML to describe the pictorial format

---

## Helper Scripts

### `gemini_regen.py`

Regeneration helper for QC agents. Takes a matplotlib backup image, an output path, and a prompt file:

```
python gemini_regen.py <matplotlib_backup.jpg> <output.jpg> <prompt.txt>
```

The agent writes its corrected prompt to a `.txt` file, then calls this script. 180-second timeout.

### `generate_{subject}_diagrams.py`

Per-subject matplotlib generation script. Contains one function per lesson that creates the data-accurate baseline chart. Run with:

```
python generate_{subject}_diagrams.py
```

Generates all diagrams for the subject in one go. Skips existing files unless forced.

### `generate_{subject}_gemini_infographics.py`

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
