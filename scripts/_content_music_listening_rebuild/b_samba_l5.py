# -*- coding: utf-8 -*-
"""music-edexcel / aos4-fusions / L5 -- Samba em Preludio, ELEMENTS walk.
Same recording as L4 (8vOkY94xjnY, 312 s) and the same verified pin times, one
card per element: texture, melody, rhythm, improvisation, harmony and tonality,
dynamics.
NOTE FOR REVIEW: the two source lessons disagreed about which instrument takes
the extended solo (L4 said acoustic guitar, L5 said acoustic bass guitar). That
cannot be settled by machine ear, so both decks now say 'an extended improvised
solo' without naming the instrument, and the bass's dual role is described from
what the source text does support: chord roots plus melodic dialogue with the
voice in the opening duet."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos4-fusions__L05"
d = Deck(lesson_id="b405f74e-2c10-4f3f-9c9d-ab2d93358720",
         subject="music-edexcel", unit="aos4-fusions", lesson_no=5,
         yt="8vOkY94xjnY", dur=312, track_label="Samba Em Preludio",
         credit="Official audio, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Esperanza Spalding: Samba Em Preludio (2008).")
TITLE = "Esperanza Spalding: Samba em Preludio — The Elements in Close-Up"

d.pins = [
    ("t1c1", 0,   "Texture",       "Two parts, and one performer playing both. Count what is actually sounding."),
    ("t1c2", 15,  "Melody",        "Long, flowing phrases in Portuguese, sung without force."),
    ("t1c3", 78,  "Rhythm",        "Syncopated chords under a smooth vocal line. The bossa nova fingerprint."),
    ("t1c4", 144, "Improvisation", "New melody invented over chords you have already heard."),
    ("t1c5", 214, "Harmony",       "A minor key, but the chords carry far more than three notes."),
    ("t1c6", 286, "Dynamics",      "Nothing is ever loud. Listen to how the track gets smaller instead."),
]

d.add_cover(
  "The same track, element by element",
  [
    "Esperanza Spalding&rsquo;s 2008 recording of a 1962 song by Baden Powell and Vinicius de Moraes: a %s in a "
    "minor key, sung in Portuguese, for voice with acoustic bass guitar, acoustic guitar and strings."
    % dfn("bossa nova", "A gentle Brazilian style blending samba rhythm with cool jazz harmony"),
    "The previous lesson followed the arch from the solo bass to the thinned close. This one stops six times, once "
    "for each %s the exam sets questions on here: texture, melody, rhythm, improvisation, harmony and dynamics."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Texture", "1 &middot; Two parts, one musician",
  "Count the parts: bass, then voice, and nothing else. %s That is a %s. The bass is doing two jobs at once, "
  "supplying the chord roots that hold the harmony and answering the singer with shaped melodic phrases. Naming that "
  "double function is worth more than calling the opening sparse."
  % (d.ref(1), dfn("duet texture", "A texture made by exactly two performing parts sounding together")),
  "the bass moving from harmony to melody and back. One performer, two musical roles.")

d.add_statement(2, "Melody", "2 &middot; The line",
  "The vocal line moves in long, flowing phrases, mostly by step, with very little decoration. %s Even once the "
  "tempo arrives it keeps a %s freedom, leaning slightly ahead of or behind the beat. The Portuguese lyric is kept "
  "from the original, which is what anchors the recording in its Brazilian identity."
  % (d.ref(2), dfn("rubato", "Flexible tempo, speeding up or slowing down for expressive effect")),
  "how unhurried the phrasing is. Describe it as lyrical and flexible, not as slow.")

d.add_statement(3, "Rhythm", "3 &middot; Off the beat, on purpose",
  "The accompaniment now plays a repeating chordal pattern, and its accents fall slightly off the main beats. %s "
  "That %s is the rhythmic fingerprint of Brazilian popular music, and this way of playing it is called %s. Above it "
  "the vocal stays smooth and long-noted, so tight and relaxed rhythms run at the same time."
  % (d.ref(3), dfn("syncopation", "Accents placed off the main beats, creating a lilting or unsettled feel"),
     dfn("comping", "Playing repeated chordal rhythmic patterns to support a melody")),
  "the gap between a busy accompaniment and an unhurried voice. That contrast is the bossa nova style itself.")

d.add_statement(4, "Improvisation", "4 &middot; Invented on the spot",
  "The singing stops and an extended solo takes over. %s The soloist %s: the melody is being invented now, over the "
  "chord pattern the song has already set up. That procedure comes from jazz, not from the Brazilian song tradition, "
  "and it is the clearest single sign of the fusion."
  % (d.ref(4), dfn("improvises", "Creates and performs musical ideas spontaneously rather than from a written part")),
  "the familiar chords continuing underneath an unfamiliar tune. Say what stays fixed as well as what is invented.")

d.add_statement(5, "Harmony", "5 &middot; Chords with extra notes",
  "The key is minor, which gives the song its reflective, bittersweet colour. %s The chords are not plain triads "
  "though: bossa nova and jazz both favour %s, sevenths and ninths and more, voiced smoothly so that the added notes "
  "colour rather than clash. Spalding keeps that sophistication instead of simplifying it."
  % (d.ref(5), dfn("extended chords", "Chords with notes added above the basic triad, such as sevenths and ninths")),
  "chords that sound richer than three notes. Name the tonality and the extension together.")

d.add_statement(6, "Dynamics", "6 &middot; Restraint as a style",
  "Across five minutes nothing is ever pushed. %s The dynamic range is narrow and the vocal stays soft and unforced "
  "even when the ensemble is at its fullest, and the track ends by removing layers rather than by getting louder. "
  "Set that beside Release, where the same fusion problem is solved by density."
  % d.ref(6),
  "how little the volume changes. Restraint here is a deliberate style, not a lack of intensity.")

d.add_checklist(
  "Melody: long, flowing, largely stepwise phrases sung in Portuguese with rubato freedom. Harmony and tonality: "
  "minor key with extended jazz chords, sevenths and ninths. Texture: a duet of voice and acoustic bass guitar, "
  "thickening slightly with comping and strings and thinning again. Rhythm: rubato at first, then syncopated bossa "
  "nova comping under a smooth vocal line. Improvisation: an extended solo invented over the established harmony. "
  "Dynamics: consistently soft and unforced, with the close made by subtraction.",
  "Attach each term to a moment. &ldquo;It is syncopated&rdquo; earns little; &ldquo;the chordal accompaniment "
  "accents just off the beat while the vocal line stays smooth above it&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>The most useful comparison in this area of study is with Release. Both fuse traditions, but by "
            "opposite means: Spalding uses a duet, acoustic timbres and restraint, while Afro Celt Sound System use "
            "dense layering, electronic production and volume. Make the comparison concrete with named features on "
            "both sides rather than saying one is calmer than the other.</p>")
conclusion = ("<p>You can now name each element of this recording and point to where it is audible: a two-part "
              "texture with the bass doing two jobs, a long lyrical vocal line, syncopated comping under smooth "
              "singing, an improvised solo over fixed harmony, extended chords in a minor key, and a dynamic range "
              "that never rises. That completes the Fusions area of study.</p>")
description = ("Six numbered stops in Samba em Preludio, one for each element: texture, melody, rhythm, "
               "improvisation, harmony and dynamics.")

flashcards = [
  {"q": "What does rubato mean and where is it used in Samba em Preludio?",
   "a": "Flexible, free tempo without a strict pulse. It is used in the opening voice-and-bass duet, and the vocal keeps some of that freedom even after the tempo settles."},
  {"q": "What is the centrepiece improvised section of the recording?",
   "a": "An extended solo in which the soloist improvises new melodic material over the harmonic pattern already established by the song."},
  {"q": "What two musical roles does the acoustic bass guitar play in the opening duet?",
   "a": "It supplies the harmony by outlining the chord roots, and it answers the voice with shaped melodic phrases, so it accompanies and converses at the same time."},
  {"q": "What harmonic features show the jazz influence in this piece?",
   "a": "Extended chords such as sevenths and ninths, smoothly voiced within a minor tonality, kept from the bossa nova tradition rather than simplified."},
  {"q": "How does the texture of Samba em Preludio differ from Release?",
   "a": "Samba em Preludio is a sparse duet that thickens only slightly and thins again, while Release builds a dense, layered ensemble texture using many instruments and electronic production."},
  {"q": "How are dynamics used in this recording?",
   "a": "The range stays narrow. The vocal is soft and unforced even at the fullest point, and the track closes by removing layers rather than by growing louder."},
]

practice = [
  {"text": "Name the two parts heard in the opening rubato section of Samba em Preludio.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for voice and acoustic bass guitar."},
  {"text": "Describe the rhythmic relationship between the comping pattern and the vocal line once the tempo is established.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: the accompaniment is syncopated, accenting off the main beats. One mark: the vocal line moves in smoother, longer notes above it, so tight and relaxed rhythms sound together."},
  {"text": "Explain the two musical roles played by the acoustic bass guitar in the opening duet.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: it outlines the chord roots, supplying the harmony. One mark: it plays shaped melodic phrases that answer the voice. One mark: with only two parts sounding, that dual role is what makes the thin texture sound complete."},
  {"text": "Identify the tonality of Samba em Preludio and state one effect this has on the mood.", "marks": 2, "kind": "Identification",
   "mark_scheme": "One mark for minor. One mark for a reflective, wistful or bittersweet mood."},
  {"text": "Explain how Samba em Preludio combines jazz and Brazilian musical elements, referring to specific musical features.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: Brazilian, the Portuguese lyric and bossa nova song style. One mark: Brazilian, syncopated comping. One mark: jazz, extended chords such as sevenths and ninths. One mark: jazz, an extended improvised solo over the established harmony."},
  {"text": "Compare the texture of Samba em Preludio with the texture of Release.", "marks": 4, "kind": "Comparison",
   "mark_scheme": "One mark: Samba em Preludio opens as a duet and stays comparatively sparse. One mark: Release builds a dense, layered texture over a drone. One mark: Spalding's layers are acoustic and few, while Afro Celt Sound System add loops and programmed beats. One mark: a clear comparative statement that both achieve fusion, by opposite textural means."},
]

kcs = [
  {"q": "Who composed the original music for Samba em Preludio?",
   "options": ["Baden Powell", "Antonio Carlos Jobim", "Esperanza Spalding", "Vinicius de Moraes"], "correct": 0},
  {"q": "What instrument does Esperanza Spalding play while singing on this recording?",
   "options": ["Guitar", "Piano", "Acoustic bass guitar", "Saxophone"], "correct": 2},
  {"q": "How does the piece begin?",
   "options": ["With a full band groove", "In free time (rubato) as a duet", "With an electronic drum loop", "With a solo guitar cadenza"], "correct": 1},
  {"q": "What creates the bossa nova feel in the accompaniment?",
   "options": ["A syncopated comping pattern", "A strict march rhythm", "A slow waltz pulse", "Silence between phrases"], "correct": 0},
  {"q": "Which best describes the fusion in Samba em Preludio compared with Release?",
   "options": ["Both use identical dense electronic textures", "Samba em Preludio is sparse and intimate; Release is dense and layered", "Samba em Preludio uses no improvisation at all", "Release uses only acoustic instruments"], "correct": 1},
]

pq, kc, fc = build_questions(BACKUP, practice, kcs, flashcards)
errs, warns = d.verify(content, exam_tip + conclusion)
for o, lbl in ((pq, "practice"), (kc, "kc"), (fc, "flashcards")):
    check_plain(o, lbl, errs)
if len(description) > 160:
    errs.append("description %d chars" % len(description))
print("cards", len(d.cards), "| narration ids", d._n, "| chars", len(content), "| desc", len(description))
for w in warns:
    print("WARN", w)
if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print("verify OK")
payload = {"title": TITLE, "content_html": content, "exam_tip_html": exam_tip, "conclusion_html": conclusion,
           "description": description, "flashcard_questions": fc, "practice_questions": pq,
           "knowledge_checks": kc, "narration_manifest": None}
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "samba_l5.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
