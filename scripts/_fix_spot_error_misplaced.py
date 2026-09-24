"""spot_error misplaced error tokens (24 Sep 2026). The builder wrote an error word into the
sentence AND added it again as a separate clickable token elsewhere, so a pupil saw
'there knowledge there is' or 'Their are many ways Their to get involved'. Each question's
tokens are rebuilt: a string is a plain token, an int keeps that original error token
(its correction and explanation) in its right place. Dry run unless --apply; backup on apply."""
import os, sys, json, time, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]; H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(p): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H)).read())
FIX = [
 ("english-language-edexcel", "paper-1-writing", 5, "silver", 4,
  [0, "Selene's character by showing how her dad's job has ", "affected ", "her whole life. The ", 4,
   "of the keys as a library suggests that ", 6, "knowledge is like a shared language. The reader ", 8,
   "that Selene is independent and resourceful."], None),
 ("english-language-edexcel", "paper-1-writing", 10, "bronze", 1,
  [0, "important to proofread ", 2, "work before handing it in. Many ", 4, 6,
   "marks because of basic errors that ", 8, "been avoided."], None),
 ("english-language-edexcel", "paper-1-writing", 12, "silver", 3,
  ["Zain stood in the wings with his violin, ", 1, "the girl playing before him and she was ", 3,
   "good. His hands were sweating and he felt like he ", 5, 7,
   ". When it was his turn, he walked on stage and played his piece."], {7: ("of come", "have come")}),
 ("english-language-edexcel", "paper-1-writing", 1, "silver", 4,
  ["The writer creates a ", 1, "of neglect through ", 3, "description of the house. The wallpaper peeling to ", 5,
   "older layers suggest that many people have lived here before, ", 7, "Priya feel like an outsider in the house."], None),
 ("english-language-2-edexcel", "paper-2-writing", 1, "silver", 4,
  ["The writer creates a ", 1, "of neglect through ", 3, "description of the house. The wallpaper peeling to ", 5,
   "older layers suggest that many people have lived here before, ", 7, "Priya feel like an outsider in the house."], None),
 ("english-language-ocr", "component-1-writing", 9, "bronze", 5,
  ["Volunteering is a great way to ", 1, "people and make a difference in ", 3, "community. ", 5,
   "are many ways to get involved, ", 7, "you have a little time or a lot."], None),
 ("english-language-ocr", "component-1-writing", 10, "silver", 5,
  [0, "anger throughout the article. ", 3, "vocabulary is precise and deliberate, which creates a sense of authority. The ", 5,
   "never becomes emotional or ranty, ", 7, "the argument more convincing."], None),
 ("english-language-ocr", "component-1-writing", 7, "silver", 5,
  [0, "techniques to argue that the town centre can be saved. ", 2, "that shops have closed, ", 4, 6,
   "argument more believable because the reader can see they are being honest about the problems."], None),
 ("english-language-ocr", "component-2-writing", 9, "bronze", 7,
  ["The narrator uses ", 1, " tone to describe their first day.", " This is shown when they describe writing the date neatly on a blank page,",
   " which reveals their sense of being out of their depth."], {1: ("an angry, bitter", "a dry, self-deprecating")}),
 ("english-language-edexcel", "paper-2-writing", 12, "silver", 6, "COPY_1EN2", None),
]
APPLY = "--apply" in sys.argv; backup = {}; rows = {}
for sub, unit, n, tier, i, spec, retext in FIX:
    key = (sub, unit, n)
    if key not in rows:
        rows[key] = get("lessons?select=id,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s&units.slug=eq.%s&lesson_number=eq.%s" % key)[0]
        backup[rows[key]["id"]] = json.loads(json.dumps(rows[key]["practice_data"]))
    q = rows[key]["practice_data"]["problem_bank"][tier][i]; old = q["tokens"]
    if spec == "COPY_1EN2":
        src = get("lessons?select=practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.english-language-2-edexcel&units.slug=eq.paper-1-writing&lesson_number=eq.12")[0]["practice_data"]["problem_bank"]["silver"][6]
        assert "".join(t["text"] for t in src["tokens"]) == "".join(t["text"] for t in old), "texts differ"
        q["tokens"], q["question"] = src["tokens"], src["question"]
    else:
        new = []
        for s in spec:
            if isinstance(s, str): new.append({"text": s, "error": False})
            else:
                t = dict(old[s]); assert t.get("error"), (key, s)
                if retext and s in retext: t["text"], t["correction"] = retext[s]
                new.append(t)
        # the sentence must now read as the old one with the stray copy removed: no word lost
        assert sum(1 for t in new if t.get("error")) == sum(1 for t in old if t.get("error")), key
        q["tokens"] = new
    print("%s/%s/%s/%s/%s\n  before: %s\n  after:  %s" % (sub, unit, n, tier, i, "".join(t["text"] for t in old), "|".join(("[%s]" % t["text"]) if t.get("error") else t["text"] for t in q["tokens"])))
if APPLY:
    json.dump(backup, open("scripts/_backup_spot_error_misplaced_%s.json" % time.strftime("%Y-%m-%d"), "w", encoding="utf-8"), ensure_ascii=False)
    for r in rows.values():
        urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/lessons?id=eq." + r["id"], data=json.dumps({"practice_data": r["practice_data"]}).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH")).read()
    print("applied to", len(rows), "lessons")
