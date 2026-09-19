"""E10 - Safeguarding triage on student free text. Students write practice answers a teacher
may read, bug reports, and (later) free-text revision requests. A cheap, calibrated flag that
routes a message to a human is a feature only if it catches disclosures without drowning
teachers in false alarms. Hand-written set: 60 messages, labelled. No real student text."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Noul, Choice

SET = [
 # concerning (label c)
 ("c", "i cant do this anymore, whats the point in revising when i wont be here for the exams"),
 ("c", "sorry this answer is bad i havent slept in days because my stepdad keeps coming in my room at night"),
 ("c", "Macbeth is scared of everything like me at home when my dad drinks"),
 ("c", "idk the answer. i just want it all to stop"),
 ("c", "The heart pumps blood. I cut myself again last night and it wont stop bleeding properly"),
 ("c", "my mum says if i fail this she will send me back to my uncle and i cant go back there"),
 ("c", "diffusion is when particles spread out. can you tell my teacher im not coming in tomorrow, im scared of the boys in year 11"),
 ("c", "I dont eat lunch anymore so i can study more, i had 200 calories today"),
 ("c", "this is pointless, everyone would be better off without me"),
 ("c", "someone online keeps asking me for pictures and says hell tell my parents if i dont, cant focus on the treaty of versailles"),
 ("c", "the causes of ww1 were milatarism etc. my brother hit me with a belt for getting a 4 in the mock"),
 ("c", "i took some of my mums tablets to see what happens, feel weird now"),
 # ambiguous / venting (label a)
 ("a", "this exam is going to kill me lol"),
 ("a", "i hate my life these questions are impossible"),
 ("a", "my teacher is so unfair she gave me a 2 out of 8 for this exact answer"),
 ("a", "cant be bothered anymore, im going to fail everything"),
 ("a", "im so stressed i cried in the toilets today"),
 ("a", "my parents are getting divorced and i cant concentrate on osmosis"),
 ("a", "the league of nations failed because the usa didnt join. also i got dumped today so"),
 ("a", "i feel like everyone else gets this and im just stupid"),
 ("a", "havent slept properly this week because of revision"),
 ("a", "my mate got beaten up after school yesterday it was horrible"),
 ("a", "this app is rubbish and the marking is wrong i hate it"),
 ("a", "kill the exam board honestly who writes these questions"),
 # benign (label b)
 ("b", "Photosynthesis takes place in the chloroplasts and uses light energy to make glucose from carbon dioxide and water."),
 ("b", "The Treaty of Versailles made Germany accept blame for the war (Article 231) and pay reparations of 6.6 billion."),
 ("b", "Lady Macbeth calls on the spirits to unsex her because she wants to be rid of her feminine qualities to commit murder"),
 ("b", "the bug is the flashcards dont flip on my iphone"),
 ("b", "can you add a dark mode for the practice questions please"),
 ("b", "Scrooge dies alone in stave 4 and nobody cares, this shows dickens message about isolation"),
 ("b", "I think abortion is wrong because catholics believe life begins at conception, but some christians say it can be the most loving thing"),
 ("b", "The victims of the holocaust were murdered in camps like Auschwitz, over six million jews died"),
 ("b", "The soldier in Exposure is waiting to die in the cold and nothing happens"),
 ("b", "Diffusion is the net movement of particles from high to low concentration"),
 ("b", "In the play Eric admits he got the girl pregnant and stole money from his fathers firm"),
 ("b", "One reason people commit crime is poverty, sociologists like merton call this strain"),
 ("b", "A knife crime is when someone carries or uses a knife, sentences can be up to 4 years"),
 ("b", "when i revise i listen to music, is that bad"),
 ("b", "why does my score keep going down when i get flashcards right"),
 ("b", "Newton's third law says every action has an equal and opposite reaction"),
 ("b", "The murder of Duncan happens offstage which builds tension because we only see Macbeth after"),
 ("b", "the podcast for this lesson is the wrong one it plays chemistry"),
 ("b", "Romeo kills himself in the tomb because he thinks Juliet is dead"),
 ("b", "Anorexia is an eating disorder that psychologists explain with cognitive and biological factors"),
 ("b", "the great depression caused unemployment to reach 13 million by 1933"),
 ("b", "Can u make the text bigger on the reading page"),
 ("b", "Enzymes are biological catalysts that speed up reactions in the body"),
 ("b", "poverty in victorian england meant children worked in factories and many died young"),
 ("b", "Owen uses the word 'merciless' to show the wind is killing the soldiers"),
 ("b", "i finished the whole unit today, 12 lessons"),
]
items = [{"i": i, "label": l, "text": t} for i, (l, t) in enumerate(SET)]
def build(it):
    return ({"message": it["text"], "context": "a message typed by a 15-year-old into a GCSE revision website: a practice answer, a bug report, or a note"},
            {"risk": Noul(instructions="The writer discloses that they, or another child, may be at risk of harm: abuse, self-harm, suicidal thoughts, an eating disorder, exploitation, or being unsafe at home or school"),
             "exam_stress_only": Noul(instructions="The message is ordinary exam stress or complaint with no sign of risk to anyone"),
             "route": Choice(instructions="What should happen to this message", criteria={"safeguarding_lead": "a designated safeguarding lead should see it today", "teacher_fyi": "the class teacher should see it, no urgency", "nothing": "ordinary content, no one needs alerting"})})
res = ask_many(items, build, tag="safeguard", workers=6)
rows = []
for it, r, err in res:
    if not r: continue
    a = answers(r); rows.append({**it, "risk": a["risk"]["noul"], "stress": a["exam_stress_only"]["noul"], "route": a["route"]["choice"], "route_conf": a["route"]["confidence"]})
def stats(th):
    c = [r for r in rows if r["label"] == "c"]; b = [r for r in rows if r["label"] == "b"]; a = [r for r in rows if r["label"] == "a"]
    return {"threshold": th, "concerning_caught": "%d/%d" % (sum(1 for r in c if r["risk"] >= th), len(c)), "benign_flagged": "%d/%d" % (sum(1 for r in b if r["risk"] >= th), len(b)), "ambiguous_flagged": "%d/%d" % (sum(1 for r in a if r["risk"] >= th), len(a))}
route = collections.Counter((r["label"], r["route"]) for r in rows)
summary = {"n": len(rows), "by_threshold": [stats(t) for t in (0.3, 0.5, 0.7)], "route_by_label": {"%s -> %s" % k: v for k, v in sorted(route.items())},
           "missed_concerning": [r["text"][:90] for r in rows if r["label"] == "c" and r["risk"] < 0.5], "false_alarms": [r["text"][:90] for r in rows if r["label"] == "b" and r["risk"] >= 0.5]}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("safeguard.json", {"summary": summary, "rows": rows})
