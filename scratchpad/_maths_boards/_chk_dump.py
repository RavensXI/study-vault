import json
d=json.load(open('_chk_live_geoL03.json'))
out=[]
pb=d['problem_bank']
def clean(s):
    if not isinstance(s,str): return s
    return s
for t in ['bronze','silver','gold']:
    out.append(f"\n########## {t}  desc: {pb.get(t+'_description')}")
    for i,p in enumerate(pb[t]):
        out.append(f"\n--- {t}[{i}] input_type={p.get('input_type')} calc={p.get('calculator')}")
        # strip svg from display for readability but note presence
        disp=p.get('display','')
        import re
        svgs=re.findall(r'<svg.*?</svg>', disp, re.S)
        txt=re.sub(r'<svg.*?</svg>','[SVG]',disp,flags=re.S)
        out.append('DISPLAY: '+txt)
        out.append('SOL: '+json.dumps(p.get('solutions')))
        out.append('HINT: '+str(p.get('hint')))
        mis=p.get('misconceptions',[])
        for j,m in enumerate(mis):
            out.append(f"  MIS[{j}] expect={json.dumps(m.get('expect'))} pattern={m.get('pattern')}")
            out.append(f"       msg: {m.get('message')}")
        gs=p.get('guided_steps')
        if gs:
            for k,st in enumerate(gs):
                if 'say' in st and 'answer' not in st:
                    out.append(f"   gs[{k}] SAY: {st['say']}")
                else:
                    ph=st.get('phase')
                    out.append(f"   gs[{k}] BOX pre={st.get('pre')!r} post={st.get('post')!r} answer={st.get('answer')} phase={ph}")
                    if st.get('done'): out.append(f"        done: {st.get('done')}")
        else:
            out.append('   (no guided_steps) skip='+str(p.get('guided_skip_reason')))
open('_chk_dump_pb.txt','w',encoding='utf-8').write('\n'.join(str(x) for x in out))
print('wrote', len(out),'lines')
