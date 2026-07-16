import os, urllib.request
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
raw=urllib.request.urlopen(req).read()
# clean £ = C2 A3 ; double-encoded Â£ = C3 82 C2 A3
print("total bytes:", len(raw))
print("occurrences of double-encoded £ (C3 82 C2 A3):", raw.count(b'\xc3\x82\xc2\xa3'))
print("occurrences of double-encoded ÷ (C3 83 C2 B7):", raw.count(b'\xc3\x83\xc2\xb7'))
print("occurrences of double-encoded × (C3 83 C2 97):", raw.count(b'\xc3\x83\xc2\x97'))
print("occurrences of double-encoded − minus (C3 A2 C2 88 C2 92):", raw.count(b'\xc3\xa2\xc2\x88\xc2\x92'))
# clean single-encoded £ would be C2 A3 NOT preceded by C3 82
