import json
changes={
  "key":"geometry-L06",
  "figures_added":[
    {"tier":"silver","index":0,"kind":"svg",
     "what":"Relocated the 75 degree angle arc and label from vertex P2 (bottom-right, drawn 65 deg) to vertex P1 (bottom-left, the real 75 deg vertex, opposite the labelled side b). New arc M96.7 141.0 A16 16 0 0 0 84.9 125.6 with label at (102.5,126.5). Figure now shows angle B=75 deg opposite side b, consistent with the sine rule. Geometry, side/label positions, and the 40 deg apex marker were already correct and left unchanged."}
  ],
  "opener_touched":False,
  "notes":"Single-defect diagram-pass revision. Checker FAIL was a mislabelled corner only (figure geometry P1=75, P2=65, P3=40 already correct). Removed the 75 deg arc/text at P2 and drew the equivalent arc/text at P1 so the 75 deg marker is opposite side b. No question text, solutions, guided_steps, misconceptions, or other figures touched. Validator PASS; PATCHed live and verified (204)."
}
json.dump(changes, open("changes_geometry-L06_diagrams.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote changes_geometry-L06_diagrams.json")
