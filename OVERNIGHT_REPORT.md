# Overnight Pilot Build — Morning Report (23 Apr 2026)

## TL;DR

Two subjects shipped through the rebuilt pipeline. Content complete for both. Narration complete for Business. Heroes partially complete due to Unsplash rate-limit (50/hour on demo tier). Podcasts deliberately skipped — need your NotebookLM browser session.

Everything is on branch `pipeline-rebuild-pilot-overnight`, pushed to origin. Vercel preview: https://github.com/RavensXI/study-vault/pull/new/pipeline-rebuild-pilot-overnight

All lessons are `status: pending_review` — invisible to students, visible to you at `/admin/review`.

---

## Business Studies (AQA 8132) — free-tier

**Subject ID:** `0490733d-622e-41ac-a1b6-eb3e7293f8fd` · slug `business-aqa`

| Asset | Coverage | Notes |
|---|---|---|
| Content (article) | 30/30 | All 6 units, 800-928 words per lesson |
| Hero images | 21/30 | Unsplash rate-limited — retry in ~1 hour to fill the remaining 9 |
| Narration (Azure TTS) | 30/30 | Ollie/Ada alternating, uploaded to R2 |
| Related media | 30/30 | ~300 items curated + verified across categories |
| Revision guides | 8/8 | Hub + 7 techniques with Business-specific examples |
| Exam guides | — | Intentionally skipped per rebuild decision |
| Cinematic video | — | Free-tier policy: skip |
| Podcasts | — | Deferred to you (NotebookLM) |

**Unit structure** (all article format):
1. Business in the Real World (6L)
2. Influences on Business (5L)
3. Business Operations (4L)
4. Human Resources (4L)
5. Marketing (6L)
6. Finance (5L)

**Live 2026 spec change** picked up by grounded research: AQA has altered the 6-mark Analyse question to allow (not require) multiple factors with developed chains. All mark schemes reflect this. Confirmed "not tested": Maslow theory, exchange-rate conversions, drawing break-even/PLC charts, full cash-flow construction.

---

## French (AQA 8652) — free-tier

**Subject ID:** `ce35f41d-2a29-4001-bd66-93c399ad3c35` · slug `french-aqa`

| Asset | Coverage | Notes |
|---|---|---|
| Content (practice) | 26/26 | All 3 units, 20 problems per lesson, 10 input types |
| Dictation audio | 78 clips | French Azure voices (Henri/Denise), all uploaded to R2 |
| Hero images | 3/26 | Unsplash rate-limited — retry to fill remaining 23 |
| Narration (content) | 0/26 | **Gap** — `batch_narration.py` only handles `content_html`, not practice lessons' `practice_data`. Unity Spanish has method-card narration (32 entries). Needs a dedicated generator — flagged for the follow-up. |
| Related media | 26/26 | ~270 items with Lesson Podcast placeholders |
| Revision guides | 8/8 | Filled with French-specific examples (SSC drills, MRS VANDERTRAMP, etc.) |
| Podcasts | — | Deferred (NotebookLM) |

**Unit structure** (all practice format):
1. People and Lifestyle (10L)
2. Popular Culture (8L)
3. Communication and the World Around Us (8L)

**Note on French content:** The first content agent (P&L 1-5) reused existing Unity French source content (`scripts/language-practice/french_people-and-lifestyle.json`) and wrapped it in the new free-tier schema. All agents followed the Spanish L1 reference for structure but wrote fresh French where no source existed. Content is identical or near-identical to Unity French for units where source files existed — which is fine given both are AQA 8652, but worth knowing.

---

## Things I left for you

### 1. Heroes — retry after rate-limit resets (~1 hour from last attempt)

The Unsplash free-tier key is rate-limited at 50/hour. I burned through it. To top up the remaining 35 heroes (9 Business + 23 French):

```bash
python scripts/_batch_heroes_generic.py scripts/_gen_business/
python scripts/_batch_heroes_french.py
```

Each run will get partway through before hitting the limit. Run both a few times across the morning.

### 2. Podcasts — NotebookLM browser auth

Both subjects have Lesson Podcast placeholders in their `related_media`. When you run:

```bash
python scripts/batch_podcasts.py --subject business-aqa
python scripts/batch_podcasts.py --subject french-aqa
```

...the podcast URLs will replace the `#` placeholders automatically.

### 3. French method-card narration

French practice lessons have no `narration_manifest`. Unity Spanish has 32 narration entries per practice lesson (method card + worked examples). To match, we'd need a variant of `batch_narration.py` that reads `practice_data.method_card.content` and narrates the worked example steps. Not blocking — the practice page works fine without it — but missing parity with Unity.

### 4. Homepage additions to `index.html`

Neither new subject appears in the free-tier picker or homepage card grid. The changes span ~5 locations:
- `.home-card` in the subject grid
- `.picker-item` in the picker modal
- `subjectMeta` dict (~line 819 of index.html)
- `subjectBoards` dict (~line 957)
- Category list for the accordion picker (~line 1081)

I left this manual since you said you might handle it yourself. Happy to do it on your signal.

### 5. Gemini diagram policy — not affected

Free-tier policy per PIPELINE.md: no Gemini diagrams. Neither subject has any diagram figures in `content_html`.

---

## Drift & quality observations

### Content agent behaviour
- Most agents validated clean on first pass (24/30 Business, 22/26 French).
- Six Business agents self-retried when content came in short (<800 words) and fixed it without a second prompt.
- One found the existing Unity French source file and reused it wholesale (good pragmatic call; worth noting).
- Zero spec-code leaks, zero Level-descriptor leaks, zero component-code leaks across 56 lessons.

### Planning agent observation
- The Business planning agent's `teaching_brief` included one citation to **Save My Exams** (explicitly on the PLANNING_PROMPT.md forbidden list). I stripped all `source` fields from the teaching_brief before passing it to content agents, so no content inherits the forbidden source. Recommend tightening the planning prompt's source enforcement — the agent's summary message says it avoided forbidden sources, but it didn't.

### Practice agent observation
- Four of the six French agents reused or semi-reused existing Unity practice JSONs from `scripts/language-practice/french_*.json`. They noted this in their summaries. If the intent was for free-tier French to be distinct from Unity French, we have work to do; if parity is fine, this is a non-issue.

---

## Review links

Once you're logged in as admin:
- **Business:** `/browse/business-aqa` (will be empty until homepage is wired up — use direct lesson URLs like `/lesson/business-aqa/business-real-world/1`)
- **French:** `/practice/french-aqa/people-and-lifestyle/1`
- **Admin review:** `/admin/review` — should list the 56 `pending_review` lessons

---

## Files changed (branch `pipeline-rebuild-pilot-overnight`)

- 64 files changed, ~41K insertions, ~12K deletions
- Mostly docs/ restructure + new orchestration scripts
- Commit: `Pipeline rebuild v2 + pilot subjects (Business AQA, French AQA free-tier)`

Not committed: generated content JSONs under `scripts/_gen_business/` and `scripts/_gen_french/` — they're the handoff artefacts, contents already in Supabase. Left in working tree in case you want to inspect them.

---

## Task state

All task IDs #15–#27 are resolved except:
- #22 Business assets (heroes partial — 21/30)
- #23 French assets (heroes partial — 3/26; narration gap)
- #25 Podcast attempt (deferred to you)

Everything else completed.
