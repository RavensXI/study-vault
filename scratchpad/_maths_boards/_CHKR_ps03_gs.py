import json
pd=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
out=[]
def dump_steps(steps):
    for j,s in enumerate(steps):
        if "say" in s and "answer" not in s and "pre" not in s:
            out.append(f"    [{j}] SAY: {s['say']}")
        else:
            out.append(f"    [{j}] pre={s.get('pre')!r} post={s.get('post')!r} ANS={s.get('answer')} phase={s.get('phase')} hint={s.get('hint')!r} done={s.get('done')!r} say={s.get('say')!r}")
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if gs:
            out.append(f"\n### {t}[{i}] DISPLAY(short): {p.get('display','')[:80]} | SOL={p.get('solutions')}")
            dump_steps(gs)
open("_CHKR_ps03_gs.txt","w",encoding="utf-8").write("\n".join(out))
print("done",len(out))
