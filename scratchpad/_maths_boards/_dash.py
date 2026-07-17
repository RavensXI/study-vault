import json,re
live=json.load(open("_live_L03.json",encoding="utf-8"))
s=json.dumps(live,ensure_ascii=False)
# em dash U+2014, en dash U+2013, figure dash, minus sign U+2212 is allowed
for name,ch in [("EM DASH","—"),("EN DASH","–")]:
    idxs=[m.start() for m in re.finditer(ch,s)]
    print(f"{name} count: {len(idxs)}")
    for i in idxs[:20]:
        print("   ...",s[max(0,i-45):i+15].replace("\n"," "))
