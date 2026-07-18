import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["1563a319-bb93-438e-9b64-e079bd7e410a","ea8d64f3-4cf2-4568-afe6-d4d41d065f55"]
datas=[]
for i in ids:
    url = BASE + "?id=eq.%s&select=practice_data" % i
    req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    d = json.loads(urllib.request.urlopen(req).read())[0]["practice_data"]
    datas.append(json.dumps(d, sort_keys=True, ensure_ascii=False))
print("live rows byte-identical:", datas[0]==datas[1])
# dump canonical live for validator
json.dump(json.loads(datas[0]), io.open("_live_after_ocrb.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
# has guided?
d=json.loads(datas[0])
print("has guided:", "guided" in d, "has tier_guides:", "tier_guides" in d)
print("gold[0] guided_steps count:", len(d["problem_bank"]["gold"][0]["guided_steps"]))
