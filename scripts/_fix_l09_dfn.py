import json, re

with open('scripts/_content_physical-education-edexcel/lessons/commercialisation-sponsorship-and-the-media.json', encoding='utf-8') as f:
    data = json.load(f)

# Add a third dfn term inline - replace 'financial and commercial interests' in body
target = 'financial and commercial interests'
replacement = 'financial and <dfn class="term" data-def="The growing dominance of money, media rights and sponsorship in shaping how sport is organised and presented.">commercial interests</dfn>'
data['content_html'] = data['content_html'].replace(target, replacement, 1)

# Add matching glossary entry
terms = [g['term'] for g in data['glossary_terms']]
if 'commercial interests' not in terms:
    data['glossary_terms'].append({'term': 'commercial interests', 'definition': "The growing dominance of money, media rights and sponsorship in shaping how sport is organised and presented."})

with open('scripts/_content_physical-education-edexcel/lessons/commercialisation-sponsorship-and-the-media.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

dfns = re.findall(r'<dfn class="term"', data['content_html'])
print(f'dfn count: {len(dfns)}')
print(f'glossary count: {len(data["glossary_terms"])}')
print('Done')
