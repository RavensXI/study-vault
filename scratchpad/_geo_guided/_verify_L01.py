# -*- coding: utf-8 -*-
"""Independent re-solve of every L01 problem from its chart config."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L01.json"), encoding="utf-8"))
pb = pd["problem_bank"]

def ds(p, i=0):
    return p["chart"]["data"]["datasets"][i]["data"]
def labs(p):
    return p["chart"]["data"]["labels"]

ok = []
def chk(tag, got, want):
    try: same = abs(float(got) - float(want)) < 1e-9
    except (TypeError, ValueError): same = (got == want)
    ok.append((tag, got, want, same))

b, s, g = pb["bronze"], pb["silver"], pb["gold"]

chk("b0 Oct rainfall", ds(b[0])[labs(b[0]).index("Oct")], b[0]["solutions"][0])
d = ds(b[1]); chk("b1 max month idx", b[1]["options"].index(["Oct","Nov","Dec","Jan"][[d[9],d[10],d[11],d[0]].index(max(d[9],d[10],d[11],d[0]))].replace("Oct","October").replace("Nov","November").replace("Dec","December").replace("Jan","January")), b[1]["solutions"][0])
chk("b1 global max is Nov", labs(b[1])[d.index(max(d))], "Nov")
chk("b2 Apr temp", ds(b[2])[3], b[2]["solutions"][0])
chk("b3 pop 2010", ds(b[3])[labs(b[3]).index("2010")], b[3]["solutions"][0])
d = ds(b[4]); chk("b4 range", max(d) - min(d), b[4]["solutions"][0])
d = ds(b[5]); chk("b5 Spain-Italy", d[1] - d[2], b[5]["solutions"][0])
d = ds(b[6]); chk("b6 peak hour", float(labs(b[6])[d.index(max(d))]), b[6]["solutions"][0])
d = ds(b[7]); chk("b7 lowest idx", d.index(min(d)), b[7]["solutions"][0])

lon, mos = ds(s[0], 0), ds(s[0], 1)
gaps = {"January": abs(lon[0]-mos[0]), "April": abs(lon[3]-mos[3]),
        "July": abs(lon[6]-mos[6]), "October": abs(lon[9]-mos[9])}
best = max(gaps, key=gaps.get)
chk("s0 widest gap", s[0]["options"].index(best), s[0]["solutions"][0])
print("   s0 gaps:", gaps)
d = ds(s[1]); chk("s1 pct increase", round((d[-1]-d[0])/d[0]*100), s[1]["solutions"][0])
chk("s2 total", sum(ds(s[2])), s[2]["solutions"][0])
man, lond = ds(s[3], 0), ds(s[3], 1)
chk("s3 diff of totals", sum(man) - sum(lond), s[3]["solutions"][0])
print("   s3 totals:", sum(man), sum(lond))
d = ds(s[4]); L = labs(s[4])
drops = {}
for a, bq in [(0,1),(1,2),(2,3),(4,5)]:
    drops["%s to %s" % (L[a], L[bq])] = d[a]-d[bq]
best = max(drops, key=drops.get)
chk("s4 biggest drop", s[4]["options"].index(best), s[4]["solutions"][0])
print("   s4 drops:", drops)
chk("s5 CountryB tertiary", ds(s[5], 2)[1], s[5]["solutions"][0])
chk("s5 B sums to 100", ds(s[5],0)[1]+ds(s[5],1)[1]+ds(s[5],2)[1], 100)
rain, disc = ds(s[6], 0), ds(s[6], 1)
lag = float(labs(s[6])[disc.index(max(disc))]) - float(labs(s[6])[rain.index(max(rain))])
chk("s6 lag", lag, s[6]["solutions"][0])

chk("g0 tertiary 2020", ds(g[0], 2)[2], g[0]["solutions"][0])
chk("g0 2020 sums 100", ds(g[0],0)[2]+ds(g[0],1)[2]+ds(g[0],2)[2], 100)
chk("g0 tertiary 2010", ds(g[0], 2)[1], 73)
ch = ds(g[1], 0); chk("g1 china increase", ch[-1]-ch[0], g[1]["solutions"][0])
ind = ds(g[1], 2); chk("g1 india increase (expect)", ind[-1]-ind[0], 1600)
d = ds(g[2]); chk("g2 dec/jul ratio", d[11]/d[6], 17)
chk("g2 summer min is Jul", labs(g[2])[d.index(min(d))], "Jul")
chk("g2 max is Dec", labs(g[2])[d.index(max(d))], "Dec")
d = ds(g[3]); chk("g3 rise", d[-1]-d[0], 34)
chk("g3 per decade rounded", round((d[-1]-d[0])/12.0), g[3]["solutions"][0])
chk("g3 divided by points", round((d[-1]-d[0])/7.0), 5)
br, dr = ds(g[4], 0), ds(g[4], 1)
chk("g4 death fall 60-80", dr[0]-dr[2], 13)
chk("g4 birth fall 60-80", br[0]-br[2], 5)
chk("g4 birth fall 80-2000", br[2]-br[4], 16)

# every guided_steps final numeric box lands on the stored solution (non-MC)
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        if p.get("input_type") == "multiple_choice":
            continue
        boxes = [st["answer"] for st in p["guided_steps"] if st.get("answer") is not None]
        assert p["solutions"][0] in boxes, "%s[%d]: solution not reached in walk" % (tier, i)

bad = [r for r in ok if not r[3]]
for t, gt, w, o in ok:
    print(("OK  " if o else "FAIL"), t, "got", gt, "want", w)
print("\n%d checks, %d failures" % (len(ok), len(bad)))
