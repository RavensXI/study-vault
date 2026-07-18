import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
r=[r for r in pre if r.get('id')==cid][0]
ppd=r.get('pd') or {}
print("pre pd keys:",list(ppd.keys()))
pb=ppd.get('problem_bank',{})
print("pre bank sizes:",{k:len(v) for k,v in pb.items() if isinstance(v,list)})
pd=json.load(open('_chk689_live.json',encoding='utf-8'))
for f in ['worked_examples','related_videos','topic_links','exam_context']:
    same=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
for t in ['bronze','silver','gold']:
    opb=pb.get(t,[]); npb=pd['problem_bank'][t]
    print(f"bank {t}: pre={len(opb)} now={len(npb)}")
    for i in range(min(len(opb),len(npb))):
        a=opb[i];b=npb[i]
        for fld in ['solutions','display','accept','unit','higher_only','input_type']:
            if a.get(fld)!=b.get(fld):
                print(f"  {fld} CHANGED {t}[{i}]: {a.get(fld)} -> {b.get(fld)}")
