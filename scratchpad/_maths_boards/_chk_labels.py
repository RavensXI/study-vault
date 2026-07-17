import json,re
d=json.load(open('_chk_live_geoL03.json',encoding='utf-8'))
pb=d['problem_bank']
out=[]
def labels(disp):
    return re.findall(r'<text[^>]*>(.*?)</text>', disp, re.S)
def aria(disp):
    m=re.search(r'aria-label="([^"]*)"',disp); return m.group(1) if m else None
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        disp=p.get('display','')
        has_svg='<svg' in disp
        txt=re.sub(r'<svg.*?</svg>','',disp,flags=re.S).strip()
        txt=re.sub(r'<[^>]+>','',txt).strip()
        out.append(f"{t}[{i}] svg={has_svg} sol={p.get('solutions')}")
        out.append(f"    aria: {aria(disp)}")
        out.append(f"    labels: {labels(disp)}")
        out.append(f"    qtext: {txt}")
open('_chk_labels.txt','w',encoding='utf-8').write('\n'.join(out))
print('done')
