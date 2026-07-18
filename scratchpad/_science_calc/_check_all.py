import os, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    req=urllib.request.Request(f"{BASE}?id=eq.{rid}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.loads(urllib.request.urlopen(req).read())[0]['practice_data']
ids=["9733399d-1134-4649-8166-74c5b738c4a3","c49b71fa-ab62-4285-81eb-9ad075aec3c6","e9831803-7f3f-4d55-8185-0214e8c30fe0","56441c6c-8673-40d6-8926-e12ffab466b9","74bcba45-696c-41bc-8621-7f287a6d72f9","c90d746e-bfa5-4660-8c6f-4b2b91c90933","750f8228-0cc3-4ebd-a3c7-df4fa104448c"]
canon=json.dumps(get(ids[0]),sort_keys=True,ensure_ascii=False)
for rid in ids:
    d=json.dumps(get(rid),sort_keys=True,ensure_ascii=False)
    print(rid[:8], "identical" if d==canon else "*** DIFFERS ***")
