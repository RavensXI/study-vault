import json
LID="fe5f6191-4452-4313-934d-8e5d16ba1032"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
e=[x for x in pre if x["id"]==LID][0]
print("title", e["title"], "lesson#", e["lesson_number"], "unit", e["units"].get("slug") if isinstance(e["units"],dict) else e["units"])
pd_pre=e["practice_data"]
print("pre top keys", sorted(pd_pre.keys()))
live=json.load(open("_CHK_live_geomL02.json",encoding="utf-8"))
print("live top keys", sorted(live.keys()))
for fld in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(pd_pre.get(fld),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(fld),sort_keys=True,ensure_ascii=False)
    print(f"{fld}: preserved={same}")
    if not same:
        print("  PRE :", json.dumps(pd_pre.get(fld),ensure_ascii=False)[:800])
        print("  LIVE:", json.dumps(live.get(fld),ensure_ascii=False)[:800])
# also method_card and problem_bank displays/solutions preservation vs pre
print("\n--- pre problem_bank tiers/sizes ---")
pb_pre=pd_pre.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    print(t, len(pb_pre.get(t,[])) if isinstance(pb_pre.get(t),list) else "n/a")
