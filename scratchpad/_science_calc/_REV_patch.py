# -*- coding: utf-8 -*-
import os, json, urllib.request, hashlib
KEY = os.environ['SUPABASE_SERVICE_KEY']
BASE = 'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons'
IDS = ['a28c155d-46f2-49af-9cc4-27d907de0ae2']  # all_row_ids (single canonical row)

pd = json.load(open('lesson_higher-calculations-L05@c023b518a1.json', encoding='utf-8'))
body = json.dumps({'practice_data': pd}).encode('utf-8')

def h(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

canon = h(pd)
for ID in IDS:
    req = urllib.request.Request('%s?id=eq.%s' % (BASE, ID), data=body, method='PATCH',
        headers={'apikey': KEY, 'Authorization': 'Bearer ' + KEY,
                 'Content-Type': 'application/json', 'Prefer': 'return=minimal'})
    r = urllib.request.urlopen(req)
    print('PATCH', ID, r.status)

for ID in IDS:
    req = urllib.request.Request('%s?id=eq.%s&select=practice_data' % (BASE, ID),
        headers={'apikey': KEY, 'Authorization': 'Bearer ' + KEY})
    got = json.load(urllib.request.urlopen(req))[0]['practice_data']
    print('BYTE-IDENTICAL', ID, h(got) == canon)
    print('  half-lifes:', json.dumps(got, ensure_ascii=False).count('half-lifes'),
          '| ((arbitrary:', json.dumps(got, ensure_ascii=False).count('((arbitrary'),
          '| gold[4] x-title:', got['problem_bank']['gold'][4]['chart']['options']['scales']['x']['title']['text'],
          '| gold[4] span:', got['problem_bank']['gold'][4]['chart']['data']['labels'][-1])
