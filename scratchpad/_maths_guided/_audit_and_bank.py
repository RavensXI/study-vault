import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="ee087e5f-7971-4f5d-b6e0-2fe13585d6f4"
KEY="number-L03"
# audit result
try:
    ar=json.load(open("_maths_audit/_audit_result.json",encoding="utf-8"))
    def scan(o):
        out=[]
        def w(x):
            if isinstance(x,dict):
                s=json.dumps(x,ensure_ascii=False)
                if ID in s or "L03" in s or "decimals" in s.lower() or "rounding" in s.lower():
                    out.append(x)
                for v in x.values(): w(v)
            elif isinstance(x,list):
                for v in x: w(v)
        w(o); return out
    for sect in ["issues","unconfirmed"]:
        items=ar.get(sect,[])
        hits=[it for it in items if ID in json.dumps(it,ensure_ascii=False) or "L03" in json.dumps(it,ensure_ascii=False) or "decimals" in json.dumps(it,ensure_ascii=False).lower()]
        print(f"AUDIT {sect}: {len(hits)} hits for this lesson")
        for h in hits: print("  ",json.dumps(h,ensure_ascii=False)[:300])
except Exception as e:
    print("audit read error:",e)

# bank pre vs live displays/solutions
live=json.load(open("_maths_guided/_pd.json",encoding="utf-8"))
dump=json.load(open("_maths_guided/_pre_fanout_dump.json",encoding="utf-8"))
def find(d):
    if isinstance(d,list):
        for e in d:
            if isinstance(e,dict) and e.get("id")==ID: return e
    if isinstance(d,dict):
        if ID in d: return d[ID]
        for v in d.values():
            r=find(v)
            if r: return r
pre=find(dump); pp=pre.get("practice_data",pre)
for t in ["bronze","silver","gold"]:
    pa=pp["problem_bank"][t]; la=live["problem_bank"][t]
    print(f"--- {t}: pre {len(pa)} live {len(la)} ---")
    for i in range(max(len(pa),len(la))):
        pd_=pa[i]["display"] if i<len(pa) else "MISSING"
        ld_=la[i]["display"] if i<len(la) else "MISSING"
        ps=pa[i]["solutions"] if i<len(pa) else None
        ls=la[i]["solutions"] if i<len(la) else None
        pit=pa[i].get("input_type") if i<len(pa) else None
        lit=la[i].get("input_type") if i<len(la) else None
        mark=""
        if pd_!=ld_ or ps!=ls or pit!=lit: mark=" <<< CHANGED"
        print(f"  [{i}] pre:{pd_} {ps} {pit} | live:{ld_} {ls} {lit}{mark}")
