# History (Eduqas) — Related Media Curation Prompt

You are curating `related_media` for a SMALL batch of GCSE History lessons. Quality bar is high: a student must be able to **click any link and land directly on the content** — the specific video, the specific documentary's page, the specific topic page. Never a channel homepage, never a search-results page, never a site root.

## Files to read
1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (skim).
2. Your assigned lesson JSONs (listed in your task) at `scripts/_content_history-eduqas/lessons/{file}.json`. Each has `title`, `description`, `content_html`, `section_markers` context — use them to pick on-topic media.

## Output schema — ADD a `related_media` field to each lesson JSON
Use these EXACT category names (the verifier requires them):

```json
"related_media": [
  { "category": "Videos & Channels", "emoji": "📺", "items": [
      { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID" } ] },
  { "category": "Documentaries", "emoji": "🎬", "items": [
      { "title": "Title (Year)", "description": "...", "url": "https://www.justwatch.com/uk/movie/SLUG" } ] },
  { "category": "Study Tools", "emoji": "🧰", "items": [
      { "title": "...", "description": "...", "url": "https://..." } ] },
  { "category": "Articles & Web", "emoji": "📰", "items": [
      { "title": "...", "description": "...", "url": "https://..." } ] }
]
```

Do NOT add a Podcasts category — the NotebookLM generator inserts it later.

## Hard rules (count + categories)
- **Each lesson: ≥6 items total**, spread across categories.
- **MUST include ≥1 in `Videos & Channels`, ≥1 in `Documentaries`, ≥1 in `Study Tools`.** `Articles & Web` is encouraged (helps reach 6).
- One fact/resource per item. Keep descriptions to one plain sentence, GCSE-appropriate, no HTML entities (use unicode).

## URL rules — DEEP LINKS ONLY (this is the #1 requirement)
Every URL must open the actual content, not a hub:

- **YouTube** — use `https://www.youtube.com/watch?v=VIDEO_ID` for a SPECIFIC, ON-TOPIC video. **You MUST verify every YouTube video via oembed BEFORE including it:**
  ```
  curl -s -o /dev/null -w "%{http_code}" "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  200 = alive; anything else (404/401/403) = dead/private/region-locked → DROP it. NEVER use HEAD requests (YouTube returns 200 for dead videos). **Agents hallucinate YouTube IDs ~20% of the time — assume every ID you produce is suspect until oembed returns 200.** If you cannot verify a specific video, do NOT guess an ID. Instead use one of the approved CHANNEL handle URLs below (these are real and stable) for that slot, or move the slot to Study Tools/Articles with a verified deep link.
- **Documentaries** — `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}` for a SPECIFIC title (deep link to that title's page). Do NOT link to Netflix/Amazon directly, and do NOT link to a JustWatch search page. If you cannot confirm a specific JustWatch slug, use a BBC programme page (`https://www.bbc.co.uk/programmes/{pid}`) for a real series, or skip Documentaries and ensure the count is met elsewhere (but you still need ≥1 Documentaries item — prefer a well-known BBC/IWM series page).
- **Study Tools / Articles** — deep-link to the SPECIFIC topic page, not the site root. Good: a Bitesize topic guide, a National Archives source-based lesson, a Britannica article on the exact event, an IWM/museum page on the exact topic, a History Extra article. Bad: `bbc.co.uk/bitesize` root, a search URL, a homepage.
- After building each lesson's list, re-read every URL and ask: "does this open the content itself?" If it's a homepage or search, replace it.

## Approved, real YouTube channel handles (stable — safe to use as a channel link if you can't verify a specific video)
- `https://www.youtube.com/@Simplehistory` (Simple History — warfare, world wars, social history)
- `https://www.youtube.com/@EpicHistoryTV` (Epic History TV — long-form narrative history)
- `https://www.youtube.com/@OverSimplified` (OverSimplified — engaging overviews; verify facts)
- `https://www.youtube.com/@TheHistoryMatters` (History Matters — short Q&A explainers)
- `https://www.youtube.com/@crashcourse` (Crash Course — World/European/US History)
- `https://www.youtube.com/@TED-Ed` (TED-Ed — animated history explainers)
- `https://www.youtube.com/@KingsandGenerals` (Kings and Generals — medieval/military)
- `https://www.youtube.com/@MarkFeltonProductions` (Mark Felton — WW2 / Cold War)
- `https://www.youtube.com/@I_W_M` (Imperial War Museums)
- `https://www.youtube.com/@BBCTeach` (BBC Teach — curriculum class clips)

## Approved Study Tools / Articles sources (deep-link to the specific page)
- BBC Bitesize topic guides (`bbc.co.uk/bitesize/guides/...` or `/topics/...`)
- The National Archives education / source pages (`nationalarchives.gov.uk/education/...`)
- Imperial War Museums histories (`iwm.org.uk/history/...`)
- Britannica articles on the exact event/person (`britannica.com/...`)
- History Extra (`historyextra.com/...`)
- Spartacus Educational topic pages (`spartacus-educational.com/...`)
- Royal Museums Greenwich, National Museum of the Royal Navy, USHMM (`encyclopedia.ushmm.org/...`), gov.uk where relevant
- Wikipedia: MAX 1 per lesson, never the primary item

## Era cheat-sheet (match channels/docs to your unit)
- **Medieval (Hundred Years War, Crusades, Black Death, Peasants' Revolt)** → Simple History, Epic History TV, Kings and Generals; IWM/Britannica; docs on the Crusades / medieval England.
- **Early modern (Elizabethan, Voyages/Conquest of the Americas)** → Epic History TV, History Matters; Britannica; Elizabeth I / Spanish Armada / conquistador documentaries.
- **Modern Britain (1890-1918, 1951-79, UK 1919-90)** → BBC Teach, Simple History; National Archives; BBC social-history documentaries.
- **Germany 1919-39 / 1919-91, USSR 1924-91** → Mark Felton, Epic History TV, USHMM (encyclopedia.ushmm.org); Weimar/Nazi/Cold War/Berlin Wall documentaries.
- **USA 1910-29 / 1929-2000** → Crash Course US History, Mark Felton (Cold War); Library of Congress; Prohibition / Wall Street Crash / Civil Rights / Cold War documentaries.
- **Thematic (Crime & Punishment, Health & Medicine, Warfare, Entertainment c.500-present)** → BBC Teach, Simple History; National Archives, Science Museum / Wellcome (medicine), National Museum of the Royal Navy (warfare); period-spanning BBC documentaries.

## Hard prohibitions
- **No spec codes** (C100QS, C100UA-H) in titles/descriptions.
- **No board names** ("Eduqas", "WJEC", "Pearson") in user-facing strings.
- **No Save My Exams, Physics & Maths Tutor (PMT), MME, Primrose Kitten, Study Mind.**
- No Wikipedia in a primary slot (max 1 per lesson).
- No homepages or search-result URLs anywhere.

## How to write back
For each lesson in your batch: read the JSON, ADD the `related_media` field (preserve every other field), write back to the same path. Do NOT touch any other field. Do NOT call Supabase.

## Output
Return only:
```
RM_DONE: lessons=<N> verified_youtube=<count> files=<comma list of filenames>
```
Do not echo the curated content back.
