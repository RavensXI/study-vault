# Fresh-solve every problem from display + chart data. Report mismatches.
import json, io
live=json.load(io.open("_L05e_live.json",encoding="utf-8"))
pb=live["practice_data"]["problem_bank"]

def interp_read(xs, cf, target_cf):
    # find x where cf == target_cf by linear interpolation
    for i in range(1,len(cf)):
        if cf[i-1] <= target_cf <= cf[i]:
            if cf[i]==cf[i-1]: return xs[i-1]
            f=(target_cf-cf[i-1])/(cf[i]-cf[i-1])
            return xs[i-1]+f*(xs[i]-xs[i-1])
    return None

reports=[]
# BRONZE
b=pb["bronze"]
# B1 median CF 60
c=b[0]["chart"]["data"]; xs=c["labels"]; cf=c["datasets"][0]["data"]
reports.append(("B1 median n/2=30", interp_read(xs,cf,30), b[0]["solutions"]))
# B2 IQR boxplot
d=b[1]["chart"]["data"]["datasets"][0]["data"][0]
reports.append(("B2 IQR", d["q3"]-d["q1"], b[1]["solutions"], "range=",d["max"]-d["min"]))
# B3 median boxplot
d=b[2]["chart"]["data"]["datasets"][0]["data"][0]
reports.append(("B3 median", d["median"], b[2]["solutions"]))
# B4 Q1 CF 80
c=b[3]["chart"]["data"]; xs=c["labels"]; cf=c["datasets"][0]["data"]
reports.append(("B4 Q1 n/4=20 [ORIG cf]", interp_read(xs,cf,20), b[3]["solutions"], "cf=",cf))
# B5 range boxplot
d=b[4]["chart"]["data"]["datasets"][0]["data"][0]
reports.append(("B5 range", d["max"]-d["min"], b[4]["solutions"], "iqr=",d["q3"]-d["q1"]))
# B6 freq=FD*w 5*4
reports.append(("B6 5*4", 5*4, b[5]["solutions"]))
# B7 FD=24/8
reports.append(("B7 24/8", 24/8, b[6]["solutions"]))
# B8 IQR 50-30
reports.append(("B8 50-30", 50-30, b[7]["solutions"]))
# SILVER
s=pb["silver"]
# S1 MC consistency: IQR Y10 vs Y11
d=s[0]["chart"]["data"]["datasets"][0]["data"]
reports.append(("S1 IQR Y10,Y11", d[0]["q3"]-d[0]["q1"], d[1]["q3"]-d[1]["q1"], "ans idx",s[0]["solutions"]))
# S2 between 30 and 60, 120
c=s[1]["chart"]["data"]; xs=c["labels"]; cf=c["datasets"][0]["data"]
cf60=cf[xs.index(60)]; cf30=cf[xs.index(30)]
reports.append(("S2 cf60-cf30", cf60-cf30, s[1]["solutions"]))
# S3 hist freq 10-20 FD4 w10
reports.append(("S3 4*10", 4*10, s[2]["solutions"]))
# S4 IQR 62-35
reports.append(("S4 62-35", 62-35, s[3]["solutions"]))
# S5 total freq
reports.append(("S5 total", 3*5+5*5+4*10+1*20, s[4]["solutions"]))
# S6 MC
reports.append(("S6 A med60 iqr15 vs B med55 iqr25 -> idx", s[5]["solutions"]))
# S7 above70 200-150
reports.append(("S7 200-150", 200-150, s[6]["solutions"]))
# GOLD
g=pb["gold"]
# G1 hist 15-25: bars labels/fd
c=g[0]["chart"]["data"]; print("G1 labels",c["labels"],"fd",c["datasets"][0]["data"])
reports.append(("G1 15-20:4*5 +20-25:3*5", 4*5+3*5, g[0]["solutions"], "calc",g[0]["calculator"]))
# G2 pass mark 80% pass -> cf=20
c=g[1]["chart"]["data"]; xs=c["labels"]; cf=c["datasets"][0]["data"]
reports.append(("G2 read cf=20 x=", interp_read(xs,cf,20), g[1]["solutions"]))
# G3 modal class MC: FD 2,4,8,1.5 -> 25-30
reports.append(("G3 modal highest FD=8 -> idx", g[2]["solutions"]))
# G4 median class: freqs 3*20,5*10,2*20 =60,50,40 total150 med75.5th
reports.append(("G4 freqs",[3*20,5*10,2*20],"total",150,"-> idx",g[3]["solutions"]))
# G5 boxplot median diff
d=g[4]["chart"]["data"]["datasets"][0]["data"]
reports.append(("G5 B-A median", d[1]["median"]-d[0]["median"], g[4]["solutions"]))

for r in reports: print(r)
