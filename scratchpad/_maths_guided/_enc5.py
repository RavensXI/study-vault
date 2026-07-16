import os, urllib.request
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
raw=urllib.request.urlopen(urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})).read()
patterns={"pound":b'\xc3\x82\xc2\xa3',"div":b'\xc3\x83\xc2\xb7',
 "times_D7":b'\xc3\x83\xc2\x97',"minus_2212":b'\xc3\xa2\xc2\x88\xc2\x92',
 "times_wrong":b'\xc3\x97'}
for n,p in patterns.items(): print(n, raw.count(p))
# Is there ANY clean single-encoded pound not part of double? count C2 A3 total vs double
print("total C2A3:", raw.count(b'\xc2\xa3'), "double C382C2A3:", raw.count(b'\xc3\x82\xc2\xa3'))
