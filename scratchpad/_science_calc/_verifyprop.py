import json, os, io, urllib.request, hashlib
KEY=os.environ['SUPABASE_SERVICE_KEY']
ids=[
 "9733399d-1134-4649-8166-74c5b738c4a3","c49b71fa-ab62-4285-81eb-9ad075aec3c6",
 "e9831803-7f3f-4d55-8185-0214e8c30fe0","56441c6c-8673-40d6-8926-e12ffab466b9",
 "74bcba45-696c-41bc-8621-7f287a6d72f9","c90d746e-bfa5-4660-8c6f-4b2b91c90933",
 "750f8228-0cc3-4ebd-a3c7-df4fa104448c",
]
hashes={}
for ID in ids:
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
    req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
    pd=json.load(urllib.request.urlopen(req))[0]['practice_data']
    s=json.dumps(pd, sort_keys=True, ensure_ascii=False)
    h=hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
    hashes[ID]=h
    # spot-check the two fixes
    pr=pd['topic_links']['prerequisites'][1]
    b=pd['problem_bank']['bronze'][3]['guided_steps'][1]['answer']
    print(ID[:8], h, '| prereq_ok=', pr=="Sampling with quadrats and transects (fieldwork practical)", '| box=', b)
print('unique hashes:', set(hashes.values()))
print('ALL IDENTICAL' if len(set(hashes.values()))==1 else 'MISMATCH!')
