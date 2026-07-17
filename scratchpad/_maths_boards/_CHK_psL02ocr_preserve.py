import json

live = json.load(open("_CHK_psL02ocr_live.json", encoding="utf-8"))["practice_data"]
dump = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))

# pre-dump structure: find the L02 / venn lesson
def find(d):
    if isinstance(d, dict):
        # could be keyed by id or a list
        for k,v in d.items():
            yield k,v
key = None
# inspect top structure
print("dump top type:", type(dump))
if isinstance(dump, dict):
    print("dump keys sample:", list(dump.keys())[:5])
elif isinstance(dump, list):
    print("dump list len:", len(dump))
    print("sample item keys:", list(dump[0].keys()) if dump else None)

SID = "1a8441e6-115c-473e-a9b7-a2276e5b7faa"
entry = None
if isinstance(dump, dict):
    if SID in dump:
        entry = dump[SID]
    else:
        for k,v in dump.items():
            if isinstance(v,dict) and (v.get("id")==SID or v.get("slug","").startswith("venn")):
                entry = v; break
elif isinstance(dump, list):
    for v in dump:
        if v.get("id")==SID or v.get("slug","")=="venn-diagrams-and-conditional-probability":
            entry = v; break
print("found entry:", entry is not None)
if entry:
    pdp = entry.get("practice_data", entry)
    for fld in ("related_videos","topic_links","worked_examples"):
        a = json.dumps(pdp.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"{fld}: {'SAME' if a==b else 'DIFF'}")
        if a!=b:
            print("  PRE :", a[:300])
            print("  LIVE:", b[:300])
    # display texts preserved?
    print("pre keys:", list(pdp.keys()))
