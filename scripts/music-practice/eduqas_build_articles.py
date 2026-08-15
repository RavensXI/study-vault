# -*- coding: utf-8 -*-
"""Phase 4: the 13 music-eduqas article lessons (EDUQAS_BUILD_PLAN.md).

One API call per lesson (claude-sonnet-5), validated hard before insert:
counts (6 PQ / 5 KC / 5 FC / 8-12 glossary), KC shape {q,type,options,
correct}, plain-text fields free of HTML/entities, *_html free of board
names and AQA paper structure, narration ids sequential, no lyrics.
Study lessons carry <!-- EMBED: key --> markers; the weave step replaces
them with oEmbed-verified official YouTube figures. Resume-safe: lessons
already present are skipped. Drafts saved to _eduqas_drafts/ before insert.

Run: python eduqas_build_articles.py            (all 13, inserts as it goes)
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
DRAFTS = os.path.join(HERE, "_eduqas_drafts")
os.makedirs(DRAFTS, exist_ok=True)

SPEC = io.open(os.path.join(HERE, "_eduqas_aos_spec_extract.md"),
               encoding="utf-8").read()


def spec_slice(marker, nxt):
    i = SPEC.find(marker)
    j = SPEC.find(nxt, i + 10) if nxt else len(SPEC)
    seg = SPEC[i:j][:5500] if i != -1 else ""
    # strip board names and page furniture from the coverage source — the
    # model echoes whatever the brief contains (three lessons failed on it)
    lines = [l for l in seg.splitlines()
             if not re.search(r"(?i)WJEC|Eduqas|CBAC|©|GCSE MUSIC\s*\d*$", l)]
    return re.sub(r"(?i)\b(WJEC|Eduqas|CBAC)\b", "", "\n".join(lines))


AOS1 = spec_slice("Area of study 1: Musical Forms and Devices", "Area of study 2")
AOS2 = spec_slice("Area of study 2: Music for Ensemble", "Area of study 3")
AOS3 = spec_slice("Area of study 3: Film Music", "Area of study 4")
AOS4 = spec_slice("Area of study 4: Popular Music", None)

SYSTEM = """You write complete GCSE Music revision lessons (age 15-16,
British English) for a revision platform. Return ONE JSON object, nothing
else, with fields:

  "title": string (plain text)
  "description": one sentence, plain text, no HTML, no entities
  "content_html": 5-6 <h2> sections. EVERY <h2> and <p> carries
      data-narration-id="nX" with X sequential from 1. Use 1-3
      <div class="key-fact"><p data-narration-id="nX">...</p></div> boxes.
      Use 2-4 listen prompts:
      <figure class="sv-listen" data-narration-id="nX"><figcaption
      class="sv-listen-label">Listen &mdash; [named REAL work]: what to
      listen for</figcaption></figure>. HTML entities (&mdash; &lsquo;
      &rsquo;) belong ONLY in *_html fields. Aim 7,500-9,500 characters.
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
- If the brief includes EMBED markers, place each <!-- EMBED: key --> on
  its own line inside content_html where the video belongs (it will be
  replaced with an embedded player); write the surrounding prose assuming
  the student can watch it there.
- The spec extract in the brief is the coverage authority: teach ITS
  bullet content in the lesson's scope."""

