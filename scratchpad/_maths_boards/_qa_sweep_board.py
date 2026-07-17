# -*- coding: utf-8 -*-
"""Fable QA sweep for a board: live validator + preservation + mojibake +
opener concept list. Usage: python _qa_sweep_board.py maths-aqa"""
import json, io, os, sys, urllib.request, importlib.util

sys.stdout.reconfigure(errors="replace")
board = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
GUIDED = os.path.join(os.path.dirname(HERE), "_maths_guided")
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

spec = importlib.util.spec_from_file_location("vg", os.path.join(GUIDED, "_validate_guided.py"))
vg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vg)

pre = {r["units"]["slug"] + "-L%02d" % r["lesson_number"]: r
       for r in json.load(io.open(os.path.join(HERE, "_pre_dump_%s.json" % board), encoding="utf-8"))}
wl = json.load(io.open(os.path.join(HERE, "_worklist_%s.json" % board), encoding="utf-8"))

def get_pd(lid):
    r = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))[0]["practice_data"]

fails, moji, pres, nog = {}, {}, {}, []
openers = []
for key in sorted(wl):
    pd = get_pd(wl[key]["id"])
    if not pd.get("guided"):
        nog.append(key)
        continue
    tmp = os.path.join(HERE, "_qa_tmp.json")
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False))
    vg.fails = []
    try:
        vg.main(tmp)
    except SystemExit:
        fails[key] = vg.fails[:10]
    blob = json.dumps(pd, ensure_ascii=False)
    m = [x for x in ("Ã", "Â", "âˆ", "â€") if x in blob]
    if m:
        moji[key] = m
    old = pre[key]["practice_data"]
    lost = [f for f in ("related_videos", "topic_links", "passages") if f in old and old.get(f) != pd.get(f)]
    if lost:
        pres[key] = lost
    op = (pd.get("guided") or {}).get("opener") or {}
    first = next((st["say"][:80] for st in op.get("steps", []) if st.get("say")), "")
    openers.append(key + " :: " + first)

n = len(wl)
print("%s: validator %d/%d PASS | mojibake: %s | preservation diffs: %s | missing guided: %s"
      % (board, n - len(fails), n, moji or "clean", pres or "intact", nog or "none"))
for k, v in fails.items():
    print("FAIL", k)
    for f in v:
        print("   -", f)
io.open(os.path.join(HERE, "_qa_openers_%s.txt" % board), "w", encoding="utf-8").write("\n".join(openers))
print("openers ->", "_qa_openers_%s.txt" % board)
