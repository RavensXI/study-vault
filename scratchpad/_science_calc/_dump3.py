import json,io
pd=json.load(io.open('_live_canonical.json',encoding='utf-8'))
out=io.open('_gsteps.txt','w',encoding='utf-8')
pb=pd['problem_bank']
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        gs=p.get('guided_steps')
        out.write(f'\n=== {t}[{i}] sol={p.get("solutions")} ===\n')
        if not gs:
            out.write('  NO guided_steps; skip_reason='+str(p.get('guided_skip_reason'))+'\n'); continue
        nboxes=0; boundary=None
        for j,s in enumerate(gs):
            if 'answer' in s and not (s.get('say') and 'answer' not in s):
                if 'answer' in s:
                    nboxes+=1
                    ph=s.get('phase')
                    if ph=='substitute' and boundary is None: boundary=j
                    out.write(f'  [{j}] BOX pre={s.get("pre")!r} post={s.get("post")!r} ans={s.get("answer")!r} phase={ph} done={s.get("done")!r}\n')
            else:
                out.write(f'  [{j}] SAY: {s.get("say")}\n')
        # count live boxes at/after boundary
        if boundary is not None:
            liveafter=sum(1 for k,s in enumerate(gs) if k>=boundary and 'answer' in s)
            before=sum(1 for k,s in enumerate(gs) if k<boundary and 'answer' in s)
            out.write(f'   >> boundary at [{boundary}]; boxes before={before}, at/after={liveafter}\n')
        else:
            out.write('   >> NO phase:substitute boundary\n')
out.close()
print('done')
