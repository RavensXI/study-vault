# -*- coding: utf-8 -*-
import json
ID = "a36e47ae-bd22-4127-af9d-5b37e34c0b64"
live = json.load(open("_ADVCHK_L06eq_live.json", encoding="utf-8"))
dump = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# dump may be a list of rows or dict keyed by id
pre = None
if isinstance(dump, list):
    for r in dump:
        if r.get("id")==ID:
            pre = r.get("practice_data"); break
elif isinstance(dump, dict):
    if ID in dump:
        v = dump[ID]
        pre = v.get("practice_data") if isinstance(v,dict) and "practice_data" in v else v
    elif "practice_data" in dump:
        pre = dump["practice_data"]
print("pre found:", pre is not None, "| dump type:", type(dump).__name__,
      "| len:", len(dump) if hasattr(dump,'__len__') else '?')
if pre is None:
    print("keys sample:", list(dump)[:3] if isinstance(dump,dict) else [r.get('id') for r in dump[:3]])
else:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else '*** CHANGED'}")
        if not same:
            print("   PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:300])
            print("   LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:300])
    # Did solutions/displays of problems change? report per problem
    pb_pre = pre.get("problem_bank",{}); pb_live=live.get("problem_bank",{})
    for t in ["bronze","silver","gold"]:
        pp=pb_pre.get(t,[]); pl=pb_live.get(t,[])
        print(f"\n{t}: pre {len(pp)} vs live {len(pl)}")
        for i in range(min(len(pp),len(pl))):
            solp=pp[i].get("solutions"); soll=pl[i].get("solutions")
            if solp!=soll:
                print(f"  {t}[{i}] SOLUTION changed: {solp} -> {soll}")
            # display text (strip svg to compare question core)
            dp=pp[i].get("display",""); dl=pl[i].get("display","")
            import re
            cp=re.sub(r'<svg.*?</svg>','',dp,flags=re.S); cp=re.sub(r'<span.*?</span>','',cp)
            cl=re.sub(r'<svg.*?</svg>','',dl,flags=re.S); cl=re.sub(r'<span.*?</span>','',cl)
            if cp.strip()!=cl.strip():
                print(f"  {t}[{i}] QTEXT changed:\n     PRE : {cp.strip()[:160]}\n     LIVE: {cl.strip()[:160]}")
