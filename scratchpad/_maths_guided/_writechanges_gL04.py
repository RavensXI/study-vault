# -*- coding: utf-8 -*-
import os, json, io, urllib.request, subprocess, sys

ID = "0b5aef96-fa58-45be-a8fe-6d63c2baf002"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    live = json.load(r)[0]["practice_data"]
io.open("_gL04_live_after.json", "w", encoding="utf-8").write(json.dumps(live, ensure_ascii=False, indent=2))
res = subprocess.run([sys.executable, "_validate_guided.py", "_gL04_live_after.json"],
                     capture_output=True, text=True)
print("LIVE VALIDATOR:", res.stdout.strip(), res.stderr.strip())

changes = {
  "key": "geometry-L04",
  "figures_added": [
    {"tier": "opener", "index": 0, "kind": "svg", "what": "grid with counter at (2,1), the concrete translation hook"},
    {"tier": "teach-bronze", "index": 0, "kind": "svg", "what": "segment A(1,2)-B(3,2) on grid, translation walk"},
    {"tier": "teach-silver", "index": 0, "kind": "svg", "what": "P(4,1), Q(4,3) with origin O, 90 CW rotation walk"},
    {"tier": "teach-gold", "index": 0, "kind": "svg", "what": "point (5,4) + centre cross (1,1), enlargement walk"},
    {"tier": "bronze", "index": 0, "kind": "svg", "what": "point (4,2) to translate"},
    {"tier": "bronze", "index": 1, "kind": "svg", "what": "point (5,3) + x-axis mirror highlighted"},
    {"tier": "bronze", "index": 2, "kind": "svg", "what": "point (3,7) + y-axis mirror highlighted"},
    {"tier": "bronze", "index": 3, "kind": "svg", "what": "point (2,5) + origin O, 180 rotation"},
    {"tier": "bronze", "index": 4, "kind": "svg", "what": "point (2,4) + centre cross at origin, SF3"},
    {"tier": "bronze", "index": 7, "kind": "svg", "what": "point (1,6) to translate"},
    {"tier": "silver", "index": 0, "kind": "svg", "what": "point (4,1) + mirror line y=x drawn"},
    {"tier": "silver", "index": 1, "kind": "svg", "what": "point (3,2) + origin O, 90 CW"},
    {"tier": "silver", "index": 2, "kind": "svg", "what": "point (8,6) + centre cross at origin, SF 1/2"},
    {"tier": "silver", "index": 3, "kind": "svg", "what": "A(1,3) and A'(5,1) both plotted, find vector"},
    {"tier": "silver", "index": 4, "kind": "svg", "what": "triangle (2,1),(4,1),(2,4) area 3, enlargement"},
    {"tier": "silver", "index": 5, "kind": "svg", "what": "point (5,2) + origin O, 90 ACW"},
    {"tier": "silver", "index": 6, "kind": "svg", "what": "point (-3,4) + mirror line x=1 drawn"},
    {"tier": "gold", "index": 0, "kind": "svg", "what": "point (3,2) + centre cross (1,1), SF -2"},
    {"tier": "gold", "index": 1, "kind": "svg", "what": "(2,5) and (5,2) both plotted, describe transform"},
    {"tier": "gold", "index": 4, "kind": "svg", "what": "point (5,7) + centre cross (2,3), SF -1"}
  ],
  "opener_touched": True,
  "notes": "Transformations lesson: every coordinate problem gets an exam-realistic grid, drawn to scale from its own numbers. Only GIVEN points/lines/centres plotted (never the answer); reflections show the amber dashed mirror line, rotations mark origin O, enlargements mark an amber centre cross. All text uses fill=currentColor and marks use blue/amber/soft-green so figures read on light and dark themes; no external refs, each svg <2.7KB. No 'not drawn accurately' caption because grids are to scale. Skipped figures on the 4 genuinely textual problems: bronze[5] (which transform resizes, conceptual), bronze[6] (reading a vector's meaning, a drawing would give the answer), gold[2] (side 4cm->10cm scale factor, pure ratio), gold[3] (area 12->SF3, pure numeric). No content/answers/steps changed; figures only."
}
io.open("changes_geometry-L04_diagrams.json", "w", encoding="utf-8").write(
    json.dumps(changes, ensure_ascii=False, indent=2))
print("wrote changes_geometry-L04_diagrams.json")
