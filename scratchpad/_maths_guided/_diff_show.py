import json, difflib
live = json.load(open("_checker_live_L06.json",encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=[e for e in dump if e.get("id")=="f6f5708d-edf9-42e6-81d8-49c3cf282310"][0]
old = entry.get("practice_data", entry).get("worked_examples")
new = live.get("worked_examples")
for i in [1,2,3]:
    o=json.dumps(old[i],indent=1,ensure_ascii=False).splitlines()
    n=json.dumps(new[i],indent=1,ensure_ascii=False).splitlines()
    print(f"=== WE[{i}] diff ===")
    for l in difflib.unified_diff(o,n,lineterm=""):
        if l.startswith(("+","-")) and not l.startswith(("+++","---")):
            print(l)
