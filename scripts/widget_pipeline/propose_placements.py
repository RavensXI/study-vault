"""Propose an embed-strip placement for every lesson in the stage-1 clusters.

For each target lesson, fetch content_html, split it at <h2> headings, and
score each section's word overlap against the triage misconception text for
that lesson. The winning heading becomes the strip's `after:` anchor
(the strip sits immediately before that heading, i.e. after the section
where the misconception lives ends... the embed inserts BEFORE the matched
h2, so we anchor on the heading FOLLOWING the best section where one
exists, else the best-matching heading itself).

Output: _placements_%s.json  {cluster_id: [{key, after, title, score}]}
"""
import json, io, os, re, urllib.request

import sys
CLUSTERS = sys.argv[1:] or [
    "greenhouse-effect-reemission-not-blanket", "current-not-used-up",
    "state-change-energy-plateau", "synapse-electrical-to-chemical",
    "conservation-of-energy-dispersal"]

SB = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_ANON_KEY"]

def sb_get(path):
    req = urllib.request.Request(SB + path, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

STOP = set("the a an of to in and or is are was were be been it its this that "
           "with for on as at by from into not no does do can will would has "
           "have had more most than then when where which who whose why how "
           "they them their there here also so such may might must".split())

def words(t):
    return set(w for w in re.findall(r"[a-z']+", t.lower()) if w not in STOP and len(w) > 2)

s = json.load(io.open("_corpus_audit.json", encoding="utf-8"))
yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
by_key = {(l["subject"], l["unit"], l["n"]): l for l in yes}
clusters = {c["id"]: c for c in s["clusters"]}

out = {}
for cid in CLUSTERS:
    c = clusters[cid]
    rows = []
    for l in c["lessons"]:
        full = by_key.get((l["subject"], l["unit"], l["n"]))
        probe = words((full["triage"].get("misconception") or "") + " " +
                      (full["triage"].get("idea") or "")) if full else set()
        if not full:
            rows.append({"key": "%s/%s/%s" % (l["subject"], l["unit"], l["n"]),
                         "after": None, "error": "not in state"}); continue
        try:
            recs = sb_get("/rest/v1/lessons?select=content_html,title&id=eq.%s&limit=1"
                          % full["lesson_id"])
        except Exception as e:
            rows.append({"key": "%s/%s/%s" % (l["subject"], l["unit"], l["n"]),
                         "after": None, "error": str(e)[:80]}); continue
        if not recs or not recs[0].get("content_html"):
            rows.append({"key": "%s/%s/%s" % (l["subject"], l["unit"], l["n"]),
                         "after": None, "error": "no content"}); continue
        html = recs[0]["content_html"]
        # sections: [(heading, text-after-it)]
        parts = re.split(r"<h2[^>]*>(.*?)</h2>", html, flags=re.S)
        heads = []
        for i in range(1, len(parts), 2):
            head = re.sub(r"<[^>]+>", "", parts[i]).strip()
            body = re.sub(r"<[^>]+>", " ", parts[i + 1] if i + 1 < len(parts) else "")
            heads.append((head, words(body)))
        best, bscore = None, -1.0
        for idx, (head, bw) in enumerate(heads):
            sc = len(probe & bw) / max(1, len(probe))
            if sc > bscore:
                best, bscore = idx, sc
        # anchor on the heading AFTER the best section, so the strip lands
        # at the end of the passage it illuminates; last section -> anchor
        # on its own heading (strip sits at the section start instead)
        anchor = heads[best + 1][0] if best is not None and best + 1 < len(heads) \
                 else (heads[best][0] if best is not None else None)
        rows.append({"key": "%s/%s/%s" % (l["subject"], l["unit"], l["n"]),
                     "after": anchor, "score": round(bscore, 2),
                     "title": recs[0]["title"], "n_heads": len(heads)})
    out[cid] = rows
    ok = sum(1 for r in rows if r.get("after"))
    print("%s: %d/%d placed" % (cid, ok, len(rows)), flush=True)

OUT = "_placements_stage1.json" if not sys.argv[1:] else "_placements_custom.json"
io.open(OUT, "w", encoding="utf-8").write(
    json.dumps(out, indent=1, ensure_ascii=False))
print("wrote " + OUT)
