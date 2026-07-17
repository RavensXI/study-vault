import json, os
for f in ["lesson_maths-aqa_algebra-L09.json","lesson_algebra-L09.json","changes_maths-aqa_algebra-L09.json"]:
    if os.path.exists(f):
        d=json.load(open(f,encoding="utf-8"))
        print("===",f,"exists, top keys:", list(d.keys())[:8])
        # look for pound corruption
        s=json.dumps(d,ensure_ascii=False)
        print("   has U+FFFD:", "�" in s, "| has £:", "£" in s, "| len:", len(s))
    else:
        print("===",f,"MISSING")
