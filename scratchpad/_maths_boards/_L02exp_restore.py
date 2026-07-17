# -*- coding: utf-8 -*-
import json, io
ID="a1bdc834-74b8-41cf-8671-c1e3e5270619"
live=json.load(io.open("_L02exp_live.json",encoding="utf-8"))
pd=live["practice_data"]
pre=json.load(io.open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
pe=next(e for e in pre if e["id"]==ID)
good_we=pe["practice_data"]["worked_examples"]
# sanity: correct topical examples
assert len(good_we)==3
assert good_we[0]["question"]=="Expand 3(x + 4)"
assert good_we[1]["question"]=="Expand (x + 2)(x + 5)"
assert good_we[2]["question"]=="Expand (2x - 1)(3x + 4)"
# show what we're replacing
print("BEFORE worked_examples:")
for w in pd["worked_examples"]:
    print("   ", w["difficulty"], w["question"])
pd["worked_examples"]=good_we
print("AFTER worked_examples:")
for w in pd["worked_examples"]:
    print("   ", w["difficulty"], w["question"])
# write full pd for validator + patch payload
json.dump(pd, io.open("_L02exp_patched_pd.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("top keys after:", sorted(pd.keys()))
print("written _L02exp_patched_pd.json")
