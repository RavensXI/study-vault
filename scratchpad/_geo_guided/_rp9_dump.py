import json, sys
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_rp9_live.json"
d = json.load(open(p, encoding="utf-8"))
out = []
def w(s=""): out.append(str(s))
w("TOP KEYS: " + ", ".join(d.keys()))
pb = d["problem_bank"]
w("PB KEYS: " + ", ".join(pb.keys()))
for tier in ("bronze","silver","gold"):
    for i, pr in enumerate(pb[tier]):
        w("="*70)
        w(f"{tier}[{i}] type={pr.get('input_type')} image={pr.get('image')} chart={'YES' if pr.get('chart') else ''}")
        w("DISPLAY: " + str(pr.get("display")))
        w("OPTIONS: " + json.dumps(pr.get("options"), ensure_ascii=False))
        w("SOLUTIONS: " + json.dumps(pr.get("solutions"), ensure_ascii=False))
        w("HINT: " + str(pr.get("hint")))
        w("MISC: " + json.dumps(pr.get("misconceptions"), ensure_ascii=False, indent=1))
        for j, s in enumerate(pr.get("guided_steps") or []):
            w(f"  gs[{j}] " + json.dumps(s, ensure_ascii=False))
w("="*70)
w("TIER GUIDES: " + json.dumps(d.get("tier_guides"), ensure_ascii=False, indent=1))
w("="*70)
w("GUIDED: " + json.dumps(d.get("guided"), ensure_ascii=False, indent=1))
w("="*70)
w("METHOD CARD: " + json.dumps(d.get("method_card"), ensure_ascii=False, indent=1))
w("WORKED: " + json.dumps(d.get("worked_examples"), ensure_ascii=False, indent=1))
open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_rp9_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("lines", len(out))
