# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
def show(s):
    return s
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        print("\n"+"="*70)
        print(f"{tier}[{i}]  input_type={p.get('input_type')} calculator={p.get('calculator')}")
        print("DISPLAY:",repr(p.get('display')))
        print("SOLUTIONS:",p.get('solutions'))
        print("HINT:",p.get('hint'))
        if 'chart' in p:
            print("CHART:",json.dumps(p['chart'],ensure_ascii=False))
        mis=p.get('misconceptions',[])
        for j,m in enumerate(mis):
            print(f"  MIS[{j}] expect={m.get('expect')} pattern={m.get('pattern')!r} msg={m.get('message')!r}")
        gs=p.get('guided_steps',[])
        for k,st in enumerate(gs):
            if 'say' in st and 'answer' not in st:
                print(f"  gs[{k}] SAY: {st['say']!r}")
            else:
                print(f"  gs[{k}] pre={st.get('pre')!r} post={st.get('post')!r} ANSWER={st.get('answer')!r} phase={st.get('phase')} hint={st.get('hint')!r}")
