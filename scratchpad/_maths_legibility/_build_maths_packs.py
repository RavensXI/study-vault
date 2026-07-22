# -*- coding: utf-8 -*-
"""Write one readability pack per maths lesson for a board.
    python scratchpad/_maths_legibility/_build_maths_packs.py maths-aqa
Keeps answers (this is legibility, not correctness). Marks each box's post label
so a reader can see which boxes are already labelled and which are bare.
"""
import io, json, os, re, sys, urllib.request
S="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE=os.path.dirname(os.path.abspath(__file__))
if sys.platform=="win32": os.environ["PYTHONUTF8"]="1"
try: sys.stdout.reconfigure(encoding="utf-8",errors="replace")
except: pass
K=os.environ["SUPABASE_SERVICE_KEY"];H={"apikey":K,"Authorization":"Bearer "+K}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(S+u,headers=H),timeout=120))
def clean(t): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>","",str(t or ""))).strip()
def main(board):
    outdir=os.path.join(HERE,"_packs_%s"%board); os.makedirs(outdir,exist_ok=True)
    sid=get("subjects?slug=eq.%s&select=id"%board)[0]["id"]
    n=0
    for u in get("units?subject_id=eq.%s&select=id,slug"%sid):
        for l in get("lessons?unit_id=eq.%s&select=lesson_number,title,practice_data"%u["id"]):
            pb=(l.get("practice_data") or {}).get("problem_bank") or {}
            if not pb: continue
            n+=1
            lines=["# %s / %s / L%02d - %s"%(board,u["slug"],l["lesson_number"],l["title"]),""]
            for tier in ("bronze","silver","gold"):
                for i,p in enumerate(pb.get(tier,[])):
                    if not isinstance(p,dict): continue
                    lines.append("## %s[%d] (input: %s, main-box unit: %s)"%(tier,i,p.get("input_type"),p.get("unit") or "(none)"))
                    lines.append("Q: "+clean(p.get("display")))
                    for st in p.get("guided_steps") or []:
                        if not isinstance(st,dict): continue
                        if st.get("say"): lines.append("   - intro: "+clean(st["say"]))
                        if st.get("answer") is not None:
                            lab="label:'%s'"%st["post"] if st.get("post") else "NO label"
                            lines.append("   - ask: %s  [box=%s, %s]"%(clean(st.get("pre")),st["answer"],lab))
                    lines.append("")
            io.open(os.path.join(outdir,"%s__L%02d.md"%(u["slug"],l["lesson_number"])),"w",encoding="utf-8").write("\n".join(lines))
    print("wrote %d packs to %s"%(n,outdir))
if __name__=="__main__": main(sys.argv[1])
