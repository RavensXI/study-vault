# -*- coding: utf-8 -*-
"""Edexcel Phase 3: the 20 music-edexcel article lessons — 4 AoS context
lessons + 2 study lessons for each of the 8 set works.

Reuses the OCR builder's SYSTEM prompt and validator verbatim (EMBED
markers + embeds map, no listen boxes). Study briefs carry the standard
documented analysis scaffolds for each set work; the fact-check agents
gate every claim before narration as usual. NO LYRICS ever — Killer
Queen, Defying Gravity, Release and Samba Em Preludio are described,
never quoted.

Run: python edexcel_build_articles.py     (resume-safe, inserts as it goes)
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from ocr_build_articles import SYSTEM, validate

MODEL = "claude-sonnet-5"
DRAFTS = os.path.join(HERE, "_edexcel_drafts")
os.makedirs(DRAFTS, exist_ok=True)
SPEC = io.open(os.path.join(HERE, "_edexcel_spec_extract.md"),
               encoding="utf-8").read()[:6000]
SPEC = re.sub(r"(?i)\b(Edexcel|Pearson)\b", "", SPEC)

LESSONS = [
    ("aos1-instrumental-music", 1, SPEC + """
LESSON 1 of 5 in 'Instrumental Music 1700-1820'. Scope: the era's two
worlds — the late Baroque (the concerto grosso, ritornello, continuo,
terraced dynamics, patronage) and the Classical-into-early-Romantic
piano sonata (sonata form, balanced phrasing, the fortepiano's growth).
Introduce BOTH set works briefly: Bach's Brandenburg Concerto No. 5
third movement and Beethoven's 'Pathetique' Sonata first movement —
what each is, why each represents its world. Embed one performance of
each. End by pointing to the two-lesson studies that follow."""),
    ("aos1-instrumental-music", 2, SPEC + """
LESSON 2 of 5 — set work study part 1: Bach, Brandenburg Concerto No. 5
in D major, third movement (1721). Context and construction: the six
Brandenburg concertos as an unsolicited dedication to the Margrave;
concerto grosso with a concertino of flute, violin and harpsichord; the
harpsichord's unusually prominent, virtuosic role (revolutionary for
its time); the gigue-like character of the finale; ritornello and
fugal opening; D major. Embed ONE performance. Claims must be standard
documented facts about the WORK, not any recording."""),
    ("aos1-instrumental-music", 3, SPEC + """
LESSON 3 of 5 — set work study part 2: Brandenburg 5/iii in close-up
for the exam. Structure (the A-B-A da capo shape with its fugal A
section and the contrasting middle), texture (imitative/contrapuntal
writing, concertino vs ripieno dialogue, continuo), metre and rhythm
(lilting compound-style gigue feel, driving quavers/semiquavers),
melody (conjunct sequences, ornamentation), harmony/tonality (D major,
modulation to related keys), and HOW exam questions ask about this
movement. Embed the performance once where re-listening helps."""),
    ("aos1-instrumental-music", 4, SPEC + """
LESSON 4 of 5 — set work study part 1: Beethoven, Piano Sonata No. 8
in C minor 'Pathetique', first movement (published 1799). Context and
construction: Beethoven in Vienna, the sonata as public-facing drama;
the unprecedented Grave slow introduction and its returns; sonata form
(exposition with C minor first subject rocketing upward, E flat
minor-to-major second subject area, development, recapitulation, coda);
the piano writing (tremolo left hand, sudden dynamic contrasts, full
chords, chromaticism). Embed ONE performance."""),
    ("aos1-instrumental-music", 5, SPEC + """
LESSON 5 of 5 — set work study part 2: 'Pathetique' first movement in
close-up for the exam. The Grave-Allegro relationship (where the Grave
returns and why that was radical), sonata-form landmarks to HEAR
(first subject character, bridging, second subject, development
fragmentation, recapitulation arrival, coda), texture (melody over
tremolo, octaves, homophony), dynamics as drama (fp, sudden contrasts),
harmony (diminished sevenths, chromaticism, C minor gravity), and how
exam questions target this movement. Embed the performance once."""),
    ("aos2-vocal-music", 1, SPEC + """
