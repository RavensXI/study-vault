import json, io, os, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SB=os.environ["SUPABASE_URL"].rstrip("/"); KEY=os.environ["SUPABASE_SERVICE_KEY"]
HDR={"apikey":KEY,"Authorization":"Bearer "+KEY}
COLS=("id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,"
      "practice_questions,knowledge_checks,flashcard_questions,glossary_terms,narration_manifest")
req=urllib.request.Request(SB+"/rest/v1/lessons?unit_id=eq.170f32cc-ff7e-4ae6-8376-3dd18d1208f4&select=%s&order=lesson_number"%COLS,headers=HDR)
now={r["lesson_number"]:r for r in json.loads(urllib.request.urlopen(req,timeout=60).read().decode())}
pre={r["lesson_number"]:r for r in json.load(io.open("_live.json",encoding="utf-8"))}
STR=["description","content_html","exam_tip_html","conclusion_html"]
JS=["practice_questions","knowledge_checks","flashcard_questions","glossary_terms"]
ENT=re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#\d{1,7}|#[xX][0-9a-fA-F]{1,6});")
fails=[]
for n in sorted(now):
    a,b=pre[n],now[n]
    ida=[m for m in re.findall(r'data-narration-id="([^"]+)"',(a["content_html"] or "")+(a["exam_tip_html"] or "")+(a["conclusion_html"] or ""))]
    idb=[m for m in re.findall(r'data-narration-id="([^"]+)"',(b["content_html"] or "")+(b["exam_tip_html"] or "")+(b["conclusion_html"] or ""))]
    if ida!=idb: fails.append("L%d narration ids changed"%n)
    ma=[e["id"] for e in (a["narration_manifest"] or [])]; mb=[e["id"] for e in (b["narration_manifest"] or [])]
    if ma!=mb: fails.append("L%d manifest ids changed"%n)
    for k in JS:
        if len(a[k] or [])!=len(b[k] or []): fails.append("L%d %s length changed"%(n,k))
    for kc in (b["knowledge_checks"] or []):
        if "answers" in kc: fails.append("L%d KC has answers[]"%n)
        if kc.get("type") in ("mcq","fill"):
            if "correct" not in kc or "options" not in kc: fails.append("L%d KC missing correct/options"%n)
            elif not (0<=kc["correct"]<len(kc["options"])): fails.append("L%d KC correct out of range"%n)
    for pq in (b["practice_questions"] or []):
        tot=sum(int(x) for x in re.findall(r"AO\d \((\d+) marks\)",pq.get("marks") or ""))
        if "30 marks" in (pq.get("type") or "") and tot!=30: fails.append("L%d PQ marks sum %d"%(n,tot))
    for f in JS+["description"]:
        v=b.get(f); blob=v if isinstance(v,str) else json.dumps(v,ensure_ascii=False)
        if v is not None and ENT.search(blob or ""): fails.append("L%d %s entity"%(n,f))
    # dfn terms still resolvable
    for dfn in re.findall(r'<dfn class="term" data-def="[^"]*">([^<]+)</dfn>',b["content_html"] or ""):
        pass
print("manifest sizes:", {n:len(now[n]["narration_manifest"] or []) for n in sorted(now)})
print("suspect scan:")
SUS=["despair to joy","grief into joy","grief to joy","synaesthesia","moonlit","Day Lewis",
     "others may print neither","open book","We stood by a pond that winter day,\u201d",
     "Mew's 'The Farmer's Bride' (circular"]
for n in sorted(now):
    blob="".join((now[n].get(f) or "") for f in STR)+json.dumps([now[n].get(f) for f in JS],ensure_ascii=False)
    hit=[s for s in SUS if s in blob]
    if hit: print("  L%d: %s"%(n,hit)); fails.append("L%d suspect %s"%(n,hit))
print("new-reading present:")
for n,s in [(1,"Rather, instantly / Renew thy presence"),(8,"Rather, instantly / Renew thy presence"),
            (3,"signal tapped out along a wire"),(4,"closing dialogue"),(6,"Anchor. Kite."),
            (7,"closed book</strong> throughout"),(8,"AQA prints the named poem")]:
    blob="".join((now[n].get(f) or "") for f in STR)+json.dumps([now[n].get(f) for f in JS],ensure_ascii=False)
    ok = s in blob
    print("  L%d %-42s %s"%(n,s[:42],"OK" if ok else "MISSING"))
    if not ok: fails.append("L%d missing %s"%(n,s))
print("\nFAILS:", fails if fails else "none")
