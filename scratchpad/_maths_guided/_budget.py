import json,io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_L06_fresh.json",encoding="utf-8"))
def wc(s):
    s=re.sub(r"<[^>]+>"," ",s)
    return len(s.split())
for tier,g in pd["tier_guides"].items():
    tot=sum(wc(x) for x in g["steps"])
    print(f"tier_guides.{tier}: title={g['title']!r} steps_words={tot} nsteps={len(g['steps'])}")
mc=pd["method_card"]
print("method_card steps:",len(mc["steps"]),"content_words=",wc(mc["content"]))
# completion boundary check
for tier,probs in pd["problem_bank"].items():
    if not isinstance(probs,list): continue
    for i,pr in enumerate(probs):
        gs=pr.get("guided_steps")
        if not gs: continue
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        boxes_after=sum(1 for s in gs[phase_idx[0]:] if "answer" in s) if phase_idx else 0
        boxes_before=sum(1 for s in gs[:phase_idx[0]] if "answer" in s) if phase_idx else 0
        if not phase_idx:
            print(f"{tier}[{i}]: NO PHASE TAG (input_type={pr['input_type']})")
        elif boxes_before<1 or boxes_after<2:
            print(f"{tier}[{i}]: boundary before={boxes_before} after={boxes_after} <-- CHECK")
