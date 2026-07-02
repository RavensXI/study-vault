# Handover — StudyVault "Shorts" feature (short-form video revision feed)

**Written 2 Jul 2026** for the next session. Broader project context lives in `CLAUDE.md` (loaded automatically) and the auto-memory (`memory/MEMORY.md` → `memory/project_shorts_feed.md`). This doc is the *immediate state* of the one feature we've been building, and how to resume it.

---

## 1. TL;DR — where we're up to

We're prototyping a **TikTok-style vertical "doom-scroll" feed of NotebookLM short videos**, scoped to a student's GCSE subjects, in the reader-skin design. It's a **design-lab prototype** (`design-lab/shorts.html`), **not yet in production**. The feed UX is complete and validated; content and question-mapping are partially built.

- **130 shorts banked** across 36 lessons / 18 subjects (in R2 + `scripts/_shorts_manifest.json`).
- **Recall-check questions mapped for 14 of 34** focused-short lessons; 20 still unmapped (feed shows a placeholder for those — harmless).
- **The batch is paused** on the NotebookLM auth-expiry fail-safe. To add more shorts: Tom runs `nlm login` (interactive, only he can), then relaunch the batch.
- **All work is committed on branch `sandbox`, NOT pushed** (Tom's rule: commit locally, wait for explicit "push"/"deploy").
- **One decision is pending Tom** (see §6): keep grinding the full ~700-short library now (~8 more login cycles) vs. bank the 130 we have, re-map all lessons, and treat the rest as a background top-up.

## 2. What the feature is

A student opens the feed and scrolls through ~60-second vertical videos, each covering **one section of one lesson** (4 focused shorts per lesson), mixed across their subjects. Every 5 genuinely-watched shorts, a **recall check** (a real QA'd question) is spliced in. There's a deliberate **"Done for today"** endcap (finite, anti-doomscroll — not infinite).

Everything is styled in the **reader skin**: warm ground `#f2efe9`, framed portrait cards floating (not full-bleed black), per-subject accent framing, Schibsted Grotesk + Literata, soft shadows.

## 3. The three moving parts

### (a) Video generation — the batch
- **`scripts/batch_short_videos.py`** — hardened, self-contained daily batch: generate → poll → download → upload to R2 → delete notebook. Single-instance lock, orphan-notebook sweep on startup (`NB_PREFIX="SVSHORT"`), date-stamped 180/day quota (`scripts/_shorts_daily.json`), **fail-safe auth** (raises `AuthExpired` and exits code 2 — never tries interactive login mid-run).
- Uses the **`nlm` CLI** (`notebooklm-mcp-cli`, currently v0.8.1). `video create --format short --focus "<section>" --confirm`. Auth via cookies in `~/.notebooklm-mcp-cli/profiles/default`.
- **R2 key:** `shorts/{subject}/{unit}/L{NN}_{idx}.mp4` (bucket `studyvault-video`, public host `pub-157a3979382e4f98b51f7f868078e5a3.r2.dev`).
- **Source of truth:** `scripts/_shorts_manifest.json` (append-only). Fields per short: `lesson_id, subject, unit, lesson_number, title, topic, topic_index, url, created_at`. `topic` = an `<h2>` section heading; `topic_index` = its index in the lesson's section list.
- Scheduled task **"StudyVaultShorts"** runs `scripts/run_shorts.cmd` every 25h (but it also hits the auth wall — needs fresh cookies at run time).
- **Key gotcha (already handled):** NotebookLM **re-IDs artifacts** between pending→done, so never pre-capture artifact ids — download `completed` items by their *current* id and label them via the `custom_instructions` field (`topic_from_instructions()`).

### (b) The feed UI
- **`design-lab/shorts.html`** — single self-contained file. Fetches `/scripts/_shorts_manifest.json` + `/scripts/_shorts_questions.json`.
- **Served** by `design-lab/serve.py` (root-served) on **http://127.0.0.1:8901/design-lab/shorts.html**. Do NOT open the raw file (`file://`) — the absolute fetch paths only resolve through the server.
- Interactions built + verified: **tap = pause/play** (first tap turns sound on, since frame 1 is muted under browser autoplay law); **swipe/scroll = next** (+ unmutes); **sound on by default**; **auto-advance** when a short finishes; **chrome auto-fades after 10s**, returns on any touch; **recall check every 5 genuinely-watched shorts** (counts a short only past 50% or completion — engagement-gated, spliced in live).
- **Posters:** `scripts/_make_short_posters.py` extracts a frame per short (ffmpeg) to `design-lab/_posters/` mirroring the R2 key. Needed because **`r2.dev` ignores HTTP range requests**, so `<video>` can't stream — the poster paints instantly while the clip buffers. **Only the first 29 shorts have posters so far**; re-run the script to cover the new 100 (it skips existing; downloads each MP4 with a browser UA to dodge r2.dev's bot-403).
- **Production note:** r2.dev is dev-tier (no range, rate-limited). Real deployment needs a **custom domain in front of R2** (range + CDN) before video streams smoothly.

### (c) Question mapping (recall checks)
Reuses each lesson's **already-QA'd** knowledge checks — no new content to review. KC types `mcq` and `fill` both carry `options[]` + `correct`, so both map straight onto the 4-option tap card (`match` type excluded). Re-runnable 3-step pipeline:
1. **`scripts/_shorts_fetch_qbank.py`** → `scratchpad/_shorts_qbank.json` — pulls each shorts-lesson's `sections` (h2s) + usable KCs. Deterministic, no model.
2. **A workflow** (`map-short-questions`) tags the best-fit KC to each short's section — **one Sonnet agent per lesson**. This is the only model step and MUST run via the Claude Code subscription (a workflow/agent), NOT the Anthropic API (Tom's rule) — so it can't live inside the Python batch. Save its returned `{results:[...]}` to `scratchpad/_shorts_picks.json`.
3. **`scripts/_shorts_assemble_questions.py`** → `scripts/_shorts_questions.json` (`lesson_id → {topic_index: {q,opts,correct,type}}`). **Note:** the assembler *rebuilds* the file from the picks — so to add the 20 unmapped lessons you must either re-tag **all** shorts-lessons in one workflow run, or extend the assembler to merge with the existing file. Feed loads this and falls back to a placeholder for any unmapped short.

