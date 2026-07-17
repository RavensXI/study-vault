# -*- coding: utf-8 -*-
"""Cross-check every SVG figure's visible labels against the problem numbers,
and validate viewBox height matches the row count."""
import json, io, re
pd = json.load(io.open("lesson_maths-eduqas_probability-statistics-L04.json", encoding="utf-8"))
errs=[]

def texts(svg):
    return re.findall(r'>([^<>]+)</text>', svg)

def viewbox_h(svg):
    m=re.search(r'viewBox="0 0 \d+ (\d+)"', svg); return int(m.group(1))

# expected table figures: (path, header cells, data rows, aria-substrings)
tables = {
    "silver[0]": (("Score","Frequency"), [("2","3"),("3","7"),("4","6"),("5","4")]),
    "silver[1]": (("Class","Frequency"), [("0-10","5"),("10-20","15"),("20-30","10")]),
    "silver[3]": (("Class","Frequency"), [("0-20","8"),("20-40","12"),("40-60","10")]),
    "silver[4]": (("Class","Frequency"), [("0-10","8"),("10-20","15"),("20-30","12"),("30-40","5")]),
    "silver[5]": (("Score","Frequency"), [("1","4"),("2","6"),("3","10"),("4","5"),("5","5")]),
    "gold[0]":   (("Class","Frequency"), [("10-20","4"),("20-30","8"),("30-40","12"),("40-50","6")]),
    "gold[4]":   (("Class","Frequency"), [("0-20","5"),("20-40","10"),("40-60","k"),("60-80","5")]),
}
pb=pd["problem_bank"]
def getp(path):
    t,i=path[:-1].split("["); return pb[t][int(i)]

for path,(hdr,rows) in tables.items():
    svg=getp(path)["display"]
    tx=texts(svg)
    exp=[hdr[0],hdr[1]]
    for l,r in rows: exp+= [l,r]
    if tx!=exp:
        errs.append("%s labels %r != expected %r"%(path,tx,exp))
    # viewBox height = 22*(rows+1)+2
    want_h=22*(len(rows)+1)+2
    if viewbox_h(svg)!=want_h:
        errs.append("%s viewBox h %d != %d"%(path,viewbox_h(svg),want_h))

# opener money bar
op=pd["guided"]["opener"]["steps"]
svgm=[st for st in op if st.get("display")][0]["display"]
mt=texts(svgm)
if mt!=["£5","Ben","£7","Amy","£9","Cal"]:
    errs.append("opener money labels %r"%mt)

if errs:
    print("FIGCHECK FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("FIGCHECK PASS: all 8 figures match their problem numbers; viewBox heights correct")
