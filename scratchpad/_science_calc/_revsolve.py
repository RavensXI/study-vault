# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open("lesson_physics-calculations-L01@087ba4e3f7.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for idx,p in enumerate(pb[tier]):
        disp=p.get("display","")
        sol=p.get("solutions")
        acc=p.get("accept")
        unit=p.get("unit")
        ho=p.get("higher_only")
        print(f"{tier}[{idx}] sol={sol} unit={unit!r} accept={acc} HO={ho}")
        print("     ", disp[:100])
