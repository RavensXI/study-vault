# -*- coding: utf-8 -*-
import io, json, os, sys, urllib.request

ROW = "aae0e652-fbec-4f5d-b06a-abfea8eeb630"
URL = ("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
       "?id=eq." + ROW + "&select=practice_data")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY,
     "Content-Type": "application/json"}

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L14.json"), encoding="utf-8"))


def req(method, url, body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r) as resp:
        return resp.status, resp.read().decode("utf-8")


st, body = req("GET", URL)
before = json.loads(body)[0]["practice_data"]
print("BEFORE keys:", sorted((before or {}).keys()) or "(empty)")

st, body = req("PATCH", URL, {"practice_data": pd}, {"Prefer": "return=minimal"})
print("PATCH status", st)

st, body = req("GET", URL)
after = json.loads(body)[0]["practice_data"]
pb = after["problem_bank"]
print("AFTER keys:", sorted(after.keys()))
print("tiers:", len(pb["bronze"]), len(pb["silver"]), len(pb["gold"]))
print("identical to file:", json.dumps(after, sort_keys=True) == json.dumps(pd, sort_keys=True))
