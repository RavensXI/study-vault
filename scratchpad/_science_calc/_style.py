import json,re
raw=open('_pd_live.json',encoding='utf-8').read()
pd=json.loads(raw)

# em dashes
print("Em dashes (—) count:", raw.count('—'))
# board names / equation-sheet claims
for term in ['AQA','Edexcel','OCR','WJEC','Eduqas','equation sheet','memorise','your board','on your sheet','data sheet']:
    hits=[m.start() for m in re.finditer(re.escape(term),raw,re.I)]
    if hits:
        for h in hits:
            print(f"  TERM '{term}' at {h}: ...{raw[max(0,h-40):h+40]}...")

# higher_only flags per problem
print("\nhigher_only flags:")
for tier in ['bronze','silver','gold']:
    for idx,p in enumerate(pd['problem_bank'][tier]):
        print(f"  {tier}[{idx}] higher_only={p.get('higher_only')} unit={p.get('unit')} accept={p.get('accept')} sol={p.get('solutions')}")
