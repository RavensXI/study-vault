"""Pattern sweep (24 Sep 2026): two fault shapes the 1EN2 student walk found, checked on
every English Language subject. 1) spot_error tokens where the same word ends one token
and starts the next ('threw' / 'threw ...'). 2) improve_sentence / ai_write tasks with an
extract on screen but no own-words rule in the stem or marking prompt."""
import os, json, re, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]; H = {"apikey": K, "Authorization": "Bearer " + K}
def get(p): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H)).read())
OWN = re.compile(r"own (words|images|details|imagery|writing|invention)|do not (reuse|copy|lift)|lifted|borrow|verbatim|reproduce", re.I)
for sub in ["english-language-aqa", "english-language-edexcel", "english-language-ocr", "english-language-eduqas", "english-language", "english-language-2-edexcel"]:
    rows = get("lessons?select=lesson_number,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s" % sub)
    dup, own, n = [], [], 0
    for r in rows:
        pd = r["practice_data"] or {}; bank = pd.get("problem_bank") or {}
        pas = {p.get("id") for p in (pd.get("passages") or [])}
        for tier, qs in bank.items():
            for i, q in enumerate(qs or []):
                n += 1; key = "%s/%s/%s/%s" % (r["units"]["slug"], r["lesson_number"], tier, i)
                t = q.get("input_type") or q.get("type")
                if t == "spot_error":
                    toks = [x.get("text", "") for x in q.get("tokens") or []]
                    for a, b in zip(toks, toks[1:]):
                        wa, wb = re.findall(r"[A-Za-z']+", a), re.findall(r"[A-Za-z']+", b)
                        if wa and wb and wa[-1].lower() == wb[0].lower() and len(wa[-1]) > 2: dup.append((key, wa[-1]))
                if t in ("improve_sentence", "ai_write") and (q.get("passage_id") or q.get("passage")):
                    if not OWN.search((q.get("question") or "") + " " + (q.get("marking_prompt") or "")): own.append(key)
    print("%-28s questions %4d | token repeats %d | extract tasks without own-words rule %d" % (sub, n, len(dup), len(own)))
    for d in dup: print("   repeat:", d)
    for o in own[:40]: print("   own-words:", o)
