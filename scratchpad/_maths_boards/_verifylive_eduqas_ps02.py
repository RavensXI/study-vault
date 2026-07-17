# -*- coding: utf-8 -*-
import os, json, io, urllib.request, shutil
LID = "7f417926-0bef-4875-a7ad-7eb71bd15506"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
GUIDED = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_maths-eduqas_probability-statistics-L02.json"
BOARDS = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
mine = json.load(io.open(GUIDED, encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
liverow = json.load(urllib.request.urlopen(req))[0]["practice_data"]
a = json.dumps(mine, sort_keys=True, ensure_ascii=False)
b = json.dumps(liverow, sort_keys=True, ensure_ascii=False)
print("LIVE MATCHES SHARD:", a == b)

# copy shard into boards dir under required name
shard_dst = os.path.join(BOARDS, "lesson_maths-eduqas_probability-statistics-L02.json")
shutil.copyfile(GUIDED, shard_dst)
print("shard ->", shard_dst)

# changes file
changes = {
    "key": "probability-statistics-L02",
    "board": "maths-eduqas",
    "problems_fixed": [
        {"tier": "silver", "index": 6, "what": "duplicate solution [5,9] with silver[0]; changed '50 girls do drama' to '60' so P(girl|drama)=2/3",
         "old": [5, 9], "new": [2, 3]},
        {"tier": "silver", "index": 2, "what": "replaced degenerate misconception (assume-independent 0.8x0.5=0.4 equalled the correct answer) with a determinate 'union minus P(A) only' slip",
         "old": "assumed_independent expect 0.35 (==0.4 coincidence)", "new": "subtracted_one_set expect 0.1"},
    ],
    "issues_resolved": 2,
    "misconceptions_enriched": "all 20 misconceptions gained a required, derived 'expect' value (bank had none); every expect verified != correct answer",
    "opener_concept": "8 friends in swim/cycle Venn loops; count swimmers (5), spot 3 also cycle, 3/5 = conditional P(cycle|swim) by common sense before any formula",
    "figures_added": "See changes_maths-eduqas_probability-statistics-L02_diagrams note: 11 bank Venn SVGs (count/conditional problems) + opener + 3 teach-walk figures, all programmatic from each problem's own region numbers",
    "notes": "All 20 problems fresh-solved from display; every stored answer already correct except the silver duplicate. Guided walks, tier_guides, opener, 3 teach walks added; method_card slimmed (em dash removed). topic_links/related_videos/worked_examples preserved byte-for-byte. Validator PASS; live row round-trips to shard.",
}
with io.open(os.path.join(BOARDS, "changes_maths-eduqas_probability-statistics-L02.json"), "w", encoding="utf-8") as f:
    json.dump(changes, f, ensure_ascii=False, indent=1)
print("changes written")
