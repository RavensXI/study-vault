# Video Pipeline — Cinematic Overviews & Podcasts

Automated generation of NotebookLM cinematic video overviews and lesson podcasts for all 370 lessons.

---

## Prerequisites

- **Google AI Ultra subscription** (£120/mo intro, £235/mo after) — required for cinematic video overviews (20/day limit)
- **notebooklm-mcp-cli** — unofficial CLI tool for programmatic NotebookLM access
- **Auth cookies** expire frequently — the script auto-detects expiry and re-runs `nlm login` (see Auto-Reauth below)

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
- `--limit N` — max lessons to process (default: 20 for video, 200 for podcast-only)
- `--subject slug` — only process a specific subject
- `--dry-run` — show what would be generated without doing it
- `--status` — check in-progress jobs
- `--download` — download completed videos, upload to R2, update Supabase
- `--cleanup` — delete NotebookLM notebooks after downloading
- `--podcast-only` — generate only podcasts (keeps notebooks for later video generation)
- `--video-only` — add videos to existing notebooks from a prior podcast-only run

**State file:** `scripts/_cinematic_state.json` — tracks all in-progress and completed jobs across runs.

### Progress & Subject Order

Videos and podcasts generated together from the same notebook. Videos are the bottleneck (20/day limit); podcasts ride free (200/day). In practice, `--podcast-only` was used to front-load podcasts for subjects, then `--video-only` to backfill videos later.

**Status as of 16 Mar 2026:**
- **Cinematic videos on R2:** 16/370 (Sport Science 9 + Food Tech 7)
- **Podcasts on R2:** ~295/370 (see table below)
- **Remaining:** 354 videos, ~75 podcasts (Eng Lit, Science, Geography partial)

| Subject | Lessons | Videos Done | Podcasts Done |
|---------|---------|-------------|---------------|
| Sport Science | 10 | 9 (L02-L10) | 10 |
| Food Technology | 10 | 7 (L02-L08) | 10 |
| Drama | 12 | 0 | 12 |
| Separate Sciences | 22 | 0 | 22 |
| Music | 26 | 0 | 26 |
| Business | 30 | 0 | 30 |
| English Language | 30 | 0 | 30 |
| Geography | 40 | 0 | 37 |
| Religious Education | 40 | 0 | 40 |
| English Literature | 42 | 0 | 11 |
| Science | 48 | 0 | 7 |
| History | 60 | 0 | 60 |
| **Total** | **370** | **16** | **~295** |

**Target:** Complete all 370 by ~April 1st at 20 videos/day.

### How It Works

For each lesson (video + podcast in parallel from the same notebook):

1. **Export content** — strips HTML to clean text, saves to temp file
2. **Create notebook** — `nlm notebook create "{Subject} - {Unit} - L{nn} - {Title}"`
3. **Add source** — `nlm source add {notebook_id} --file {temp_file} --title "Lesson Material"`
4. **Generate video** — `nlm video create {notebook_id} --format cinematic --focus "{prompt}"`
5. **Generate podcast** — `nlm audio create {notebook_id} --focus "{prompt}" --confirm`
6. **Poll status** — `nlm studio status {notebook_id}` (videos take 30-60 mins, podcasts ~5 mins)
7. **Download both** — `nlm download video` + `nlm download audio`
8. **Upload to R2** — video to `studyvault-video`, podcast to `studyvault-audio`
9. **Update Supabase** — video URL in `lessons.youtube_video_id`, podcast URL in `related_media`
10. **Cleanup** — deletes the NotebookLM notebook

### Auto-Reauth

NotebookLM auth cookies expire frequently mid-batch. The script handles this automatically:

- `nlm_run()` wraps all CLI calls and checks stdout/stderr for "Authentication expired" or "Authentication Error"
- On detection, `_reauth()` runs `nlm login` (browser-based) and retries the failed command once
- The `NLM_ENV` dict sets `NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8` to prevent Windows encoding crashes

### R2 Storage

