# -*- coding: utf-8 -*-
"""Apply the Phase 6 fact-check findings to the music-aqa articles.

Verdict: 3 HIGH (all Bartok, AoS4 L2), 4 MEDIUM, 6 LOW. Every replacement
below is grounded in AQA's own teacher guides (AoS1 Beethoven, AoS4 Bartok,
May 2024). Each old string must occur exactly once or the script aborts
before writing anything.
"""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

# (unit_slug, lesson_number, field, old, new)
FIXES = [
    # ---- LOWs in other lessons -------------------------------------------
    ("aos3-traditional-music", 1, "content_html",
     "which is where the style gets its sound and its name.",
     "which is where the style gets its characteristic sound."),
    ("aos1-western-classical", 1, "content_html",
     "texture &mdash; every string moving together, not weaving separate lines.",
     "texture &mdash; rippling arpeggiated string figuration over sustained harmonies, with no independent melodic lines."),
    ("aos1-western-classical", 1, "content_html",
     "two eight-bar sections, each repeated. Then, with no warning, the full orchestra crashes in on a single fortissimo chord.",
     "two eight-bar sections, each repeated &mdash; and at the very end of the first section&rsquo;s repeat, with no warning, the full orchestra crashes in on a single fortissimo chord."),
    ("aos1-western-classical", 3, "content_html",
     "Beethoven wrote his First Symphony as a student and admirer of Haydn and Mozart,",
     "Beethoven wrote his First Symphony as a former pupil of Haydn and an admirer of Mozart,"),
    # ---- Minimalism (AoS4 L3): In C is not additive ----------------------
    ("aos4-since-1910", 3, "content_html",
     "Terry Riley&rsquo;s <em>In C</em> is the piece that made this technique famous. It is not one fixed melody but 53 short numbered patterns;",
     "Terry Riley&rsquo;s <em>In C</em> works differently &mdash; built not on note-by-note growth but on staggered repetition. It is not one fixed melody but 53 short numbered patterns;"),
    ("aos4-since-1910", 3, "content_html",
     "<em>In C</em> runs to about 43 minutes &mdash; far too long for a revision session.",
     "A performance of <em>In C</em> typically runs anywhere from forty-five to ninety minutes &mdash; far too long for a revision session."),
    # ---- Bartok (AoS4 L2): the three HIGHs and three MEDIUMs -------------
    ("aos4-since-1910", 2, "content_html",
     "Bartók called it the most important work of his life.</p>",
     "</p>"),
    ("aos4-since-1910", 2, "content_html",
     '<h2 data-narration-id="n9">Orchestration, and the cimbalom sound</h2>',
     '<h2 data-narration-id="n9">Orchestration with a light touch</h2>'),
    ("aos4-since-1910", 2, "content_html",
     "Hungarian Sketches is written for full orchestra &mdash; woodwind, brass, timpani and light percussion, harp, celesta and strings &mdash; but used with a light touch.",
     "Hungarian Sketches is written for orchestra &mdash; woodwind including piccolo, bass clarinet and contrabassoon, horns, trumpets, trombones and tuba, timpani, percussion including side drums, triangle, cymbals and bass drum, and strings &mdash; but used with a light touch. Evening in the Village uses only woodwind, two horns and strings."),
    # the whole cimbalom paragraph (n11) becomes a string-colour paragraph
    ("aos4-since-1910", 2, "content_html",
     'The <dfn class="term" data-def="A Hungarian folk instrument: a large trapezoid box of strings struck with small beaters, giving a bright, ringing, metallic sound.">cimbalom</dfn> is a hammered dulcimer at the centre of a traditional Hungarian folk band, and its shimmering sound is one of the clearest markers of Hungarian folk colour in orchestral music of this period. Hungarian Sketches does not actually call for a real cimbalom. Instead, Bartók suggests its bright, rattling shimmer with instruments he does have &mdash; harp, celesta, and <dfn class="term" data-def="A string technique: plucking the string with a finger instead of drawing the bow across it.">pizzicato</dfn> strings, sometimes combined with fast <dfn class="term" data-def="A rapid repetition of a single note or quick alternation between two notes, used for shimmer or tension.">tremolo</dfn>. Listen for that glittering texture whenever the orchestra thins out and a folk-dance idea takes over.',
     'What examiners reward here is Bartók&rsquo;s precision about sonority. The strings switch constantly between bowed playing and <dfn class="term" data-def="A string technique: plucking the string with a finger instead of drawing the bow across it.">pizzicato</dfn>, add fast <dfn class="term" data-def="A rapid repetition of a single note or quick alternation between two notes, used for shimmer or tension.">tremolo</dfn> for shimmer, play muted (con sordino) and are even asked to play <em>ruvido</em> &mdash; coarsely. The brass mute and unmute; the triangle player is told to use a metal beater. Almost every note of the woodwind melodies carries an articulation instruction. That level of detailed instruction about instrumental colour and dynamics is a signature of the piece &mdash; and a ready-made Section B answer.'),
    ("aos4-since-1910", 2, "content_html",
     "Listen for it in the dance movements especially &mdash; Bear Dance and Swineherd&rsquo;s Dance both lean on it hard, alongside short repeated",
     "Its home in this suite is Evening in the Village: the quicker dance melody of that movement&rsquo;s Allegretto sections is built on scotch snaps. The dance movements drive differently &mdash; on short repeated"),
    ("aos4-since-1910", 2, "content_html",
     "given first to a solo woodwind voice over a quiet <dfn class=\"term\" data-def=\"A sustained note or chord held underneath a melody.\">drone</dfn> in the strings beneath it. A brisker dance episode interrupts partway through before the opening mood returns &mdash; a simple frame of stillness around a burst of movement, evoking dusk settling over a village.",
     "given first to a solo clarinet over a chordal string accompaniment whose bass steps quietly down through the mode &mdash; both melodies here are pentatonic. The slow, rubato song (Lento rubato) alternates with a quicker Allegretto dance tune nearly twice its speed &mdash; five sections in all, slow-fast-slow-fast-slow &mdash; and it is this dance tune that carries the movement&rsquo;s scotch snaps. Sustained <dfn class=\"term\" data-def=\"A sustained note held underneath or above changing harmony.\">pedal</dfn> notes in clarinet and then horn anchor the faster music, evoking dusk settling over a village.",),
    ("aos4-since-1910", 2, "content_html",
     "listen for the long, freely-sung opening melody over a hushed drone, and the brief faster dance episode that interrupts it.",
     "listen for the long, freely-sung clarinet melody over quiet string chords, and the two quicker dance episodes with their scotch-snap rhythms."),
    ("aos4-since-1910", 2, "content_html",
     "The music is heavy, insistent, and built from short repeated motifs low in the orchestra, with strong accents landing off the beat. It is loud, comic, and deliberately clumsy rather than graceful: the orchestration keeps pulling the weight downward, as if the &ldquo;dancer&rdquo; cannot lift its feet cleanly.",
     "The music is heavy, insistent, and built over a near-constant even-quaver <dfn class=\"term\" data-def=\"A short musical pattern repeated persistently, often in the bass or accompaniment.\">ostinato</dfn>, almost everything staccato and marcato, with sforzando stabs, abrupt changes of dynamic and clashing pedal-note drones underneath. It is comic and deliberately clumsy rather than graceful &mdash; and after all that force, the movement ends quietly: a surprise worth naming in the exam."),
    ("aos4-since-1910", 2, "content_html",
     "listen for the heavy, low-register motif and the off-beat accents that give the bear its lumbering weight.",
     "listen for the relentless quaver ostinato, the staccato weight of the low register, and the quiet ending that catches everyone out."),
    ("aos4-since-1910", 2, "content_html",
     "The suite ends with its fastest, most driven movement: a lively folk dance for the full orchestra, built on the snap rhythms and repeated dance motifs already established earlier in the suite. Energy and volume build toward the close, giving Hungarian Sketches a bright, high-spirited finish.",
     "The suite ends with a movement built on a genuine collected folk tune &mdash; the only one in the suite &mdash; set to driving dance rhythms with syncopation, semiquaver runs and triplets. Its journey is the examinable fact: a fairly calm dance at the start, a fortissimo climax in the <em>middle</em> of the movement, then a long winding-down &mdash; calmo, then sempre più calmo with a gradual rallentando, sinking to a sustained pianissimo chord as if the dancers are exhausted &mdash; before the final five bars snap back to tempo and a one-bar molto crescendo lands the last loud chord."),
    ("aos4-since-1910", 2, "content_html",
     "listen for the driving snap rhythms and full-orchestra energy building to the close of the suite.",
     "listen for the real folk tune, the mid-movement climax, the long calmo wind-down, and the five-bar burst that ends the suite."),
    ("aos4-since-1910", 2, "content_html",
     "&ldquo;Bartók uses a snap rhythm in the dance tune of Swineherd&rsquo;s Dance&rdquo; earns marks, because it names the feature, uses the right term, and locates it.",
     "&ldquo;Bartók builds the Allegretto dance tune of Evening in the Village on scotch-snap rhythms&rdquo; earns marks, because it names the feature, uses the right term, and locates it."),
    ("aos4-since-1910", 2, "content_html",
     "keep the cimbalom-effect and snap-rhythm vocabulary ready &mdash; both come up again and again across Bartók&rsquo;s folk-influenced writing.",
     "keep the ostinato and scotch-snap vocabulary ready &mdash; and make sure each one is attached to the right movement."),
    ("aos4-since-1910", 2, "conclusion_html",
     "with the cimbalom-effect and the snap rhythm as the two features examiners come back to most often.",
     "with the scotch snaps of Evening in the Village&rsquo;s dance tune and the driving ostinati of the dance movements as the features examiners come back to most often."),
]

