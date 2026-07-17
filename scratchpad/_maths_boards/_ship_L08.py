# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
key=os.environ["SUPABASE_SERVICE_KEY"]
data=json.load(io.open("lesson_maths-aqa_geometry-L08.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":data}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live==shard:", json.dumps(live,sort_keys=True)==json.dumps(data,sort_keys=True))

# write changes file
changes={
 "key":"geometry-L08",
 "problems_fixed":[
   {"tier":"silver","index":6,"what":"Duplicate magnitude answer within silver (both sv4 and sv6 gave 10); re-posed sv6 coordinates so the answer is distinct and clean.","old":"A = (1, 3), B = (7, 11). Find |AB|. -> 10","new":"A = (3, 2), B = (15, 7). Find |AB|. -> 13"},
   {"tier":"gold","index":1,"what":"Repaired garbled display: original leaked pipeline reasoning text ('Actually, is BX = 2a-2b...'). Rewrote as a clean ratio question consistent with options.","old":"Show that BX is parallel to OA... Actually, is BX = 2a - 2b = 2(a - b)? ... Find the ratio |BX| : |BA|.","new":"OA = a and OB = b. A point X satisfies BX = 2a - 2b. Find the ratio |BX| : |BA|."}
 ],
 "issues_resolved":2,
 "opener_concept":"Delivery robot on a block grid: total blocks east and north is exactly vector addition, revealed as (3,2)+(1,5)=(4,7).",
 "figures_added":[
   {"tier":"bronze","index":2,"kind":"svg","what":"Right-angled triangle, legs 5 and 12, hypotenuse ? (magnitude)."},
   {"tier":"bronze","index":3,"kind":"svg","what":"Schematic triangle O-A-B, sides a and b, AB marked ?."},
   {"tier":"bronze","index":5,"kind":"svg","what":"Right-angled triangle, legs 3 and 4, hypotenuse ?."},
   {"tier":"silver","index":0,"kind":"svg","what":"Triangle O-A-B, P midpoint of AB, OP dashed to ?."},
   {"tier":"silver","index":1,"kind":"svg","what":"Triangle O-A-B, sides 2a and 2b, M midpoint of AB."},
   {"tier":"silver","index":4,"kind":"svg","what":"Right-angled triangle, legs 8 and 6, hypotenuse ?."},
   {"tier":"silver","index":5,"kind":"svg","what":"Triangle O-A-B, P dividing AB 1:3 from A."},
   {"tier":"silver","index":6,"kind":"svg","what":"Displacement triangle, 12 across and 5 up, distance ?."},
   {"tier":"gold","index":0,"kind":"svg","what":"Triangle O-A-B with point X, BX marked ?."},
   {"tier":"gold","index":1,"kind":"svg","what":"B, A and X roughly collinear, BX shown for the ratio."},
   {"tier":"gold","index":2,"kind":"svg","what":"Triangle O-A-B (3a,3b), P on OA and Q on OB, PQ marked ?."},
   {"tier":"gold","index":4,"kind":"svg","what":"Triangle O-A-B, M midpoint OA, N midpoint OB, MN marked ?."},
   {"tier":"opener","index":0,"kind":"svg","what":"Block grid showing the robot's two-leg path (3E,2N then 1E,5N)."},
   {"tier":"teach.silver","index":0,"kind":"svg","what":"Triangle O-A-B, M midpoint of OB, AM dashed."}
 ],
 "opener_touched":True,
 "notes":"Fresh-solved all 20 problems (8 bronze, 7 silver, 5 gold); all stored answers correct except the two repairs above. Every misconception expect reproduced by committing the error (MC expects = wrong-option index; single_value expects = numeric wrong answer). All 14 SVG figures theme-safe (currentColor, opacity fills) and label-checked against the numbers. related_videos, topic_links, worked_examples preserved byte-for-byte. Validator PASS."
}
json.dump(changes, io.open("changes_maths-aqa_geometry-L08.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("WROTE changes_maths-aqa_geometry-L08.json")
