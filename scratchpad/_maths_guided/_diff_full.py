# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
ship=json.load(open('lesson_probability-statistics-L04.json',encoding='utf-8'))
ship = ship.get('practice_data', ship) if isinstance(ship,dict) and 'practice_data' in ship else ship
live=json.load(open('_live_pd.json',encoding='utf-8'))

def norm(o): return json.dumps(o, sort_keys=True, ensure_ascii=False)

allkeys=set(ship)|set(live)
for k in sorted(allkeys):
    same = norm(ship.get(k))==norm(live.get(k))
    print(f'{"SAME " if same else "DIFF "} {k}')
