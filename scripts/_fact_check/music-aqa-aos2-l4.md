# Fact-check: music-aqa / aos2-popular-music / Lesson 4 — "Placing a Track in Time"

Lesson id: `d601ff11-c8f9-49f1-a7f4-1197165795dc`
Checked: 2026-08-09

## Method

- Pulled `content_html`, `knowledge_checks`, `flashcard_questions`, `practice_questions`, `glossary_terms` directly from Supabase (raw dump: `scripts/_fact_check/_music_l4_raw.json`).
- Confirmed the lesson's four-period framework against the actual AQA spec source file `specs/aqa/music-8271-8271.md` (lines 572–588): "music of Broadway 1950s to 1990s / rock music of 1960s and 1970s / film and computer gaming music 1990s to present / pop music 1990s to present." This matches the lesson's opening paragraph exactly (VERIFIED, sourced from spec, not flagged below).
- Verified every other technical/historical claim (instrumentation, effects, recording technology, theatre history, game-audio theory) against external sources: Britannica, Wikipedia (cross-checked against primary/trade sources it cites), Guitar World, Reverb.com, Perfect Circuit, Berklee Online, The Game Audio Co, IUP Press ("The Megamusical"), Antares/UAudio (Auto-Tune history).
- bbc.co.uk was not queried directly (known to block automated fetch); no claim required it — better-fitting specialist/trade sources were used instead.

## Findings

### HIGH — "Timing Test": grid-exact drum timing wrongly dated to "the 1990s or later"

**Quoted text (content_html, Key Fact box, `n8`):**
> "Key Fact — The Timing Test... Ask yourself whether the drums are perfectly even. Human drumming pushes and pulls very slightly. A grid-exact beat almost always means programming, which points to the 1990s or later."

**Also repeated in `flashcard_questions[4]`:**
> Q: "What is the quickest test for whether a track was programmed or played?"
> A: "Listen to the drum timing. Human playing pushes and pulls slightly; grid-exact timing means programming, which points to the 1990s or later."

**And underpins `knowledge_checks[0]`**, where "Drums quantised exactly to the beat" is marked correct as the strongest indicator of "a recording from the 1990s or later."

**What's wrong:** Machine-exact, quantised drum programming was mainstream in pop music a full decade or more before the 1990s. The Linn LM-1 (1980) and Roland TR-808 (1980), and their quantisation function, put grid-exact programmed drums on globally huge 1982 records — Michael Jackson's "Thriller" and Prince's "1999" both use the Linn LM-1 throughout. New wave and synth-pop acts (e.g. Human League's "Don't You Want Me," 1981) were built on the same technology. So "grid-exact = 1990s or later" is wrong by roughly 15 years as a general/historical claim, and it is presented in the lesson as an absolute, exam-technique "test," not scoped to "within this exam's four periods only."

**Why it matters:** It is taught three times (main content, a boxed "Key Fact," and a flashcard) and is the reasoning behind a marked-correct knowledge-check answer. A student who takes the rule at face value and applies it to any real unfamiliar programmed-drum extract that isn't from the specific four AQA periods (e.g. in a mock exam, on the radio, revising more broadly) will misdate it by up to 15 years.

**Note on the exam context:** Within the narrow AQA period set actually tested (rock 1960s–70s / Broadway 1950s–90s / pop or film-game 1990s+ — note the syllabus has no 1980s pop/rock category at all), quantised drums genuinely do rule out "rock 1960s–70s" and point to pop or film/game music, so KC1's marked answer is still the best of the four options given. The error is in the general historical claim taught as fact, not in which MCQ option is marked correct.

**Correction:** Grid-exact/quantised drum programming became mainstream in pop from around 1980–82 (Linn LM-1, Roland TR-808, Oberheim DMX), not "the 1990s or later." Within this exam's four period-categories specifically, grid-exact timing rules out 1960s–70s rock (the technology didn't exist yet) and points to pop or film/game music (1990s+) — but that is a fact about the exam's four buckets, not a general rule that "quantised = 1990s+."

**Sources:**
- https://reverb.com/news/prince-and-the-linn-lm-1 (Linn LM-1 on Prince's "1999" and Michael Jackson's "Thriller," both 1982)
- https://en.wikipedia.org/wiki/Roland_TR-808 (TR-808 launched 1980)
- https://www.perfectcircuit.com/signal/1980s-drum-machines (LM-1 "heard all over early 80s music from Prince ('1999'), Michael Jackson ('Thriller'), ... Human League ('Don't You Want Me')")
- https://www.sweetwater.com/insync/history-of-drum-machines/ (Roger Linn built quantisation into the LM-1 from the start)

---

### LOW — Glossary "Overdrive" is inconsistent with its own in-text tooltip, and narrower than accurate

**Quoted text — inline tooltip (`content_html`, `n6`):**
> `data-def="A warm, gritty distortion made by pushing an amplifier hard."` (overdrive)

**Quoted text — `glossary_terms`:**
> "Overdrive" — "A warm, gritty distortion produced by pushing a valve amplifier hard."

**What's wrong:** The two representations of the same term disagree — the pulled-out glossary card specifies "valve amplifier," the in-lesson tooltip just says "amplifier." Overdrive is most classically associated with pushing a valve/tube amp into clipping, but solid-state amps and dedicated overdrive pedals also produce overdrive; restricting the definition to "valve amplifier" is narrower than the term is generally used.

