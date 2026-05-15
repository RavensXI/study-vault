# Edexcel Religious Studies — Related Media Curation Prompt

You are curating `related_media` for a batch of GCSE Religious Studies lessons (Edexcel 1RA0). Quality bar is high: students should be able to **click any link and immediately reach the content**. The exception is Movies/TV/Documentaries — those use JustWatch aggregator pages.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_religious-studies-edexcel/lessons/{lesson_slug}.json` for the lessons assigned to you. You will write back to each.

## Output schema

For each lesson in your batch, ADD a `related_media` field to its lesson JSON:

```json
"related_media": [
  {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
      {
        "title": "Episode title",
        "description": "1-line context: who's hosting, what they cover, why it suits the lesson",
        "url": "https://open.spotify.com/episode/... OR https://podcasts.apple.com/... OR https://youtu.be/..."
      }
    ]
  },
  {
    "category": "Videos & Channels",
    "emoji": "📺",
    "items": [
      { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ]
  },
  {
    "category": "Documentaries",
    "emoji": "🎬",
    "items": [
      { "title": "Title (Year)", "description": "...", "url": "https://www.justwatch.com/uk/movie/SLUG" }
    ]
  },
  {
    "category": "Study Tools",
    "emoji": "🛠️",
    "items": [
      { "title": "...", "description": "...", "url": "https://..." }
    ]
  }
]
```

## Hard rules

- **Each lesson: ≥6 items total**, spanning all four categories (≥1 each).
- **Every URL must be clickable** and go directly to the content — not a search page or homepage.
- **YouTube URLs**: `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. Verify each with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  Drop if oembed returns non-200 or an error. **DO NOT use HEAD requests.**
- **Podcasts**: direct link to the EPISODE (not the show homepage).
  - Good RS sources: Undeceptions (John Dickson, RZIM/CPX Australia), The Liturgists (Michael Gungor + Mike McHargue), Speak Life (Krish Kandiah), Thinking Allowed (David Wilkins, BBC R4, sociology of religion), RE:Thinking (NATRE teachers), Nomad Podcast (progressive Christianity), On Being (Krista Tippett — wide interfaith), From Our Own Correspondent (BBC R4 — world religion context), BBC The Documentary (faith and society episodes), The Islamic History Podcast (Jacob Riyad), Short and Curly (ABC Kids — ethics, suitable for younger RS students), Thinking Faith (Jesuit podcast), Interfaith Voices (NPR), Breadth of Life (Jewish podcast), The Rabbi's Podcast (Dov Laimon), The Long View (BBC World Service — history of ideas).
- **Documentaries / Films**: JustWatch UK URLs (`https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`).
  - Good RS titles by topic:
    - **Christianity/Catholic**: The Two Popes (2019), Silence (2016, Scorsese), Of Gods and Men (2010), The Mission (1986), Calvary (2014), Romero (1989), Priest (1994), Mass (2021), Benedetta (2021), Vision — From the Life of Hildegard von Bingen (2009), The Young Pope / The New Pope (HBO), Rev. (BBC), Fleabag S2 (BBC — explores priesthood and faith)
    - **Islam**: The Message (1976), Omar (2012 series), Muhammad: The Last Prophet (2002), Four Lions (2010, black comedy on radicalisation), Al-Farabi (documentary), The Muslims Are Coming! (2013), Inside Mecca (National Geographic)
    - **Judaism**: Schindler's List (1993), The Boy in the Striped Pyjamas (2008), Fiddler on the Roof (1971), Unorthodox (Netflix 2020), Shtisel (Netflix), The Two of Us (2004), A Serious Man (2009 Coen Brothers)
    - **Buddhism**: Spring Summer Fall Winter and Spring (2003), Samsara (2011), The Cup (1999), Kundun (1997), Why Has Bodhi-Dharma Left for the East? (1989), The Dhamma Brothers (2007 documentary)
    - **Hinduism**: Gandhi (1982), Bride and Prejudice (2004), Dil Se (1998), Water (2005), Lagaan (2001), Oh My God (2012), PK (2014)
    - **Sikhism**: Bend It Like Beckham (2002 — Sikh family), Viceroy's House (2017), The Black Prince (2017), The Warrior (2001)
    - **Philosophy of Religion / Ethics**: Contact (1997), Signs (2002), The Tree of Life (2011), Doubt (2008), Dogma (1999), Ordet (1955), Calvary (2014), The Exorcism of Emily Rose (2005)
    - **General**: God on Trial (BBC 2008, philosophy of God), The Imam and the Pastor (documentary), The Story of God (NatGeo, Morgan Freeman), Sacred Journeys (BBC, pilgrimage)
- **Study Tools**: BBC Bitesize RS, NATRE (natreuk.org), RE Today (retoday.org.uk), Philosophy Now (philosophynow.org), The Philosophy Foundation (philosophy-foundation.org), Stanford Encyclopedia of Philosophy (plato.stanford.edu) for technical philosophy terms, Exploring Christianity (exploringchristianity.org), Muslim Hands (for Islamic charity content), Al-Islam.org (Shi'a texts), Sikh Net (sikhnet.com), Hinduism Today (hinduismtoday.com), My Jewish Learning (myjewishlearning.com), BBC In Our Time (philosophy episodes, melvyn bragg), RSRevision.com, BBC Religions (bbc.co.uk/religion/religions/), Trussell Trust / CAFOD / Christian Aid / Tearfund websites for charity content.
- **No Wikipedia in primary slots** — fine as one occasional study tool entry.
- **No Save My Exams, PMT, MME, or revision aggregators** — banned per pipeline doctrine.
- **No reference to past papers or mark schemes.**
- **Tonal match**: items must connect to THIS LESSON's topic, not just the subject generally.
- **UK-relevance preferred**: British students. UK-produced media first where equally strong.

## Verification step (mandatory)

For each YouTube URL, run the oembed check before including. Drop and replace if it fails. For non-YouTube URLs, sanity-check that the URL path looks like a direct content page (not a homepage or search URL).

## How to write back

For each lesson:

1. Read `scripts/_content_religious-studies-edexcel/lessons/{lesson_slug}.json`
2. Add the `related_media` field (preserve all other fields)
3. **If there is already a "Podcasts" category with a StudyVault lesson podcast item** — keep it first, add curated items alongside it
4. Write the JSON back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo the curated content. Just write and confirm.
