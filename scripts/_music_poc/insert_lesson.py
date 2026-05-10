"""Insert a single proof-of-concept Music listening lesson into Supabase.

Subject: music-aqa (free-tier, status=live).
Unit: listening (Listening Skills).
Lesson 1: Mozart Symphony No. 40 in G minor, K. 550, Mvt 1.

Audio: PD recording from MusOpen Symphony, hosted on R2.
Practice questions: 5 drafted from verified facts (see fact-sheet-mozart-40.md).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


AUDIO_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-aqa/listening/mozart-40-mvt1.mp3"


CONTENT_HTML = f"""
<p data-narration-id="n1">This lesson is a listening drill on the opening movement of <strong>Mozart's Symphony No. 40 in G minor</strong> (K. 550), composed in 1788. The recording below is a public-domain performance by the Musopen Symphony &mdash; you can pause, replay, and jump to any timestamp the questions reference.</p>

<figure class="lesson-audio-player" style="margin: 1.5rem 0;">
  <audio controls preload="metadata" src="{AUDIO_URL}" style="width: 100%;"></audio>
  <figcaption style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem;">Mozart, Symphony No. 40 in G minor, K. 550, I. Molto allegro &mdash; Musopen Symphony (public domain). Duration 5:59.</figcaption>
</figure>

<h2 data-narration-id="n2">What you should listen for</h2>
<p data-narration-id="n3">Before you tackle the practice questions, listen to the whole movement once. As you do, notice three things:</p>

<ul>
  <li data-narration-id="n4"><strong>The opening texture.</strong> The piece does not begin with the main melody. Instead, the lower strings (violas, divided into two parts) play a quiet, restless accompaniment. The famous main theme &mdash; a falling, sighing figure on the violins &mdash; only enters a couple of bars later.</li>
  <li data-narration-id="n5"><strong>The mood of the main theme.</strong> Encyclopaedia Britannica describes the opening as "plaintive sighs" in the so-called <em>Sturm und Drang</em> (storm and stress) style. Listen for the descending semitone shape that gives the theme its anxious quality.</li>
  <li data-narration-id="n6"><strong>The development section</strong> (around the middle of the movement, roughly 2:30 to 3:30). Mozart writes a passage that touches every note of the chromatic scale except one &mdash; the tonic G itself &mdash; which destabilises the home key dramatically.</li>
</ul>

<details class="collapsible">
  <summary>Quick context: why this piece appears in Music GCSE</summary>
  <p>Mozart's Symphony No. 40 is one of three symphonies he wrote in the summer of 1788 (Nos. 39, 40, and 41). It is the only one in a minor key, and is commonly studied for its compressed sonata form, vocal-style melodic writing, and Mozart's later revision adding clarinets to the original 1788 scoring. The first movement is dense with features GCSE specifications love to test: classical sonata form, contrasting subjects, key relationships, and the development's chromaticism.</p>
</details>

<details class="collapsible">
  <summary>Glossary terms used in the questions</summary>
  <p><dfn class="term">Sonata form</dfn> &mdash; the standard structure for a classical symphony's first movement: an exposition presenting two contrasting themes in different keys, a development reworking those themes, and a recapitulation bringing them back in the home key.</p>
  <p><dfn class="term">Tonic</dfn> &mdash; the home note and chord that a piece is centred on. Here, that is G.</p>
  <p><dfn class="term">Sturm und Drang</dfn> &mdash; an 18th-century artistic style emphasising emotion, agitation, and minor keys. Mozart drew on it for several G minor works.</p>
</details>

