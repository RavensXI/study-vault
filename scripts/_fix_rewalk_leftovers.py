"""Faults left after the English Language 2.0 re-walk (22 Sep 2026), and the one live twin.

  - "any休day": a stray CJK character (休 = rest) in a Paper 1 reading passage -> "any rest day".
  - "Identify the sentence in Model C that uses a semicolon": the options were all error-riddled
    sentences from Model B and the stored answer had no semicolon at all. Rebuilt from Model C's own
    sentences. The same broken question is live in english-language-edexcel paper-2-writing/10.
  - "a missing comma and a missing word": the only stored error is 'diffrence' (spelling, plus the
    comma after it). Stem now says so.
  - "Which statement about planning narratives is good advice?" over a click-the-wrong-ones control.
  - a green/amber/red stem worded as supported/not supported over True/Partly true/False labels.
"""
import io, json, os, re, sys, time, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(p): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H), timeout=120).read())
def lesson(sub, unit, n):
    sid = get("subjects?select=id&slug=eq." + sub)[0]["id"]
    return get("lessons?select=id,practice_data,units!inner(slug,subject_id)&units.subject_id=eq.%s&units.slug=eq.%s&lesson_number=eq.%d" % (sid, unit, n))[0]
apply = "--apply" in sys.argv
backup, todo = {}, {}
def take(sub, unit, n):
    L = lesson(sub, unit, n)
    if L["id"] not in todo:
        backup[L["id"]] = json.loads(json.dumps(L["practice_data"])); todo[L["id"]] = L
    return todo[L["id"]]["practice_data"]

pd = take("english-language-2-edexcel", "paper-1-reading", 6)
for p in pd["passages"]:
    if "any休day" in p["text"]:
        p["text"] = p["text"].replace("any休day", "any rest day"); print("TEXT     p1r/6 %s: any rest day" % p["id"])

SEMI = "Transport costs have risen; insurance requirements have tightened; staff are reluctant to give up their weekends."
for sub, unit in [("english-language-2-edexcel", "paper-1-writing"), ("english-language-edexcel", "paper-2-writing")]:
    pd = take(sub, unit, 10)
    c = [p for p in pd["passages"] if p["id"] == "gold"][0]["text"].replace("\n", " ")
    sents = re.split(r"(?<=[.!?])\s+", c)
    colon = next(s for s in sents if ":" in s and "Dear" not in s)
    dash = next(s for s in sents if "—" in s and ":" not in s)
    comma = next(s for s in sents if s.startswith("These are real constraints"))
    assert SEMI in c, sub
    q = pd["problem_bank"]["silver"][2]
    assert "semicolon" in q["question"]
    q["options"] = [SEMI, colon.strip(), dash.strip(), comma.strip()]
    q["solutions"] = [0]; q["passage_id"] = "gold"
    q.pop("misconceptions", None)
    q["explain"] = ("Each part of 'Transport costs have risen; insurance requirements have tightened; staff are reluctant to give up "
                    "their weekends' could stand as a sentence on its own, and the semicolons join them because they are closely related. "
                    "The other sentences use a colon to introduce a list, a dash to add an aside, and a comma with 'and' to join two clauses.")
    print("OPTIONS  %s %s/10 silver[2]: rebuilt from Model C" % (sub, unit))

pd = take("english-language-2-edexcel", "paper-1-writing", 11)
q = pd["problem_bank"]["silver"][6]; assert "missing word" in q["question"]
q["question"] = "This sentence from Model A has a spelling mistake and a missing comma, both at the same word. Find it."
print("STEM     p1w/11 silver[6]:", q["question"])

pd = take("english-language-2-edexcel", "paper-2-writing", 2)
q = pd["problem_bank"]["bronze"][4]; assert q["question"].startswith("Which statement about planning")
q["question"] = "Two of these pieces of advice about planning a narrative are wrong. Click each piece of bad advice."
print("STEM     p2w/2 bronze[4]:", q["question"])

pd = take("english-language-2-edexcel", "paper-2-reading", 8)
q = pd["problem_bank"]["bronze"][1]; assert "supported" in q["question"]
q["question"] = re.sub(r"fully supported by the text \(green\), partly supported \(amber\), or not supported at all", "true (green), partly true (amber) or false (red)", q["question"])
print("STEM     p2r/8 bronze[1]:", q["question"][:120])

if apply:
    for lid, L in todo.items():
        urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/lessons?id=eq." + lid, data=json.dumps({"practice_data": L["practice_data"]}).encode(),
            headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()
    p = "scripts/_backup_rewalk_leftovers_%s.json" % time.strftime("%Y-%m-%d")
    io.open(p, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False)); print("written %d lessons, backup %s" % (len(todo), p))
else:
    print("dry run")
