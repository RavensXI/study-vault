import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre = json.load(open("_pre_L12.json",encoding="utf-8"))
live = json.load(open("_live_L12.json",encoding="utf-8"))
pw=pre["worked_examples"]; lw=live["worked_examples"]
for i in range(4):
    a=pw[i]; b=lw[i]
    ak=set(a.keys()); bk=set(b.keys())
    if ak!=bk: print(f"we[{i}] keys pre={a.keys()} live={b.keys()}")
    for k in a:
        if k=="steps": continue
        if a.get(k)!=b.get(k):
            print(f"we[{i}].{k}: PRE={a.get(k)!r} LIVE={b.get(k)!r}")
    # steps deep
    for j in range(max(len(a['steps']),len(b['steps']))):
        sa=a['steps'][j] if j<len(a['steps']) else None
        sb=b['steps'][j] if j<len(b['steps']) else None
        if sa!=sb:
            print(f"we[{i}].steps[{j}] keys pre={sa and list(sa.keys())} live={sb and list(sb.keys())}")
            if sa and sb:
                for k in set(list(sa)+list(sb)):
                    if sa.get(k)!=sb.get(k):
                        print(f"    .{k}: PRE={sa.get(k)!r} LIVE={sb.get(k)!r}")