LESSONS = [
    # unit_slug, n, brief
    ("aos1-forms-and-devices", 1, AOS1 + """
LESSON 1 of 4 in 'Musical Forms and Devices'. Scope: the structures —
binary (AB), ternary (ABA), rondo (ABACA), theme and variations, strophic
form, and minuet and trio. How to HEAR each one (repetition, contrast,
return), with named Western Classical examples 1650-1910. End by pointing
to the listening practice."""),
    ("aos1-forms-and-devices", 2, AOS1 + """
LESSON 2 of 4. Scope: the devices — ostinato, sequence, imitation, canon,
pedal, drone, conjunct/disjunct motion, repetition and contrast — plus
cadences as punctuation (perfect, imperfect, plagal, interrupted). How
each sounds, with named examples."""),
    ("aos1-forms-and-devices", 3, AOS1 + """
LESSON 3 of 4 — study piece part 1: Bach's Badinerie (Orchestral Suite
No. 2 in B minor, BWV 1067 — final movement, flute with strings and
continuo). Context: the Baroque suite, the dance-movement tradition, what
'badinerie' means (playful jesting), the scoring, binary form structure.
Include ONE marker line <!-- EMBED: badinerie --> after the opening
section for an embedded performance. Claims must be standard facts about
the WORK (key, form, scoring, character) — no claims about a specific
recording."""),
    ("aos1-forms-and-devices", 4, AOS1 + """
LESSON 4 of 4 — study piece part 2: Badinerie in close-up. Binary form in
detail (A and B sections, repeats, modulation to the relative/dominant),
the virtuosic flute writing, semiquaver figuration, terraced dynamics,
continuo role, and how forms-and-devices questions ask about this piece.
Include <!-- EMBED: badinerie --> once where re-listening helps."""),
    ("aos2-music-for-ensemble", 1, AOS2 + """
LESSON 1 of 3 in 'Music for Ensemble'. Scope: texture and sonority as THE
lens — monophonic, homophonic, polyphonic/contrapuntal, unison, melody and
accompaniment, layering — and how ensembles balance: who leads, who
supports. Named examples across chamber music."""),
    ("aos2-music-for-ensemble", 2, AOS2 + """
LESSON 2 of 3. Scope: jazz and blues ensembles — rhythm section roles
(drums, bass, piano/guitar), front line, improvisation over changes,
12-bar blues as ensemble practice, swing feel, call and response."""),
    ("aos2-music-for-ensemble", 3, AOS2 + """
LESSON 3 of 3. Scope: musical theatre and chamber ensembles — pit bands,
vocal ensemble writing (duet, trio, chorus), sonority choices that carry
drama; classical chamber groups (string quartet, wind quintet) and how
four or five players create full textures."""),
    ("aos3-film-music", 1, AOS3 + """
LESSON 1 of 3 in 'Film Music'. Scope: the composer's toolkit — leitmotif,
theme, underscore vs source music, hitting the action, and the elements
(instrumentation, dynamics, harmony, rhythm) used to build character and
tension. Named examples from the concert-and-film repertoire."""),
    ("aos3-film-music", 2, AOS3 + """
LESSON 2 of 3. Scope: creating mood, time and place — how scores signal
period and location (instrument choice, scales/modes, texture), building
and releasing tension, the climax and resolution shapes exam extracts
use."""),
    ("aos3-film-music", 3, AOS3 + """
LESSON 3 of 3. Scope: writing about film music in the exam — describing an
unfamiliar cue step by step (opening, build, peak, close), naming
elements with evidence, and composing-to-a-brief thinking (what YOU would
choose for a scene and why)."""),
    ("aos4-popular-music", 1, AOS4 + """
LESSON 1 of 4 in 'Popular Music'. Scope: pop forms and hooks — verse,
chorus, bridge, middle 8, intro/outro, riffs and hooks, 32-bar song form,
strophic writing — plus melody-and-accompaniment textures in pop."""),
    ("aos4-popular-music", 2, AOS4 + """
LESSON 2 of 4. Scope: bhangra and fusion — dhol drum, chaal rhythm,
traditional-meets-produced textures; how fusion combines instruments,
scales and production across traditions. Neutral, factual treatment with
named styles rather than lyric content."""),
    ("aos4-popular-music", 3, AOS4 + """
LESSON 3 of 4 — study piece part 1: Toto's 'Africa' (1982). Context and
construction: personnel roles in a studio band, the kalimba-like synth
intro, layered keyboards, drum groove (the famous half-time shuffle
feel), verse-chorus form with the lifted chorus. Include ONE marker
<!-- EMBED: africa --> after the opening section. NO lyric quotation —
describe what the music does, never what the words say."""),
    ("aos4-popular-music", 4, AOS4 + """
LESSON 4 of 4 — study piece part 2: 'Africa' in close-up for the exam —
texture layers through the arrangement, vocal harmony in the chorus,
synth solo, production techniques (layering, reverb), and how questions
ask about this track. Include <!-- EMBED: africa --> once. NO lyrics."""),
]

# board names always banned; "Section A" only as PAPER structure — in a
# forms lesson "section A" is musical terminology (the A section of AB form)
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
    if "<!-- EMBED:" in brief and "<!-- EMBED:" not in ch:
        errs.append("embed marker missing")
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
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
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
