import json,sys
sys.stdout.reconfigure(encoding="utf-8")
s=json.load(open("_CHKR_ps03_shard.json",encoding="utf-8"))
g=s["guided"]
print("##### OPENER #####")
print(json.dumps(g["opener"],ensure_ascii=False,indent=1))
print("\n##### TEACH BRONZE #####")
print(json.dumps(g["teach"]["bronze"],ensure_ascii=False,indent=1))
print("\n##### TEACH SILVER #####")
print(json.dumps(g["teach"]["silver"],ensure_ascii=False,indent=1))
print("\n##### TEACH GOLD #####")
print(json.dumps(g["teach"]["gold"],ensure_ascii=False,indent=1))
print("\n##### TIER GUIDES #####")
print(json.dumps(s["tier_guides"],ensure_ascii=False,indent=1))
