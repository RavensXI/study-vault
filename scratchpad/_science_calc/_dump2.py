import json, io
d=json.load(open('_live_L05.json',encoding='utf-8'))['canonical']
out=io.StringIO()
def p(*a): print(*a, file=out)
pb=d['problem_bank']
for tier in ['bronze','silver','gold']:
    p(f"\n########## {tier.upper()} ##########")
    for i,prob in enumerate(pb[tier]):
        p(f"\n----- {tier}[{i}] -----")
        p("display:", prob.get('display'))
        p("input_type:", prob.get('input_type'), "| solutions:", prob.get('solutions'),
          "| accept:", prob.get('accept'), "| unit:", prob.get('unit'),
          "| calc:", prob.get('calculator'), "| higher_only:", prob.get('higher_only'))
        if 'options' in prob: p("options:", prob['options'])
        if 'equation_hint' in prob: p("equation_hint:", prob['equation_hint'])
        if 'hint' in prob: p("hint:", prob['hint'])
        if 'chart' in prob: p("CHART:", json.dumps(prob['chart'], ensure_ascii=False))
        for m in prob.get('misconceptions',[]):
            p(f"  MISC pattern={m.get('pattern')} expect={m.get('expect')} :: {m.get('message')}")
        gs=prob.get('guided_steps')
        if gs is None:
            p("  guided_steps: NONE  skip_reason:", prob.get('guided_skip_reason'))
        else:
            for j,s in enumerate(gs):
                if 'say' in s and 'answer' not in s:
                    p(f"  step{j} SAY: {s['say']}")
                else:
                    tag=' [PHASE]' if s.get('phase')=='substitute' else ''
                    p(f"  step{j}{tag} pre={repr(s.get('pre'))} post={repr(s.get('post'))} answer={s.get('answer')} hint={repr(s.get('hint'))}"+ (f" done={repr(s.get('done'))}" if s.get('done') else ''))
open('_readable_bank.txt','w',encoding='utf-8').write(out.getvalue())
print("done")
