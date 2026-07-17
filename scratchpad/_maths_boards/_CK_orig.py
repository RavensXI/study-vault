import json, re, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
pp=[r for r in pre if r["id"]==ID][0]["practice_data"]
def strip(s):
    s=re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
    return s.strip()
print("=== PRE silver[6] ===")
p=pp["problem_bank"]["silver"][6]
print("disp:",strip(p["display"]))
print("sol:",p["solutions"],"opts:",p.get("options"))
print("\n=== PRE gold ===")
for i,p in enumerate(pp["problem_bank"]["gold"]):
    print(f"[{i}] sol={p['solutions']} :: {strip(p['display'])[:130]}")
