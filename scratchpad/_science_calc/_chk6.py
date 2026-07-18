import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
ppd=[r for r in pre if r.get('id')==cid][0]['pd']
pd=json.load(open('_chk689_live.json',encoding='utf-8'))
pb=ppd['problem_bank']
print("=== ALL bank field changes ===")
for t in ['bronze','silver','gold']:
    opb=pb.get(t,[]); npb=pd['problem_bank'][t]
    for i in range(min(len(opb),len(npb))):
        a=opb[i];b=npb[i]
        for fld in ['solutions','display','accept','unit','higher_only','input_type']:
            if a.get(fld)!=b.get(fld):
                print(f"[{t}[{i}] {fld}]\n  PRE : {a.get(fld)}\n  NOW : {b.get(fld)}")
print("\n=== exam_context ===")
print("PRE:",json.dumps(ppd.get('exam_context'),ensure_ascii=False))
print("NOW:",json.dumps(pd.get('exam_context'),ensure_ascii=False))
print("\n=== worked_examples titles/difficulty ===")
print("PRE:",[ (w.get('difficulty'),w.get('question')[:40]) for w in ppd.get('worked_examples',[])])
print("NOW:",[ (w.get('difficulty'),w.get('question')[:40]) for w in pd.get('worked_examples',[])])
