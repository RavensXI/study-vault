import json,re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_LIVE_eduqas_probstat_L02.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
ID="7f417926-0bef-4875-a7ad-7eb71bd15506"
row=[r for r in pre if r.get("id")==ID][0]
prb_pre=row["practice_data"]["problem_bank"]
prb_live=live["problem_bank"]
def stripfig(d):
    d=re.sub(r'<svg.*?</svg>','',d,flags=re.S)
    d=d.replace('<br>','').strip()
    return d
issues=0
for tier in ["bronze","silver","gold"]:
    lp=prb_live[tier]; pp=prb_pre[tier]
    for i,(a,b) in enumerate(zip(pp,lp)):
        # compare solutions
        if a.get('solutions')!=b.get('solutions'):
            print(f"{tier}[{i}] SOLUTION CHANGED pre={a.get('solutions')} live={b.get('solutions')}"); issues+=1
        # compare text sans figure
        if stripfig(a.get('display',''))!=stripfig(b.get('display','')):
            print(f"{tier}[{i}] TEXT CHANGED")
            print("  pre:",stripfig(a.get('display','')))
            print("  liv:",stripfig(b.get('display','')))
            issues+=1
print("bank text/solution issues:",issues)
