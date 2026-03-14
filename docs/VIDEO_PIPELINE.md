# Video Pipeline — Cinematic Overviews & Podcasts

Automated generation of NotebookLM cinematic video overviews and lesson podcasts for all 370 lessons.

---

## Prerequisites

- **Google AI Ultra subscription** (£120/mo intro, £235/mo after) — required for cinematic video overviews (20/day limit)
- **notebooklm-mcp-cli** — unofficial CLI tool for programmatic NotebookLM access
- **Auth cookies** expire frequently — re-run `nlm login` if you get auth errors

### Installation

```bash
pip install notebooklm-mcp-cli
nlm login  # opens browser, extracts cookies
```

### Daily Limits (Ultra tier)

| Feature | Limit |
|---------|-------|
| Cinematic video overviews | 20/day (rolling 24hr window) |
| Standard video overviews | 200/day |
| Audio overviews (podcasts) | 200/day |
| Chat queries | 5,000/day |

No usage tracker in the app — you only find out when it blocks you. The automation script tracks count internally.

---

## Cinematic Video Pipeline

### Script: `scripts/generate_cinematic_videos.py`

Three-phase workflow:

```bash
# Phase 1: Generate (creates notebooks, adds sources, launches renders)
python scripts/generate_cinematic_videos.py --limit 20

# Phase 2: Poll status
python scripts/generate_cinematic_videos.py --status

# Phase 3: Download, upload to R2, update Supabase, clean up notebooks
python scripts/generate_cinematic_videos.py --download --cleanup
```

**Options:**
- `--limit N` — max lessons to process (default: 20, the daily cap)
- `--subject slug` — only process a specific subject
- `--dry-run` — show what would be generated without doing it
- `--status` — check in-progress jobs
- `--download` — download completed videos, upload to R2, update Supabase
- `--cleanup` — delete NotebookLM notebooks after downloading

**State file:** `scripts/_cinematic_state.json` — tracks all in-progress and completed jobs across runs.

### Subject Order (smallest first)

1. Sport Science (10) — DONE
2. Food Technology (10) — 8/10 done
3. Drama (12)
4. Separate Sciences (22)
5. Music (26)
6. Business (30)
7. English Language (30)
8. Religious Education (40)
9. Geography (40)
10. English Literature (42)
11. Science (48)
12. History (60)

At 20/day = ~19 days for all 370 lessons.

### How It Works

For each lesson:

1. **Export content** — strips HTML to clean text, saves to temp file
2. **Create notebook** — `nlm notebook create "{Subject} - {Unit} - L{nn} - {Title}"`
3. **Add source** — `nlm source add {notebook_id} --file {temp_file} --title "Lesson Material"`
4. **Generate video** — `nlm video create {notebook_id} --format cinematic --focus "{prompt}"`
5. **Poll status** — `nlm studio status {notebook_id}` (renders take 30-60 mins)
6. **Download** — `nlm download video {notebook_id} --id {artifact_id}`
7. **Upload to R2** — stored at `{subject}/{unit}/cinematic_{l_nn}.mp4` in `studyvault-images` bucket
8. **Update Supabase** — sets `lessons.youtube_video_id` to the R2 URL
9. **Cleanup** — deletes the NotebookLM notebook (unless keeping for podcast generation)

### Video Player

`lesson-loader.js` detects R2 video URLs (containing `r2.dev/` or ending `.mp4`) and renders:
- **Sidebar:** Dark thumbnail card with play button overlay (class `sidebar-video--gdrive`)
- **Modal:** Native `<video>` element with controls, no autoplay (`preload="metadata"`)
- Existing Google Drive and YouTube embeds continue to work unchanged

---

## Focus Prompt Template

Used for both cinematic videos and podcasts. Adapted per lesson.

```
This is an overview of the {ordinal} GCSE revision lesson for students
studying {exam_board} {subject_name} ({unit_name}). It covers {title} -
{topic_summary}. Stick only to info present in the source material so
as not to confuse or overwhelm students. Keep language easy to understand
but maintain the key subject-specific terms that students will need to
know for their exams. Explain and define these where appropriate.
```

**Fields:**
- `{ordinal}` — "1st", "2nd", "3rd", etc.
- `{exam_board}` — e.g. "AQA", "Edexcel", "OCR"
- `{subject_name}` — e.g. "Combined Science (Biology Paper 1)"
- `{unit_name}` — e.g. "Conflict & Tension"
- `{title}` — lesson title
- `{topic_summary}` — auto-generated from h2 headings in the lesson content

**Important:** Only the lesson content is added as a source (titled "Lesson Material"). No external sources — keeps the output consistent and spec-aligned.

---

## Podcast Pipeline (planned)

Same notebooks can generate audio podcasts. **Do not delete notebooks with `--cleanup` if you also need podcasts.**

```bash
# Generate podcast from existing notebook
nlm audio create {notebook_id} --focus "{prompt}" --confirm

# Download
nlm download audio {notebook_id} --id {artifact_id}
```

Podcasts are stored in lesson `related_media` under the "Podcasts" category with title "Lesson Podcast". The player is integrated into the narration player as a tabbed interface (Narration / Podcast) — see `feature/tabbed-player` branch.

---

## CLI Reference

### Windows Fix

The CLI uses the `rich` library which crashes on Windows with Unicode characters. Always prefix commands with:

```bash
NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 nlm ...
```

The automation script handles this internally via `NLM_ENV`.

### Key Commands

```bash
# Auth
nlm login                          # browser-based auth (cookies expire frequently)

# Notebooks
nlm notebook list                  # list all notebooks (JSON)
nlm notebook create "Title"        # create notebook
nlm notebook delete {id} --confirm # delete notebook

# Sources
nlm source add {nb_id} --file {path} --title "Lesson Material" --wait
nlm source list {nb_id}

# Video
nlm video create {nb_id} --format cinematic --focus "..." --confirm
nlm studio status {nb_id}          # check generation progress
nlm download video {nb_id} --id {artifact_id} --output {path} --no-progress

# Audio
nlm audio create {nb_id} --focus "..." --confirm
nlm download audio {nb_id} --id {artifact_id} --output {path} --no-progress
```

### Video Styles

`nlm video create` supports `--format`: `explainer`, `brief`, `cinematic`
and `--style`: `auto_select`, `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro_print`, `heritage`, `paper_craft`

We use `--format cinematic` (best quality, Ultra-only).

---

## Cost & Storage

- **Google AI Ultra:** £120/mo (intro) / £235/mo (standard). Downgrade to Pro (£16/mo) after video batch is complete.
- **R2 storage:** Videos average ~50 MB each. 370 videos ≈ 18.5 GB. R2 free tier is 10 GB, then $0.015/GB/month ≈ $0.28/mo for overage.
- **R2 egress:** 10 GB free/month, then $0.09/GB. Video streaming will be the main cost if many students watch.
