import os, json, urllib.request, io
ID="a769c80a-697d-4ae1-a042-6299738f9021"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
with io.open("_diag_L12_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
out=[]
out.append("keys: "+", ".join(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    probs=pb.get(t,[])
    out.append(f"--- {t}: {len(probs)} problems ---")
    for i,p in enumerate(probs):
        out.append(f"[{t}][{i}] input={p.get('input_type')} chart={'Y' if p.get('chart') else '-'} svg={'Y' if '<svg' in str(p.get('display','')) else '-'}")
        out.append("   disp: "+str(p.get('display',''))[:200].replace(chr(10),' '))
with io.open("_diag_L12_summary.txt","w",encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
