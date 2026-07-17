import json, io
ID="971cfba0-badb-4c6b-b0f8-e9d33d450b8c"
live=json.load(io.open("_CHK_algL12ocr_live.json","r",encoding="utf-8"))
dump=json.load(io.open("_pre_dump_maths-ocr.json","r",encoding="utf-8"))
entry=[v for v in dump if v.get("id")==ID][0]
print("title:", entry["title"])
pre=entry["practice_data"]
print("pre keys:", sorted(pre.keys()))
print("live keys:", sorted(live.keys()))

# Preservation checks per SPEC section 9 / checker brief 6
def show(name):
    print("\n==",name,"==")
    print(" pre :", json.dumps(pre.get(name), ensure_ascii=False)[:400])
    print(" live:", json.dumps(live.get(name), ensure_ascii=False)[:400])

for f in ["related_videos","topic_links","worked_examples","method_card"]:
    a=json.dumps(pre.get(f),ensure_ascii=False,sort_keys=True)
    b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
    print(f, "IDENTICAL" if a==b else "CHANGED")

# problem_bank: compare displays / solutions / options preserved
print("\n-- problem_bank displays & solutions --")
for tier in ["bronze","silver","gold"]:
    pb_pre=pre.get("problem_bank",{}).get(tier,[])
    pb_live=live.get("problem_bank",{}).get(tier,[])
    print(f"{tier}: pre n={len(pb_pre)} live n={len(pb_live)}")
    for i,(pp,pl) in enumerate(zip(pb_pre,pb_live)):
        dchg = pp.get("display")!=pl.get("display")
        schg = pp.get("solutions")!=pl.get("solutions")
        ochg = pp.get("options")!=pl.get("options")
        itchg= pp.get("input_type")!=pl.get("input_type")
        flags=[]
        if dchg: flags.append("DISPLAY")
        if schg: flags.append(f"SOL {pp.get('solutions')}->{pl.get('solutions')}")
        if ochg: flags.append("OPTIONS")
        if itchg: flags.append(f"INPUT {pp.get('input_type')}->{pl.get('input_type')}")
        if flags: print(f"  [{i}] "+", ".join(flags))
