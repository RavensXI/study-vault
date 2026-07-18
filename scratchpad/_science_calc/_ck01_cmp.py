import json, io
a=json.load(io.open("_ck01_row0.json",encoding="utf-8"))
b=json.load(io.open("_ck01_row1.json",encoding="utf-8"))
# canonical serialization for equality
sa=json.dumps(a,sort_keys=True,ensure_ascii=False)
sb=json.dumps(b,sort_keys=True,ensure_ascii=False)
print("PROP IDENTICAL:", sa==sb)
print("len a",len(sa),"len b",len(sb))
# top-level keys
print("keys:", sorted(a.keys()))
pb=a.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    print(t, "count", len(pb.get(t,[])))
