"""spot_error doubled words (24 Sep 2026). The builder sometimes wrote an error word into the
token before the error token as well, so a pupil saw 'threw threw' or 'Their are many ways
Their'. Finds every error token whose text also appears as a whole phrase in the previous
token and removes the copy from the previous token. Dry run unless --apply; backup on apply."""
import os, sys, json, re, time, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]; H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(p): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H)).read())
APPLY = "--apply" in sys.argv
SUBS = [s["slug"] for s in get("subjects?select=slug&slug=like.english-language*")] + \
       [s["slug"] for s in get("subjects?select=slug&or=(slug.like.*english*,slug.like.*spanish*,slug.like.*french*,slug.like.*german*)&slug=not.like.english-language*")]
backup, hits = {}, 0
for sub in SUBS:
    for r in get("lessons?select=id,lesson_number,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s" % sub):
        pd = r["practice_data"] or {}; changed = False
        for tier, qs in (pd.get("problem_bank") or {}).items():
            for i, q in enumerate(qs or []):
                toks = q.get("tokens") or []
                for j in range(1, len(toks)):
                    t, prev = toks[j], toks[j - 1]
                    if not t.get("error") or prev.get("error"): continue
                    w = (t.get("text") or "").strip()
                    if not w: continue
                    pt = prev.get("text") or ""
                    m = list(re.finditer(r"(?<![\w'])" + re.escape(w) + r"(?![\w'])\s*$", pt))
                    if not m: continue
                    hits += 1
                    new = pt[:m[-1].start()]
                    print("%s/%s/%s/%s/%s  %r + %r  ->  %r + %r" % (sub, r["units"]["slug"], r["lesson_number"], tier, i, pt, t["text"], new, t["text"]))
                    if new.strip() == "": print("   !! would empty the token; skipped"); continue
                    backup.setdefault(r["id"], json.loads(json.dumps(r["practice_data"])))
                    prev["text"] = new; changed = True
        if changed and APPLY:
            urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/lessons?id=eq." + r["id"], data=json.dumps({"practice_data": pd}).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH")).read()
print("doubled words:", hits, "| lessons:", len(backup), "| applied" if APPLY else "| dry run")
if APPLY and backup: json.dump(backup, open("scripts/_backup_spot_error_dupes_%s.json" % time.strftime("%Y-%m-%d"), "w", encoding="utf-8"), ensure_ascii=False)
