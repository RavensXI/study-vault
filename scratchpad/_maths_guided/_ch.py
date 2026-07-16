import json,io,sys,glob
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
for f in glob.glob("changes_*.json"):
    if "L12" in f or "l12" in f:
        print("==",f)
        print(open(f,encoding="utf-8").read())
