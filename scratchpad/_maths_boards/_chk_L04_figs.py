# -*- coding: utf-8 -*-
import json, re
live = json.load(open("_chk_L04_live.json", encoding="utf-8"))
pb = live["problem_bank"]
errors=[]; notes=[]

def figs():
    yield ("opener", live["guided"]["opener"]["steps"][1].get("display",""))
    for tier in ("bronze","silver","gold"):
        for i,p in enumerate(pb[tier]):
            d=p.get("display","")
            if "<svg" in d: yield (f"{tier}[{i}]", d)

for path,d in figs():
    if "<svg" not in d: continue
    # external refs
    if re.search(r'(xlink:href|https?://|url\()', d):
        errors.append(f"{path}: external ref in svg")
    # role + aria
    if 'role="img"' not in d: errors.append(f"{path}: no role=img")
    if 'aria-label' not in d: errors.append(f"{path}: no aria-label")
    # theme safety: any hard-coded dark text fill
    for m in re.finditer(r'<text[^>]*fill="([^"]+)"', d):
        c=m.group(1)
        if c!="currentColor": notes.append(f"{path}: <text> fill={c} (not currentColor)")
    # region fills should be soft w/ opacity - check rect fills
    for m in re.finditer(r'<rect[^>]*fill="(#[0-9a-fA-F]{6})"[^>]*fill-opacity="([0-9.]+)"', d):
        pass
    # extract aria-label numbers and the text labels
    aria=re.search(r'aria-label="([^"]+)"',d).group(1)
    texts=re.findall(r'>([^<>]+)</text>',d)
    notes.append(f"{path} labels: {texts}")

# Cross-check each figure's numeric labels against its data
checks={
 "opener":["£4","£6","£8","Sam","Kim","Jo"],
 "silver[0]":["Score","Frequency","1","3","2","5","3","8","4","4"],
 "silver[1]":["Class","Frequency","0-10","4","10-20","10","20-30","6"],
 "silver[3]":["Class","Frequency","0-20","5","20-40","15","40-60","10"],
 "silver[4]":["Class","Frequency","0-10","6","10-20","12","20-30","8","30-40","4"],
 "silver[5]":["Score","Frequency","3","2","4","5","5","8","6","3","7","2"],
 "gold[0]":["Class","Frequency","0-10","3","10-20","7","20-30","12","30-40","8"],
 "gold[4]":["Class","Frequency","100-120","5","120-140","10","140-160","k","160-180","5"],
}
for path,d in figs():
    if path in checks:
        texts=re.findall(r'>([^<>]+)</text>',d)
        exp=checks[path]
        if texts!=exp:
            errors.append(f"{path} label mismatch: got {texts} expected {exp}")

print("=== FIG ERRORS ===")
for e in errors: print(" ",e)
print("=== FIG NOTES ===")
for n in notes: print(" ",n)
print("TOTAL",len(errors))
