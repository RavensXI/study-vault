# -*- coding: utf-8 -*-
"""music-edexcel / aos4-fusions / L3 -- Release, ELEMENTS walk.
Same recording as L2 (U6vkehDfYXI, 457 s) and the same verified pin times, one
card per element: the drone as harmony, rhythm, melody and voice, instruments
of each tradition, texture, and technology."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos4-fusions__L03"
d = Deck(lesson_id="6e32afcb-325c-4133-900c-b707784b162f",
         subject="music-edexcel", unit="aos4-fusions", lesson_no=3,
         yt="U6vkehDfYXI", dur=457, track_label="Release",
         credit="Official audio, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Afro Celt Sound System: Release (1999).")
TITLE = "Afro Celt Sound System: Release — The Elements in Close-Up"

d.pins = [
    ("t1c1", 0,   "Harmony",    "A fixed note underneath everything. No chord progression is driving this track."),
    ("t1c2", 49,  "Rhythm",     "Two rhythmic traditions pulling gently against one steady electronic pulse."),
    ("t1c3", 79,  "Melody",     "Ornament on almost every note, in the voice and in the pipes alike."),
    ("t1c4", 153, "Instruments", "Name them: which side of the fusion does each one come from?"),
    ("t1c5", 295, "Texture",    "Layers returning one at a time. Count them as they arrive."),
    ("t1c6", 352, "Technology", "Loops, samples and processing. The studio is playing too."),
]

d.add_cover(
  "The same track, element by element",
  [
    "Afro Celt Sound System&rsquo;s title track from <em>Volume 2: Release</em> (1999): Irish traditional "
    "instruments, West African %s instruments and electronic dance production, built by layering rather than into "
    "verses and choruses."
    % dfn("griot", "The hereditary West African tradition of musician-storytellers"),
    "The previous lesson followed the build from end to end. This one stops six times, once for each %s the exam "
    "sets questions on here: harmony, rhythm, melody, instrumentation, texture and technology."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Harmony", "1 &middot; A fixed foundation",
  "There is no chord sequence pushing this music forward. %s Instead a %s holds a fixed note, or a narrow group of "
  "notes, while everything else moves above it. That is how harmony works in Irish traditional music and in many "
  "African and Asian traditions too, so the drone is common ground rather than one side&rsquo;s idea."
  % (d.ref(1), dfn("drone", "A sustained or repeated note that stays fixed while other material moves above it")),
  "the note that never changes. Say the harmony is drone-based, not that the track &lsquo;has no harmony&rsquo;.")

d.add_statement(2, "Rhythm", "2 &middot; Two traditions, one pulse",
  "Three rhythmic layers are working at once. %s The Irish melodic lines carry a %s, the swinging dance feel of jigs "
  "and reels. The West African percussion adds %s, accents that do not line up with the main beat. Underneath, an "
  "unchanging programmed pulse holds both in place."
  % (d.ref(2), dfn("lilt", "A gentle swinging, dance-like rhythmic feel"),
     dfn("cross-rhythm", "Patterns accenting beats that do not align with the main pulse")),
  "two rhythmic feels pulling gently against each other. The programmed beat is what stops them coming apart.")

d.add_statement(3, "Melody", "3 &middot; Decorated lines",
  "Melody here is not a tune with a chorus; it is a decorated line. %s The vocal is close to %s, the unaccompanied "
  "Irish style with free rhythm and heavy ornament, and the pipes and whistle decorate in the same way, with %s. The "
  "vocal functions as a lament over the groove."
  % (d.ref(3), dfn("sean-n&oacute;s", "An unaccompanied, highly ornamented Irish vocal tradition with free rhythm"),
     dfn("rolls, cuts and grace notes", "Standard ornaments of Irish traditional playing, added around the main notes")),
  "how few notes are left plain. Name the ornament type, not just &lsquo;it sounds decorated&rsquo;.")

d.add_statement(4, "Instruments", "4 &middot; Both sides, by name",
  "Marks come from pairing each instrument with its tradition. %s From Ireland: uilleann pipes, tin whistle, fiddle "
  "and button accordion. From West Africa: the %s, whose pitch bends as the player squeezes its cords, the kora, and "
  "the goblet-shaped %s played with bass, tone and slap strokes."
  % (d.ref(4), dfn("talking drum", "A West African hourglass drum whose pitch changes as the player squeezes cords along its body"),
     dfn("djembe", "A goblet-shaped West African hand drum played with bass, tone and slap strokes")),
  "which family answers which. Learn the six names and which side each belongs to.")

d.add_statement(5, "Texture", "5 &middot; Dialogue, not unison",
  "The layers come back one at a time. %s Above the drone the texture is built from dialogue: a phrase from the "
  "whistle or pipes is answered or overlapped by the kora or the voice, over repeating %s patterns in the "
  "percussion. The traditions converse; they almost never play the same line together."
  % (d.ref(5), dfn("ostinato", "A pattern repeated persistently throughout a section")),
  "call and response between named instruments. That is the sentence examiners want, with the names in it.")

d.add_statement(6, "Technology", "6 &middot; The studio as a player",
  "Treat the production as an instrument, because the specification does. %s Short sections are %s so percussion and "
  "bass run continuously while live playing is added on top; %s, reverb and filtering blend acoustic timbres with "
  "electronic ones; and muting layers is what creates the breakdown and this final build."
  % (d.ref(6), dfn("looped", "Repeated automatically, so a short recorded section runs continuously"),
     dfn("sampling", "Taking a recorded sound and reusing or processing it within a new piece")),
  "how seamlessly acoustic and electronic sit together. That blend is a production achievement, not an accident.")

d.add_checklist(
  "Melody: ornamented Irish lines and a sean-nos style vocal lament, with rolls, cuts and grace notes. Harmony: "
  "drone-based, with no driving chord progression. Rhythm: Irish lilt and West African cross-rhythm over a steady "
  "programmed pulse. Texture: drone foundation with call-and-response dialogue and layered ostinato patterns. "
  "Instrumentation: uilleann pipes, whistle, fiddle and accordion against kora, talking drum and djembe. Technology: "
  "loops, samples, reverb and filtering, used to build, break down and rebuild the track.",
  "Pair the term with the tradition and the moment. &ldquo;It uses cross-rhythm&rdquo; earns little; &ldquo;the West "
  "African percussion accents beats off the programmed pulse, so two rhythmic layers pull against each other&rdquo; "
  "earns the mark.")

content = d.content()
exam_tip = ("<p>The commonest lost mark here is vagueness about which tradition a feature belongs to. Attach every "
            "observation to a side of the fusion: lilt and ornamented melody from the Irish tradition, cross-rhythm "
            "and interlocking drum patterns from West Africa, drone shared by both, and loops, samples and "
            "programmed beats from dance production. Then say where you heard it.</p>")
conclusion = ("<p>You can now describe each element of Release and point to where it is audible: a drone instead of "
              "a chord progression, an Irish lilt and West African cross-rhythm above a programmed pulse, heavily "
              "ornamented melodic lines, named instruments from each tradition, a texture built from dialogue, and "
              "production used as a creative tool. Set it beside Samba em Preludio and you can compare two very "
              "different answers to the same fusion question.</p>")
description = ("Six numbered stops in Afro Celt Sound System's Release, one for each element: harmony, rhythm, "
               "melody, instrumentation, texture and technology.")

flashcards = [
  {"q": "What is the function of the drone in the texture of Release?",
   "a": "It provides a sustained, fixed foundation over which melodic and rhythmic layers move, instead of a chord progression driving the harmony."},
  {"q": "What rhythmic feature comes from the Irish tradition in Release?",
   "a": "A lilting, dance-like rhythmic feel associated with jigs and reels, giving the pipes and whistle lines their bounce."},
  {"q": "What rhythmic feature comes from the West African tradition in Release?",
   "a": "Cross-rhythm: percussion patterns accenting beats that do not align with the main pulse, so two rhythmic layers pull against one another."},
  {"q": "How does the programmed pulse function in the track?",
   "a": "It is a steady, unchanging anchor. However much the Irish lilt and the African cross-rhythm pull against each other, the electronic beat keeps everything locked together."},
  {"q": "How is technology used as an active musical tool in Release rather than just a recording method?",
   "a": "Loops, sampling and processing shape the rhythm and texture, blend acoustic and electronic timbres, and create the build, breakdown and rebuild by muting and reintroducing layers."},
  {"q": "Name the ornaments typical of the Irish melodic lines in Release.",
   "a": "Rolls, cuts and grace notes, added around the main notes of the melody by the pipes, whistle and voice."},
]

practice = [
  {"text": "Identify the term used to describe a sustained or repeated note that underpins the texture of Release.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for drone."},
  {"text": "Explain how the drone shapes the harmony of the track.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: a fixed note or narrow group of notes is held while other material moves above it. One mark: there is no driving chord progression, and the drone is common to both Irish and West African traditions, so it works as shared ground."},
  {"text": "Explain how rhythm from the Irish tradition differs from rhythm associated with the West African tradition in Release.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the Irish melodic lines carry a lilting, dance-like swing. One mark: the West African percussion uses cross-rhythm, accenting beats away from the main pulse. One mark: a valid comparison, including that both sit over a steady programmed beat that holds them together."},
  {"text": "Explain the role of technology in shaping the texture and structure of Release.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: loops keep percussion and bass running continuously. One mark: sampling and processing such as reverb and filtering blend acoustic with electronic timbres. One mark: layers can be muted and reintroduced precisely. One mark: this is what produces the build, the breakdown and the rebuild, so technology determines the structure."},
  {"text": "Name one instrument associated with the West African tradition heard in Release.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for kora, talking drum or djembe."},
  {"text": "Discuss how melodic dialogue is used between instruments in Release, referring to specific instruments.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: phrases are exchanged rather than played in unison. One mark: named instruments on each side, for example whistle or uilleann pipes answered by kora or voice. One mark: an explanation that this call and response creates a multi-stranded texture in which each tradition keeps its identity."},
]

kcs = [
  {"q": "What structural device is used in the middle of Release to strip the texture back before it rebuilds?",
   "options": ["A key change", "A breakdown", "A cadenza", "A modulation"], "correct": 1},
  {"q": "Which feature is most closely associated with the West African tradition in Release?",
   "options": ["Lilting dotted rhythm", "Cross-rhythmic percussion", "A programmed dance pulse", "Sustained drone alone"], "correct": 1},
  {"q": "What is a drone in the context of Release?",
   "options": ["A fast repeated bass riff", "A sustained or repeated note underpinning the texture", "A vocal effect created with reverb", "A type of cross-rhythm"], "correct": 1},
  {"q": "Which instrument is a plucked, harp-like instrument from West Africa heard in the track?",
   "options": ["Uilleann pipes", "Kora", "Fiddle", "Bodhran"], "correct": 1},
  {"q": "How does the programmed pulse function within the overall texture?",
   "options": ["It disrupts the rhythm to create tension throughout", "It acts as a steady anchor holding contrasting rhythms together", "It only appears in the breakdown section", "It replaces the drone as the main melodic feature"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "release_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
