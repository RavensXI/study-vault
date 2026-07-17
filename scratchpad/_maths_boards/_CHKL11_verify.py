import json, re

live = json.load(open("_CHKL11_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))

# find pre entry for this lesson
ID = "04953988-ada8-4eb2-bbd4-401fb67247ff"
preentry = None
if isinstance(pre, dict):
    if ID in pre:
        preentry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                preentry = v
                break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id") == ID:
            preentry = v
            break
print("pre entry found:", preentry is not None)
if preentry is not None:
    pp = preentry.get("practice_data", preentry)
    print("pre practice_data top keys:", list(pp.keys()) if isinstance(pp, dict) else type(pp))
    # Preservation check for key fields
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pp.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {f}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("   pre :", a[:300])
            print("   live:", b[:300])

# SVG tick verification
print("\n--- SVG checks ---")
def check_svg(display, label):
    # extract ticks: text x=.. >LABEL<  and their line x1
    texts = re.findall(r'<text x="([\d.]+)" y="48"[^>]*>([^<]+)</text>', display)
    circles = re.findall(r'<circle cx="([\d.]+)" cy="30" r="5" fill="(none|currentColor)"', display)
    hl = re.findall(r'<line x1="([\d.]+)" y1="30" x2="([\d.]+)" y2="30" stroke="#60a5fa"', display)
    print(f"{label}: ticks={[(v,x) for x,v in texts]}")
    print(f"   circles(cx,fill)={circles}")
    print(f"   highlight={hl}")
    return texts, circles, hl

bronze = live["problem_bank"]["bronze"]
check_svg(bronze[3]["display"], "bronze[3] (-2<=x<6)")
check_svg(bronze[6]["display"], "bronze[6] (1<x<8)")
