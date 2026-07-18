import os,urllib.request,json
key=os.environ['SUPABASE_SERVICE_KEY']
url='https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.c36f2b4d-aeaa-4c83-a6b2-9a5da3abb976&select=practice_data,title'
req=urllib.request.Request(url,headers={'apikey':key,'Authorization':'Bearer '+key})
d=json.load(urllib.request.urlopen(req))[0]
live=d['practice_data']
json.dump(live,open('_live_pd.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
e=[x for x in pre if x['id']=='c36f2b4d-aeaa-4c83-a6b2-9a5da3abb976'][0]
p=e['pd']
print('LIVE keys:',sorted(live.keys()))
print('PRE keys :',sorted(p.keys()))
print('related_videos preserved:',p.get('related_videos')==live.get('related_videos'), '| pre=',p.get('related_videos'),'live=',live.get('related_videos'))
print('topic_links preserved:',p.get('topic_links')==live.get('topic_links'),'| pre=',p.get('topic_links'),'live=',live.get('topic_links'))
pw=[w.get('question') for w in p.get('worked_examples',[])]
lw=[w.get('question') for w in live.get('worked_examples',[])]
print('worked_examples questions preserved:',pw==lw,'(n_pre %d n_live %d)'%(len(pw),len(lw)))
print()
for tier in ['bronze','silver','gold']:
    pp=p['problem_bank'][tier]; ll=live['problem_bank'][tier]
    print('%s pre_n=%d live_n=%d'%(tier,len(pp),len(ll)))
    for i in range(max(len(pp),len(ll))):
        ps=pp[i].get('solutions') if i<len(pp) else None
        ls=ll[i].get('solutions') if i<len(ll) else None
        pdisp=pp[i].get('display','')[:45] if i<len(pp) else '--'
        ldisp=ll[i].get('display','')[:45] if i<len(ll) else '--'
        if ps!=ls: print('   sol drift %s[%d]: %s -> %s'%(tier,i,ps,ls))
        if pdisp!=ldisp: print('   display drift %s[%d]:\n     PRE: %s\n     LIVE:%s'%(tier,i,pdisp,ldisp))
