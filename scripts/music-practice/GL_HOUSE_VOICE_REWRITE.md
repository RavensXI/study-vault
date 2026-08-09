# GL study-piece house-voice rewrite — brief (Tom approved, 8 Aug)

Rewrite BOTH study-piece Guided Listening lessons in house voice. Same facts, new register.
1. Spalding: music-aqa / aos3-traditional-music / L2 (title contains "Spalding")
2. Queen: music-aqa / aos2-popular-music / L3

## Why (Tom's words)
"None of it makes sense to me... a lot of musical terminology that isn't underlined and defined...
smells a lot like Fable 5 writing and not really like the rest of the website."

## House voice rules (from docs/CONTENT_PROMPT.md register + Tom feedback tonight)
- Short sentences. One idea per sentence. GCSE readability (age 15-16). British English.
- EVERY musical term gets a <dfn class="term" data-def="plain gloss.">term</dfn> on FIRST use per lesson.
- NO critic asides: banned phrases incl "wonderfully", "masterclass", "giveaway", "theatre, not rock",
  "the ear's anchor", "worth banking". Explain purpose plainly instead ("worth naming in an answer" ok).
- No lyrics (multi-word). No "AQA" anywhere (assert). Motif names (Galileo, Bismillah) ok.
- Paragraphs <= ~420 chars so two-column bodies stay short. 2+ body children per card (or only-child).

## Hard constraints (learned tonight — all bit us already)
- DO NOT touch pin data-t values (Tom's saved times: Queen t2 = 5/25/63/84/157; rest as in DB).
- Keep figure blocks (player) EXACTLY as-is incl track buttons/yt ids; Queen t3 = live video sUJkCXE4sAA
  with the q15 note+link card element (KEEP note, can reword to house voice).
- Keep card skeleton: data-title / data-track / data-chapters attrs as currently in DB.
- data-narration-id on every block (unique). Refs: <button class="sv-ap-ref" data-t data-track>N</button>
  re-anchor AT the term they illustrate; never inside a word (the "mus①ic" bug).
- Div/section balance assert on the .sv-listening stage BEFORE saving (regex counts).
- Key Fact blocks: preserve their FACTS verbatim-ish; may reword register but not content claims.
- Overflow target: every card fits at 2293x800 (Tom's 150% ultrawide) AND ideally 1366x768.
  Current failure: Spalding "I Know You Know" card 125px over -> its content must split across
  "I Know You Know" + "Know: the rhythm" + "The hidden detail" cards more evenly.
- Verify after each lesson: Playwright vs http://127.0.0.1:8901/lesson/... (serve.py must run;
  kill plain http.server on 8901 if found), admin session + tour-flag init script, print per-card
  scrollHeight-clientHeight, dots count, chunks count (#study-notes .sv-chunk).

## Fact sources (READ THESE, invent nothing)
- Fresh DB dumps (make before rewrite): tmp/spalding_db.html, tmp/queen_v2_db.html
  (C:\Users\tshau\.claude\jobs\4059242c\tmp\)
- Originals: tmp/spalding_current.html, tmp/queen_current.html (pre-GL article versions, fact-checked)
- Fact allocation warning: in spalding, E major / 84 bpm / two-bar double-bass riff / Emaj7-E7
  chord families / held dischords = LITTLE FLY facts. 176 bpm samba-jazz / fretless bass opening /
  F major chorus / blue notes Ab+Db / B major interlude vamp / reverb-panning-EQ = I KNOW YOU KNOW.
  Unpitched samba percussion open+close / G mixolydian groove / fade-out / some 3/4 / double bass
  (not fretless electric) / scat vocalise / sectional groove-verses-bridge = I ADORE YOU.
  VERIFY each fact's home card against the original dumps before writing.
- Queen facts: see tmp/queen_current.html (six sections, B flat 6 opening chord, keys/metre,
  syllabic/portamento/Scotch snap/word painting, 180 overdubs, D major hard rock/power chords/
  blues notes SSoR, F major travelling home key LoML studio = piano+harp).

## Terms needing dfn gloss (first use, per lesson — non-exhaustive)
a cappella, homorhythmic, arpeggiated, modulation, sforzando (Queen already has some via original
dfn tags — PRESERVE existing dfn tags when reusing sentences), syllabic, portamento, Scotch snap,
word painting, octaves, homophonic, alla breve/compound time, power chords, blues notes, falsetto,
sonority, texture, vocalise/scat, chamber music, tremolo, imitation, arco, pizzicato (last four done),
riff, vamp, syncopation, polyrhythm, mixolydian/mode, fretless bass, dischord, fade-out.

## Pin tips
Keep the pin-tip contract (see QUEEN_GL_V2_PLAN.md): "Term — what you hear right now", facts only.
Spalding tips may need updating where prose fact-allocation was wrong (e.g. t2c2 "176 bpm" tip is
right; t1 tips currently thin — improve from Little Fly facts above).

## After both lessons
- Re-verify Beethoven L3 untouched. Report to Tom. No git push needed (content-only) but note
  main.js/css already pushed at sv-v19/sv-v21.
- Then: "any other fixes" queue = Save-pins credential fix on preview; Spalding pin ear-pass ask;
  flashcards task #42.

## Pin-copy contract (Tom, 9 Aug)
Pins are TEACHABLE MOMENTS, not section markers. Every pin must be anchored by exactly one numbered
ref in the copy, at the sentence that teaches it; every hear-it-worthy claim gets a pin. No
unreferenced pins (deleted "Strings alone"). Machine-audit: pin data-t set == ref data-t set per track.

## Embed ladder result (9 Aug)
Little Fly t1 = MgeAQNBXKk0, the auto-generated album art-track (3:33) - PLAYS embedded and is the
set recording (Tom ear-confirmed). Precedent: Concord (indie) art-tracks allow embedding where
UMG/SME blocked theirs. Ladder step: try the art-track even when majors have refused before.
Spalding deck now: t1 album audio / t2 Official Audio / t3 Album Version - all set recordings.

## Fact-check pass 9 Aug (all three embed decks)
Source: BBC Bitesize AQA GCSE Music ARTICLES (not the older /guides/ pages, which cover the PREVIOUS
study-piece rotation - Beatles/Santana/Copland). Tom saved the pages to "BBC Bitesize Music.txt" in
repo root because bbc.co.uk blocks our web fetcher entirely; use that file, or his browser.
Facts used, prose written fresh (facts are not copyrightable; their wording is).
Errors found and fixed: Bartok 7 (see above), Queen 3, Spalding 4.
