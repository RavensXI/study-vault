import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
live=json.load(open('_live_ratio_L01.json',encoding='utf-8'))
# For share-a-total problems: check if total/target_ratio_number == correct share (degenerate shortcut)
cases=[
 ("silver[0]","Share 450 in 2:3:4 middle",450,[2,3,4],3,150),
 ("bronze[0]","Share 100 in 3:2 larger",100,[3,2],3,60),
 ("bronze[6]","Share 72 in 5:3:1 largest",72,[5,3,1],5,40),
 ("silver[0b]","alt largest check",450,[2,3,4],4,200),
]
for name,desc,total,parts,tgt,correct in cases:
    tp=sum(parts)
    proper=total/tp*tgt
    shortcut=total/tgt
    flag="DEGENERATE (shortcut==answer)" if abs(shortcut-proper)<1e-9 else "ok"
    print(f"{name}: proper={proper} shortcut(total/{tgt})={shortcut} correct_stored={correct} -> {flag}")
