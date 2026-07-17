import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open('_live_L04.json', encoding='utf-8'))[0]['problem_bank'] if False else json.load(open('_live_L04.json', encoding='utf-8'))[0]['practice_data']['problem_bank']

def coords(opt):
    # extract a coordinate pair (a,b) from an option like '(6, 2)' or vector binom{3}{-3}
    o = opt.replace('−', '-')
    mb = re.search(r'binom\{(-?\d+)\}\{(-?\d+)\}', o)
    if mb:
        return (int(mb.group(1)), int(mb.group(2)))
    m = re.search(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', o)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None

# expected correct answers computed independently
expected = {
 ('bronze',0):(6,2),('bronze',1):(5,-1),('bronze',2):(3,4),('bronze',3):(3,-3),
 ('bronze',4):(3,4),('bronze',5):(6,0),('bronze',6):(6,3),('bronze',7):(-3,-2),
 ('silver',0):(1,4),('silver',1):(-2,-4),('silver',3):(4,3),('silver',4):(-5,2),('silver',5):(5,2),
 ('gold',0):(-1,-1),('gold',1):(3,4),('gold',4):(-5,-1),
}
# describe/composite problems verified by index only
describe = {('silver',2):0,('silver',6):0,('gold',2):0,('gold',3):0}

fails=[]
for t in ['bronze','silver','gold']:
    for i,p in enumerate(d[t]):
        sol=p['solutions'][0]
        opts=p['options']
        key=(t,i)
        if key in expected:
            exp=expected[key]
            got=coords(opts[sol])
            ok = got==exp
            # uniqueness: no other option equals exp
            others=[coords(o) for j,o in enumerate(opts) if j!=sol]
            uniq = exp not in others
            if not ok: fails.append(f'{t}[{i}] WRONG: expected {exp} got option[{sol}]={opts[sol]}={got}')
            if not uniq: fails.append(f'{t}[{i}] NON-UNIQUE: {exp} also in another option {opts}')
            print(f'{t}[{i}] sol_idx={sol} opt={opts[sol]!r} computed={exp} match={ok} unique={uniq}')
        elif key in describe:
            print(f'{t}[{i}] DESCRIBE sol_idx={sol} (expected {describe[key]}) opts={opts}')
            if sol!=describe[key]: fails.append(f'{t}[{i}] describe sol idx {sol}!={describe[key]}')
        # expect check
        for mc in p.get('misconceptions',[]):
            ex=mc.get('expect')
            if ex is not None and (ex<0 or ex>=len(opts)):
                fails.append(f'{t}[{i}] expect {ex} out of range')
            if ex==sol:
                fails.append(f'{t}[{i}] expect equals correct index {sol}!')
print('\nFAILS:',len(fails))
for f in fails: print('  ',f)