LESSON 1 of 5 in 'Vocal Music'. Scope: two vocal worlds three centuries
apart — Baroque theatre song (Purcell's London, continuo song, ground
bass, word painting) and 1970s studio rock (multitrack layering, the
voice as production instrument). Introduce BOTH set works briefly:
Purcell's Music for a While and Queen's Killer Queen. Embed one
performance of each. NO lyric quotation anywhere — describe what the
music does with the words, never quote them."""),
    ("aos2-vocal-music", 2, SPEC + """
LESSON 2 of 5 — set work study part 1: Purcell, Music for a While
(1692, from the incidental music to Oedipus). Context and construction:
Restoration theatre music; the ground bass foundation (a short
repeating bass line, and what stays fixed versus what floats above);
voice and continuo texture; word painting as the engine of the song
(describe the falling/repeated-note effects WITHOUT quoting lyrics);
ornamentation. Embed ONE performance."""),
    ("aos2-vocal-music", 3, SPEC + """
LESSON 3 of 5 — set work study part 2: Music for a While in close-up
for the exam. The ground bass in detail (how many statements, how
Purcell blurs the joins by phrase overlap), melody (conjunct with
expressive leaps, ornaments), harmony above the ground (suspensions,
dissonance resolving), the A-B-A' return shape, performing forces
(voice, harpsichord/continuo realisation, bass viol), and how exam
questions ask about it. NO lyric quotation. Embed once."""),
    ("aos2-vocal-music", 4, SPEC + """
LESSON 4 of 5 — set work study part 1: Queen, Killer Queen (1974, from
Sheer Heart Attack). Context and construction: Queen's studio ambition
pre-Bohemian Rhapsody; piano-led verse-chorus with varied strophes;
the layered, multitracked backing vocals; Brian May's guitar
(overdubs, bell-like effects, the solo as a composed feature); studio
production (panning, flanger, wah-wah); flamboyant word-setting
(describe the character and word painting WITHOUT quoting lyrics).
Embed the official video once."""),
    ("aos2-vocal-music", 5, SPEC + """
LESSON 5 of 5 — set work study part 2: Killer Queen in close-up for the
exam. Structure (verses, choruses, guitar solo, varied final section),
tonality and harmony (major-key urbanity, chromatic slips, circle-of-
fifths touches), texture (voice-and-piano core, stacked vocal harmony,
guitar layers), rhythm (swung 12/8-vs-4/4 lilt feel), production
techniques as exam points, and comparison hooks against Purcell (voice
+ accompaniment three centuries apart). NO lyrics. Embed once."""),
    ("aos3-stage-and-screen", 1, SPEC + """
LESSON 1 of 5 in 'Music for Stage and Screen'. Scope: what stage and
screen music must DO — carry character, situation and action; the
musical theatre showstopper tradition and the symphonic film main
title. Introduce BOTH set works briefly: Defying Gravity (Wicked) and
the Star Wars Main Title. Embed one performance of each. NO lyric
quotation."""),
    ("aos3-stage-and-screen", 2, SPEC + """
