# -*- coding: utf-8 -*-
import json, re
live = json.load(open("_CHK_psL02b_live.json", encoding="utf-8"))
pd = live["practice_data"]

txtpat = re.compile(r'<text[^>]*x="(\d+)"[^>]*>([^<]*)</text>')
totpat = re.compile(r'Total:\s*([\d.]+)')

def analyze(display, label):
    if "<svg" not in display: return
    texts = txtpat.findall(display)
    nums = []
    total = None
    for x,val in texts:
        v=val.strip()
        mt=totpat.search(v)
        if mt: total=float(mt.group(1)); continue
        # region numbers (skip letters/labels/?, 'neither 0.3')
        m=re.search(r'(-?\d+\.?\d*)', v)
        if m and v not in ("A","B") and not v.isalpha():
            # capture standalone numbers or 'neither 0.x'
            try: nums.append((int(x), float(m.group(1)), v))
            except: pass
    regionvals=[n[1] for n in sorted(nums)]
    s=sum(regionvals)
    ok = (total is not None and abs(s-total)<1e-6)
    print(f"{label}: total={total} regions={regionvals} sum={round(s,4)} {'OK' if ok else '<<< MISMATCH'}")

for t in ["gold","bronze","silver"]:
    for i,p in enumerate(pd["problem_bank"][t]):
        analyze(p.get("display",""), f"{t}[{i}]")
for t in ["gold","bronze","silver"]:
    analyze(pd["guided"]["teach"][t].get("display",""), f"teach.{t}")
analyze(pd["guided"]["opener"]["steps"][0].get("display",""), "opener")
