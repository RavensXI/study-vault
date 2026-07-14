"""Apply verified problem repairs on top of the already-enriched live rows.

- Fetches each lesson FRESH (the enrichment pass already changed rows).
- passed repairs apply directly; failed-check repairs apply only when the
  checker's own answer contains the repaired x-values (the known
  "x-values vs coordinate pairs" quibble on two_solutions problems).
- Derives m.expect from computable check names (equals_5/7, equals_-2_and_1,
  equals_3); non-computable checks keep expect null (matcher just skips).
"""
import json, io, os, re, sys, urllib.request

sys.stdout.reconfigure(errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

doc = json.load(io.open(r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\tasks\walu56dt1.output", encoding="utf-8"))
res = doc["result"]
passed = list(res.get("passed", []))
failed = res.get("failed", [])
print("passed:", len(passed), "| failed-check:", len(failed))

# salvage x-values quibbles: find the repair + verdict in agents? failed list has only item+note+answer.
# The repair details for failed items live in the repair_*.json files; match by display check.
repair_files = {}
import glob
for f in glob.glob(os.path.join(ROOT, "scratchpad", "_maths_audit", "repair_*.json")):
    try:
        j = json.load(io.open(f, encoding="utf-8"))
        repair_files[f] = j
    except Exception as e:
        print("  unreadable", f, e)

queue = json.load(io.open(os.path.join(ROOT, "scratchpad", "_maths_audit", "_repair_queue.json"), encoding="utf-8"))

def find_repair_for(item):
    # queue order == repair_N index used in prompts
    for i, q in enumerate(queue):
        if q["key"] == item["key"] and q["tier"] == item["tier"] and q["index"] == item["index"]:
            fn = os.path.join(ROOT, "scratchpad", "_maths_audit", "repair_%d.json" % i)
            if fn in repair_files:
                return repair_files[fn]
    return None

for f in failed:
    rep = find_repair_for(f)
    if not rep:
        print("  SKIP failed (no repair file):", f); continue
    sols = [str(s) for s in rep.get("new_solutions", [])]
    ans = (f.get("answer") or "")
    if all(re.search(r"(?<![\d.])" + re.escape(s.rstrip('.0') or s) + r"(?![\d])", ans.replace("−", "-")) for s in sols):
        print("  SALVAGE (x-values quibble):", f["key"], f["tier"], f["index"])
        passed.append({"item": {"key": f["key"], "tier": f["tier"], "index": f["index"]}, "rep": rep})
    else:
        print("  REJECT failed repair:", f["key"], f["tier"], f["index"], "-", (f.get("note") or "")[:90])

def derive_expect(check):
    if not check: return None
    m = re.fullmatch(r"equals_(-?\d+(?:\.\d+)?)", check)
    if m: return float(m.group(1))
    m = re.fullmatch(r"equals_(-?\d+)/(-?\d+)", check)
    if m: return round(float(m.group(1)) / float(m.group(2)), 4)
    m = re.fullmatch(r"equals_(-?\d+(?:\.\d+)?)_(?:and_|or_)?(-?\d+(?:\.\d+)?)", check)
    if m: return [float(m.group(1)), float(m.group(2))]
    return None

d = json.load(io.open(os.path.join(ROOT, "scratchpad", "_maths_edexcel_practice.json"), encoding="utf-8"))
ids = {r["units"]["slug"] + "-L%02d" % r["lesson_number"]: r["id"] for r in d}

def get(lid):
    r = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid + "&select=id,practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))[0]

def patch(lid, pd):
    r = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"},
        data=json.dumps({"practice_data": pd}).encode())
    urllib.request.urlopen(r)

by_lesson = {}
for p in passed:
    by_lesson.setdefault(p["item"]["key"], []).append(p)

applied = 0
for key, reps in sorted(by_lesson.items()):
    row = get(ids[key])
    pd = row["practice_data"]
    for p in reps:
        it, rep = p["item"], p["rep"]
        prob = pd["problem_bank"][it["tier"]][it["index"]]
        prob["display"] = rep["new_display"]
        sols = rep["new_solutions"]
        prob["solutions"] = [int(s) if float(s).is_integer() else s for s in sols]
        ms = []
        for m in rep.get("new_misconceptions", []):
            ms.append({"pattern": m.get("pattern"), "check": m.get("check"),
                       "message": m.get("message"), "expect": derive_expect(m.get("check"))})
        if ms: prob["misconceptions"] = ms
        applied += 1
        print("  repair", key, it["tier"], it["index"], "->", prob["solutions"])
    patch(row["id"], pd)
print("repairs applied:", applied, "across", len(by_lesson), "lessons")
