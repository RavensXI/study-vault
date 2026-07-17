# -*- coding: utf-8 -*-
import json, re

live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L11_live.json", encoding="utf-8"))

# ---- em dash / style scan on student-facing strings ----
EMDASH = "—"
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            # skip internal note fields
            if k == "note":
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash_hits = []
entity_hits = []
for p, s in walk(live):
    if EMDASH in s:
        emdash_hits.append((p, s))
    if re.search(r"&(rsquo|lsquo|amp|lt|gt|nbsp|mdash|ndash|deg|times|divide|le|ge|hellip|pound|eacute);", s):
        entity_hits.append((p, s))

print("EM DASH hits:", len(emdash_hits))
for p, s in emdash_hits:
    print("  ", p, "::", s[:90])
print("HTML ENTITY hits:", len(entity_hits))
for p, s in entity_hits[:20]:
    print("  ", p, "::", s[:90])

# ---- preservation vs pre-dump ----
pre = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-aqa.json", encoding="utf-8"))
# pre may be list of rows or dict keyed by id/key
ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
prerow = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id") == ID or r.get("lesson_id") == ID:
            prerow = r
            break
    if prerow is None:
        # maybe keyed by slug algebra-L11
        for r in pre:
            if str(r.get("key")) == "algebra-L11" or str(r.get("slug","")).endswith("algebra-L11"):
                prerow = r
                break
elif isinstance(pre, dict):
    prerow = pre.get(ID) or pre.get("algebra-L11")
print("\nPRE-DUMP row found:", prerow is not None, "| type:", type(pre).__name__, "| len:", len(pre) if hasattr(pre,'__len__') else '?')
if isinstance(pre, list) and pre:
    print("sample pre keys:", list(pre[0].keys())[:12])
