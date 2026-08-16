# -*- coding: utf-8 -*-
"""OCR Phase 3: the 13 fresh music-ocr article lessons (OCR_BUILD_PLAN.md).
(Film L1-L3 are copied from music-eduqas by ocr_copy_film_articles.py —
this file builds concerto x4, rhythms-of-the-world x4, film L4, pop x4.)

Same contract as eduqas_build_articles.py with the Eduqas retro applied:
NO sv-listen figures. Every listening example is an <!-- EMBED: key -->
marker plus an "embeds" JSON field mapping key -> full work name; the wire
step (ocr_wire_embeds.py) searches, verifies and replaces the markers.
Drafts (with the embeds map) saved to _ocr_drafts/ before insert.

Run: python ocr_build_articles.py            (resume-safe)
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

MODEL = "claude-sonnet-5"
DRAFTS = os.path.join(HERE, "_ocr_drafts")
os.makedirs(DRAFTS, exist_ok=True)

SPEC = io.open(os.path.join(HERE, "_ocr_aos_spec_extract.md"),
               encoding="utf-8").read()


def spec_slice(marker, nxt):
    i = SPEC.find(marker)
    j = SPEC.find(nxt, i + 10) if nxt else len(SPEC)
    seg = SPEC[i:j][:5500] if i != -1 else ""
    lines = [l for l in seg.splitlines()
             if not re.search(r"(?i)\bOCR\b|©|Version 1\.\d|GCSE \(9–1\)", l)]
    return re.sub(r"(?i)\bOCR\b", "", "\n".join(lines))


AOS2 = spec_slice("Area of Study 2: The Concerto Through Time",
                  "Area of Study 3")
AOS3 = spec_slice("Area of Study 3: Rhythms of the World",
                  "Area of Study 4")
AOS4 = spec_slice("Area of Study 4: Film Music", "Area of Study 5")
AOS5 = spec_slice("Area of Study 5", "5d.  Suggested repertoire")
REP = spec_slice("5d.  Suggested repertoire", None)

SYSTEM = """You write complete GCSE Music revision lessons (age 15-16,
British English) for a revision platform. Return ONE JSON object, nothing
else, with fields:

  "title": string (plain text)
  "description": one sentence, plain text, no HTML, no entities
  "content_html": 5-6 <h2> sections. EVERY <h2> and <p> carries
      data-narration-id="nX" with X sequential from 1. Use 1-3
      <div class="key-fact"><p data-narration-id="nX">...</p></div> boxes.
      HTML entities (&mdash; &lsquo; &rsquo;) belong ONLY in *_html fields.
      Aim 7,500-9,500 characters.
  "embeds": an object mapping short kebab-case keys to the full name of a
      REAL work/performance ("Composer or artist - work title"). For each
      key, place ONE marker line <!-- EMBED: key --> inside content_html
      at the point where a performance video of that work belongs, with
      the surrounding prose telling the student exactly what to listen
      for in it. Use 2-4 embeds per lesson. NEVER use
      <figure class="sv-listen"> boxes — the embed markers replace them.
  "exam_tip_html": one <p> adding mark-scheme value BEYOND the content
      (a worked phrasing, a common mistake) — never a restatement.
  "conclusion_html": one short <p> rounding up + pointing to practice.
  "practice_questions": exactly 6 of {"text","type","marks"} — type like
      "1 mark — Identification" up to "4 marks — Explanation"; marks is the
      marking guidance sentence. Plain text, no entities.
  "knowledge_checks": exactly 5 of {"q","type":"mcq","options":[3-4
      strings],"correct":index}. Plain text.
  "flashcard_questions": exactly 5 of {"q","a"}. Plain text.
  "glossary_terms": 8-12 of {"term","definition"}. Plain text. Every term
      must appear in content_html.

HARD RULES:
- NEVER name any exam board (no AQA, Edexcel, OCR, Eduqas, WJEC) and never
  reference board paper structure ("Section A"). Say "your listening exam".
- No spec codes or component codes. No song lyrics, ever — describe, never
  quote lyrics.
- Musical claims must be standard, checkable musicological facts about
  named real works. Never invent a recording detail.
