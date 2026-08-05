# -*- coding: utf-8 -*-
"""Prototype: an ARTICLE lesson for AoS3 with listening extracts inline.

The point being tested: the Unity article format failed because it described
music the reader could not hear. Here every technical claim is followed
immediately by the extract that demonstrates it, so the prose and the sound sit
in the same breath. lesson-loader.js injects content_html raw (no sanitising),
so audio players work inside an article body.

Format is decided per UNIT, so this needs its own article unit - it cannot sit
in the practice unit next to the drills.

Extracts are labelled as StudyVault study extracts. They are generated to
demonstrate a style, and a student should never be left thinking they are
hearing a historic recording.

Usage: python scripts/music-practice/build_article_prototype.py [--dry-run]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client

DRY = "--dry-run" in sys.argv
R2 = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-aqa/aos-listening"
UNIT_SLUG = "aos3-traditional-music"


def excerpt(nid, label, clip, listen_for):
    """Inline listening extract.

    CLASSES, NOT INLINE STYLES. The first version hard-coded a 16px radius
    inline, which meant the redesign could not restyle it - inline styles beat
    any stylesheet, so the card stayed round inside a squared-off skin. The
    look now lives in css/style.css (production) and css/reskin.css (redesign),
    so each skin owns its own treatment and the content stays presentational-
    free. Deliberately no coloured edge stripe in either.
    """
    return (
        '<figure class="sv-listen" data-narration-id="%s">'
        '<figcaption class="sv-listen-label">Listen &mdash; %s</figcaption>'
        '<audio class="sv-listen-player" controls preload="none" src="%s/%s.mp3"></audio>'
        '<p class="sv-listen-for"><strong>Listen for:</strong> %s</p>'
        '<p class="sv-listen-credit">StudyVault study extract &mdash; written to '
        'demonstrate the style.</p></figure>' % (nid, label, R2, clip, listen_for))


CONTENT = """
<h2 data-narration-id="n1">What &ldquo;Traditional Music&rdquo; Means in This Exam</h2>
<p data-narration-id="n2">Traditional music covers two things on this specification. The first is music that takes its influences from traditional sources &mdash; folk music, for example &mdash; and reworks them in a modern style. The second is traditional music from its own culture, performed as it was meant to be performed. Both count, and both turn up in the listening paper.</p>
<p data-narration-id="n3">You will meet four styles, and you are expected to recognise each one from a short extract you have never heard before: blues from 1920 to 1950, fusion music drawing on African and/or Caribbean music, contemporary Latin music, and contemporary folk music of the British Isles.</p>
<p data-narration-id="n4">Reading about these styles is not enough. Each section below gives you the features examiners look for, and then an extract so you can hear the feature straight away. Play every extract. The point is to attach a word to a sound, so that when the sound turns up in the exam the word comes back to you.</p>

<h2 data-narration-id="n5">Blues, 1920&ndash;1950</h2>
<p data-narration-id="n6">Blues is built on repetition. Most blues songs follow the <dfn class="term" data-def="A repeating twelve-bar chord pattern using chords I, IV and V, the harmonic backbone of most blues songs.">twelve-bar blues</dfn> &mdash; a twelve-bar chord pattern using chords I, IV and V that repeats for the whole song. Once you hear the pattern come round again, you have found it.</p>
<p data-narration-id="n7">Three other features give blues away. The rhythm is usually <dfn class="term" data-def="An uneven long-short division of the beat that gives blues and jazz their characteristic lilt.">swung</dfn>, so the beat divides unevenly into a long-short lilt rather than straight halves. The singer is answered by an instrument in <dfn class="term" data-def="A phrase from one performer answered by another, a structure found across blues, gospel and African music.">call and response</dfn>. And the melody bends certain notes flat &mdash; the <dfn class="term" data-def="A flattened third, fifth or seventh, giving blues melodies their characteristic sound.">blue notes</dfn> &mdash; which is where the style gets its sound and its name.</p>
__BLUES__
<div class="key-fact" data-narration-id="n9">
  <div class="key-fact-label">Key Fact</div>
  <p>If you can hear a chord pattern returning to the start every twelve bars, and the beat has an uneven long-short swing, you are almost certainly listening to blues.</p>
</div>