sb = get_client()
s = [x for x in sb.table("subjects").select("id,school_id").eq(
    "slug", "music-aqa").execute().data if not x["school_id"]][0]
units = {u["slug"]: u["id"] for u in sb.table("units").select(
    "id,slug").eq("subject_id", s["id"]).execute().data}

cache = {}
for uslug, num, field, old, new in FIXES:
    k = (uslug, num)
    if k not in cache:
        cache[k] = sb.table("lessons").select(
            "id,title,content_html,conclusion_html,practice_questions,knowledge_checks"
        ).eq("unit_id", units[uslug]).eq("lesson_number", num).single().execute().data
    l = cache[k]
    assert old in l[field], "NOT FOUND %s L%d %s: %r" % (uslug, num, field, old[:70])
    assert l[field].count(old) == 1, "AMBIGUOUS %s L%d: %r" % (uslug, num, old[:70])
    l[field] = l[field].replace(old, new)

# ---- question fixes (Bartok L2 + minimalism L3) --------------------------
bartok = cache[("aos4-since-1910", 2)]
pqs = bartok["practice_questions"]
assert "off-beat accents" in pqs[1]["marks"]
pqs[1]["marks"] = ("3 marks, one for each valid point: near-constant repeated quaver "
                   "ostinato; staccato and marcato articulation with sforzando accents "
                   "and abrupt dynamic changes; low register or low instruments and "
                   "dissonant pedal drones suggesting lumbering weight.")
