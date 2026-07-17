import json, re
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_live_L01.json", encoding="utf-8"))
SID="32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
entry=[e for e in pre if e.get("id")==SID][0]["practice_data"]
def strip_svg(d):
    # remove svg, keep trailing text
    d = re.sub(r'<svg.*?</svg>', '', d, flags=re.S)
    d = re.sub(r'<[^>]+>','',d)
    return d.strip()
for tier in ["bronze","silver","gold"]:
    pb_pre = entry["problem_bank"].get(tier,[])
    pb_live = live["problem_bank"].get(tier,[])
    print(f"=== {tier}: pre {len(pb_pre)} live {len(pb_live)}")
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        sol_same = a.get("solutions")==b.get("solutions")
        disp_same = strip_svg(a.get("display",""))==strip_svg(b.get("display",""))
        it_same = a.get("input_type")==b.get("input_type")
        flag = "" if (sol_same and it_same) else "  <-- CHANGED"
        print(f" [{i}] sol {a.get('solutions')} -> {b.get('solutions')} same={sol_same} disp_text_same={disp_same} it_same={it_same}{flag}")
        if not disp_same:
            print("     PRE :", strip_svg(a.get('display','')))
            print("     LIVE:", strip_svg(b.get('display','')))
