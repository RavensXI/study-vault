import json

ID = "431cf470-df7f-4654-8c83-df7aeb1e0322"
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
pre = json.load(open(base + r"\_pre_dump_maths-aqa.json", encoding="utf-8"))
live = json.load(open(base + r"\_CHK_algL04_live.json", encoding="utf-8"))

# pre_dump structure: find entry
entry = None
if isinstance(pre, list):
    for e in pre:
        if e.get("id") == ID:
            entry = e; break
elif isinstance(pre, dict):
    entry = pre.get(ID)
    if entry is None and "lessons" in pre:
        for e in pre["lessons"]:
            if e.get("id") == ID:
                entry = e; break

print("entry found:", entry is not None)
if entry is None:
    print("pre keys sample:", list(pre)[:3] if isinstance(pre,dict) else "list len "+str(len(pre)))
    raise SystemExit

ppd = entry.get("practice_data") or entry.get("practice_data".upper()) or entry
if "practice_data" in entry:
    ppd = entry["practice_data"]
print("pre practice_data keys:", list(ppd.keys()))

for field in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(ppd.get(field), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"{field}: preserved={same}")
    if not same:
        print("  PRE :", json.dumps(ppd.get(field), ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(field), ensure_ascii=False)[:400])

# Also compare problem displays / solutions preserved vs changed
print("\n=== bank display/solution diff pre vs live ===")
for tier in ["bronze","silver","gold"]:
    pre_bank = ppd.get("problem_bank",{}).get(tier,[])
    live_bank = live.get("problem_bank",{}).get(tier,[])
    print(f"[{tier}] pre={len(pre_bank)} live={len(live_bank)}")
    for i in range(max(len(pre_bank),len(live_bank))):
        pd = pre_bank[i].get("display") if i < len(pre_bank) else "<none>"
        ld = live_bank[i].get("display") if i < len(live_bank) else "<none>"
        ps = pre_bank[i].get("solutions") if i < len(pre_bank) else None
        ls = live_bank[i].get("solutions") if i < len(live_bank) else None
        flag = "" if (pd==ld and ps==ls) else "  <-- CHANGED"
        print(f"  {i}: sol pre={ps} live={ls}{flag}")
        if pd != ld:
            print(f"      disp pre : {pd}")
            print(f"      disp live: {ld}")
