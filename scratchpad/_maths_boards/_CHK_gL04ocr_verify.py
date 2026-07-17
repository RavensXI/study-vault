import json, re

ID = "9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
live = json.load(open(r"_CHK_gL04ocr_live.json", encoding="utf-8"))[0]["practice_data"]

# --- em dash / student-facing style scan ---
EM = "—"
def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            # skip internal note fields
            if k == "note":
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EM in obj:
            print("EM DASH:", path, "->", obj[:80])

walk(live, "root")
print("em-dash scan done")

# --- preservation diff vs pre-dump ---
pre_all = json.load(open(r"_pre_dump_maths-ocr.json", encoding="utf-8"))
# find entry for this id
pre = None
if isinstance(pre_all, dict):
    pre = pre_all.get(ID)
    if pre is None:
        # maybe keyed by slug or list
        for k, v in pre_all.items():
            if isinstance(v, dict) and v.get("id") == ID:
                pre = v
                break
elif isinstance(pre_all, list):
    for v in pre_all:
        if isinstance(v, dict) and v.get("id") == ID:
            pre = v
            break
print("pre found:", pre is not None, "| pre_all type:", type(pre_all).__name__)
if isinstance(pre_all, dict):
    print("pre_all keys sample:", list(pre_all.keys())[:5])
