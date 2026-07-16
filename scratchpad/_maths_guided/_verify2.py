import json
live=json.load(open('_live_L12.json',encoding='utf-8'))
problems=[]
# collect all box steps that have 'answer' and their 'pre'/'check' expressions
def dump_boxes(steps, tag):
    for i,st in enumerate(steps):
        if 'answer' in st:
            print(f"  {tag}[{i}] answer={st['answer']!r} pre={st.get('pre','')!r}")

print("=== OPENER ===")
dump_boxes(live['guided']['opener']['steps'],'opener')
for tier in ['bronze','silver','gold']:
    print(f"=== TEACH {tier} ===")
    dump_boxes(live['guided']['teach'][tier]['steps'],tier)
