# -*- coding: utf-8 -*-
from fractions import Fraction as F
# fresh-solve every displayed problem; compare to stored [num,den]
probs = {
 "bronze":[
  ("1/4+1/3", F(1,4)+F(1,3), [7,12]),
  ("3/5+1/10", F(3,5)+F(1,10), [7,10]),
  ("5/6-1/3", F(5,6)-F(1,3), [1,2]),
  ("7/8-1/4", F(7,8)-F(1,4), [5,8]),
  ("2/3*3/5", F(2,3)*F(3,5), [2,5]),
  ("1/2*4/7", F(1,2)*F(4,7), [2,7]),
  ("3/4÷1/2", F(3,4)/F(1,2), [3,2]),
  ("2/5÷4/5", F(2,5)/F(4,5), [1,2]),   # duplicate of 5/6-1/3 -> will change
 ],
 "silver":[
  ("2/3+5/8", F(2,3)+F(5,8), [31,24]),
  ("5/6-3/8", F(5,6)-F(3,8), [11,24]),
  ("1 1/3+2 1/4", F(4,3)+F(9,4), [43,12]),
  ("3 1/2-1 2/3", F(7,2)-F(5,3), [11,6]),
  ("3/4*8/9", F(3,4)*F(8,9), [2,3]),
  ("2 1/5*5/11", F(11,5)*F(5,11), [1,1]),
  ("1 3/4÷7/8", F(7,4)/F(7,8), [2,1]),
 ],
 "gold":[
  ("2/3+3/4-1/6", F(2,3)+F(3,4)-F(1,6), [5,4]),
  ("2 2/3*1 1/4", F(8,3)*F(5,4), [10,3]),
  ("4 1/5÷1 2/5", F(21,5)/F(7,5), [3,1]),
  ("5/6÷2/3+1/4", F(5,6)/F(2,3)+F(1,4), [3,2]),
  ("3/7*14/9÷2/3", F(3,7)*F(14,9)/F(2,3), [1,1]),
 ],
}
for tier,ps in probs.items():
  seen={}
  for i,(disp,val,stored) in enumerate(ps):
    got=[val.numerator, val.denominator]
    ok = got==stored
    print(f"{tier}[{i}] {disp} = {val}  got{got} stored{stored} {'OK' if ok else 'MISMATCH'}")
    seen.setdefault(tuple(stored),[]).append(i)
  dups={k:v for k,v in seen.items() if len(v)>1}
  if dups: print(f"  !! DUP in {tier}: {dups}")
# proposed replacement for bronze[7]
print("REPLACE bronze[7]: 2/5 ÷ 3/5 =", F(2,5)/F(3,5))
