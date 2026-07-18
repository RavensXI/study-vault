import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
ppd=[r for r in pre if r.get('id')==cid][0]['pd']
pd=json.load(open('_chk689_live.json',encoding='utf-8'))
# duplicate answers within tier
print("=== duplicate answers within tier ===")
for t in ['bronze','silver','gold']:
    sols=[p['solutions'][0] for p in pd['problem_bank'][t]]
    dups=[x for x in set(sols) if sols.count(x)>1]
    print(t, sols, 'DUP:'+str(dups) if dups else 'no dup')
# worked_examples diff
print("\n=== worked_examples diff ===")
import difflib
a=json.dumps(ppd['worked_examples'],ensure_ascii=False,indent=1).splitlines()
b=json.dumps(pd['worked_examples'],ensure_ascii=False,indent=1).splitlines()
for line in difflib.unified_diff(a,b,lineterm='',n=0):
    if line.startswith(('+','-')) and not line.startswith(('+++','---')):
        print(line)
