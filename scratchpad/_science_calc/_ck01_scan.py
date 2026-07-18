import json, io, re
pd=json.load(io.open("_ck01_row0.json",encoding="utf-8"))
blob=json.dumps(pd,ensure_ascii=False)
# board-neutrality / equation-sheet scans
for term in ["AQA","Edexcel","OCR","WJEC","Eduqas","equation sheet","formula sheet","memorise","memorize","on your sheet","given to you"]:
    hits=[m.start() for m in re.finditer(re.escape(term),blob,re.I)]
    if hits: print("TERM HIT:",term,len(hits))
# em dash
if "—" in blob: print("EM DASH FOUND")
else: print("no em dash")
# en dash occurrences (allowed, just note)
print("en dash count:", blob.count("–"))
print("scan done")
