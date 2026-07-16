import json
LID = "76260360-c757-49f2-a1c6-cf0e389564c3"
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = next(v for v in pre if v.get("id")==LID)
old = entry["practice_data"]
new = json.load(open("_chk_L05_fresh.json", encoding="utf-8"))
print("title:", entry.get("title"), "lnum:", entry.get("lesson_number"))
print("OLD keys:", sorted(old.keys()))
print("NEW keys:", sorted(new.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(old.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(new.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    if not same:
        print("  OLD:", json.dumps(old.get(f),ensure_ascii=False)[:500])
        print("  NEW:", json.dumps(new.get(f),ensure_ascii=False)[:500])
# check old problem displays/solutions vs new
def banks(pd):
    b=pd.get("problem_bank",{})
    out={}
    for t in ["bronze","silver","gold"]:
        out[t]=[(p.get("display"),tuple(p.get("solutions",[]))) for p in b.get(t,[])]
    return out
ob,nb=banks(old),banks(new)
for t in ["bronze","silver","gold"]:
    print(f"--- {t}: old {len(ob[t])} new {len(nb[t])}")
    for i,(o,n) in enumerate(zip(ob[t],nb[t])):
        flag = "" if o==n else "  <<< CHANGED"
        if o!=n:
            print(f"  [{i}] OLD {o}  NEW {n}{flag}")
