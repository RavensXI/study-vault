import json, re

pd = json.load(open("_zchk_canon.json", encoding="utf-8"))
blob = json.dumps(pd, ensure_ascii=False)

# em dash and en dash
print("em-dash count:", blob.count("—"))
print("en-dash count:", blob.count("–"))
for m in re.finditer(r'[^"]{0,25}[–—][^"]{0,25}', blob):
    print("  DASH:", m.group(0))

# board names / equation-sheet claims
for term in ["AQA", "Edexcel", "OCR", "WJEC", "Eduqas", "equation sheet", "formula sheet", "must memorise", "on your sheet", "given to you", "data sheet"]:
    idx = blob.lower().find(term.lower())
    print(f"term {term!r}:", "FOUND" if idx >= 0 else "absent")

# HTML entities in plain-text-ish
for ent in ["&rsquo;", "&amp;", "&nbsp;", "&mdash;"]:
    print(f"entity {ent}:", blob.count(ent))

# write validator input (full practice_data)
json.dump(pd, open("_zchk_valinput.json", "w", encoding="utf-8"), ensure_ascii=False)
print("wrote valinput")
