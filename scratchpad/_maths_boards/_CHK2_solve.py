# -*- coding: utf-8 -*-
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK2_eduqasL14_live.json"
PRE  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-eduqas.json"
ID   = "15c509ec-bdaf-466b-b9e4-1f1803fc4b3d"

pd = json.load(io.open(LIVE, encoding="utf-8"))["practice_data"]
pre = json.load(io.open(PRE, encoding="utf-8"))
pe = None
if isinstance(pre, list):
    for e in pre:
        if e.get("id")==ID: pe=e
ppd = (pe or {}).get("practice_data", {})

def secdiff_nth(seq):
    # fit an^2+bn+c to first 3 terms
    a1,a2,a3 = seq[0],seq[1],seq[2]
    d1=a2-a1; d2=a3-a2; sd=d2-d1
    a=sd/2
    # a*1+b*1+c... use n=1,2
    # T1=a+b+c, T2=4a+2b+c => T2-T1=3a+b => b=(a2-a1)-3a
    b=(a2-a1)-3*a
    c=a1-a-b
    return a,b,c

pb=pd["problem_bank"]
print("=== SEQUENCE nth-term problems ===")
seqs = {
 "silver[0]": ([3,8,15,24], "n^2+2n"),
 "silver[4]": ([0,3,8,15,24], "n^2-1"),
 "gold[0]": ([2,9,20,35,54], "2n^2+n-1"),
 "gold[4]": ([5,12,23,38], "2n^2+n+2, 10th"),
}
for k,(s,note) in seqs.items():
    a,b,c=secdiff_nth(s)
    print(k, "seq",s,"-> a,b,c=",a,b,c," note:",note)
    if k=="gold[4]":
        t10=a*100+b*10+c
        print("   10th term =",t10)

# Solution comparison live vs pre
print("\n=== solutions: live vs pre ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        pp = ppd.get("problem_bank",{}).get(tier,[])
        pre_sol = pp[i].get("solutions") if i<len(pp) else "N/A"
        if pre_sol != p.get("solutions"):
            print(tier,i,"CHANGED disp:",p['display'][:60],"pre",pre_sol,"now",p.get("solutions"))
print("(any CHANGED lines above are solution edits vs pre-dump)")

# check pre displays match live displays (were problems reworded?)
print("\n=== displays changed vs pre ===")
for tier in ("bronze","silver","gold"):
    pp = ppd.get("problem_bank",{}).get(tier,[])
    for i,p in enumerate(pb[tier]):
        if i<len(pp):
            pd_disp = pp[i].get("display","")
            # strip svg for compare
            def strip(s):
                import re; return re.sub("<svg.*?</svg>","",s,flags=re.S)
            if strip(pd_disp)!=strip(p.get("display","")):
                print(tier,i,"disp changed")
                print("  PRE:",strip(pd_disp)[:100])
                print("  NOW:",strip(p.get('display',''))[:100])
