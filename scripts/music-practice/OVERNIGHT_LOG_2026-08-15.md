# Overnight log — 15 Aug 2026

## 16 Aug — Tom's morning review: every decision applied

Tom ear-checked the score-player work (L4, L2 Extract F, whole-tone) — all
good. Then, one desk item at a time:
- **Ear-vs-fact applied** (c2eeb608): 8 rewrites, 9 detaches, L8 dup dropped.
- **MC diagnoses applied fresh** (2b55eb95): 201/213 music MC problems,
  373 diagnoses; enrich_mc max_tokens 4000→8000.
- **Videos: IN THE BODY, not the sidebar** (b1662d5b) — Tom corrected the
  first wiring; 11 sv-embed figures at the discussing sections; the sidebar
  slot stays reserved for the explainer. New .sv-embed CSS.
- **Tour built** (ee8f1127 + e7515e30): step 2 spotlights the helper
  bubbles; weights on step-4 copy and all five activity controls as
  percent tags (Tom: numbers alone read as question counts; flashcard tag
  had inherited the label's bold — countered in reskin.css).
- **Explainers**: verified none of the 39 stuck lessons has any video
  live; cleared the 27 psych/history entries (state backup
  `.bak-20260816-clear27`) so the hourly dispatcher rebuilds them fresh;
  the 12 music jobs stay PINNED as a deliberate hold until Tom flips the
  30 pending lessons. Shorts confirmed healthy: 3,982 banked, running
  nightly.

**Tier retry BUILT** (655f3c70, 15 Aug evening): two attempts capped, a
worked-example interstitial between them, twice-failed tiers marked "to
revisit" and the lesson moves on; attempt counts + revisit both logged.
E2E-proven on the real page (double-fail run + pass-on-attempt-2 control).
Applies to every guided-practice subject. Note: the interstitial shows the
lesson's best-matching worked example — music lessons each carry one
(bronze/silver), so a gold fail shows that same example; per-tier examples
are an authoring option if Tom wants depth later.

**Still open on #53:** Tom's review of the 30 pending lessons → then clear
the 12 music explainer pins + podcast batch + AoS1 L2 re-narration.

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

- **Music MC misconception drafts DONE — desk copy only** (3db4624e).
  All 211 MC problems across the four practice units carry drafted
  per-distractor diagnoses in
  `scripts/music-practice/MC_MISCONCEPTION_DRAFTS_2026-08-15.md`
  (~$1.15). Same contract as EngLang/MFL; **nothing in the DB** — your
  approval applies them with the standard script. Side fix: enrich_mc
  max_tokens 4000→8000 (aos-listening L3's response truncated mid-JSON
  twice until the bump — deterministic, now clean).
- **WC-7 Adjust Pins: verified safe, no change needed** (54e4baf9).
  The button's role check is cosmetic, but the SAVE posts to
  `/api/pipeline/update-lesson`, which is requireTeacher-gated and
  scope-checked server-side (override layer for shared content). Live
  unauthenticated probe → 401. This is the scope-the-data model working.
- **WC-5 AI-feedback hash marks FIXED** (54e4baf9, pushed). The
  formatter only handled `###`; the marker drifts between `#`, `##`
  and `###`, so hashes leaked as raw text. All three now render as the
  small heading. Proven on the extracted live function + a real render
  with site CSS (screenshot).

## Queue (what's left of the catalogue)
- **WC-2 / WC-3 morning decision packs ready** — tour screenshots saved
  as `scripts/music-practice/wc_tour_step1..8.png` (taken on the live
  psychology lesson; the tour is shared by every article lesson).
  - **WC-2** (step 2, `wc_tour_step2.png`): the spotlight lights the
    PARAGRAPH; the three helper icons pop up small at its bottom-left
    while the card sits far right — nothing points at the icons, which
    is exactly why you only just noticed them. The tour already has a
    spotlight mechanism (`sv-tour-spot`), so my recommendation: when
    step 2 opens, trigger the paragraph popover and move the spotlight
    to enclose the ICON CLUSTER, card beside it. (Alternatives: pulse
    ring on the icons; or move the card next to them. The re-anchor is
    cleanest.)
  - **WC-3** (step 4, `wc_tour_step4.png`): anchoring is already good —
    the gap is copy and controls. Draft tour copy: "Each activity is
    worth points — practice questions 40, flashcards 15, revision task
    15, quiz, video and podcast 10 each. Reach half of what a lesson
    offers and it counts as complete." Controls get a quiet type-style
    tag, no pill: "Quick Quiz · 10", "Flashcards · 15", "Practice
    Questions · 40", and the same on podcast/video where labelled.
  - Say the word on either and I build it.
- WC-6 study-piece completion signpost — design call, parked for morning.
- LS-3 tier retry (4+3 worked-example interstitial, attempt count,
  cap 2) — decided but "don't build this now"; build queued for after
  your review.
- aos1-western-classical L2 re-narration — after you approve content.

## For Tom's morning
- whole-tone retest (after LS-2 lands), noting panel vs modal if it recurs
- the 30 pending music lessons (your approval gates the podcast batch)
- ear-check regenerated excerpts (dynamics/legato/extract F) once done below
- post-approval re-narration list so far: aos1-western-classical **L2**
  (two unnarrated listen boxes — WC-4)
- everything in the "drafts" pile below as it accumulates
