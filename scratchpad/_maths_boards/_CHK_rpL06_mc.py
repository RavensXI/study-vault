import json,io
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_mc.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice":
            w(f"{tier}[{i}] options={p.get('options')} solutions={p.get('solutions')}")
            w("  display:",p.get("display"))
out.close()
print(open("_CHK_rpL06_mc.txt",encoding="utf-8").read())
