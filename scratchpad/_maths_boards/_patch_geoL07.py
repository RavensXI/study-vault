import os, json, urllib.request
ID="6e789a76-e66f-4ed3-9031-599c6406ca45"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_geometry-L07.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode()
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify roundtrip
url2=f"{url}&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("keys:",list(back.keys()))
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back)
print("gold[3] sol:", back["problem_bank"]["gold"][3]["solutions"], "| display:", back["problem_bank"]["gold"][3]["display"].split("</svg>")[-1].strip()[:60])
