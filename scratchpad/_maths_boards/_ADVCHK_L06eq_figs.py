# -*- coding: utf-8 -*-
import json, re
live=json.load(open("_ADVCHK_L06eq_live.json",encoding="utf-8"))

def scan_svg(path, display):
    if "<svg" not in display:
        return
    svg = display[display.find("<svg"):display.find("</svg>")+6]
    # external refs
    for bad in ["http://","https://","xlink:href","<script","url("]:
        if bad in svg:
            print(f"{path}: *** external/script ref: {bad}")
    # hard-coded dark fills in <text>
    for m in re.finditer(r'<text[^>]*fill="([^"]+)"', svg):
        if m.group(1)!="currentColor":
            print(f"{path}: *** text fill not currentColor: {m.group(1)}")
    # region fill opacity present?
    if "<polygon" in svg and "fill-opacity" not in svg:
        print(f"{path}: *** polygon without fill-opacity")
    # collect visible text labels
    labels=[re.sub(r'<[^>]+>','',t) for t in re.findall(r'<text[^>]*>(.*?)</text>', svg)]
    # numbers in problem text (strip svg)
    qtext=re.sub(r'<svg.*?</svg>','',display,flags=re.S)
    qnums=set(re.findall(r'\d+', re.sub(r'<[^>]+>','',qtext)))
    for lab in labels:
        nums=re.findall(r'\d+', lab)
        for n in nums:
            if n not in qnums:
                print(f"{path}: label {lab!r} num {n} NOT in problem numbers {sorted(qnums)}")
    print(f"{path}: labels={labels}  qnums={sorted(qnums)}")

# openers/teach
g=live["guided"]
scan_svg("opener", g["opener"]["display"])
for t in ["bronze","silver","gold"]:
    scan_svg(f"teach.{t}", g["teach"][t]["display"])
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][t]):
        scan_svg(f"{t}[{i}]", p.get("display",""))
