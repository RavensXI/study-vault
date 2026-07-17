import json

d = json.load(open('_pre_dump_maths-aqa.json', encoding='utf-8'))
ID = '6f3f98f9-e772-40d9-8e54-b76a2ed3e8c7'
entry = None
if isinstance(d, dict):
    for k, v in d.items():
        if k == ID or (isinstance(v, dict) and v.get('id') == ID):
            entry = v
            print('found under key', k)
            break
    if entry is None and ID in d:
        entry = d[ID]
elif isinstance(d, list):
    for v in d:
        if v.get('id') == ID:
            entry = v
            break

if entry is None:
    print('NOT FOUND; top keys:', list(d.keys())[:10] if isinstance(d, dict) else 'list len ' + str(len(d)))
else:
    pd = entry.get('practice_data', entry)
    live = json.load(open('_CHK_rpL04_LIVE.json', encoding='utf-8'))
    for f in ['related_videos', 'topic_links', 'worked_examples']:
        pre = pd.get(f)
        lv = live.get(f)
        same = json.dumps(pre, sort_keys=True) == json.dumps(lv, sort_keys=True)
        print(f'{f}: preserved={same}')
        if not same:
            print('  PRE :', json.dumps(pre)[:400])
            print('  LIVE:', json.dumps(lv)[:400])
    # pre problem counts and solutions
    prepb = pd.get('problem_bank', {})
    livepb = live.get('problem_bank', {})
    for t in ['bronze','silver','gold']:
        pre_sols = [p.get('solutions') for p in prepb.get(t,[])]
        live_sols = [p.get('solutions') for p in livepb.get(t,[])]
        print(t, 'PRE sols', pre_sols)
        print(t, 'LIV sols', live_sols)
