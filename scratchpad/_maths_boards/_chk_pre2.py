import json
d=json.load(open('_pre_dump_maths-eduqas.json', encoding='utf-8'))
pre = next(x for x in d if x["id"]=="e58f9467-dd87-4589-9b18-b603c1966291")
json.dump(pre["practice_data"], open("_chk_pre_numberL01.json","w",encoding='utf-8'), indent=1, ensure_ascii=False)
pd=pre["practice_data"]
print("PRE keys:", list(pd.keys()))
print("title:", pre["title"])
