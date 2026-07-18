import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
print("len",len(pre),"sample item keys:",list(pre[0].keys()) if pre else None)
row=[r for r in pre if r.get('id')==cid]
print("matches:",len(row))
if row:
    r=row[0]
    ppd=r.get('practice_data') or {}
    print("pre practice_data keys:",list(ppd.keys()))
    pb=ppd.get('problem_bank',{})
    print("pre bank sizes:",{k:len(v) for k,v in pb.items() if isinstance(v,list)})
    import json as J
    pd=J.load(open('_chk689_live.json',encoding='utf-8'))
    for f in ['worked_examples','related_videos','topic_links','exam_context']:
        same=J.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==J.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    # bank display/solutions preservation
    for t in ['bronze','silver','gold']:
        opb=pb.get(t,[]); npb=pd['problem_bank'][t]
        print(f"bank {t}: pre={len(opb)} now={len(npb)}")
        for i in range(min(len(opb),len(npb))):
            if opb[i].get('solutions')!=npb[i].get('solutions'):
                print(f"  SOL CHANGED {t}[{i}]: {opb[i].get('solutions')}->{npb[i].get('solutions')}")
            if opb[i].get('display')!=npb[i].get('display'):
                print(f"  DISPLAY CHANGED {t}[{i}]")
            if opb[i].get('accept')!=npb[i].get('accept'):
                print(f"  ACCEPT CHANGED {t}[{i}]: {opb[i].get('accept')}->{npb[i].get('accept')}")
            if opb[i].get('unit')!=npb[i].get('unit'):
                print(f"  UNIT CHANGED {t}[{i}]: {opb[i].get('unit')}->{npb[i].get('unit')}")
            if opb[i].get('higher_only')!=npb[i].get('higher_only'):
                print(f"  HIGHER_ONLY CHANGED {t}[{i}]: {opb[i].get('higher_only')}->{npb[i].get('higher_only')}")
