import json
ID="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
pre=[r for r in json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8")) if r.get("id")==ID][0]
prepd=pre["practice_data"] if "practice_data" in pre else pre
live=json.load(open("_live_geoL02.json",encoding="utf-8"))
out=[]
out.append("=== PRE method_card ===")
out.append(json.dumps(prepd.get("method_card"),indent=1,ensure_ascii=False))
out.append("=== LIVE method_card ===")
out.append(json.dumps(live.get("method_card"),indent=1,ensure_ascii=False))
out.append("=== PRE worked_examples ===")
out.append(json.dumps(prepd.get("worked_examples"),indent=1,ensure_ascii=False))
out.append("=== LIVE worked_examples ===")
out.append(json.dumps(live.get("worked_examples"),indent=1,ensure_ascii=False))
open("_cmp3_out.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
