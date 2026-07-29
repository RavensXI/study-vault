"""
Hero Image Index — search and reuse existing hero images by keywords.

Usage:
    from lib.hero_index import search_heroes, add_to_index
    results = search_heroes("medieval medicine plague")
    # Returns list of {title, subject, unit, hero_url, score} sorted by relevance

    add_to_index("Lesson Title", "description", "subject-slug", "unit-slug", "lesson-slug", "https://r2.dev/...")
    # Adds a new entry with auto-generated tags and saves to disk
"""

import json
import os

_INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'hero-image-index.json')
_cache = None

_STOP_WORDS = frozenset([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
    'with', 'by', 'from', 'is', 'it', 'its', 'as', 'be', 'was', 'are', 'were',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'this', 'that', 'these',
    'those', 'how', 'what', 'which', 'who', 'whom', 'when', 'where', 'why',
    'your', 'our', 'their', 'my', 'his', 'her', 'we', 'you', 'they', 'us',
    'them', 'he', 'she', 'lesson', 'lessons', 'unit', 'part', 'paper', 'using',
    'used', 'between', 'through', 'into', 'over', 'after', 'before', 'during',
    'about', 'each', 'other', 'than', 'then', 'some', 'such', 'only', 'also',
    'just', 'more', 'most', 'very', 'well', 'back', 'much', 'many', 'own',
    'way', 'long', 'make', 'like', 'new', 'first', 'come', 'know', 'take',
    'get', 'made', 'find', 'here', 'thing', 'world', 'still', 'need', 'too',
    'any', 'right', 'not', 'now', 'old',
])


def _load():
    global _cache
    if _cache is None:
        with open(_INDEX_PATH, 'r', encoding='utf-8') as f:
            _cache = json.load(f)
    return _cache


def _save():
    global _cache
    if _cache is not None:
        with open(_INDEX_PATH, 'w', encoding='utf-8') as f:
            json.dump(_cache, f, indent=2, ensure_ascii=False)


def _generate_tags(title, description='', unit_name='', subject_name=''):
    """Generate keyword tags from text fields."""
    import re
    text = f"{title} {description} {unit_name} {subject_name}".lower()
    words = re.sub(r'[^a-z0-9\s-]', ' ', text).split()
    return list(set(w for w in words if len(w) > 2 and w not in _STOP_WORDS))


def search_heroes(query, limit=10, exclude_subjects=None, min_score=2):
    """Search hero images by keyword query. Returns top matches sorted by relevance score.

    DEPRECATED for hero SELECTION (July 2026): keyword scores assigned
    other subjects' heroes sight-unseen to psychology lessons. Use
    lib/hero_pipeline.py::HeroFinder, which vision-checks every candidate.
    This function remains for lookups/reporting only.
    """
    import warnings
    warnings.warn("search_heroes() must not choose hero images — "
                  "use lib.hero_pipeline.HeroFinder (see docs/PIPELINE.md Phase 4)",
                  stacklevel=2)
    index = _load()
    query_words = set(query.lower().split())

    results = []
    for entry in index:
        if exclude_subjects and entry['subject'] in exclude_subjects:
            continue

        tags = set(entry.get('tags', []))
        title_words = set(entry['title'].lower().split())

        # Score: title matches worth 3x, tag matches worth 1x
        title_hits = len(query_words & title_words)
        tag_hits = len(query_words & tags)
        score = (title_hits * 3) + tag_hits

        if score >= min_score:
            results.append({
                'title': entry['title'],
                'subject': entry['subject'],
                'unit': entry['unit'],
                'hero_url': entry['hero_url'],
                'score': score
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]


def get_heroes_for_subject(subject_slug):
    """Get all hero images for a specific subject."""
    index = _load()
    return [e for e in index if e['subject'] == subject_slug]


def add_to_index(title, description, subject_slug, subject_name,
                 unit_slug, unit_name, lesson_slug, hero_url):
    """Add a new hero image to the index with auto-generated tags. Saves to disk."""
    index = _load()

    # Check for duplicate URL
    existing_urls = {e['hero_url'] for e in index}
    if hero_url in existing_urls:
        return  # Already indexed

    entry = {
        'title': title,
        'description': description or '',
        'subject': subject_slug,
        'subject_name': subject_name,
        'unit': unit_slug,
        'unit_name': unit_name,
        'lesson_slug': lesson_slug,
        'hero_url': hero_url,
        'tags': _generate_tags(title, description, unit_name, subject_name),
    }

    index.append(entry)
    _save()


if __name__ == '__main__':
    import sys
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'medieval medicine'
    print(f'Searching for: "{query}"')
    for r in search_heroes(query):
        print(f"  [{r['score']}] {r['title']} ({r['subject']}/{r['unit']}) -> {r['hero_url'][:80]}...")
