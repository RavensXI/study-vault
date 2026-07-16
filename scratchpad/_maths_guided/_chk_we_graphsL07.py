import json, io, difflib
pd=json.load(io.open("_CHK_graphsL07_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
entry=None
for v in dump:
    if isinstance(v,dict) and v.get("id")==ID: entry=v; break
pre=entry.get("practice_data",entry)
a=json.dumps(pre.get("worked_examples"),indent=1,ensure_ascii=False).splitlines()
b=json.dumps(pd.get("worked_examples"),indent=1,ensure_ascii=False).splitlines()
d=list(difflib.unified_diff(a,b,lineterm="",n=1))
print("WORKED_EXAMPLES DIFF ("+str(len(d))+" lines):")
for line in d: print(line)
print("=== GOLD[3] options PRE ===", pre["problem_bank"]["gold"][3].get("options"))
print("=== GOLD[3] options NOW ===", pd["problem_bank"]["gold"][3].get("options"))
print("method_card same:", json.dumps(pre.get("method_card"),sort_keys=True)==json.dumps(pd.get("method_card"),sort_keys=True))
