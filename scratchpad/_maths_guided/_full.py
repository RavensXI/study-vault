import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
L=json.load(open("_live_L04_refetch.json",encoding="utf-8"))

issues=[]

# ---- preservation vs pre-dump ----
try:
    dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
    # find L04 entry
    entry=None
    if isinstance(dump,dict):
        for k,v in dump.items():
            if "1d039d5e" in str(k): entry=v
        if entry is None and "1d039d5e-b358-4864-b935-b3334ba99d20" in dump:
            entry=dump["1d039d5e-b358-4864-b935-b3334ba99d20"]
    if isinstance(dump,list):
        for row in dump:
            if row.get("id")=="1d039d5e-b358-4864-b935-b3334ba99d20" or "1d039d5e" in json.dumps(row)[:200]:
                entry=row; break
    if entry is not None:
        pd=entry.get("practice_data",entry)
        for fld in ["related_videos","topic_links","worked_examples"]:
            a=json.dumps(pd.get(fld),sort_keys=True,ensure_ascii=False)
            b=json.dumps(L.get(fld),sort_keys=True,ensure_ascii=False)
            print(f"PRESERVE {fld}: {'SAME' if a==b else 'CHANGED'}")
            if a!=b:
                issues.append(f"{fld} changed from pre-dump")
                print("   pre:",a[:300]); print("   now:",b[:300])
    else:
        print("PRE-DUMP: L04 entry not found; keys sample:", (list(dump)[:3] if isinstance(dump,dict) else type(dump)))
except FileNotFoundError:
    print("PRE-DUMP file not found")

print()
# ---- expects reproduce ----
def check(cond,msg):
    if not cond: issues.append(msg); print("  FAIL:",msg)

# manual expect verification map: (tier,idx)->list of (pattern, computed_wrong)
# I compute each error's result:
exp={
 ("gold",0):[("range_is_largest",10)],
 ("gold",1):[("wrong_count",[120,10])],
 ("gold",2):[("averaged_means",24)],
 ("gold",3):[("used_lower_bounds",14.67)],
 ("gold",4):[("forgot_extra_count",36)],
 ("bronze",0):[("forgot_to_divide",30)],
 ("bronze",2):[("frequency_not_value",3)],
 ("bronze",3):[("added_not_subtracted",17)],
 ("bronze",4):[("picked_one_middle",6)],
 ("bronze",5):[("divided_not_multiplied",1.6)],
 ("bronze",6):[("forgot_to_divide",90)],
 ("bronze",7):[("sign_error",4)],
 ("silver",0):[("divided_by_rows",12.25)],
 ("silver",1):[("averaged_values",15)],
 ("silver",2):[("used_lower_bounds",11.2)],
 ("silver",3):[("included_median",5)],
 ("silver",4):[("averaged_means",68.5)],
 ("silver",5):[("gave_upper_bound",15)],
 ("silver",6):[("off_by_one_class",15)],
}
for (tier,idx),lst in exp.items():
    p=L["problem_bank"][tier][idx]
    mc={m["pattern"]:m["expect"] for m in p.get("misconceptions",[])}
    for pat,want in lst:
        got=mc.get(pat,"<<missing>>")
        ok = got==want
        print(f"EXPECT {tier}[{idx}] {pat}: stored={got} computed={want} {'OK' if ok else 'MISMATCH'}")
        check(ok,f"{tier}[{idx}] misconception {pat} expect stored={got} but committing error gives {want}")

print()
# ---- final box lands on solution ----
def lastbox(gs):
    boxes=[s["answer"] for s in gs if "answer" in s]
    return boxes
# For each problem verify the ANSWER-producing box (the one before check) equals solution
# heuristic: the box whose done/say announces the answer. We just confirm the solution value appears among boxes.
for tier in ["gold","bronze","silver"]:
    for j,p in enumerate(L["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s["answer"] for s in gs if "answer" in s]
        sols=p["solutions"]
        # solution value(s) must appear in boxes
        present=all(any(abs(sv-b)<1e-9 if isinstance(b,(int,float)) and isinstance(sv,(int,float)) else sv==b for b in boxes) for sv in sols)
        if not present:
            issues.append(f"{tier}[{j}] solution {sols} not reached by any box {boxes}")
            print(f"  BOXMISS {tier}[{j}] sols={sols} boxes={boxes}")

print("\nISSUES:",len(issues))
for i in issues: print(" -",i)
