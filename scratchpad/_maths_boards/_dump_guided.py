import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_L09_live_fresh.json", encoding="utf-8"))["practice_data"]
gd = pd["guided"]
print("### OPENER  label:", gd["opener"].get("label"))
print("display:", repr(gd["opener"]["display"]))
for k,st in enumerate(gd["opener"]["steps"]):
    if st.get("answer") is not None:
        print(f"  {k} BOX pre={st.get('pre')!r} ans={st.get('answer')} | say={st.get('say')!r}")
    else:
        print(f"  {k} say={st.get('say')!r}")
for tier in ("bronze","silver","gold"):
    t = gd["teach"][tier]
    print(f"\n### TEACH {tier}  display: {t['display']}  label={t.get('label')!r}")
    for k,st in enumerate(t["steps"]):
        ph=" [sub]" if st.get("phase")=="substitute" else ""
        if st.get("answer") is not None:
            print(f"  {k}{ph} BOX pre={st.get('pre')!r} post={st.get('post')!r} ans={st.get('answer')}")
        else:
            print(f"  {k}{ph} say={st.get('say')!r}")
print("\n### METHOD_CARD")
mc = pd["method_card"]
print("title:", mc.get("title"))
print("steps:", mc.get("steps"))
import re
c = re.sub("<[^>]+>","",mc.get("content",""))
print("content words:", len(c.split()))
print("content:", mc.get("content"))
print("\n### TIER_GUIDES steps word counts")
for tier in ("bronze","silver","gold"):
    g = pd["tier_guides"][tier]
    tot = sum(len(s.replace("\\("," ").replace("\\)"," ").split()) for s in g["steps"])
    print(f"  {tier}: title={g['title']!r} words={tot} example_q={g['example']['question']!r}")