- The spec extract in the brief is the coverage authority: teach ITS
  bullet content in the lesson's scope. Prefer the suggested-repertoire
  works when choosing examples."""

LESSONS = [
    ("aos2-the-concerto-through-time", 1, AOS2 + REP + """
LESSON 1 of 4 in 'The Concerto Through Time'. Scope: what a concerto is,
then the Baroque era 1650-1750 — the concerto grosso (concertino vs
ripieno, Corelli Op. 6) and the Baroque solo concerto (Vivaldi's Four
Seasons, Bach's Brandenburg No. 4), ritornello form, the continuo
(harpsichord + cello), terraced dynamics, small string orchestra, court
and church patronage. Embed Vivaldi (Spring or Winter) and one grosso."""),
    ("aos2-the-concerto-through-time", 2, AOS2 + REP + """
LESSON 2 of 4. Scope: the Classical concerto 1750-1820 — three-movement
plan (fast-slow-fast), the cadenza, balanced phrasing and cadences, the
orchestra's growth (added winds and horns), soloist-orchestra dialogue.
Works: Mozart's Flute Concerto in D, Haydn's Trumpet Concerto in E flat
(written for the new keyed trumpet), Beethoven's Piano Concerto No. 1 and
the fortepiano-to-piano development. Public concerts replace court
patronage. Embed Haydn Trumpet Concerto and one Mozart movement."""),
    ("aos2-the-concerto-through-time", 3, AOS2 + REP + """
LESSON 3 of 4. Scope: the Romantic concerto 1820-1910 — the virtuoso
celebrity soloist, bigger orchestras and concert halls, longer and more
technically demanding works, lyrical themes, chromatic harmony, wider
dynamics. Works: Brahms's Violin Concerto in D, Rachmaninov's Piano
Concerto No. 2 in C minor. The commissioner becomes the paying public.
Embed one movement of each."""),
    ("aos2-the-concerto-through-time", 4, AOS2 + REP + """
LESSON 4 of 4. Scope: answering concerto questions — hearing the period
of an unfamiliar extract step by step (forces and orchestra size, continuo
or not, dynamics terraced or graded, harmony diatonic or chromatic,
soloist writing plain or virtuosic), then naming elements with evidence:
instruments/timbre, melody, rhythm/metre, texture, structure and
cadences, harmony/tonality, ornamentation. Embed one Baroque and one
Romantic movement for A/B period comparison."""),
    ("aos3-rhythms-of-the-world", 1, AOS3 + REP + """
LESSON 1 of 4 in 'Rhythms of the World'. Scope: India and Punjab — Indian
Classical music (raga as melodic framework, tala as rhythmic cycle, sitar,
tabla, tanpura drone, improvisation, microtonal ornamentation) and
Punjabi bhangra (dhol drum with dagga and tilli sticks, the chaal
rhythm's swung quaver feel, harvest-festival origins, modern produced
bhangra). Embed one classical sitar-and-tabla performance and one bhangra
track."""),
    ("aos3-rhythms-of-the-world", 2, AOS3 + REP + """
LESSON 2 of 4. Scope: the Eastern Mediterranean and Middle East — Greek
folk music (bouzouki, syrtos and other dances, irregular metres like 7/8
kalamatianos), Palestinian and Israeli folk traditions (dabke line dance,
hora), Arabic maqam as a melodic system, ornamented vocal lines, oud,
darbuka goblet drum, riq. How irregular metres and additive rhythms
work. Embed one Greek and one Middle Eastern performance."""),
    ("aos3-rhythms-of-the-world", 3, AOS3 + REP + """
LESSON 3 of 4. Scope: traditional African drumming — the djembe and dunun
family, the talking drum's pitch bending, the master drummer's role and
signals, polyrhythm and cross-rhythm, repetition and ostinato, call and
response, oral tradition (music learned by ear), how texture builds as
parts are added, drumming as social and ceremonial music. Embed one
West African drum ensemble performance."""),
    ("aos3-rhythms-of-the-world", 4, AOS3 + REP + """
LESSON 4 of 4. Scope: Central and South America — samba (Rio carnival,
the bateria: surdo, caixa, agogo, tamborim; syncopation over a driving
two-beat feel; call-and-response with the leader's whistle) and calypso
(Trinidad, steel pans and their oil-drum origin, verse-chorus songs with
topical words - described never quoted, soca as its faster offshoot).
Embed one samba bateria and one steel pan performance."""),
    ("aos4-film-music", 4, AOS4 + REP + """
LESSON 4 of 4 in 'Film Music' (lessons 1-3 covered the composer's
toolkit, mood and place, and exam method). Scope: the two remaining
strands — existing Western Classical music used WITHIN films (why
directors borrow: instant period, scale or irony; famous cases such as
Wagner's Ride of the Valkyries in Apocalypse Now and Strauss's Also
sprach Zarathustra in 2001: A Space Odyssey) and music composed for
VIDEO GAMES: loops and layers, adaptive/dynamic scoring that responds to
play, leitmotif in games, technology from chip sound to live orchestra,
composers such as Koji Kondo (Super Mario Bros., Zelda), Martin
O'Donnell (Halo), Jesper Kyd (Assassin's Creed). Embed the Halo theme
and one borrowed-classic film cue."""),
    ("aos5-conventions-of-pop", 1, AOS5 + REP + """
LESSON 1 of 4 in 'Conventions of Pop'. Scope: Rock 'n' Roll of the 1950s
and 1960s — 12-bar blues foundations, backbeat drumming, walking and
riff bass (double bass slap to electric bass), line-ups (guitars, piano,
sax), energetic vocals, short verse-chorus forms. Works: Elvis Presley's
Hound Dog, The Beatles' I Saw Her Standing There, The Beach Boys' Surfin'
USA (vocal harmony). Social context: youth culture, radio and records.
Embed two of the named works."""),
    ("aos5-conventions-of-pop", 2, AOS5 + REP + """
LESSON 2 of 4. Scope: Rock Anthems of the 1970s and 1980s — power chords,
distorted guitar timbre, anthemic singalong choruses, stadium rock,
guitar solos and virtuosity, drum sounds of the era. Works: Queen's We
Will Rock You (stamp-clap ostinato, a cappella verses into the guitar
outro), Bon Jovi's Livin' On A Prayer (talk-box, key lift), Guns N'
Roses' Sweet Child O' Mine (the opening guitar riff). Embed two."""),
    ("aos5-conventions-of-pop", 3, AOS5 + REP + """
LESSON 3 of 4. Scope: Pop Ballads of the 1970s, 1980s and 1990s — slow
tempo, expressive lead vocal, piano or guitar-led backing that builds
(strings, backing vocals), slow harmonic rhythm, the emotional key
change, verse-chorus with a middle 8. Works: Elton John's Candle in the
Wind, Bette Midler's Wind Beneath My Wings, Bob Dylan's Make You Feel My
Love (also recorded by Billy Joel and later Adele — same song, different
production). Embed two."""),
    ("aos5-conventions-of-pop", 4, AOS5 + REP + """
LESSON 4 of 4. Scope: Solo Artists from 1990 to now — the producer's role,
studio technology (programmed beats, sampling, pitch correction,
layering), image and the industry, streaming's effect on song structure
(shorter intros, earlier hooks). Works: Michael Jackson's Black or White,
Kylie Minogue's Can't Get You Out of My Head (synth-pop hook and
production), Adele's Someone Like You (a modern ballad — voice and piano
only, proving the older conventions still work). Close with how pop
questions ask about ANY strand: name the convention, place the decade,
give evidence. Embed two."""),
]

BANNED = re.compile(r"(?i)\bAQA\b|\bEdexcel\b|\bOCR\b|\bEduqas\b|\bWJEC\b"
                    r"|Section A of (the|your) (exam|paper|listening)")
ENTITY = re.compile(r"&[a-z]+;|<[^>]+>")


def validate(d, brief):
    errs = []
    for f in ("title", "description", "content_html", "exam_tip_html",
              "conclusion_html"):
        if not (d.get(f) or "").strip():
            errs.append("missing " + f)
    ch = d.get("content_html", "")
    if BANNED.search(ch + d.get("exam_tip_html", "") + d.get("conclusion_html", "")):
        errs.append("board name / Section A in html")
    ids = re.findall(r'data-narration-id="n(\d+)"', ch)
    if not ids or [int(x) for x in ids] != list(range(1, len(ids) + 1)):
        errs.append("narration ids not sequential (%d found)" % len(ids))
    if not 6000 < len(ch) < 14000:
        errs.append("content length %d" % len(ch))
    if "sv-listen" in ch:
        errs.append("sv-listen box used — embeds only")
    emb = d.get("embeds") or {}
    markers = re.findall(r"<!-- EMBED: ([\w-]+) -->", ch)
    if not 1 <= len(markers) <= 5:
        errs.append("%d embed markers" % len(markers))
    if sorted(set(markers)) != sorted(emb.keys()):
        errs.append("embeds field/markers mismatch (%s vs %s)"
                    % (sorted(set(markers)), sorted(emb.keys())))
    pq = d.get("practice_questions") or []
    kc = d.get("knowledge_checks") or []
    fc = d.get("flashcard_questions") or []
    gl = d.get("glossary_terms") or []
    if len(pq) != 6:
        errs.append("PQ %d" % len(pq))
    if len(kc) != 5:
        errs.append("KC %d" % len(kc))
    if len(fc) != 5:
        errs.append("FC %d" % len(fc))
    if not 8 <= len(gl) <= 12:
        errs.append("glossary %d" % len(gl))
    for k in kc:
        if k.get("type") != "mcq" or not isinstance(k.get("correct"), int) \
           or not 3 <= len(k.get("options", [])) <= 4 \
           or not 0 <= k["correct"] < len(k["options"]):
            errs.append("bad KC shape")
            break
    plain = json.dumps([pq, kc, fc, gl, d.get("description")])
    if ENTITY.search(plain):
        errs.append("HTML/entities in plain-text fields")
    if BANNED.search(plain):
        errs.append("board name in plain-text fields")
    return errs


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    sub = sb.table("subjects").select("id").eq("slug", "music-ocr").execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == sub}
    cost_in = cost_out = built = 0
    for uslug, num, brief in LESSONS:
        uid = units[uslug]
        existing = sb.table("lessons").select("id").eq("unit_id", uid) \
            .eq("lesson_number", num).execute().data
        if existing:
            print("%s L%d: exists — skipped" % (uslug, num))
            continue
        d = None
        for attempt in range(2):
            r = cl.messages.create(model=MODEL, max_tokens=12000, system=SYSTEM,
                                   messages=[{"role": "user", "content": brief}])
            cost_in += r.usage.input_tokens
            cost_out += r.usage.output_tokens
            text = re.sub(r"```(?:json)?", "",
                          "".join(getattr(b, "text", "") or "" for b in r.content))
            m = re.search(r"\{[\s\S]*\}", text)
            if not m:
                print("%s L%d: no JSON (attempt %d)" % (uslug, num, attempt + 1))
                continue
            try:
                cand = json.loads(m.group(0))
            except ValueError as e:
                print("%s L%d: parse failed (attempt %d): %s" % (uslug, num, attempt + 1, e))
                continue
            errs = validate(cand, brief)
            if errs:
                print("%s L%d: REJECTED (attempt %d): %s" % (uslug, num, attempt + 1,
                                                             "; ".join(errs)))
                continue
            d = cand
            break
        if d is None:
            print("%s L%d: FAILED both attempts — continuing" % (uslug, num))
            continue
        io.open(os.path.join(DRAFTS, "%s_L%d.json" % (uslug, num)), "w",
                encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
        sb.table("lessons").insert({
            "unit_id": uid, "lesson_number": num, "slug": "lesson-%02d" % num,
            "title": d["title"], "description": d["description"],
            "content_html": d["content_html"],
            "exam_tip_html": d["exam_tip_html"],
            "conclusion_html": d["conclusion_html"],
            "practice_questions": d["practice_questions"],
            "knowledge_checks": d["knowledge_checks"],
            "flashcard_questions": d["flashcard_questions"],
            "glossary_terms": d["glossary_terms"],
            "status": "pending_review",
        }).execute()
        built += 1
        print("%s L%d: BUILT + inserted — %s" % (uslug, num, d["title"][:55]))
    print("\nbuilt %d | tokens %d in / %d out | ~$%.2f"
          % (built, cost_in, cost_out, cost_in / 1e6 * 2 + cost_out / 1e6 * 10))


if __name__ == "__main__":
    main()
