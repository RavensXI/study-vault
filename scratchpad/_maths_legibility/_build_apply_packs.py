# -*- coding: utf-8 -*-
"""Build apply-packs for the rewrite pass: one per lesson basename, holding the
referenced problems' real walks across all 4 boards + the findings.
    python scratchpad/_maths_legibility/_build_apply_packs.py
An apply-agent reads a pack and returns exact prose-only edits against the real
board data. Board-specific findings match whichever board's text contains them.
"""
import json,io,os,re,collections,urllib.request
S="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE=os.path.dirname(os.path.abspath(__file__))
if sys.platform=="win32" if (sys:=__import__("sys")) else False: os.environ["PYTHONUTF8"]="1"
try: sys.stdout.reconfigure(encoding="utf-8",errors="replace")
except: pass
K=os.environ["SUPABASE_SERVICE_KEY"];H={"apikey":K,"Authorization":"Bearer "+K}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(S+u,headers=H),timeout=120))
def clean(t): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>","",str(t or ""))).strip()
BOARDS=["maths-aqa","maths-edexcel","maths-ocr","maths-eduqas"]
hm=json.load(io.open(os.path.join(HERE,"_all_findings","rewrites_hm.json"),encoding="utf-8"))
# cache: board -> unit -> {lesson_num -> practice_data}
cache={}
def lesson_pd(board,unit,ln):
    if board not in cache:
        sid=get("subjects?slug=eq.%s&select=id"%board)[0]["id"]
        cache[board]={u["slug"]:u["id"] for u in get("units?subject_id=eq.%s&select=id,slug"%sid)}
        cache[board]["_les"]={}
    key=(unit,ln)
    if key not in cache[board]["_les"]:
        uid=cache[board].get(unit)
        if not uid: cache[board]["_les"][key]=None
        else:
            rows=get("lessons?unit_id=eq.%s&lesson_number=eq.%d&select=practice_data"%(uid,ln))
            cache[board]["_les"][key]=rows[0]["practice_data"] if rows else None
    return cache[board]["_les"][key]
outdir=os.path.join(HERE,"_apply_packs"); os.makedirs(outdir,exist_ok=True)
n=0
for base,finds in hm.items():
    m=re.match(r"([a-z\-]+)__L(\d+)",base)
    if not m: continue
    unit,ln=m.group(1),int(m.group(2))
    probs=sorted(set((re.match(r"(bronze|silver|gold)\s*\[?(\d+)\]?",f.get("problem","")).group(1),
                      int(re.match(r"(bronze|silver|gold)\s*\[?(\d+)\]?",f.get("problem","")).group(2)))
                     for f in finds if re.match(r"(bronze|silver|gold)\s*\[?(\d+)\]?",f.get("problem",""))))
    lines=["# apply-pack: %s"%base,"",
           "Return prose-only edits. NEVER change an answer, NEVER add or remove a step.",
           "Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.","",
           "## FINDINGS to address (from readers):"]
    for f in finds:
        lines.append("- [%s] %s | %s | fix: %s"%(f.get("severity"),f.get("problem"),clean(f.get("step"))[:80],clean(f.get("fix"))[:160]))
    lines.append("")
    lines.append("## REAL walk data per board (edit against THIS text):")
    for board in BOARDS:
        pd=lesson_pd(board,unit,ln)
        if not pd: continue
        pb=pd.get("problem_bank") or {}
        shown=False
        for tier,idx in probs:
            items=pb.get(tier) or []
            if idx>=len(items): continue
            p=items[idx]
            if not isinstance(p,dict): continue
            if not shown: lines.append("### board=%s"%board); shown=True
            lines.append("%s[%d] Q: %s"%(tier,idx,clean(p.get("display"))[:90]))
            for si,st in enumerate(p.get("guided_steps") or []):
                if not isinstance(st,dict): continue
                txt=clean(st.get("pre") or st.get("say") or "")
                fld="pre" if st.get("pre") else ("say" if st.get("say") else "?")
                lines.append("   step%d field=%s answer=%s text=%r"%(si,fld,st.get("answer"),txt[:90]))
            lines.append("")
    io.open(os.path.join(outdir,base.replace(".md","")+"__apply.md"),"w",encoding="utf-8").write("\n".join(lines))
    n+=1
print("wrote %d apply-packs to %s"%(n,outdir))
