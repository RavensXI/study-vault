# -*- coding: utf-8 -*-
"""Run the planning stage (Opus + plancheck) for every prepped board arm and
summarise lesson counts + planning spend. Configs prepped in the jobs tmp dir.

Usage: python scripts/api_build/run_arm_plans.py
"""
import io
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS_DIR = r'C:\Users\tshau\.claude\jobs\4059242c\tmp\arm_plans'

results = []
for slug in sorted(os.listdir(ARMS_DIR)):
    arm_dir = os.path.join(ARMS_DIR, slug)
    cfg_path = os.path.join(arm_dir, 'config.json')
    if not os.path.isfile(cfg_path):
        continue
    plan_path = os.path.join(arm_dir, 'plan.json')
    if os.path.exists(plan_path):
        print('== %s: plan exists, skipping generation' % slug, flush=True)
    else:
        print('== planning %s' % slug, flush=True)
        p = subprocess.run([sys.executable, os.path.join(HERE, 'driver.py'),
                            '--config', cfg_path, 'plan'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        tail = ((p.stdout or '') + (p.stderr or ''))[-500:]
        print(tail, flush=True)
        if p.returncode != 0 or not os.path.exists(plan_path):
            results.append({'slug': slug, 'error': 'plan failed: ' + tail[-200:]})
            continue
    c = subprocess.run([sys.executable, os.path.join(HERE, 'driver.py'),
                        '--config', cfg_path, 'plancheck'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    check = 'PASS' if 'PLANCHECK PASS' in (c.stdout or '') else 'FAIL'
    plan = json.load(io.open(plan_path, encoding='utf-8'))
    units = plan.get('article_units', [])
    n_lessons = sum(len(u.get('lessons', [])) for u in units)
    mix = {}
    for u in units:
        for l in u.get('lessons', []):
            s = (l.get('content_transfer') or {}).get('transfer_score', '?')
            mix[s] = mix.get(s, 0) + 1
    cost = 0.0
    ledger = os.path.join(arm_dir, 'costs.jsonl')
    if os.path.exists(ledger):
        for line in io.open(ledger, encoding='utf-8'):
            try:
                r = json.loads(line)
                cost += (r['input_tokens'] * 5 + r['cache_read'] * 0.5
                         + (r['cache_write_5m'] or 0) * 6.25 + (r['cache_write_1h'] or 0) * 10
                         + r['output_tokens'] * 25) / 1e6 + r.get('web_searches', 0) * 0.01
            except (ValueError, KeyError):
                pass
    results.append({'slug': slug, 'units': len(units), 'lessons': n_lessons,
                    'transfer_mix': mix, 'plancheck': check,
                    'gaps': plan.get('gaps') or [], 'plan_cost': round(cost, 2)})
    print('   -> %d units, %d lessons, mix %s, plancheck %s ($%.2f)'
          % (len(units), n_lessons, mix, check, cost), flush=True)

out = os.path.join(ARMS_DIR, '_summary.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(results, ensure_ascii=False, indent=1))
total_lessons = sum(r.get('lessons', 0) for r in results if 'lessons' in r)
total_cost = sum(r.get('plan_cost', 0) for r in results)
print('\nTOTAL: %d arms planned, %d lessons, planning spend ~$%.2f'
      % (len([r for r in results if 'lessons' in r]), total_lessons, total_cost))
print('summary: ' + out)
