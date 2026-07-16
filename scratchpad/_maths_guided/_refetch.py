import os, json, urllib.request, time
ID="a43f9613-dd40-45e2-b692-00ac9c01fb92"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=title,lesson_number,practice_data"
for i in range(3):
    req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
    data=json.load(urllib.request.urlopen(req))
    pd=data[0]["practice_data"]
    # topic sniff
    disp=pd["problem_bank"]["bronze"][0]["display"][:60]
    print(f"fetch {i}: title={data[0]['title']!r} num={data[0]['lesson_number']} | bronze[0]: {disp}")
    if i==2:
        json.dump(pd,open("_live_L04.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
    time.sleep(2)
