import json,sys
sys.stdout.reconfigure(encoding="utf-8")
pre=json.load(open("_ck3_pre_pd.json",encoding="utf-8"))
now=json.load(open("_ck3_L03_live.json",encoding="utf-8"))
print("PRE keys",list(pre.keys()))
for k in ("related_videos","topic_links","worked_examples"):
    print(k, "SAME" if pre.get(k)==now.get(k) else "*** DIFFERENT ***")
    if pre.get(k)!=now.get(k):
        print("  pre:",json.dumps(pre.get(k),ensure_ascii=False)[:1500])
        print("  now:",json.dumps(now.get(k),ensure_ascii=False)[:1500])
pb0=pre["problem_bank"]; pb1=now["problem_bank"]
for t in ("bronze","silver","gold"):
    a,b=pb0[t],pb1[t]
    print("###",t,len(a),len(b))
    for i in range(max(len(a),len(b))):
        pa=a[i] if i<len(a) else {}
        pb=b[i] if i<len(b) else {}
        for k in ("display","solutions","options","input_type","unit","image","chart","ruler","calculator"):
            va,vb=pa.get(k),pb.get(k)
            if va!=vb:
                print(" %s[%d].%s"%(t,i,k))
                print("   PRE:",json.dumps(va,ensure_ascii=False)[:900])
                print("   NOW:",json.dumps(vb,ensure_ascii=False)[:900])
        extra_pre=[k for k in pa if k not in pb]
        if extra_pre: print(" %s[%d] KEYS DROPPED: %s"%(t,i,extra_pre))
print("--- method_card PRE:"); print(json.dumps(pre.get("method_card"),ensure_ascii=False)[:2500])
print("--- tier_guides PRE keys:", list((pre.get("tier_guides") or {}).keys()))
