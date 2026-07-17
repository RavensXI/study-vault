import json,re
pre=json.load(open('_pre_dump_maths-eduqas.json',encoding='utf-8'))
ID="27ec4539-cb68-4e60-ad0d-fa0828706d80"
row=[r for r in pre if r.get('id')==ID][0]
ppd=row['practice_data']; live=json.load(open('_CHK_L10_live.json',encoding='utf-8'))
def clean(d): 
    d=re.sub(r'<svg.*?</svg>','',d,flags=re.S); d=re.sub(r'<span.*?</span>','',d,flags=re.S)
    return d.strip()
for tier in ['bronze','silver','gold']:
    pb=ppd['problem_bank'][tier]; lb=live['problem_bank'][tier]
    print(f"--- {tier}: pre {len(pb)} live {len(lb)}")
    for i in range(max(len(pb),len(lb))):
        ps=pb[i]['solutions'] if i<len(pb) else None
        ls=lb[i]['solutions'] if i<len(lb) else None
        pdisp=clean(pb[i]['display']) if i<len(pb) else None
        ldisp=clean(lb[i]['display']) if i<len(lb) else None
        flag=""
        if ps!=ls: flag+=" SOLCHG"
        if pdisp!=ldisp: flag+=" DISPCHG"
        print(f"  [{i}] pre{ps} live{ls}{flag}")
        if 'DISPCHG' in flag:
            print("     PRE :",pdisp)
            print("     LIVE:",ldisp)
