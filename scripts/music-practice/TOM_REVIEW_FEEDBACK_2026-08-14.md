# Music AQA — Tom's review feedback, 14 Aug 2026

Dictated during the Supabase outage; catalogued as received. Each item gets a
triage note and a fix plan before anything is changed. Nothing here is fixed
until it says so.

---

## Unit: listening-skills

### LS-1 — Whole-tone player in the method card does not play
**Tom:** hit play, nothing happens. Also no SoundCloud-style waveform players on
the gold classical pieces in that lesson — possibly deliberate, he half-recalls
a reason we could not do that.

**Triage:** two separate things.
(a) The dead play button is a defect regardless — either the `audio_url` is
missing/broken on that method-card asset or the player is not wired. Verify the
URL in `practice_data` once Supabase is back; the L1 method-card audio was part
of the real-recordings rebuild (task #46), so a regression there is plausible.
(b) The missing waveform players on gold: the half-remembered reason is likely
the licence rule — the gold classical excerpts came from the PD/CC0-only
sourcing pass, and third-party embeds (SoundCloud) were avoided in favour of
self-hosted R2 audio through our own waveform player (task #44). Confirm
whether gold problems have `audio_url`s that simply lack the waveform wrapper,
or no audio at all. If it was deliberate, write the reason HERE so it stops
being half-remembered.

**Status:** open — needs DB access to verify.

### LS-2 — Audio keeps playing across question/tier transitions
**Tom:** an extract kept playing after answering/skipping onward; playing the
next extract layered both. No stop control at that point. Noticed at the
silver→gold transition; unsure whether it affects every question move or only
tier boundaries.

**Triage:** client-side renderer bug in `practice.html` — no `pause()` on the
active audio element when the problem (or tier screen) changes. This is
investigable RIGHT NOW during the outage, since it is pure front-end code. The
tier-transition observation is a good lead: the tier summary/intro screens are
a different code path from next-problem, and may be the one that skips cleanup.

**Status:** open — investigating locally.

### LS-3 — Repeating a failed tier until you pass it teaches the answers, not the skill
**Tom:** stuck on L3 gold, repeated it three times; by the third pass he was
recognising the answers rather than hearing the music. Structural, not a bug.

**Triage:** design decision, his call on direction. The honest options:
1. **Draw unseen problems first on retry.** The bank holds more problems per
   tier than one pass shows; a retry that prefers unplayed problems tests the
   skill again rather than the memory. Cheapest real fix if bank sizes allow —
   check per-tier counts in listening-skills (music runs smaller banks, ~12-17
   per lesson, so second attempts may partially repeat and third attempts
   will; worth knowing the real numbers before promising this).
2. **Vary the QUESTION on the same audio.** Same excerpt, different ask
   (instrument → texture → cadence). Needs authoring; the flow work from the
   AoS2 pass has the pattern.
3. **Cooldown with teaching between attempts.** Failed tier → back through the
   method card / a worked example before retrying, so the retry follows
   re-instruction rather than immediate memory.
4. **Accept-and-move-on.** Cap retries; after N, mark the tier "revisit later"
   and let the lesson complete — resurfacing handles the return visit. Fits
   the recall-resurfacing design already agreed for lesson completion.

**Status:** open — awaiting Tom's steer on direction; bank-size check queued
for when the DB returns.

---

## Unit: AoS1 listening practice (western-classical-1650-1910)

### AOS1-1 — Irrelevant audio extract beside term-matching questions
**Tom:** on vocab/term-matching questions the extract player sits in the left
panel but is irrelevant — no listening is needed to match terms, and it would
confuse a student. Seen "a couple of times"; explicitly again in Lesson 3
(AOS1-3 below, same defect).

**Triage:** the panel shows whenever a problem carries a `passage_id` — so
either those vocab_match problems reference an excerpt they do not use (data
fix: strip the reference), or the renderer should never show the audio panel
for types that need no audio (renderer guard, prevents recurrence everywhere).
Do both: strip the stray references AND add vocab_match to the no-panel list in
practice.html. Enumerate affected problems by query once the DB is back.

**Status:** open — data query queued; renderer guard can be written now.

### AOS1-2 — Worked example walks through Mozart Symphony No. 40 with no audio
**Tom:** Lesson 2's example teaches you to listen through the piece, then there
is nothing to listen to. He believes the same happens in several lessons —
wants all examples scanned for it.

**Triage:** scannable programmatically: worked_examples (and method-card
audio) that talk about listening but carry no `audio_url`, across every music
unit. Mozart 40 is PD-recordable, so where audio SHOULD exist the licence-clean
sourcing route from the earlier rebuild applies; where no PD recording can be
found, the example text must change rather than promise audio it has not got.

**Status:** open — full scan queued for DB recovery.

### AOS1-3 — Lesson 3 term-matching, same irrelevant extract
Folded into AOS1-1; counted as a second confirmed instance.

### AOS1-4 — Fact-recall questions about untaught pieces are semi-unanswerable
**Tom:** "What is the key of the third movement of Mozart's Clarinet Concerto
K.622?" — no student can answer that if it was never taught; these wider-
repertoire pieces are not our set works, and students use the site TO revise.
He could only answer the Beethoven one in L1 because he had already done the
L3 deep dive. "There are loads of them like that." Wants rework ideas.

**Triage + proposed principle:** align each question with what the EXAM can
ask, which is also what a student can fairly answer:
- **Unfamiliar/wider repertoire → ear questions only.** The exam plays
  unfamiliar music and asks what can be HEARD: mode, tempo, texture,
  instrumentation, cadence. "What key is K.622's third movement" is not
  hearable at GCSE and not askable about unfamiliar music — so on our side,
  any question about a non-set-work must be answerable from the audio in
  front of you.
- **Set works / deep-dive pieces → factual depth allowed.** Key, form,
  context — because we teach them (the Beethoven case proves the pattern:
  taught first, answerable after).
- Where a fact question about a wider piece is worth keeping, precede it with
  a one-line teaching step (the `say` pattern) so it becomes immediate recall,
  not impossible recall.
The rework is then an audit pass: classify every AoS listening question as
ear-answerable / taught-fact / untaught-fact, and rewrite or re-anchor the
third group. Countable by query; the rewrite itself is authored work that
lands on Tom's desk per the ear-verification rule.

**Status:** open — classification query queued; direction agreed in principle?
(Tom to confirm.)

---

## Unit: AoS1 Western Classical — the ARTICLE lessons (incl. study pieces)

### WC-1 — No related media, podcasts, or video on these lessons
**Tom:** wondered if generation started failing; pushed back on the first
triage (rightly — explainer videos DO run on free tier; only cinematic video is
Unity-only) and offered the publish-gate theory.

**Resolved from the batch state files (checkable during the outage):**
- **Podcasts — never queued.** 798 jobs in `_batch_podcast_state.json`, zero
  music. No coded live-only gate by default. Action: run the music-aqa batch
  AFTER Tom's review approves the lessons, so NLM slots are not spent on audio
  his edits might invalidate.
- **Explainers — ran, then dropped the baton.** 27 music jobs: 15 videos
  generated and DOWNLOADED but never attached to lessons; 12 stuck
  in_progress. The videos exist while the lessons show none. Action: complete
  the attach step (verify R2 + Supabase, per the standing rule) for the 15;
  rescue or restart the 12.
- **Related media — genuine gap to verify by query** once the DB returns; if
  the study-piece builds skipped that phase, run it with the mandatory URL
  audit.

**Status:** open — three concrete actions, two runnable at DB recovery, the
podcast batch after Tom's approval.

### WC-2 — The three AI helpers are invisible during the tour
**Tom:** tour step 2 names "Explain it differently / Simplify language / Ask
the tutor", which sit bottom-left; he only just noticed them. The tour should
annotate/point at them on screen. Applies to every article lesson.

**Triage:** front-end (the lesson tour). Fix: anchor that tour step to the
helper buttons (spotlight/arrow), not a floating card. Investigable locally
during the outage.

**Status:** open — local investigation possible now.

### WC-3 — Completion weights should be visible: in the tour, and on the buttons
**Tom:** tour step 4 explains activities add to completion but not what each is
worth. Also: put the weight on each activity control itself — NOT a pill (we
have worked hard to remove AI-looking pills), a small tag, e.g. exam questions
(40), podcast (10) — so students see what to work towards per lesson.

**Triage:** weights already exist in the completion spec (exam 40, flashcards
15, revision task 15, quick quiz 10, video 10, podcast 10; complete at half of
what is available). Two changes: tour copy gains the numbers; the activity
controls gain a quiet weight tag in the site's own type style. Applies to all
article lessons.

**Status:** open — design tweak, front-end + tour copy.

### WC-4 — L2: first "listen box" skipped by narration and styled slightly off
**Tom:** unlike (he believes) all the others; looks a little different too.

**Triage:** both symptoms point at one cause — non-standard markup on that one
box, so the narration selector misses it and the CSS half-applies. Find it in
L2's content_html when the DB is back; fix the markup, then re-narrate that
lesson if the narration text changes.

**Status:** open — query queued.

### WC-5 — L3 (Beethoven): AI feedback shows raw markdown (# and ##)
**Tom:** practice-question feedback rendered hash marks as plain text — janky.

**Triage:** the marker responds in markdown ("# Mark: 2/2 ... **Feedback:**")
and the article-lesson feedback renderer shows it verbatim. Fix client-side in
the feedback insert: convert the minimal markdown set (headings, bold) to
markup — or strip it — in main.js. Also worth instructing the marking prompt
toward plain prose, but the renderer must cope regardless because the model
will drift. Investigable locally now.

**Status:** open — local fix possible now.

### WC-6 — Study-piece lessons: what a student must DO is invisible until the end
**Tom:** the lessons are good, but only the final card gives the student a
task; before that it is listen-and-read with no expectation set.

**Triage:** content/design tweak, pairs with WC-3: an early one-line signpost
("By the end you'll answer X on this movement") and/or the completion tag
making the target visible throughout. Study-piece template change, then applied
to the built lessons.

**Status:** open — direction agreed with WC-3, wording to Tom.

### WC-7 — "Adjust Pins" button visible bottom-left
**Tom:** possibly admin-only because he is signed in as admin — but if not,
students can move the annotated-player pins. Wants it gated properly.

**Triage:** that is the annotated study-piece player's pin editor. Two
questions to answer in code (locally, now): is the button gated by staff
session, and — the part that matters — is the WRITE path gated server-side, or
does the client just hide the button? A hidden button with an open write is the
review-queue bug shape again: gate the data, not the control.

**Status:** open — local code check possible now.

---

## Unit: AoS2 Popular Music (article lessons)

### AOS2-1 — No videos or podcasts here either
Same mechanism as WC-1, now confirmed for a second unit: podcasts never
queued; explainers generated-but-unattached or stuck. Folded into WC-1's three
actions; noting the unit so the attach pass covers it.

### AOS2-2 — L2: exam tip duplicated at the end of the content
**Tom:** "Don't guess what show, film, or game it's from" appears twice near
the bottom — the exam tip repeats content that is already there. Something
needs chopping.

**Triage:** content fix in L2 — likely the same sentence in both
`exam_tip_html` and the closing content block. Query, chop the duplicate,
re-narrate only if the narrated text changes.

**Status:** open — query queued.

### AOS2-3 — L4 needs a listening example for every type it names; use YouTube embeds for pop
**Tom:** L4 discusses types of pop music with nothing to hear. AoS1 has its
examples (the PD sourcing); pop repertoire cannot be PD. Asks: can we embed
videos, played on StudyVault, just linking to YouTube?

**Answer: yes, and it is the right route.** The platform already embeds
YouTube (sidebar player via youtube_video_id); inline embeds inside lesson
content are equally buildable. Licence-wise it is the standard legal path —
playback happens in YouTube's own player, we host nothing. Honest caveats to
design around:
- some label uploads disable embedding — pick embeddable uploads (official
  artist channels usually allow it);
- YouTube links rot — these must join the related-media URL audit;
- some school networks block YouTube — degrade to a labelled link, never a
  silent hole.

**Proposed action:** curate one embeddable example per type named in L4 (and
wherever else pop lessons name a style without audio), wire as inline embeds.
Curation list lands on Tom's desk for the ear check before wiring.

**Status:** open — direction answered; curation to follow.

### AOS2-3b — RESOLVED: the second unit is AoS4 (Western classical since 1910)
Tom clarified: "the one that contains minimalism" — AoS4. Same embed route
applies, for the same reason as pop: Reich/Glass-era repertoire is still in
copyright, so PD sourcing is impossible and YouTube embeds are the only clean
path. The curation list therefore covers BOTH: every type named in AoS2 L4,
and every style named in the AoS4 lessons (minimalism etc.), one embeddable
example each, ear-checked by Tom before wiring.

---

## Unit: score-reading

### SR-1 — L2 Q4 (bronze): question and extract disagree about the time signature
**Tom:** question says the piece has 6/8, asks simple or compound — but the
extract image shows a DIFFERENT piece in simple time, with 2/4 printed on it.

**Triage:** question↔asset mismatch. Either the extract reference points at
the wrong figure or the question text names the wrong signature. Query the
problem's passage/figure pairing when the DB steadies; fix whichever side is
wrong; the notation SVGs are regenerable from `notation.py` inputs.

**Status:** open — asset alignment fix.

### SR-2 — L2 Q10 (extract F): identically notated bars played differently
**Tom:** the question says one bar is "not played in even threes", but bars 1
and 2 look identical on the score — yet sound different. Asks whether that is
his musicianship or our mistake.

**Triage: OUR mistake, by definition.** If two identically notated bars sound
different, the score/audio pair is wrong — either the audio generator applied
a rhythm variant the rendered score does not show, or the score render dropped
a triplet/duplet marking. This is exactly what synthesis was supposed to make
impossible, so extract F's generation inputs need pulling apart. Not a
judgement call and not Tom's ear.

**Status:** open — regenerate/verify extract F's score+audio pair.

### SR-3 — L4: printed dynamics do not change the playback volume
**Tom:** asks if it is a software limitation.

**Triage: CONFIRMED in code, fixable.** `gen_excerpts.py` (music21) sets
velocity only for metre accents (110/70); printed dynamics are drawn by
`notation.py` as labels but never mapped to volume. Fix: scale note velocity
per marking (p≈50, mf≈80, f≈110 or similar) in the generator and regenerate
the dynamics excerpts. Principle for the whole unit: never ask about a feature
the synth does not audibly render.

**Status:** open — implement velocity mapping, regenerate affected excerpts.

### SR-4 — L4 Q4: asks about mf while the annotation circles the p
**Tom:** "What does the marking MF mean?" over a score showing p and f with
the p circled — misread-inviting; caught him. He half-forgives it ("students
should read carefully") but flags it.

**Triage:** the annotation should agree with the ask. Either circle the mf or
ask about the circled p. Distraction by mismatch is not a reading-skills test,
it is noise — and this unit teaches score-READING, so the annotation is the
teaching surface. Fix the pairing.

**Status:** open — asset alignment fix.

### SR-5 — L4 Q6: "legato" notes sound plain, only the staccato contrast is audible
**Tom:** wonders if he does not know what legato really means.

**Triage: his understanding is fine — the synth never renders legato.** No
articulation implementation exists in the generator; staccato reads as audible
only where note gaps were baked in, and "legato" is just the default
disconnected rendering. Fix options: implement slur→connected playback
(overlap/no-gap note timing) and regenerate; or reword the question to
contrast only what is audibly rendered (staccato vs plain). Prefer the first —
legato belongs in a score-reading unit.

**Status:** open — same generator work as SR-3; do together.

---

## Session wrap — 14 Aug

22 items across 5 units: listening-skills 3, AoS1 practice 4, AoS1/WC articles
7, AoS2 3 (+1 resolved to AoS4), score-reading 5.

**Common causes worth naming:**
- Synth fidelity (SR-2/3/5): the generator renders pitch and rhythm but not
  dynamics or articulation — one code fix + regeneration covers all three.
- Question↔asset mismatches (SR-1/4, AOS1-1/3): pairing errors, individually
  small, found by eye — the kind of thing a per-unit pairing check could catch
  mechanically in future builds.
- Pipeline coverage (WC-1/AOS2-1): podcasts never queued for music; explainers
  generated but unattached (15) or stuck (12).
- Design decisions needing Tom: LS-3 (tier retry model), AOS1-4 (ear-vs-fact
  principle — proposed, awaiting confirm), WC-3/6 wording, AOS2-3/AoS4 embed
  curation list (to his desk).

**Everything queryable fires when Supabase steadies**, queued: LS-1 audio_url,
AOS1-1 stray passage refs, AOS1-2 examples-without-audio scan, AOS1-4
classification counts, WC-1 related-media check, WC-4 markup diff, AOS2-2
duplicate tip, SR-1/4 pairings, LS-3 bank sizes.
