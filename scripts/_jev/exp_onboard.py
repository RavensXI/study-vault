"""E14 - Onboarding from a pasted description. A student types or pastes what they study
("triple science aqa, edexcel maths, history with mr shaun doing elizabeth and germany...") and
Jev fills the wizard: which families, which board per family, which option topics. Hand-written
set of 40 with truth. Choice per family (board or 'not taken')."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Choice, Noul

FAMILIES = {"maths": "Maths", "lang": "English Language", "lit": "English Literature", "science": "Combined Science (double award)", "triple": "Separate sciences / triple science (biology, chemistry, physics as three GCSEs)",
            "history": "History", "geog": "Geography", "rs": "Religious Studies", "business": "Business", "cs": "Computer Science", "french": "French", "spanish": "Spanish", "german": "German", "pe": "PE / Physical Education", "psych": "Psychology", "music": "Music", "drama": "Drama", "food": "Food Preparation and Nutrition", "dt": "Design and Technology", "socio": "Sociology"}
BOARDS = {"aqa": "AQA", "edexcel": "Edexcel / Pearson", "ocr": "OCR / Cambridge", "eduqas": "Eduqas / WJEC", "unknown": "the board is not stated", "not_taken": "the student does not take this subject"}
SET = [
 ("i do triple science with aqa, edexcel maths, english lit and lang aqa, history aqa, french and rs", {"triple": "aqa", "maths": "edexcel", "lit": "aqa", "lang": "aqa", "history": "aqa", "french": "unknown", "rs": "unknown", "science": "not_taken"}),
 ("combined science, maths, english, geography (edexcel b) and business. everything else is aqa i think", {"science": "aqa", "maths": "aqa", "lang": "aqa", "lit": "aqa", "geog": "edexcel", "business": "aqa", "triple": "not_taken"}),
 ("Year 11. Subjects: Maths (Edexcel), English Language and Literature (AQA), Combined Science Trilogy (AQA), History (Edexcel), Spanish (AQA), Computer Science (OCR)", {"maths": "edexcel", "lang": "aqa", "lit": "aqa", "science": "aqa", "history": "edexcel", "spanish": "aqa", "cs": "ocr", "triple": "not_taken"}),
 ("im doing the sciences separately (bio chem phys) all ocr gateway, maths ocr, english eduqas, and pe", {"triple": "ocr", "science": "not_taken", "maths": "ocr", "lang": "eduqas", "lit": "eduqas", "pe": "unknown"}),
 ("just maths and english im resitting them, edexcel maths and aqa english language", {"maths": "edexcel", "lang": "aqa", "lit": "not_taken", "science": "not_taken", "history": "not_taken"}),
 ("we do WJEC for everything cause im in wales. maths, english, science double, history, geography, welsh", {"maths": "eduqas", "lang": "eduqas", "lit": "eduqas", "science": "eduqas", "history": "eduqas", "geog": "eduqas", "triple": "not_taken"}),
 ("my options are psychology, sociology and drama. core is aqa for english and science, maths is edexcel", {"psych": "unknown", "socio": "unknown", "drama": "unknown", "lang": "aqa", "lit": "aqa", "science": "aqa", "maths": "edexcel"}),
 ("History: AQA, doing Elizabeth, Health and the People, Conflict and Tension, and America. Geography AQA. RE AQA spec A christianity and islam.", {"history": "aqa", "geog": "aqa", "rs": "aqa", "maths": "unknown"}),
 ("I take music (edexcel), food tech aqa, DT aqa, and the usual core - dont know the boards for core sorry", {"music": "edexcel", "food": "aqa", "dt": "aqa", "maths": "unknown", "lang": "unknown", "science": "unknown", "lit": "unknown"}),
 ("german edexcel, business edexcel, computer science aqa, plus maths lit lang and combined sci all aqa", {"german": "edexcel", "business": "edexcel", "cs": "aqa", "maths": "aqa", "lit": "aqa", "lang": "aqa", "science": "aqa", "triple": "not_taken"}),
 ("dunno the boards, i do maths english science history and french", {"maths": "unknown", "lang": "unknown", "lit": "unknown", "science": "unknown", "history": "unknown", "french": "unknown", "geog": "not_taken"}),
 ("my school does everything with edexcel except science which is aqa and english which is eduqas. i take geography and pe as options", {"maths": "edexcel", "science": "aqa", "lang": "eduqas", "lit": "eduqas", "geog": "edexcel", "pe": "edexcel", "history": "not_taken"}),
]
items = [{"i": i, "text": t, "truth": tr} for i, (t, tr) in enumerate(SET)]
def build(it):
    qs = {}
    for fam, label in FAMILIES.items():
        qs[fam] = Choice(instructions="Which exam board does the student sit for %s? Pick not_taken if they do not study it, unknown if they study it but no board can be inferred for it." % label, criteria=BOARDS)
    return ({"student_message": it["text"], "notes": "A school usually uses one board per subject; 'english' alone means both English Language and English Literature; 'science' or 'combined' or 'double' means Combined Science, 'triple' or 'separate' or listing biology chemistry physics means separate sciences; 'core' means maths, English and science."}, qs)
res = ask_many(items, build, tag="onboard", workers=4)
rows = []; right = total = 0; conf_right = collections.defaultdict(lambda: [0, 0])
for it, r, err in res:
    if not r: continue
    a = answers(r); got = {k: (v["choice"], v["confidence"]) for k, v in a.items()}
    for fam, truth in it["truth"].items():
        total += 1; ok = got[fam][0] == truth; right += ok
        band = "high" if got[fam][1] >= 0.8 else ("mid" if got[fam][1] >= 0.5 else "low"); conf_right[band][0] += ok; conf_right[band][1] += 1
    rows.append({"text": it["text"], "truth": it["truth"], "jev": {k: v[0] for k, v in got.items()}, "conf": {k: round(v[1], 2) for k, v in got.items()},
                 "wrong": {k: [tr, got[k][0]] for k, tr in it["truth"].items() if got[k][0] != tr}})
summary = {"messages": len(rows), "labelled_fields": total, "right": right, "accuracy": round(right / max(total, 1), 3), "by_confidence": {k: {"right": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 3)} for k, v in conf_right.items()},
           "wrong_fields": [{"text": r["text"][:70], "wrong": r["wrong"]} for r in rows if r["wrong"]]}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("onboard.json", {"summary": summary, "rows": rows})
