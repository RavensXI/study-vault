"""Match hero-less drama-aqa lessons against the hero index using subject-relevance filtering.

Writes a match plan to /tmp/drama_hero_plan.json for review before applying.
"""
import sys, json, glob, re, os
sys.path.insert(0, os.path.dirname(__file__))
from lib.supabase_client import get_client
from lib.hero_index import _load

# Subjects whose imagery is visually plausible for Drama lessons.
ALLOWED = {
    'drama', 'drama-aqa',
    'english-literature', 'english-literature-aqa', 'english-literature-edexcel',
    'english-literature-eduqas', 'english-literature-ocr',
    'history', 'history-aqa', 'history-edexcel',
    'music', 'music-technology', 'gcse-music',
    'citizenship-aqa',
    'religious-education',
    'art-design',
}

STOP = {'the','a','an','and','or','but','in','on','at','to','for','of','with','by','from','is','it','as','be','was','are','were','been','being','have','has','had','do','does','did','will','would','could','should','may','might','shall','can','this','that','these','those','how','what','which','who','whom','when','where','why','your','our','their','my','his','her','we','you','they','us','them','he','she','lesson','lessons','unit','part','paper','using','used','between','through','into','over','after','before','during','about','each','other','than','then','some','such','only','also','just','more','most','very','well','back','much','many','own','way','long','make','like','new','first','come','know','take','get','made','find','here','thing','world','still','need','too','any','right','not','now','old'}


def main():
    sb = get_client()
    sid = sb.table('subjects').select('id').eq('slug', 'drama-aqa').is_('school_id', 'null').execute().data[0]['id']
    units = sb.table('units').select('id,slug').eq('subject_id', sid).execute().data

    existing = sb.table('lessons').select('hero_image_url').not_.is_('hero_image_url', 'null').in_('unit_id', [u['id'] for u in units]).execute().data
    already_used = {x['hero_image_url'] for x in existing if x.get('hero_image_url')}
    print(f'Already-used drama-aqa hero URLs: {len(already_used)}')

    missing = []
    for u in units:
        L = sb.table('lessons').select('id,lesson_number,title,slug').eq('unit_id', u['id']).is_('hero_image_url', 'null').execute().data
        for x in L:
            x['unit_slug'] = u['slug']
            missing.append(x)
    print(f'Lessons without hero: {len(missing)}')

    content_by_slug = {}
    for fp in glob.glob('scripts/_content_drama-aqa/lessons/*.json'):
        d = json.load(open(fp, encoding='utf-8'))
        if d.get('_lesson_slug'):
            content_by_slug[d['_lesson_slug']] = d

    idx = _load()
    filtered_idx = [e for e in idx if e['subject'] in ALLOWED]
    print(f'Hero index entries (filtered to drama-relevant subjects): {len(filtered_idx)}')

    def search_filtered(query, exclude_urls):
        qwords = set(re.sub(r'[^a-z0-9\s]', ' ', query.lower()).split()) - STOP
        if not qwords:
            return None
        best = None
        for entry in filtered_idx:
            if entry['hero_url'] in exclude_urls:
                continue
            tags = set(entry.get('tags', [])) - STOP
            title_words = set(re.sub(r'[^a-z0-9\s]', ' ', entry['title'].lower()).split()) - STOP
            title_hits = len(qwords & title_words)
            tag_hits = len(qwords & tags)
            score = (title_hits * 3) + tag_hits
            if entry['subject'] in ('drama', 'drama-aqa'):
                score += 2
            if entry['subject'].startswith('english-literature'):
                score += 1
            if score >= 2 and (not best or score > best['_score']):
                best = dict(entry)
                best['_score'] = score
        return best

    plan = []
    exclude = set(already_used)
    for L in missing:
        content = content_by_slug.get(L['slug'])
        if not content:
            plan.append({'lesson': L, 'best': None, 'reason': 'no content JSON'})
            continue
        keywords = content.get('hero_keywords', [])
        caption = content.get('hero_image_caption', '')
        query_text = ' '.join([L['title'], L['unit_slug'].replace('-', ' '), ' '.join(keywords)])
        best = search_filtered(query_text, exclude)
        if best:
            exclude.add(best['hero_url'])
        plan.append({'lesson': L, 'caption': caption, 'best': best, 'keywords': keywords})

    matched = sum(1 for p in plan if p['best'])
    print(f'\nMatched: {matched}/{len(plan)}')
    print('Sample:')
    for p in plan[:18]:
        L = p['lesson']
        if p['best']:
            print(f'  L{L["lesson_number"]:2d} {L["title"][:46]:46s} -> [{p["best"]["subject"]:22s}] {p["best"]["title"][:40]} (score {p["best"]["_score"]})')
        else:
            print(f'  L{L["lesson_number"]:2d} {L["title"][:46]:46s} -> NO MATCH')

    out = []
    for p in plan:
        out.append({
            'lesson_id': p['lesson']['id'],
            'lesson_slug': p['lesson']['slug'],
            'unit_slug': p['lesson']['unit_slug'],
            'lesson_number': p['lesson']['lesson_number'],
            'title': p['lesson']['title'],
            'best_url': p['best']['hero_url'] if p['best'] else None,
            'best_title': p['best']['title'] if p['best'] else None,
            'best_subject': p['best']['subject'] if p['best'] else None,
            'score': p['best']['_score'] if p['best'] else 0,
            'caption': p.get('caption', ''),
        })
    with open('/tmp/drama_hero_plan.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('\nPlan saved to /tmp/drama_hero_plan.json')


if __name__ == '__main__':
    main()
