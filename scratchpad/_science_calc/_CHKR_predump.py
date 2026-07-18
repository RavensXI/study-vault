import json
p=json.load(open('_pre_dump_all.json',encoding='utf-8'))
row=[r for r in p if r.get('id')=='9941e716-ac52-4486-8f10-a81babbb8cc1'][0]
pd=row['pd']
print('pre-dump pd keys:', list(pd.keys()))
# extract structure to compare preservation
live=json.load(open('_CHKR_canon_live.json',encoding='utf-8'))['practice_data']

# 1. related_videos, topic_links, worked_examples, exam_context, method_card identical?
for f in ['related_videos','topic_links','exam_context','worked_examples','method_card']:
    same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, 'PRESERVED' if same else 'CHANGED', '(pre has:', f in pd, ')')

# 2. equation_hint per bronze/silver problem preserved?
def hints(bank):
    out={}
    for tier in ['bronze','silver','gold']:
        for i,prob in enumerate(bank.get(tier,[])):
            out[(tier,i)]=prob.get('equation_hint')
    return out
ph=hints(pd.get('problem_bank',{}))
lh=hints(live.get('problem_bank',{}))
print('\nequation_hint comparison:')
for k in sorted(set(list(ph.keys())+list(lh.keys()))):
    if ph.get(k)!=lh.get(k):
        print('  DIFF',k,'pre=',repr(ph.get(k)),'live=',repr(lh.get(k)))
    #else: print('  same',k, repr(lh.get(k)))
print('equation_hint all preserved:', ph==lh)

# 3. displays / solutions / higher_only preserved?
def core(bank):
    out={}
    for tier in ['bronze','silver','gold']:
        for i,prob in enumerate(bank.get(tier,[])):
            out[(tier,i)]=(prob.get('display'),json.dumps(prob.get('solutions')),prob.get('unit'),prob.get('accept'),prob.get('higher_only'),prob.get('input_type'))
    return out
pc=core(pd.get('problem_bank',{}))
lc=core(live.get('problem_bank',{}))
print('\ncore fields (display/solutions/unit/accept/higher_only/input_type):')
for k in sorted(set(list(pc.keys())+list(lc.keys()))):
    if pc.get(k)!=lc.get(k):
        print('  DIFF',k)
        print('    pre =',pc.get(k))
        print('    live=',lc.get(k))
print('done')
