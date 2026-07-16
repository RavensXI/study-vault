import json
live = json.load(open('_live_graphs_l05.json', encoding='utf-8'))
pb = live['problem_bank']
issues = []
for tier in ['bronze', 'silver', 'gold']:
    for i, p in enumerate(pb[tier]):
        h = p.get('hint', '')
        if '\\(' in h or '<' in h:
            issues.append((f'{tier}[{i}].hint', h))
        for j, st in enumerate(p.get('guided_steps', [])):
            for f in ('pre', 'post'):
                v = st.get(f, '')
                if v and ('\\(' in v or '<' in v):
                    issues.append((f'{tier}[{i}].guided_steps[{j}].{f}', v))
            if 'answer' in st and not isinstance(st.get('answer'), (int, float)):
                issues.append((f'{tier}[{i}].gs[{j}].answer', st.get('answer')))
print('hint/pre/post/answer issues:', len(issues))
for x in issues:
    print('  ', x)
# teach + opener numeric boxes, pre/post plain
for tier in ['bronze', 'silver', 'gold']:
    for j, st in enumerate(live['guided']['teach'][tier]['steps']):
        if 'answer' in st and not isinstance(st['answer'], (int, float)):
            print('teach nonnum', tier, j)
        for f in ('pre', 'post'):
            v = st.get(f, '')
            if v and ('\\(' in v or '<' in v):
                print('teach pre/post latex', tier, j, f)
for j, st in enumerate(live['guided']['opener']['steps']):
    if 'answer' in st and not isinstance(st['answer'], (int, float)):
        print('opener nonnum', j)
# tier_guides step word budget
for tier in ['bronze', 'silver', 'gold']:
    tg = live['tier_guides'][tier]
    words = sum(len(s.split()) for s in tg['steps'])
    print(f'tier_guides {tier}: {len(tg["steps"])} steps, {words} words, title={tg["title"]!r}')
print('done')
