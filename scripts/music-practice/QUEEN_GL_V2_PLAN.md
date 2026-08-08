# Queen Guided Listening v2 — work plan (Tom's review, 8 Aug)

Lesson: music-aqa / aos2-popular-music / L3 (id 6f19*-check via query). Sandbox + main checkout, push to landing-wizard preview.

## Tom's four findings
1. **De-AQA the prose.** Remove every "AQA's guide highlights/tracks the way AQA teaches" framing —
   legal exposure (derivative of AQA teaching materials). Keep the musical FACTS (not copyrightable),
   restate in our own words and our own structure. Sweep ALL cards incl. cover + Section B card.
2. **Too verbose — more, smaller cards.** Some cards still scroll. Target: no card over ~90 words body.
3. **Equal weight for all three songs.** Seven Seas of Rhye + Love of My Life need the same player
   treatment as Bohemian Rhapsody:
   - ONE dock player with a **track switcher** (3 tabs). Each track: own videoId, own pins, own dur.
   - Video IDs: extract from the existing lesson's ul blocks (official-video links already whitelisted;
     ul markup in `C:\Users\tshau\.claude\jobs\4059242c\tmp\queen_current.html` blocks 10 & 14).
   - Cards declare `data-track`; when the active card's track differs, dock cues that video
     (cueVideoById) and swaps the visible pin set. Refs carry data-track too (switch then seek).
   - Pin times for SSoR + LoML are ESTIMATES — tell Tom to use Adjust pins → set to here → Save.
     Estimates: SSoR (official ~3:07): intro 0:00 / verse 0:19 / bridge 1:11 / solo 1:33 / seaside outro 2:24.
     LoML (official upload — check duration on cue): intro 0:00 / verse 0:12 / middle 1:10 / instrumental 1:45 / return 2:20.
   - Staff save: pins carry data-cid unique across tracks (t1c1, t2c1...).
4. **Chunk menu broken** (Explain differently / Simplify wording / Ask the tutor — js/simplify.js):
   - Some blocks unselectable: my paragraph splits created <p> without data-narration-id (check what
     simplify.js keys on — recon first: grep selectors + how menu is positioned/appended).
   - Menu "hidden behind text": popover clipped/overlapped inside card columns (column-count) or
     behind sibling cards — z-index/overflow fix; if menu is absolutely positioned inside the card,
     consider appending to body or raising z-index above .sv-ll-track siblings.
   - Verify SAME fixes on Beethoven L3 (Tom hasn't checked it there).

## Engine notes (current state)
- main.js: setupYTFigure (lazy YT.get adapter, fig._ap) + initListeningLesson (carousel).
  SW: sandbox sv-v15, main sv-v13 — bump BOTH on next main.js/css change.
- Local test: python design-lab/serve.py on 127.0.0.1:8901 (rewrites /lesson/). Kill any plain
  http.server on 8901 first. Localhost SW may serve stale assets — unregister + clear caches in tab.
- Playwright CANNOT start YouTube playback (needs real user gesture); verify structure only,
  Tom confirms playback. Screenshots of fixed dock layer unreliable in claude-in-chrome captures —
  trust elementFromPoint/hit-testing.
- Beethoven regression check after any engine change:
  /lesson/music-aqa/aos1-western-classical/3 — canvas painted, ref seeks, pause no re-follow.

## Order of work
1. Recon simplify.js (selectors, menu insertion point) → design fix.
2. Multi-track engine in setupYTFigure (+ CSS for track tabs; keep single-track back-compat for
   possible AoS4 embeds).
3. Content rebuild: de-AQA rewrite, 3-4 tight cards per song + cover + Section B card, refs per track,
   ~12 cards total. Facts source: existing fact-checked prose only — no new claims.
4. Chunk-menu fixes (ids on every block + z-index/clip).
5. Verify (Playwright structure + real-Chrome hit tests), SW bumps, commit BOTH checkouts,
   push origin sandbox:landing-wizard. Preview URL:
   https://study-vault-git-landing-wizard-tom-shauns-projects.vercel.app/lesson/music-aqa/aos2-popular-music/3
6. Report to Tom: what to click, pin-adjust expectations for the two new tracks.

## Also open (unrelated but this lesson)
- Flashcards: only Beethoven L3 has a deck (task #42 subject-wide retrofit).
