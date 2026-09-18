"""Pair each free-tier lesson with the school lesson on the same topic, for the progress
carry-over in js/school-session.js (svCarrySchoolProgress). Title similarity on unit name +
lesson title; an equal unit slug and lesson number counts as a match at a lower bar.
  python scripts/build_school_lesson_map.py   -> data/school-lesson-map.json"""
import os, io, json, re, difflib, requests
H = {'apikey': os.environ['SUPABASE_SERVICE_KEY'], 'Authorization': 'Bearer ' + os.environ['SUPABASE_SERVICE_KEY']}
U = os.environ['SUPABASE_URL']
SCHOOLS = {'unity-college': {'id': 'a5414d1c-8841-4bc5-8573-a9756752361b', 'pairs': {
    'history-aqa': 'history', 'geography-aqa': 'geography', 'science-aqa': 'science', 'separate-sciences': 'separate-sciences',
    'english-literature-aqa': 'english-literature', 'english-language-aqa': 'english-language', 'religious-studies-aqa': 'religious-studies',
    'business-edexcel': 'business', 'computer-science': 'computer-science', 'design-technology': 'design-technology',
    'music-eduqas': 'gcse-music', 'food-preparation-and-nutrition-aqa': 'food-preparation-and-nutrition',
    'french-aqa': 'french', 'spanish-aqa': 'spanish', 'german-aqa': 'german'}}}
def norm(t): return re.sub(r'[^a-z0-9 ]', ' ', (t or '').lower()).replace(' and ', ' ').replace(' the ', ' ')
GENERIC = {'beliefs','belief','practices','practice','teachings','teaching','theme','paper','unit','study','studies','component','gcse'}
def uname(t): return ' '.join(w for w in norm(t).split() if w not in GENERIC)   # 'judaism beliefs' -> 'judaism', so religions never pair by their shared suffix
def lessons(slug, school):
    subs = requests.get(U + '/rest/v1/subjects?slug=eq.%s&school_id=%s&select=id' % (slug, ('eq.' + school) if school else 'is.null'), headers=H).json()
    if not subs: return {}
    out = {}
    for u in requests.get(U + '/rest/v1/units?subject_id=eq.%s&select=id,slug,name' % subs[0]['id'], headers=H).json():
        for l in requests.get(U + '/rest/v1/lessons?unit_id=eq.%s&status=eq.live&select=lesson_number,title' % u['id'], headers=H).json():
            out[(u['slug'], l['lesson_number'])] = (u['name'], l['title'])
    return out
result = {}
for sslug, cfg in SCHOOLS.items():
    result[sslug] = {}
    for free, bes in cfg['pairs'].items():
        F = lessons(free, None); B = lessons(bes, cfg['id'])
        if not F or not B: print('skip', free, '->', bes, len(F), len(B)); continue
        lmap = {}; umap = {}
        # stage 1: pair units by how well their lesson titles line up (mean of best ratios)
        fu_all = sorted({k[0] for k in F}); bu_all = sorted({k[0] for k in B})
        def titles(D, u): return [norm(v[1]) for k, v in D.items() if k[0] == u]
        for fu in fu_all:
            ft = titles(F, fu); best = None
            fname = norm(next(v[0] for k, v in F.items() if k[0] == fu))
            for bu in bu_all:
                bt = titles(B, bu); bname = norm(next(v[0] for k, v in B.items() if k[0] == bu))
                lesson_score = sum(max(difflib.SequenceMatcher(None, a, b).ratio() for b in bt) for a in ft) / len(ft)
                name_score = max(difflib.SequenceMatcher(None, uname(fname), uname(bname)).ratio(), difflib.SequenceMatcher(None, uname(fu.replace('-', ' ')), uname(bu.replace('-', ' '))).ratio())
                score = 0.5 * lesson_score + 0.5 * name_score
                if name_score < 0.45: continue       # a different unit, however similar its lesson titles
                if best is None or score > best[0]: best = (score, bu)
            # a unit is the same unit only when its name AND its lessons both line up
            if best and best[0] >= 0.62: umap[fu] = best[1]
        # stage 2: within paired units, pair lessons by title; fall back to the same number when the counts match
        for (fu, fn), (fun, ft) in F.items():
            bu = umap.get(fu)
            if not bu: continue
            cands = [(bn, B[(bu, bn)][1]) for (u2, bn) in B if u2 == bu]
            best = max(((difflib.SequenceMatcher(None, norm(ft), norm(bt)).ratio(), bn) for bn, bt in cands), default=None)
            if best and best[0] >= 0.55: lmap['%s/%d' % (fu, fn)] = '%s/%d' % (bu, best[1])
            elif len(cands) == len([1 for k in F if k[0] == fu]) and any(bn == fn for bn, _ in cands) and best and best[0] >= 0.35:
                lmap['%s/%d' % (fu, fn)] = '%s/%d' % (bu, fn)
        result[sslug][free] = {'to': bes, 'lessons': lmap, 'units': umap}
        print('%-36s -> %-30s %3d of %3d free lessons paired (%d school lessons)' % (free, bes, len(lmap), len(F), len(B)))
os.makedirs('data', exist_ok=True)
io.open('data/school-lesson-map.json', 'w', encoding='utf-8').write(json.dumps(result, ensure_ascii=False, indent=1))
print('written data/school-lesson-map.json')
