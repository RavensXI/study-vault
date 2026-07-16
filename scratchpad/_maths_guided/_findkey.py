import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
wl=json.load(open('_maths_guided/_worklist.json',encoding='utf-8'))
# find entry with this id
def walk(o,path=''):
    if isinstance(o,dict):
        if o.get('id')==ID or o.get('lesson_id')==ID:
            print("WL entry:",json.dumps(o,ensure_ascii=False)[:400])
        for k,v in o.items(): walk(v,path+'/'+k)
    elif isinstance(o,list):
        for x in o: walk(x)
walk(wl)
a=json.load(open('_maths_audit/_audit_result.json',encoding='utf-8'))
# find all keys containing 'ratio'
for k in ['issues','unconfirmed']:
    print("="*8,k)
    for e in a[k]:
        if 'ratio' in e.get('key','').lower():
            print(json.dumps(e,ensure_ascii=False))