## 4. How to run / resume everything

```bash
# from the worktree: C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox

# serve the prototype
python design-lab/serve.py            # then open http://127.0.0.1:8901/design-lab/shorts.html

# resume the video batch (Tom must refresh auth first — interactive, only he can):
#   in the chat prompt he types:  ! nlm login
# then relaunch (run in background):
python -u scripts/batch_short_videos.py --daily-cap 180
#   useful flags: --status  --dry-run  --limit N  --subject <slug>  --sweep-only

# re-run question mapping after more shorts are banked (see §3c):
python scripts/_shorts_fetch_qbank.py                 # -> scratchpad/_shorts_qbank.json
#   ...run the map-short-questions workflow over the lessons-with-shorts,
#      save its {results:[...]} to scratchpad/_shorts_picks.json...
python scripts/_shorts_assemble_questions.py          # -> scripts/_shorts_questions.json

# regenerate posters for newly-banked shorts (optional; skips existing):
python scripts/_make_short_posters.py
```

**The auth wall:** each `nlm login` buys ~one session (~90 generations / ~23 lessons / ~67 banked shorts) before NotebookLM drops the token. It's usage-triggered, not our 180/day cap, and re-auth is interactive so it can't be automated. Finishing the ~180-lesson queue (~700 shorts) = ~8 more login+relaunch cycles.

## 5. Exact state (2 Jul 2026)

- **Branch `sandbox`**, committed not pushed. Shorts commits (newest first): `07d49989` (manifest snapshot), `035818ce` (question mapping), `d31b46a9` (tap-to-pause), `a970fc29` (chrome fade), `e292fe00` (caption clearance + engagement-gated checks), `8486e79b` (auto-advance + sound), `b4affed9` (feed prototype), `954ad132`/`4f0a6f0f`/`96069ffc` (batch build).
- **130 shorts / 36 lessons / 18 subjects** banked; **14 lessons mapped, 20 unmapped**.
- Untracked/intermediate (regenerable, safe to ignore or clean): `scratchpad/_shorts_qbank.json`, `scratchpad/_shorts_picks.json`, `scripts/_test_short_video.py`.

