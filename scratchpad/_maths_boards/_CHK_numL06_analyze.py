import json, re

ID = "d15fddc3-0766-4882-bfc8-15a0b7208d89"
live = json.load(open("_CHK_numL06_live.json", encoding="utf-8"))["practice_data"]

# em dash scan across student-facing strings (exclude internal 'note')
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note":  # internal exempt
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash = []
for p, s in walk(live):
    if "—" in s:
        emdash.append((p, s))
print("=== EM DASHES ===", len(emdash))
for p,s in emdash[:20]:
    print(p, "::", s[:80])

# Preservation vs pre-dump
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
entry = None
if isinstance(pre, dict):
    # maybe keyed by id
    if ID in pre:
        entry = pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry=v; break
elif isinstance(pre, list):
    for v in pre:
        if isinstance(v, dict) and v.get("id")==ID:
            entry=v; break
print("\n=== PREDUMP entry found:", entry is not None)
if entry:
    pdold = entry.get("practice_data", entry)
    for field in ["related_videos","topic_links","worked_examples"]:
        old = pdold.get(field)
        new = live.get(field)
        same = json.dumps(old, sort_keys=True, ensure_ascii=False)==json.dumps(new, sort_keys=True, ensure_ascii=False)
        print(f"{field}: preserved={same}")
        if not same:
            print("  OLD:", json.dumps(old, ensure_ascii=False)[:400])
            print("  NEW:", json.dumps(new, ensure_ascii=False)[:400])
    print("predump top keys:", list(pdold.keys()))
