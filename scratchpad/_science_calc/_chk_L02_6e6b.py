import json, os, io, urllib.request
ID="33f0478e-34e4-42ed-b1d1-06aa232a5a65"
key=os.environ.get("SUPABASE_SERVICE_KEY")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
row=json.load(urllib.request.urlopen(req))[0]
pd=row["practice_data"]
json.dump(pd, io.open("_L02_6e6b_live.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
out=io.open("_L02_6e6b_report.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
w("TITLE:",row.get("title"),"| slug:",row.get("slug"),"| unit:",row.get("unit_slug"))
w("top keys:",list(pd.keys()))
# compare to shard
shard=json.load(io.open("lesson_higher-calculations-L02@6e6bcbcbc7.json",encoding="utf-8"))
w("shard==live:", json.dumps(shard,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False))
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    w("="*60); w("TIER",tier,"desc:",pb.get(tier+"_description"))
    for i,p in enumerate(pb[tier]):
        w("-"*40)
        w(f"{tier}[{i}] {p.get('display')}")
        w("   sol:",p.get("solutions"),"accept:",p.get("accept"),"unit:",p.get("unit"),"HT:",p.get("higher_only"),"calc:",p.get("calculator"),"it:",p.get("input_type"))
        if p.get("options"): w("   options:",p["options"])
        w("   eqhint:",p.get("equation_hint"),"| hint:",p.get("hint"))
        for j,m in enumerate(p.get("misconceptions") or []):
            w(f"   misc[{j}] {m.get('pattern')} expect={m.get('expect')} :: {m.get('message')}")
        gs=p.get("guided_steps") or []
        for k,s in enumerate(gs):
            if s.get("answer") is not None:
                w(f"     gs[{k}] BOX pre={s.get('pre')!r} post={s.get('post')!r} ans={s.get('answer')} phase={s.get('phase')} hint={s.get('hint')!r} done={s.get('done')!r}")
            else:
                w(f"     gs[{k}] SAY {s.get('say')!r} done={s.get('done')!r}")
out.close()
print("done")
