import json, io, re
live=json.load(io.open("_live_graphs-L01.json",encoding="utf-8"))["practice_data"]
pb=live["problem_bank"]
# chart verification
for t,i in [("bronze",6),("bronze",7)]:
    p=pb[t][i]; ch=p["chart"]; ds=ch["data"]["datasets"][0]["data"]; labs=ch["data"]["labels"]
    print(f"{t}[{i}] labels={labs} data={ds} sol={p['solutions']}")
    # bronze6 asks y at x=3 -> data[3]; bronze7 gradient
    if i==6: print("  y at x=3 =", ds[3], "expected 7")
    if i==7:
        grads=set((ds[k+1]-ds[k]) for k in range(len(ds)-1))
        print("  step gradients:", grads, "expected {-2}")
# theme safety: scan all svg <text> for hard-coded non-currentColor fills
def walk(o):
    if isinstance(o,dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
    elif isinstance(o,str): yield o
bad=[]
ext=[]
for s in walk(live):
    if "<svg" in s:
        for m in re.finditer(r'<text[^>]*fill="([^"]+)"', s):
            if m.group(1)!="currentColor": bad.append(m.group(1))
        if "href" in s or "http" in s or "<script" in s: ext.append(s[:40])
print("non-currentColor text fills:", bad)
print("external refs in svg:", ext)
