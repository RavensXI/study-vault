import json
pd = json.load(open("_CHK_gL02ocr_live.json", encoding="utf-8"))["practice_data"]
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
ID="7134e062-5209-4de5-894e-c315dc3ee9d0"
row=[r for r in pre if r.get("id")==ID][0]
pwe=row["practice_data"].get("worked_examples")
nwe=pd.get("worked_examples")
print("pre count:",len(pwe),"now count:",len(nwe))
print("equal object:", pwe==nwe)
import difflib
a=json.dumps(pwe,ensure_ascii=False,indent=1).splitlines()
b=json.dumps(nwe,ensure_ascii=False,indent=1).splitlines()
d=list(difflib.unified_diff(a,b,lineterm=""))
if not d:
    print("NO DIFF (identical content; earlier CHANGED was sort_keys artefact)")
else:
    for l in d[:60]: print(l)