assert "cimbalom" in pqs[2]["text"]
pqs[2] = {"text": "Describe two ways Bartok asks the strings to change their sound in Hungarian Pictures.",
          "type": "2 marks — Description",
          "marks": "Any two of: pizzicato (plucked) versus arco (bowed); tremolo for shimmer; con sordino (muted); playing ruvido (coarsely). 1 mark each."}
assert "Bear Dance or Swineherd's Dance" in pqs[3]["marks"]
pqs[3]["marks"] = ("2 marks: 1 mark for a correct definition, a very short accented note "
                   "followed by a longer note; 1 mark for locating it in Evening in the "
                   "Village (its quicker Allegretto dance melody).")
kcs = bartok["knowledge_checks"]
assert "cimbalom" in kcs[2]["q"]
kcs[2] = {"q": "What drives Bear Dance forward underneath the melody?",
          "type": "mcq", "correct": 1,
          "options": ["A waltz accompaniment in the horns",
                      "A near-constant repeated quaver ostinato, mostly in the strings",
                      "Snap rhythms in the timpani",
                      "Harp arpeggios"]}

mini = cache.setdefault(("aos4-since-1910", 3), sb.table("lessons").select(
    "id,title,content_html,conclusion_html,practice_questions,knowledge_checks"
).eq("unit_id", units["aos4-since-1910"]).eq("lesson_number", 3).single().execute().data)
mpqs = mini["practice_questions"]
tgt = [q for q in mpqs if "grows by one note" in q["text"]][0]
tgt["marks"] = ("1 mark for 'additive process'. 1 mark for a correct composer: Philip "
                "Glass most clearly, or Steve Reich for build-up passages. (Terry "
                "Riley's In C is NOT additive - its 53 modules are fixed patterns "
                "players repeat and move through at their own pace.)")

for (uslug, num), l in cache.items():
    sb.table("lessons").update({
        "content_html": l["content_html"],
        "conclusion_html": l["conclusion_html"],
        "practice_questions": l["practice_questions"],
        "knowledge_checks": l["knowledge_checks"],
    }).eq("id", l["id"]).execute()
    print("fixed: %s L%d  %s" % (uslug, num, l["title"][:48]))
print("done - %d replacements + question fixes applied" % len(FIXES))
