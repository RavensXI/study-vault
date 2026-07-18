import json
a=json.load(open("_live_fc32b93d-51c8-4260-a199-7268fa33979d.json",encoding="utf-8"))
b=json.load(open("_live_d2088054-e987-4e06-8480-34549a015d79.json",encoding="utf-8"))
# canonical-JSON compare
sa=json.dumps(a,sort_keys=True,ensure_ascii=False)
sb=json.dumps(b,sort_keys=True,ensure_ascii=False)
print("byte-identical(sorted):", sa==sb)
print("len a,b:", len(sa),len(sb))
if sa!=sb:
    # find diff location
    for i,(x,y) in enumerate(zip(sa,sb)):
        if x!=y:
            print("first diff at",i, repr(sa[i-40:i+40]),"|VS|",repr(sb[i-40:i+40]))
            break
