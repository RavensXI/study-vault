import json,io
pd=json.load(io.open('_live_canonical.json',encoding='utf-8'))
out=io.open('_tg.txt','w',encoding='utf-8')
tg=pd['tier_guides']
for t in ['bronze','silver','gold']:
    g=tg[t]
    out.write(f'\n=== {t}: {g.get("title")}\n')
    for s in g.get('steps',[]): out.write('  STEP: '+s+'\n')
    ex=g.get('example',{})
    out.write('  EX Q: '+str(ex.get('question'))+'\n')
    for st in ex.get('steps',[]):
        out.write(f'    - {st.get("label")}: {st.get("content")} [ans={st.get("isAnswer") or st.get("is_answer")}]\n')
mc=pd['method_card']
out.write('\n=== method_card ===\n'+mc.get('title','')+'\n'+mc.get('content','')+'\n')
out.write('word count content approx: '+str(len(mc.get('content','').split()))+'\n')
out.close()
print('done')
