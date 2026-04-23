"""
One-off backfill: set subjects.settings.has_exam_guides = true for every
subject that currently has any exam-technique guide pages in Supabase.

Preserves "How do I answer this?" link behaviour for existing content after
the getGuideUrl flag check. New subjects default to false (no exam guides).
"""
import sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

sb = get_client()

# Find every subject with at least one exam-technique guide page
subjects_with_guides = set()
page = 0
while True:
    resp = sb.table('guide_pages').select('subject_id,guide_type').eq('guide_type', 'exam-technique').range(page*1000, (page+1)*1000 - 1).execute()
    if not resp.data:
        break
    for g in resp.data:
        if g.get('subject_id'):
            subjects_with_guides.add(g['subject_id'])
    if len(resp.data) < 1000:
        break
    page += 1

print(f"Found {len(subjects_with_guides)} subjects with exam-technique guide pages")

# Update each one's settings.has_exam_guides = true (merging into existing settings)
for sid in subjects_with_guides:
    subj = sb.table('subjects').select('slug,name,settings').eq('id', sid).single().execute().data
    settings = subj.get('settings') or {}
    if isinstance(settings, str):
        import json
        try:
            settings = json.loads(settings)
        except Exception:
            settings = {}
    if settings.get('has_exam_guides') is True:
        continue
    settings['has_exam_guides'] = True
    sb.table('subjects').update({'settings': settings}).eq('id', sid).execute()
    print(f"  flagged: {subj['slug']} ({subj['name']})")

print("Done.")
