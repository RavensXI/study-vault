# Computer Science (Edexcel) — Related Media Curation Prompt

You are curating `related_media` for GCSE Computer Science (Edexcel 1CP2) lessons.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md`
2. The lesson JSONs at `scripts/_content_computer-science-edexcel/lessons/{lesson_slug}.json` for assigned lessons

## Output schema

For each lesson, ADD a `related_media` field to the JSON:

```json
"related_media": [
  {"category":"Podcasts","emoji":"🎙️","items":[...]},
  {"category":"Videos & Channels","emoji":"📺","items":[...]},
  {"category":"Documentaries","emoji":"🎬","items":[...]},
  {"category":"Study Tools","emoji":"🛠️","items":[...]}
]
```

## EXACT category names (verifier rejects deviations)

- `Podcasts`
- `Videos & Channels` (with ampersand)
- One of `Documentaries`, `Movies`, `TV Shows` (Documentaries fits CS best)
- `Study Tools`

## Hard rules

- **≥6 items per lesson**, ≥1 per category group
- **Verify EVERY URL** with WebFetch (YouTube oembed; non-YouTube direct fetch). Drop and replace if 404 or homepage-redirect.
- **The `_audit_related_media_urls.py` script will run after you finish — anything dead WILL be caught and dropped.** The script is the source of truth, not your verification claims. So: pick URLs you genuinely believe are alive based on prior knowledge, but don't lie about having verified what you couldn't.
- **No competitor revision sites** (Save My Exams, PMT, MME, Primrose Kitten)
- **Tonal match**: items must connect to the LESSON's specific topic (e.g. "binary search" lesson links to actual binary search videos, not generic CS content)
- **British relevance preferred** where it doesn't compromise quality

## Pre-vetted CS sources (use these where the lesson topic fits)

### Podcasts
- **CodeNewbie Podcast** (Saron Yitbarek) — accessible CS for beginners
- **Software Engineering Daily** — deeper dives
- **Lex Fridman Podcast** — episodes with computer scientists (Turing, Knuth, Hinton)
- **The Changelog** — software development culture
- **BBC Click** (Spreaker) — UK tech weekly
- **The Vergecast** — tech news, CS-adjacent
- **Reply All** — internet/tech stories with strong narrative
- **Darknet Diaries** — cybersecurity true stories (perfect for Unit 5 cyber lessons)
- **Hidden Brain — episodes on algorithms** — algorithmic decision-making
- **Hard Fork** (NYT) — tech ethics + AI

### Videos & Channels
- **Computerphile** (Brady Haran) — *the* GCSE CS YouTube channel; verifiable URLs at `https://www.youtube.com/@Computerphile`
- **Tom Scott Plus** — explanatory CS videos (e.g. "How does HTTPS work?")
- **Khan Academy Computing** — bite-size CS basics
- **3Blue1Brown** — visual algorithm explainers (binary search, sorting)
- **Crash Course Computer Science** (Carrie Anne Philbin — 40-episode series, perfect GCSE-level)
- **Craig'n'Dave** — UK GCSE CS tutoring channel (huge GCSE following; covers Edexcel spec)
- **Mr Benn Computing** — UK GCSE-specific revision (search on YouTube)
- **The Coding Train** (Daniel Shiffman) — visual coding explainers
- **Real Engineering** — episodes on internet infrastructure, cryptography
- **Veritasium** — episodes on encryption, algorithms

### Documentaries (JustWatch UK)
- **The Imitation Game** (2014) — Turing biopic, perfect for computing history
- **Citizenfour** (2014) — Snowden, surveillance state — for cybersecurity lessons
- **Lo and Behold: Reveries of the Connected World** (Herzog 2016) — internet history
- **The Social Dilemma** (2020) — algorithmic ethics, AI
- **Hidden Figures** (2016) — programming history (Katherine Johnson)
- **Coded Bias** (2020) — algorithmic discrimination (perfect for Unit 5 AI/ML lesson)
- **The Internet's Own Boy** (Aaron Swartz documentary, 2014)
- **Halt and Catch Fire** (TV series, 2014–2017) — early PC industry

### Study Tools
- **BBC Bitesize Computer Science** — `https://www.bbc.co.uk/bitesize/subjects/z34k7ty`
- **Isaac Computer Science** (`isaaccomputerscience.org`) — DfE-funded free CS revision platform
- **Craig'n'Dave GCSE CS revision** — `https://student.craignave.org` (Edexcel-specific content available)
- **Code.org** — visual programming intro (Hour of Code, AI for Everyone)
- **Replit** — browser-based Python coding
- **Trinket.io** — embedded Python coding
- **Visualgo** — algorithm/data structure visualisations
- **Computer Science Field Guide** (`csfieldguide.org.nz`)
- **NCSC for Schools** (`ncsc.gov.uk/cyberfirst`) — UK National Cyber Security Centre student resources
- **GitHub Education** — student platform

## Verification step (mandatory)

For each YouTube URL, WebFetch the oembed endpoint. For non-YouTube URLs, WebFetch the URL itself. Drop if 404 or homepage redirect. **Don't claim verification you didn't perform — the audit script will catch lies.**

## How to write back

For each lesson:
1. Read the JSON
2. Add `related_media` field (preserve other fields)
3. Write back with `indent=2, ensure_ascii=False`

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```
