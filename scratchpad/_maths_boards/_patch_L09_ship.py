import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
pd = json.load(open("lesson_maths-aqa_algebra-L09.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer "+key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# Verify round-trip
u2 = url + "&select=practice_data"
req2 = urllib.request.Request(u2, headers={"apikey":key,"Authorization":"Bearer "+key})
got = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("round-trip equal:", json.dumps(got,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False))
g0 = got["problem_bank"]["gold"][0]["display"]
print("gold0 non-ascii codepoints:", [hex(ord(c)) for c in g0 if ord(c)>127])

# changes file
changes = {
    "key": "maths-aqa_algebra-L09",
    "board": "maths-aqa",
    "lesson_id": ID,
    "problems_fixed": [],
    "issues_resolved": 0,
    "opener_concept": "Cafe bill: 2 teas + cake = £5, 1 tea + cake = £3, so a tea is £2 (elimination) and cake £1 (substitution), then named as x and y.",
    "notes": "Fresh-solved all 17 problems (8 bronze / 5 silver / 4 gold) from display; every stored solution correct. Recomputed every guided_steps box, all three teach walks, and the opener: all land exactly on stored solutions. Reproduced all 15 misconception expects by committing each error; all match. Completion boundaries valid (>=2 live boxes each). tier_guides within 115-word budget (76/40/61); method_card 78 words. related_videos, topic_links, worked_examples byte-equal to pre-dump. No em dashes. The 'cafe/pound' characters render correctly (U+00E9 / U+00A3); no corruption. Validator PASS."
}
json.dump(changes, open("changes_maths-aqa_algebra-L09.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

diagrams = {
    "key": "maths-aqa_algebra-L09",
    "figures_added": [],
    "opener_touched": False,
    "notes": "Linear simultaneous equations is a textual algebra unit; GCSE papers print no figure for solving a given pair of equations. The two word problems (cafe prices, sum-of-two-numbers) set up equations in prose with no printable diagram, and the opener is a money comparison shown as text (no figure claimed). Per the exam-realism test, no figures apply. figures_added = 0."
}
json.dump(diagrams, open("changes_maths-aqa_algebra-L09_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("changes files written.")
