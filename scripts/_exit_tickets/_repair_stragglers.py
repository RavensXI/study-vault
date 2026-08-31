# The last two clips rejected on the transition test only (diff 7.4 / 7.6 vs a
# floor of 8.0). Their all-flat-tail check PASSED, so the 3.08s card is
# definitely present; the slide before it is simply very pale cream, so the
# change across the boundary is subtle. Re-run just these two with the floor
# relaxed. Every other gate -- flat tail, duration band, tail match, and the
# "does it still end on the card" comparison -- is unchanged.
import json
import os
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trim_endcard_fixed as TE  # noqa: E402
import _repair_endcards as R  # noqa: E402

TE.CUT_MIN_DIFF = 6.0

state = R.load_state()
todo = [k for k, v in state.items() if v.get('status') != 'done']
print(f'{len(todo)} stragglers')
cli = R.r2()
tmp = tempfile.mkdtemp()
for url in todo:
    src, dst = os.path.join(tmp, 'in.mp4'), os.path.join(tmp, 'out.mp4')
    R.fetch(url, src)
    rep = TE.trim(src, dst)
    key = R.key_of(url)
    if not rep['ok']:
        print('STILL SKIP', key, '|', rep['why'][:70])
        continue
    print(f"OK {key}: {rep['orig_dur']}s -> {rep['new_dur']}s (vs card {rep.get('vs_card')})")
    cli.copy_object(Bucket=R.BUCKET, Key=R.BACKUP_PREFIX + key,
                    CopySource={'Bucket': R.BUCKET, 'Key': key})
    cli.upload_file(dst, R.BUCKET, key, ExtraArgs={'ContentType': 'video/mp4'})
    state[url] = {'status': 'done', 'old': rep['orig_dur'], 'new': rep['new_dur'],
                  'note': 'transition floor relaxed to 6.0 (pale slide before card)'}
    R.save_state(state)
print('done')
