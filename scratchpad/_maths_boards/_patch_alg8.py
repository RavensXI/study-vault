# -*- coding: utf-8 -*-
import os, json, urllib.request, shutil

ID = "6589946a-1739-4d22-add3-1a9081309921"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID

pd = json.load(open("lesson_maths-aqa_algebra-L08.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# diagrams shard = same content (opener figure lives in main object)
shutil.copyfile("lesson_maths-aqa_algebra-L08.json", "lesson_maths-aqa_algebra-L08_diagrams.json")

# changes (guided)
json.dump({
 "key": "maths-aqa_algebra-L08",
 "problems_fixed": [
   {"tier":"bronze","index":1,"what":"duplicate discriminant answer (1) collided with bronze[6] roots count; changed constant +1 to -1 for a clean unique discriminant","old":"2x^2 - 3x + 1 = 0 (disc 1)","new":"2x^2 - 3x - 1 = 0 (disc 17)"},
   {"tier":"silver","index":6,"what":"turning-point x-coordinate (3) collided with silver[4] q (3); shifted bracket to keep a clean unique integer","old":"y = (x - 3)^2 + 5 (x = 3)","new":"y = (x - 4)^2 + 5 (x = 4)"}
 ],
 "issues_resolved": 2,
 "opener_concept": "Algebra-tile completing the square: build ONE bigger square from an x-by-x tile plus 6 x-long strips. Sharing the 6 strips over two sides (3 each) and filling the 3x3 corner IS x^2+6x=(x+3)^2-9. Inline SVG shows the decomposition.",
 "notes": "Full guided stack added: opener (with SVG), 3 teach walks, tier_guides x3, tier descriptions, per-problem hints, guided_steps on all 20 bank problems, derived misconceptions. All 20 solutions fresh-solved and independently re-verified; every final box lands on its solution. Slimmed method_card. Preserved topic_links, related_videos, worked_examples byte-for-byte. Validator PASS."
}, open("changes_maths-aqa_algebra-L08.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

# changes (diagrams)
json.dump({
 "key": "maths-aqa_algebra-L08",
 "figures_added": [
   {"tier":"opener","index":0,"kind":"svg","what":"Completing-the-square algebra-tile figure: x-by-x square, two x-long strips, and the 3x3 corner square, theme-safe (currentColor strokes/text, soft opacity fills). Makes x^2+6x=(x+3)^2-9 concrete."}
 ],
 "opener_touched": True,
 "notes": "Textual algebra lesson: discriminant, quadratic formula and completing-the-square bank questions are pure calculation, which real AQA papers print without figures, so no bank figures added (exam-realism test). The one warranted figure is the completing-the-square tile diagram in the opener."
}, open("changes_maths-aqa_algebra-L08_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes + diagrams shard written")