LESSON 2 of 5 — set work study part 1: Schwartz, Defying Gravity
(2003, Wicked). Context and construction: the Act One finale as
dramatic hinge; the opening dialogue-like exchange before the song
proper; the 'Unlimited' motif and its deliberate rhythmic disguise of
a famous rainbow-song quotation (name the connection carefully as
Schwartz's acknowledged in-joke); the power-ballad build, key scheme
rising towards the D flat major ending; orchestration blending pit
band and rock kit. NO lyric quotation. Embed one official
performance."""),
    ("aos3-stage-and-screen", 3, SPEC + """
LESSON 3 of 5 — set work study part 2: Defying Gravity in close-up for
the exam. Structure (recit-like opening, verse-chorus core, the
soaring final section and coda), melody (the rising 'Unlimited' motif,
pentatonic colouring, wide-leap climaxes), harmony and tonality (key
changes as dramatic lift, the chromatic mediant moves), rhythm (driving
quaver accompaniment vs held vocal lines), texture and orchestration,
and how exam questions target it. NO lyrics. Embed once."""),
    ("aos3-stage-and-screen", 4, SPEC + """
LESSON 4 of 5 — set work study part 1: John Williams, Main Title from
Star Wars Episode IV: A New Hope (1977). Context and construction: the
revival of the symphonic film score; Korngold and Holst as stylistic
ancestors; the fanfare opening (brass, rising fourths and fifths,
triplet figures); leitmotif as the score's engine (the Main Title as
the hero's theme); B flat major brightness; the full symphony
orchestra as the sound of adventure. Embed ONE official recording."""),
    ("aos3-stage-and-screen", 5, SPEC + """
LESSON 5 of 5 — set work study part 2: the Star Wars Main Title in
close-up for the exam. Structure (fanfare, the A theme, the lyrical
contrasting B section on strings, return and link into the film),
melody (triadic, wide leaps, triplet upbeats), rhythm and metre
(march-like drive, syncopated stabs), orchestration section by section
(brass fanfares, string lyricism, percussion punctuation), harmony
(quartal touches inside confident major tonality), and exam question
angles including comparison with Defying Gravity. Embed once."""),
    ("aos4-fusions", 1, SPEC + """
LESSON 1 of 5 in 'Fusions'. Scope: what fusion MEANS — musics meeting:
instruments, scales, rhythms and production traditions combining, and
the questions the exam asks about identifying the ingredients.
Introduce BOTH set works briefly: Afro Celt Sound System's Release
(Celtic + West African + electronic dance) and Esperanza Spalding's
Samba Em Preludio (jazz + Brazilian bossa nova). Embed one recording of
each. NO lyric quotation."""),
    ("aos4-fusions", 2, SPEC + """
LESSON 2 of 5 — set work study part 1: Afro Celt Sound System, Release
(1999, Volume 2: Release). Context and construction: the band's
project of joining Irish traditional music and West African tradition
inside electronic production; the instrumental ingredients to NAME
(uilleann pipes, whistle, fiddle, accordion on the Celtic side; talking
drum, kora and djembe on the African side; synth drones, loops and
programmed beats underneath); the long-form build from atmospheric
opening to full groove; the guest vocal's keening, ornamented style
described without quoting words. Embed ONE official recording."""),
    ("aos4-fusions", 3, SPEC + """
LESSON 3 of 5 — set work study part 2: Release in close-up for the
exam. Structure as a build (sections added layer by layer, breakdown
and return), rhythm (the meeting of Irish dance lilt and African
cross-rhythm over a programmed pulse), texture (drone foundation,
melodic dialogue between pipes/whistle and kora/voice), technology as
an instrument (loops, processing, production), and how exam questions
ask students to identify each tradition's contribution. NO lyrics.
Embed once."""),
    ("aos4-fusions", 4, SPEC + """
LESSON 4 of 5 — set work study part 1: Esperanza Spalding, Samba Em
Preludio (2010, Chamber Music Society). Context and construction: a
jazz bassist-singer reimagining a Brazilian classic (the song is by
Baden Powell and Vinicius de Moraes, 1962 — credit it properly); the
intimate opening as a duet of voice and double bass; the Portuguese-
language vocal described without quotation; acoustic guitar entering
with bossa nova comping; the string ensemble colour; minor-key
lyricism. Embed ONE official recording."""),
    ("aos4-fusions", 5, SPEC + """
LESSON 5 of 5 — set work study part 2: Samba Em Preludio in close-up
for the exam. Structure (free, rubato opening into tempo; the bass
solo as centrepiece; the return), rhythm (bossa nova comping patterns
against flowing vocal lines), texture (duet growing to ensemble;
virtuosic double bass as both foundation and soloist), harmony
(extended jazz chords, minor tonality), fusion ingredients to name
(jazz improvisation + Brazilian song), and exam angles including
comparison with Release. NO lyrics. Embed once."""),
]


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    sub = sb.table("subjects").select("id").eq("slug", "music-edexcel").execute().data[0]["id"]
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
