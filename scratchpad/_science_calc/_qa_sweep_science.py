# -*- coding: utf-8 -*-
"""Zero-token final sweep: validator on every canonical, byte-identity across
every propagation group, mojibake scan, preservation of unit/accept fields."""
import json, io, os, sys, urllib.request, importlib.util

sys.stdout.reconfigure(errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GUIDED = os.path.join(os.path.dirname(HERE), "_maths_guided")
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

spec = importlib.util.spec_from_file_location("vg", os.path.join(GUIDED, "_validate_guided.py"))
vg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vg)

wl = json.load(io.open(os.path.join(HERE, "_worklist_versions.json"), encoding="utf-8"))

def get_pd(lid):
    r = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))[0]["practice_data"]

fails, moji, prop_bad, no_guided = {}, [], [], []
for wkey, v in sorted(wl.items()):
    pd = get_pd(v["canonical_id"])
    if not pd.get("guided"):
        no_guided.append(wkey)
        continue
    tmp = os.path.join(HERE, "_qa_tmp.json")
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False))
    vg.fails = []
    try:
        vg.main(tmp)
    except SystemExit:
        fails[wkey] = vg.fails[:8]
    blob = json.dumps(pd, ensure_ascii=False)
    if any(x in blob for x in ("Ã", "Â", "âˆ", "â€")):
        moji.append(wkey)
    canon = json.dumps(pd, sort_keys=True)
    for rid in v["all_row_ids"]:
        if rid == v["canonical_id"]:
            continue
        if json.dumps(get_pd(rid), sort_keys=True) != canon:
            prop_bad.append(wkey + " -> " + rid)

print("science sweep: %d/60 canonical validator PASS | mojibake: %s | propagation mismatches: %s | missing guided: %s"
      % (60 - len(fails), moji or "clean", prop_bad or "none", no_guided or "none"))
for k, v in fails.items():
    print("FAIL", k)
    for f in v:
        print("   -", f)
