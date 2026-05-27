#!/usr/bin/env python3
"""Re-slug Severn Vale's "Combined Science" subject `science` -> `science-severnvale`
to clear the cross-school slug clash with Unity's `science`.

WHY: both Unity ("Science") and Severn Vale ("Combined Science") used slug
`science` with DIFFERENT content, so their slug-keyed R2 audio
(science/{unit}/...mp3) collided — re-narrating Unity's lessons would clobber
SV's audio. Giving SV its own slug + its own audio namespace decouples them.
See memory/architecture_multi_school_slug_model.md.

WHAT (in safe order):
  1. Copy SV's audio objects science/{unit}/...  ->  science-severnvale/{unit}/...
     (server-side R2 copy — same bytes, so the tester hears no change)
  2. Rewrite SV's narration_manifest URLs to the new keys
  3. Flip the subject row slug science -> science-severnvale

SV biology units have no narration yet (nothing to copy there).
Dry-run by default; --apply to execute. Resolves SV by its fixed subject id
so it's safe to re-run even after the slug has flipped.
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, AUDIO_BUCKET, AUDIO_PUBLIC_URL

SV_SUBJECT_ID = '541d9f22-8853-48fa-bd05-6e812852ae9a'  # Severn Vale Combined Science
OLD_SLUG = 'science'
NEW_SLUG = 'science-severnvale'
OLD_PREFIX = OLD_SLUG + '/'
NEW_PREFIX = NEW_SLUG + '/'
BASE = AUDIO_PUBLIC_URL + '/'


def remap_key(key):
    """science/chemistry-paper-2/x.mp3 -> science-severnvale/chemistry-paper-2/x.mp3"""
    if key.startswith(OLD_PREFIX):
        return NEW_PREFIX + key[len(OLD_PREFIX):]
    return None  # not ours / already migrated — leave alone


def gather(sb):
    """-> (lessons_with_manifest, copy_jobs[(src_key,dst_key)], skipped[])"""
    units = sb.table('units').select('id,slug').eq('subject_id', SV_SUBJECT_ID).execute().data
    lessons, copies, skipped = [], [], []
    for u in units:
        L = sb.table('lessons').select('id,lesson_number,title,narration_manifest') \
            .eq('unit_id', u['id']).order('lesson_number').execute().data
        for l in L:
            man = l.get('narration_manifest') or []
            if not man:
                continue
            new_man = []
            for e in man:
                src = e.get('src', '')
                if not src.startswith(BASE):
                    skipped.append((l['id'], src)); new_man.append(e); continue
                key = src[len(BASE):]
                nk = remap_key(key)
                if nk is None:
                    skipped.append((l['id'], src)); new_man.append(e); continue
                copies.append((key, nk))
                new_man.append({'id': e['id'], 'src': BASE + nk, 'duration': e.get('duration')})
            lessons.append((l['id'], u['slug'], l['lesson_number'], l['title'], new_man))
    return lessons, copies, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    sb = get_client()

    subj = sb.table('subjects').select('id,name,slug,school_id').eq('id', SV_SUBJECT_ID).single().execute().data
    print(f"Subject: {subj['name']!r}  current slug={subj['slug']!r}  school_id={subj['school_id']}")
    if subj['slug'] == NEW_SLUG:
        print(f"  (slug already {NEW_SLUG} — audio copy/manifest steps still idempotent)")

    lessons, copies, skipped = gather(sb)
    print(f"\nLessons with narration: {len(lessons)}")
    print(f"Audio objects to copy: {len(copies)}  (science/ -> science-severnvale/)")
    if skipped:
        print(f"Skipped (non-matching src, left as-is): {len(skipped)}")
        for lid, s in skipped[:5]:
            print(f"   {lid[:8]} {s}")

    if not args.apply:
        # verify a sample of source objects exist
        r2 = get_r2_client()
        sample = copies[:3] + copies[-3:]
        print("\nSample source-object existence check:")
        for src, dst in sample:
            try:
                r2.head_object(Bucket=AUDIO_BUCKET, Key=src)
                print(f"   OK   {src}  ->  {dst}")
            except Exception as ex:
                print(f"   MISSING  {src}  ({ex.__class__.__name__})")
        print(f"\nDRY-RUN. Pass --apply to: copy {len(copies)} objects, rewrite "
              f"{len(lessons)} manifests, then flip slug {OLD_SLUG} -> {NEW_SLUG}.")
        return

    r2 = get_r2_client()
    # 1+2: copy objects, rewrite manifests
    copied = 0
    for lid, uslug, ln, title, new_man in lessons:
        for e in new_man:
            nk = e['src'][len(BASE):]
            if not nk.startswith(NEW_PREFIX):
                continue
            src = OLD_PREFIX + nk[len(NEW_PREFIX):]
            r2.copy_object(Bucket=AUDIO_BUCKET,
                           CopySource={'Bucket': AUDIO_BUCKET, 'Key': src},
                           Key=nk)  # plain copy preserves source audio/mpeg content-type
            copied += 1
        sb.table('lessons').update({'narration_manifest': new_man}).eq('id', lid).execute()
        print(f"  {uslug}/L{ln}: copied+repointed {len(new_man)} clips")
    print(f"\nCopied {copied} objects, rewrote {len(lessons)} manifests.")

    # 3: flip slug
    sb.table('subjects').update({'slug': NEW_SLUG}).eq('id', SV_SUBJECT_ID).execute()
    print(f"Subject slug flipped: {OLD_SLUG} -> {NEW_SLUG}")
    print("\nDONE. Note: students mid-session must re-login (bespoke_subjects is "
          "cached in sessionStorage and only refreshes at login).")


if __name__ == '__main__':
    main()
