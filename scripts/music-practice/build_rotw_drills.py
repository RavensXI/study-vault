# -*- coding: utf-8 -*-
"""Build the OCR Rhythms of the World listening drills (task #59).

Unit aos3-rhythms-listening, 4 lessons (India & Punjab, Eastern
Mediterranean & Middle East, Africa, Central & South America).
Bronze/silver run on the machine-verified synthesised patterns from
gen_rotw_rhythms.py (rhythm/metre questions ONLY — house synth rule).
Gold runs on real recordings where sourced licence-clean:
  L2 gold — Cheikh Youssef El-Manyalawi, Cairo 1909 (both PD; probes
            passed: melismatic solo voice, microtonal ornament, plucked
            accompaniment, acoustic-era technology).
  L4 gold — 'Dengozo' (Ernesto Nazareth), Argentine Marimba Band, Victor
            1923 (PD; probes: 3/3 marimba lead, syncopated duple dance).
L1/L3 gold carries the HARDEST synthetic questions for now — real
recordings for India/Africa were not sourceable licence-clean (Tom's
generation-fallback conversation covers the upgrade).

Run: python build_rotw_drills.py [--apply]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from gen_drill_peaks import peaks_for


def _fmt(t):
    t = max(0, int(t or 0))
    return "%d:%02d" % (t // 60, t % 60)


def player_html(url, entry):
    # same markup apply_inline_player.py embeds site-wide
    payload = json.dumps({"peaks": entry["peaks"],
                          "duration": entry["duration"]},
                         separators=(",", ":"))
    return (
        '<figure class="sv-ap-inline" data-audio="%s">'
        '<button type="button" class="sv-api-play" aria-label="Play">'
        "&#9654;</button>"
        '<div class="sv-api-wrap"><canvas class="sv-api-canvas"></canvas>'
        "</div>"
        '<span class="sv-api-tick">0:00 / %s</span>'
        '<script type="application/json" class="sv-api-peaks">%s</script>'
        "</figure>"
    ) % (url, _fmt(entry["duration"]), payload)

APPLY = "--apply" in sys.argv
R2 = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-ocr/aos3-rhythms-listening/"


def passage(pid, heading, filename, local_folder):
    peaks, dur = peaks_for(os.path.join(HERE, local_folder, filename))
    html = ('<div style="text-align:center;"><p style="font-family:Inter,'
            'sans-serif;font-size:0.95rem;color:var(--text-primary);'
            'margin-bottom:0.75rem;">%s</p>%s</div>'
            % (heading, player_html(R2 + filename,
                                    {"peaks": peaks, "duration": dur})))
    return {"id": pid, "text": html}


def mc(pid, q, opts, sol, expl, miscon=None):
    p = {"question": q, "options": opts, "solutions": [sol],
         "input_type": "multiple_choice", "passage_id": pid,
         "explanation": expl, "misconceptions": []}
    if miscon:
        mid, exp, msg = miscon
        p["misconceptions"] = [{"id": mid, "expect": exp, "message": msg}]
    return p


EXAM_CTX = {"marks": "varies — questions are 1–6 marks",
            "paper": "Listening (Component 1)",
            "frequency": "Rhythms of the World appears on every listening "
                         "paper"}


def lesson1():
    """India & Punjab."""
    ps = [
        passage("p-chaal", "Bhangra chaal groove &middot; synthesised "
                "pattern (studio-built for this drill)", "chaal_swung.mp3",
                "_rotw_synth"),
        passage("p-tintal", "16-beat tala cycle &middot; synthesised "
                "pattern", "tintal_16.mp3", "_rotw_synth"),
        passage("p-keherwa", "8-beat tala cycle &middot; synthesised "
                "pattern", "keherwa_8.mp3", "_rotw_synth"),
    ]
    bronze = [
        mc("p-chaal", "Listen to the groove. Are the pairs of quick notes "
           "even, or is each pair swung (long-short)?",
           ["Swung — each pair is long-short", "Perfectly even",
            "Getting steadily faster", "In a three-beat waltz rhythm"],
           0, "The chaal rides on swung quavers: each pair divides "
           "long-short, giving bhangra its bounce. Count the underlying "
           "beat — it stays in four while the pairs swing.",
           ("swing-vs-tempo-change", 2,
            "You heard the lilt as speeding up, but the beat itself is "
            "steady — it is the SPLIT of each beat that is uneven "
            "(long-short), which is what swung rhythm means.")),
        mc("p-chaal", "The drum pattern alternates two sounds. What is the "
           "relationship between them?",
           ["A deep stroke on the beat, a higher stroke between the beats",
            "Two identical strokes", "A higher stroke on the beat, a "
            "deeper stroke between", "The two sounds never alternate"],
           0, "The dhol works exactly this way: the heavy dagga (bass) "
           "side marks the beat while the sharp tilli (treble) side "
           "answers between the beats.", None),
        mc("p-keherwa", "Count the repeating cycle marked by the deep "
           "drum strokes. How many steady beats before it repeats?",
           ["8", "16", "7", "3"], 0,
           "This is an eight-beat cycle (like the keherwa tala): a strong "
           "stroke on beat 1, a lighter marker halfway through on beat 5.",
           ("cycle-vs-strokes", 1,
            "You may have counted every sound rather than the steady "
            "underlying pulse. Count the even background clicks between "
            "the deep strokes — eight per cycle.")),
        mc("p-chaal", "Is this metre regular or irregular?",
           ["Regular — a steady four with an even split possible",
            "Irregular — groups of unequal length",
            "Free time with no pulse", "Constantly changing metre"],
           0, "For all its swing, the chaal sits in a completely regular "
           "four. Swing changes the FEEL of the subdivision, not the "
           "regularity of the metre.", None),
    ]
    silver = [
        mc("p-tintal", "This tala cycle is longer. Count the steady "
           "pulse: how many beats before the strongest stroke returns?",
           ["16", "8", "12", "20"], 0,
           "This is the shape of tintal, the most common Hindustani "
           "tala: sixteen beats in four groups of four, with the "
           "strongest stroke (sam) restarting the cycle.",
           ("tala-half-count", 1,
            "Eight is the halfway marker — keep counting: the truly "
            "strongest stroke only returns after sixteen beats.")),
        mc("p-tintal", "Listen around the middle of each cycle. What "
           "happens at the start of the third group of four beats?",
           ["The marking gets quieter — an 'empty' group",
            "A cymbal crash", "The tempo doubles", "The cycle restarts"],
           0, "In tintal the third group (beats 9-12) is khali, the "
           "'empty' section — marked by a wave, not a clap, so the "
           "accompaniment goes quiet there. Hearing sam and khali is how "
           "performers keep their place in the cycle.", None),
        mc("p-chaal", "Which description best fits the chaal's cycle?",
           ["Eight swung quavers over a four-beat bar",
            "Sixteen even semiquavers over two bars",
            "Seven quavers grouped 3+2+2",
            "Six quavers in two groups of three"],
           0, "The chaal is an eight-stroke pattern across one bar of "
           "four beats, every pair swung. It repeats every bar — short "
           "cycle, high energy, built for dancing.", None),
        mc("p-keherwa", "Compare this cycle with the sixteen-beat one. "
           "Which statement is TRUE?",
           ["Both are regular cycles; one is half the length of the other",
            "This one is irregular", "The sixteen-beat one is irregular",
            "They are the same length"],
           0, "Both talas are perfectly regular cycles of steady beats — "
           "the difference is scale: eight versus sixteen. Indian "
           "classical rhythm builds long regular cycles rather than "
           "short Western-style bars.", None),
    ]
    gold = [
        mc("p-tintal", "A performer following this cycle claps on beats "
           "1, 5 and 13 but waves silently at beat 9. What does that "
           "silent wave tell the listeners?",
           ["Beat 9 begins the khali ('empty') group — a deliberately "
            "unstressed quarter of the cycle",
            "The performer has lost the beat",
            "The music is about to stop", "Beat 9 is the loudest beat"],
           0, "The clap-clap-wave-clap scheme IS the tala's identity "
           "card: sam at 1, tali (claps) at 5 and 13, khali waved at 9. "
           "The 'empty' group is structural, not a mistake — soloists "
           "use it to feel where they are in the cycle.", None),
        mc("p-chaal", "An exam question asks how this drumming creates "
           "energy for dancing. Which TWO features would earn the marks?",
           ["The swung subdivision and the constant low-high alternation "
            "of strokes",
            "A gradual accelerando and a final cymbal roll",
            "Irregular metre and free rhythm",
            "Silence between every stroke"],
           0, "Two cycle-level engines drive bhangra: the swing (each "
           "beat split long-short) and the dhol's relentless "
           "low-high conversation. Name concrete features, not vague "
           "'it is lively'.", None),
        mc("p-keherwa", "These cycle patterns were built in a studio for "
           "this drill. In a real performance, what would a tabla player "
           "add that a fixed loop cannot?",
           ["Improvised variations and fills that decorate the cycle "
            "while keeping its shape",
            "A completely random pulse", "A different number of beats "
            "every cycle", "Nothing — real players repeat exactly"],
           0, "The cycle is a framework, not a straitjacket: real "
           "players improvise around the theka, decorating and "
           "displacing while sam stays sacred. That balance of fixed "
           "cycle and free decoration is the heart of the tradition.",
           None),
    ]
    worked = [{
        "difficulty": "bronze",
        "question": "<p>Play the tala excerpt below before reading on, "
                    "then follow the steps.</p>" + ps[1]["text"],
        "steps": [
            {"label": "Find the pulse first",
             "content": "<p>Ignore the accents to begin with — lock onto "
                        "the steady background clicks. Tap along until "
                        "your tapping feels automatic.</p>"},
            {"label": "Find the strongest stroke",
             "content": "<p>One stroke is heavier than everything else. "
                        "That is sam, the cycle's beat 1. Start counting "
                        "from it.</p>"},
            {"label": "Count to the next sam",
             "content": "<p>Keep counting steady beats until the heavy "
                        "stroke returns. You should reach sixteen — four "
                        "groups of four.</p>"},
            {"label": "Answer",
             "content": "<p>A sixteen-beat cycle — the shape of tintal, "
                        "the most common tala in Hindustani music.</p>"},
        ]}]
    return {"exam_context": EXAM_CTX,
            "method_card": {
                "title": "What to listen for",
                "steps": ["Find the steady pulse before anything else.",
                          "Find the strongest stroke — cycles restart "
                          "there.",
                          "Count beats between strong strokes to get the "
                          "cycle length.",
                          "Listen for swing: are pairs of quick notes "
                          "even or long-short?"],
                "content": "<p>Indian and Punjabi rhythm is built on "
                           "<strong>cycles</strong>: the tala in "
                           "classical music (count it), the "
                           "<strong>chaal</strong> in bhangra (feel its "
                           "swing). Every question in this drill is "
                           "answered by counting or by listening to how "
                           "beats divide.</p>"},
            "passages": ps,
            "problem_bank": {"bronze": bronze, "silver": silver,
                             "gold": gold},
            "worked_examples": worked}


def lesson2():
    """Eastern Mediterranean & Middle East. Gold = Manyalawi 1909."""
    ps = [
        passage("p-kala", "Dance rhythm in seven &middot; synthesised "
                "pattern (studio-built for this drill)",
                "kalamatianos_78.mp3", "_rotw_synth"),
        passage("p-kars", "Dance rhythm in nine &middot; synthesised "
                "pattern", "karsilamas_98.mp3", "_rotw_synth"),
        passage("p-dumtek", "Goblet-drum pattern in four &middot; "
                "synthesised pattern", "dum_tek_44.mp3", "_rotw_synth"),
        passage("p-manyalawi-a",
                "Cheikh Youssef El-Manyalawi, Cairo, 1909 &middot; "
                "public-domain recording", "gold_manyalawi_a.mp3",
                "_rotw_goldcut"),
        passage("p-manyalawi-b",
                "Cheikh Youssef El-Manyalawi, Cairo, 1909 &middot; "
                "second extract", "gold_manyalawi_b.mp3", "_rotw_goldcut"),
    ]
    bronze = [
        mc("p-dumtek", "Is this drum pattern in a regular or irregular "
           "metre?",
           ["Regular — a steady four you could march to",
            "Irregular — the groups keep limping",
            "Free time", "A waltz in three"],
           0, "This dum-tek pattern sits squarely in four: deep 'dum' "
           "strokes on the strong beats, crisp 'tek' strokes answering. "
           "Keep its steadiness in your ear before tackling the "
           "irregular patterns.", None),
        mc("p-kala", "Try to march in two or waltz in three to this "
           "pattern. Why does it not fit?",
           ["The bar has SEVEN quick pulses — an irregular metre",
            "The tempo keeps changing", "There is no drum on beat 1",
            "It fits a march perfectly"],
           0, "Seven quavers per bar: you can't split seven evenly, so "
           "every bar 'limps'. This is the kalamatianos metre — Greece's "
           "most famous dance rhythm.",
           ("irregular-vs-rubato", 1,
            "The SPEED is steady — count the quick pulses and you get "
            "seven every time. Irregular metre means uneven GROUPING, "
            "not unsteady tempo.")),
        mc("p-kala", "Listen to where the accents fall. How are the "
           "seven pulses grouped?",
           ["3+2+2 — one long group, two short",
            "2+2+3 — two short groups, one long",
            "7 equal accents", "4+3"],
           0, "The kalamatianos groups its seven as LONG-short-short: a "
           "three-pulse stride then two quicker steps. Hear the heavy "
           "accent, then two lighter ones.", None),
        mc("p-dumtek", "The deep stroke and the crisp stroke on this "
           "goblet drum are traditionally called what?",
           ["Dum (deep, centre) and tek (crisp, edge)",
            "Boom and crash", "Sam and khali", "Call and response"],
           0, "On the darbuka, the resonant centre stroke is the dum "
           "and the sharp rim stroke the tek — drummers speak entire "
           "patterns in these syllables.", None),
    ]
    silver = [
        mc("p-kars", "This dance rhythm has NINE quick pulses per bar. "
           "Where does the long group come?",
           ["At the end — 2+2+2+3", "At the start — 3+2+2+2",
            "In the middle — 2+3+2+2", "There is no long group"],
           0, "The karsilamas groups its nine as short-short-short-LONG: "
           "three quick steps then the stretched final group. Contrast "
           "with the kalamatianos, whose long group comes FIRST.",
           ("nine-eight-compound", 3,
            "Nine quavers CAN divide evenly as 3+3+3 (compound triple), "
            "but listen to the accents here: three quick twos then a "
            "stretched three — the uneven 2+2+2+3 of the dance.")),
        mc("p-kala", "A friend says this is in 7/8 grouped 2+2+3. What "
           "listening evidence proves them wrong?",
           ["The LONGEST gap between accents comes first in each bar, "
            "not last",
            "There are only six pulses", "There are no accents at all",
            "The tempo is too fast to tell"],
           0, "Both are seven — the grouping is the identity. Here the "
           "big stride opens the bar (3+2+2); in 2+2+3 the stretch "
           "would come last, like the karsilamas's ending.", None),
        mc("p-kars", "Which pair correctly matches dance to metre?",
           ["Kalamatianos 7/8, karsilamas 9/8",
            "Kalamatianos 9/8, karsilamas 7/8",
            "Both 7/8", "Both 4/4"],
           0, "Kalamatianos = seven (3+2+2); karsilamas = nine "
           "(2+2+2+3). Naming dance, metre AND grouping is full-mark "
           "territory.", None),
        mc("p-dumtek", "How would you turn this regular pattern into an "
           "additive, irregular one?",
           ["Regroup the same fast pulses into unequal groups such as "
            "3+3+2 or 3+2+2",
            "Play it faster", "Add more drums", "Play it more quietly"],
           0, "Irregular (additive) metre is about GROUPING, not speed "
           "or volume: the same stream of quick pulses bundled unevenly. "
           "That is exactly how 7/8 and 9/8 dances are built.", None),
    ]
    gold = [
        mc("p-manyalawi-a", "This is a 1909 recording from Cairo. How "
           "does the solo singer treat the notes of the melody?",
           ["Heavily decorated — slides, shakes and runs between and "
            "around the notes",
            "One plain note per syllable throughout",
            "Spoken rhythmically rather than sung",
            "In block harmony with other singers"],
           0, "This is melismatic, ornamented singing — the voice bends, "
           "slides and quivers around the melodic line. Ornamentation "
           "IS the artistry in this tradition, not an extra.",
           ("melisma-vs-out-of-tune", 1,
            "Those slides between pitches are not poor tuning — Arabic "
            "maqam melody uses intervals and inflections smaller than "
            "Western semitones, applied deliberately as ornament.")),
        mc("p-manyalawi-a", "Some of the singer's pitches fall BETWEEN "
           "the notes a piano could play. What is this feature called?",
           ["Microtonal intervals — characteristic of the maqam system",
            "Bad intonation", "A minor key", "Modulation"],
           0, "Arabic maqam scales include intervals finer than the "
           "semitone — often described as quarter-tones. A piano cannot "
           "play them; this voice lives on them.", None),
        mc("p-manyalawi-b", "Listen to the accompaniment texture behind "
           "the voice. Which best describes it?",
           ["A small group shadowing the voice heterophonically — "
            "versions of the same melody, not chords",
            "A full orchestra playing block harmony",
            "Solo piano accompaniment", "Unaccompanied voice"],
           0, "The takht (small Arabic ensemble) plays the SAME melodic "
           "line as the singer, each instrument decorating it its own "
           "way — heterophony, not Western chordal harmony.", None),
        mc("p-manyalawi-b", "The sound is narrow, noisy and has no deep "
           "bass. What does that tell you about HOW it was recorded?",
           ["Acoustic-era technology: performers sang into a horn, "
            "decades before microphones",
            "A modern digital recording deliberately distorted",
            "A live stadium concert", "Multitrack studio layering"],
           0, "In 1909 sound was captured by a horn driving a cutting "
           "stylus — no microphones, no electricity. The constrained, "
           "crackly sound IS the technology of the era, a legitimate "
           "exam observation about recording technology and its impact.",
           None),
    ]
    worked = [{
        "difficulty": "silver",
        "question": "<p>Play the seven-pulse excerpt below, then follow "
                    "the steps.</p>" + ps[0]["text"],
        "steps": [
            {"label": "Count the fast pulses",
             "content": "<p>Count the quickest even layer until the "
                        "pattern repeats: you get seven, so the metre is "
                        "irregular — no way to halve or third it "
                        "evenly.</p>"},
            {"label": "Find the accents",
             "content": "<p>Listen for the heavier strokes: one big "
                        "accent, then two lighter ones. The gaps are "
                        "long-short-short.</p>"},
            {"label": "Name the grouping",
             "content": "<p>Long-short-short across seven pulses is "
                        "3+2+2 — the kalamatianos grouping. If the long "
                        "group came last you would write 2+2+3.</p>"},
            {"label": "Answer",
             "content": "<p>7/8, grouped 3+2+2 — an irregular (additive) "
                        "dance metre.</p>"},
        ]}]
    return {"exam_context": EXAM_CTX,
            "method_card": {
                "title": "What to listen for",
                "steps": ["Count the fastest steady pulse per bar — "
                          "seven or nine means irregular.",
                          "Find the accent pattern: where is the LONG "
                          "group?",
                          "In vocal music, listen for ornamentation and "
                          "pitches between the piano's notes.",
                          "Describe old recordings' sound as evidence of "
                          "their technology."],
                "content": "<p>This region's signature is the "
                           "<strong>irregular (additive) metre</strong> "
                           "— equal fast pulses in unequal groups — and, "
                           "in Arabic music, the <strong>maqam</strong> "
                           "with its microtonal, heavily ornamented "
                           "melody. The gold questions use a real "
                           "recording made in Cairo in 1909.</p>"},
            "passages": ps,
            "problem_bank": {"bronze": bronze, "silver": silver,
                             "gold": gold},
            "worked_examples": worked}


def lesson3():
    """Africa."""
    ps = [
        passage("p-cross", "Bell against drum &middot; synthesised "
                "pattern (studio-built for this drill)", "cross_3v2.mp3",
                "_rotw_synth"),
        passage("p-layers", "Ensemble building in layers &middot; "
                "synthesised pattern", "layers_build.mp3", "_rotw_synth"),
        passage("p-callresp", "Lead drum and ensemble &middot; "
                "synthesised pattern", "call_response.mp3", "_rotw_synth"),
    ]
    bronze = [
        mc("p-callresp", "The texture alternates bar by bar. What is "
           "happening?",
           ["A lead drum plays a phrase alone, then the group answers — "
            "call and response",
            "Two groups play the same thing together throughout",
            "One drummer plays continuously", "The music keeps stopping"],
           0, "One bar of solo lead drum, one bar of ensemble answer: "
           "call and response, the fundamental conversation of African "
           "ensemble drumming (and of the music it fed, from gospel to "
           "funk).", None),
        mc("p-layers", "How does this piece begin and grow?",
           ["One pattern starts alone and new layers join one at a time",
            "Everything starts together at full power",
            "It gets steadily quieter", "The tempo increases each bar"],
           0, "The texture BUILDS: bell first, then shaker, then low "
           "drum, then high drum — each entry thickening the sound. "
           "Describing texture growth like this earns marks.", None),
        mc("p-cross", "The bell and the low drum are both repeating "
           "patterns. What is the general name for a short, constantly "
           "repeated pattern?",
           ["Ostinato", "Melody", "Cadence", "Drone"],
           0, "Each layer is an ostinato — a short pattern repeated "
           "over and over. African ensemble music stacks ostinati of "
           "different lengths to build its interlocking texture.", None),
        mc("p-layers", "Which layer enters FIRST?",
           ["The bell pattern", "The deep drum", "The shaker",
            "The high drum"],
           0, "The bell opens alone. In many West African traditions "
           "the iron bell carries the timeline — the reference pattern "
           "every other player locks onto.", None),
    ]
    silver = [
        mc("p-cross", "The bell divides the bar into THREE equal strokes "
           "while the drum divides the same bar into TWO. What is this "
           "device called?",
           ["Cross-rhythm — three against two",
            "Syncopation", "Rubato", "A drum fill"],
           0, "Both parts share the same bar but split it differently — "
           "3 against 2, the classic African cross-rhythm. Neither part "
           "is 'wrong'; the friction between them is the point.",
           ("crossrhythm-vs-mistake", 3,
            "It can sound like the players disagree, but both patterns "
            "repeat perfectly — the clash of three against two is "
            "deliberate, sustained and structural: cross-rhythm.")),
        mc("p-layers", "What is the correct order of entries?",
           ["Bell, shaker, low drum, high drum",
            "Low drum, bell, high drum, shaker",
            "Shaker, bell, high drum, low drum",
            "High drum, low drum, shaker, bell"],
           0, "Bell (timeline) → shaker → low drum → high drum. "
           "Tracking entry order is a classic texture question — answer "
           "by register and timbre, in sequence.", None),
        mc("p-callresp", "In many traditions the lead (master) drummer's "
           "phrases do a JOB beyond decoration. What is it?",
           ["Signalling changes — cueing the ensemble and dancers",
            "Playing the tune", "Keeping the drone",
            "Providing harmony"],
           0, "The master drummer is the conductor: signal phrases tell "
           "the ensemble and the dancers when to change pattern, "
           "tempo or section. Leadership by rhythm, learned by ear.",
           None),
        mc("p-cross", "How is this music traditionally learned and "
           "passed on?",
           ["By ear and imitation — an oral tradition",
            "From printed notation", "From audio recordings only",
            "It is improvised from nothing each time"],
           0, "Traditional African drumming is an oral tradition: "
           "patterns pass from master to student by listening, "
           "imitation and correction — no notation involved.", None),
    ]
    gold = [
        mc("p-cross", "Musicians describe this texture as POLYRHYTHM. "
           "What makes that the precise term here?",
           ["Two or more conflicting rhythmic groupings sound "
            "simultaneously and continuously",
            "The music is merely fast",
            "The players take turns", "The metre changes bar by bar"],
           0, "Polyrhythm = simultaneous conflicting groupings (here 3 "
           "against 2) sustained as the texture's foundation — not "
           "taking turns, not tempo, not metre change.", None),
        mc("p-layers", "As each layer enters, what happens to the "
           "DENSITY of onsets (struck sounds per bar), and why does it "
           "matter for the dancers?",
           ["Density rises with each entry, driving intensity up — "
            "dancers respond to the thickening groove",
            "Density falls", "Density is constant throughout",
            "Only the volume changes, not the density"],
           0, "Every added ostinato adds strokes per bar: the groove "
           "literally thickens. This staged intensification is choreo- "
           "graphic — dance and drumming escalate together.", None),
        mc("p-callresp", "An exam asks you to COMPARE this call-and- "
           "response with the texture build in the previous excerpt. "
           "Which contrast earns the mark?",
           ["Alternation of solo and ensemble versus gradual "
            "accumulation of simultaneous layers",
            "Fast versus slow", "Loud versus quiet",
            "Regular versus irregular metre"],
           0, "Both are ensemble textures, but one is a conversation in "
           "TIME (solo, then answer) while the other stacks parts in "
           "SPACE (layer upon layer). Naming the mechanism, not the "
           "mood, is what scores.", None),
    ]
    worked = [{
        "difficulty": "silver",
        "question": "<p>Play the bell-against-drum excerpt below, then "
                    "follow the steps.</p>" + ps[0]["text"],
        "steps": [
            {"label": "Follow one layer at a time",
             "content": "<p>First tap with the bell alone: three even "
                        "strokes per bar. Then switch and tap with the "
                        "deep drum: two even strokes in the same "
                        "bar.</p>"},
            {"label": "Feel the clash",
             "content": "<p>Only the first stroke of the bar lines up. "
                        "After that the two patterns pull apart, then "
                        "meet again at the next bar line.</p>"},
            {"label": "Name the device",
             "content": "<p>Two simultaneous groupings of the same bar — "
                        "three against two — is cross-rhythm, the "
                        "building block of polyrhythmic texture.</p>"},
            {"label": "Answer",
             "content": "<p>Cross-rhythm (3 against 2), built from "
                        "repeating ostinati.</p>"},
        ]}]
    return {"exam_context": EXAM_CTX,
            "method_card": {
                "title": "What to listen for",
                "steps": ["Follow ONE layer at a time before judging the "
                          "whole texture.",
                          "Listen for conflicting groupings of the same "
                          "bar — that is cross-rhythm.",
                          "Track the ORDER in which layers enter.",
                          "Alternation = call and response; accumulation "
                          "= layered build."],
                "content": "<p>African ensemble drumming interlocks "
                           "<strong>ostinati</strong>: a bell timeline, "
                           "then layer upon layer, with "
                           "<strong>cross-rhythms</strong> pulling "
                           "against each other and a master drummer "
                           "steering by <strong>call and response"
                           "</strong>. Answer by mechanism: which "
                           "layers, entering when, grouped how.</p>"},
            "passages": ps,
            "problem_bank": {"bronze": bronze, "silver": silver,
                             "gold": gold},
            "worked_examples": worked}


def lesson4():
    """Central & South America. Gold = Dengozo 1923."""
    ps = [
        passage("p-samba", "Samba bateria groove &middot; synthesised "
                "pattern (studio-built for this drill)", "samba_groove.mp3",
                "_rotw_synth"),
        passage("p-tresillo", "3+3+2 pattern &middot; synthesised "
                "pattern", "tresillo_332.mp3", "_rotw_synth"),
        passage("p-march", "Straight march (contrast) &middot; "
                "synthesised pattern", "march_straight.mp3", "_rotw_synth"),
        passage("p-dengozo-a", "&lsquo;Dengozo&rsquo; (Ernesto Nazareth) "
                "&middot; Victor, 1923 &middot; public-domain recording",
                "gold_dengozo_a.mp3", "_rotw_goldcut"),
        passage("p-dengozo-b", "&lsquo;Dengozo&rsquo; &middot; second "
                "extract", "gold_dengozo_b.mp3", "_rotw_goldcut"),
    ]
    bronze = [
        mc("p-samba", "Listen for the deepest drum. Which beat does it "
           "hit hardest?",
           ["Beat 2 — the surdo's trademark", "Beat 1", "Every beat "
            "equally", "Off the beat entirely"],
           0, "The surdo, samba's bass heartbeat, lands heaviest on "
           "beat TWO of the 2/4 bar. That answering thump is what makes "
           "a samba walk feel different from a march.",
           ("surdo-beat-one", 1,
            "March logic says the big drum owns beat 1 — but listen "
            "again: samba's surdo answers on beat 2, and that "
            "displacement is the genre's signature.")),
        mc("p-march", "Compare this pattern with the samba groove. What "
           "is missing here?",
           ["Syncopation — every stroke lands squarely on the beat",
            "A steady pulse", "Drums", "A duple metre"],
           0, "This is the control experiment: bass drum on 1, snare on "
           "2, nothing pulling against the beat. Both are duple — the "
           "difference is syncopation.", None),
        mc("p-samba", "What is the fastest layer doing?",
           ["Running semiquavers — four quick strokes per beat",
            "One stroke per beat", "A waltz pattern",
            "Random free rhythm"],
           0, "The caixa (snare) sizzles in constant semiquavers — the "
           "16th-note carpet under the bateria that gives samba its "
           "momentum.", None),
        mc("p-tresillo", "Count the accented strokes against the steady "
           "pulse. The quavers group as:",
           ["3+3+2", "2+3+3", "4+4", "3+2+2"],
           0, "Three, three, two: the tresillo. The first two accents "
           "arrive later than a marching ear expects, then the final "
           "two-group snaps the bar shut.", None),
    ]
    silver = [
        mc("p-tresillo", "The 3+3+2 accents pull against the steady "
           "cowbell beat. What is this effect called?",
           ["Syncopation", "Cross-rhythm in three parts", "Rubato",
            "Polymetre"],
           0, "Accents displaced against a steady beat = syncopation. "
           "The 3+3+2 is the Caribbean's syncopation engine, driving "
           "calypso, reggaeton and much more.",
           ("syncopation-vs-crossrhythm", 1,
            "Cross-rhythm needs two simultaneous CONFLICTING groupings "
            "running independently. Here there is one steady beat with "
            "accents displaced against it — that is syncopation.")),
        mc("p-samba", "Which metre and subdivision is the samba groove "
           "built on?",
           ["Duple metre with semiquaver subdivision",
            "Triple metre with quaver subdivision",
            "Irregular 7/8", "Compound 6/8"],
           0, "Samba is emphatically duple (2/4) with the sixteenth-note "
           "engine running underneath — fast subdivision inside a "
           "simple metre, not an irregular one.", None),
        mc("p-samba", "In a full Rio bateria, who keeps the whole "
           "ensemble together and how?",
           ["A leader with whistle and hand signals cueing pattern "
            "changes",
            "A conductor with a baton and printed score",
            "Nobody — it is fully improvised",
            "A singer counting aloud"],
           0, "The mestre de bateria runs a drum orchestra of dozens "
           "with whistle blasts (the apito) and gestures — calls that "
           "cue breaks and pattern changes mid-parade.", None),
        mc("p-tresillo", "Which Caribbean genre took shape in Trinidad "
           "around verse-chorus songs and, later, steel pans — powered "
           "by exactly this kind of grouping?",
           ["Calypso", "Samba", "Flamenco", "Tango"],
           0, "Calypso: Trinidad's topical song tradition, driven by "
           "3+3+2 syncopation, later joined by the steel pan — the "
           "20th century's great new acoustic instrument.", None),
    ]
    gold = [
        mc("p-dengozo-a", "This 1923 disc records a maxixe — the "
           "Brazilian dance that fed into samba. Is its metre duple or "
           "triple, and how does it feel?",
           ["Duple — two beats per bar, heavily syncopated",
            "Triple — a waltz feel", "Irregular sevens",
            "Free rhythm"],
           0, "The maxixe struts in syncopated duple time — the same "
           "2/4 framework samba inherited. Feel the two-step underneath "
           "the busy surface.",
           ("maxixe-waltz", 1,
            "A smoother middle strain can drift towards a lilting feel, "
            "but track the dance step underneath: it is two beats per "
            "bar throughout — a syncopated duple, not a waltz.")),
        mc("p-dengozo-a", "The lead melody is played on struck wooden "
           "bars. Which instrument is this?",
           ["Marimba", "Clarinet", "Piano", "Accordion"],
           0, "A marimba band led this Victor disc: wooden bars struck "
           "with mallets, bright attack, quick decay. (On worn early "
           "recordings the attack can fool the ear — listen for the "
           "woody ring under the crackle.)", None),
        mc("p-dengozo-b", "The rhythm section keeps placing accents "
           "just off the strong beats. Which written figure captures "
           "the maxixe's characteristic cell?",
           ["A semiquaver-quaver-semiquaver snap inside each beat",
            "Four even crotchets", "A dotted minim per bar",
            "Straight quavers with no accents"],
           0, "The maxixe (like its cousins the habanera and tango "
           "brasileiro) lives on the short-LONG-short cell — the snap "
           "that displaces weight inside the beat and points straight "
           "towards samba.", None),
        mc("p-dengozo-b", "What does the sound of this disc tell you "
           "about its recording technology, and why does that matter "
           "for what you can hear?",
           ["Acoustic horn recording: limited frequency range, so bass "
            "instruments and subtle dynamics are hard to capture",
            "Digital remastering has removed all noise",
            "Stereo microphones separate the instruments",
            "Electric amplification boosts the bass"],
           0, "1923 sits at the very end of the acoustic era: horn-"
           "captured, narrow-band, bass-light. When you describe early "
           "recordings in the exam, connecting SOUND to TECHNOLOGY is "
           "exactly the point the mark scheme rewards.", None),
    ]
    worked = [{
        "difficulty": "bronze",
        "question": "<p>Play the samba groove below, then follow the "
                    "steps.</p>" + ps[0]["text"],
        "steps": [
            {"label": "Find the two-beat walk",
             "content": "<p>Step left-right with the music: it fits a "
                        "steady two. Samba is duple, whatever the "
                        "surface is doing.</p>"},
            {"label": "Find the deepest drum",
             "content": "<p>The surdo booms once per bar louder than "
                        "everything else. Notice WHERE: on the second "
                        "step, not the first.</p>"},
            {"label": "Hear the engine underneath",
             "content": "<p>Under the booms, the snare runs four quick "
                        "strokes per beat — the semiquaver engine that "
                        "keeps the groove rolling.</p>"},
            {"label": "Answer",
             "content": "<p>Duple metre; surdo accenting beat 2; "
                        "semiquaver subdivision in the snare — three "
                        "concrete features worth three marks.</p>"},
        ]}]
    return {"exam_context": EXAM_CTX,
            "method_card": {
                "title": "What to listen for",
                "steps": ["Confirm the metre first — these dances are "
                          "duple.",
                          "Find which beat the deepest drum owns.",
                          "Listen for 3+3+2 accents pulling against the "
                          "pulse.",
                          "On old discs, describe the recording "
                          "technology as well as the music."],
                "content": "<p>The Americas' signature is "
                           "<strong>syncopation inside a duple frame"
                           "</strong>: the surdo answering on beat 2, "
                           "semiquavers underneath, and the 3+3+2 "
                           "<strong>tresillo</strong>. The gold "
                           "questions use a real 1923 recording of a "
                           "maxixe — the dance that became samba.</p>"},
            "passages": ps,
            "problem_bank": {"bronze": bronze, "silver": silver,
                             "gold": gold},
            "worked_examples": worked}


LESSONS = [
    (1, "India and Punjab — Rhythm Drills",
     "Count tala cycles and feel the bhangra chaal: swung quavers, "
     "sixteen-beat cycles and the empty khali group.", lesson1),
    (2, "Eastern Mediterranean and Middle East — Rhythm Drills",
     "Irregular dance metres in seven and nine, dum and tek, and a real "
     "1909 Cairo recording of ornamented maqam singing.", lesson2),
    (3, "African Drumming — Rhythm Drills",
     "Cross-rhythm, layered ostinati, call and response and the master "
     "drummer's signals.", lesson3),
    (4, "Samba, Calypso and the Americas — Rhythm Drills",
     "Surdo on beat two, the 3+3+2 tresillo, and a real 1923 recording "
     "of the maxixe — samba's ancestor.", lesson4),
]


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id,settings").eq("slug", "music-ocr") \
        .execute().data[0]
    units = sb.table("units").select("id,slug,sort_order,subject_id") \
        .execute().data
    mine = [u for u in units if u["subject_id"] == sub["id"]]
    have = {u["slug"] for u in mine}
    if "aos3-rhythms-listening" not in have:
        print("unit missing — will create (sort 5, bumping later units)")
    for n, title, desc, fn in LESSONS:
        pd = fn()
        counts = {t: len(v) for t, v in pd["problem_bank"].items()}
        print("L%d %s | passages %d | %s | worked %d"
              % (n, title[:42], len(pd["passages"]), counts,
                 len(pd["worked_examples"])))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if "aos3-rhythms-listening" not in have:
        for u in mine:
            if u["sort_order"] >= 5:
                sb.table("units").update({"sort_order": u["sort_order"] + 1}) \
                    .eq("id", u["id"]).execute()
        r = sb.table("units").insert({
            "subject_id": sub["id"], "slug": "aos3-rhythms-listening",
            "name": "Area of Study 3: Listening Practice",
            "subtitle": "Rhythm drills for every region — plus real "
                        "century-old recordings",
            "sort_order": 5, "accent": "#7c3aed",
            "accent_light": "#7c3aed22", "accent_badge": "#7c3aed33",
            "body_class": "unit-music-ocr-aos3-listening",
        }).execute()
        uid = r.data[0]["id"]
    else:
        uid = next(u["id"] for u in mine
                   if u["slug"] == "aos3-rhythms-listening")
    settings = sub.get("settings") or {}
    pu = settings.get("practice_units") or []
    if "aos3-rhythms-listening" not in pu:
        pu.append("aos3-rhythms-listening")
        settings["practice_units"] = pu
        sb.table("subjects").update({"settings": settings}) \
            .eq("id", sub["id"]).execute()
    existing = {r["lesson_number"] for r in sb.table("lessons")
                .select("lesson_number").eq("unit_id", uid).execute().data}
    for n, title, desc, fn in LESSONS:
        if n in existing:
            print("L%d exists — skipped" % n)
            continue
        sb.table("lessons").insert({
            "unit_id": uid, "lesson_number": n, "slug": "lesson-%02d" % n,
            "title": title, "description": desc, "practice_data": fn(),
            "status": "pending_review",
        }).execute()
        print("L%d inserted" % n)
    print("done")


if __name__ == "__main__":
    main()
