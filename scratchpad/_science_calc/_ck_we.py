import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid="91158ba8-389c-4771-9735-326785654ccb"
pre_pd=[e for e in pre if e.get('id')==cid][0]['pd']
live=json.load(open('_ck_canonical_live.json',encoding='utf-8'))
print("=== PRE worked_examples ===")
print(json.dumps(pre_pd['worked_examples'],ensure_ascii=False,indent=1))
print("=== PRE exam_context ===")
print(json.dumps(pre_pd['exam_context'],ensure_ascii=False))
print("=== LIVE exam_context ===")
print(json.dumps(live['exam_context'],ensure_ascii=False))