<h2 data-narration-id="n10">Fusion with African and Caribbean Music</h2>
<p data-narration-id="n11">Fusion means two traditions meeting. In this strand, African or Caribbean musical thinking meets a contemporary style, and the result usually shows it in the rhythm section rather than the tune.</p>
<p data-narration-id="n12">Listen for guitars playing short repeated patterns that lock together rather than strumming as one, and for percussion layered so that different parts pull against each other. That pull is <dfn class="term" data-def="Two or more conflicting rhythms sounding at the same time.">cross-rhythm</dfn>, and it is the single most reliable sign of this strand. In Caribbean styles you will often hear the chords land on the offbeat, which is what gives reggae and ska their lift.</p>
__FUSION__

<h2 data-narration-id="n14">Contemporary Latin Music</h2>
<p data-narration-id="n15">Latin music is percussion-led. Congas, bongos and timbales layer up under a piano riff called the <dfn class="term" data-def="A repeated syncopated piano riff that drives a salsa arrangement.">montuno</dfn>, and brass adds short punched chords on top. Underneath it all sits the <dfn class="term" data-def="A repeated five-note rhythmic pattern that underpins salsa and much Latin music.">clave</dfn>, a five-note rhythmic pattern that the whole band organises itself around.</p>
__LATIN__
<p data-narration-id="n17">Latin songs also have a distinctive structure. A lead singer improvises a line and the group answers with a fixed repeated phrase &mdash; the <dfn class="term" data-def="The fixed repeated group response in a salsa song, answering the lead singer.">coro</dfn>. It is call and response again, but arranged differently from blues: the group answer stays the same while the lead line changes.</p>
__CORO__

<h2 data-narration-id="n19">Contemporary Folk of the British Isles</h2>
<p data-narration-id="n20">British and Irish folk melodies often sit in a <dfn class="term" data-def="A scale other than standard major or minor, giving folk melodies their distinctive colour.">mode</dfn> rather than a straightforward major or minor key, which is why they can sound neither happy nor sad but somewhere else entirely. Underneath the tune you will often hear a <dfn class="term" data-def="A long held note or chord sounding continuously underneath a melody.">drone</dfn>, a held note that never moves.</p>
__FOLK__
<p data-narration-id="n22">The other giveaway is decoration. A folk player rarely repeats a tune identically. On the repeat they add <dfn class="term" data-def="Extra decorative notes such as rolls and grace notes added to a folk melody, especially on a repeat.">ornamentation</dfn> &mdash; quick grace notes and rolls threaded through the melody. Dance tunes such as jigs also move in compound time, with the beat dividing into three rather than two, which produces their characteristic bounce.</p>
__FIDDLE__

<h2 data-narration-id="n24">Writing About What You Hear</h2>
<p data-narration-id="n25">Recognising a style earns you nothing unless you can say why. Examiners want the technical word, not an impression. &ldquo;It sounds happy and bouncy&rdquo; scores nothing; &ldquo;the melody is decorated with grace notes over a drone, in compound time&rdquo; scores.</p>
<p data-narration-id="n26">Use this three-step habit for any listening answer. Name the element the question asks about. Give the technical term for what that element is doing. Say where in the extract you heard it. For example: &ldquo;The texture is call and response &mdash; the guitar answers each sung phrase throughout the extract.&rdquo;</p>
<div class="collapsible">
  <button class="collapsible-toggle" aria-expanded="false">
    <span>Words that earn marks in this Area of Study</span>
    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="collapsible-content"><div class="collapsible-inner">
    <p data-narration-id="n27">Twelve-bar blues, swung rhythm, blue note, call and response, cross-rhythm, offbeat chords, clave, montuno, coro, drone, modal melody, ornamentation, compound time. Each of these names something you can point to in a recording &mdash; which is exactly what an examiner is asking you to do.</p>
  </div></div>
