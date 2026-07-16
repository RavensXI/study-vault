import json
d=json.load(open('_checker_live.json',encoding='utf-8'))
ID="5cb3f019-6030-4136-8917-af379ab9e503"
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
def findpd(o):
    if isinstance(o,dict):
        if o.get('id')==ID: return o
        for v in o.values():
            r=findpd(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=findpd(v)
            if r: return r
pd=findpd(pre)['practice_data']
preWE=pd['worked_examples']; newWE=d['worked_examples']
# normalize by replacing em dash + en dash with colon-equivalent to see if that's the ONLY diff
def norm(s): return s.replace(' — ',': ').replace('—',':').replace('–',':')
import copy
def deep_norm(o):
    if isinstance(o,dict): return {k:deep_norm(v) for k,v in o.items()}
    if isinstance(o,list): return [deep_norm(v) for v in o]
    if isinstance(o,str): return norm(o)
    return o
print("Only-diff-is-dashes?", json.dumps(deep_norm(preWE),sort_keys=True)==json.dumps(deep_norm(newWE),sort_keys=True))
# show exact per-string diffs
def strs(o,p=''):
    r={}
    if isinstance(o,dict):
        for k,v in o.items(): r.update(strs(v,p+'.'+k))
    elif isinstance(o,list):
        for i,v in enumerate(o): r.update(strs(v,f"{p}[{i}]"))
    elif isinstance(o,str): r[p]=o
    return r
a=strs(preWE); b=strs(newWE)
for k in a:
    if a.get(k)!=b.get(k):
        print("DIFF",k)
        print("  PRE:",a.get(k))
        print("  NEW:",b.get(k))
