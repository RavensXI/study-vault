# -*- coding: utf-8 -*-
"""music-edexcel / aos4-fusions / L2 -- Release, STRUCTURAL walk.
Video U6vkehDfYXI (official audio), 7:37 = 457 s.
Pin times: 0:00 first sound (3/3), 0:49 the full groove locks in (3/3 in the
targeted round), 1:19 the voice first sings (2/3), 2:33 the sung line stops and
an instrumental passage takes over (3/3 in the targeted round), 4:55 the voice
returns (2/3), 5:52 the last section begins (2/3). The track ends at 7:16
(3/3), described inside card 6 rather than pinned.
The old lesson's two embedded reference videos are dropped."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos4-fusions__L02"
d = Deck(lesson_id="e908a094-9ce0-4eb9-96e7-baf033d34578",
         subject="music-edexcel", unit="aos4-fusions", lesson_no=2,
         yt="U6vkehDfYXI", dur=457, track_label="Release",
         credit="Official audio, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Afro Celt Sound System: Release (1999).")
TITLE = "Afro Celt Sound System: Release — Guided Listening"

d.pins = [
    ("t1c1", 0,   "Drone",        "A sustained drone opens the space. Colour, not yet pulse."),
    ("t1c2", 49,  "The groove",   "The programmed beat and percussion lock in and the track starts to move."),
    ("t1c3", 79,  "The voice",    "The keening, ornamented vocal line enters over the layers already running."),
    ("t1c4", 153, "Instruments",  "The voice steps back and the two traditions talk to each other."),
    ("t1c5", 295, "The voice returns", "Layers rebuild around the singer for the second half."),
    ("t1c6", 352, "The last build", "Everything in at once, then a slow fade rather than a final chord."),
]

d.add_cover(
  "Afro Celt Sound System: Release",
  [
    "The title track of the 1999 album <em>Volume 2: Release</em>. Three traditions at once: Irish traditional "
    "instruments, West African %s instruments and electronic dance production. There is no verse and chorus here; "
    "the track is built by %s and taken apart again."
    % (dfn("griot", "The hereditary West African tradition of musician-storytellers"),
       dfn("layering", "Adding parts one at a time so the texture thickens cumulatively")),
    "The band formed in the mid-1990s around the producer and guitarist Simon Emmerson, with close links to Peter "
    "Gabriel&rsquo;s Real World Studios and the WOMAD festival. Fusion is not a side effect of that history: it is "
    "the band&rsquo;s whole purpose.",
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Drone", "1 &middot; Atmosphere before pulse",
  "Nothing here is in time yet. %s A sustained synthesiser %s holds a fixed note underneath a few exposed fragments, "
  "and that is the whole texture. Drones belong to Irish traditional music and to West African and Asian traditions "
  "alike, so the track opens on ground both sides already share."
  % (d.ref(1), dfn("drone", "A sustained note or narrow group of notes held fixed while other material moves above")),
  "how little is playing. This sparseness is the measure against which everything later is judged.")

d.add_statement(2, "The groove", "2 &middot; The engine starts",
  "Percussion arrives and the track finds its pulse. %s Underneath sits a %s, made in the studio rather than played "
  "live, which will not change for the rest of the piece. It is the anchor: however much the other rhythmic layers "
  "pull against each other, this keeps them locked together."
  % (d.ref(2), dfn("programmed beat", "A rhythmic pulse created electronically rather than played in real time")),
  "the steady electronic pulse under the hand percussion. Say &lsquo;programmed&rsquo;, not &lsquo;drum kit&rsquo;.")

d.add_statement(3, "The voice", "3 &middot; The lament",
  "The voice enters over layers that are already running, which is why it feels like an arrival rather than a start. "
  "%s The style is close to %s, the unaccompanied Irish tradition of highly ornamented, rhythmically free singing, "
  "and the intense wailing tone is described as %s. It works as a lament, not a pop hook."
  % (d.ref(3), dfn("sean-n&oacute;s", "An unaccompanied, highly ornamented Irish vocal tradition with free rhythm"),
     dfn("keening", "An intense, wailing vocal quality associated with lament")),
  "ornament on almost every long note. Name the style, and say the vocal is a lament rather than a chorus.")

d.add_statement(4, "Instruments", "4 &middot; The traditions meet",
  "With the voice out of the way you can hear the fusion working. %s Irish %s and whistle offer a phrase; the West "
  "African %s or drums answer or overlap it. Nobody plays the same tune together: the traditions keep their own "
  "identity and pass material between them over the programmed pulse."
  % (d.ref(4), dfn("uilleann pipes", "Irish bagpipes inflated by a bellows worked with the elbow, giving drone and ornamented melody"),
     dfn("kora", "A twenty-one-string West African harp-lute plucked with thumbs and forefingers")),
  "phrases handed from one tradition to the other. That dialogue is the fusion, not the fact of playing at once.")

d.add_statement(5, "The voice returns", "5 &middot; Built back up",
  "The singer comes back and the layers rebuild around her. %s Notice that nothing new has been composed: the same "
  "loops, drones and patterns are simply muted and reintroduced. That is dance-music architecture, a %s followed by "
  "a rebuild, applied to acoustic folk material."
  % (d.ref(5), dfn("breakdown", "A section where most layers drop out, thinning the texture before it is rebuilt")),
  "which layer returns first. Being able to name the order of entries is worth more than calling the track busy.")

d.add_statement(6, "The last build", "6 &middot; Everything at once",
  "The final section brings every strand back together: Celtic melody, West African cross-rhythm and the electronic "
  "engine underneath. %s The track does not end on a decisive chord; it fades. That is a production decision as much "
  "as a musical one, and it is typical of the dance tradition this band draws on."
  % d.ref(6),
  "the density at its greatest, then the fade. Compare it directly with the opening drone you heard first.")

d.add_checklist(
  "Genre: fusion of Irish traditional music, West African griot music and electronic dance production. Forces: "
  "uilleann pipes, whistle, fiddle and accordion; kora, talking drum and djembe; voice; synthesisers, loops and "
  "programmed beats. Structure: a layer-by-layer build, a breakdown, a rebuild and a fade, with no verse or chorus. "
  "Texture: drone foundation with melodic dialogue above it. Rhythm: Irish lilt and West African cross-rhythm over a "
  "steady programmed pulse. Context: 1999, from Volume 2: Release, made at Real World Studios.",
  "Pair each instrument with its tradition and its moment. &ldquo;There are lots of instruments&rdquo; earns little; "
  "&ldquo;the drone underpins the texture while whistle and kora exchange phrases above it&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Listen for the order in which things enter, and learn it. Saying &lsquo;the drone and a melodic "
            "fragment open the track, then the programmed beat and percussion, then the voice&rsquo; shows "
            "structural understanding. Saying the track sounds busy shows none. The same applies to the breakdown: "
            "name which layer drops out and which returns first.</p>")
conclusion = ("<p>You can now follow Release as a build: drone, groove, voice, instrumental dialogue, rebuild and "
              "final fade, with the programmed pulse holding it together throughout. The next lesson takes the same "
              "recording element by element &mdash; the drone as harmony, the two rhythmic traditions, the vocal and "
              "melodic writing, the instruments of each side, the layered texture and the technology itself.</p>")
description = ("Follow Afro Celt Sound System's Release through six landmarks, from the opening drone to the final "
               "build and fade.")

flashcards = [
  {"q": "What are uilleann pipes and how are they played?",
   "a": "Irish bagpipes inflated by a bellows strapped to the elbow rather than blown by mouth, producing a continuous drone plus a highly ornamented melody."},
  {"q": "What is a talking drum?",
   "a": "A West African hourglass-shaped drum whose pitch is changed by squeezing the cords along its sides, so it can imitate the rise and fall of speech."},
  {"q": "What is the kora?",
   "a": "A twenty-one-string West African harp-lute, plucked with the thumbs and forefingers, producing rippling, cascading patterns."},
  {"q": "How does Release build structurally?",
   "a": "It grows layer by layer from a sparse drone through added percussion, melodic instruments and voice to a dense full groove, then drops to a breakdown before rebuilding and fading."},
  {"q": "What is sean-nos singing and how does it relate to keening?",
   "a": "An unaccompanied, highly ornamented Irish vocal tradition with free rhythm. Keening describes the intense, wailing emotional tone heard in that style."},
  {"q": "Which three traditions are fused in Release?",
   "a": "Irish traditional music, West African griot music, and electronic dance-music production. Naming all three, not just two, is the point of the set work."},
]

practice = [
  {"text": "Name one instrument from the Irish traditional side of Release and one from the West African side.", "marks": 2, "kind": "Identification",
   "mark_scheme": "One mark for a Celtic instrument such as uilleann pipes, fiddle, whistle or accordion. One mark for a West African instrument such as kora, talking drum or djembe."},
  {"text": "Describe how the uilleann pipes are typically played and the sound they produce.", "marks": 3, "kind": "Description",
   "mark_scheme": "One mark: inflated by a bellows worked with the elbow rather than blown by mouth. One mark: they sound a continuous drone. One mark: the melodic line is highly ornamented, with rolls, cuts and grace notes."},
  {"text": "Describe the order in which material enters at the start of Release.", "marks": 3, "kind": "Description",
   "mark_scheme": "One mark: a sustained drone and exposed fragments open the track with no clear pulse. One mark: percussion and a programmed beat enter and establish the groove. One mark: melodic instruments and then the voice are layered on top, so the texture thickens cumulatively."},
  {"text": "What term describes the intense, wailing quality often heard in the sean-nos vocal style used in Release?", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for keening, or an accurate equivalent description."},
  {"text": "Compare the opening of Release with its later full-groove section in terms of texture.", "marks": 3, "kind": "Comparison",
   "mark_scheme": "One mark: the opening is sparse and atmospheric, drone plus a fragment. One mark: the later section is dense and multi-layered, with both traditions and the electronic engine sounding at once. One mark: a clear statement of the contrast, and that the change happens by accumulation rather than by moving to a new section."},
  {"text": "Explain why Release can be described as a fusion of more than just two folk traditions.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: Irish traditional instruments and melodic style. One mark: West African griot instruments and rhythmic patterns. One mark: electronic dance production, with drones, loops and programmed beats. One mark: an explanation that the production is a creative element in its own right, shaping structure and texture, not merely a recording method."},
]

kcs = [
  {"q": "Which instrument is a bellows-blown Irish bagpipe played while seated?",
   "options": ["Uilleann pipes", "Kora", "Djembe", "Talking drum"], "correct": 0},
  {"q": "Which West African instrument is a twenty-one-string harp-lute?",
   "options": ["Talking drum", "Kora", "Djembe", "Accordion"], "correct": 1},
  {"q": "What is the overall structural shape of Release?",
   "options": ["Strict verse-chorus form", "A gradual build from sparse atmosphere to full groove, with a breakdown", "Theme and variations", "Sudden alternation between two contrasting sections"], "correct": 1},
  {"q": "What vocal tradition is associated with the guest vocal in Release?",
   "options": ["Bel canto opera", "Sean-nos singing", "Gospel choir singing", "Yodelling"], "correct": 1},
  {"q": "What is heard first, before the pulse arrives?",
   "options": ["A full drum groove", "A sustained drone with exposed fragments", "A kora solo", "A vocal chorus"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "release_l2.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
