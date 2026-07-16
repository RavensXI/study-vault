# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = "geometry-L07"
LID = "aee11210-c33f-4e61-a25e-1ef101e95ab3"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
sk = os.environ["SUPABASE_SERVICE_KEY"]

# fetch fresh
req = urllib.request.Request(BASE + "?id=eq.%s&select=practice_data" % LID,
                             headers={"apikey": sk, "Authorization": "Bearer " + sk})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]

figs = json.load(io.open("_figs.json", encoding="utf-8"))
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def prepend(display, svg):
    return svg + CAP + display

added = []
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, prob in enumerate(pb[tier]):
        k = "%s|%d" % (tier, i)
        if k in figs:
            if "<svg" in prob["display"]:
                raise SystemExit("already has svg: " + k)
            prob["display"] = prepend(prob["display"], figs[k])
            added.append({"tier": tier, "index": i, "kind": "svg",
                          "what": prob["display"].split("</svg>")[0][:0] or ""})

# teach walks
tw_added = []
for tier in ("bronze", "silver", "gold"):
    k = "teach|%s" % tier
    t = pd["guided"]["teach"][tier]
    if "<svg" in t["display"]:
        raise SystemExit("teach already svg: " + k)
    t["display"] = prepend(t["display"], figs[k])
    tw_added.append(tier)

out = io.open("lesson_%s_diagrams.json" % KEY, "w", encoding="utf-8")
json.dump(pd, out, ensure_ascii=False, indent=1)
out.close()
print("problem figures:", len(added), "teach figures:", len(tw_added))
