import json, re

pd = json.load(open("_CK_L05_row0.json", encoding="utf-8"))
blob = json.dumps(pd, ensure_ascii=False)

# board names
for b in ["AQA","Edexcel","OCR","WJEC","Eduqas","equation sheet","equation-sheet","memorise","your board"]:
    if b.lower() in blob.lower():
        print("BOARD/SHEET HIT:", b)

# em dashes in student-facing (exclude internal 'note' fields — none here)
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note":
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            # en dash – used in exam_context "2–4"; flag both
            print("DASH", repr(o[:60]), path)

walk(pd)
print("scan done")
