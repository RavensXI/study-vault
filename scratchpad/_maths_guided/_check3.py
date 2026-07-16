import json
d=json.load(open('_checker_live.json',encoding='utf-8'))
ID="5cb3f019-6030-4136-8917-af379ab9e503"

# worklist key
try:
    wl=json.load(open('_worklist.json',encoding='utf-8'))
    def find(o):
        if isinstance(o,dict):
            if o.get('id')==ID or o.get('lesson_id')==ID: return o
            for v in o.values():
                r=find(v)
                if r: return r
        if isinstance(o,list):
            for v in o:
                r=find(v)
                if r: return r
    print("WORKLIST ENTRY:", find(wl))
except Exception as e: print("worklist err",e)

# pre-dump
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
def findpd(o):
    if isinstance(o,dict):
        if o.get('id')==ID or o.get('lesson_id')==ID: return o
        for v in o.values():
            r=findpd(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=findpd(v)
            if r: return r
entry=findpd(pre)
if entry is None:
    print("PRE-DUMP: entry not found by id; top keys:", list(pre.keys())[:5] if isinstance(pre,dict) else type(pre))
else:
    pd = entry.get('practice_data', entry)
    for f in ['related_videos','topic_links','worked_examples']:
        same = json.dumps(pd.get(f),sort_keys=True)==json.dumps(d.get(f),sort_keys=True)
        print(f"PRESERVE {f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("   PRE:",json.dumps(pd.get(f))[:200])
            print("   NEW:",json.dumps(d.get(f))[:200])
