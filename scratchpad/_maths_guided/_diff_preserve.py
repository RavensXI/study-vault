import json
pre=json.load(open('_pre_ratio_L01.json',encoding='utf-8'))
live=json.load(open('_live_ratio_L01.json',encoding='utf-8'))

def eq(a,b): return json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)

for f in ['related_videos','topic_links']:
    print(f, "UNCHANGED" if eq(pre.get(f),live.get(f)) else "CHANGED")

# worked_examples
print("worked_examples", "UNCHANGED" if eq(pre.get('worked_examples'),live.get('worked_examples')) else "CHANGED")
# method_card
print("method_card", "UNCHANGED" if eq(pre.get('method_card'),live.get('method_card')) else "CHANGED")

# problem_bank: compare displays, solutions, options, input_type per problem
for tier in ['bronze','silver','gold']:
    pb_pre=pre['problem_bank'][tier]
    pb_live=live['problem_bank'][tier]
    if len(pb_pre)!=len(pb_live):
        print(f"{tier}: LEN CHANGED {len(pb_pre)} -> {len(pb_live)}")
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        for k in ['display','solutions','options','input_type','calculator']:
            if a.get(k)!=b.get(k):
                print(f"{tier}[{i}].{k}: {a.get(k)!r} -> {b.get(k)!r}")
    # descriptions
for k in ['bronze_description','silver_description','gold_description']:
    if pre['problem_bank'].get(k)!=live['problem_bank'].get(k):
        print(f"problem_bank.{k}: {pre['problem_bank'].get(k)!r} -> {live['problem_bank'].get(k)!r}")
print("done")
