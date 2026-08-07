# Annotated Study-Piece Player — Build Plan

**DO NOT EXECUTE until Tom says go.** (His word, 7 Aug dinner-time.)

Tom's idea, 7 Aug: a large player for the Beethoven study-piece lesson with
the full recording and clickable feature annotations that seek the audio.
Target: AoS1 L3 (Beethoven Symphony No. 1, mvt 1 — the COMPULSORY study
piece), using the hosted US Marine Band recording (lesson-01.mp3, 581.5s,
PD 17 U.S.C. §105).

## Why Beethoven (and what it does NOT apply to)
Seeking requires HOSTED audio. Beethoven qualifies. Bartok's extracts are
YouTube embeds (in-copyright) — cannot seek; Bartok keeps prose timestamps.
SCOPE (Tom's call): this is a ONE-OFF for the Beethoven study piece.
Prove it works first. Porting to K.622 Rondo / Haydn 94 (also hosted) is an
optional later conversation only if the component turns out easy to reuse.

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

## Chapters to annotate — DRIVEN BY THE LESSON'S OWN CONTENT (Tom's spec)
Granularity rule: "anything we talk about in this lesson that students need
to know for this study piece." So step 1 of execution is to PARSE AoS1 L3's
content_html and list every analytical claim it teaches (the V7-of-F opening
chord, Adagio molto intro, first subject + sforzandi, second subject in the
dominant with woodwind, development, recapitulation in the tonic, prominent
wind writing, coda, etc.), cross-referenced against the AQA teacher guide
(fetch AQA-8271-TEACHER-GUIDE-AOS1-BEETHOVEN.PDF, markitdown works). Every
taught feature that is locatable in the recording gets a chapter/moment
button; nothing the lesson does not teach gets one. Structural anchors
already known: intro 0:00; Allegro con brio ~1:47 (triple-probed). Detect
whether the exposition repeat is taken (581s suggests yes) since it shifts
all later timestamps.

## Staff chapter editing (Tom's addition, 7 Aug)
Chapters must be adjustable by staff without a code round-trip. Design:
- When the staff flag is present (same studyvault-auth check the loaders
  use), the player shows an "Adjust chapters" toggle.
- In adjust mode every chapter gets: nudge buttons (−1s / +1s) AND a
  "set to here" button that stamps the audio's CURRENT position onto that
  chapter — pause exactly where the boundary really is, click, done. This
  beats dragging for precision, but ALSO render the chapters as markers on
  a click-to-seek timeline strip; markers are draggable in adjust mode for
  coarse moves. Students never see any of this.
- Persistence: "Save chapters" writes the updated list back to the lesson.
  Investigate the admin editor's existing save path first (/admin/editor
  must have one); if it needs a service key we cannot use client-side,
  fallback = the button copies the adjusted chapter JSON to the clipboard
  with a one-line "paste this to the session" instruction, and I apply it.
- Chapter data lives as data-t attributes in the content_html block either
  way, so a save is a single content_html update.

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
Staff mode: toggle adjust, nudge a chapter, "set to here", verify the
data-t updates and (if the save path works) persists after reload.
Check both skins (default + reader).

## Files touched
- js/main.js (main checkout + sandbox worktree)
- css/style.css (main) + css/reskin.css (sandbox)
- AoS1 L3 content_html (DB)
- AUDIO_PROVENANCE.md (timestamp evidence), TOM_REVIEW_CHECKLIST.md (add:
  "click every chapter — does each land where its label says?")
- Commits local both branches; preview needs a sandbox push (Tom's word).

## Questions — ALL ANSWERED by Tom, 7 Aug
1. Granularity: everything the lesson teaches about the piece, no more.
2. Scope: Beethoven one-off; porting is a later maybe.
3. Design: ANSWERED — house style, Tom critiques the render. In the
   reader skin (redesign) the player must be SQUARED OFF like everything
   else there (4px radii, no pill shapes, native audio controls squared via
   the ::-webkit-media-controls-enclosure treatment already in reskin.css).
