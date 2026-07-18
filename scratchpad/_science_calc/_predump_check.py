import json
d=json.load(open('_pre_dump_all.json',encoding='utf-8'))
CID="5473906a-ccfa-43f0-8230-5b9171181f19"
row=None
for r in d:
    if r.get('id')==CID:
        row=r; break
if row is None:
    # maybe keyed differently
    print("not found by id; sample keys:", list(d[0].keys()))
else:
    pd=row['practice_data']
    print("PRE-DUMP top keys:", list(pd.keys()))
    print("has 'guided'?", 'guided' in pd)
    print("has 'tier_guides'?", 'tier_guides' in pd)
    pb=pd.get('problem_bank',{})
    # find equation_hints in pre-dump
    for tier in ['bronze','silver','gold']:
        for i,p in enumerate(pb.get(tier,[])):
            eh=p.get('equation_hint')
            if eh and 'sheet' in eh.lower():
                print(f"PRE {tier}[{i}] equation_hint: {eh}")
    # does pre-dump have guided_steps already?
    print("bronze[0] pre has guided_steps?", 'guided_steps' in pb.get('bronze',[{}])[0])
