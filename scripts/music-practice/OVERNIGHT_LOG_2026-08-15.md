# Overnight log — 15 Aug 2026

Tom asleep; reviewing in the morning. Working the music fix programme
(task #53) in catalogue order. Every entry below says what was done, how it
was verified, and whether it was pushed. Anything audible is drafted for
Tom's ear, never shipped as fact.

Check-in discipline: scheduled wakeups every ~25 min; at each one, running
jobs' OUTPUT FILES are checked and stalled work resumed — completion claims
are not trusted (twice bitten today).

---

## Done

- **LS-2 FIXED and proven** — root cause: `stopOrphans()` (the only thing
  able to silence a removed player's detached Audio object) ran only when a
  NEW player was added. Tier summaries add no player, so the removed clip
  played on — audible, invisible, unstoppable; precisely Tom's silver→gold
  sighting. Fix: the observer now reacts to REMOVALS too, plus an explicit
  stop-everything at every tier boundary (intro, celebration, fail modal)
  covering both audio systems. Harness proof: play whole-tone → replace the
  area with a playerless summary → `playing:false` within 600ms. A
  `svPracticeAudioState()` debug hook is exposed for the test suite.
  Pushed.

- **Mechanical fixes applied, verified by fresh re-query, pushed** (834fd846).
  - AOS1-1: all **14** stray excerpt anchors stripped (vocab_match +
    reorder, western-classical L1–L8). The count is 14 not 16: L2's pair
    are multiple_choice on `mozart-40-mvt1` — that is the separate
    "example has no audio" item (AOS1-2/ear-vs-fact), left for that pass.
  - Renderer guard: `vocab_match` never gets a passage panel. **NOT
    reorder** — a pre-flight query showed all 37 EngLang reorder problems
    legitimately use their extract; a blanket guard would have broken
    English Language. Inline-script syntax check clean.
  - SR-1: the 6/8 theory question's wrong "Simple time" anchor removed.
  - AOS2-2 re-diagnosed: the dup was body-paragraph-vs-exam-tip (both
    render). Cut the restating sentence from the un-narrated **tip**;
    narrated body untouched, so no narration desync. L2 + L4 done.
  - WC-4 re-diagnosed: L2's first two sv-listen figures simply lack
    `data-narration-id` — narration skips them, styling differs. Adding
    ids without audio would fake a dead control, so no write; **L2 needs
    re-narration after content approval** (queued below).
  - Backups: `scripts/music-practice/_backup_mechanical_2026-08-15.json`.

- **Score player now PERFORMS the markings** (78a40f10, pushed). The
  dynamics/legato complaints turned out to live in `js/score-player.js`
  (the browser synth behind every Score Reading figure), not the MP3
  drill bank — `gen_excerpts.py` needed no change (no dynamics or
  articulation questions exist in the drill bank).
  - Root causes: flat gain (dynamics printed, never performed — the
    caption even apologised for it); fixed 8% gap (legato impossible);
    staccato faked by shortening `beats`, which shortened the CLOCK, so
    staccato bars **rushed** — that rushing is very likely what made
    extracts with mixed articulation feel wrong.
  - Fix: per-note `vel` + `art` in the map; the clock always advances
    the full printed beat. All ten L4 playables rebuilt; the dynamics
    card now rings **mf** (the thing the bronze question asks about, was
    ringing p — SR-4), ring widened/centred, screenshot-verified.
  - **Found + fixed a real data bug while in there**: L4 Extract H's
    final note played midi 76 against a printed d (74) — a second,
    unclaimed pitch departure. The question claims exactly one.
  - **SR-2 re-diagnosed**: L2 Extract F prints bars 1–2 identically and
    swings bar 2 DELIBERATELY — it is the gold spot-the-departure task,
    not a broken score. Your "is that a mistake with the score?" is the
    framing failing, so the caption now says the departure is deliberate.
    The old staccato clock-rushing will also have muddied comparisons.
  - Proof (stubbed-AudioContext harness, real score-player.js, live
    figures): p/f gain ratio 0.45; staccato sounds 45% of the beat with
    a full-beat clock; legato 103%; Extract H final = 587.3 Hz (74).
  - ⚠ EAR CHECK NEEDED (morning pile): the proofs are behavioural, not
    aural — play L4's figures and L2 Extract F yourself.
  - Note: the pre-fix L4 snapshot in `_backup_score_playables_*.json`
    was overwritten by an idempotent rerun before I added the guard; the
    pre-tonight L4 state would need `fix_score_reading_tiers.py` /
    `fix_last_tiers.py` backups to reconstruct. Restore paths for L2 and
    everything else are intact.

- **AOS1-4 ear-vs-fact worklist DRAFTED** (994ba751, pushed; desk file
  `EAR_VS_FACT_WORKLIST_2026-08-15.md`, nothing applied). Scanned all
  228 practice problems answer-first, then hand-reviewed the 24 flags:
  **8 real rewrites drafted** (named keys/catalogue facts asked as
  listening — including your K.622 example), **9 detach-the-excerpt**
  candidates (good revision questions wearing an irrelevant excerpt —
  your "extract on the left is irrelevant" list), 5 scan
  false-positives kept, and a bonus find: **L8 gold[0] and gold[3] are
  near-duplicate Handel-vs-Verdi questions** — one should go.
- **YouTube curation list DONE** (desk file
  `YOUTUBE_CURATION_2026-08-15.md`, nothing wired). AoS2 L4 gets one
  era anchor per section (Beatles VEVO, Britney VEVO, WSS via Amazon
  MGM, Jurassic Park via UMG Topic); AoS4 L1/L2/L3 get sidebar picks
  (Boosey & Hawkes score video, Hungarian Sketches complete, BBC Proms
  Short Ride) + related-media extras. Every URL oEmbed-verified
  (resolves AND embeddable) and channel-checked; three unofficial
  re-uploads were rejected and replaced along the way.

## Dead ends (so you don't re-walk them)

- **Explainer canaries died.** The two refired music jobs were still
  artifact-less 26 min later (a successful create shows its artifact at
  launch), same as their previous 3 attempts. NLM is still swallowing
  creates for these old notebooks despite pool contention being solved.
  Stopped per plan — no more quota burned. All 39 stuck jobs (12 music,
  19 psychology-edexcel, 8 history-aqa) likely need FRESH notebooks
  rather than refires on the dead ones; that is a decision for your
  morning (it re-uploads sources and re-burns creates). Stale note
  corrected: there were never 15 downloaded-unattached music videos.
  State backup: `scripts/_batch_explainer_state.json.bak-20260815-overnight`.

## In progress

- **Music MC misconception drafts** (desk only, never --apply) running
  in the background across the four practice units
  (`scripts/misconceptions/run_music_drafts.py`, fail-loud loop).
  Next wakeup checks its output file and assembles the desk markdown.

## Queue
MC drafts assembly (job running) → catalogue items that survive the night
(WC-2 tour anchoring, WC-3 weight tags, WC-5 markdown-in-feedback,
WC-6 signpost, WC-7 Adjust Pins gating check).

## For Tom's morning
- whole-tone retest (after LS-2 lands), noting panel vs modal if it recurs
- the 30 pending music lessons (your approval gates the podcast batch)
- ear-check regenerated excerpts (dynamics/legato/extract F) once done below
- post-approval re-narration list so far: aos1-western-classical **L2**
  (two unnarrated listen boxes — WC-4)
- everything in the "drafts" pile below as it accumulates
