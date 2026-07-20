# -*- coding: utf-8 -*-
"""PATCH only practice_data on the single L13 row, then read it back."""
import io, json, os, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ROW = "55ede5fd-81e7-43de-95ed-d0b3bb681d06"
URL = ("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
       "?id=eq." + ROW + "&select=practice_data")

pd = json.load(io.open("lesson_L13.json", encoding="utf-8"))


def req(method, body=None, extra=None):
    h = {"apikey": KEY, "Authorization": "Bearer " + KEY,
         "Content-Type": "application/json"}
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(URL, data=data, headers=h, method=method)
    with urllib.request.urlopen(r) as resp:
        return resp.status, resp.read().decode("utf-8")


st, before = req("GET")
print("GET before:", st, "len", len(before), "| empty?", json.loads(before)[0]["practice_data"])

st, _ = req("PATCH", {"practice_data": pd}, {"Prefer": "return=minimal"})
print("PATCH:", st)

st, after = req("GET")
live = json.loads(after)[0]["practice_data"]
print("GET after:", st)
print("identical to file:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
print("tiers:", {t: len(live["problem_bank"][t]) for t in ("bronze", "silver", "gold")})
print("keys:", sorted(live.keys()))
