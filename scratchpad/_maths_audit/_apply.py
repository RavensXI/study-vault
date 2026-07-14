"""Apply the audit's verified fixes to live maths-edexcel practice_data.

- Solution fixes: only entries where claimed_correct parses cleanly to a number
  or numeric pair AND the stored value still matches what the auditor saw
  (guard against drift). Anything else goes to the repair queue for the
  repair workflow (problem wording gets fixed, stored answer kept).
- Misconception enrichment: replaces each problem's misconceptions with the
  audited copy carrying `expect`; drops an expect that equals the correct
  solution (would never fire — matcher only runs on wrong answers — but keep
  the data honest).

Writes: _apply_log.json, _repair_queue.json. Requires SUPABASE_SERVICE_KEY.
"""
import json, io, os, re, sys, urllib.request

sys.stdout.reconfigure(errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUD = os.path.join(ROOT, "scratchpad", "_maths_audit")
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

def req(method, path, body=None):
    r = urllib.request.Request(SUPA + path, method=method,
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"},
        data=json.dumps(body).encode() if body is not None else None)
    return urllib.request.urlopen(r)

def parse_claim(s):
    s = s.strip()
    m = re.fullmatch(r"\[?\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]?", s)
    if m: return [float(m.group(1)), float(m.group(2))]
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", s)
    if m: return [float(s)]
    return None

def norm(v):
    out = []
    for x in (v if isinstance(v, list) else [v]):
        try: out.append(float(x))
        except (TypeError, ValueError): return None
    return out

def close(a, b):
    return a is not None and b is not None and len(a) == len(b) and all(abs(x - y) < 1e-9 for x, y in zip(a, b))

lessons = {}
for r in json.load(io.open(os.path.join(ROOT, "scratchpad", "_maths_edexcel_practice.json"), encoding="utf-8")):
    key = r["units"]["slug"] + "-L%02d" % r["lesson_number"]
    lessons[key] = r

split = json.load(io.open(os.path.join(AUD, "_confirmed_split.json"), encoding="utf-8"))
log = {"solution_fixes": [], "enriched": 0, "expect_dropped": 0, "skipped": []}
repair_queue = list(split["rep"])
touched = set()

# ---- solution fixes ----
for d in split["sol"]:
    claim = parse_claim(d["claimed_correct"])
    prob = lessons[d["key"]]["practice_data"]["problem_bank"][d["tier"]][d["index"]]
    if claim is None:
        repair_queue.append(d); continue
    stored_now = norm(prob.get("solutions"))
    stored_seen = parse_claim(d["stored_solution"])
    if stored_seen is not None and not close(stored_now, stored_seen):
        log["skipped"].append({"key": d["key"], "tier": d["tier"], "index": d["index"],
                               "why": "stored solution drifted", "now": prob.get("solutions")})
        continue
    # ints stay ints where clean
    newsol = [int(x) if float(x).is_integer() else x for x in claim]
    log["solution_fixes"].append({"key": d["key"], "tier": d["tier"], "index": d["index"],
                                  "old": prob.get("solutions"), "new": newsol})
    prob["solutions"] = newsol
    touched.add(d["key"])

# ---- enrichment merge ----
for key, r in lessons.items():
    fn = os.path.join(AUD, "enrich_" + key + ".json")
    if not os.path.exists(fn):
        log["skipped"].append({"key": key, "why": "no enrich file"}); continue
    en = json.load(io.open(fn, encoding="utf-8"))
    bank = r["practice_data"]["problem_bank"]
    for ep in en.get("problems", []):
        try:
            prob = bank[ep["tier"]][ep["index"]]
        except (KeyError, IndexError):
            log["skipped"].append({"key": key, "why": "enrich index OOB", "at": [ep.get("tier"), ep.get("index")]})
            continue
        cur = prob.get("misconceptions") or []
        new = ep.get("misconceptions") or []
        if len(new) != len(cur):
            log["skipped"].append({"key": key, "why": "misconception count mismatch", "at": [ep["tier"], ep["index"]]})
            continue
        sols = norm(prob.get("solutions"))
        for m in new:
            e = m.get("expect")
            if e is not None and close(norm(e), sols):
                m["expect"] = None
                log["expect_dropped"] += 1
            if m.get("expect") is not None:
                log["enriched"] += 1
        prob["misconceptions"] = new
    touched.add(key)

# ---- push ----
print("lessons to update:", len(touched))
for key in sorted(touched):
    r = lessons[key]
    req("PATCH", "/rest/v1/lessons?id=eq." + r["id"], {"practice_data": r["practice_data"]})
    print("  patched", key)

json.dump(log, io.open(os.path.join(AUD, "_apply_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(repair_queue, io.open(os.path.join(AUD, "_repair_queue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("solution fixes:", len(log["solution_fixes"]), "| enriched expects:", log["enriched"],
      "| dropped expects:", log["expect_dropped"], "| skipped:", len(log["skipped"]), "| repair queue:", len(repair_queue))
for s in log["skipped"][:10]: print("  SKIP", s)
