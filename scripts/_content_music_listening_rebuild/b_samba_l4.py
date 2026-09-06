# -*- coding: utf-8 -*-
"""music-edexcel / aos4-fusions / L4 -- Samba em Preludio, STRUCTURAL walk.
Video 8vOkY94xjnY (official audio), 5:12 = 312 s.
Pin times: 0:00 the bass alone (3/3), 0:15 the voice joins (3/3), 1:18 the
accompaniment enters and the music settles into tempo (guitar 3/3, strings 2/3
at the same moment), 2:24 the extended instrumental solo (3/3 in both rounds),
3:34 the voice returns (2/3), 4:46 the texture thins back (3/3). The track ends
at 5:04 (2/3), described inside card 6 rather than pinned.
The old lesson's two embedded Baden Powell videos are dropped."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos4-fusions__L04"
d = Deck(lesson_id="d8d5d20f-bde4-47ce-abb1-972d59e6b3c2",
         subject="music-edexcel", unit="aos4-fusions", lesson_no=4,
         yt="8vOkY94xjnY", dur=312, track_label="Samba Em Preludio",
         credit="Official audio, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Esperanza Spalding: Samba Em Preludio (2008).")
TITLE = "Esperanza Spalding: Samba em Preludio — Guided Listening"

d.pins = [
    ("t1c1", 0,   "Bass alone",   "Spalding opens alone on the acoustic bass guitar. Free time, no pulse yet."),
    ("t1c2", 15,  "The voice",    "The voice joins and the track becomes a duet: two parts, nothing else."),
    ("t1c3", 78,  "In tempo",     "Chordal accompaniment and sustained strings arrive, and the music finds its pulse."),
    ("t1c4", 144, "The solo",     "The singing stops and an extended improvised solo takes the centre of the track."),
    ("t1c5", 214, "The voice returns", "The song material comes back with the ensemble now filled out."),
    ("t1c6", 286, "The close",    "The accompaniment thins back towards the duet. The arch completes and fades."),
]

d.add_cover(
  "Esperanza Spalding: Samba em Preludio",
  [
    "Esperanza Spalding&rsquo;s 2008 recording, from the album <em>Esperanza</em>, of a song written in 1962 by the "
    "Brazilian guitarist Baden Powell and the poet Vinicius de Moraes. A minor key, a Portuguese lyric, and a %s "
    "arranged for voice with acoustic bass guitar, acoustic guitar and strings."
    % dfn("bossa nova", "A gentle Brazilian style blending samba rhythm with cool jazz harmony, popularised around 1960"),
    "It counts as a %s because a Brazilian song is filtered through the harmony, instrumentation and improvisatory "
    "freedom of jazz. Spalding is a bassist and a singer at once, and the arrangement is built around that double "
    "identity."
    % dfn("fusion", "Music that combines elements from two or more distinct genres or traditions"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Bass alone", "1 &middot; One instrument, no pulse",
  "The track begins with the acoustic bass guitar on its own, played %s. %s There is no fixed beat: the tempo is "
  "%s, flexing as the phrase requires. For these few seconds the bass line is the only harmony there is, which is a "
  "striking way to open a song about to be sung."
  % (dfn("pizzicato", "Plucked rather than bowed"), d.ref(1),
     dfn("rubato", "Flexible tempo, speeding up or slowing down for expressive effect")),
  "the absence of a beat. Say &lsquo;free time&rsquo; or &lsquo;rubato&rsquo;, not &lsquo;slow&rsquo;.")

d.add_statement(2, "The voice", "2 &middot; A duet, and only a duet",
  "The voice enters and the texture is complete: two parts. %s That is a %s, and it is worth naming precisely rather "
  "than calling the sound thin. The bass alternates between chord roots and shaped melodic phrases that answer the "
  "singer, so the two lines converse rather than one accompanying the other."
  % (d.ref(2), dfn("duet texture", "A texture made by exactly two performing parts sounding together")),
  "the bass answering the voice. Both parts are Spalding: the exposure is the point of the opening.")

d.add_statement(3, "In tempo", "3 &middot; The groove arrives",
  "Chordal accompaniment and sustained string colour arrive together and the music locks into tempo. %s The chordal "
  "pattern is bossa nova %s: light, syncopated chords that echo the original guitar accompaniment without taking it "
  "over. The Brazilian roots stay audible as the arrangement grows."
  % (d.ref(3), dfn("comping", "Playing chordal rhythmic patterns to support a melody, standard in jazz and bossa nova")),
  "the exact moment a pulse appears. The move from rubato into tempo is a favourite short-answer question.")

d.add_statement(4, "The solo", "4 &middot; The improvised centre",
  "The singing stops and an extended instrumental solo takes over. %s The soloist %s over the harmonic pattern the "
  "song has already established, which is a jazz procedure applied to a Brazilian song form. Nothing new is "
  "introduced harmonically; the interest is entirely in what is invented above it."
  % (d.ref(4), dfn("improvises", "Creates and performs musical ideas spontaneously rather than from a written part")),
  "the same chord pattern continuing underneath. That is what makes it an improvised solo rather than a new section.")

d.add_statement(5, "The voice returns", "5 &middot; The song comes back",
  "The solo ends and the song material returns with the ensemble filled out. %s Notice how little Spalding changes "
  "in her delivery: even with more instruments around her the vocal stays soft and unforced. That restraint is "
  "characteristic both of bossa nova performance and of her own style."
  % d.ref(5),
  "the fuller accompaniment against an unchanged vocal. Restraint is a stylistic choice, not a lack of power.")

d.add_statement(6, "The close", "6 &middot; Back to two",
  "The accompaniment thins away and the track returns towards the texture it began with. %s That gives the whole "
  "recording an %s: duet, ensemble, solo, ensemble, duet. It is looser than verse-chorus form, and the looseness is "
  "the jazz influence on the shape as much as on the notes."
  % (d.ref(6), dfn("arch", "A shape that builds up and then reduces again, returning near its starting point")),
  "how close the ending is to the opening. Describing the shape as an arch is worth more than listing the sections.")

d.add_checklist(
  "Genre: fusion of Brazilian bossa nova with jazz. Forces: voice, acoustic bass guitar, acoustic guitar and "
  "strings. Key: minor. Structure: a free rubato duet introduction, a section in tempo, an extended improvised solo, "
  "a return of the song and a thinned close, an arch rather than verse-chorus form. Texture: duet, thickening by "
  "addition and thinning again. Rhythm: rubato, then syncopated bossa nova comping under a smooth vocal line. "
  "Context: written in 1962 by Baden Powell and Vinicius de Moraes, recorded by Spalding in 2008.",
  "Say what changes and when. &ldquo;The texture builds&rdquo; earns little; &ldquo;the opening duet becomes a full "
  "ensemble when the chordal accompaniment and strings enter and the music settles into tempo&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>The transition from the free opening into a steady tempo is one of the most commonly set short "
            "questions on this track, so learn to name it exactly: rubato duet of voice and acoustic bass guitar, "
            "then chordal comping and strings arriving together as the pulse is established. Naming the texture as a "
            "duet, rather than calling it thin or quiet, is worth a mark on its own.</p>")
conclusion = ("<p>You can now follow the recording as an arch: bass alone, duet, the arrival of tempo and "
              "accompaniment, the improvised solo, the return of the song and the thinning close. The next lesson "
              "takes the same recording element by element &mdash; texture, melody, rhythm, improvisation, harmony "
              "and dynamics &mdash; and sets it against Release.</p>")
description = ("Follow Esperanza Spalding's Samba em Preludio through six landmarks, from the solo bass opening to "
               "the thinned close.")

flashcards = [
  {"q": "Who wrote the original Samba em Preludio and in what year?",
   "a": "Baden Powell wrote the music and Vinicius de Moraes the words, in 1962."},
  {"q": "What two parts open Spalding's recording in a duet texture?",
   "a": "Voice and acoustic bass guitar, both performed by Spalding herself, in free rubato time."},
  {"q": "What term describes the syncopated chordal accompaniment style of bossa nova?", "a": "Comping."},
  {"q": "What tonality is Samba em Preludio set in, and what mood does this create?",
   "a": "A minor key, creating a reflective, bittersweet mood."},
  {"q": "Describe the overall shape of Spalding's recording.",
   "a": "An arch: a free rubato duet, then the ensemble and a steady tempo, an extended improvised solo, a return of the song, and a thinning back towards the duet at the close."},
  {"q": "Why is this recording classed as a fusion?",
   "a": "A Brazilian bossa nova song, with its Portuguese lyric and syncopated feel, is filtered through jazz harmony, jazz instrumentation and improvisation."},
]

practice = [
  {"text": "Identify the two parts that open Spalding's recording of Samba em Preludio.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for voice and acoustic bass guitar."},
  {"text": "Name the original songwriters credited with writing Samba em Preludio in 1962.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for Baden Powell and Vinicius de Moraes."},
  {"text": "Describe how the texture develops across the recording from the opening to the middle of the track.", "marks": 3, "kind": "Description",
   "mark_scheme": "One mark: the bass plays alone, then the voice joins to make a duet. One mark: chordal comping and sustained strings enter together and the music settles into tempo. One mark: the texture is fuller for the solo and the return, then thins back towards the duet at the close."},
  {"text": "Explain how this recording can be described as a fusion of styles.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the Brazilian bossa nova song survives intact, with Portuguese lyric, minor key and syncopated comping. One mark: jazz supplies the instrumentation, the extended harmony and the improvised solo. One mark: Spalding's double role as bassist and singer is itself part of the fusion."},
  {"text": "Explain the effect of the minor tonality and rubato phrasing on the character of the piece.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the minor key gives a reflective, bittersweet colour. One mark: rubato removes a strict pulse, so phrases breathe. One mark: together they create the intimate, unhurried lyricism typical of both bossa nova and Spalding's own style."},
  {"text": "Discuss how Spalding's arrangement both preserves and transforms features of the original bossa nova song.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: preserved, the Portuguese lyric and the minor key. One mark: preserved, the syncopated bossa nova comping and its harmonic language. One mark: transformed, the opening becomes a voice and bass duet rather than solo guitar. One mark: transformed, added strings, jazz instrumentation and an extended improvised solo reshape the song for a jazz audience."},
]

kcs = [
  {"q": "Who originally wrote Samba em Preludio in 1962?",
   "options": ["Antonio Carlos Jobim and Joao Gilberto", "Baden Powell and Vinicius de Moraes", "Stan Getz and Astrud Gilberto", "Esperanza Spalding and Wayne Shorter"], "correct": 1},
  {"q": "What texture opens Spalding's recording of Samba em Preludio?",
   "options": ["Full orchestral texture", "Solo unaccompanied voice", "A duet between voice and acoustic bass guitar", "A guitar and drums duo"], "correct": 2},
  {"q": "What happens when the chordal accompaniment enters?",
   "options": ["The music settles into a steady tempo", "The key changes to the major", "The voice stops for the rest of the track", "The tempo becomes freer"], "correct": 0},
  {"q": "What is the overall tonality of the piece?",
   "options": ["Major key throughout", "Minor key", "Atonal", "Modal with no clear key centre"], "correct": 1},
  {"q": "Which genre is bossa nova generally considered to be a blend of?",
   "options": ["Rock and blues", "Samba rhythms and cool jazz harmony", "Classical minuet and folk song", "Reggae and calypso"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "samba_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
