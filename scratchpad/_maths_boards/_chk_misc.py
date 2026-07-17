import json
live=json.load(open("_ocrL11_live.json",encoding="utf-8"))
print("=== OCR LIVE: existing misconceptions & guided_steps presence ===")
for t in ("bronze","silver","gold"):
    for i,p in enumerate(live["problem_bank"][t]):
        m=p.get("misconceptions")
        gs="Y" if p.get("guided_steps") else "N"
        print(t,i,"it=",p.get("input_type"),"gs=",gs,"hint=",bool(p.get("hint")),"| misc:",json.dumps(m,ensure_ascii=False) if m else None)
print("has tier_guides:",bool(live.get("tier_guides")),"has guided:",bool(live.get("guided")))
print("method_card keys:",list((live.get("method_card") or {}).keys()))
print("worked_examples count:",len(live.get("worked_examples") or []))
print("related_videos:",json.dumps(live.get("related_videos"),ensure_ascii=False)[:400])
print("topic_links:",json.dumps(live.get("topic_links"),ensure_ascii=False)[:400])
