import json,re
pd=json.load(open("_live_1fcee1e4.json",encoding="utf-8"))
claims=["diagram","graph shows","the chart","sankey","arrow"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        d=p.get("display","")
        if any(re.search(c,d,re.I) for c in claims):
            has_svg="<svg" in d
            has_chart="chart" in p
            print(f"{tier}[{i}] claims-figure={True} svg={has_svg} chart={has_chart}: {d[:90]}")
