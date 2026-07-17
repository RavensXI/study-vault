import json
ID="9a6f1e85-41b4-4b82-87c6-e919e48362a9"
live=json.load(open("_CHK_ocrL01_live.json", encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
pre=[r for r in dump if r.get("id")==ID][0]["practice_data"]
pwe=pre["worked_examples"]; lwe=live["worked_examples"]
print("count pre/live:", len(pwe), len(lwe))
def flat(we):
    out=[]
    for ex in we:
        out.append(("Q", ex.get("question"), ex.get("difficulty")))
        for st in ex["steps"]:
            out.append(("label", st.get("label")))
            out.append(("content", st.get("content")))
    return out
fp=flat(pwe); fl=flat(lwe)
for i,(a,b) in enumerate(zip(fp,fl)):
    if a!=b:
        print("DIFF:", a, "|||", b)
print("len same:", len(fp)==len(fl))
