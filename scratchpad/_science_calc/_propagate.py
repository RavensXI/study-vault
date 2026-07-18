import json, os, io, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
pd=json.load(io.open('lesson_biology-data-skills-L03@40fdb75726.json',encoding='utf-8'))
ids=[
 "9733399d-1134-4649-8166-74c5b738c4a3",
 "c49b71fa-ab62-4285-81eb-9ad075aec3c6",
 "e9831803-7f3f-4d55-8185-0214e8c30fe0",
 "56441c6c-8673-40d6-8926-e12ffab466b9",
 "74bcba45-696c-41bc-8621-7f287a6d72f9",
 "c90d746e-bfa5-4660-8c6f-4b2b91c90933",
 "750f8228-0cc3-4ebd-a3c7-df4fa104448c",
]
body=json.dumps({'practice_data':pd}, ensure_ascii=False).encode('utf-8')
for ID in ids:
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
    req=urllib.request.Request(url, data=body, method='PATCH', headers={
        'apikey':KEY,'Authorization':f'Bearer {KEY}',
        'Content-Type':'application/json','Prefer':'return=minimal'})
    r=urllib.request.urlopen(req)
    print(ID, r.status)
print('patched', len(ids), 'rows')