Videos are uploaded to the dedicated `studyvault-video` R2 bucket (not `studyvault-images`):
- **Bucket:** `studyvault-video`
- **Public URL:** `https://pub-157a3979382e4f98b51f7f868078e5a3.r2.dev`
- **Path pattern:** `{subject}/{unit}/cinematic_l{nn}.mp4`
- **Podcasts** go to `studyvault-audio` at `{subject}/{unit}/podcast_l{nn}.mp3`

Note: Some early videos (Sport Science, partial Food Tech) were uploaded to `studyvault-images` before the dedicated video bucket was created. These still work fine.

### Video Player

`lesson-loader.js` detects R2 video URLs (containing `r2.dev/` or ending `.mp4`) and renders:
- **Sidebar:** Dark thumbnail card with play button overlay (class `sidebar-video--gdrive`)
- **Modal:** Native `<video>` element with controls, no autoplay (`preload="metadata"`)
- Existing Google Drive and YouTube embeds continue to work unchanged

---

## Focus Prompt Templates

Video and podcast use different prompts. Video is simpler; podcast includes unit context so the AI hosts know what students have and haven't covered.

### Cinematic Video Prompt

```
This is an overview of the {ordinal} GCSE revision lesson for students
studying {exam_board} {subject_name} ({unit_name}). It covers {title} -
{topic_summary}. Stick only to info present in the source material so
as not to confuse or overwhelm students. Keep language easy to understand
but maintain the key subject-specific terms that students will need to
know for their exams. Explain and define these where appropriate.
```

### Lesson Podcast Prompt

```
This is a lesson podcast for the {ordinal} of {total_lessons} GCSE revision
lessons in the {unit_name} unit, for students studying {exam_board}
{subject_name}. The lesson is called "{title}".

UNIT CONTEXT — here is where this lesson sits in the sequence:
1. The Peacemakers & the 14 Points (covered)
2. The Treaty of Versailles (covered)
3. Reactions to the Treaty <-- THIS LESSON
4. The Wider Peace Settlement (upcoming)
5. The League of Nations (upcoming)
...

The source titled "Lesson Material" is the focus of this podcast. The hosts
should treat lessons before this one as things students have already covered,
and lessons after it as things still to come. They can reference earlier
topics as assumed knowledge and tease future ones briefly, but should not
teach content from other lessons in detail — that is what those lessons are
for.

TONE AND LANGUAGE:
- Two hosts having a natural, engaging conversation — not a lecture.
- Keep language accessible for 15-16 year olds but preserve the key
  subject-specific terms students need for exams. Define and explain these
  when first introduced.
- Use relatable analogies or everyday examples to make concepts stick.
```

The lesson list is generated automatically from the unit's lessons in Supabase.

**Fields:**
- `{ordinal}` — "1st", "2nd", "3rd", etc.
- `{exam_board}` — e.g. "AQA", "Edexcel", "OCR"
- `{subject_name}` — e.g. "Combined Science (Biology Paper 1)"
- `{unit_name}` — e.g. "Conflict & Tension"
- `{title}` — lesson title
- `{topic_summary}` — auto-generated from h2 headings in the lesson content

**Important:** Only the lesson content is added as a source (titled "Lesson Material"). No external sources — keeps the output consistent and spec-aligned.

---

## Podcast Integration

Podcasts are generated in the same batch as cinematic videos — same notebook, same source, same focus prompt. The script fires off both `nlm video create` and `nlm audio create` from each notebook.

**Storage:** Podcast MP3s uploaded to R2 `studyvault-audio` at `{subject}/{unit}/podcast_l{nn}.mp3`.

**Supabase:** Podcast URL stored in the lesson's `related_media` JSON under the "Podcasts" category with title "Lesson Podcast".

**Player:** Integrated into the narration player as a tabbed pill toggle (Narration / Lesson Podcast). Tabs only appear when a lesson has both narration and a podcast. When podcast tab is active, the player switches to single-file mode with progress bar seeking. When "Podcasts" category appears in sidebar Related Media, it's renamed to "Other Podcasts" and the "Lesson Podcast" item is filtered out (since it's in the player).

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
