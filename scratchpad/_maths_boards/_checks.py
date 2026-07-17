import json, io, re
pd=json.load(io.open("_live_L06.json",encoding="utf-8"))
s=io.open("_live_L06.json",encoding="utf-8").read()
# em dash scan
print("em dash count:", s.count("—"))
# find any em dash contexts
for m in re.finditer(r".{20}—.{20}", s):
    print("EMDASH:", m.group(0))

# Preservation vs pre-dump
pre=json.load(io.open("_pre_dump_maths-aqa.json",encoding="utf-8"))
print("pre-dump type:", type(pre), "len" , len(pre) if isinstance(pre,(list,dict)) else "")
