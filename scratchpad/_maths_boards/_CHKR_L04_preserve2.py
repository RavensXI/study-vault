import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="6e383a58-7e5b-4917-a28d-2881938a3def"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(open("_CHKR_L04_live.json",encoding="utf-8"))["practice_data"]
entry=None
for l in (pre if isinstance(pre,list) else pre.values()):
    if isinstance(l,dict) and l.get("id")==ID: entry=l
ppd=entry.get("practice_data",entry)
print("=== PRE method_card ===")
print(json.dumps(ppd.get("method_card"),ensure_ascii=False,indent=1))
print("=== PRE guided present? ===", "guided" in ppd)
print("=== PRE problem_bank keys ===", list(ppd.get("problem_bank",{}).keys()))
# did pre have &pound in opener/anywhere?
s=json.dumps(ppd,ensure_ascii=False)
print("pre &pound; count:", s.count("&pound;"))
print("pre solutions bronze:", [p.get("solutions") for p in ppd.get("problem_bank",{}).get("bronze",[])])
print("pre displays bronze:", [p.get("display") for p in ppd.get("problem_bank",{}).get("bronze",[])])
print("pre solutions silver:", [p.get("solutions") for p in ppd.get("problem_bank",{}).get("silver",[])])
print("pre solutions gold:", [p.get("solutions") for p in ppd.get("problem_bank",{}).get("gold",[])])