**Correction:** Align the two definitions, and either drop "valve" or soften to "typically a valve amplifier" since overdrive is not exclusive to tube amps.

**Source:** https://robrobinette.com/Tube_Guitar_Amp_Overdrive.htm ; https://blog.andertons.co.uk/labs/amp-distortion-vs-distortion-pedals-which-is-better (overdrive/distortion produced by both valve and solid-state circuits and by pedals)

---

### LOW — "Sung-through" glossary definition is internally self-contradictory

**Quoted text (`glossary_terms`):**
> "Sung-through" — "A musical with little or no spoken dialogue, where the story is carried entirely in song."

**What's wrong:** "Little... spoken dialogue" and "carried entirely in song" contradict each other — if there is any spoken dialogue, the story is not carried *entirely* in song. (This is a wording slip, not a factual error about the megamusical genre itself, which the lesson otherwise describes accurately.)

**Correction:** "A musical with no spoken dialogue, where the story is carried entirely in song" (drop "little or no"), or "...with little or no spoken dialogue, where almost the whole story is carried in song."

---

## Claims checked and confirmed sound (not flagged above)

- Four AQA periods (Broadway 1950s–90s; rock 1960s–70s; film/gaming 1990s–present; pop 1990s–present) — verbatim match to AQA spec 8271, §3.1.4.
- Fuzz "popular in the 1960s" — Maestro Fuzz-Tone (1962), popularised via the Rolling Stones' "(I Can't Get No) Satisfaction" (1965). https://www.guitarworld.com/features/history-of-the-maestro-fz1
- Hammond organ as a 1960s/70s rock marker — https://bestclassicbands.com/best-rock-organists-9-6-166/ ; corroborated generally (Deep Purple's Jon Lord, Procol Harum, prog rock).
- Double-tracked vocals, "never pitch-corrected," for 1960s/70s rock — technically impossible to be otherwise, since pitch-correction software did not exist until 1997. https://en.wikipedia.org/wiki/Double_tracking ; https://www.waves.com/behind-abbey-road-adt-effect
- "Pitch correction... from the late 1990s onwards" — Auto-Tune released September 1997 by Antares; first prominent/audible use on Cher's "Believe" (1998). https://www.antarestech.com/about ; https://www.uaudio.com/blogs/ua/pitch-correction-basics
- 1950s Broadway large pit orchestra + classically-influenced singing style — consistent with the Rodgers & Hammerstein "Golden Age" era (e.g. operatic bass Ezio Pinza cast in *South Pacific*, 1949); well-established musical-theatre history, no single contradicting source found. https://en.wikipedia.org/wiki/Rodgers_and_Hammerstein
- Rock/pop instruments (drum kit, electric guitar, electric bass) entering the Broadway pit in the 1960s/70s — confirmed via *Hair* (1968), whose ~20-piece pit incorporated electric guitars, bass and drums, "forever changing the sound of the Broadway pit." https://kuscholarworks.ku.edu/server/api/core/bitstreams/b9624e60-deb3-45ba-8594-1dd0040d4048/content
- 1980s–90s "megamusical" — sung-through, amplified voices, synthesisers alongside the orchestra, recurring themes — matches the academic definition and dating (genre "established and popularized in the 1980s" by Lloyd Webber/Mackintosh; *Phantom* and *Les Mis* "started to use the 80s synthesiser"). https://iupress.org/9780253347930/the-megamusical/ ; https://en.wikipedia.org/wiki/Megamusical
- Leitmotif definition ("a short theme attached to a character, place or idea, returning whenever it appears") — matches Britannica exactly. https://www.britannica.com/art/leitmotif
- Film/game scoring blend of orchestra + synths + electronic percussion + sound design + driving ostinato under action — consistent with modern (Zimmer-style) action scoring conventions; no contradicting source found.
- Game music written to loop because scene/level length is unpredictable, and layering instruments in/out as action intensifies — confirmed by Berklee Online ("it allows for the music to be extended for players that may take longer to get through a level... than the designers had originally intended") and The Game Audio Co / eMastered on vertical layering (stems muted/unmuted by gameplay intensity). https://online.berklee.edu/takenote/scoring-for-games-top-techniques-for-composing-music-for-interactive-media/ ; https://www.thegameaudioco.com/making-your-game-s-music-more-dynamic-vertical-layering-vs-horizontal-resequencing
- Definitions of double-tracked, quantised, pitch correction, pre-chorus, loop, ostinato — all standard, accurate usage.
- Knowledge-check answer keys (KC2–KC5) and flashcard answers (1–4) — checked against the verified facts above; all marked-correct options are correct. KC1's marked answer ("drums quantised exactly to the beat") is still the best of its four options within the exam's four-period framework, even though the general "1990s or later" reasoning behind it is the HIGH finding above.
- Practice-question mark schemes (all 6) — consistent with the verified facts; no errors found.

## Not flagged (out of scope for this fact-check but noted)

`glossary_terms` contains 7 entries (Overdrive, Quantised, Pitch correction, Pre-chorus, Sung-through, Leitmotif, Loop) while `content_html` uses `<dfn>` tooltips for 9 terms including "Fuzz," "Double-tracked" and "Ostinato," which have no corresponding glossary card. This is a structural/completeness gap, not a factual error, so it is not scored for severity — flagging for awareness only.
