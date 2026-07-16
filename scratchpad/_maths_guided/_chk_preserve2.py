import json
LID="fe5f6191-4452-4313-934d-8e5d16ba1032"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
print("n entries", len(pre))
print("sample keys", list(pre[0].keys()))
match=[e for e in pre if e.get("id")==LID or e.get("lesson_id")==LID]
print("matches by id", len(match))
# try find any field containing the id
for e in pre[:3]:
    print({k:(str(v)[:40]) for k,v in e.items() if k!='practice_data'})
