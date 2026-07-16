import json, re

pd = json.load(open("_CHK_L03_NOW.json", encoding="utf-8"))

pb = pd["problem_bank"]
tiers = ["bronze", "silver", "gold"]

def has_svg(s): return isinstance(s,str) and "<svg" in s
def has_chart(p): return isinstance(p,dict) and p.get("chart")

print("=== PROBLEM BANK ===")
for t in tiers:
    probs = pb.get(t, [])
    print(f"\n--- {t.upper()} ({len(probs)} problems) ---")
    for i,p in enumerate(probs):
        disp = p.get("display","")
        flags=[]
        if has_svg(disp): flags.append("SVG")
        if has_chart(p): flags.append("CHART")
        marker = "  [FIG:"+",".join(flags)+"]" if flags else ""
        # strip svg for text preview
        txt = re.sub(r"<svg.*?</svg>", "[SVG]", disp, flags=re.S)
        print(f"[{t}[{i}]]{marker}")
        print("  display:", txt[:400])
        print("  input_type:", p.get("input_type"), "| solutions:", p.get("solutions"))
        print()

# opener + teach
print("\n=== OPENER ===")
g = pd.get("guided",{})
op = g.get("opener",{})
print(json.dumps(op, ensure_ascii=False)[:1500])
