import json
pd=json.load(open("_live_L03.json",encoding="utf-8"))
pb=pd["problem_bank"]
print("pb type", type(pb), "keys", [k for k in pb])
for t in ["gold","bronze","silver"]:
    arr=pb[t]
    print(t, type(arr), len(arr))
    for i,p in enumerate(arr):
        sol=p["solutions"]; opts=p.get("options"); it=p.get("input_type")
        if it=="multiple_choice":
            for s in sol:
                if not (0<=s<len(opts)): print("BAD",t,i,s)
        # duplicate options within a problem
        if opts and len(set(opts))!=len(opts):
            print("DUP OPTS",t,i,opts)
print("done")
