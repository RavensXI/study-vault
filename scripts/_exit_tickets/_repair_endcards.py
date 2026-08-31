"""Backfill: strip the untrimmed Gemini Notebook endcard from shorts made
18-31 Aug 2026 (the fortnight the detector silently skipped).

Modes, in the order you should use them:

  --dry-run [N]    detect only. Downloads, measures, verifies a trim WOULD
                   pass every gate. Writes nothing anywhere. Safe to run.
  --canary N       trim N clips to ./_endcard_canary/ for eyeballing.
                   Writes nothing to R2. Safe to run.
  --apply [--limit N]
                   for each clip: copy the ORIGINAL to the R2 key
                   shorts_untrimmed/<same path> (rollback copy), then
                   overwrite the live key with the trimmed file.

Chaos control:
  * every clip passes trim_endcard_fixed's gates (dominant-spike, flat-card,
    duration band, tail-frame match, non-flat new ending) before any upload;
  * the original is backed up to R2 BEFORE the live key is touched, so any
    clip can be restored with a single copy;
  * a JSON state file makes runs idempotent and resumable — a clip already
    marked done is never processed twice;
  * --apply refuses to run between 00:30 and 03:30, when the nightly shorts
    build holds the pipeline;
  * R2 object PUT is atomic: a student mid-stream gets the old object or the
    new one, never a half-written file. The manifest carries no duration,
    so it needs no update and the feed keeps working throughout.
"""
import argparse
import datetime
import json
import os
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trim_endcard_fixed as TE  # noqa: E402

MANIFEST = 'https://www.studyvault.co.uk/data/_shorts_manifest.json'
BUCKET = 'studyvault-video'
BACKUP_PREFIX = 'shorts_untrimmed/'
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '_endcard_repair_state.json')
CANARY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_endcard_canary')
H = {'User-Agent': 'Mozilla/5.0 (StudyVault repair)'}
FIRST_BAD, LAST_BAD = '2026-08-18', '2026-08-31'


def load_state():
    try:
        return json.load(open(STATE, encoding='utf-8'))
    except Exception:
        return {}


def save_state(s):
    json.dump(s, open(STATE, 'w', encoding='utf-8'), indent=0)


def affected():
    d = json.loads(urllib.request.urlopen(
        urllib.request.Request(MANIFEST, headers=H), timeout=90).read())
    items = d if isinstance(d, list) else (d.get('items') or [])
    out = [i for i in items if i.get('created_at')
           and FIRST_BAD <= i['created_at'][:10] <= LAST_BAD]
    out.sort(key=lambda i: i['created_at'])
    return out


def key_of(url):
    return url.split('.r2.dev/', 1)[1]


def fetch(url, path):
    open(path, 'wb').write(urllib.request.urlopen(
        urllib.request.Request(url, headers=H), timeout=300).read())


def r2():
    import boto3
    return boto3.client(
        's3',
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
        region_name='auto')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canary', type=int, default=0)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    if not (a.dry_run or a.canary or a.apply):
        ap.error('choose --dry-run, --canary N or --apply')

    if a.apply:
        now = datetime.datetime.now().time()
        if datetime.time(0, 30) <= now <= datetime.time(3, 30):
            sys.exit('refusing to run during the nightly shorts build (00:30-03:30)')

    clips = affected()
    state = load_state()
    todo = [c for c in clips if state.get(c['url'], {}).get('status') != 'done']
    print(f'{len(clips)} clips in range {FIRST_BAD}..{LAST_BAD}; {len(todo)} not yet repaired')

    n = a.canary or a.limit or (10 if a.dry_run else len(todo))
    todo = todo[:n]
    if a.canary:
        os.makedirs(CANARY_DIR, exist_ok=True)
    cli = r2() if a.apply else None
    tmp = tempfile.mkdtemp()
    ok = fail = 0

    for idx, c in enumerate(todo, 1):
        src = os.path.join(tmp, 'in.mp4')
        dst = (os.path.join(CANARY_DIR, key_of(c['url']).replace('/', '__'))
               if a.canary else os.path.join(tmp, 'out.mp4'))
        label = f"{c['subject']}/{c['unit']}/L{c['lesson_number']}"
        try:
            fetch(c['url'], src)
        except Exception as e:
            print(f'{idx:4d} DOWNLOAD FAIL {label}: {str(e)[:60]}')
            fail += 1
            continue
        rep = TE.trim(src, dst)
        if not rep['ok']:
            print(f'{idx:4d} SKIP  {label}: {rep["why"][:70]}')
            state[c['url']] = {'status': 'skipped', 'why': rep['why']}
            fail += 1
            continue
        print(f'{idx:4d} OK    {label}: {rep["orig_dur"]}s -> {rep["new_dur"]}s '
              f'(card {rep["endcard"]}s, {rep["method"]}, tail std {rep.get("tail_std")})')
        ok += 1
        if a.apply:
            key = key_of(c['url'])
            try:
                cli.copy_object(Bucket=BUCKET, Key=BACKUP_PREFIX + key,
                                CopySource={'Bucket': BUCKET, 'Key': key})
                cli.upload_file(dst, BUCKET, key,
                                ExtraArgs={'ContentType': 'video/mp4'})
                state[c['url']] = {'status': 'done', 'old': rep['orig_dur'],
                                   'new': rep['new_dur'],
                                   'ts': datetime.datetime.now().isoformat(timespec='seconds')}
            except Exception as e:
                print(f'      UPLOAD FAIL: {str(e)[:80]}')
                state[c['url']] = {'status': 'upload_failed', 'why': str(e)[:120]}
                fail += 1
        if a.apply or a.canary:
            save_state(state)
        if os.path.exists(src):
            os.remove(src)

    print(f'\n{ok} passed every gate, {fail} skipped/failed')
    if a.canary:
        print('canary files in', CANARY_DIR)
    if a.dry_run:
        print('dry run — nothing written to R2')


if __name__ == '__main__':
    main()
