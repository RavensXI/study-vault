# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_ratio-proportion-L03.json", encoding="utf-8"))
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        opts = p["options"]
        assert p["solutions"] == [0], (tier,i,p["solutions"])
        line = f"{tier}[{i}] correct={opts[0]!r}"
        for j,m in enumerate(p.get("misconceptions") or []):
            e = m["expect"]
            tgt = opts[e] if isinstance(e,int) else "null"
            line += f" | m{j}({m.get('pattern')}) expect={e}->{tgt}"
        print(line)
