import os, json, urllib.request, hashlib
k=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?slug=eq.contours-and-relief&select=id,title,practice_data,unit_id"
r=urllib.request.Request(url, headers={"apikey":k,"Authorization":"Bearer "+k})
d=json.load(urllib.request.urlopen(r))
for row in d:
    pdj=json.dumps(row["practice_data"], sort_keys=True, ensure_ascii=False)
    print(row["id"], hashlib.md5(pdj.encode()).hexdigest()[:10], len(pdj))
