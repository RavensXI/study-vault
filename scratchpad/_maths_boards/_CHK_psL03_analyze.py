import json
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
pd = json.load(open(base + r"\_CHK_psL03_LIVE.json", encoding="utf-8"))
bank = pd["problem_bank"]

for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(bank[tier]):
        it = p.get("input_type")
        disp = p.get("display","")
        # strip svg
        d = disp
        if d.startswith("<svg"):
            d = d.split("</svg>",1)[-1]
        d = (d[:90]).replace("\n"," ")
        print(f"{tier}[{i}] {it} sol={p.get('solutions')} :: {d}")
        if it == "multiple_choice":
            opts = p.get("options",[])
            for j,o in enumerate(opts):
                print(f"      opt{j}{'*' if j in p.get('solutions',[]) else ' '}: {o}")
        # guided final box lands on solution?
        gs = p.get("guided_steps")
        if gs:
            boxes = [s for s in gs if "answer" in s]
            finals = [b["answer"] for b in boxes]
            sols = p.get("solutions")
            # for single_value: check some box equals sol
            print(f"      box answers: {finals}")
print("\n--- em/en dash scan in student-facing ---")
import re
def scan(s, path):
    if isinstance(s,str):
        if "—" in s:
            print("EM DASH", path, repr(s[:80]))
    elif isinstance(s,dict):
        for k,v in s.items():
            if k=="note": continue
            scan(v, path+"."+k)
    elif isinstance(s,list):
        for idx,v in enumerate(s):
            scan(v, f"{path}[{idx}]")
scan(pd,"pd")
print("scan done")