## 6. Pending decision for Tom

Batch paused. Options I put to him (awaiting answer):
- **(Recommended) Bank the 130 as the feature's content set**, re-map all 34 shorts-lessons in one pass, call the *feature* done; treat the remaining ~570 shorts as a background top-up he does whenever (one `nlm login` + relaunch, no rush — manifest resumes cleanly).
- **Or keep grinding the full library now** — ~8 more supervised login+relaunch cycles.

## 7. Open items / next steps

- **Re-map the 20 unmapped lessons** (once he decides §6) — needs the all-lessons re-tag or a merge-aware assembler (§3c).
- **Done-card stat** still counts *all* shorts as "topics revised" rather than watched-only — wire to the real watched count.
- **Posters** for shorts #30–130 not generated yet (§3b).
- **Feature graduation:** decide if/when this leaves `design-lab` for the real platform, and how a student *reaches* it (a "Shorts" entry point on the dashboard).
- **Production serving:** custom domain in front of R2 for range/streaming before real use.

## 8. Broader context — the wider redesign (a sibling effort, NOT part of shorts)

The shorts feed is one thread of a larger **summer 2026 visual redesign** that's mostly settled. The detail is in auto-loaded memory (read these before touching lesson/unit/hero design):
- **`memory/project_summer_redesign.md`** — the **Reader skin** is the LOCKED platform look. Tokens: `--bg-body:#f7f6f4`/white cards, text `#1d1c1a`/`#54524d`/`#7f7c75`, `--border-light:#e6e4e0`, **radius 8px/6px**, flat (subtle shadows only), easing `cubic-bezier(.22,1,.36,1)`, **Schibsted Grotesk** (head/UI) + **Literata** (body), **one muted accent per subject**. Lives in `css/reskin.css` under `body[data-skin="reader"]`, applied to lesson + all student templates + rebuilt homepage. The shorts feed uses these exact tokens.
- **`memory/project_progressive_fidelity_backdrops.md`** — the **line-and-wash** (pen-and-ink + thin watercolour wash on cream) is the LOCKED **signature hero style** for every lesson hero. Refined-only (the mastery-ladder idea was dropped). Generated by Gemini **Pro** img2img on the real hero; refused heroes (real people/sensitive) get person-free original art auto-generated from the lesson title. Accent-tinting was rejected. **Piloted on SAM's History (40/40); platform-wide rollout (~2,741 unique heroes, ~$360 on the Google AI Ultra credit) is PENDING Tom's greenlight.** (NotebookLM shorts happen to render in a similar line-and-wash look, so they sit naturally in the skin.)
- **`memory/project_dashboard_two_door.md`** — dashboard direction (Guided vs Revision).
- **`memory/project_hero_caption_standard.md`** — site-wide hero caption format + Wikimedia attribution audit (CC BY-SA copyleft = the derivative-licence risk).

All of the above is on branch `sandbox`, nothing pushed. The prototypes live in `design-lab/*.html` (e.g. `dashboard-paths-cards.html`, `hero-showcase.html`, `_pilot-history.html`). `design-lab/skin-switcher.js` swaps heroes to their line-and-wash variant locally.

## 9. Standing constraints (from Tom / memory — don't violate)

- All AI work via the **Claude Code subscription, never the Anthropic API**.
- **Don't auto-push/deploy** — commit locally, wait for explicit "push"/"deploy"/"open PR". Every push spawns a Vercel preview.
- Work on the **`sandbox` worktree** only; don't `cd` to the main repo.
- **Never wipe Supabase rows**; never mix generic and school-specific content.
- Default fan-out **agents to Sonnet**; use **Opus for code/planning**. (Ultracode was on this session — workflows encouraged.)
- Never pass LaTeX through a shell heredoc (backslashes get mangled).
- Tom prefers **prose over multiple-choice menus** for design/strategy calls; "do the work, don't defer."
