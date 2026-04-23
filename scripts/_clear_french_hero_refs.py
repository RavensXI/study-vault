"""
Clear hero_image_url / hero_image_alt / hero_image_caption / hero_image_position
from free-tier French lesson rows. Practice pages don't render heroes so these
fields are invisible dead data on the lessons themselves.

DOES NOT touch:
- R2 assets (still referenced by the hero image index)
- data/hero-image-index.json (entries stay, so other subjects can reuse these
  images via index search — avoids fresh Unsplash calls when German, Spanish,
  or any new subject hits a matching query)
- units.image_url (unit card art — leave as-is, might be used on browse landing)
"""
import sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

sb = get_client()

subj = sb.table('subjects').select('id').eq('slug', 'french-aqa').is_('school_id', 'null').single().execute().data
units = sb.table('units').select('id,slug').eq('subject_id', subj['id']).execute().data
uids = [u['id'] for u in units]

lessons = sb.table('lessons').select('id,title,hero_image_url').in_('unit_id', uids).execute().data
with_hero = [l for l in lessons if l.get('hero_image_url')]
print(f"Found {len(with_hero)} French lessons with hero_image_url set. Clearing...")

for l in with_hero:
    sb.table('lessons').update({
        'hero_image_url': None,
        'hero_image_alt': None,
        'hero_image_caption': None,
        'hero_image_position': None,
    }).eq('id', l['id']).execute()
    print(f"  cleared: {l['title']}")

print(f"\nDone. {len(with_hero)} lesson rows cleared.")
print("R2 assets + index entries left intact for cross-subject reuse.")
