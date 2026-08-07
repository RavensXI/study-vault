# Annotated Study-Piece Player — Build Plan (execute on usage reset)

Tom's idea, 7 Aug: a large player for the Beethoven study-piece lesson with
the full recording and clickable feature annotations that seek the audio.
Target: AoS1 L3 (Beethoven Symphony No. 1, mvt 1 — the COMPULSORY study
piece), using the hosted US Marine Band recording (lesson-01.mp3, 581.5s,
PD 17 U.S.C. §105).

## Why Beethoven (and what it does NOT apply to)
Seeking requires HOSTED audio. Beethoven qualifies. Bartok's extracts are
YouTube embeds (in-copyright) — cannot seek; Bartok keeps prose timestamps.
Viable follow-ons (phase 2, also hosted): K.622 Rondo (refrain/episode
buttons) and Haydn 94 mvt 2 (theme + variations buttons) — this makes the
structures teaching audible per lesson L2's forms.

## Component design
- content_html block (NO narration ids → no re-narration):
  <figure class="sv-annotated-player" data-audio="…lesson-01.mp3">
    <figcaption>The whole movement, mapped</figcaption>
    <audio controls preload="metadata"></audio>
    <ol class="sv-ap-chapters">
      <li><button class="sv-ap-chapter" data-t="0">Adagio molto introduction
          — the famous "wrong-key" opening chord …</button></li>
      … one per section, each with a one-line "what to hear" …
    </ol>
  </figure>
- JS (~30 lines) in main.js initLessonFeatures() Phase 2, BOTH main checkout
  and sandbox worktree: click delegate on .sv-ap-chapter → set audio
  .currentTime = data-t, play(); timeupdate listener highlights the active
  chapter. Real <button>s (keyboard-accessible).
- CSS in css/style.css + sandbox css/reskin.css reader-skin overrides:
  house card style, buttons look like buttons, squared corners in reader
  skin, NO coloured left-border stripe. Player sized prominently at the
  lesson's end (replaces the current "complete movement" figure; the
  intro-only clip stays as the first figure).

## Sections to annotate (from AQA's teacher guide landmarks)
Fetch + extract AQA-8271-TEACHER-GUIDE-AOS1-BEETHOVEN.PDF (markitdown works
on these). Chapters: 1 Adagio molto intro (0:00) · 2 Allegro: first subject
(C major, ~1:47 — ALREADY LOCATED, triple-probed) · 3 transition · 4 second
subject (G major, woodwind dialogue) · 5 codetta/exposition end · 6
exposition REPEAT if taken (581s total suggests yes — must detect) · 7
development · 8 recapitulation (first subject back in C) · 9 coda. Plus at
most 2-3 highlight moments (sforzandi passage; timpani) — keep scannable.

## Timestamp methodology (no human ear needed — proven on the intro)
Per boundary: (a) coarse probe (wide window, "at what mm:ss does X begin"),
(b) narrow confirm probe (20-30s window, "does X begin here? at what
offset"), (c) energy/onset profile cross-check where the boundary has an
energy signature. ACCEPT only when two independent probes agree within ±3s.
Then a describe-probe on each chapter's first 8s must match the expected
content (e.g. "woodwind dialogue" for the second subject). Exposition-repeat
detection: probe for a second occurrence of the first-subject opening in the
200-420s range. Record every timestamp + probe evidence in
AUDIO_PROVENANCE.md appendix.

## Verification before telling Tom it works
Playwright on the sandbox worktree: render L3, click every chapter, assert
currentTime jumped to data-t ±0.5s and audio is playing; assert active-
chapter highlight follows on timeupdate; screenshot the player for Tom.
Check both skins (default + reader).

## Files touched
- js/main.js (main checkout + sandbox worktree)
- css/style.css (main) + css/reskin.css (sandbox)
- AoS1 L3 content_html (DB)
- AUDIO_PROVENANCE.md (timestamp evidence), TOM_REVIEW_CHECKLIST.md (add:
  "click every chapter — does each land where its label says?")
- Commits local both branches; preview needs a sandbox push (Tom's word).

## Open questions (answers may arrive from Tom before execution)
1. Granularity: six structural chapters + 2-3 highlight moments is the
   recommendation — more becomes clutter. Confirm or trim.
2. Phase 2 (K.622 rondo map + Haydn variations map, same component):
   recommended, same session if budget allows. Confirm scope.
3. Design authority: build to house style, Tom critiques on the render.
