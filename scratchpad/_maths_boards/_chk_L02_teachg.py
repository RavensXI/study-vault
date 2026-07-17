import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
teach = pd["guided"]["teach"]
print(json.dumps(teach["gold"], indent=1, ensure_ascii=False))
