import os, json, re, urllib.request
from sympy import symbols, expand, sympify
x=symbols('x')
key=os.environ['SUPABASE_SERVICE_KEY']
url='https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.622f7959-f9e9-45aa-b2bd-8a5b6698e357&select=practice_data'
req=urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
data=json.load(urllib.request.urlopen(req))[0]['practice_data']

def pe(s):
    s=s.replace('\(','').replace('\)','').replace('−','-')
    s=s.replace('^2','**2').replace('^','**')
    s=re.sub(r'(\d)x',r'\1*x',s); s=s.replace(')(',')*(')
    s=re.sub(r'(\d)\(',r'\1*(',s); s=re.sub(r'x\(','x*(',s)
    return sympify(s)
def dp(d): return pe(re.search(r'Factorise\s*(.*)',d).group(1))

fails=[]
print("=== BANK ===")
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(data['problem_bank'][tier]):
        assert p['input_type']=='multiple_choice'
        t=expand(dp(p['display'])); sol=p['solutions']
        m=[j for j,o in enumerate(p['options']) if expand(pe(o))==t]
        status='OK' if m==sol else 'MISMATCH'
        if m!=sol: fails.append(f"{tier}[{i}] sol={sol} correct={m}")
        # misconception checks
        exps=[mc['expect'] for mc in p['misconceptions']]
        prob=[]
        if len(exps)!=len(set(exps)): prob.append('dupexpect')
        for e in exps:
            if e in sol: prob.append(f'expect{e}=correct')
            if not 0<=e<len(p['options']): prob.append(f'expect{e}oob')
        print(f"{tier}[{i}] {p['display']} {status} {'PROB:'+str(prob) if prob else ''}")
        if prob: fails.append(f"{tier}[{i}] {prob}")

print("\n=== TEACH WALKS ===")
def num(v): return v
for tier,walk in data['guided']['teach'].items():
    print(f"-- {tier}: {walk['display']}")
    for j,st in enumerate(walk['steps']):
        if 'answer' in st:
            print(f"   box[{j}] pre='{st['pre']}' ans={st['answer']}")

print("\n=== OPENER ===")
for j,st in enumerate(data['guided']['opener']['steps']):
    if 'answer' in st: print(f"   box[{j}] pre='{st.get('pre')}' ans={st['answer']}")

print("\n=== EM DASH (non-note) ===")
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            scan(v,path+'.'+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f'{path}[{j}]')
    elif isinstance(o,str):
        if '—' in o or '–' in o: print(f"  DASH {path}: {o[:50]}")
scan(data,'')

print("\nFAILS:", fails if fails else "NONE")
