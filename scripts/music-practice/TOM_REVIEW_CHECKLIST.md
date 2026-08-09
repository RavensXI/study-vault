# Tom's Music Review Checklist — what's still owed

Tick as you go; tell the session anything that fails and it gets fixed.
Updated 9 Aug (Guided Listening build complete).

## A. From the Guided Listening work — not yet seen by Tom

- [ ] **Queen L3 read-through** (aos2-popular-music/3). The prose was fully
      rewritten in house voice; the player, pins and times were carried over
      untouched. Check it reads plainly for a non-musician, glosses cover every
      term, popups sit correctly.
- [ ] **Queen: Bohemian Rhapsody pins** — the only pin set never ear-verified.
      You approved them by feel before the drag tool existed. One play-through.
- [ ] **Beethoven L3 spot-check** (aos1-western-classical/3). Only two glossary
      definitions were added (crescendo, cadence); everything else untouched.
- [ ] **Bartók: Slightly Tipsy + Swineherd's Dance pins.** Rebuilt 9 Aug on the
      published section structure; timings came from that source's recording,
      not our Boulez one. Drag-check both.
- [ ] **Flashcards — 55 new cards, 11 lessons, none reviewed.** 3 decks written
      in-session (Queen / Spalding / Bartók), 7 by agent from each lesson's own
      content, Beethoven pre-existing. Spot-check a couple of decks.

## B. Older ear checks still owed

### Listening Skills L3 (cadences)
- [ ] **exC_plagal** (silver): softer "Amen" close, not a hard full stop?
- [ ] **exC_imperfect** (gold): does it end HANGING, waiting to continue?
- [ ] **exC_interrupted** (gold): last chord somewhere darker/unexpected?
      (Score-verified; the machine ear can't judge cadence character on synth
      audio. The perfect cadence passed machine votes 3/3.)

### AoS1 L2 (Structures)
- [ ] **Binary miniature**: can you hear A-A-B-B, A ending away from home?
- [ ] **Ternary miniature**: bright A, minor-key B, exact return of A?

### Listening Skills L1 (Tonality)
- [ ] Spot-check the nine rebuilt excerpts, especially the two whole-tone golds.

### Listening Skills L2 (Families)
- [ ] The constructed timpani (bronze percussion) sits among ten real
      recordings — acceptable next to them?

### AoS1 articles
- [ ] Credit lines under embedded extracts — do they name performers properly?
      (Drill-side credits done and hidden behind disclosures; article-side
      lines are agent-written.)

### Carried over from 3 Aug
- [ ] Batch-2 ear-review page: 2 clips / 5 questions await verdicts.
- [ ] 6 public-domain orchestral questions where the distractor audit was
      overruled on documented grounds (Gershwin/Prokofiev/Respighi).

## C. Decisions and actions only Tom can take

- [ ] **Vercel env var**: tick `ADMIN_PASSWORD` for the **Preview** environment
      (Settings → Environment Variables). Removes the Save-pins password prompt.
- [ ] **Flip music-aqa lessons from `pending_review` to live** when satisfied.
- [ ] **Production deploy** of the whole Guided Listening feature + the older
      practice-page fixes (audio-stop + dyslexia font). Everything so far lives
      only on sandbox → landing-wizard preview.
- [ ] **Podcasts** for the music lessons (your NotebookLM batches).
- [ ] **AQA Media CSP booklet** via the exams officer (unblocks task #35).

## Done (was on this list)
- Beethoven annotated player: superseded by the waveform Guided Listening
  build; chapters became pins, all times re-verified.
- Beethoven intro extract boundary: the inline extracts were removed when the
  player took over the lesson.
