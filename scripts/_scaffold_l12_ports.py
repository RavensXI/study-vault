"""Scaffold l12-retail-business + l12-sport-and-coaching-principles (Eduqas/WJEC
L1/2 Vocational Awards, Unit 1 exam content only). Subject=live, lessons=
pending_review, content filled later. NO spec codes in any text. Idempotent."""
import sys, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

PLANS = {
    'l12-retail-business': {
        'name': 'Retail Business', 'board': 'Eduqas / WJEC', 'code': '5299QA', 'accent': '#b45309',
        'units': [
            ('the-retail-business-environment', 'The Retail Business Environment',
             'Types, scale, ownership, aims, functional areas and the supply chain of retail businesses.',
             [('Types of Retail Business and Activity', 'Retail activity, channels and the main types of retail business.'),
              ('Scale and Ownership of Retail Businesses', 'Micro to large retailers and the forms of business ownership.'),
              ('Aims of Retail Businesses', 'Survival, profit, growth, customer service and other retail aims.'),
              ('Functional Areas and the Supply Chain', 'How retail departments work together and how goods reach the shelf.')]),
            ('the-competitive-and-dynamic-environment', 'The Competitive and Dynamic Environment',
             'Competition, location, external factors and seasonality in retail.',
             [('The Competitive Environment', 'Competition, market share and how retailers gain an advantage.'),
              ('Retail Location', 'Choosing where to locate a retail business and why it matters.'),
              ('External Factors and Seasonality', 'Economic, social and seasonal influences on retail businesses.')]),
            ('using-retail-business-data', 'Using Retail Business Data',
             'Reading, calculating and interpreting retail data to make business judgements.',
             [('Retail Data and Its Formats', 'Tables, charts and graphs used to present retail business data.'),
              ('Calculating Retail Business Data', 'Percentages, averages, profit and other retail calculations.'),
              ('Interpreting Data and Making Judgements', 'Reading retail data to draw conclusions and recommend solutions.')]),
        ],
    },
    'l12-sport-and-coaching-principles': {
        'name': 'Sport and Coaching Principles', 'board': 'Eduqas / WJEC', 'code': '5259QA', 'accent': '#0891b2',
        'units': [
            ('body-systems', 'Body Systems',
             'Structure and function of the body systems and the effects of exercise on them.',
             [('The Structure of Body Systems', 'Skeletal, muscular, cardiovascular and respiratory system structure.'),
              ('The Functions of Body Systems', 'What the skeletal, muscular, cardiovascular and respiratory systems do.'),
              ('Short-Term Effects of Exercise', 'How the body responds during a single bout of exercise.'),
              ('Long-Term Adaptations of Exercise', 'How the body systems adapt to regular training over time.')]),
            ('health-and-fitness', 'Health and Fitness',
             'Components of health and fitness, fitness testing and why it matters.',
             [('Components of Health and Fitness', 'Aerobic endurance, strength, flexibility and the other components.'),
              ('Measuring Health and Fitness', 'Fitness tests for each component and how they are carried out.'),
              ('Why Fitness Testing Is Important', 'Reasons for testing fitness and how the results are used.')]),
            ('principles-of-training', 'Principles of Training',
             'Factors before training, the principles of training and the main training methods.',
             [('Factors to Consider Before Training', 'Health screening, goals and safety before starting a programme.'),
              ('The Principles of Training', 'Specificity, progression, overload, reversibility and the FITT principle.'),
              ('Training Methods', 'Continuous, interval, circuit, weight and other training methods.')]),
        ],
    },
}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    for slug, p in PLANS.items():
        ex = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').execute().data
        if ex and any(sb.table('lessons').select('id').eq('unit_id', u['id']).execute().data
                      for u in sb.table('units').select('id').eq('subject_id', ex[0]['id']).execute().data):
            print(f"[ABORT] {slug} already has lessons — skip"); continue
        nl = sum(len(u[3]) for u in p['units'])
        print(f"{slug}: {len(p['units'])} units, {nl} lessons (subject live, lessons pending_review)")
        if not args.commit:
            continue
        settings = {'practice_units': [], 'has_exam_guides': True}
        sid = sb.table('subjects').insert({'slug': slug, 'name': p['name'], 'exam_board': p['board'],
            'spec_code': p['code'], 'color': p['accent'], 'status': 'live', 'is_active': True,
            'school_id': None, 'settings': settings}).execute().data[0]['id']
        for i, (uslug, uname, usub, lessons) in enumerate(p['units']):
            uid = sb.table('units').insert({'subject_id': sid, 'slug': uslug, 'name': uname, 'subtitle': usub,
                'accent': p['accent'], 'accent_light': p['accent'] + '22', 'accent_badge': p['accent'] + '33',
                'body_class': f'unit-{slug}-{i+1}', 'sort_order': i, 'lesson_count': len(lessons)}).execute().data[0]['id']
            rows = [{'unit_id': uid, 'lesson_number': j + 1, 'slug': f'lesson-{j+1:02d}', 'title': t,
                     'description': d, 'status': 'pending_review', 'tier': 'both'} for j, (t, d) in enumerate(lessons)]
            sb.table('lessons').insert(rows).execute()
            print(f"   unit {uslug}: {len(rows)} lessons")
        print(f"   created subject {sid}")


if __name__ == '__main__':
    main()