</div>
"""


def main():
    blocks = {
        "__BLUES__": excerpt("n8", "Blues, 1920&ndash;1950", "aos3_blues",
                             "the guitar answering each sung line, and the uneven "
                             "long-short swing in the beat."),
        "__FUSION__": excerpt("n13", "Fusion &mdash; Caribbean influence",
                              "aos3_caribbean_fusion",
                              "two guitars playing interlocking repeated patterns, and "
                              "percussion layered into cross-rhythms."),
        "__LATIN__": excerpt("n16", "Contemporary Latin", "aos3_latin",
                             "layered hand percussion, and the repeated piano riff "
                             "driving the whole band."),
        "__CORO__": excerpt("n18", "Contemporary Latin &mdash; the coro",
                            "aos3_latin_coro",
                            "the group answering the lead singer with the same fixed "
                            "phrase each time."),
        "__FOLK__": excerpt("n21", "Folk of the British Isles", "aos3_british_folk",
                            "the sustained drone underneath, and the voice joining to "
                            "double the melody."),
        "__FIDDLE__": excerpt("n23", "Folk dance tune", "aos3_folk_fiddle",
                              "the fiddle leading, and the extra ornaments it adds when "
                              "the tune comes round again."),
    }
    content = CONTENT
    for token, html in blocks.items():
        content = content.replace(token, html)
    assert "__" not in content, "unreplaced excerpt token"

    row = {
        "lesson_number": 1,
        "slug": "lesson-01",
        "title": "Traditional Music: The Four Styles You Must Recognise",
        "description": "Blues, African and Caribbean fusion, contemporary Latin and British "
                       "folk — the features examiners listen for, with an extract for each.",
        "status": "pending_review",
        "tier": "both",
        "content_html": content.strip(),
        "exam_tip_html": "<p>Never describe an extract with feeling words alone. "
                         "&ldquo;Lively&rdquo; and &ldquo;sad&rdquo; earn nothing. Name the "
                         "element, give it its technical term, and say where you heard it "
                         "&mdash; three short clauses will out-score a paragraph of "
                         "impressions.</p>",
        "conclusion_html": "<p>Four styles, and one habit that unlocks all of them: attach a "
                           "word to a sound. Go back through this lesson and play each "
                           "extract once more, saying the feature out loud as you hear it. "
                           "Then take the Area of Study 3 listening drill, where the "
                           "extracts arrive without labels &mdash; exactly as they will in "
                           "the exam.</p>",
        "glossary_terms": [
            {"term": "Twelve-bar blues", "definition": "A repeating twelve-bar chord pattern using chords I, IV and V, the harmonic backbone of most blues songs."},
            {"term": "Swung rhythm", "definition": "An uneven long-short division of the beat that gives blues and jazz their characteristic lilt."},
            {"term": "Call and response", "definition": "A phrase from one performer answered by another."},
            {"term": "Blue note", "definition": "A flattened third, fifth or seventh, giving blues melodies their characteristic sound."},
            {"term": "Cross-rhythm", "definition": "Two or more conflicting rhythms sounding at the same time."},
            {"term": "Clave", "definition": "A repeated five-note rhythmic pattern that underpins salsa and much Latin music."},
            {"term": "Montuno", "definition": "A repeated syncopated piano riff that drives a salsa arrangement."},
            {"term": "Coro", "definition": "The fixed repeated group response in a salsa song, answering the lead singer."},
            {"term": "Drone", "definition": "A long held note or chord sounding continuously underneath a melody."},
            {"term": "Ornamentation", "definition": "Extra decorative notes such as rolls and grace notes added to a melody, especially on a repeat."},
        ],
        # plain text only by project rule - audio questions live in the practice unit
        "knowledge_checks": [
            {"q": "What is the twelve-bar blues?", "type": "mcq", "correct": 2,
             "options": ["A twelve-note melody used in every blues song",
                         "A group of twelve blues musicians",
                         "A repeating twelve-bar chord pattern using chords I, IV and V",
                         "A tempo marking of twelve beats per bar"]},
            {"q": "What does 'call and response' describe?", "type": "mcq", "correct": 1,
             "options": ["A melody played twice at different pitches",
                         "A phrase from one performer answered by another",
                         "A gradual increase in volume",
                         "Two instruments playing exactly together"]},
            {"q": "What is a drone?", "type": "mcq", "correct": 3,
             "options": ["A short repeated rhythmic pattern on percussion",
                         "A sudden loud chord",
                         "A melody decorated with grace notes",
                         "A long held note sounding continuously under a melody"]},
            {"q": "In a salsa arrangement, what is the coro?", "type": "mcq", "correct": 0,
             "options": ["The fixed repeated group response answering the lead singer",
                         "The improvised trumpet solo",
                         "The opening piano riff",
                         "The closing drum break"]},
            {"q": "Which rhythmic feel is typical of blues from 1920 to 1950?",
             "type": "mcq", "correct": 1,
             "options": ["A strict march rhythm",
                         "A swung, uneven long-short division of the beat",
                         "Free rhythm with no pulse",
                         "A fast waltz"]},
        ],
        "practice_questions": [
            {"text": "Name the chord pattern that forms the harmonic backbone of most blues songs.",
             "type": "1 mark — Identification",
             "marks": "1 mark for: twelve-bar blues / 12-bar blues."},
            {"text": "Describe two features of the rhythm you would expect to hear in a blues extract.",
             "type": "2 marks — Description",
             "marks": "1 mark each for any two of: swung/shuffle rhythm; uneven long-short division of the beat; steady four-in-a-bar pulse; syncopation."},
            {"text": "Explain what is meant by cross-rhythm, and say why it is a useful clue when identifying music with African or Caribbean influence.",
             "type": "3 marks — Explanation",
             "marks": "1 mark for a correct definition (two or more conflicting rhythms at once); 1 mark for locating it in the percussion or guitar parts; 1 mark for linking it to the style's identity rather than to the melody."},
            {"text": "A salsa extract features a lead singer and a group of backing singers. Describe how they interact, using the correct technical term.",
             "type": "2 marks — Description",
             "marks": "1 mark for call and response; 1 mark for identifying the coro as the fixed repeated group answer while the lead line varies."},
            {"text": "Identify two features that would suggest an extract is contemporary folk music of the British Isles.",
             "type": "2 marks — Identification",
             "marks": "1 mark each for any two of: drone; modal melody; ornamentation/grace notes on the repeat; compound time; fiddle leading the melody; acoustic plucked or strummed accompaniment."},
            {"text": "A student writes: 'The music sounds lively and happy.' Rewrite this as an exam answer that would earn marks.",
             "type": "3 marks — Application",
             "marks": "Credit any answer that names an element, gives its technical term and locates it — for example: 'The tempo is fast and the fiddle melody is decorated with grace notes over a drone, in compound time.' 1 mark per accurate technical point, maximum 3.",
             },
        ],
    }

    sb = get_client()
    subj = sb.from_("subjects").select("id, settings").eq("slug", "music-aqa") \
             .is_("school_id", "null").execute().data[0]
    existing = sb.from_("units").select("id").eq("subject_id", subj["id"]) \
                 .eq("slug", UNIT_SLUG).execute().data
    if existing:
        unit_id = existing[0]["id"]
    elif DRY:
        unit_id = "(dry)"
    else:
        unit_id = sb.from_("units").insert({
            "subject_id": subj["id"], "slug": UNIT_SLUG,
            "name": "Area of Study 3: Traditional Music",
            "subtitle": "Blues, fusion, Latin and British folk — what each style sounds "
                        "like and how to write about it.",
            "body_class": "unit-music-aqa-aos3", "accent": "#0f766e",
            "accent_light": "#0f766e22", "accent_badge": "#0f766e33",
            "lesson_count": 1, "sort_order": 5,
        }).execute().data[0]["id"]
    row["unit_id"] = unit_id
    print("unit:", unit_id)
    print("content: %d chars, %d inline extracts, %d glossary terms, %d KCs, %d practice Qs"
          % (len(row["content_html"]), row["content_html"].count("<audio"),
             len(row["glossary_terms"]), len(row["knowledge_checks"]),
             len(row["practice_questions"])))
    if DRY:
        print("dry run - nothing written")
        return
    old = sb.from_("lessons").select("id").eq("unit_id", unit_id) \
            .eq("lesson_number", 1).execute().data
    if old:
        sb.from_("lessons").update(row).eq("id", old[0]["id"]).execute()
        print("updated lesson", old[0]["id"])
    else:
        rec = sb.from_("lessons").insert(row).execute().data[0]
        print("inserted lesson", rec["id"])
    # article unit: must NOT be in practice_units
    pu = (subj.get("settings") or {}).get("practice_units") or []
    print("practice_units (unchanged, article unit stays out):", pu)


if __name__ == "__main__":
    main()
