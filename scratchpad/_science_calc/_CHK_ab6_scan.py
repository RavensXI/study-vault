import json, re

d = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/"
pd = json.load(open(d+"_CHK_ab6_canon.json", encoding="utf-8"))

blob = json.dumps(pd, ensure_ascii=False)
# em dash U+2014, en dash U+2013 in student-facing? spec bans em dash. Also board names.
print("EM DASH (\\u2014) count:", blob.count("—"))
# find contexts of en dash 2013 (allowed? spec says no em dash; en dash used in ranges maybe)
print("EN DASH (\\u2013) count:", blob.count("–"))
for board in ["AQA","Edexcel","OCR","Eduqas","WJEC","equation sheet","formula sheet","data sheet","memorise","must remember"]:
    if board.lower() in blob.lower():
        print("BOARD/SHEET TERM FOUND:", board)

# locate en dashes
for m in re.finditer("–", blob):
    print("  en-dash ctx:", blob[max(0,m.start()-40):m.start()+40])
print("---")
# minus sign usage sanity
print("minus sign U+2212 count:", blob.count("−"))
