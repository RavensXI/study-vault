# -*- coding: utf-8 -*-
"""Fable QA sweep: fetch every live maths-edexcel practice_data, run the
deterministic validator in-process, verify preserved fields against the
pre-fan-out dump, and print each lesson's opener concept for taste review."""
import json, io, os, sys, urllib.request, importlib.util

sys.stdout.reconfigure(errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

spec = importlib.util.spec_from_file_location("vg", os.path.join(HERE, "_validate_guided.py"))
vg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vg)

pre = {r["units"]["slug"] + "-L%02d" % r["lesson_number"]: r
       for r in json.load(io.open(os.path.join(HERE, "_pre_fanout_dump.json"), encoding="utf-8"))}
wl = json.load(io.open(os.path.join(HERE, "_worklist.json"), encoding="utf-8"))
wl["algebra-L09"] = {"id": pre["algebra-L09"]["id"], "title": "Simultaneous Equations (Linear)", "unit": "algebra", "n": 9}

def get_pd(lid):
    r = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))[0]["practice_data"]

report = {"pass": [], "fail": {}, "preservation": {}, "no_guided": []}
openers = []
for key in sorted(wl):
    pd = get_pd(wl[key]["id"])
    if not pd.get("guided"):
        report["no_guided"].append(key)
        continue
    vg.fails = []
    try:
        vg.scan_dashes(pd, "pd")
        # reuse full main() logic by temp file
        tmp = os.path.join(HERE, "_qa_tmp.json")
        io.open(tmp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False))
        vg.fails = []
        try:
            vg.main(tmp)
            report["pass"].append(key)
        except SystemExit:
            report["fail"][key] = vg.fails[:12]
    except Exception as e:
        report["fail"][key] = ["QA sweep exception: " + repr(e)]
    # preservation
    old = pre[key]["practice_data"]
    lost = []
    for f in ("related_videos", "topic_links", "passages", "exam_context"):
        if f in old and old.get(f) != pd.get(f):
            lost.append(f)
    if lost:
        report["preservation"][key] = lost
    op = (pd.get("guided") or {}).get("opener") or {}
    first = ""
    for st in op.get("steps", []):
        if st.get("say"):
            first = st["say"][:90]
            break
    openers.append(key + " :: " + (op.get("display") or "")[:70].replace("\n", " ") + " | " + first)

print("PASS: %d | FAIL: %d | no guided yet: %s" % (len(report["pass"]), len(report["fail"]), report["no_guided"]))
for k, v in report["fail"].items():
    print("FAIL", k)
    for f in v:
        print("   -", f)
if report["preservation"]:
    print("PRESERVATION diffs (may be legit trims):")
    for k, v in report["preservation"].items():
        print("  ", k, v)
else:
    print("preservation: all preserved fields intact")
io.open(os.path.join(HERE, "_qa_openers.txt"), "w", encoding="utf-8").write("\n".join(openers))
print("openers written for taste review: _qa_openers.txt")
