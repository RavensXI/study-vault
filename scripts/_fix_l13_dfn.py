import json, re

with open('scripts/_content_physical-education-edexcel/lessons/revision-synthesis-component-2-synoptic-practice.json', encoding='utf-8') as f:
    data = json.load(f)

html = data['content_html']

# Add dfn for 'sport psychology'
old1 = 'knowledge from sport psychology (Unit 2 Topic 2) and socio-cultural influences'
new1 = 'knowledge from <dfn class="term" data-def="The study of how psychological factors affect performance and participation in sport, including motivation, mental preparation, skill learning and feedback.">sport psychology</dfn> (Topic 2) and socio-cultural influences'
html = html.replace(old1, new1, 1)

# Add dfn for 'socio-cultural influences'
old2 = 'and <dfn class="term" data-def="The study of how psychological factors affect performance and participation in sport, including motivation, mental preparation, skill learning and feedback.">sport psychology</dfn> (Topic 2) and socio-cultural influences (Unit 2 Topic 3)'
new2 = 'and <dfn class="term" data-def="The study of how psychological factors affect performance and participation in sport, including motivation, mental preparation, skill learning and feedback.">sport psychology</dfn> (Topic 2) and <dfn class="term" data-def="The external social, cultural and economic factors that shape who participates in sport and how sport is organised and governed.">socio-cultural influences</dfn> (Topic 3)'

# Simpler - just replace the text in the general prose
old2 = 'socio-cultural influences (Unit 2 Topic 3) in a single extended response'
new2 = '<dfn class="term" data-def="The external social, cultural and economic factors that shape who participates in sport and how sport is organised.">socio-cultural influences</dfn> (Topic 3) in a single extended response'
html = html.replace(old2, new2, 1)

# If neither worked, try an even simpler replacement
dfns_now = len(re.findall(r'<dfn class="term"', html))
if dfns_now < 2:
    # Add dfn to 'sport psychology and socio-cultural' in body paragraph
    old3 = 'The sport psychology topics covered in this unit are'
    new3 = 'The <dfn class="term" data-def="The study of psychological factors that affect sport performance, including mental preparation, skill learning, motivation and feedback.">sport psychology</dfn> topics covered in this unit are'
    html = html.replace(old3, new3, 1)

if dfns_now < 3:
    old4 = 'The socio-cultural topics are'
    new4 = 'The <dfn class="term" data-def="Topics covering how gender, age, income, ethnicity, disability, media and ethics shape participation and sporting behaviour.">socio-cultural</dfn> topics are'
    html = html.replace(old4, new4, 1)

data['content_html'] = html

# Update glossary to match dfns (need at least 3 entries and must match dfn count)
terms_in_glossary = [g['term'] for g in data['glossary_terms']]
if 'sport psychology' not in terms_in_glossary:
    data['glossary_terms'].append({'term': 'sport psychology', 'definition': 'The study of how psychological factors affect performance and participation in sport, including motivation, mental preparation and skill learning.'})
if 'socio-cultural' not in terms_in_glossary:
    data['glossary_terms'].append({'term': 'socio-cultural', 'definition': 'Relating to the combined social and cultural factors that shape people\'s behaviour, opportunities and engagement with sport.'})

with open('scripts/_content_physical-education-edexcel/lessons/revision-synthesis-component-2-synoptic-practice.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

dfns = re.findall(r'<dfn class="term"', data['content_html'])
print(f'dfn count: {len(dfns)}')
print(f'glossary count: {len(data["glossary_terms"])}')
print('Done')
