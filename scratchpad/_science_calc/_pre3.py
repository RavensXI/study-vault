import json
raw=open('_pre_dump_all.json','r',encoding='utf-8',errors='replace').read()
pre=json.loads(raw)
cid="a20c4a08-3698-4cb8-9f8c-b8978c3f9060"
entry=[v for v in pre if v.get('id')==cid][0]
print("entry keys:",list(entry.keys()))
pd=entry.get('practice_data')
print("pd type:",type(pd), "pd keys:", list(pd.keys()) if isinstance(pd,dict) else pd)
