# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "a4c149cd-abd5-4180-9ea3-449d4ac37f88"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
vurl = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
back = json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(back, io.open("_live_after_num6.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

changes = {
    "key": "number-L06",
    "board": "maths-aqa",
    "lesson_id": ID,
    "problems_fixed": [],
    "issues_resolved": 0,
    "figures_added": [
        {"tier": "opener", "index": None, "kind": "svg",
         "what": "384,000 with its three trailing zeros highlighted, reinforcing that 3 zeros = 10^3 (supports opener box 1)."}
    ],
    "opener_concept": "Distance to the Moon (384,000 km): count the trailing zeros, see they equal 10^3, so 384,000 = 384 x 10^3 = 3.84 x 10^5. Names standard form as packing zeros into a power of 10.",
    "notes": "Fresh-solved all 20 problems from their displays: every stored solution was already correct, no degenerate/duplicate/non-calculator issues found, so no answer edits (problems_fixed empty). Full guided layer added: opener (2 boxes + reveal), teach walks bronze/silver/gold (>=4 boxes each, gold teaches the front-below-1 adjust), tier_guides with worked examples, guided_steps on every one of the 20 bank problems with a substitute completion boundary, one plain-text hint per problem, tier descriptions, and a slimmed method_card. Misconceptions rewritten to honest-diagnosis form: each expect derived by committing the error (e.g. standard_form no_adjust expects [40,3]/[30,2], added-powers-on-divide expects [3,11], added-fronts-on-add expects [5,4]/[12.5,5]). No em dashes; unicode superscripts throughout; solutions/displays/input_types and worked_examples/topic_links/related_videos preserved byte-for-byte.",
}
json.dump(changes, io.open("changes_maths-aqa_number-L06.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes_maths-aqa_number-L06.json and _live_after_num6.json")
