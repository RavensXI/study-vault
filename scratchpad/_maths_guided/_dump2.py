import json, io, sys
d = json.load(open("_CHK_geomL01_live.json",encoding="utf-8"))
pd = d["practice_data"]
pb = pd["problem_bank"]
out = io.open("_dump2_out.txt","w",encoding="utf-8")
def w(s): out.write(s+"\n")
# check for replacement char
raw = open("_CHK_geomL01_live.json",encoding="utf-8").read()
w("REPL CHARS U+FFFD count: %d" % raw.count("�"))
w("degree ° count: %d" % raw.count("°"))
for t in ["bronze","silver","gold"]:
    w("\n########## "+t.upper())
    for i,p in enumerate(pb.get(t,[])):
        w("\n=== %s[%d] sol=%s ==="%(t,i,p.get("solutions")))
        w("DISPLAY: "+p.get("display",""))
        w("HINT: "+str(p.get("hint","")))
out.close()
print("done")
