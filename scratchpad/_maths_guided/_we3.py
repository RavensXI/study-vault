import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre = json.load(open("_pre_L12.json",encoding="utf-8"))
live = json.load(open("_live_L12.json",encoding="utf-8"))
sa=pre["worked_examples"][0]["steps"][0]["content"]
sb=live["worked_examples"][0]["steps"][0]["content"]
print("pre codes:",[hex(ord(c)) for c in sa if ord(c)>127])
print("live codes:",[hex(ord(c)) for c in sb if ord(c)>127])
print("equal?",sa==sb, len(sa),len(sb))
# find first diff pos
for i,(x,y) in enumerate(zip(sa,sb)):
    if x!=y:
        print("first diff at",i,repr(x),repr(y)); break
