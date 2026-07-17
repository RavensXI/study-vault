import json

ID = "9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
live = json.load(open(r"_CHK_gL04ocr_live.json", encoding="utf-8"))[0]["practice_data"]
pre_all = json.load(open(r"_pre_dump_maths-ocr.json", encoding="utf-8"))
pre = None
for v in pre_all:
    if isinstance(v, dict) and v.get("id") == ID:
        pre = v
        break
pd_pre = pre.get("practice_data", pre)

# preservation-critical fields
for f in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(pd_pre.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
    if a != b:
        print("  PRE :", a[:300])
        print("  LIVE:", b[:300])

# What keys existed pre vs live
print("pre keys :", sorted(pd_pre.keys()))
print("live keys:", sorted(live.keys()))

# Check pre problem displays/solutions preserved where not repaired
def bank(pd):
    return pd.get("problem_bank", {})
pb_pre, pb_live = bank(pd_pre), bank(live)
for tier in ["bronze","silver","gold"]:
    pp, pl = pb_pre.get(tier, []), pb_live.get(tier, [])
    print(f"\n{tier}: pre {len(pp)} live {len(pl)}")
    for i in range(max(len(pp), len(pl))):
        dp = pp[i]["display"] if i < len(pp) else "<none>"
        dl = pl[i]["display"] if i < len(pl) else "<none>"
        sp = pp[i].get("solutions") if i < len(pp) else None
        sl = pl[i].get("solutions") if i < len(pl) else None
        # strip svg for display compare
        import re
        dp2 = re.sub(r"<svg.*?</svg>", "[svg]", dp, flags=re.S).strip()
        dl2 = re.sub(r"<svg.*?</svg>", "[svg]", dl, flags=re.S).strip()
        flag = "" if (dp2==dl2 and sp==sl) else "  <-- CHANGED"
        print(f"  [{i}] sol pre={sp} live={sl}{flag}")
        if dp2 != dl2:
            print("      DISP pre :", dp2[:120])
            print("      DISP live:", dl2[:120])
