import json
ID='f6f5708d-edf9-42e6-81d8-49c3cf282310'
KEY='number-L06'
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
# find entry
entry=None
if isinstance(pre,dict):
    if KEY in pre: entry=pre[KEY]
    elif ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if ID in json.dumps(v)[:2000]:
                entry=v; print('found under',k); break
elif isinstance(pre,list):
    for e in pre:
        if ID in json.dumps(e)[:500]:
            entry=e;break
print('type pre', type(pre), 'keys' , list(pre.keys())[:3] if isinstance(pre,dict) else len(pre))
pd = None
if entry:
    pd = entry.get('practice_data', entry)
    json.dump(pd, open('_pre_l06.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
    print('PRE keys:', list(pd.keys()))
    print('related_videos:', json.dumps(pd.get('related_videos'),ensure_ascii=False))
    print('topic_links:', json.dumps(pd.get('topic_links'),ensure_ascii=False))
    print('worked_examples count:', len(pd.get('worked_examples',[])))
