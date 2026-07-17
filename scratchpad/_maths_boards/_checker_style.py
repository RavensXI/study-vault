import json
live=json.load(open("_LIVE_eduqas_L12.json",encoding="utf-8"))["practice_data"]
# walk all strings, flag em/en dash in student-facing (exclude 'note' fields)
bad=[]
def walk(o,path,in_note=False):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v,f"{path}.{k}",in_note or k=="note")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]",in_note)
    elif isinstance(o,str):
        if not in_note:
            for ch in ["—","–"]:
                if ch in o: bad.append((path,repr(ch),o[:80]))
walk(live,"root")
print("em/en dashes in student-facing:", len(bad))
for b in bad[:20]: print(" ",b)
# check misconception expects reproduce for MCQ: expect must be an index into options
print("\n--- MCQ expect index sanity ---")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        if p.get("input_type")=="multiple_choice":
            nopt=len(p.get("options",[]))
            for m in p.get("misconceptions",[]):
                e=m.get("expect")
                if e is not None and (not isinstance(e,int) or e<0 or e>=nopt):
                    print(f"  {tier}[{i}] bad expect index {e} (nopt {nopt})")
                if e is not None and e==p["solutions"][0]:
                    print(f"  {tier}[{i}] expect equals correct answer index {e}!")
print("done")
