import json,re
pd=json.load(open('_pd_live.json',encoding='utf-8'))
issues=[]

def evalbox(pre,answer,path):
    if pre is None: return
    # find last "<expr> = " pattern; normalize unicode operators
    s=pre.replace('×','*').replace('÷','/').replace('−','-').replace('→','')
    # capture arithmetic before trailing '='
    m=re.findall(r'([0-9().\s*/+\-]+?)\s*=\s*$',s.strip())
    if not m:
        return  # no explicit arithmetic (e.g. "Read off c = ")
    expr=m[-1].strip()
    # must contain an operator to evaluate
    if not re.search(r'[*/+\-]',expr): return
    try:
        val=eval(expr)
    except Exception as ex:
        return
    if abs(val-float(answer))>0.005:
        issues.append(f"{path}: '{expr}' = {val} but box answer = {answer}")

# guided_steps
for tier in ['bronze','silver','gold']:
    for idx,prob in enumerate(pd['problem_bank'][tier]):
        for j,st in enumerate(prob.get('guided_steps',[])):
            if 'answer' in st:
                evalbox(st.get('pre'),st['answer'],f"{tier}[{idx}].guided_steps[{j}]")
# teach
for tier,walk in pd['guided']['teach'].items():
    for j,st in enumerate(walk['steps']):
        if 'answer' in st:
            evalbox(st.get('pre'),st['answer'],f"teach.{tier}[{j}]")
# opener
for j,st in enumerate(pd['guided']['opener']['steps']):
    if 'answer' in st:
        evalbox(st.get('pre'),st['answer'],f"opener[{j}]")

print("BOX ARITHMETIC mismatches:")
for i in issues: print("  ",i)
if not issues: print("   none (all parseable box expressions match their answers)")
