# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY = os.environ['SUPABASE_SERVICE_KEY']
BASE = 'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons'
ALL_ROW_IDS = ['fee04afb-d041-4b63-8f67-73da3b882d74']
pd = json.load(io.open('lesson_higher-calculations-L02@a3108b4601.json', encoding='utf-8'))
body = json.dumps({'practice_data': pd}, ensure_ascii=False).encode('utf-8')

for rid in ALL_ROW_IDS:
    req = urllib.request.Request(BASE + '?id=eq.' + rid, data=body, method='PATCH',
        headers={'apikey': KEY, 'Authorization': 'Bearer ' + KEY,
                 'Content-Type': 'application/json', 'Prefer': 'return=minimal'})
    r = urllib.request.urlopen(req)
    print('PATCH', rid, r.status)

# verify each row now byte-identical to shard
target = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for rid in ALL_ROW_IDS:
    req = urllib.request.Request(BASE + '?id=eq.' + rid + '&select=practice_data',
        headers={'apikey': KEY, 'Authorization': 'Bearer ' + KEY})
    got = json.load(urllib.request.urlopen(req))[0]['practice_data']
    ok = json.dumps(got, sort_keys=True, ensure_ascii=False) == target
    print('VERIFY', rid, 'identical=' + str(ok))
    if not ok:
        raise SystemExit('MISMATCH on ' + rid)
print('ALL PATCHED + VERIFIED')
