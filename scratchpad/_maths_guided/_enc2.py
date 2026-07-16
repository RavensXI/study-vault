import json
pd=json.load(open("_live_check.json",encoding="utf-8"))
clean=pd["problem_bank"]["gold"][0]["hint"]
suspect=pd["guided"]["teach"]["gold"]["steps"][0]["say"]
suspect2=pd["guided"]["teach"]["gold"]["steps"][1]["pre"]
for name,s in [("clean_hint",clean),("teach_say",suspect),("teach_pre",suspect2)]:
    nonascii=[(c,hex(ord(c))) for c in s if ord(c)>127]
    print(name, "->", nonascii)
