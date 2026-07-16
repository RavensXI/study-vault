import os, json, urllib.request, time
ID="a43f9613-dd40-45e2-b692-00ac9c01fb92"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=title,practice_data"
seen=set()
for i in range(6):
    req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
    data=json.load(urllib.request.urlopen(req))
    pd=data[0]["practice_data"]
    b0=pd["problem_bank"]["bronze"][0]["display"][:40]
    seen.add(b0)
    print(f"GET {i}: {b0}")
    time.sleep(3)
print("distinct bronze[0] seen:", len(seen))
