import json,re
LID="65e7a745-9820-431a-8b99-d96cd7514bf3"
live=json.load(open('_live_ps_L03.json',encoding='utf-8'))[0]['practice_data']
pre=json.load(open('_pre_dump_maths-ocr.json',encoding='utf-8'))
entry=[r for r in pre if r.get('id')==LID][0]
pp=entry['practice_data']['problem_bank']
lp=live['problem_bank']
def strip_svg(s):
    return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
for t in ['bronze','silver','gold']:
    print("=== TIER",t,"===")
    for i,(a,b) in enumerate(zip(pp[t],lp[t])):
        da=strip_svg(a.get('display','')); db=strip_svg(b.get('display',''))
        sa=a.get('solutions'); sb=b.get('solutions')
        dchg = da!=db
        schg = sa!=sb
        flag = '  CHANGED' if (dchg or schg) else ''
        print(f"[{t}[{i}]] sol pre={sa} live={sb}{flag}")
        if dchg:
            print("   DISP pre :", da[:120])
            print("   DISP live:", db[:120])
