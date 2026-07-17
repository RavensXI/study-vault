import json,re
ID="66a1ec53-d20f-4b82-b436-1b31fc88e998"
live=json.load(open("_LIVE_eduqas_L12.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
entry=None
if isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID: entry=v; break
pd=entry["practice_data"]
def core(disp):
    # strip svg
    return re.sub(r'<svg.*?</svg>','',disp,flags=re.S).replace('<span class="figure-caption">Sketch, not drawn to scale</span>','').strip()
for tier in ["bronze","silver","gold"]:
    for i,(p,l) in enumerate(zip(pd["problem_bank"][tier],live["problem_bank"][tier])):
        dp=core(p.get("display","")); dl=core(l.get("display",""))
        if dp!=dl:
            print(f"{tier}[{i}] DISPLAY changed:\n  pre: {dp}\n  live:{dl}")
        if p.get("solutions")!=l.get("solutions"):
            print(f"{tier}[{i}] SOLUTIONS changed: pre {p.get('solutions')} live {l.get('solutions')}")
        if p.get("options")!=l.get("options"):
            print(f"{tier}[{i}] OPTIONS changed: pre {p.get('options')} live {l.get('options')}")
print("diff done")
