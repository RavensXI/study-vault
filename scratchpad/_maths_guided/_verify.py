import json,io,sys,math
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_pd.json",encoding="utf-8"))
pb=live["problem_bank"]

# Verify the suspect inverse "check" boxes: displayed arithmetic vs stored answer
print("=== SUSPECT CHECK BOXES (displayed product vs stored answer) ===")
def check(tier,idx,expr_a,expr_b,stored):
    print(f"{tier}[{idx}] check: {expr_a} vs stored {stored}: computed={expr_b}, match={expr_b==stored}")
check("gold",0,"1 × 3² (=1×9)",1*9,36)
check("gold",4,"2 × √9 (=2×3)",2*3,12)
check("silver",5,"0.8 × 2² (=0.8×4)",0.8*4,20)
# correct versions if they'd used NEW x:
print("If NEW x used: gold0 1×6²=",1*36," gold4 2×√36=",2*6," silver5 0.8×5²=",0.8*25)

print("\n=== EXPECTS: recompute committed error ===")
def show(tier):
    for i,p in enumerate(pb[tier]):
        for j,m in enumerate(p.get("misconceptions",[])):
            print(f"{tier}[{i}].misconceptions[{j}] expect={m.get('expect')} note={m.get('note')}")
for t in ["bronze","silver","gold"]:
    show(t)
