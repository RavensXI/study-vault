import os, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="91158ba8-389c-4771-9735-326785654ccb"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
raw=urllib.request.urlopen(req).read()
print("content-type / len:", len(raw))
# find "Square it: 1000 " occurrence
idx=raw.find(b"Square it: 1000 ")
print("raw bytes around multiply sign:", raw[idx:idx+40])
# count utf-8 encodings
print("count b'\xc3\x97' (× utf8):", raw.count(b"\xc3\x97"))
print("count b'\xe2\x80\x94' (— utf8):", raw.count(b"\xe2\x80\x94"))
