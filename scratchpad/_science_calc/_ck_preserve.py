import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid="91158ba8-389c-4771-9735-326785654ccb"
pre_pd=[e for e in pre if e.get('id')==cid][0]['pd']
live=json.load(open('_ck_canonical_live.json',encoding='utf-8'))
for f in ('worked_examples','related_videos','topic_links','exam_context'):
    same = json.dumps(pre_pd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f,"PRESERVED" if same else "CHANGED")
# method_card diff
print("method_card same:", json.dumps(pre_pd.get('method_card'),sort_keys=True)==json.dumps(live.get('method_card'),sort_keys=True))
print("pre mc title:",pre_pd['method_card'].get('title'))
print("pre mc steps count:",len(pre_pd['method_card'].get('steps',[])))
