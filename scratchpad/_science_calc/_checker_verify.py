import json, re, math
pd = json.load(open("_live_3c4aa292.json", encoding="utf-8"))

# Board-name scan across whole object
raw = json.dumps(pd, ensure_ascii=False)
for board in ["AQA","Edexcel","OCR","WJEC","Eduqas","equation sheet","memorise","equation-sheet"]:
    if board.lower() in raw.lower():
        print("BOARD/SHEET HIT:", board)
# em dash
if "—" in raw: print("EM DASH present")
print("en dashes:", raw.count("–"))

# Check every problem has accept field?
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        has_accept = "accept" in p
        print(f"{tier}[{i}] sols={p['solutions']} unit={p.get('unit')} HT={p.get('higher_only',False)} accept={'accept' in p} ({p.get('accept','-')})")
