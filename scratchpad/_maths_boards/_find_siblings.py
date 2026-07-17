# -*- coding: utf-8 -*-
import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
def q(url):
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(req))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?slug=eq.venn-diagrams-and-conditional-probability&select=id,subject_id"
rows = q(url)
out=[]
for r in rows:
    s = q("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/subjects?id=eq.%s&select=*" % r["subject_id"])
    sub = s[0]
    out.append({"lesson_id": r["id"], "subject_slug": sub.get("slug"), "subject_keys": [k for k in sub.keys()]})
print(json.dumps(out,ensure_ascii=False,indent=1))
