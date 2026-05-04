# Eduqas Film Studies — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Film Studies lessons (Eduqas C670QS / WJEC 3670QS). Quality bar high — every URL clicks straight to the content.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full rules
2. The lesson JSONs at `scripts/_content_film-studies-eduqas/lessons/{lesson_slug}.json` for the lessons you're assigned. Write back to each.

## Output schema

```json
"related_media": [
  { "category": "Podcasts", "emoji": "🎙️", "items": [...] },
  { "category": "Videos & Channels", "emoji": "📺", "items": [...] },
  { "category": "Documentaries", "emoji": "🎬", "items": [...] },
  { "category": "Study Tools", "emoji": "🛠️", "items": [...] }
]
```

**EXACT category names** (validator hard-checks):
- `Podcasts`
- `Videos & Channels`
- `Documentaries`
- `Study Tools`

## Hard rules

- **≥6 items per lesson, all 4 categories represented**.
- **Direct links** — not search results, not homepages.
- **YouTube URLs verified via `curl` oembed** before inclusion. **DO NOT use browser MCP tools** — `curl` only via the Bash tool.
- **Podcasts** — link to a SPECIFIC episode.
- **Film-relevant podcast sources**:
  - BBC Radio 4 Front Row (film-related episodes)
  - The Big Picture (The Ringer)
  - Kermode and Mayo's Take (formerly Wittertainment)
  - Truth and Movies (Little White Lies)
  - The Director's Cut (DGA podcast)
  - The Q&A (Jeff Goldsmith)
  - The Treatment (KCRW film podcast)
  - Filmmaker Magazine podcast
  - Film Comment Podcast
  - 99% Invisible — design and aesthetic episodes
  - Cinephile (Empire Magazine)
  - You Must Remember This (Karina Longworth — film history)
  - Script Apart
- **Movies / TV / Documentaries** (JustWatch UK):
  - For film analysis: documentaries about specific films (e.g. "Singin' in the Rain: Behind the Scenes")
  - Director documentaries (Spielberg, Kubrick, Hitchcock, Scorsese, Coen Bros etc.)
  - Film history docs: Story of Film: An Odyssey (Mark Cousins), De Palma, Five Came Back
  - For specific set films, the FILM ITSELF on JustWatch is appropriate
  - Hitchcock/Truffaut (2015), Side by Side (2012, on digital vs film), Lost in La Mancha
- **Free YouTube channels for Film Studies**:
  - **Every Frame a Painting** — film analysis (legendary; archived but episodes still up)
  - **Lessons from the Screenplay** — narrative analysis
  - **Now You See It** — film theory and analysis
  - **The Cinema Cartography** — director-focused
  - **The Discarded Image** — production design analysis
  - **CinemaTyler** — cinematography breakdowns
  - **Channel Criswell** — director studies
  - **Patrick Willems** — accessible film theory
  - **The Take** — character/theme analysis (Glamour-owned but often genuinely good)
  - **Kaptain Kristian** — auteur studies
  - **Wisecrack** — philosophical readings of films
  - **Rossatron** — action/cinematography
  - **Tony Zhou** — Every Frame a Painting back catalog
  - **NerdWriter1** — broad film analysis
- **Study Tools**:
  - BBC Bitesize Film Studies (per-topic where applicable)
  - BFI Education resources (BFI Player, BFI online resources)
  - BFI Player (some content free)
  - Eduqas/WJEC subject pages (factual reference)
  - Senses of Cinema journal (free open-access film theory)
  - Film at Lincoln Center (free articles)
  - The Criterion Collection's free essay archive
  - MoMA online film essays (where free)
  - Film Form and Style (Academia.edu free papers — be selective)
- **No Wikipedia in primary slots** (≤1 per lesson, study-tool only).
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned.
- **No reproduction** of past papers, mark schemes, or model answers.
- **Tonal match**: items must connect to the LESSON's specific topic. A film-form lesson on cinematography gets cinematography-analysis content; a set-film lesson gets that-film-specific content.
- **UK-relevance preferred** where possible. For UK set films, lean heavily into UK sources.
- **Dual-board universality**: lessons serve BOTH Eduqas (English) and WJEC (Welsh) students. No England-only or Wales-only sources.

## Verification

For every YouTube URL: `curl` oembed before inclusion. Drop and replace if it errors. For other URLs: sanity-check by reading them; replace homepage/search-result URLs with deeper links.

## How to write back

For each lesson:
1. Read `scripts/_content_film-studies-eduqas/lessons/{lesson_slug}.json`
2. Add `related_media` field (preserve all other fields)
3. **Preserve any existing `related_media`** if a "Lesson Podcast" item is already there
4. Write back

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo content. Just write + confirm.
