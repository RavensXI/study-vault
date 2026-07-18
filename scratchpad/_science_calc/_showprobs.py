import json, io
pd=json.load(io.open('_live_canon_fresh.json',encoding='utf-8'))
for tier,idx in [('bronze',3),('silver',1)]:
    p=pd['problem_bank'][tier][idx]
    print('='*60)
    print(tier,idx)
    print('display:', p.get('display'))
    print('solutions:', p.get('solutions'), 'unit:', p.get('unit'), 'accept:', p.get('accept'))
    for i,s in enumerate(p.get('guided_steps',[])):
        if 'say' in s and 'pre' not in s:
            print(f'  [{i}] SAY: {s["say"]}')
        else:
            print(f'  [{i}] pre={s.get("pre")!r} post={s.get("post")!r} answer={s.get("answer")!r} phase={s.get("phase")} done={s.get("done")!r}')
