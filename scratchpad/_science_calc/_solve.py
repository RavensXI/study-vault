# Independent fresh-solve of every problem + expect reproduction
R=[]
def near(a,b,t): return abs(a-b)<=t

# GOLD
# g0: 2.0g NaOH Mr40 ->200cm3; 25cm3 titre 31.25 vs HCl 1:1 -> conc HCl
n=2.0/40; c_flask=n/0.2; ns=c_flask*0.025; cH=ns/0.03125
R.append(('gold[0]',cH,0.2,None,{1.6:0.05/0.03125}))
# g1: 5.3g Na2CO3 ->250; 25 titre 25 vs HCl 1:2
Mr=2*23+12+3*16; n=5.3/Mr; cf=n/0.25; ns=cf*0.025; nH=ns*2; cH=nH/0.025
R.append(('gold[1]',cH,0.4,None,{0.2:ns/0.025}))
# g2: mass HCl for 250cm3 0.5M ; 1dp
n=0.5*0.25; MrH=36.5; mass=n*MrH
R.append(('gold[2]',round(mass,1),4.6,0.01,{4562.5:0.5*250*36.5, 4.4:round(0.125*35.5,1)}))
# g3: KOH ->500; 25 sample titrated w 20cm3 0.1 HCl 1:1 ; mass KOH Mr56
nH=0.1*0.02; cK=nH/0.025; tot=cK*0.5; mass=tot*56
R.append(('gold[3]',mass,2.24,0.01,{0.112:nH*56}))

# BRONZE
R.append(('bronze[0]',0.1*0.025,0.0025,None,{2.5:0.1*25}))
R.append(('bronze[1]',0.5/0.25,2,None,{0.5:0.25/0.5}))
R.append(('bronze[2]',0.2/0.5,0.4,None,{2.5:0.5/0.2}))
R.append(('bronze[3]',4.0/40,0.1,None,{10:40/4.0}))
R.append(('bronze[4]',0.15/0.5,0.3,None,{0.0003:0.15/500}))
R.append(('bronze[5]',0.25*58.5,14.625,0.01,{0.00427:round(0.25/58.5,5)}))

# SILVER
R.append(('silver[0]',(0.125*0.02)/0.025,0.1,None,{0.125:(0.125*0.02)/0.02}))
R.append(('silver[1]',(0.2*0.025/2)/0.02,0.125,None,{0.25:(0.2*0.025)/0.02}))
R.append(('silver[2]',(0.15*0.025)/0.01875,0.2,None,{0.15:(0.15*0.025)/0.025}))
# s3: NaOH->250;25 titrated 20cm3 0.2 HNO3 1:1; mass NaOH Mr40
nH=0.2*0.02; cN=nH/0.025; tot=cN*0.25; mass=tot*40
R.append(('silver[3]',mass,1.6,None,{0.16:nH*40}))
R.append(('silver[4]',(0.1*0.025*2)/0.02,0.25,None,{0.125:(0.1*0.025)/0.02}))

bad=0
for name,got,stored,acc,expects in R:
    t=acc if acc else 1e-6
    ok=near(got,stored,t)
    if not ok:
        print(f"SOLUTION MISMATCH {name}: computed {got} vs stored {stored} (acc {acc})"); bad+=1
    # expects: must be outside accept window of stored
    win=acc if acc else 0.005
    for exp_stored,exp_calc in expects.items():
        if not near(exp_stored,exp_calc,max(win,0.001)):
            print(f"EXPECT VALUE {name}: stored expect {exp_stored} but committing error gives {exp_calc}"); bad+=1
        if abs(exp_stored-stored)<=win:
            print(f"DEAD EXPECT {name}: expect {exp_stored} inside accept window of {stored} (+/-{win})"); bad+=1
print("Total problems:",len(R),"issues:",bad)
