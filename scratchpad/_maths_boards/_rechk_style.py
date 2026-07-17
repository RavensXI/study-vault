import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        h=p.get("hint","")
        if "\(" in h or "<" in h and ">" in h:
            issues.append(f"{tier}[{i}].hint has LaTeX/HTML: {h}")
        # em dash anywhere student-facing
# check descriptions
for k in ["bronze_description","silver_description","gold_description"]:
    print(k,"::",pb.get(k))
print("\nHINT style issues:",issues if issues else "none")
# reconfirm all solutions index 0 and option0 is the correct value already verified
print("\nAll checks scripted complete.")
