import json,io,re
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_svg.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        d=p.get("display","")
        if "<svg" in d:
            w(f"===== {tier}[{i}] =====")
            m=re.search(r'(<svg.*?</svg>)',d,re.S)
            w(m.group(1))
            # texts
            w("TEXTS:", re.findall(r'<text[^>]*>(.*?)</text>',d))
            w("---")
# also hard-coded dark fills check
allsvg="".join(p.get("display","") for t in ["bronze","silver","gold"] for p in pb[t] if "<svg" in p.get("display",""))
w("\nHARDCODED FILL COLORS in text:", re.findall(r'<text[^>]*fill="(#[0-9a-fA-F]{3,6})"',allsvg))
w("external refs (http):", "http" in allsvg)
out.close()
print(open("_CHK_rpL06_svg.txt",encoding="utf-8").read())
