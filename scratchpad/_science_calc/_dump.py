import json, io
d=json.load(open('_live_L05.json',encoding='utf-8'))['canonical']
out=io.StringIO()
def p(*a): print(*a, file=out)

p("========== TEACH WALKS ==========")
for tier, walk in d['guided']['teach'].items():
    p(f"\n--- TEACH {tier} ---")
    p(json.dumps(walk, indent=1, ensure_ascii=False))

p("\n\n========== TIER GUIDES ==========")
for tier, g in d['tier_guides'].items():
    p(f"\n--- {tier} ---")
    p(json.dumps(g, indent=1, ensure_ascii=False))

p("\n\n========== DESCRIPTIONS ==========")
for k in ['bronze_description','silver_description','gold_description']:
    p(k, ':', d['problem_bank'].get(k))

open('_readable_walks.txt','w',encoding='utf-8').write(out.getvalue())
print("done")
