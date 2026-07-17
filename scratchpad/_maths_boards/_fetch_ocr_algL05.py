import os, json, urllib.request
ID="320a6b1d-a96c-400f-8807-5828376373ea"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(d, open("_live_ocr_algL05.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("top keys:", list(d.keys()))
pb=d.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(f"\n=== {t} ({len(arr)}) ===")
    for i,p in enumerate(arr):
        print(f"[{i}] disp={p.get('display')!r} sol={p.get('solutions')} it={p.get('input_type')} calc={p.get('calculator')}")
