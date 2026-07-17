import json

ID = "660796ad-070d-4a2d-af11-900e5a5af1c1"
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L07graphs_live.json", encoding="utf-8"))
pre = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-eduqas.json", encoding="utf-8"))

# pre may be dict keyed by id, or list
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    elif "lessons" in pre:
        for l in pre["lessons"]:
            if l.get("id") == ID:
                entry = l.get("practice_data"); break
    else:
        # maybe keyed by key with practice_data
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry = v.get("practice_data"); break
elif isinstance(pre, list):
    for l in pre:
        if l.get("id") == ID:
            entry = l.get("practice_data"); break

if entry is None:
    print("PRE ENTRY NOT FOUND. top type:", type(pre))
    if isinstance(pre, dict):
        print("top keys sample:", list(pre.keys())[:5])
        # show one value shape
        firstk = list(pre.keys())[0]
        print("first val type:", type(pre[firstk]))
        if isinstance(pre[firstk], dict):
            print("first val keys:", list(pre[firstk].keys())[:8])
    raise SystemExit

if "practice_data" in entry:
    entry = entry["practice_data"]

for fld in ("related_videos","topic_links","worked_examples","method_card"):
    same = json.dumps(entry.get(fld), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
    print(f"{fld}: {'SAME' if same else 'DIFFERENT'}  (pre_present={fld in entry})")
    if not same:
        print("  PRE:", json.dumps(entry.get(fld), ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(fld), ensure_ascii=False)[:400])
