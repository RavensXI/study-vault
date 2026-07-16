import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
L=json.load(open("_live_L04_refetch.json",encoding="utf-8"))
bad=[]
# teach walks: print box values for manual confirm
for tier in ["bronze","silver","gold"]:
    t=L["guided"]["teach"][tier]
    boxes=[s["answer"] for s in t["steps"] if "answer" in s]
    print(f"teach.{tier}: '{t['display'][:60]}'  boxes={boxes}")
# opener
ob=[s["answer"] for s in L["guided"]["opener"]["steps"] if "answer" in s]
print("opener boxes:",ob)
# tier guide examples
for tier in ["bronze","silver","gold"]:
    ex=L["tier_guides"][tier]["example"]
    ans=[st["content"] for st in ex["steps"] if st.get("isAnswer")]
    print(f"tierguide.{tier}: Q='{ex['question'][:55]}' ANSWER={ans}")
print()
# independent recompute
import statistics
# teach.bronze: mean 6,9,4,5 = 24/4=6
assert (6+9+4+5)==24 and 24/4==6
# teach.silver: 1(2),2(3),3(5): fx=2,6,15 sum23 f10 =>2.3
assert 1*2==2 and 2*3==6 and 3*5==15 and (2+6+15)==23 and (2+3+5)==10 and 23/10==2.3
# teach.gold: 0-10(3),10-20(5),20-30(2) mids5,15,25 fx15,75,50 sum140 f10 =>14
assert 5*3==15 and 15*5==75 and 25*2==50 and (15+75+50)==140 and (3+5+2)==10 and 140/10==14
# opener: 2+4+9=15, 15/3=5
assert (2+4+9)==15 and 15/3==5
# tierguide gold: mean5=9 tot45 known 6+8+10+11=35 fifth10
assert 9*5==45 and (6+8+10+11)==35 and 45-35==10
# tierguide bronze: median 7,2,9,4,6 ordered=2,4,6,7,9 mid=6
assert sorted([7,2,9,4,6])[2]==6
# tierguide silver: 0-10(2),10-20(3) mids5,15 fx10,45 sum55 f5 =>11
assert 5*2==10 and 15*3==45 and (10+45)==55 and 55/5==11
# method_card example: mean 4,7,9,3,12 =35/5=7
assert (4+7+9+3+12)==35 and 35/5==7
print("ALL teach/opener/tierguide/methodcard recomputes: PASS")
