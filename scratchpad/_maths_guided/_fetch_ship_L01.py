import os, json, urllib.request
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
sv=pd["problem_bank"]["silver"][0]
print("LIVE silver[0] display:", sv["display"])
print("LIVE silver[0] solutions:", sv["solutions"])
print("LIVE silver[0] expect:", sv["misconceptions"][0]["expect"])
