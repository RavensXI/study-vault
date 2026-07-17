import os, json, urllib.request

ID = "0a7ff82d-058f-480c-86fe-63a16ac98dc5"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open('lesson_maths-ocr_algebra-L06.json', encoding='utf-8'))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode('utf-8')
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method='PATCH', headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
url2 = url + "&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": key, "Authorization": f"Bearer {key}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]['practice_data']
print("live has guided:", 'guided' in live, "| tier_guides:", 'tier_guides' in live,
      "| bronze_desc set:", bool(live['problem_bank'].get('bronze_description')))
print("round-trip equal:", json.dumps(live, sort_keys=True, ensure_ascii=False)==json.dumps(pd, sort_keys=True, ensure_ascii=False))
