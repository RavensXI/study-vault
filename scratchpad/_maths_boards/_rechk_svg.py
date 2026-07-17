import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        d=p.get("display","")
        m=re.search(r'<svg.*?</svg>',d,flags=re.S)
        if not m: continue
        svg=m.group(0)
        # checks
        hard=re.findall(r'fill="#[0-9a-fA-F]{3,6}"',svg)  # text fills etc
        texts=re.findall(r'<text[^>]*>(.*?)</text>',svg)
        al=re.search(r'aria-label="([^"]*)"',svg)
        ext=('href=' in svg) or ('<script' in svg)
        print(f"\n### {tier}[{i}] textlabels={texts}")
        print("   aria:",al.group(1) if al else None)
        print("   external_ref:",ext, " hardcoded_fills:",set(hard))
        print("   SVG:",svg[:1200])
