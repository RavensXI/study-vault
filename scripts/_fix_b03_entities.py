import json

def fix_entities_in_plain_text(s):
    replacements = [
        ('&mdash;', '—'),
        ('&ndash;', '–'),
        ('&rsquo;', '’'),
        ('&lsquo;', '‘'),
        ('&rdquo;', '”'),
        ('&ldquo;', '“'),
        ('&amp;', '&'),
        ('&nbsp;', ' '),
    ]
    for ent, uni in replacements:
        s = s.replace(ent, uni)
    return s

def fix_plain_text_fields(data):
    for pq in data.get('practice_questions', []):
        for field in ['text', 'type', 'marks']:
            if field in pq:
                pq[field] = fix_entities_in_plain_text(pq[field])
    for kc in data.get('knowledge_checks', []):
        for field in ['q']:
            if field in kc:
                kc[field] = fix_entities_in_plain_text(kc[field])
        for opt_list in ['options', 'left', 'right']:
            if opt_list in kc:
                kc[opt_list] = [fix_entities_in_plain_text(o) for o in kc[opt_list]]
    for fc in data.get('flashcard_questions', []):
        for field in ['q', 'a']:
            if field in fc:
                fc[field] = fix_entities_in_plain_text(fc[field])
    for gt in data.get('glossary_terms', []):
        for field in ['term', 'definition']:
            if field in gt:
                gt[field] = fix_entities_in_plain_text(gt[field])
    for field in ['description', 'hero_image_caption']:
        if field in data:
            data[field] = fix_entities_in_plain_text(data[field])
    return data

slugs = [
    'physical-emotional-and-social-wellbeing',
    'lifestyle-choices-and-sedentary-living',
    'diet-nutrition-and-hydration',
    'classification-of-skills-and-practice-structures',
    'goal-setting-and-smart-targets',
    'guidance-and-feedback-in-sport',
    'mental-preparation-for-performance',
    'engagement-patterns-in-sport',
    'commercialisation-sponsorship-and-the-media',
    'ethical-behaviour-and-deviance-in-sport',
    'performance-enhancing-drugs-recap-and-application',
    'interpreting-data-on-health-and-participation',
    'revision-synthesis-component-2-synoptic-practice',
]

for slug in slugs:
    path = f'scripts/_content_physical-education-edexcel/lessons/{slug}.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    data = fix_plain_text_fields(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Fixed: {slug}')

print('All done')
