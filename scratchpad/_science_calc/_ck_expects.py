import json
pd=json.load(open('_ck_canonical_live.json',encoding='utf-8'))
pb=pd['problem_bank']
# manual reproduction table: (tier,i,pattern,expect,my_wrong_value)
rep={
 ('bronze',0,'inverse_ratio'):230*1000/50,        #4600
 ('bronze',1,'wrong_rearrange'):460*230/12,        #8816.67
 ('bronze',2,'inverse_ratio'):25*500/2000,         #6.25
 ('bronze',3,'inverse_ratio'):240*1200/60,         #4800
 ('bronze',4,'wrong_rearrange'):400*230/11.5,      #8000
 ('bronze',6,'inverse_ratio'):120*600/300,         #240
 ('silver',0,'wrong_rearrange'):230*4/11.5,        #80
 ('silver',1,'inverse_error'):20*20,               #400
 ('silver',2,'wrong_rearrange'):23*0.5/... if False else 23/115,  #0.2
 ('silver',3,'wrong_rearrange'):5000*11000/220,    #250000
 ('silver',4,'wrong_rearrange'):11000*40/220,      #2000
 ('silver',5,'wrong_rearrange'):6*2*0.1,           #1.2
 ('gold',0,'forgot_square'):62.5*10/1000,          #0.625 kW
 ('gold',1,'forgot_square'):1000*10/1e6,           #0.01 MW
 ('gold',2,'inverse_error'):60/48*100,             #125
 ('gold',3,'wrong_rearrange'):36*9/230,            #1.409
 ('gold',4,'wrong_rearrange'):500*25000/400000,    #31.25
 ('gold',5,'forgot_efficiency'):460/20,            #23
}
bad=0
for t in ('bronze','silver','gold'):
    for i,pr in enumerate(pb[t]):
        sol=pr.get('solutions',[None])[0]
        acc=pr.get('accept',0.005)
        for m in pr.get('misconceptions',[]):
            exp=m.get('expect')
            pat=m.get('pattern')
            key=(t,i,pat)
            mine=rep.get(key)
            if exp is None:
                tag="null(ok)"
            else:
                # inside accept window of correct?
                inside = (isinstance(sol,(int,float)) and abs(exp-sol)<=acc)
                match = (mine is not None and abs(mine-exp)<0.01)
                tag=("MATCH" if match else ("mine=%s"%mine)) + (" INSIDE-WINDOW!!" if inside else "")
                if inside or (mine is not None and not match): bad+=1
            print(f"{t}[{i}] {pat} expect={exp} sol={sol} acc={acc} -> {tag}")
print("BAD:",bad)
