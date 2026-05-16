import json, re

with open('scripts/_content_physical-education-edexcel/lessons/commercialisation-sponsorship-and-the-media.json', encoding='utf-8') as f:
    data = json.load(f)

# Find a good place to add a third dfn - in "Positive impacts" for Spectators section
# The word "commercialisation" appears without dfn in "Positive impacts" paragraph
target = 'This commercial reality has transformed sport'
replacement = 'This <dfn class="term" data-def="The growing influence of financial, media and sponsorship interests on how sport is structured and presented.">commercial reality</dfn> has transformed sport'
if target in data['content_html']:
    data['content_html'] = data['content_html'].replace(target, replacement, 1)
    print('Replaced via target 1')
else:
    # Try alternative
    target2 = 'media is essential for evaluating both the benefits and the distortions that commercialisation'
    replacement2 = 'media is essential for evaluating both the benefits and the distortions that <dfn class="term" data-def="The process by which sport becomes increasingly shaped by financial motives, broadcasting rights and sponsorship.">commercialisation</dfn>'
    if target2 in data['content_html']:
        data['content_html'] = data['content_html'].replace(target2, replacement2, 1)
        print('Replaced via target 2')
    else:
        # Final fallback - add dfn to the golden triangle paragraph
        target3 = 'describes the three-way relationship between sport'
        replacement3 = 'describes the three-way <dfn class="term" data-def="A set of interconnected relationships between organisations or entities where each sustains the others.">relationship</dfn> between sport'
        data['content_html'] = data['content_html'].replace(target3, replacement3, 1)
        print('Replaced via target 3')

terms = [g['term'] for g in data['glossary_terms']]
if 'commercial reality' not in terms and 'commercialisation' not in terms and 'relationship' not in terms:
    data['glossary_terms'].append({'term': 'commercialisation', 'definition': 'The process by which sport becomes increasingly shaped by financial motives, broadcasting rights and sponsorship.'})

with open('scripts/_content_physical-education-edexcel/lessons/commercialisation-sponsorship-and-the-media.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

dfns = re.findall(r'<dfn class="term"', data['content_html'])
print(f'dfn count: {len(dfns)}')
print(f'glossary count: {len(data["glossary_terms"])}')
