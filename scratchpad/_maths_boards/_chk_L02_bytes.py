import json
raw = open("_CHK_L02_live.json","rb").read()
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
gold = pd["problem_bank"]["gold"]
for i in [3,4]:
    h = gold[i]["hint"]
    print(f"gold[{i}] hint repr:", repr(h))
    print("  codepoints:", [hex(ord(c)) for c in h if ord(c)>127])
# check U+FFFD replacement char present in whole doc
txt = raw.decode("utf-8")
print("\nU+FFFD count in doc:", txt.count("�"))
# find contexts
import re
for m in re.finditer("�", txt):
    print("  ctx:", repr(txt[m.start()-25:m.start()+10]))
