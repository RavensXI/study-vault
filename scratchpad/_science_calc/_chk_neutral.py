import json, io, re
raw=io.open("_L02_6e6b_live.json",encoding="utf-8").read()
# board names
for term in ["AQA","Edexcel","OCR","Eduqas","WJEC","equation sheet","formula sheet","memorise","memorize","on your sheet","given to you","you must remember"]:
    hits=[m.start() for m in re.finditer(re.escape(term), raw, re.I)]
    if hits:
        for h in hits[:3]:
            print(f"BOARD/CLAIM '{term}' @ {h}: ...{raw[max(0,h-40):h+40]}...")
# em dash
for m in re.finditer("—", raw):
    print("EM DASH @",m.start(),":",raw[m.start()-30:m.start()+30])
# en dash occurrences (informational)
en=[m.start() for m in re.finditer("–", raw)]
print("en-dash count:",len(en))
for h in en[:5]:
    print("  en @",h,":",raw[max(0,h-30):h+20])
print("DONE neutral scan")