<p data-narration-id="n7" data-revision-tip="Always listen to a piece TWICE before answering: once with no questions in front of you (just absorb the shape), then a second time with the question stems in mind so you know what to look for.">Now use the audio player to answer the practice questions below. You can replay any section as many times as you need.</p>
"""

PRACTICE_QUESTIONS = [
    {
        "type": "1 mark — Multiple Choice",
        "marks": "1",
        "text": "Listen to the opening 30 seconds of the recording. What is the home key of this piece?",
        "options": ["G major", "G minor", "D minor", "B-flat major"],
        "correct": 1,
        "mark_scheme": "<p><strong>Mastering (1 mark):</strong> selects G minor. The tempo marking 'Molto allegro' and the sustained minor tonality throughout the opening confirm the key. The work is universally catalogued as Mozart's Symphony No. 40 'in G minor', K. 550.</p><p><strong>Other options:</strong> G major (wrong mode), D minor (the dominant minor, plausible if you only hear the tension), B-flat major (the relative major, which features later in the exposition but is not the home key).</p>",
    },
    {
        "type": "1 mark — Identify / State",
        "marks": "1",
        "text": "Listen to the very opening, before the main melody enters. Which family of instruments plays the accompaniment first?",
        "options": ["Woodwind", "Brass", "Strings", "Full orchestra together"],
        "correct": 2,
        "mark_scheme": "<p><strong>Mastering (1 mark):</strong> selects Strings. Mozart begins the movement, unusually, with the lower strings (the violas, written in two parts) playing a quiet pulsing accompaniment. The violins then enter with the main 'sighing' theme on top. Accept any specific correct answer such as 'lower strings' or 'violas'.</p><p><strong>Why this matters:</strong> opening with the accompaniment rather than the melody was a bold gesture &mdash; it foreshadows a technique later used by Mozart and by Romantic composers such as Mendelssohn.</p>",
    },
    {
        "type": "2 marks — Describe",
        "marks": "2",
        "text": "Describe one feature of the opening melody (the violins' main theme) that contributes to its anxious, restless mood.",
        "options": [
            "It uses a falling, sighing shape with descending semitones.",
            "It uses a major-key melody with a confident, marching rhythm.",
            "It is played by solo trumpet.",
            "It uses long, slow, sustained notes throughout."
        ],
        "correct": 0,
        "mark_scheme": "<p><strong>Mastering (2 marks):</strong> identifies a specific musical feature (descending semitone / falling 'sigh' figure / minor-key melody / agitated string accompaniment / soft dynamic / repeated rhythmic motif) AND links it to the unsettled mood.</p><p><strong>Secure (1 mark):</strong> identifies a feature OR gives a mood-word, but does not connect them.</p><p><strong>Developing / Emerging:</strong> incorrect feature (e.g. major key, slow tempo) or vague mood description without justification.</p><p><strong>Reference quote (Britannica):</strong> the opening's character is described as 'plaintive sighs' in the Sturm und Drang style.</p>",
    },
    {
        "type": "3 marks — Explain",
        "marks": "3",
        "text": "Mozart wrote two versions of this symphony. The original 1788 version did not include clarinets; in 1791 he revised the score to add them. Which of the following best explains why a composer might revise a work in this way?",
        "options": [
            "The composer wanted to make the piece harder to perform.",
            "Clarinets had only just been invented in 1791.",
            "A specific upcoming performance had clarinettists available, and Mozart wanted to take advantage of their warmer woodwind blend.",
            "Modern audiences prefer clarinets to oboes, so the revision was made for popular taste."
        ],
        "correct": 2,
        "mark_scheme": "<p><strong>Mastering (3 marks):</strong> selects option 3. The revision involved adding two clarinet parts and redistributing some woodwind lines so the oboes did not double the new clarinets. Mozart's likely motivation, as suggested by Wikipedia and confirmed by the existence of separately-prepared parts, was a planned performance with available clarinettists. The clarinet's warmer, mellower timbre also softens the oboe-led blend in the original.</p><p><strong>Why the other options are wrong:</strong> clarinets were already common by 1788 (Mozart had used them in his Clarinet Quintet K. 581 in 1789); composers do not normally add instruments to make a piece harder; the revision predates 'modern audiences' by 200 years.</p>",
    },
    {
        "type": "4 marks — Describe",
        "marks": "4",
        "text": "Listen to the section between roughly 2:30 and 3:30 of the recording. This passage is from the development section. Describe one feature of how Mozart destabilises the home key here.",
        "options": [
            "He uses extensive chromatic movement, touching every note of the chromatic scale except the tonic G itself.",
            "He stays firmly in G minor throughout, never modulating.",
            "He stops the orchestra completely for ten seconds of silence.",
            "He has the brass section play a fanfare in C major."
        ],
        "correct": 0,
        "mark_scheme": "<p><strong>Mastering (4 marks):</strong> identifies the chromatic passage AND explains its destabilising effect. A model answer: 'In the development, Mozart sequences the main motif through a chromatic passage that uses every note of the chromatic scale except G. By deliberately omitting the tonic, he prevents the listener from grounding the music in any clear key, which heightens tension before the recapitulation returns to G minor.'</p><p><strong>Secure (3 marks):</strong> identifies the chromatic passage but explanation is partial or imprecise.</p><p><strong>Developing (2 marks):</strong> identifies that the music modulates a lot or feels unstable, without naming the chromatic technique.</p><p><strong>Emerging (1 mark):</strong> vague reference to 'modulation' without further detail.</p><p><strong>Source:</strong> Wikipedia article on Symphony No. 40 (Mozart) describes this passage directly, noting that G &mdash; the tonic &mdash; is the single chromatic note Mozart leaves out.</p>",
    },
]


def main():
    sb = get_client()

    # Idempotency: if subject exists, abort with clear error
    existing = sb.table('subjects').select('id, slug').eq('slug', 'music-aqa').execute().data
    if existing:
        print(f"  ABORT: subject music-aqa already exists ({existing[0]['id']}). Delete it first if you want to rebuild.")
        return 1

    # 1. Subject row
    settings = {
        "quote_ticker_html": (
            '<div class="quote-ticker"><div class="quote-ticker-track">'
            '<span class="quote-item" style="--q-color: #7c3aed;">Music expresses that which cannot be put into words and that which cannot remain silent. <em>&mdash; Victor Hugo</em></span>'
            '<span class="quote-item" style="--q-color: #be185d;">Music is the silence between the notes. <em>&mdash; Claude Debussy</em></span>'
            '<span class="quote-item" style="--q-color: #7c3aed;">Music expresses that which cannot be put into words and that which cannot remain silent. <em>&mdash; Victor Hugo</em></span>'
            '<span class="quote-item" style="--q-color: #be185d;">Music is the silence between the notes. <em>&mdash; Claude Debussy</em></span>'
            '</div></div>'
        ),
        "practice_units": [],
    }
    subject_row = sb.table('subjects').insert({
        "slug": "music-aqa",
        "name": "Music",
        "exam_board": "AQA",
        "spec_code": "8271",
        "school_id": None,
        "status": "live",
        "settings": settings,
    }).execute().data[0]
    print(f"  subject inserted: {subject_row['id']}")

    # 2. Unit row
    unit_row = sb.table('units').insert({
        "subject_id": subject_row['id'],
        "slug": "listening",
        "name": "Listening Skills",
        "subtitle": "Public-domain works for listening drills",
        "body_class": "unit-music-aqa-1",
        "accent": "#7c3aed",
        "accent_light": "#f5f3ff",
        "accent_badge": "#7c3aed33",
        "lesson_count": 1,
        "sort_order": 1,
    }).execute().data[0]
    print(f"  unit inserted: {unit_row['id']}")

    # 3. Lesson row
    lesson_row = sb.table('lessons').insert({
        "unit_id": unit_row['id'],
        "lesson_number": 1,
        "title": "Mozart Symphony No. 40 — Opening Listening Drill",
        "slug": "mozart-symphony-40-opening",
        "description": "Five listening questions on the opening movement of Mozart's Symphony No. 40 in G minor.",
        "status": "pending_review",
        "content_html": CONTENT_HTML.strip(),
        "practice_questions": PRACTICE_QUESTIONS,
        "knowledge_checks": [],
        "flashcard_questions": [],
        "glossary_terms": [
            {"term": "Sonata form", "definition": "The standard structure for a classical symphony's first movement: exposition, development, and recapitulation."},
            {"term": "Tonic", "definition": "The home note and chord that a piece is centred on. In this work the tonic is G."},
            {"term": "Sturm und Drang", "definition": "An 18th-century artistic style emphasising emotion and agitation, often using minor keys."},
        ],
    }).execute().data[0]
    print(f"  lesson inserted: {lesson_row['id']}")

    print()
    print(f"  URL to test: /lesson/music-aqa/listening/1")
    print(f"  Browse URL: /browse/music-aqa")
    return 0


if __name__ == "__main__":
    sys.exit(main())
