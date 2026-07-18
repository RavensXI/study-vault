import json
live=json.load(open('_live_L03.json'))
pre=json.loads(open('_pre_dump_all.json','r',encoding='utf-8',errors='replace').read())
cid="a20c4a08-3698-4cb8-9f8c-b8978c3f9060"
pd=[v for v in pre if v.get('id')==cid][0]['pd']
print("=== PRE exam_context ==="); print(json.dumps(pd['exam_context'],ensure_ascii=False,indent=1))
print("=== LIVE exam_context ==="); print(json.dumps(live['exam_context'],ensure_ascii=False,indent=1))
print("=== PRE worked_examples questions ===")
for w in pd['worked_examples']: print(" ",w['difficulty'],"::",w['question'][:70],"=>",[s['content'] for s in w['steps'] if s.get('is_answer')])
print("=== LIVE worked_examples questions ===")
for w in live['worked_examples']: print(" ",w['difficulty'],"::",w['question'][:70],"=>",[s['content'] for s in w['steps'] if s.get('is_answer')])
print("=== PRE method_card title/steps ==="); print(pd['method_card'].get('title'),"|",pd['method_card'].get('steps'))
print("=== LIVE method_card title/steps ==="); print(live['method_card'].get('title'),"|",live['method_card'].get('steps'))
