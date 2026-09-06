# -*- coding: utf-8 -*-
"""music-edexcel / aos1-instrumental-music / L3 -- the ELEMENTS walk over the
same recording as L2 (T_HioE0FWAI, 5:35). L2 does the structural walk, so this
deck takes one card per musical element: melody, dynamics, tonality, timbre,
texture, metre. Pin times: 2s and 8s = the flute and harpsichord subject entries
(3/3 votes, and bar 3 / bar 9 at ~1.05 s per bar = 2.1 s / 8.4 s); 29 / 82 / 164
/ 242 / 305 carried over from the verified L2 probe; 271 = the ripieno rejoining
after the da capo (2/3 votes at 4:31, and bar 261 = 242 + 28x1.05 = 271 s).
Dropped: "loudest tutti in the middle section" (votes 2:14 / 1:30 / 3:13, split).
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos1-instrumental-music__L03"
d = Deck(lesson_id="24776f1d-3e91-4816-a573-7888116af67c",
         subject="music-edexcel", unit="aos1-instrumental-music", lesson_no=3,
         yt="T_HioE0FWAI", dur=335, track_label="Brandenburg 5/iii",
         credit="Chamber Orchestra of Europe performance, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Bach: Brandenburg Concerto No. 5, 3rd movement.")

TITLE = "Bach: Brandenburg Concerto No. 5, Third Movement — The Elements in Close-Up"

d.pins = [
    ("t1c1", 2,   "Melody",        "Bar 3: the flute answers with the identical subject, so you hear its shape twice over."),
    ("t1c2", 29,  "Dynamics",      "Bar 29: the ripieno arrives and the volume jumps. No crescendo &mdash; the players simply add themselves."),
    ("t1c3", 82,  "Tonality",      "Bar 79: D major gives way to B minor. Name the keys, do not just say the music modulates."),
    ("t1c4", 164, "Timbre",        "The harpsichord takes the lead. Plucked and bright against the sustained flute and bowed violin."),
    ("t1c5", 271, "Texture",       "Bar 261: after the da capo entries, the ripieno rejoins and the full weave is back."),
    ("t1c6", 305, "Metre",         "The drive to the final cadence. It lilts like a gigue, but count it and it is a simple two."),
]

d.add_cover(
    "The same finale, element by element",
    [
      "Bach&rsquo;s finale of about 1721 sets a %s of flute, violin and harpsichord against a string %s with %s. D major, Allegro, 2/4, and built as a fugue inside a da capo A B A frame."
      % (dfn("concertino", "The small group of soloists in a concerto grosso"),
         dfn("ripieno", "The larger body of strings in a concerto grosso; also called the tutti"),
         dfn("continuo", "The Baroque accompanying bass line, realised by harpsichord and a bass instrument")),
      "The previous lesson walked the movement from start to finish. This one stops at six moments, one for each %s an examiner can ask you about: melody, dynamics, tonality, timbre, texture and metre."
      % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
      "Press play and the cards follow the music. Tap any number to jump to that moment.",
    ])

d.add_statement(1, "Melody", "1 &middot; The shape of the subject",
  "Every bar of this movement grows from one tune. Its shape is worth learning: running quavers and semiquavers, mostly %s, with small leaps that spell out the chord underneath. %s There are almost no long notes. Later Bach stretches it by %s, lifting the same short pattern up or down a step at a time."
  % (dfn("conjunct", "Moving by step, from one note to the next one above or below"), d.ref(1),
     dfn("sequence", "The immediate repetition of a musical idea at a higher or lower pitch")),
  "the flute repeating the violin&rsquo;s tune note for note. Fix that rising-then-falling shape in your ear &mdash; you must spot it later in any instrument.")

d.add_statement(2, "Dynamics", "2 &middot; Volume in steps, not slopes",
  "Listen to what happens to the loudness here, and to what does not. The sound jumps, then stays. %s A Baroque string band cannot swell gradually, so Bach changes volume by adding or removing players: three soloists, then the whole ensemble. That is %s, and it is the only dynamic device this movement needs."
  % (d.ref(2), dfn("terraced dynamics", "Sudden changes of volume made by adding or removing players, rather than by a gradual crescendo or diminuendo")),
  "a step up in volume, not a slope. If you hear no crescendo anywhere in the movement, that is the point, not an accident.")

d.add_statement(3, "Tonality", "3 &middot; Name the keys",
  "The movement is anchored in D major, the home key of the whole concerto. Here it turns to B minor, the %s. %s The central section also touches A major, the %s, before working back. Baroque tonal planning is exactly this: leave the tonic, visit closely related keys, return decisively."
  % (dfn("relative minor", "The minor key sharing a key signature with the major: B minor for D major"), d.ref(3),
     dfn("dominant", "The fifth degree of the scale, and the key built on it: A major in D major")),
  "the change of colour from bright to shadowed. In the exam, write &lsquo;it modulates to B minor, the relative minor&rsquo; &mdash; naming the key earns the mark, &lsquo;it modulates&rsquo; does not.")

d.add_statement(4, "Timbre", "4 &middot; Telling them apart",
  "Three solo %s, three different sounds. %s The harpsichord is plucked, so every note starts sharply and dies away at once; the flute is breathy and sustained; the violin is bowed, and can hold and swell a single note. One trap to avoid: the famous unaccompanied harpsichord %s belongs to the first movement, not to this one."
  % (dfn("timbres", "The characteristic tone colour of an instrument or voice"), d.ref(4),
     dfn("cadenza", "An extended passage for a soloist alone, showing off technique")),
  "the plucked attack cutting through. Decide by attack and decay, not by how high or low the line is.")

d.add_statement(5, "Texture", "5 &middot; The full weave",
  "The ripieno is back, and the texture is at its thickest. %s Even now the lines stay independent, which is what makes this %s rather than a tune with chords: each part carries its own material, and entries %s each other. Underneath it all the continuo bass keeps the harmony moving."
  % (d.ref(5), dfn("polyphonic", "Made of two or more independent melodic lines sounding together; also called contrapuntal"),
     dfn("imitate", "Repeat a melodic idea shortly after another part has played it, usually at a different pitch")),
  "how many separate lines you can follow at once. Answers score when you say who imitates whom, not just &lsquo;polyphonic&rsquo;.")

d.add_statement(6, "Metre", "6 &middot; Count it in two",
  "The movement rushes to its close, and the lilt is unmistakably that of a %s. %s That is the trap: the character is dance-like, but the %s is 2/4, a simple duple beat, not the 6/8 a gigue usually takes. Tap along and you will find two beats in a bar, each divided into ordinary halves and quarters."
  % (dfn("gigue", "A lively Baroque dance, usually the last movement of a suite"), d.ref(6),
     dfn("metre", "The pattern of strong and weak beats in a bar")),
  "two firm beats per bar under all that semiquaver motion. Feel the pulse, then count it, before you write down a time signature.")

d.add_checklist(
  "Melody: one fugal subject, conjunct with chordal leaps, extended by sequence and decorated with trills. Dynamics: terraced, made by adding or removing players. Tonality: D major, through B minor and A major and back. Timbre: plucked harpsichord against sustained flute and bowed violin. Texture: polyphonic and imitative, with a continuo bass; thickest when the ripieno plays. Metre and tempo: 2/4, Allegro, gigue-like in character. Harmony: functional, driving to perfect cadences.",
  "Each of those words is worth a mark only when it is attached to something audible. &ldquo;Terraced dynamics&rdquo; earns little; &ldquo;the volume jumps at bar 29 because the ripieno is added, with no crescendo&rdquo; earns the mark.")

content = d.content()

exam_tip = ("<p>Element questions are marked on evidence, not vocabulary. If you are asked about texture, say which "
            "instrument imitates which and roughly where; if you are asked about tonality, name the key, not just the "
            "fact of a change; if you are asked about dynamics, say that the change is terraced and explain that it is "
            "made by adding or removing players. A correct term with no supporting detail caps the mark every time.</p>")
conclusion = ("<p>You can now take each element of this movement in turn and point to a moment where it is audible: the "
              "shape of the subject, the terraced jump when the ripieno enters, the turn to B minor, the plucked "
              "harpsichord, the full polyphonic weave after the da capo, and the simple duple metre under the gigue-like "
              "lilt. Next comes Beethoven&rsquo;s Path&eacute;tique Sonata, where the same elements are handled in a "
              "completely different style.</p>")
description = ("Six numbered stops in Bach's Brandenburg 5 finale, one for each element: melody, dynamics, tonality, "
               "timbre, texture and metre.")

flashcards = [
  {"q": "What are the two contrasting forces in a concerto grosso, and who plays each here?",
   "a": "The concertino, a small solo group of flute, violin and harpsichord, against the ripieno, the larger body of strings with continuo."},
  {"q": "Describe the shape of the fugal subject in the third movement.",
   "a": "Running quavers and semiquavers, mostly conjunct (stepwise), with small leaps that outline the underlying chord, and almost no long notes. Bach extends it by sequence."},
  {"q": "What is terraced dynamics, and where is it heard in this movement?",
   "a": "Sudden changes of volume made by adding or removing players rather than by a crescendo. It is heard whenever the ripieno strings join or drop away around the concertino, for example at bar 29."},
  {"q": "Which keys does the finale visit, and what is the home key?",
   "a": "The home key is D major. The music moves to B minor, the relative minor, and touches A major, the dominant, before returning to D major."},
  {"q": "How can you tell the harpsichord from the flute and violin by ear?",
   "a": "The harpsichord is plucked, so each note starts sharply and dies away immediately. The flute is breathy and sustained, and the bowed violin can hold and swell a note."},
  {"q": "What is the metre of the third movement, and why is it easy to get wrong?",
   "a": "It is 2/4, a simple duple metre. The continuous running notes give it the lilt of a gigue, which is usually in compound time, so students often write 6/8 instead."},
]

practice = [
  {"text": "Identify the metre of the third movement of Brandenburg Concerto No. 5.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for 2/4. Do not credit 6/8."},
  {"text": "Describe two features of the melodic subject that opens this movement.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark each, up to two, from: continuous quavers and semiquavers; mostly conjunct or stepwise; small leaps outlining the chord; decorated with trills or scalic flourishes; extended by sequence."},
  {"text": "Describe the texture heard at the opening of the third movement.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark for imitative, contrapuntal or polyphonic. One mark for the detail that the violin states the subject first and the flute and harpsichord follow with the same idea."},
  {"text": "Explain what is meant by terraced dynamics and describe where it is heard in this movement.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: sudden shifts of volume. One mark: made by adding or removing players rather than a gradual crescendo. One mark: heard when the ripieno strings join or leave, for example the tutti entry at bar 29."},
  {"text": "Explain how key relationships contribute to the overall structure of the movement.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: D major is the tonic. One mark: the middle section moves to B minor, the relative minor. One mark: related keys such as A major, the dominant, are touched on the way. One mark: the decisive return to D major closes the movement and reinforces the da capo return."},
  {"text": "Compare the role of the harpsichord in this movement with its role elsewhere in the concerto.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the extended unaccompanied cadenza belongs to the first movement. One mark: in the finale the harpsichord plays the subject as an equal member of the concertino. One mark: it also continues to supply continuo harmony under the other parts."},
]

kcs = [
  {"q": "What is the metre of the third movement of Brandenburg Concerto No. 5?",
   "options": ["3/4", "2/4", "6/8", "4/4"], "correct": 1},
  {"q": "Which term best describes the opening texture of the finale?",
   "options": ["Homophonic", "Monophonic", "Imitative and contrapuntal", "Heterophonic"], "correct": 2},
  {"q": "Where does the famous extended harpsichord cadenza in this concerto actually occur?",
   "options": ["In the third movement", "In the first movement", "In the second movement", "It does not exist in this concerto"], "correct": 1},
  {"q": "How does Bach change the volume in this movement?",
   "options": ["By marking gradual crescendos in the strings", "By adding or removing players, giving terraced dynamics", "By changing the tempo", "By muting the ripieno strings"], "correct": 1},
  {"q": "Which key is the relative minor visited in the middle section?",
   "options": ["G minor", "A major", "B minor", "F sharp minor"], "correct": 2},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "brandenburg_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
