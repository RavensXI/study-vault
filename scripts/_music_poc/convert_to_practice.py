"""Convert the music-aqa PoC lesson from article format to practice format.

Practice format mirrors the structure used by Maths / English Lang /
Languages / Geography Skills:
- A passage (here: a brief intro + native HTML5 audio player) lives
  in `practice_data.passages[]`.
- Problems are tiered (bronze/silver/gold) and reference the passage by id.
- Each problem uses input_type "multiple_choice" so the existing renderer
  in practice.html handles it without code changes.
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
LESSON_ID = "35e3c439-5e65-4819-886c-84076dee0357"
SUBJECT_ID = "505cc121-7381-458c-aa5b-5bb5f1152786"

PASSAGE = {
    "id": "mozart-40-mvt1",
    "label": "Mozart, Symphony No. 40 in G minor, K. 550 — I. Molto allegro",
    "audio_url": AUDIO_URL,
    "text": (
        '<div style="text-align: center;">'
        '<p style="font-style: normal; font-family: Inter, sans-serif; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 1rem;">'
        'Mozart, <em>Symphony No. 40 in G minor</em>, K. 550<br>'
        'I. Molto allegro &middot; 5 min 59 s'
        '</p>'
        f'<audio controls preload="metadata" src="{AUDIO_URL}" style="width: 100%; max-width: 480px; margin: 0.5rem auto;"></audio>'
        '<p style="font-size: 0.78rem; color: var(--text-muted); font-style: italic; margin-top: 1rem;">'
        'Recording: Musopen Symphony (public domain). Pause, replay, and scrub to the timestamp each question references.'
        '</p>'
        '</div>'
    ),
}

METHOD_CARD = {
    "title": "What to listen for",
    "content": (
        "<p>Before tackling the questions, listen to the whole movement once without pausing &mdash; just absorb the shape.</p>"
        "<p>On a second listen, focus on these three things:</p>"
        "<ul>"
        "<li><strong>The opening texture.</strong> The piece doesn't begin with the main melody. Lower strings (violas, divided into two parts) play a quiet, restless accompaniment first; the violins enter with the famous \"sighing\" theme on top.</li>"
        "<li><strong>The mood.</strong> Listen for the descending semitone shape that gives the theme its anxious quality &mdash; characteristic of the <em>Sturm und Drang</em> (storm-and-stress) style.</li>"
        "<li><strong>The development</strong> (around 2:30&ndash;3:30). Mozart writes a passage that touches every chromatic note <em>except</em> the tonic G itself, which destabilises the home key dramatically.</li>"
        "</ul>"
    ),
    "steps": [
        "Play the recording all the way through once with no questions in front of you.",
        "Read each question stem before replaying its referenced section.",
        "Use the audio scrubber to jump to specific timestamps.",
        "If the question gives a key term like 'sonata form' or 'tonic', open the glossary in the methods card to ground yourself before answering.",
    ],
}

EXAM_CONTEXT = {
    "paper": "Listening",
    "marks": "varies (typically 1–6 marks per question)",
    "frequency": "Every listening paper",
}

PROBLEM_BANK = {
    "bronze": [
        {
            "input_type": "multiple_choice",
            "passage_id": "mozart-40-mvt1",
            "question": "Listen to the opening 30 seconds. What is the home key of this piece?",
            "options": ["G major", "G minor", "D minor", "B-flat major"],
            "solutions": [1],
            "explanation": "The work is universally catalogued as Mozart's Symphony No. 40 'in G minor', K. 550. The sustained minor tonality through the opening confirms the key. D minor is the dominant minor (a plausible distractor if you only feel the tension); B-flat major is the relative major and features later in the exposition but is not the home key.",
        },
        {
            "input_type": "multiple_choice",
            "passage_id": "mozart-40-mvt1",
            "question": "Listen to the very opening, before the main melody enters. Which family of instruments plays the accompaniment first?",
            "options": ["Woodwind", "Brass", "Strings", "Full orchestra together"],
            "solutions": [2],
            "explanation": "Mozart begins, unusually, with the lower strings (the violas, divided into two parts) playing a quiet, pulsing accompaniment. The violins then enter with the main 'sighing' theme on top. Opening with accompaniment rather than melody was a bold gesture &mdash; later favoured by Romantic composers.",
        },
    ],
    "silver": [
        {
            "input_type": "multiple_choice",
            "passage_id": "mozart-40-mvt1",
            "question": "What feature of the violins' main theme contributes most to its anxious, restless mood?",
            "options": [
                "A falling shape with descending semitones (the 'sighing' figure)",
                "A confident major-key marching rhythm",
                "A solo trumpet fanfare",
                "Long sustained whole notes throughout",
            ],
            "solutions": [0],
            "explanation": "The opening melody descends in 'sighing' semitones over an agitated string accompaniment. Britannica describes the character as 'plaintive sighs' in the Sturm und Drang style. The descending semitone is the single most testable feature of this opening.",
        },
        {
            "input_type": "multiple_choice",
            "passage_id": "mozart-40-mvt1",
            "question": "Mozart wrote two versions of this symphony. The 1788 original had no clarinets; in 1791 he revised it to add them. What is the most likely reason for the revision?",
            "options": [
                "The composer wanted to make the piece harder to play.",
                "Clarinets were only invented in 1791.",
                "An upcoming performance had clarinettists available, and Mozart wanted their warmer woodwind blend.",
                "Modern audiences prefer clarinets to oboes.",
            ],
            "solutions": [2],
            "explanation": "The revision added two clarinet parts and redistributed some woodwind lines so the oboes did not double the new clarinets. Mozart's likely motivation was a planned performance with clarinettists available; the warmer clarinet timbre also softens the oboe-led blend in the original. Clarinets had been around for decades by 1788 (Mozart wrote his Clarinet Quintet in 1789).",
        },
    ],
    "gold": [
        {
            "input_type": "multiple_choice",
            "passage_id": "mozart-40-mvt1",
            "question": "Listen to the section between roughly 2:30 and 3:30. This passage is from the development. How does Mozart destabilise the home key here?",
            "options": [
                "He stays firmly in G minor throughout, never modulating.",
                "He uses a chromatic passage that touches every note of the chromatic scale except the tonic G.",
                "He stops the orchestra entirely for ten seconds of silence.",
                "He has the brass section play a fanfare in C major.",
            ],
            "solutions": [1],
            "explanation": "Wikipedia describes this development passage as one in which 'every tone in the chromatic scale but one is played, strongly destabilising the key' &mdash; the omitted note is G, the tonic. By withholding the home note while saturating the other eleven, Mozart prevents the listener from grounding the music in any clear key, heightening tension before the recapitulation returns to G minor.",
        },
    ],
}

WORKED_EXAMPLES = [
    {
        "difficulty": "silver",
        "question": "Listen to the opening eight bars (roughly the first 15 seconds). Identify two features that establish the unsettled mood.",
        "steps": [
            "<strong>Step 1 &mdash; texture.</strong> Notice that the first thing you hear is NOT a melody. The lower strings (divided violas) play a soft, restless accompaniment. The melody only enters a moment later. Beginning with the accompaniment is unusual and immediately creates a feeling of music already in motion.",
            "<strong>Step 2 &mdash; melodic shape.</strong> When the violins enter with the main theme, listen to the contour: it falls. Specifically, it falls in semitones (small, narrow steps). The descending semitone is sometimes called a 'sigh' figure because it imitates the way a person's voice falls when sighing.",
            "<strong>Step 3 &mdash; key.</strong> The whole opening is firmly in G minor (the tonic). The minor key, plus the descending sigh figure, plus the agitated string accompaniment, are the three features that put this music squarely in the <em>Sturm und Drang</em> (storm-and-stress) tradition.",
            "<strong>Putting it together.</strong> A strong answer would name TWO of: the unusual opening with accompaniment first; the descending semitone (sigh) figure in the violins; the minor key tonality; the agitated string accompaniment; the soft (piano) dynamic. Each named feature scores 1 mark; linking each feature to the mood scores another mark.",
        ],
    },
]


def main():
    sb = get_client()

    # Build the practice_data blob
    practice_data = {
        "method_card": METHOD_CARD,
        "exam_context": EXAM_CONTEXT,
        "passages": [PASSAGE],
        "problem_bank": PROBLEM_BANK,
        "worked_examples": WORKED_EXAMPLES,
    }

    # Update the lesson row: wipe content_html (article relic), set practice_data
    sb.table('lessons').update({
        "content_html": None,
        "practice_questions": None,
        "practice_data": practice_data,
    }).eq('id', LESSON_ID).execute()
    print(f"  lesson {LESSON_ID} converted to practice format")

    # Mark the unit as practice in subjects.settings.practice_units
    sub = sb.table('subjects').select('settings').eq('id', SUBJECT_ID).execute().data[0]
    settings = sub['settings'] if isinstance(sub['settings'], dict) else json.loads(sub['settings'])
    settings.setdefault('practice_units', [])
    if 'listening' not in settings['practice_units']:
        settings['practice_units'].append('listening')
    sb.table('subjects').update({'settings': settings}).eq('id', SUBJECT_ID).execute()
    print(f"  subject settings: practice_units = {settings['practice_units']}")

    # Counts
    counts = {tier: len(PROBLEM_BANK[tier]) for tier in ('bronze', 'silver', 'gold')}
    print(f"  problem counts: {counts} (total {sum(counts.values())})")
    print()
    print("  Test URL: /practice/music-aqa/listening/1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
