import json
pre = json.load(open("_pre_dump_all.json", encoding="utf-8"))
print("total entries:", len(pre))
print("first entry keys:", list(pre[0].keys()))
cid = "3c4aa292-cf3a-4cda-876d-25b030880bb5"
# exact id match
matches=[e for e in pre if e.get("id")==cid]
print("exact id matches:", len(matches))
if matches:
    e=matches[0]
    print("entry keys:", list(e.keys()))
    pdp=e.get("practice_data")
    print("has practice_data:", pdp is not None)
    if pdp:
        live=json.load(open("_live_3c4aa292.json",encoding="utf-8"))
        for f in ("related_videos","worked_examples","topic_links","exam_context"):
            same=json.dumps(pdp.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
            print(f"{f}: preserved={same}")
            if not same:
                import difflib
                print("  PRE :", json.dumps(pdp.get(f),ensure_ascii=False)[:400])
                print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
        print("pre keys:", sorted(pdp.keys()))
        print("live keys:", sorted(live.keys()))
