import json
ID="93469b0d-2704-499c-a20b-587a84c2e214"
live = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]
pre_raw = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
entry = next(r for r in pre_raw if r.get("id")==ID)
pre = entry["practice_data"]

pw = pre["worked_examples"]; lw = live["worked_examples"]
print("counts pre/live:", len(pw), len(lw))
for i,(a,b) in enumerate(zip(pw,lw)):
    print(f"\n=== WE[{i}] question pre==live: {a['question']==b['question']}")
    if a['question']!=b['question']:
        print("  PRE Q:",a['question']); print("  LIVE Q:",b['question'])
    for j,(sa,sb) in enumerate(zip(a['steps'],b['steps'])):
        la,lb=sa.get('label'),sb.get('label')
        ca,cb=sa.get('content'),sb.get('content')
        if la!=lb:
            print(f"  step[{j}] LABEL: {la!r} -> {lb!r}")
        if ca!=cb:
            print(f"  step[{j}] CONTENT CHANGED:\n     PRE : {ca!r}\n     LIVE: {cb!r}")
